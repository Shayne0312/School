# Medical Center SQL Script

This SQL script sets up a database schema for a medical center system. It creates tables for medical centers, doctors, patients, appointments, and afflictions. It also includes constraints, indexes, and sample data to populate the tables.

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

-  `medical_centers` : Stores information about medical centers such as name, address, and phone number.
-  `doctors` : Stores information about doctors such as first name, last name, specialty, and the medical center they belong to.
-  `patients` : Stores information about patients such as first name, last name, birth date, and the medical center they belong to.
-  `appointments` : Stores details about appointments including the doctor, patient, appointment date, and the medical center.
-  `afflictions` : Stores information about patient afflictions including the name, patient ID, and description.

The script also includes constraints, indexes, and default values to ensure data integrity and performance.

## Usage

1. Open a terminal and navigate to the directory containing the SQL script file.
2. Run the following command to execute the script and create the database and tables:
psql < medical_center.sql
3. The script will drop any existing database and tables with the same name and create new ones.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This SQL script is released under the [MIT License](LICENSE).

## Testing
### Select all rows from a table

SELECT * FROM medical_centers;
SELECT * FROM doctors;
SELECT * FROM patients;
SELECT * FROM appointments;
SELECT * FROM afflictions;

**Select specific columns from a table**

SELECT name, address FROM medical_centers;
SELECT first_name, last_name, specialty FROM doctors;
SELECT first_name, last_name, birth_date FROM patients;
SELECT doctor_id, patient_id, appointment_date FROM appointments;
SELECT name, patient_id FROM afflictions;

**Filter rows using WHERE**

SELECT * FROM medical_centers WHERE id = 1;
SELECT * FROM doctors WHERE specialty = 'Pediatrics';
SELECT * FROM patients WHERE birth_date > '1995-01-01';
SELECT * FROM appointments WHERE doctor_id = 1 AND patient_id = 1;
SELECT * FROM afflictions WHERE name = 'Broken arm';

**Join tables using JOIN**

SELECT doctors.first_name, doctors.last_name, patients.first_name, patients.last_name
FROM doctors
JOIN appointments ON doctors.id = appointments.doctor_id
JOIN patients ON appointments.patient_id = patients.id;

**Aggregate data using GROUP BY**

SELECT specialty, COUNT(*) AS count
FROM doctors
GROUP BY specialty;