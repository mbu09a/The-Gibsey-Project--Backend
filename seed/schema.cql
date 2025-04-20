-- gibsey keyspace and pages table with vector column for C* 4.x + Stargate v2
CREATE KEYSPACE IF NOT EXISTS gibsey WITH replication = {'class':'SimpleStrategy','replication_factor':1};
USE gibsey;

CREATE TABLE IF NOT EXISTS pages (
    story_id  text,
    page_num  int,
    html      text,
    embedding list<float>,
    PRIMARY KEY ((story_id), page_num)
);

-- SAI index is not available in this Cassandra version, using query-time vector similarity instead
-- CREATE CUSTOM INDEX IF NOT EXISTS pages_embedding_idx 
-- ON pages(embedding) 
-- USING 'StorageAttachedIndex'
-- WITH OPTIONS = {
--   'similarity_function':'cosine',
--   'embedding_dimension':'1536'
-- };

CREATE TABLE IF NOT EXISTS stories (
  story_id text PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS bots (
  bot_id text PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS vault (
  user_id text,
  ts      timestamp,
  PRIMARY KEY (user_id, ts)
); 