-- from the terminal run:
-- psql < outer_space.sql

-- Table of Contents
-- 1. Drop existing database and tables
-- 2. Create tables
-- 3. Create indexes  
-- 4. Insert sample data

-- 1. Drop existing database and tables
DROP DATABASE IF EXISTS outer_space;
CREATE DATABASE outer_space;
\c outer_space
DROP TABLE IF EXISTS stars, planets, moons;

-- 2. Create tables
CREATE TABLE stars (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE planets (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  orbital_period_in_years FLOAT NOT NULL,
  star_id INTEGER REFERENCES stars(id),
  galaxy TEXT NOT NULL
);

CREATE TABLE moons (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  planet_id INTEGER REFERENCES planets(id)
);

-- 3. Create indexes
CREATE INDEX idx_stars_name ON stars (name);
CREATE INDEX idx_planets_name ON planets (name);
CREATE INDEX idx_planets_star_id ON planets (star_id);
CREATE INDEX idx_moons_name ON moons (name);
CREATE INDEX idx_moons_planet_id ON moons (planet_id);

-- 4. Insert sample data
INSERT INTO stars (name)
VALUES
  ('The Sun'),
  ('Proxima Centauri'),
  ('Gliese 876');

INSERT INTO planets (name, orbital_period_in_years, star_id, galaxy)
VALUES
  ('Earth', 1.00, 1, 'Milky Way'),
  ('Mars', 1.88, 1, 'Milky Way'),
  ('Venus', 0.62, 1, 'Milky Way'),
  ('Neptune', 164.8, 1, 'Milky Way'),
  ('Proxima Centauri b', 0.03, 2, 'Milky Way'),
  ('Gliese 876 b', 0.23, 3, 'Milky Way');

INSERT INTO moons (name, planet_id)
VALUES
  ('The Moon', 1),
  ('Phobos', 2),
  ('Deimos', 2),
  ('Naiad', 4),
  ('Thalassa', 4),
  ('Despina', 4),
  ('Galatea', 4),
  ('Larissa', 4),
  ('S/2004 N 1', 4),
  ('Proteus', 4),
  ('Triton', 4),
  ('Nereid', 4),
  ('Halimede', 4),
  ('Sao', 4),
  ('Laomedeia', 4),
  ('Psamathe', 4),
  ('Neso', 4);