-- Part 1: SQL Query

SELECT population FROM world
  WHERE name = 'Germany'


SELECT name, population
FROM countries
WHERE name IN ('Sweden', 'Norway', 'Denmark');


SELECT country, area
FROM countries
WHERE area BETWEEN 200000 AND 250000;


-- Part 2: SQL Query
SELECT * FROM people WHERE age > 50 ORDER BY age DESC;

SELECT SUM(age) AS age_sum FROM people;

SELECT MIN(age) AS age_min, MAX(age) AS age_max FROM people;

SELECT * FROM students WHERE IsActive = 1;

SELECT age, COUNT(*) AS people_count FROM people GROUP BY age;

SELECT age, COUNT(*) AS total_people FROM people GROUP BY age HAVING COUNT(*) >= 10;