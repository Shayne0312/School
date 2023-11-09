-- from the terminal run:
-- psql < craigslist.sql

-- Table of Contents
-- 1. Drop existing database and tables
-- 2. Create tables
-- 3. Create indexes  
-- 4. Insert sample data

-- 1. Drop existing database and tables
DROP DATABASE IF EXISTS craigslist;
CREATE DATABASE craigslist;
\c craigslist;

-- 2. Create tables
CREATE TABLE regions (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE 
);

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  preferred_region_id INTEGER REFERENCES regions(id) 
);

CREATE TABLE categories (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE posts (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  text TEXT,
  user_id INTEGER REFERENCES users(id),
  location TEXT,
  region_id INTEGER REFERENCES regions(id) 
);

CREATE TABLE post_categories (
  post_id INTEGER REFERENCES posts(id),
  category_id INTEGER REFERENCES categories(id),
  PRIMARY KEY (post_id, category_id)
);

-- 3. Create indexes
CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_posts_region_id ON posts(region_id);
CREATE INDEX idx_post_categories_post_id ON post_categories(post_id);
CREATE INDEX idx_post_categories_category_id ON post_categories(category_id);

-- *1. Add default values
ALTER TABLE posts ALTER COLUMN text SET DEFAULT '';
ALTER TABLE posts ALTER COLUMN location SET DEFAULT '';

-- *2. Add validation constraints
ALTER TABLE regions ADD CONSTRAINT regions_name_length CHECK (LENGTH(name) <= 100);
ALTER TABLE users ADD CONSTRAINT users_name_length CHECK (LENGTH(name) <= 100);
ALTER TABLE posts ADD CONSTRAINT posts_title_length CHECK (LENGTH(title) <= 200);

-- 4. Insert sample data
INSERT INTO regions (name) VALUES ('Region 1'), ('Region 2');

INSERT INTO categories (name) VALUES ('Category 1'), ('Category 2');

INSERT INTO users (name, preferred_region_id) VALUES ('User 1', 1), ('User 2', 2);

INSERT INTO posts (title, text, user_id, location, region_id) VALUES ('Post 1', 'Text 1', 1, 'Location 1', 1), ('Post 2', 'Text 2', 2, 'Location 2', 2);

INSERT INTO post_categories (post_id, category_id) VALUES (1, 1), (2, 2);