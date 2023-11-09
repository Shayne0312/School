# Craigslist Database Setup

This repository contains the necessary SQL code to set up a PostgreSQL database for a simplified version of Craigslist. The code creates tables for regions, users, categories, posts, and post_categories, and includes sample data to populate the tables.

## Table of Contents

1. [Database Setup](#database-setup)
   - [Drop Existing Database and Tables](#drop-existing-database-and-tables)
   - [Create Tables](#create-tables)
   - [Create Indexes](#create-indexes)
   - [Insert Sample Data](#insert-sample-data)
   - [Insert Data into Tables](#insert-data-into-tables)
2. [Database Schema](#database-schema)
3. [Contributing](#contributing)
4. [License](#license)
5. [Testing](#testing)

## Database Setup

### Drop Existing Database and Tables

To start fresh, the script drops any existing "craigslist" database and all its tables if they exist.

### Create Tables

The script creates the following tables:

-  `regions` : Stores information about different regions.
-  `users` : Stores information about users, including their preferred region.
-  `categories` : Stores information about different categories.
-  `posts` : Stores information about individual posts, including the user, location, and region.
-  `post_categories` : Stores the relationship between posts and categories.

### Create Indexes

Indexes are created on the following columns for improved query performance:

-  `user_id`  and  `region_id`  columns in the  `posts`  table.
-  `post_id`  and  `category_id`  columns in the  `post_categories`  table.

### Insert Sample Data

Some sample data is inserted into the  `regions`  and  `categories`  tables to demonstrate the functionality of the database.

### Insert Data into Tables

Additional sample data is inserted into the  `users` ,  `posts` , and  `post_categories`  tables to showcase how the tables are related.

## Database Schema

The database schema consists of the following tables:

-  `regions` :
  -  `id`  (Primary Key): Unique identifier for each region.
  -  `name` : Name of the region.

-  `users` :
  -  `id`  (Primary Key): Unique identifier for each user.
  -  `name` : Name of the user.
  -  `preferred_region_id`  (Foreign Key): Reference to the preferred region of the user.

-  `categories` :
  -  `id`  (Primary Key): Unique identifier for each category.
  -  `name` : Name of the category.

-  `posts` :
  -  `id`  (Primary Key): Unique identifier for each post.
  -  `title` : Title of the post.
  -  `text` : Text content of the post.
  -  `user_id`  (Foreign Key): Reference to the user who created the post.
  -  `location` : Location of the post.
  -  `region_id`  (Foreign Key): Reference to the region associated with the post.

-  `post_categories` :
  -  `post_id`  (Foreign Key): Reference to the post.
  -  `category_id`  (Foreign Key): Reference to the category.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

# Testing
**Select all rows from a table**

SELECT * FROM regions;
SELECT * FROM users;
SELECT * FROM categories;
SELECT * FROM posts;
SELECT * FROM post_categories;

**Select specific columns from a table**

SELECT name FROM regions;
SELECT id, name FROM users;
SELECT id, title, location FROM posts;

**Filter rows using WHERE**

SELECT * FROM regions WHERE id = 1;
SELECT * FROM users WHERE preferred_region_id = 2;
SELECT * FROM posts WHERE region_id = 1 AND user_id = 1;

**Join tables using JOIN**

SELECT posts.title, categories.name
FROM posts
JOIN post_categories ON posts.id = post_categories.post_id
JOIN categories ON post_categories.category_id = categories.id;

**Aggregate data using GROUP BY**

SELECT region_id, COUNT(*) AS post_count
FROM posts
GROUP BY region_id;