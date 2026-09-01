-- Grower-based access control for GMS.
-- The application performs this migration defensively at startup; this file is
-- provided for reviewed/manual deployments.

CREATE TABLE IF NOT EXISTS grower_memberships (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  user_id BIGINT UNSIGNED NOT NULL,
  Grower_ID BIGINT UNSIGNED NOT NULL,
  role ENUM('viewer','editor','admin') NOT NULL DEFAULT 'viewer',
  status ENUM('pending','active','rejected') NOT NULL DEFAULT 'pending',
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  approved_at TIMESTAMP NULL,
  approved_by BIGINT UNSIGNED NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uq_grower_membership (user_id, Grower_ID),
  CONSTRAINT fk_membership_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  CONSTRAINT fk_membership_grower FOREIGN KEY (Grower_ID) REFERENCES Grower(Grower_ID) ON DELETE CASCADE,
  CONSTRAINT fk_membership_approver FOREIGN KEY (approved_by) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

ALTER TABLE Cart ADD COLUMN Grower_ID BIGINT UNSIGNED NULL;
ALTER TABLE Storage_Location ADD COLUMN Grower_ID BIGINT UNSIGNED NULL;
ALTER TABLE Delivery_Location ADD COLUMN Grower_ID BIGINT UNSIGNED NULL;
ALTER TABLE MarketPriceMonthly ADD COLUMN Grower_ID BIGINT UNSIGNED NULL;
ALTER TABLE Delivery ADD COLUMN Grower_ID BIGINT UNSIGNED NULL;

-- For an existing single-Grower installation, substitute the intended Grower ID
-- below before executing these backfills manually.
-- SET @existing_grower_id = 2;
-- UPDATE Cart SET Grower_ID=@existing_grower_id WHERE Grower_ID IS NULL;
-- UPDATE Storage_Location SET Grower_ID=@existing_grower_id WHERE Grower_ID IS NULL;
-- UPDATE Delivery_Location SET Grower_ID=@existing_grower_id WHERE Grower_ID IS NULL;
-- UPDATE MarketPriceMonthly SET Grower_ID=@existing_grower_id WHERE Grower_ID IS NULL;
-- UPDATE Delivery SET Grower_ID=@existing_grower_id WHERE Grower_ID IS NULL;
-- INSERT INTO grower_memberships (user_id,Grower_ID,role,status,approved_at)
-- SELECT id,@existing_grower_id,IF(role='admin','admin','editor'),'active',NOW()
-- FROM users WHERE is_active=1;
