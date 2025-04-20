-- Create a sample f1drivers_dataset table
CREATE TABLE IF NOT EXISTS "f1drivers_dataset" (
    "Driver" VARCHAR(255),
    "Team" VARCHAR(255),
    "Country" VARCHAR(255), 
    "Age" INT,
    "RaceWins" INT,
    "PodiumFinishes" INT,
    "Points" FLOAT,
    "Season" INT
);

-- Insert sample data
INSERT INTO "f1drivers_dataset" ("Driver", "Team", "Country", "Age", "RaceWins", "PodiumFinishes", "Points", "Season")
VALUES
    ('Max Verstappen', 'Red Bull Racing', 'Netherlands', 25, 35, 77, 454.5, 2022),
    ('Lewis Hamilton', 'Mercedes', 'United Kingdom', 38, 103, 191, 240.0, 2022),
    ('Charles Leclerc', 'Ferrari', 'Monaco', 25, 5, 24, 308.0, 2022),
    ('Sergio Perez', 'Red Bull Racing', 'Mexico', 33, 4, 26, 305.0, 2022),
    ('Carlos Sainz', 'Ferrari', 'Spain', 28, 1, 15, 246.0, 2022),
    ('George Russell', 'Mercedes', 'United Kingdom', 25, 1, 10, 275.0, 2022),
    ('Lando Norris', 'McLaren', 'United Kingdom', 23, 0, 6, 122.0, 2022),
    ('Fernando Alonso', 'Alpine', 'Spain', 41, 32, 98, 81.0, 2022); 