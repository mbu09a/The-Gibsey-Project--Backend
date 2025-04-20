-- Keyspace
CREATE KEYSPACE IF NOT EXISTS gibsey
  WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE gibsey;

-- Table to hold your pages + future embeddings
CREATE TABLE IF NOT EXISTS pages (
  story_id text,
  page_num int,
  html text,
  embedding vector<float, 1536>,
  PRIMARY KEY (story_id, page_num)
);

-- Create the stories table
CREATE TABLE IF NOT EXISTS gibsey.stories (
  story_id text PRIMARY KEY
);

-- Create the bots table
CREATE TABLE IF NOT EXISTS gibsey.bots (
  bot_id text PRIMARY KEY
);

-- Create the vault table
CREATE TABLE IF NOT EXISTS gibsey.vault (
  user_id text,
  ts timestamp,
  PRIMARY KEY ((user_id), ts)
);