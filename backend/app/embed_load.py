#!/usr/bin/env python3
"""
Embed loader: reads a normalized text file, splits into pages,
generates embeddings via OpenAI, and writes to Cassandra.
"""
import os
import re
import sys
import argparse

from dotenv import load_dotenv
import openai
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement, ConsistencyLevel

# Regex to split pages: captures page number, allow optional whitespace
PAGE_SPLIT_REGEX = re.compile(r"###Page\s*(\d+)###")
STORY_ID = 'an_author_preface'

def load_pages(text):
    parts = PAGE_SPLIT_REGEX.split(text)
    pages = []
    # parts: [prefix, '1', page1, '2', page2, ...]
    for i in range(1, len(parts), 2):
        page_num = int(parts[i])
        content = parts[i+1].strip()
        pages.append((page_num, content))
    return pages

def main():
    parser = argparse.ArgumentParser(description="Embed loader for Cassandra pages table")
    parser.add_argument('--dry-run', action='store_true', help='skip DB writes')
    parser.add_argument('--input_file', required=True, help='path to input text file')
    args = parser.parse_args()

    print(f"[embed_load] Starting with input_file={args.input_file}, dry_run={args.dry_run}")

    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print('OPENAI_API_KEY not set', file=sys.stderr)
        sys.exit(1)
    openai.api_key = api_key

    # Read and split pages
    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f'File not found: {args.input_file}', file=sys.stderr)
        sys.exit(1)
    pages = load_pages(text)
    total = len(pages)
    print(f"[embed_load] Found {total} pages after splitting")
    if args.dry_run:
        # Dry-run: count and sample pages
        print(f'Found {total} pages. Dry-run: no writes.')
        for page_num, content in pages[:3]:
            print(f'Page {page_num}: length={len(content)}')
        sys.exit(0)

    # Cassandra setup and processing with safe shutdown
    cass_host = os.getenv('CASS_HOST', 'localhost')
    cass_keyspace = os.getenv('CASS_KEYSPACE', 'gibsey')
    cluster = Cluster([cass_host])
    session = None
    try:
        session = cluster.connect()
        session.set_keyspace(cass_keyspace)
        insert_stmt = session.prepare(
            'INSERT INTO pages (story_id, page_num, html, embedding) VALUES (?, ?, ?, ?)'
        )

        # Process in batches of 25
        batch_size = 25
        for start in range(0, total, batch_size):
            chunk = pages[start:start + batch_size]
            batch = BatchStatement(consistency_level=ConsistencyLevel.LOCAL_QUORUM)
            for page_num, content in chunk:
                # Generate embedding
                resp = openai.Embedding.create(
                    model='text-embedding-3-small',
                    input=content
                )
                # Extract embedding from legacy response
                embedding = resp['data'][0]['embedding']
                batch.add(insert_stmt, (STORY_ID, page_num, content, embedding))
                # Add to HNSW index
                import ann_hnsw
                int_id = ann_hnsw.pack_id(STORY_ID, page_num)
                ann_hnsw.add(embedding, int_id)
            session.execute(batch)
            print(f'Inserted batch {start+1}-{start+len(chunk)} of {total} pages')

        import ann_hnsw
        ann_hnsw.save()
        print(f'Done: inserted {total} pages + hnsw index saved')
    finally:
        if session:
            try:
                session.shutdown()
            except Exception:
                pass
        cluster.shutdown()

if __name__ == '__main__':
    main()