-- PART 1

-- Join the two tables so that every column and record appears, regardless of if there is not an owner_id . Your output should look like this:

SELECT o1.id, o1.first_name, o1.last_name, v2.id, v2.make, v2.model, v2.year, v2.price, v2.owner_id
FROM owners o1
LEFT JOIN vehicles v2 ON o1.id = v2.owner_id;


-- Count the number of cars for each owner. Display the owners first_name , last_name and count of vehicles. 
-- The first_name should be ordered in ascending order. Your output should look like this:

SELECT o1.first_name, o1.last_name, COUNT(v2.id)
FROM owners o1
LEFT JOIN vehicles v2 ON o1.id = v2.owner_id
GROUP BY o1.first_name, o1.last_name;

-- Count the number of cars for each owner and display the average price for each of the cars as integers. 
-- Display the owners first_name , last_name, average price and count of vehicles. 
-- The first_name should be ordered in descending order. Only display results with more than one vehicle and an average price greater than 10000. 
-- Your output should look like this:

SELECT o1.first_name, o1.last_name, AVG(v2.price), COUNT(v2.id)
FROM owners o1
LEFT JOIN vehicles v2 ON o1.id = v2.owner_id
GROUP BY o1.first_name, o1.last_name
HAVING AVG(v2.price) > 10000 AND COUNT(v2.id) > 1
ORDER BY o1.first_name DESC;


-- PART 2

-- To JOIN game with eteam you could use either
-- game JOIN eteam ON (team1=eteam.id) or game JOIN eteam ON (team2=eteam.id)
-- Notice that because id is a column name in both game and eteam you must specify eteam.id instead of just id


-- List the dates of the matches and the name of the team in which 'Fernando Santos' was the team1 coach.

SELECT game.mdate, eteam.teamname
FROM game
JOIN eteam ON (game.team1 = eteam.id)
WHERE eteam.coach = 'Fernando Santos';


-- List the player for every goal scored in a game where the stadium was 'National Stadium, Warsaw'

SELECT player
FROM goal
JOIN game ON (goal.matchid = game.id)
WHERE stadium = 'National Stadium, Warsaw'

