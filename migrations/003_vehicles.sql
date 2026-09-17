CREATE TABLE IF NOT EXISTS Vehicles (
    Vehicle_ID BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    Grower_ID BIGINT UNSIGNED NOT NULL,
    Vehicle_Code VARCHAR(120) NOT NULL,
    Vehicle_Name VARCHAR(120) NOT NULL,
    Load_Cell VARCHAR(100) NULL,
    PRIMARY KEY (Vehicle_ID),
    UNIQUE KEY uq_vehicle_grower_code (Grower_ID, Vehicle_Code),
    CONSTRAINT fk_vehicle_grower FOREIGN KEY (Grower_ID)
        REFERENCES Grower(Grower_ID) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
