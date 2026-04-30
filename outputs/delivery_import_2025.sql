START TRANSACTION;

INSERT INTO delivery_location (DelLoc_code, Location)
SELECT 'ANF', 'Feedmill Bins (ANF)'
WHERE NOT EXISTS (
  SELECT 1 FROM delivery_location WHERE DelLoc_code = 'ANF'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  -100005, '2025-10-31',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'HMC' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'HMC Beef' ORDER BY StorLoc_ID LIMIT 1),
  NULL, NULL, NULL, 97015.00,
  NULL, NULL, 0.00, NULL, 'LoadRef=Field Direct'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  -100006, '2025-10-31',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'ANB' ORDER BY StorLoc_ID LIMIT 1),
  NULL, NULL, NULL, 6279.76,
  NULL, NULL, 0.00, NULL, 'LoadRef=Field Direct'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  -100007, '2025-10-31',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'ANF' ORDER BY StorLoc_ID LIMIT 1),
  NULL, NULL, NULL, 21024.11,
  NULL, NULL, 0.00, NULL, 'LoadRef=Field Direct'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  1, '2025-11-07',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin15' ORDER BY StorLoc_ID LIMIT 1),
  14.00, 64740.00, 27450.00, 665.89,
  NULL, NULL, 0.00, NULL, 'LoadRef=S1'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  2, '2025-11-07',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin15' ORDER BY StorLoc_ID LIMIT 1),
  14.00, 48220.00, 27470.00, 370.54,
  NULL, NULL, 0.00, NULL, 'LoadRef=S2'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  3, '2025-11-10',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin13' ORDER BY StorLoc_ID LIMIT 1),
  13.80, 59130.00, 27210.00, 570.00,
  NULL, NULL, 0.00, NULL, 'LoadRef=S3'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  4, '2025-11-10',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin13' ORDER BY StorLoc_ID LIMIT 1),
  14.70, 60330.00, 27110.00, 593.21,
  NULL, NULL, 0.00, NULL, 'LoadRef=S4'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  5, '2025-11-14',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin12' ORDER BY StorLoc_ID LIMIT 1),
  15.10, 57280.00, 26180.00, 555.36,
  NULL, NULL, 0.00, NULL, 'LoadRef=S5'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  6, '2025-11-14',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin12' ORDER BY StorLoc_ID LIMIT 1),
  15.20, 60390.00, 27280.00, 591.25,
  NULL, NULL, 0.00, NULL, 'LoadRef=S6'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  7, '2025-11-14',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'SCB' ORDER BY StorLoc_ID LIMIT 1),
  13.20, 55380.00, 27300.00, 501.43,
  NULL, NULL, 0.00, NULL, 'LoadRef=S7'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  8, '2025-11-19',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'SCB' ORDER BY StorLoc_ID LIMIT 1),
  13.20, 61820.00, 27100.00, 620.00,
  NULL, NULL, 0.00, NULL, 'LoadRef=S8'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  9, '2025-11-19',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin14' ORDER BY StorLoc_ID LIMIT 1),
  13.70, 62400.00, 27070.00, 630.89,
  NULL, NULL, 0.00, NULL, 'LoadRef=S9'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  10, '2025-11-21',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  13.20, 63200.00, 27080.00, 645.00,
  NULL, NULL, 0.00, NULL, 'LoadRef=S10'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  11, '2025-11-25',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  13.40, 59230.00, 26310.00, 587.86,
  NULL, NULL, 0.00, NULL, 'LoadRef=S11'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  12, '2025-11-25',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  13.30, 56680.00, 26790.00, 533.75,
  NULL, NULL, 0.00, NULL, 'LoadRef=S12'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  13, '2025-11-25',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  13.70, 60130.00, 26140.00, 606.96,
  NULL, NULL, 0.00, NULL, 'LoadRef=S13'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  14, '2025-12-02',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  13.60, 62800.00, 27100.00, 637.50,
  NULL, NULL, 0.00, NULL, 'LoadRef=S14'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  15, '2025-12-02',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  13.70, 64190.00, 27240.00, 659.82,
  NULL, NULL, 0.00, NULL, 'LoadRef=S15'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  16, '2025-12-05',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  13.60, 64970.00, 27340.00, 671.96,
  NULL, NULL, 0.00, NULL, 'LoadRef=S16'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  17, '2025-12-05',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  13.80, 62550.00, 27350.00, 628.57,
  NULL, NULL, 0.00, NULL, 'LoadRef=S17'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  18, '2025-12-08',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  14.20, 62810.00, 27360.00, 633.04,
  NULL, NULL, 0.00, NULL, 'LoadRef=S18'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  19, '2025-12-08',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  14.30, 63620.00, 27480.00, 645.36,
  NULL, NULL, 0.00, NULL, 'LoadRef=S19'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  20, '2025-12-11',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  14.00, 65870.00, 27540.00, 684.46,
  NULL, NULL, 0.00, NULL, 'LoadRef=S20'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  21, '2025-12-11',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  14.60, 64820.00, 27620.00, 664.29,
  NULL, NULL, 0.00, NULL, 'LoadRef=S21'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  22, '2025-12-11',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  14.60, 62850.00, 27600.00, 629.46,
  NULL, NULL, 0.00, NULL, 'LoadRef=S22'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  23, '2025-12-15',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  15.00, 61870.00, 27500.00, 613.75,
  NULL, NULL, 0.00, NULL, 'LoadRef=S23'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  24, '2025-12-15',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  15.00, 64590.00, 27530.00, 661.79,
  NULL, NULL, 0.00, NULL, 'LoadRef=S24'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  25, '2025-12-17',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  14.40, 63750.00, 27590.00, 645.71,
  NULL, NULL, 0.00, NULL, 'LoadRef=S25'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  26, '2025-12-18',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  14.50, 61010.00, 26040.00, 624.46,
  NULL, NULL, 0.00, NULL, 'LoadRef=S26'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  27, '2025-12-18',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  14.50, 59740.00, 26260.00, 597.86,
  NULL, NULL, 0.00, NULL, 'LoadRef=S27'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  28, '2025-12-18',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  14.50, 59200.00, 26280.00, 587.86,
  NULL, NULL, 0.00, NULL, 'LoadRef=S28'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  29, '2025-12-18',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  14.50, 58330.00, 26120.00, 575.18,
  NULL, NULL, 0.00, NULL, 'LoadRef=S29'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  30, '2025-12-18',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  14.50, 58180.00, 26360.00, 568.21,
  NULL, NULL, 0.00, NULL, 'LoadRef=S30'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  31, '2025-12-19',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  14.50, 61030.00, 24970.00, 643.93,
  NULL, NULL, 0.00, NULL, 'LoadRef=S31'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  32, '2025-12-19',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  14.50, 60890.00, 25350.00, 634.64,
  NULL, NULL, 0.00, NULL, 'LoadRef=S32'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  33, '2025-12-19',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  14.50, 58400.00, 26120.00, 576.43,
  NULL, NULL, 0.00, NULL, 'LoadRef=S33'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  34, '2025-12-19',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  14.50, 57710.00, 26310.00, 560.71,
  NULL, NULL, 0.00, NULL, 'LoadRef=S34'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  35, '2025-12-19',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  14.50, 57110.00, 25760.00, 559.82,
  NULL, NULL, 0.00, NULL, 'LoadRef=S35'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  36, '2025-12-19',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin12' ORDER BY StorLoc_ID LIMIT 1),
  14.30, 63020.00, 27380.00, 636.43,
  NULL, NULL, 0.00, NULL, 'LoadRef=S36'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  37, '2025-12-19',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin12' ORDER BY StorLoc_ID LIMIT 1),
  13.70, 61440.00, 27280.00, 610.00,
  NULL, NULL, 0.00, NULL, 'LoadRef=S37'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  38, '2025-12-19',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin12' ORDER BY StorLoc_ID LIMIT 1),
  14.60, 61590.00, 26920.00, 619.11,
  NULL, NULL, 0.00, NULL, 'LoadRef=S38'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  39, '2025-12-22',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  14.00, 59710.00, 26220.00, 598.04,
  NULL, NULL, 0.00, NULL, 'LoadRef=S39'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  40, '2025-12-22',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  14.20, 59640.00, 26220.00, 596.79,
  NULL, NULL, 0.00, NULL, 'LoadRef=S40'
);

COMMIT;
