-- Preserve harvest loads when an incorrect cart assignment is removed.
ALTER TABLE Harvest MODIFY COLUMN Cart_ID BIGINT UNSIGNED NULL;
