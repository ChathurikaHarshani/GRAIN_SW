-- Apply before deploying the updated website. Imports need no changes.
-- Separate state keeps dismissal intact when Raven refreshes harvest values.
CREATE TABLE IF NOT EXISTS Harvest_Attention (
    Harvest_ID BIGINT UNSIGNED NOT NULL,
    Grower_ID BIGINT UNSIGNED NOT NULL,
    Dismissed TINYINT(1) NOT NULL DEFAULT 0,
    Reason VARCHAR(500) NULL,
    User_ID BIGINT UNSIGNED NOT NULL,
    Updated_At TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (Harvest_ID, Grower_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
