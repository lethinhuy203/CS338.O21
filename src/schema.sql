DROP TABLE IF EXISTS PlantDisease;

CREATE TABLE PlantDisease (
  disease_id TEXT PRIMARY KEY NOT NULL UNIQUE,
  plant_name TEXT NOT NULL,
  disease_name TEXT NOT NULL,
  affect TEXT,
  solution TEXT
);