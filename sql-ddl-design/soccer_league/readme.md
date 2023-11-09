# Soccer League Database Setup

This repository contains the necessary SQL code to set up a PostgreSQL database for a soccer league. The code creates tables for teams, players, referees, matches, goals, seasons, and team_standings, and includes sample data to populate the tables.

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

To start fresh, the script drops any existing "soccer_league" database and all its tables if they exist.

### Create Tables

The script creates the following tables:

-  `teams` : Stores information about the teams in the league, including the team's unique identifier, name, and city.
-  `players` : Stores information about the players in the league, including the player's unique identifier, name, and the team they belong to.
-  `referees` : Stores information about the referees in the league, including the referee's unique identifier and name.
-  `matches` : Stores information about the matches played between teams, including the match's unique identifier, home team, away team, and match date.
-  `goals` : Stores information about the goals scored in each match, including the goal's unique identifier, the match it belongs to, and the player who scored the goal.
-  `seasons` : Stores information about the seasons in the league, including the season's unique identifier, start date, and end date.
-  `team_standings` : Stores the standings/rankings of each team in the league for each season, including the team's unique identifier, the season it belongs to, and the number of wins, draws, losses, and points accumulated by the team.

### Create Indexes

Indexes are created on various columns for improved query performance.

### Insert Sample Data

Some sample data is inserted into the tables to demonstrate the functionality of the database.

## Database Schema

The database schema consists of the following tables:

-  `teams` :
  -  `id`  (Primary Key): Unique identifier for each team.
  -  `name` : Name of the team.
  -  `city` : City where the team is located.

-  `players` :
  -  `id`  (Primary Key): Unique identifier for each player.
  -  `name` : Name of the player.
  -  `team_id`  (Foreign Key): Reference to the team the player belongs to.

-  `referees` :
  -  `id`  (Primary Key): Unique identifier for each referee.
  -  `name` : Name of the referee.

-  `matches` :
  -  `id`  (Primary Key): Unique identifier for each match.
  -  `home_team_id`  (Foreign Key): Reference to the home team.
  -  `away_team_id`  (Foreign Key): Reference to the away team.
  -  `match_date` : Date of the match.

-  `goals` :
  -  `id`  (Primary Key): Unique identifier for each goal.
  -  `match_id`  (Foreign Key): Reference to the match the goal belongs to.
  -  `player_id`  (Foreign Key): Reference to the player who scored the goal.

-  `seasons` :
  -  `id`  (Primary Key): Unique identifier for each season.
  -  `start_date` : Start date of the season.
  -  `end_date` : End date of the season.

-  `team_standings` :
  -  `id`  (Primary Key): Unique identifier for each team standing.
  -  `team_id`  (Foreign Key): Reference to the team.
  -  `season_id`  (Foreign Key): Reference to the season.
  -  `wins` : Number of wins for the team.
  -  `draws` : Number of draws for the team.
  -  `losses` : Number of losses for the team.
  -  `points` : Total points accumulated by the team.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Testing
### Select all rows from a table

SELECT * FROM teams;
SELECT * FROM players;
SELECT * FROM referees;
SELECT * FROM matches;
SELECT * FROM goals;
SELECT * FROM seasons;
SELECT * FROM team_standings;

**Select specific columns from a table**

SELECT name, city FROM teams;
SELECT name, team_id FROM players;
SELECT name FROM referees;
SELECT home_team_id, away_team_id, match_date FROM matches;
SELECT match_id, player_id FROM goals;
SELECT start_date, end_date FROM seasons;
SELECT team_id, season_id, wins, draws, losses, points FROM team_standings;

**Filter rows using WHERE**

SELECT * FROM teams WHERE id = 1;
SELECT * FROM players WHERE team_id = 1;
SELECT * FROM referees WHERE id = 1;
SELECT * FROM matches WHERE home_team_id = 1 AND away_team_id = 2;
SELECT * FROM goals WHERE match_id = 1;
SELECT * FROM seasons WHERE id = 1;
SELECT * FROM team_standings WHERE team_id = 1 AND season_id = 1;

**Join tables using JOIN**

SELECT teams.name, players.name
FROM teams
JOIN players ON teams.id = players.team_id;

SELECT matches.match_date, teams.name, goals.player_id
FROM matches
JOIN teams ON matches.home_team_id = teams.id

**Aggregate functions using GROUP BY**

SELECT teams.name, COUNT(matches.id) AS matches_played
FROM teams
JOIN matches ON teams.id = matches.home_team_id OR teams.id = matches.away_team_id
GROUP BY teams.name;

SELECT teams.name, COUNT(goals.id) AS goals_scored
FROM teams
JOIN goals ON teams.id = goals.player_id
GROUP BY teams.name;

**Order results using ORDER BY**

SELECT teams.name, COUNT(matches.id) AS matches_played
FROM teams
JOIN matches ON teams.id = matches.home_team_id OR teams.id = matches.away_team_id
GROUP BY teams.name
ORDER BY matches_played DESC;

SELECT teams.name, COUNT(goals.id) AS goals_scored
FROM teams
JOIN goals ON teams.id = goals.player_id
GROUP BY teams.name
ORDER BY goals_scored DESC;