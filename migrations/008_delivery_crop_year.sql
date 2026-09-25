-- Apply once before deploying the crop-year inventory changes.
-- Historical assignments require review; delivery date is not harvest year.
ALTER TABLE Delivery ADD COLUMN Crop_Year SMALLINT UNSIGNED NULL,
    ADD INDEX idx_delivery_grower_crop_year (Grower_ID, Crop_Year);
