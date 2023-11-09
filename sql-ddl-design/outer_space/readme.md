# Outer Space SQL Script

This SQL script sets up a database schema for an outer space system. It creates tables for stars, planets, and moons. It also includes constraints, indexes, and sample data to populate the tables.

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
-  `stars` : Stores information about stars such as name.
-  `planets` : Stores information about planets such as name, orbital period in years, star ID, and galaxy.
-  `moons` : Stores information about moons such as name and planet ID.

## Usage
1. Open a terminal and navigate to the directory containing the SQL script file.
2. Run the following command to execute the script and create the database and tables:
psql < outer_space.sql
3. The script will drop any existing database and tables with the same name and create new ones.

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License
This SQL script is released under the [MIT License](LICENSE).

## Testing
### Select all rows from a table
SELECT * FROM stars;
SELECT * FROM planets;
SELECT * FROM moons;

### Select specific columns from a table
SELECT name FROM stars;
SELECT name, orbital_period_in_years FROM planets;
SELECT name, planet_id FROM moons;

### Filter rows using WHERE
SELECT * FROM stars WHERE name = 'The Sun';
SELECT * FROM planets WHERE galaxy = 'Milky Way';
SELECT * FROM moons WHERE name LIKE 'P%';