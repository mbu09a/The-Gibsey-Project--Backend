#!/usr/bin/env python3
"""
Load text files into Cassandra with embeddings.
Used to seed book2.txt and book3.txt with page-level embeddings.
"""
import argparse
import os
import sys
from typing import List

import openai
from dotenv import load_dotenv
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_cassandra_session():
    """Connect to Cassandra."""
    cass_host = os.getenv("CASS_HOST", "localhost")
    cass_keyspace = os.getenv("CASS_KEYSPACE", "gibsey")
    cluster = Cluster([cass_host])
    return cluster.connect(cass_keyspace)

def load_text_file(file_path: str, story_id: str, batch_size: int = 10):
    """Load a text file into Cassandra."""
    # Parse the input file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into pages (assuming the format is similar to cleaned_normalised.txt)
    pages = content.split('===')
    if pages and pages[0].strip() == '':
        pages = pages[1:]
    
    print(f"Found {len(pages)} pages in {file_path}")
    
    # Connect to Cassandra
    session = get_cassandra_session()
    
    # Prepare the insert statement
    insert_stmt = session.prepare(
        'INSERT INTO pages (story_id, page_num, html, embedding) VALUES (?, ?, ?, ?)'
    )
    
    # Process pages in batches to avoid rate limits
    for i in range(0, len(pages), batch_size):
        batch = pages[i:i+batch_size]
        print(f"Processing batch {i//batch_size + 1}/{(len(pages)-1)//batch_size + 1}")
        
        # Create batch for Cassandra
        cassandra_batch = BatchStatement()
        
        for j, page in enumerate(batch):
            page_num = i + j + 1
            
            # Clean the page content
            page_content = page.strip()
            if not page_content:
                continue
            
            # Get embedding for the page
            try:
                resp = openai.Embedding.create(
                    model="text-embedding-3-small",
                    input=page_content
                )
                embedding = resp["data"][0]["embedding"]
                
                # Add to batch
                cassandra_batch.add(insert_stmt, (story_id, page_num, page_content, embedding))
                print(f"  Processed page {page_num}")
                
            except Exception as e:
                print(f"Error processing page {page_num}: {e}")
        
        # Execute batch
        session.execute(cassandra_batch)
        print(f"Inserted batch {i//batch_size + 1}")

def main():
    parser = argparse.ArgumentParser(description='Load text files into Cassandra with embeddings')
    parser.add_argument('--input_file', required=True, help='Path to the input text file')
    parser.add_argument('--story_id', required=True, help='Story ID')
    parser.add_argument('--batch_size', type=int, default=10, help='Batch size for processing')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_file):
        print(f"Error: Input file {args.input_file} not found")
        sys.exit(1)
    
    load_text_file(args.input_file, args.story_id, args.batch_size)
    print(f"Successfully loaded {args.input_file} into Cassandra with story_id={args.story_id}")

if __name__ == "__main__":
    main() 