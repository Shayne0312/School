# Music Database SQL Script

This SQL script sets up a database schema for a music database. It creates tables for artists, albums, producers, and songs. It also includes constraints, indexes, and sample data to populate the tables.

## Table of Contents

1. [Database Setup](#database-setup)
   - [Drop Existing Database and Tables](#drop-existing-database-and-tables)
   - [Create Tables](#create-tables)
   - [Create Indexes](#create-indexes)
   - [Insert Sample Data](#insert-sample-data)
2. [Database Schema](#database-schema)
3. [Contributing](#contributing)
4. [License](#license)
5. [Testing](#testing)

## Prerequisites

- PostgreSQL database server installed and running.
-  `psql`  command-line tool installed.

## Installation

1. Clone the repository or download the SQL script file.
2. Open a terminal and navigate to the directory containing the SQL script file.

## Database Schema

The script creates the following tables:

-  `artists` : Stores information about artists, including their ID and name.
-  `albums` : Stores information about albums, including their ID and title.
-  `producers` : Stores information about producers, including their ID and name.
-  `songs` : Stores information about songs, including their ID, title, duration, release date, and references to artists, albums, and producers.

The script also includes constraints, indexes, and default values to ensure data integrity and performance.

## Usage

1. Open a terminal and navigate to the directory containing the SQL script file.
2. Run the following command to execute the script and create the database and tables:
psql < music.sql
3. The script will drop any existing database and tables with the same name and create new ones.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This SQL script is released under the [MIT License](LICENSE).

## Testing

### Select all rows from a table
SELECT * FROM artists;
SELECT * FROM albums;
SELECT * FROM producers;
SELECT * FROM songs;

### Select specific columns from a table
SELECT name FROM artists;
SELECT title FROM albums;
SELECT name FROM producers;
SELECT title, duration FROM songs;

### Filter rows using WHERE
SELECT * FROM artists WHERE id = 1;
SELECT * FROM albums WHERE title LIKE '%Night%';
SELECT * FROM producers WHERE name = 'Max Martin';
SELECT * FROM songs WHERE duration > 200;