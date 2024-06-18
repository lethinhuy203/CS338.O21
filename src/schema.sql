DROP TABLE IF EXISTS PlantDisease;

CREATE TABLE PlantDisease (
	disease_id	TEXT NOT NULL UNIQUE,
	plant_name	TEXT NOT NULL,
	disease_name	TEXT NOT NULL,
	affect	TEXT,
	solution	TEXT,
	PRIMARY KEY(disease_id)
);

CREATE TABLE PredictionLog (
	image_url	TEXT NOT NULL UNIQUE,
	predict_result	TEXT NOT NULL,
	model_name	TEXT,
	PRIMARY KEY(image_url)
);