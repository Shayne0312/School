-- from the terminal run:
-- psql < medical_center.sql

-- Table of Contents
-- 1. Drop existing database and tables
-- 2. Create tables
-- 3. Create indexes  
-- 4. Insert sample data

-- 1. Drop existing database and tables
DROP DATABASE IF EXISTS medical_center;
CREATE DATABASE medical_center;
\c medical_center;
DROP TABLE IF EXISTS afflictions, appointments, patients, doctors, medical_centers;

-- 2. Create tables
CREATE TABLE medical_centers (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  address TEXT NOT NULL, 
  phone_number TEXT NOT NULL
);
COMMENT ON TABLE medical_centers IS 'Medical centers information';

CREATE TABLE doctors (
  id SERIAL PRIMARY KEY,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  specialty TEXT NOT NULL,
  medical_center_id INTEGER NOT NULL REFERENCES medical_centers(id) ON DELETE CASCADE
);
COMMENT ON TABLE doctors IS 'Information about doctors';
COMMENT ON COLUMN doctors.medical_center_id IS 'Reference to medical center';

CREATE TABLE patients (
  id SERIAL PRIMARY KEY,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  birth_date DATE NOT NULL,
  medical_center_id INTEGER NOT NULL REFERENCES medical_centers(id) ON DELETE CASCADE
);  
COMMENT ON TABLE patients IS 'Information about patients';

CREATE TABLE appointments (
  id SERIAL PRIMARY KEY,
  doctor_id INTEGER NOT NULL REFERENCES doctors(id),
  patient_id INTEGER NOT NULL REFERENCES patients(id),
  appointment_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  medical_center_id INTEGER NOT NULL REFERENCES medical_centers(id)
);
COMMENT ON TABLE appointments IS 'Appointment details';

CREATE TABLE afflictions (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  patient_id INTEGER NOT NULL REFERENCES patients(id),
  description TEXT NOT NULL CHECK (LENGTH(description) <= 500)
);
COMMENT ON TABLE afflictions IS 'Patient afflictions data';

-- Validate maximum lengths
ALTER TABLE medical_centers 
  ADD CONSTRAINT medical_centers_name_max_length CHECK (LENGTH(name) <= 100);

ALTER TABLE medical_centers
  ADD CONSTRAINT medical_centers_address_max_length CHECK (LENGTH(address) <= 200);

ALTER TABLE doctors
  ADD CONSTRAINT doctors_first_name_max_length CHECK (LENGTH(first_name) <= 50);

ALTER TABLE doctors 
  ADD CONSTRAINT doctors_last_name_max_length CHECK (LENGTH(last_name) <= 50);

-- Validate phone number format
ALTER TABLE medical_centers
  ADD CONSTRAINT medical_centers_phone_number_format CHECK (phone_number ~ '^[0-9]{3}-[0-9]{4}$');

-- Add default values  
ALTER TABLE appointments 
  ALTER COLUMN appointment_date SET DEFAULT NOW();

ALTER TABLE afflictions
  ALTER COLUMN description SET DEFAULT 'Description not provided';

-- 3. Create indexes
CREATE INDEX idx_medical_centers_name ON medical_centers(name);
CREATE INDEX idx_doctors_specialty ON doctors(specialty);  
CREATE INDEX idx_patients_last_name ON patients(last_name);
CREATE INDEX idx_appointments_date ON appointments(appointment_date);
CREATE INDEX idx_afflictions_name ON afflictions(name);

-- 4. Insert sample data
INSERT INTO medical_centers (name, address, phone_number)
VALUES
  ('St. Marys', '123 Main St', '555-1234'),
  ('St. Johns', '456 Park Ave', '555-5678');   
  
INSERT INTO doctors (first_name, last_name, specialty, medical_center_id)  
VALUES
  ('John', 'Doe', 'Pediatrics', 1),
  ('Jane', 'Doe', 'Cardiology', 1);

INSERT INTO patients (first_name, last_name, birth_date, medical_center_id)
VALUES
  ('Bob', 'Smith', '2000-05-06', 1),
  ('Mary', 'Jones', '1990-08-23', 1);
 
INSERT INTO appointments (doctor_id, patient_id, medical_center_id, appointment_date)
VALUES
  (1, 1, 1, '2023-01-15 10:00');

INSERT INTO afflictions (name, patient_id)  
VALUES
  ('Broken arm', 1);