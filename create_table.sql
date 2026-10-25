CREATE TABLE air_quality_hourly (
    measured_at       TIMESTAMP     NOT NULL,
    latitude          NUMERIC(7,4)  NOT NULL,
    longitude         NUMERIC(7,4)  NOT NULL,
    pm10              REAL,
    pm2_5             REAL,
    carbon_monoxide   REAL,
    nitrogen_dioxide  REAL,
    source_file       TEXT,
    loaded_at         TIMESTAMP DEFAULT now(),
    PRIMARY KEY (measured_at, latitude, longitude)
);