-- Apply to the development database before running the updated app/importer.
-- No backfill: historical manual corrections cannot be inferred reliably.
CREATE TABLE IF NOT EXISTS Harvest_Raven_State (
    Harvest_ID BIGINT UNSIGNED NOT NULL PRIMARY KEY,
    Source_Values LONGTEXT NOT NULL,
    Override_Fields LONGTEXT NOT NULL,
    Updated_At TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS Harvest_Correction_History (
    Change_ID BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Harvest_ID BIGINT UNSIGNED NOT NULL,
    User_ID BIGINT UNSIGNED NOT NULL,
    Attribute_Name VARCHAR(40) NOT NULL,
    Previous_Value LONGTEXT NULL,
    Corrected_Value LONGTEXT NULL,
    Changed_At TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    KEY idx_correction_load (Harvest_ID, Changed_At)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
