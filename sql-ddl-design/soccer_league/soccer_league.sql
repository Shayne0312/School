-- from the terminal run:
-- psql < soccer_league.sql

-- Table of Contents
-- 1. Drop existing database and tables
-- 2. Create tables
-- 3. Create indexes  
-- 4. Insert sample data

-- 1. Drop existing database and tables
DROP DATABASE IF EXISTS soccer_league;
CREATE DATABASE soccer_league;
\c soccer_league;
DROP TABLE IF EXISTS teams, players, referees, matches, goals, seasons, team_standings;

-- 2. Create tables
CREATE TABLE teams (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  city TEXT NOT NULL 
);

CREATE TABLE players (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  team_id INTEGER REFERENCES teams(id)
);

CREATE TABLE referees (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE matches (
  id SERIAL PRIMARY KEY,
  home_team_id INTEGER REFERENCES teams(id),
  away_team_id INTEGER REFERENCES teams(id),
  match_date DATE NOT NULL
);

CREATE TABLE goals (
  id SERIAL PRIMARY KEY,
  match_id INTEGER REFERENCES matches(id),
  player_id INTEGER REFERENCES players(id) 
);

CREATE TABLE seasons (
  id SERIAL PRIMARY KEY,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL
);

CREATE TABLE team_standings (
  id SERIAL PRIMARY KEY,
  team_id INTEGER REFERENCES teams(id),
  season_id INTEGER REFERENCES seasons(id),
  wins INTEGER,
  draws INTEGER, 
  losses INTEGER,
  points INTEGER 
);

-- 4. Create indexes
CREATE INDEX idx_teams_name ON teams (name);
CREATE INDEX idx_players_name ON players (name);
CREATE INDEX idx_matches_match_date ON matches (match_date);
CREATE INDEX idx_goals_match_id ON goals (match_id);
CREATE INDEX idx_goals_player_id ON goals (player_id);
CREATE INDEX idx_seasons_start_date ON seasons (start_date);
CREATE INDEX idx_seasons_end_date ON seasons (end_date);
CREATE INDEX idx_team_standings_team_id ON team_standings (team_id);
CREATE INDEX idx_team_standings_season_id ON team_standings (season_id);

-- 5. Insert sample data
INSERT INTO teams (name, city) 
VALUES
  ('Team A', 'City A'),
  ('Team B', 'City B'),
  ('Team C', 'City C');

INSERT INTO players (name, team_id) 
VALUES
  ('Player 1', 1),
  ('Player 2', 1),
  ('Player 3', 2),
  ('Player 4', 2),
  ('Player 5', 3),
  ('Player 6', 3);

INSERT INTO referees (name) 
VALUES
  ('Referee 1'),
  ('Referee 2'),
  ('Referee 3');

INSERT INTO matches (home_team_id, away_team_id, match_date) 
VALUES
  (1, 2, '2022-01-01'),
  (2, 3, '2022-01-02'),
  (3, 1, '2022-01-03');

INSERT INTO goals (match_id, player_id) 
VALUES
  (1, 1),
  (1, 2),
  (2, 3),
  (3, 6);

INSERT INTO seasons (start_date, end_date) 
VALUES
  ('2022-01-01', '2022-12-31');

INSERT INTO team_standings (team_id, season_id, wins, draws, losses, points) 
VALUES
  (1, 1, 2, 1, 0, 7),
  (2, 1, 1, 1, 1, 4),
  (3, 1, 0, 2, 1, 2);