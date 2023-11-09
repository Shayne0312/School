# Air Traffic Database Setup

This repository contains the necessary SQL code to set up a PostgreSQL database for tracking air traffic. The code creates tables for airlines, cities, countries, and tickets, and includes sample data to populate the tables.

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

## Database Setup

### Drop Existing Database and Tables

To start fresh, the script drops any existing "air_traffic" database and all its tables if they exist.

### Create Tables

The script creates the following tables:

-  `airlines` : Stores information about the airlines, including the airline's unique identifier and name.
-  `cities` : Stores information about the cities, including the city's unique identifier, name, and the country it belongs to.
-  `countries` : Stores information about the countries, including the country's unique identifier and name.
-  `tickets` : Stores information about the flight tickets, including the ticket's unique identifier, passenger's first name, last name, seat number, departure and arrival timestamps, airline ID, departure city ID, and arrival city ID.

### Create Indexes

Indexes are created on various columns for improved query performance.

### Insert Sample Data

Some sample data is inserted into the tables to demonstrate the functionality of the database.

## Database Schema

The database schema consists of the following tables:

-  `airlines` :
  -  `id`  (Primary Key): Unique identifier for each airline.
  -  `name` : Name of the airline.

-  `cities` :
  -  `id`  (Primary Key): Unique identifier for each city.
  -  `name` : Name of the city.
  -  `country_id`  (Foreign Key): Reference to the country the city belongs to.

-  `countries` :
  -  `id`  (Primary Key): Unique identifier for each country.
  -  `name` : Name of the country.

-  `tickets` :
  -  `id`  (Primary Key): Unique identifier for each ticket.
  -  `first_name` : First name of the passenger.
  -  `last_name` : Last name of the passenger.
  -  `seat` : Seat number of the ticket.
  -  `departure` : Departure timestamp of the flight.
  -  `arrival` : Arrival timestamp of the flight.
  -  `airline_id`  (Foreign Key): Reference to the airline providing the flight.
  -  `departure_city_id`  (Foreign Key): Reference to the city of departure.
  -  `arrival_city_id`  (Foreign Key): Reference to the city of arrival.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Testing

### Select all rows from a table

SELECT * FROM airlines;
SELECT * FROM cities;
SELECT * FROM countries;
SELECT * FROM tickets;

**Select specific columns from a table**

SELECT name FROM airlines;
SELECT name FROM cities;
SELECT name FROM countries;
SELECT first_name, last_name FROM tickets;

**Select specific rows from a table**

SELECT * FROM airlines WHERE id = 1;
SELECT * FROM cities WHERE id = 1;
SELECT * FROM countries WHERE id = 1;
SELECT * FROM tickets WHERE id = 1;

**Join tables using JOIN**

SELECT airlines.name, cities.name, tickets.seat
FROM airlines
JOIN tickets ON airlines.id = tickets.airline_id
JOIN cities ON tickets.departure_city_id = cities.id;
