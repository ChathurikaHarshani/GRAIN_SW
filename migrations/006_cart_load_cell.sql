-- Apply once before deploying the cart Load Cell UI/import changes.
-- Retain legacy Vehicles columns for recovery; do not infer a vehicle/cart mapping.
ALTER TABLE Cart
    ADD COLUMN Load_Cell VARCHAR(100) NULL,
    ADD COLUMN Load_Cell_Date DATE NULL;

-- Seed each cart from its latest linked harvest with a nonempty load cell.
-- Restrict the history to the cart's grower. Historical loads are unchanged.
UPDATE Cart c
SET c.Load_Cell = (
    SELECT TRIM(h.Load_Cell)
    FROM Harvest h
    JOIN Field f ON f.Field_ID = h.Field_ID
    JOIN Department d ON d.Dpt_ID = f.Dpt_ID
    WHERE h.Cart_ID = c.Cart_ID AND d.Grower_ID = c.Grower_ID
      AND h.Load_Cell IS NOT NULL AND LOWER(TRIM(h.Load_Cell)) NOT IN ('', 'null', 'none')
    ORDER BY h.Harvest_Date DESC, h.Harvest_ID DESC LIMIT 1
),
c.Load_Cell_Date = (
    SELECT h.Harvest_Date
    FROM Harvest h
    JOIN Field f ON f.Field_ID = h.Field_ID
    JOIN Department d ON d.Dpt_ID = f.Dpt_ID
    WHERE h.Cart_ID = c.Cart_ID AND d.Grower_ID = c.Grower_ID
      AND h.Load_Cell IS NOT NULL AND LOWER(TRIM(h.Load_Cell)) NOT IN ('', 'null', 'none')
    ORDER BY h.Harvest_Date DESC, h.Harvest_ID DESC LIMIT 1
);
