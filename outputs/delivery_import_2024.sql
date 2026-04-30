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
  -100005, '2024-10-31',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'HMC' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'HMC Beef' ORDER BY StorLoc_ID LIMIT 1),
  28.5, NULL, NULL, 74852.1,
  NULL, 3.82, 285935.022, NULL, 'LoadRef=Field Direct'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  -100006, '2024-10-31',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'HMC' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'HMC Beef-Agron' ORDER BY StorLoc_ID LIMIT 1),
  28.2, NULL, NULL, 3215.4,
  NULL, 3.82, 12282.828, NULL, 'LoadRef=Field Direct'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  -100007, '2024-10-31',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'ANF' ORDER BY StorLoc_ID LIMIT 1),
  12.3, NULL, NULL, 16484,
  NULL, 4.02, 66265.68, NULL, 'LoadRef=Field Direct'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  -100008, '2024-10-31',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'ANB' ORDER BY StorLoc_ID LIMIT 1),
  11.9, NULL, NULL, 2812.3,
  NULL, 4.02, 11305.446, NULL, 'LoadRef=Field Direct'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  1, '2024-11-01',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin8' ORDER BY StorLoc_ID LIMIT 1),
  12.3, 61530, 26100, 632.6786,
  NULL, 3.98, 2518.0607, NULL, 'LoadRef=S1'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  2, '2024-11-07',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin6' ORDER BY StorLoc_ID LIMIT 1),
  13.9, 57510, 26040, 561.9643,
  NULL, 3.98, 2236.6179, NULL, 'LoadRef=S2'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  3, '2024-11-07',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin6' ORDER BY StorLoc_ID LIMIT 1),
  14, 56560, 26230, 541.6071,
  NULL, 3.98, 2155.5964, NULL, 'LoadRef=S3'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  4, '2024-11-08',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'SCB' ORDER BY StorLoc_ID LIMIT 1),
  13.9, 60320, 26030, 612.3214,
  NULL, 3.98, 2437.0393, NULL, 'LoadRef=S4'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  5, '2024-11-14',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin15' ORDER BY StorLoc_ID LIMIT 1),
  11, 59600, 26010, 599.8214,
  NULL, 3.98, 2387.2893, NULL, 'LoadRef=S5'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  6, '2024-11-14',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin14' ORDER BY StorLoc_ID LIMIT 1),
  12, 60180, 25960, 611.0714,
  NULL, 3.98, 2432.0643, NULL, 'LoadRef=S6'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  7, '2024-11-14',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin13' ORDER BY StorLoc_ID LIMIT 1),
  11.7, 59530, 26020, 598.3929,
  NULL, 3.98, 2381.6036, NULL, 'LoadRef=S7'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  8, '2024-11-20',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin12' ORDER BY StorLoc_ID LIMIT 1),
  15.4, 59910, 26140, 603.0357,
  NULL, 3.98, 2400.0821, NULL, 'LoadRef=S8'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  9, '2024-11-20',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'SCB' ORDER BY StorLoc_ID LIMIT 1),
  12.6, 60600, 26120, 615.7143,
  NULL, 3.98, 2450.5429, NULL, 'LoadRef=S9'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  10, '2024-11-22',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin4' ORDER BY StorLoc_ID LIMIT 1),
  12.2, 60620, 26230, 614.1071,
  NULL, 3.98, 2444.1464, NULL, 'LoadRef=S10'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  11, '2024-11-22',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin12' ORDER BY StorLoc_ID LIMIT 1),
  15.5, 56280, 26210, 536.9643,
  NULL, 3.98, 2137.1179, NULL, 'LoadRef=S11'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  12, '2024-11-22',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin12' ORDER BY StorLoc_ID LIMIT 1),
  15.5, 57380, 26270, 555.5357,
  NULL, 3.98, 2211.0321, NULL, 'LoadRef=S12'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  13, '2024-11-25',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin12' ORDER BY StorLoc_ID LIMIT 1),
  15.5, 58250, 26270, 571.0714,
  NULL, 3.98, 2272.8643, NULL, 'LoadRef=S13'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  14, '2024-11-26',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin9' ORDER BY StorLoc_ID LIMIT 1),
  13, 56330, 26270, 536.7857,
  NULL, 3.98, 2136.4071, NULL, 'LoadRef=S14'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  15, '2024-11-26',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin9' ORDER BY StorLoc_ID LIMIT 1),
  13.4, 58320, 26220, 573.2143,
  NULL, 3.98, 2281.3929, NULL, 'LoadRef=S15'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  16, '2024-11-26',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin9' ORDER BY StorLoc_ID LIMIT 1),
  13.5, 60520, 26250, 611.9643,
  NULL, 3.98, 2435.6179, NULL, 'LoadRef=S16'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  17, '2024-12-03',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin12' ORDER BY StorLoc_ID LIMIT 1),
  15.5, 59570, 26250, 595,
  NULL, 4.13, 2457.35, NULL, 'LoadRef=S17'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  18, '2024-12-04',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin12' ORDER BY StorLoc_ID LIMIT 1),
  15.5, 60320, 26210, 609.1071,
  NULL, 4.13, 2515.6125, NULL, 'LoadRef=S18'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  19, '2024-12-06',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin12' ORDER BY StorLoc_ID LIMIT 1),
  15.5, 59400, 26150, 593.75,
  NULL, 4.13, 2452.1875, NULL, 'LoadRef=S19'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  20, '2024-12-06',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin12' ORDER BY StorLoc_ID LIMIT 1),
  15.5, 60610, 26190, 614.6429,
  NULL, 4.13, 2538.475, NULL, 'LoadRef=S20'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  21, '2024-12-10',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin12' ORDER BY StorLoc_ID LIMIT 1),
  15.5, 59050, 26160, 587.3214,
  NULL, 4.13, 2425.6375, NULL, 'LoadRef=S21'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  22, '2024-12-10',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin12' ORDER BY StorLoc_ID LIMIT 1),
  15.5, 58950, 26250, 583.9286,
  NULL, 4.13, 2411.625, NULL, 'LoadRef=S22'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  23, '2024-12-16',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin12' ORDER BY StorLoc_ID LIMIT 1),
  14.9, 59640, 26020, 600.3571,
  NULL, 4.13, 2479.475, NULL, 'LoadRef=S23'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  24, '2024-12-16',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin12' ORDER BY StorLoc_ID LIMIT 1),
  14.2, 60020, 26030, 606.9643,
  NULL, 4.13, 2506.7625, NULL, 'LoadRef=S24'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  25, '2024-12-17',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin12' ORDER BY StorLoc_ID LIMIT 1),
  14.2, 58730, 26250, 580,
  NULL, 4.13, 2395.4, NULL, 'LoadRef=S25'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  26, '2024-12-20',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin12' ORDER BY StorLoc_ID LIMIT 1),
  13.7, 59380, 25990, 596.25,
  NULL, 4.13, 2462.5125, NULL, 'LoadRef=S26'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  27, '2024-12-20',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin12' ORDER BY StorLoc_ID LIMIT 1),
  13.4, 60320, 26060, 611.7857,
  NULL, 4.13, 2526.675, NULL, 'LoadRef=S27'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  28, '2024-12-23',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin12' ORDER BY StorLoc_ID LIMIT 1),
  12.8, 61130, 26220, 623.3929,
  NULL, 4.13, 2574.6125, NULL, 'LoadRef=S28'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  29, '2024-12-30',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin12' ORDER BY StorLoc_ID LIMIT 1),
  12.3, 61200, 26180, 625.3571,
  NULL, 4.13, 2582.725, NULL, 'LoadRef=S29'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  30, '2025-01-02',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin12' ORDER BY StorLoc_ID LIMIT 1),
  12, 58990, 26170, 586.0714,
  NULL, 4.44, 2602.1571, NULL, 'LoadRef=S30'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  31, '2025-01-03',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin12' ORDER BY StorLoc_ID LIMIT 1),
  12.4, 60620, 26060, 617.1429,
  NULL, 4.44, 2740.1143, NULL, 'LoadRef=S31'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  32, '2025-01-08',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin12' ORDER BY StorLoc_ID LIMIT 1),
  11.9, 58460, 26110, 577.6786,
  NULL, 4.44, 2564.8929, NULL, 'LoadRef=S32'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  33, '2025-01-08',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin12' ORDER BY StorLoc_ID LIMIT 1),
  11.9, 59120, 26070, 590.1786,
  NULL, 4.44, 2620.3929, NULL, 'LoadRef=S33'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  34, '2025-01-13',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin12' ORDER BY StorLoc_ID LIMIT 1),
  11.3, 59770, 25990, 603.2143,
  NULL, 4.44, 2678.2714, NULL, 'LoadRef=S34'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  35, '2025-01-16',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin12' ORDER BY StorLoc_ID LIMIT 1),
  11.3, 60240, 26200, 607.8571,
  NULL, 4.44, 2698.8857, NULL, 'LoadRef=S35'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  36, '2025-01-16',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin12' ORDER BY StorLoc_ID LIMIT 1),
  11.5, 58560, 26180, 578.2143,
  NULL, 4.44, 2567.2714, NULL, 'LoadRef=S36'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  37, '2025-01-16',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin12' ORDER BY StorLoc_ID LIMIT 1),
  11.6, 59840, 26210, 600.5357,
  NULL, 4.44, 2666.3786, NULL, 'LoadRef=S37'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  38, '2025-01-17',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin12' ORDER BY StorLoc_ID LIMIT 1),
  11.8, 60960, 26200, 620.7143,
  NULL, 4.44, 2755.9714, NULL, 'LoadRef=S38'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  39, '2025-01-24',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin12' ORDER BY StorLoc_ID LIMIT 1),
  10.4, 59990, 26080, 605.5357,
  NULL, 4.44, 2688.5786, NULL, 'LoadRef=S39'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  40, '2025-01-24',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin12' ORDER BY StorLoc_ID LIMIT 1),
  11.8, 60900, 26140, 620.7143,
  NULL, 4.44, 2755.9714, NULL, 'LoadRef=S40'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  41, '2025-01-28',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin12' ORDER BY StorLoc_ID LIMIT 1),
  12.6, 60570, 26180, 614.1071,
  NULL, 4.44, 2726.6357, NULL, 'LoadRef=S41'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  42, '2025-01-28',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin12' ORDER BY StorLoc_ID LIMIT 1),
  12.5, 57680, 26160, 562.8571,
  NULL, 4.44, 2499.0857, NULL, 'LoadRef=S42'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  -100051, '2025-01-29',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin12' ORDER BY StorLoc_ID LIMIT 1),
  11.2, 37130, 26230, 194.6429,
  NULL, 4.44, 864.2143, NULL, 'LoadRef=S43-01'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  -100052, '2025-01-29',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin9' ORDER BY StorLoc_ID LIMIT 1),
  13.5, 61030, 37130, 426.7857,
  NULL, 4.44, 1894.9286, NULL, 'LoadRef=S43-02'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  44, '2025-01-31',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin10' ORDER BY StorLoc_ID LIMIT 1),
  11.5, 63100, 26270, 657.6786,
  NULL, 4.44, 2920.0929, NULL, 'LoadRef=S44'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  -100054, '2025-02-05',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'Shrink' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin12' ORDER BY StorLoc_ID LIMIT 1),
  NULL, NULL, NULL, 786.4872,
  NULL, 0, 0, NULL, 'LoadRef=Shrink'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  45, '2025-02-05',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin10' ORDER BY StorLoc_ID LIMIT 1),
  12.2, 61500, 26150, 631.25,
  NULL, 4.58, 2891.125, NULL, 'LoadRef=S45'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  46, '2025-02-07',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin10' ORDER BY StorLoc_ID LIMIT 1),
  12.2, 61940, 26290, 636.6071,
  NULL, 4.58, 2915.6607, NULL, 'LoadRef=S46'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  47, '2025-02-10',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin10' ORDER BY StorLoc_ID LIMIT 1),
  12.6, 60570, 26220, 613.3929,
  NULL, 4.58, 2809.3393, NULL, 'LoadRef=S47'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  48, '2025-02-13',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin10' ORDER BY StorLoc_ID LIMIT 1),
  12.2, 60980, 26270, 619.8214,
  NULL, 4.58, 2838.7821, NULL, 'LoadRef=S48'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  49, '2025-02-13',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin10' ORDER BY StorLoc_ID LIMIT 1),
  12.5, 61940, 26280, 636.7857,
  NULL, 4.58, 2916.4786, NULL, 'LoadRef=S49'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  50, '2025-02-21',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin10' ORDER BY StorLoc_ID LIMIT 1),
  12.4, 62570, 25920, 654.4643,
  NULL, 4.58, 2997.4464, NULL, 'LoadRef=S50'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  51, '2025-02-25',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin10' ORDER BY StorLoc_ID LIMIT 1),
  12.4, 59780, 26160, 600.3571,
  NULL, 4.58, 2749.6357, NULL, 'LoadRef=S51'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  52, '2025-02-25',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin10' ORDER BY StorLoc_ID LIMIT 1),
  12, 61410, 26140, 629.8214,
  NULL, 4.58, 2884.5821, NULL, 'LoadRef=S52'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  53, '2025-02-27',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin10' ORDER BY StorLoc_ID LIMIT 1),
  11.6, 61510, 26180, 630.8929,
  NULL, 4.58, 2889.4893, NULL, 'LoadRef=S53'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  54, '2025-03-03',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'SCB' ORDER BY StorLoc_ID LIMIT 1),
  11.3, 60240, 26150, 608.75,
  NULL, 4.22, 2568.925, NULL, 'LoadRef=S54'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  55, '2025-03-10',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'SCB' ORDER BY StorLoc_ID LIMIT 1),
  12.4, 59640, 26260, 596.0714,
  NULL, 4.22, 2515.4214, NULL, 'LoadRef=S55'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  56, '2025-03-10',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'SCB' ORDER BY StorLoc_ID LIMIT 1),
  12.2, 60100, 26300, 603.5714,
  NULL, 4.22, 2547.0714, NULL, 'LoadRef=S56'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  57, '2025-03-10',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'SCB' ORDER BY StorLoc_ID LIMIT 1),
  12.3, 60640, 26290, 613.3929,
  NULL, 4.22, 2588.5179, NULL, 'LoadRef=S57'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  58, '2025-03-11',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'SCB' ORDER BY StorLoc_ID LIMIT 1),
  12.6, 60010, 26280, 602.3214,
  NULL, 4.22, 2541.7964, NULL, 'LoadRef=S58'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  59, '2025-03-11',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'SCB' ORDER BY StorLoc_ID LIMIT 1),
  12.6, 60810, 26180, 618.3929,
  NULL, 4.22, 2609.6179, NULL, 'LoadRef=S59'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  60, '2025-03-11',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'SCB' ORDER BY StorLoc_ID LIMIT 1),
  12.4, 59450, 26180, 594.1071,
  NULL, 4.22, 2507.1321, NULL, 'LoadRef=S60'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  61, '2025-03-12',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'SCB' ORDER BY StorLoc_ID LIMIT 1),
  13.3, 60210, 26150, 608.2143,
  NULL, 4.22, 2566.6643, NULL, 'LoadRef=S61'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  62, '2025-03-17',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  13.8, 60140, 26220, 605.7143,
  NULL, 4.22, 2556.1143, NULL, 'LoadRef=S62'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  63, '2025-03-25',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  13.6, 60430, 26210, 611.0714,
  NULL, 4.22, 2578.7214, NULL, 'LoadRef=S63'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  64, '2025-04-01',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  13.6, 60300, 25980, 612.8571,
  NULL, 4.32, 2647.5429, NULL, 'LoadRef=S64'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  65, '2025-04-02',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  13.7, 60080, 26100, 606.7857,
  NULL, 4.32, 2621.3143, NULL, 'LoadRef=S65'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  66, '2025-04-02',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  13.8, 59680, 26050, 600.5357,
  NULL, 4.32, 2594.3143, NULL, 'LoadRef=S66'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  67, '2025-04-02',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  13.8, 60360, 26020, 613.2143,
  NULL, 4.32, 2649.0857, NULL, 'LoadRef=S67'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  68, '2025-04-03',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  14, 60770, 26290, 615.7143,
  NULL, 4.32, 2659.8857, NULL, 'LoadRef=S68'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  69, '2025-04-03',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  14.1, 60250, 26240, 607.3214,
  NULL, 4.32, 2623.6286, NULL, 'LoadRef=S69'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  70, '2025-04-15',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  13.6, 60920, 26490, 614.8214,
  NULL, 4.32, 2656.0286, NULL, 'LoadRef=S70'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  107310, '2025-04-14',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin13' ORDER BY StorLoc_ID LIMIT 1),
  10.6, NULL, NULL, 1174.29,
  '37275', 4.68, 5495.6772, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  107319, '2025-04-14',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin13' ORDER BY StorLoc_ID LIMIT 1),
  10.7, NULL, NULL, 1212.86,
  '37275', 4.68, 5676.1848, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  107346, '2025-04-15',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin13' ORDER BY StorLoc_ID LIMIT 1),
  11, NULL, NULL, 1177.86,
  '37275', 4.68, 5512.3848, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  107350, '2025-04-15',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin13' ORDER BY StorLoc_ID LIMIT 1),
  11.4, NULL, NULL, 1183.57,
  '37275', 4.68, 5539.1076, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  107360, '2025-04-15',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin13' ORDER BY StorLoc_ID LIMIT 1),
  12.3, NULL, NULL, 1191.79,
  '37275', 4.68, 5577.5772, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  107362, '2025-04-15',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin13' ORDER BY StorLoc_ID LIMIT 1),
  12.7, NULL, NULL, 1223.57,
  '37275', 4.68, 5726.3076, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  107369, '2025-04-15',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin13' ORDER BY StorLoc_ID LIMIT 1),
  13.5, NULL, NULL, 1211.07,
  '37275', 4.68, 5667.8076, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  107371, '2025-04-15',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin13' ORDER BY StorLoc_ID LIMIT 1),
  14.1, NULL, NULL, 1233.57,
  '37275', 4.68, 5773.1076, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  10737801, '2025-04-15',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin13' ORDER BY StorLoc_ID LIMIT 1),
  14.5, NULL, NULL, 391.42,
  '37275', 4.68, 1831.8456, NULL, 'LoadRef=107378-01'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  10737802, '2025-04-15',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin13' ORDER BY StorLoc_ID LIMIT 1),
  14.5, NULL, NULL, 811.44,
  '37532', 4.82, 3911.1408, NULL, 'LoadRef=107378-02'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  107381, '2025-04-15',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin13' ORDER BY StorLoc_ID LIMIT 1),
  14.9, NULL, NULL, 1177.5,
  '37532', 4.82, 5675.55, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  107388, '2025-04-15',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin13' ORDER BY StorLoc_ID LIMIT 1),
  15.4, NULL, NULL, 1207.5,
  '37532', 4.82, 5783.92, 36.23, '3 cents/bu drying charge'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  107407, '2025-04-16',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin13' ORDER BY StorLoc_ID LIMIT 1),
  14.9, NULL, NULL, 1182.14,
  '37532', 4.82, 5697.9148, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  107453, '2025-04-17',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin13' ORDER BY StorLoc_ID LIMIT 1),
  14.4, NULL, NULL, 1182.5,
  '37532', 4.82, 5699.65, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  107581, '2025-04-21',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin13' ORDER BY StorLoc_ID LIMIT 1),
  13.7, NULL, NULL, 1191.43,
  '37532', 4.82, 5742.6926, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  107613, '2025-04-22',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin13' ORDER BY StorLoc_ID LIMIT 1),
  13.8, NULL, NULL, 1188.21,
  '37532', 4.82, 5727.1722, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  107622, '2025-04-22',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin13' ORDER BY StorLoc_ID LIMIT 1),
  13.7, NULL, NULL, 1195.36,
  '37532', 4.82, 5761.6352, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  10762801, '2025-04-22',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin14' ORDER BY StorLoc_ID LIMIT 1),
  10.5, NULL, NULL, 863.92,
  '37532', 4.82, 4164.0944, NULL, 'LoadRef=107628-01'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  10762802, '2025-04-22',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin14' ORDER BY StorLoc_ID LIMIT 1),
  10.5, NULL, NULL, 334.29,
  '37127', 4.54, 1517.6766, NULL, 'LoadRef=107628-02'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  71, '2025-04-21',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  13.7, 59500, 26180, 595,
  NULL, 4.32, 2570.4, NULL, 'LoadRef=S71'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  72, '2025-04-21',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  13.5, 59440, 26140, 594.6429,
  NULL, 4.32, 2568.8571, NULL, 'LoadRef=S72'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  73, '2025-04-21',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  14, 59690, 26100, 599.8214,
  NULL, 4.32, 2591.2286, NULL, 'LoadRef=S73'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  74, '2025-04-22',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  14, 59580, 26330, 593.75,
  NULL, 4.32, 2565, NULL, 'LoadRef=S74'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  75, '2025-04-22',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  14, 60170, 26280, 605.1786,
  NULL, 4.32, 2614.3714, NULL, 'LoadRef=S75'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  631015, '2025-04-22',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  7.9, NULL, NULL, 1051.22,
  '206931', 10.24, 10757.9928, 6.5, '.2% FM 2.11bu'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  631041, '2025-04-22',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  7.9, NULL, NULL, 1095.67,
  '206931', 10.24, 11213.1608, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  631052, '2025-04-22',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  7.7, NULL, NULL, 1105.67,
  '206931', 10.24, 11315.5608, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  631080, '2025-04-22',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  7.5, NULL, NULL, 1081.33,
  '206931', 10.24, 11066.3192, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  631095, '2025-04-22',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  7.5, NULL, NULL, 1115.33,
  '206931', 10.24, 11414.4792, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  631115, '2025-04-22',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  7.4, NULL, NULL, 1091.33,
  '206931', 10.24, 11168.7192, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  631124, '2025-04-22',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  7.5, NULL, NULL, 938.67,
  '206931', 10.24, 9605.4808, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  631150, '2025-04-23',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  7.5, NULL, NULL, 1112,
  '206931', 10.24, 11380.38, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  631164, '2025-04-23',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  7.6, NULL, NULL, 1143.67,
  '206931', 10.24, 11704.6808, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  631184, '2025-04-23',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  7.5, NULL, NULL, 1134.33,
  '206931', 10.24, 11609.0392, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  631254, '2025-04-23',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  7.4, NULL, NULL, 1105,
  '206931', 10.24, 11308.7, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  63129001, '2025-04-23',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  7.5, NULL, NULL, 1025.78,
  '206931', 10.24, 10497.4872, 6.5, 'LoadRef=631290-01'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  63129002, '2025-04-23',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  7.5, NULL, NULL, 72.55,
  'S223207', 10.43, 756.2665, 0.43, 'LoadRef=631290-02'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  76, '2025-04-29',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  13.7, 59550, 26200, 595.5357,
  NULL, 4.32, 2572.7143, NULL, 'LoadRef=S76'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  77, '2025-04-29',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  13.6, 60010, 26250, 602.8571,
  NULL, 4.32, 2604.3429, NULL, 'LoadRef=S77'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  78, '2025-05-09',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin13' ORDER BY StorLoc_ID LIMIT 1),
  12.5, 50590, 26260, 434.4643,
  NULL, 4.28, 1859.5071, NULL, 'LoadRef=S78; Last Load Bin 13'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  -100121, '2025-05-09',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'Shrink' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin13' ORDER BY StorLoc_ID LIMIT 1),
  NULL, NULL, NULL, -17.948,
  NULL, 0, 0, NULL, 'LoadRef=Shrink'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  631850, '2025-05-05',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  7.9, NULL, NULL, 1126.67,
  '207773', 10.35, 11654.5345, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  632481, '2025-05-08',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  7.6, NULL, NULL, 1120,
  '207773', 10.35, 11585.5, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  632813, '2025-05-13',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  7.5, NULL, NULL, 1038.33,
  '207773', 10.35, 10740.2155, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  633240, '2025-05-16',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  7.8, NULL, NULL, 1120.33,
  '207773', 10.35, 11588.9155, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  63324901, '2025-05-16',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  7.8, NULL, NULL, 594.67,
  '207773', 10.35, 6151.1945, 3.64, 'LoadRef=633249-01'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  63324902, '2025-05-16',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  7.8, NULL, NULL, 467.66,
  '207877', 10.52, 4916.9232, 2.86, 'LoadRef=633249-02'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  108613, '2025-05-09',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin14' ORDER BY StorLoc_ID LIMIT 1),
  10.5, NULL, NULL, 1186.79,
  '37127', 4.54, 5388.0266, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  108625, '2025-05-09',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin14' ORDER BY StorLoc_ID LIMIT 1),
  10.6, NULL, NULL, 1201.07,
  '37127', 4.54, 5452.8578, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  108708, '2025-05-12',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin14' ORDER BY StorLoc_ID LIMIT 1),
  10.7, NULL, NULL, 1190.36,
  '37127', 4.54, 5404.2344, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  108714, '2025-05-13',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin14' ORDER BY StorLoc_ID LIMIT 1),
  10.8, NULL, NULL, 1185,
  '37127', 4.54, 5379.9, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  108718, '2025-05-13',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin14' ORDER BY StorLoc_ID LIMIT 1),
  11, NULL, NULL, 1156.07,
  '37127', 4.54, 5248.5578, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  108727, '2025-05-13',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin14' ORDER BY StorLoc_ID LIMIT 1),
  11.1, NULL, NULL, 1173.93,
  '37127', 4.54, 5329.6422, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  108732, '2025-05-13',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin14' ORDER BY StorLoc_ID LIMIT 1),
  11, NULL, NULL, 1175.71,
  '37127', 4.54, 5337.7234, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  108739, '2025-05-13',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin14' ORDER BY StorLoc_ID LIMIT 1),
  11.2, NULL, NULL, 1193.21,
  '37127', 4.54, 5417.1734, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  108748, '2025-05-13',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin14' ORDER BY StorLoc_ID LIMIT 1),
  11.3, NULL, NULL, 1173.21,
  '37127', 4.54, 5326.3734, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  108758, '2025-05-13',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin14' ORDER BY StorLoc_ID LIMIT 1),
  11.4, NULL, NULL, 1239.64,
  '37127', 4.54, 5627.9656, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  108775, '2025-05-13',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin14' ORDER BY StorLoc_ID LIMIT 1),
  11.5, NULL, NULL, 1148.21,
  '37127', 4.54, 5212.8734, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  108786, '2025-05-13',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin14' ORDER BY StorLoc_ID LIMIT 1),
  11.8, NULL, NULL, 1195,
  '37127', 4.54, 5425.3, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  10879501, '2025-05-13',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin14' ORDER BY StorLoc_ID LIMIT 1),
  12.3, NULL, NULL, 447.51,
  '37127', 4.54, 2031.6954, NULL, 'LoadRef=108795-01'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  10879502, '2025-05-13',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin14' ORDER BY StorLoc_ID LIMIT 1),
  12.3, NULL, NULL, 727.49,
  '37619', 4.47, 3251.8803, NULL, 'LoadRef=108795-02'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  108804, '2025-05-14',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin14' ORDER BY StorLoc_ID LIMIT 1),
  12.4, NULL, NULL, 1175.71,
  '37619', 4.47, 5255.4237, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  108916, '2025-05-15',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin15' ORDER BY StorLoc_ID LIMIT 1),
  9.9, NULL, NULL, 1186.79,
  '37619', 4.47, 5304.9513, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  108936, '2025-05-15',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin15' ORDER BY StorLoc_ID LIMIT 1),
  10.1, NULL, NULL, 1179.29,
  '37619', 4.47, 5271.4263, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  108956, '2025-05-15',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin15' ORDER BY StorLoc_ID LIMIT 1),
  10.7, NULL, NULL, 1233.21,
  '37619', 4.47, 5512.4487, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  10934801, '2025-05-22',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'SCB' ORDER BY StorLoc_ID LIMIT 1),
  12.6, NULL, NULL, 497.51,
  '37619', 4.47, 2223.8697, NULL, 'LoadRef=109348-01; 37619 50bu from Bin 15 - auger broke'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  10934802, '2025-05-22',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'SCB' ORDER BY StorLoc_ID LIMIT 1),
  12.6, NULL, NULL, 738.92,
  '37620', 4.51, 3332.5292, NULL, 'LoadRef=109348-02'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  79, '2025-05-13',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  13.6, 60330, 26420, 605.5357,
  NULL, 4.28, 2591.6929, NULL, 'LoadRef=S79'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  80, '2025-05-13',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  13.5, 59730, 26440, 594.4643,
  NULL, 4.28, 2544.3071, NULL, 'LoadRef=S80'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  634011, '2025-05-22',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  7.8, NULL, NULL, 1100,
  '207877', 10.52, 11565.5, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  634176, '2025-05-27',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  7.7, NULL, NULL, 1109.33,
  '207877', 10.52, 11663.6516, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  634281, '2025-05-27',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  7.8, NULL, NULL, 1100.67,
  '207877', 10.52, 11572.5484, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  63430001, '2025-05-28',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  7.6, NULL, NULL, 222.34,
  '207877', 10.52, 2337.7268, 1.29, 'LoadRef=634300-01'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  63430002, '2025-05-28',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  7.6, NULL, NULL, 897.33,
  '207632', 10, 8968.09, 5.21, 'LoadRef=634300-02'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  81, '2025-05-21',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin14' ORDER BY StorLoc_ID LIMIT 1),
  12.3, 59990, 26200, 603.3929,
  NULL, 4.28, 2582.5214, NULL, 'LoadRef=S81'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  82, '2025-05-21',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin14' ORDER BY StorLoc_ID LIMIT 1),
  12.4, 46810, 26160, 368.75,
  NULL, 4.28, 1578.25, NULL, 'LoadRef=S82; Last Load Bin 14'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  -100157, '2025-05-27',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'Shrink' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin14' ORDER BY StorLoc_ID LIMIT 1),
  NULL, NULL, NULL, 5.7729,
  NULL, 0, 0, NULL, 'LoadRef=Shrink'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  83, '2025-05-27',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  14, 59920, 26360, 599.2857,
  NULL, 4.28, 2564.9429, NULL, 'LoadRef=S83'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  84, '2025-05-28',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  14.1, 59480, 26280, 592.8571,
  NULL, 4.28, 2537.4286, NULL, 'LoadRef=S84'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  85, '2025-05-28',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  14.2, 60980, 26290, 619.4643,
  NULL, 4.28, 2651.3071, NULL, 'LoadRef=S85'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  86, '2025-05-28',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  14.3, 59320, 26280, 590,
  NULL, 4.28, 2525.2, NULL, 'LoadRef=S86'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  87, '2025-05-29',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  14.1, 59670, 26250, 596.7857,
  NULL, 4.28, 2554.2429, NULL, 'LoadRef=S87'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  88, '2025-05-29',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  13.9, 60460, 26250, 610.8929,
  NULL, 4.28, 2614.6214, NULL, 'LoadRef=S88'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  89, '2025-05-30',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  14.1, 59370, 26250, 591.4286,
  NULL, 4.28, 2531.3143, NULL, 'LoadRef=S89'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  90, '2025-06-04',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  13.5, 58860, 26170, 583.75,
  NULL, 4.19, 2445.9125, NULL, 'LoadRef=S90'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  91, '2025-06-04',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  13.8, 59630, 26150, 597.8571,
  NULL, 4.19, 2505.0214, NULL, 'LoadRef=S91'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  92, '2025-06-05',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  13.6, 59360, 26070, 594.4643,
  NULL, 4.19, 2490.8054, NULL, 'LoadRef=S92'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  635889, '2025-06-09',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  7.7, NULL, NULL, 1099.67,
  '207632', 10, 10990.2, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  635977, '2025-06-10',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  7.7, NULL, NULL, 1109.33,
  '207632', 10, 11086.8, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  636001, '2025-06-10',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  7.4, NULL, NULL, 1182.33,
  '207632', 10, 11816.8, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  636018, '2025-06-10',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  7.3, NULL, NULL, 1111.67,
  '207632', 10, 11110.2, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  636175, '2025-06-11',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  7.3, NULL, NULL, 1082.33,
  '207632', 10, 10816.8, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  636257, '2025-06-11',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  7.3, NULL, NULL, 1092,
  '207632', 10, 10913.5, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  636327, '2025-06-12',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  7.4, NULL, NULL, 1102,
  '207632', 10, 11013.5, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  636386, '2025-06-12',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  7.8, NULL, NULL, 1100.67,
  '207632', 10, 11000.2, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  636416, '2025-06-12',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  7.9, NULL, NULL, 1067.33,
  '207632', 10, 10666.8, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  636443, '2025-06-12',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  7.9, NULL, NULL, 1025.33,
  '207632', 10, 10246.8, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  636461, '2025-06-12',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  7.9, NULL, NULL, 1131.33,
  '207632', 10, 11306.8, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  63655901, '2025-06-13',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  7.9, NULL, NULL, 870.01,
  '207632', 10, 8694.69, 5.41, 'LoadRef=636559-01'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  636540, '2025-06-13',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  8, NULL, NULL, 1128.67,
  '207632', 10, 11280.2, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  63655902, '2025-06-13',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  7.9, NULL, NULL, 175.99,
  '207164', 10.21, 1795.7679, 1.09, 'LoadRef=636559-02'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  93, '2025-06-09',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  13.8, 59680, 26220, 597.5,
  NULL, 4.19, 2503.525, NULL, 'LoadRef=S93'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  94, '2025-06-10',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  13.8, 60450, 26230, 611.0714,
  NULL, 4.19, 2560.3893, NULL, 'LoadRef=S94; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  95, '2025-06-10',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  13.8, 60530, 26210, 612.8571,
  NULL, 4.19, 2567.8714, NULL, 'LoadRef=S95; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  96, '2025-06-10',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  13.7, 60140, 26200, 606.0714,
  NULL, 4.19, 2539.4393, NULL, 'LoadRef=S96; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  97, '2025-06-11',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  13.6, 44810, 26240, 331.6071,
  NULL, 4.19, 1389.4339, NULL, 'LoadRef=S97; HM Recon, LAST LOAD BIN 11'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  -100187, '2025-06-13',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'Shrink' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin11' ORDER BY StorLoc_ID LIMIT 1),
  NULL, NULL, NULL, -603.6014,
  NULL, 0, 0, NULL, 'LoadRef=Shrink'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  98, '2025-06-11',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin10' ORDER BY StorLoc_ID LIMIT 1),
  11.5, 61220, 26210, 625.1786,
  NULL, 4.19, 2619.4982, NULL, 'LoadRef=S98; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  99, '2025-06-11',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin10' ORDER BY StorLoc_ID LIMIT 1),
  11.4, 60330, 26150, 610.3571,
  NULL, 4.19, 2557.3964, NULL, 'LoadRef=S99; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  100, '2025-06-11',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin10' ORDER BY StorLoc_ID LIMIT 1),
  11.5, 60570, 26190, 613.9286,
  NULL, 4.19, 2572.3607, NULL, 'LoadRef=S100; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  101, '2025-06-11',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin10' ORDER BY StorLoc_ID LIMIT 1),
  11.6, 60710, 26180, 616.6071,
  NULL, 4.19, 2583.5839, NULL, 'LoadRef=S101; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  102, '2025-06-11',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin10' ORDER BY StorLoc_ID LIMIT 1),
  11.7, 60740, 26270, 615.5357,
  NULL, 4.19, 2579.0946, NULL, 'LoadRef=S102; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  103, '2025-06-11',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin10' ORDER BY StorLoc_ID LIMIT 1),
  11.5, 61440, 26200, 629.2857,
  NULL, 4.19, 2636.7071, NULL, 'LoadRef=S103; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  104, '2025-06-11',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin10' ORDER BY StorLoc_ID LIMIT 1),
  11.6, 61530, 26200, 630.8929,
  NULL, 4.19, 2643.4411, NULL, 'LoadRef=S104; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  105, '2025-06-12',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin10' ORDER BY StorLoc_ID LIMIT 1),
  12, 60150, 26400, 602.6786,
  NULL, 4.19, 2525.2232, NULL, 'LoadRef=S105'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  106, '2025-06-12',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin10' ORDER BY StorLoc_ID LIMIT 1),
  12.1, 60560, 26470, 608.75,
  NULL, 4.19, 2550.6625, NULL, 'LoadRef=S106; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  107, '2025-06-12',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin10' ORDER BY StorLoc_ID LIMIT 1),
  12, 60930, 26450, 615.7143,
  NULL, 4.19, 2579.8429, NULL, 'LoadRef=S107; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  108, '2025-06-12',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin10' ORDER BY StorLoc_ID LIMIT 1),
  12.2, 61530, 26470, 626.0714,
  NULL, 4.19, 2623.2393, NULL, 'LoadRef=S108; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  109, '2025-06-12',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin10' ORDER BY StorLoc_ID LIMIT 1),
  12.3, 60670, 26410, 611.7857,
  NULL, 4.19, 2563.3821, NULL, 'LoadRef=S109'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  110445, '2025-06-13',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'SCB' ORDER BY StorLoc_ID LIMIT 1),
  12.5, NULL, NULL, 1185,
  '37620', 4.51, 5344.35, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  110456, '2025-06-13',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'SCB' ORDER BY StorLoc_ID LIMIT 1),
  12.9, NULL, NULL, 1194.29,
  '37620', 4.51, 5386.2479, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  110463, '2025-06-13',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'SCB' ORDER BY StorLoc_ID LIMIT 1),
  12.5, NULL, NULL, 1273.93,
  '37620', 4.51, 5745.4243, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  110598, '2025-06-17',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'SCB' ORDER BY StorLoc_ID LIMIT 1),
  13.1, NULL, NULL, 1230.71,
  '37620', 4.51, 5550.5021, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  11061401, '2025-06-17',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'SCB' ORDER BY StorLoc_ID LIMIT 1),
  12.8, NULL, NULL, 377.15,
  '37620', 4.51, 1700.9465, NULL, 'LoadRef=110614-01'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  110, '2025-06-13',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin10' ORDER BY StorLoc_ID LIMIT 1),
  12.3, 60520, 26310, 610.8929,
  NULL, 4.19, 2559.6411, NULL, 'LoadRef=S110'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  111, '2025-06-13',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin10' ORDER BY StorLoc_ID LIMIT 1),
  12.3, 60600, 26420, 610.3571,
  NULL, 4.19, 2557.3964, NULL, 'LoadRef=S111; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  112, '2025-06-13',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin10' ORDER BY StorLoc_ID LIMIT 1),
  12.2, 61620, 26390, 629.1071,
  NULL, 4.19, 2635.9589, NULL, 'LoadRef=S112; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  113, '2025-06-13',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin10' ORDER BY StorLoc_ID LIMIT 1),
  12.3, 60520, 26440, 608.5714,
  NULL, 4.19, 2549.9143, NULL, 'LoadRef=S113; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  114, '2025-06-13',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin10' ORDER BY StorLoc_ID LIMIT 1),
  12.4, 60520, 26450, 608.3929,
  NULL, 4.19, 2549.1661, NULL, 'LoadRef=S114; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  115, '2025-06-13',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin10' ORDER BY StorLoc_ID LIMIT 1),
  12.3, 61300, 26480, 621.7857,
  NULL, 4.19, 2605.2821, NULL, 'LoadRef=S115; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  116, '2025-06-13',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin10' ORDER BY StorLoc_ID LIMIT 1),
  12.3, 60670, 26360, 612.6786,
  NULL, 4.19, 2567.1232, NULL, 'LoadRef=S116'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  11061402, '2025-06-17',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'SCB' ORDER BY StorLoc_ID LIMIT 1),
  12.8, NULL, NULL, 903.56,
  '37696', 4.72, 4264.8032, NULL, 'LoadRef=110614-02'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  110620, '2025-06-17',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'SCB' ORDER BY StorLoc_ID LIMIT 1),
  12.5, NULL, NULL, 1182.86,
  '37696', 4.72, 5583.0992, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  110631, '2025-06-17',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'SCB' ORDER BY StorLoc_ID LIMIT 1),
  11.8, NULL, NULL, 1234.29,
  '37696', 4.72, 5825.8488, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  110696, '2025-06-18',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'SCB' ORDER BY StorLoc_ID LIMIT 1),
  12.2, NULL, NULL, 1188.93,
  '37696', 4.72, 5611.7496, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  110731, '2025-06-18',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'SCB' ORDER BY StorLoc_ID LIMIT 1),
  12.5, NULL, NULL, 1184.29,
  '37696', 4.72, 5589.8488, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  110887, '2025-06-20',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin9' ORDER BY StorLoc_ID LIMIT 1),
  13.2, NULL, NULL, 1165,
  '37696', 4.72, 5498.8, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  110902, '2025-06-20',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin9' ORDER BY StorLoc_ID LIMIT 1),
  13.7, NULL, NULL, 1173.93,
  '37696', 4.72, 5540.9496, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  110917, '2025-06-20',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin9' ORDER BY StorLoc_ID LIMIT 1),
  13.6, NULL, NULL, 1184.64,
  '37696', 4.72, 5591.5008, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  11093301, '2025-06-20',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin9' ORDER BY StorLoc_ID LIMIT 1),
  13.9, NULL, NULL, 782.5,
  '37696', 4.72, 3693.4, NULL, 'LoadRef=110933-01'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  11093302, '2025-06-20',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin9' ORDER BY StorLoc_ID LIMIT 1),
  13.9, NULL, NULL, 383.21,
  'S032060', 4.24, 1624.8104, NULL, 'LoadRef=110933-02'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  117, '2025-07-02',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin10' ORDER BY StorLoc_ID LIMIT 1),
  13.1, 60470, 26310, 610,
  NULL, 4.19, 2555.9, NULL, 'LoadRef=S117'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  118, '2025-07-02',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin10' ORDER BY StorLoc_ID LIMIT 1),
  13.2, 60260, 26360, 605.3571,
  NULL, 4.19, 2536.4464, NULL, 'LoadRef=S118'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  119, '2025-07-03',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin10' ORDER BY StorLoc_ID LIMIT 1),
  13, 60410, 26300, 609.1071,
  NULL, 4.19, 2552.1589, NULL, 'LoadRef=S119'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  120, '2025-06-19',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin10' ORDER BY StorLoc_ID LIMIT 1),
  13.2, 60640, 26330, 612.6786,
  NULL, 4.19, 2567.1232, NULL, 'LoadRef=S120'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  121, '2025-06-19',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin10' ORDER BY StorLoc_ID LIMIT 1),
  13.7, 60220, 26040, 610.3571,
  NULL, 4.19, 2557.3964, NULL, 'LoadRef=S121'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  122, '2025-06-19',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin10' ORDER BY StorLoc_ID LIMIT 1),
  13.5, 50690, 26000, 440.8929,
  NULL, 4.19, 1847.3411, NULL, 'LoadRef=S122; HM Recon  Last Load Bin 10'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  -100228, '2025-06-19',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'Shrink' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin10' ORDER BY StorLoc_ID LIMIT 1),
  NULL, NULL, NULL, -520.0714,
  NULL, 0, 0, NULL, 'LoadRef=Shrink'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  123, '2025-06-19',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin9' ORDER BY StorLoc_ID LIMIT 1),
  12.9, 60240, 26310, 605.8929,
  NULL, 4.19, 2538.6911, NULL, 'LoadRef=S123; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  124, '2025-06-20',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin9' ORDER BY StorLoc_ID LIMIT 1),
  12.9, 59230, 26220, 589.4643,
  NULL, 4.19, 2469.8554, NULL, 'LoadRef=S124; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  125, '2025-06-20',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin4' ORDER BY StorLoc_ID LIMIT 1),
  10.8, 59310, 26230, 590.7143,
  NULL, 4.19, 2475.0929, NULL, 'LoadRef=S125; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  126, '2025-06-20',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin4' ORDER BY StorLoc_ID LIMIT 1),
  10.5, 60320, 26250, 608.3929,
  NULL, 4.19, 2549.1661, NULL, 'LoadRef=S126; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  127, '2025-06-20',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin4' ORDER BY StorLoc_ID LIMIT 1),
  11.1, 58990, 26270, 584.2857,
  NULL, 4.19, 2448.1571, NULL, 'LoadRef=S127; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  128, '2025-06-27',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin4' ORDER BY StorLoc_ID LIMIT 1),
  11.3, 58800, 26290, 580.5357,
  NULL, 4.19, 2432.4446, NULL, 'LoadRef=S128; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  129, '2025-06-27',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin4' ORDER BY StorLoc_ID LIMIT 1),
  11.4, 59560, 26320, 593.5714,
  NULL, 4.19, 2487.0643, NULL, 'LoadRef=S129; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  130, '2025-06-27',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin4' ORDER BY StorLoc_ID LIMIT 1),
  11.3, 60370, 26300, 608.3929,
  NULL, 4.19, 2549.1661, NULL, 'LoadRef=S130; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  131, '2025-06-27',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin4' ORDER BY StorLoc_ID LIMIT 1),
  11.4, 60620, 26330, 612.3214,
  NULL, 4.19, 2565.6268, NULL, 'LoadRef=S131; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  132, '2025-06-27',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin9' ORDER BY StorLoc_ID LIMIT 1),
  13.5, 59420, 26310, 591.25,
  NULL, 4.19, 2477.3375, NULL, 'LoadRef=S132; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  133, '2025-06-30',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin9' ORDER BY StorLoc_ID LIMIT 1),
  13.6, 60920, 26000, 623.5714,
  NULL, 4.19, 2612.7643, NULL, 'LoadRef=S133; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  134, '2025-06-30',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin9' ORDER BY StorLoc_ID LIMIT 1),
  13.6, 56890, 24390, 580.3571,
  NULL, 4.19, 2431.6964, NULL, 'LoadRef=S134; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  135, '2025-06-30',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin9' ORDER BY StorLoc_ID LIMIT 1),
  13.7, 59880, 26180, 601.7857,
  NULL, 4.19, 2521.4821, NULL, 'LoadRef=S135; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  136, '2025-06-30',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin9' ORDER BY StorLoc_ID LIMIT 1),
  13.5, 55550, 24740, 550.1786,
  NULL, 4.19, 2305.2482, NULL, 'LoadRef=S136; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  137, '2025-06-30',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin9' ORDER BY StorLoc_ID LIMIT 1),
  13.7, 60250, 26290, 606.4286,
  NULL, 4.19, 2540.9357, NULL, 'LoadRef=S137; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  138, '2025-06-30',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin9' ORDER BY StorLoc_ID LIMIT 1),
  13.6, 56110, 24730, 560.3571,
  NULL, 4.19, 2347.8964, NULL, 'LoadRef=S138; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  139, '2025-06-30',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin9' ORDER BY StorLoc_ID LIMIT 1),
  13.6, 60190, 26200, 606.9643,
  NULL, 4.19, 2543.1804, NULL, 'LoadRef=S139; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  140, '2025-07-01',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'SCB' ORDER BY StorLoc_ID LIMIT 1),
  12.3, 57460, 26200, 558.2143,
  NULL, 4.06, 2266.35, NULL, 'LoadRef=S140'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  141, '2025-07-01',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'SCB' ORDER BY StorLoc_ID LIMIT 1),
  12.3, 36400, 24200, 217.8571,
  NULL, 4.06, 884.5, NULL, 'LoadRef=S141; HM Recon Last Load SCB'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  142, '2025-07-01',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin4' ORDER BY StorLoc_ID LIMIT 1),
  12.6, 57990, 26240, 566.9643,
  NULL, 4.06, 2301.875, NULL, 'LoadRef=S142'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  143, '2025-07-01',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin4' ORDER BY StorLoc_ID LIMIT 1),
  12.6, 60810, 26210, 617.8571,
  NULL, 4.06, 2508.5, NULL, 'LoadRef=S143'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  -100250, '2025-07-07',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'Shrink' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'SCB' ORDER BY StorLoc_ID LIMIT 1),
  NULL, NULL, NULL, 536.7846,
  NULL, 0, 0, NULL, 'LoadRef=Shrink'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  638333, '2025-07-07',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  8.8, NULL, NULL, 1074,
  '207164', 10.21, 10959.04, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  638391, '2025-07-07',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  8.1, NULL, NULL, 1064.67,
  '207164', 10.21, 10863.7807, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  638612, '2025-07-09',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  8.1, NULL, NULL, 1060.33,
  '207164', 10.21, 10819.4693, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  638631, '2025-07-09',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  8.1, NULL, NULL, 1070,
  '207164', 10.21, 10918.2, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  638747, '2025-07-09',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  8.2, NULL, NULL, 1077.67,
  '207164', 10.21, 10996.5107, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  63876801, '2025-07-09',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  8.5, NULL, NULL, 950,
  '207164', 10.21, 9693, 6.5, 'LoadRef=638768-01; split load approx 950bu from 17'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  63876802, '2025-07-09',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  8.5, NULL, NULL, 92.33,
  '207164', 10.21, 942.6893, NULL, 'LoadRef=638768-02; Split load aprox 135 from 16'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  638828, '2025-07-10',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  9.2, NULL, NULL, 1111.33,
  '207164', 10.21, 11340.1793, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  638848, '2025-07-10',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  8.9, NULL, NULL, 1076.33,
  '207164', 10.21, 10982.8293, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  638955, '2025-07-10',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  8.6, NULL, NULL, 1127.67,
  '207164', 10.21, 11507.0107, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  639063, '2025-07-11',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  8.5, NULL, NULL, 1121.67,
  '207164', 10.21, 11445.7507, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  639070, '2025-07-11',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  8.4, NULL, NULL, 1168,
  '207164', 10.21, 11918.78, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  639126, '2025-07-11',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  8.3, NULL, NULL, 1127.67,
  '207164', 10.21, 11507.0107, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  639143, '2025-07-11',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  8.3, NULL, NULL, 1126.67,
  '207164', 10.21, 11496.8007, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  63935501, '2025-07-14',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  8.4, NULL, NULL, 575.67,
  '207164', 10.21, 5874.2207, 3.37, 'LoadRef=639355-01'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  144, '2025-07-09',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin4' ORDER BY StorLoc_ID LIMIT 1),
  13.5, 58530, 26220, 576.9643,
  NULL, 4.06, 2342.475, NULL, 'LoadRef=S144'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  145, '2025-07-09',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin4' ORDER BY StorLoc_ID LIMIT 1),
  13.6, 60380, 26250, 609.4643,
  NULL, 4.06, 2474.425, NULL, 'LoadRef=S145'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  146, '2025-07-09',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin4' ORDER BY StorLoc_ID LIMIT 1),
  13, 59950, 26270, 601.4286,
  NULL, 4.06, 2441.8, NULL, 'LoadRef=S146'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  147, '2025-07-09',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin4' ORDER BY StorLoc_ID LIMIT 1),
  13.2, 60100, 26130, 606.6071,
  NULL, 4.06, 2462.825, NULL, 'LoadRef=S147'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  148, '2025-07-10',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin4' ORDER BY StorLoc_ID LIMIT 1),
  13.6, 59380, 26220, 592.1429,
  NULL, 4.06, 2404.1, NULL, 'LoadRef=S148'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  149, '2025-07-10',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin4' ORDER BY StorLoc_ID LIMIT 1),
  13.1, 59650, 26190, 597.5,
  NULL, 4.06, 2425.85, NULL, 'LoadRef=S149'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  150, '2025-07-10',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin4' ORDER BY StorLoc_ID LIMIT 1),
  13.2, 60070, 26180, 605.1786,
  NULL, 4.06, 2457.025, NULL, 'LoadRef=S150'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  151, '2025-07-11',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin6' ORDER BY StorLoc_ID LIMIT 1),
  12.8, 59350, 26110, 593.5714,
  NULL, 4.06, 2409.9, NULL, 'LoadRef=S151; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  152, '2025-07-11',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin6' ORDER BY StorLoc_ID LIMIT 1),
  13, 59900, 26100, 603.5714,
  NULL, 4.06, 2450.5, NULL, 'LoadRef=S152; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  153, '2025-07-11',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin6' ORDER BY StorLoc_ID LIMIT 1),
  13.5, 60330, 26080, 611.6071,
  NULL, 4.06, 2483.125, NULL, 'LoadRef=S153; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  154, '2025-07-11',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin6' ORDER BY StorLoc_ID LIMIT 1),
  13.8, 59870, 26100, 603.0357,
  NULL, 4.06, 2448.325, NULL, 'LoadRef=S154; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  155, '2025-07-11',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin6' ORDER BY StorLoc_ID LIMIT 1),
  13.8, 60110, 26100, 607.3214,
  NULL, 4.06, 2465.725, NULL, 'LoadRef=S155; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  156, '2025-07-11',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin6' ORDER BY StorLoc_ID LIMIT 1),
  13.7, 60130, 26130, 607.1429,
  NULL, 4.06, 2465, NULL, 'LoadRef=S156; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  157, '2025-07-11',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin6' ORDER BY StorLoc_ID LIMIT 1),
  13.8, 59750, 26130, 600.3571,
  NULL, 4.06, 2437.45, NULL, 'LoadRef=S157; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  158, '2025-07-11',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin6' ORDER BY StorLoc_ID LIMIT 1),
  14, 59990, 26130, 604.6429,
  NULL, 4.06, 2454.85, NULL, 'LoadRef=S158; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  159, '2025-07-11',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin6' ORDER BY StorLoc_ID LIMIT 1),
  13.9, 60570, 26140, 614.8214,
  NULL, 4.06, 2496.175, NULL, 'LoadRef=S159; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  63935502, '2025-07-14',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  8.4, NULL, NULL, 534,
  '207412', 10.62, 5667.95, 3.13, 'LoadRef=639355-02'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  639373, '2025-07-14',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  8.4, NULL, NULL, 1048.67,
  '207412', 10.62, 11130.3754, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  639401, '2025-07-14',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  8.2, NULL, NULL, 1143,
  '207412', 10.62, 12132.16, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  639423, '2025-07-14',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  8.2, NULL, NULL, 1090,
  '207412', 10.62, 11569.3, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  639437, '2025-07-14',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  7.9, NULL, NULL, 1069.67,
  '207412', 10.62, 11353.3954, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  639507, '2025-07-15',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  7.9, NULL, NULL, 1111.33,
  '207412', 10.62, 11795.8246, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  639564, '2025-07-15',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  7.7, NULL, NULL, 1071,
  '207412', 10.62, 11367.52, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  639596, '2025-07-15',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  7.5, NULL, NULL, 1178,
  '207412', 10.62, 12503.86, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  639620, '2025-07-15',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  7.5, NULL, NULL, 1088.33,
  '207412', 10.62, 11551.5646, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  63963601, '2025-07-15',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  7.4, NULL, NULL, 666,
  '207412', 10.62, 7068.96, 3.96, 'LoadRef=639636-01'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  63963602, '2025-07-15',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  7.4, NULL, NULL, 426.67,
  '207567', 10.02, 4272.6934, 2.54, 'LoadRef=639636-02'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  639650, '2025-07-15',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  7.4, NULL, NULL, 1106.33,
  '207567', 10.02, 11078.9266, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  639744, '2025-07-16',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  7.4, NULL, NULL, 1101.67,
  '207567', 10.02, 11032.2334, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  160, '2025-07-14',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin6' ORDER BY StorLoc_ID LIMIT 1),
  13.8, 60690, 26440, 611.6071,
  NULL, 4.06, 2483.125, NULL, 'LoadRef=S160; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  161, '2025-07-14',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin6' ORDER BY StorLoc_ID LIMIT 1),
  13.9, 59860, 26450, 596.6071,
  NULL, 4.06, 2422.225, NULL, 'LoadRef=S161; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  162, '2025-07-14',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin6' ORDER BY StorLoc_ID LIMIT 1),
  14.1, 60430, 26480, 606.25,
  NULL, 4.06, 2461.375, NULL, 'LoadRef=S162; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  163, '2025-07-14',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin6' ORDER BY StorLoc_ID LIMIT 1),
  14.1, 59720, 26420, 594.6429,
  NULL, 4.06, 2414.25, NULL, 'LoadRef=S163; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  164, '2025-07-14',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin6' ORDER BY StorLoc_ID LIMIT 1),
  14, 61400, 26460, 623.9286,
  NULL, 4.06, 2533.15, NULL, 'LoadRef=S164; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  165, '2025-07-15',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin6' ORDER BY StorLoc_ID LIMIT 1),
  13.7, 60580, 26400, 610.3571,
  NULL, 4.06, 2478.05, NULL, 'LoadRef=S165; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  166, '2025-07-16',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin6' ORDER BY StorLoc_ID LIMIT 1),
  14.1, 60440, 26460, 606.7857,
  NULL, 4.06, 2463.55, NULL, 'LoadRef=S166; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  167, '2025-07-17',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin6' ORDER BY StorLoc_ID LIMIT 1),
  14, 60760, 26420, 613.2143,
  NULL, 4.06, 2489.65, NULL, 'LoadRef=S167; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  168, '2025-07-18',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin6' ORDER BY StorLoc_ID LIMIT 1),
  14, 60680, 26420, 611.7857,
  NULL, 4.06, 2483.85, NULL, 'LoadRef=S168; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  639951, '2025-07-17',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  7.4, NULL, NULL, 1072,
  '207567', 10.02, 10734.94, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  639954, '2025-07-17',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  7.3, NULL, NULL, 1075,
  '207567', 10.02, 10765, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  640000, '2025-07-17',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  7.2, NULL, NULL, 1103.33,
  '207567', 10.02, 11048.8666, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  640022, '2025-07-17',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  7.2, NULL, NULL, 1064.33,
  '207567', 10.02, 10658.0866, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  640074, '2025-07-17',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  7.3, NULL, NULL, 1088,
  '207567', 10.02, 10895.26, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  640084, '2025-07-17',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  7.2, NULL, NULL, 1059,
  '207567', 10.02, 10604.68, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  640092, '2025-07-17',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  7.6, NULL, NULL, 1083,
  '207567', 10.02, 10845.16, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  640093, '2025-07-18',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  7.8, NULL, NULL, 1126.33,
  '207567', 10.02, 11279.3266, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  640095, '2025-07-18',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  7.7, NULL, NULL, 1026.67,
  '207567', 10.02, 10280.7334, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  640176, '2025-07-18',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  7.9, NULL, NULL, 1115.33,
  '207567', 10.02, 11169.1066, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  169, '2025-07-16',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin6' ORDER BY StorLoc_ID LIMIT 1),
  13, 59620, 26290, 595.1786,
  NULL, 4.06, 2416.425, NULL, 'LoadRef=S169'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  170, '2025-07-17',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin4' ORDER BY StorLoc_ID LIMIT 1),
  13.8, 54240, 26210, 500.5357,
  NULL, 4.06, 2032.175, NULL, 'LoadRef=S170; Last Load Bin 4'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  329, '2025-07-17',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'Frontier(Mead)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  9, NULL, NULL, 80.67,
  NULL, 9.74, 781.7958, 3.93, 'Last Load Bin 17'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  -100317, '2025-07-18',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'Shrink' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin4' ORDER BY StorLoc_ID LIMIT 1),
  NULL, NULL, NULL, 2822.4464,
  NULL, 0, 0, NULL, 'LoadRef=Shrink; Shrink & Theft'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  -100318, '2025-07-18',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'Shrink' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin17' ORDER BY StorLoc_ID LIMIT 1),
  NULL, NULL, NULL, 275.77,
  NULL, 0, 0, NULL, 'LoadRef=Shrink'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  112594, '2025-07-21',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin15' ORDER BY StorLoc_ID LIMIT 1),
  10.5, NULL, NULL, 1187.14,
  '37572', 4.91, 5828.8574, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  112606, '2025-07-22',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin15' ORDER BY StorLoc_ID LIMIT 1),
  11, NULL, NULL, 1176.79,
  '37572', 4.91, 5778.0389, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  112623, '2025-07-22',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin15' ORDER BY StorLoc_ID LIMIT 1),
  11.2, NULL, NULL, 1214.64,
  '37572', 4.91, 5963.8824, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  112641, '2025-07-22',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin15' ORDER BY StorLoc_ID LIMIT 1),
  11.3, NULL, NULL, 1198.21,
  '37572', 4.91, 5883.2111, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  112656, '2025-07-22',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin15' ORDER BY StorLoc_ID LIMIT 1),
  11.3, NULL, NULL, 1189.29,
  '37572', 4.91, 5839.4139, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  112687, '2025-07-22',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin15' ORDER BY StorLoc_ID LIMIT 1),
  11.1, NULL, NULL, 1209.64,
  '37572', 4.91, 5939.3324, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  112694, '2025-07-23',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin15' ORDER BY StorLoc_ID LIMIT 1),
  11.7, NULL, NULL, 1187.5,
  '37572', 4.91, 5830.625, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  112712, '2025-07-23',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin15' ORDER BY StorLoc_ID LIMIT 1),
  11.8, NULL, NULL, 1178.21,
  '37572', 4.91, 5785.0111, NULL, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  11272401, '2025-07-23',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin15' ORDER BY StorLoc_ID LIMIT 1),
  12, NULL, NULL, 458.58,
  '37572', 4.91, 2251.6278, NULL, 'LoadRef=112724-01'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  11272402, '2025-07-23',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM (LPP Frmnt)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin15' ORDER BY StorLoc_ID LIMIT 1),
  12, NULL, NULL, 712.49,
  'S032330', 3.99, 2842.8351, NULL, 'LoadRef=112724-02'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  171, '2025-07-23',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin6' ORDER BY StorLoc_ID LIMIT 1),
  13.6, 60740, 26360, 613.9286,
  NULL, 4.06, 2492.55, NULL, 'LoadRef=S171'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  172, '2025-07-28',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin6' ORDER BY StorLoc_ID LIMIT 1),
  13.8, 61460, 26290, 628.0357,
  NULL, 4.06, 2549.825, NULL, 'LoadRef=S172'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  173, '2025-07-30',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin6' ORDER BY StorLoc_ID LIMIT 1),
  14.3, 59630, 26230, 596.4286,
  NULL, 4.06, 2421.5, NULL, 'LoadRef=S173'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  174, '2025-07-30',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin6' ORDER BY StorLoc_ID LIMIT 1),
  14.1, 60660, 26270, 614.1071,
  NULL, 4.06, 2493.275, NULL, 'LoadRef=S174'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  175, '2025-07-30',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin6' ORDER BY StorLoc_ID LIMIT 1),
  14.6, 60130, 26210, 605.7143,
  NULL, 4.06, 2459.2, NULL, 'LoadRef=S175'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  176, '2025-08-01',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin6' ORDER BY StorLoc_ID LIMIT 1),
  13.5, 46680, 26060, 368.2143,
  NULL, 3.79, 1395.5321, NULL, 'LoadRef=S176; Last Load Bin 6'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  -100335, '2025-08-01',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'Shrink' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin6' ORDER BY StorLoc_ID LIMIT 1),
  NULL, NULL, NULL, 612.5211,
  NULL, 0, 0, NULL, 'LoadRef=Shrink'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  177, '2025-08-04',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin15' ORDER BY StorLoc_ID LIMIT 1),
  12.9, 59750, 26360, 596.25,
  NULL, 3.79, 2259.7875, NULL, 'LoadRef=S177'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  178, '2025-08-05',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin8' ORDER BY StorLoc_ID LIMIT 1),
  11.9, 59230, 26410, 586.0714,
  NULL, 3.79, 2221.2107, NULL, 'LoadRef=S178'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  179, '2025-08-05',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin8' ORDER BY StorLoc_ID LIMIT 1),
  11.8, 59920, 26350, 599.4643,
  NULL, 3.79, 2271.9696, NULL, 'LoadRef=S179'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  180, '2025-08-05',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin8' ORDER BY StorLoc_ID LIMIT 1),
  11.6, 60270, 26330, 606.0714,
  NULL, 3.79, 2297.0107, NULL, 'LoadRef=S180'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  181, '2025-08-05',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin8' ORDER BY StorLoc_ID LIMIT 1),
  11.7, 60110, 26370, 602.5,
  NULL, 3.79, 2283.475, NULL, 'LoadRef=S181'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  182, '2025-08-05',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin8' ORDER BY StorLoc_ID LIMIT 1),
  11.7, 59760, 26350, 596.6071,
  NULL, 3.79, 2261.1411, NULL, 'LoadRef=S182'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  641186, '2025-07-30',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  8.3, NULL, NULL, 1084,
  '207567', 10.02, 10855.18, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  641195, '2025-07-31',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  8.1, NULL, NULL, 1162.67,
  '207567', 10.02, 11643.4534, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  641281, '2025-07-31',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  8.1, NULL, NULL, 1098.67,
  '207567', 10.02, 11002.1734, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  641376, '2025-08-01',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  8.1, NULL, NULL, 1085.33,
  '207567', 10.02, 10868.5066, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  641388, '2025-08-01',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  8, NULL, NULL, 1157.33,
  '207567', 10.02, 11589.9466, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  64140401, '2025-08-04',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  8.2, NULL, NULL, 964.34,
  '207567', 10.02, 9657.4668, 5.22, 'LoadRef=641404-01'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  64140402, '2025-08-04',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  8.2, NULL, NULL, 235.33,
  'S227595', 9.75, 2293.1875, 1.28, 'LoadRef=641404-02'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  641616, '2025-08-05',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ADM' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  8.3, NULL, NULL, 1064.67,
  'S227596', 9.71, 10331.4457, 6.5, NULL
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  183, '2025-08-06',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin8' ORDER BY StorLoc_ID LIMIT 1),
  12.1, 60250, 26320, 605.8929,
  NULL, 3.79, 2296.3339, NULL, 'LoadRef=S183'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  184, '2025-08-06',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin8' ORDER BY StorLoc_ID LIMIT 1),
  11.9, 60720, 26290, 614.8214,
  NULL, 3.79, 2330.1732, NULL, 'LoadRef=S184'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  185, '2025-08-06',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin8' ORDER BY StorLoc_ID LIMIT 1),
  12, 60690, 26350, 613.2143,
  NULL, 3.79, 2324.0821, NULL, 'LoadRef=S185'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  186, '2025-08-06',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin8' ORDER BY StorLoc_ID LIMIT 1),
  11.9, 60830, 26290, 616.7857,
  NULL, 3.79, 2337.6179, NULL, 'LoadRef=S186'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  59113, '2025-08-07',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'Frontier(Mead)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  8.7, NULL, NULL, 540.67,
  'S114392', 9.31, 4958.4577, 75.18, 'LoadRef=0059113; Bin 16 cleanout'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  59116, '2025-08-07',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'Frontier(Mead)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  9.5, NULL, NULL, 525,
  'S114392', 9.31, 4887.75, NULL, 'LoadRef=0059116; Bin 16 cleanout'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  59112, '2025-08-07',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'Frontier(Mead)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  8.5, NULL, NULL, 549.33,
  'S114392', 9.31, 5114.2623, NULL, 'LoadRef=0059112; Bin 16 cleanout'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  59164, '2025-08-12',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'Frontier(Mead)' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  15.7, NULL, NULL, 189.33,
  'S11452601', 9.7, 1571.491, 265.01, 'Last Load Bin 16 $7.90 grain tax, $257.11 moisture dock'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  187, '2025-08-08',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin8' ORDER BY StorLoc_ID LIMIT 1),
  12.4, 60030, 26260, 603.0357,
  NULL, 3.79, 2285.5054, NULL, 'LoadRef=S187'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  188, '2025-08-08',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin8' ORDER BY StorLoc_ID LIMIT 1),
  12.3, 60610, 26290, 612.8571,
  NULL, 3.79, 2322.7286, NULL, 'LoadRef=S188'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  189, '2025-08-08',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin8' ORDER BY StorLoc_ID LIMIT 1),
  12.4, 59670, 26290, 596.0714,
  NULL, 3.79, 2259.1107, NULL, 'LoadRef=S189'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  190, '2025-08-08',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin8' ORDER BY StorLoc_ID LIMIT 1),
  12.2, 59250, 26240, 589.4643,
  NULL, 3.79, 2234.0696, NULL, 'LoadRef=S190'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  191, '2025-08-12',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin8' ORDER BY StorLoc_ID LIMIT 1),
  11.8, 60750, 26250, 616.0714,
  NULL, 3.79, 2334.9107, NULL, 'LoadRef=S191'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  -100363, '2025-08-12',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'B' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'Shrink' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin16' ORDER BY StorLoc_ID LIMIT 1),
  NULL, NULL, NULL, 362.545,
  NULL, 0, 0, NULL, 'LoadRef=Shrink'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  192, '2025-08-15',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin8' ORDER BY StorLoc_ID LIMIT 1),
  12, 61080, 26390, 619.4643,
  NULL, 3.79, 2347.7696, NULL, 'LoadRef=S192'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  193, '2025-08-18',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin8' ORDER BY StorLoc_ID LIMIT 1),
  12.1, 56290, 24600, 565.8929,
  NULL, 3.79, 2144.7339, NULL, 'LoadRef=S193; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  194, '2025-08-18',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin8' ORDER BY StorLoc_ID LIMIT 1),
  12, 61310, 26510, 621.4286,
  NULL, 3.79, 2355.2143, NULL, 'LoadRef=S194; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  195, '2025-08-18',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin8' ORDER BY StorLoc_ID LIMIT 1),
  12, 60500, 26590, 605.5357,
  NULL, 3.79, 2294.9804, NULL, 'LoadRef=S195; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  196, '2025-08-18',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin15' ORDER BY StorLoc_ID LIMIT 1),
  12.8, 60860, 26570, 612.3214,
  NULL, 3.79, 2320.6982, NULL, 'LoadRef=S196; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  -100369, '2025-08-18',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin8' ORDER BY StorLoc_ID LIMIT 1),
  11.9, 60500, 40580, 355.7143,
  NULL, 3.79, 1348.1571, NULL, 'LoadRef=S197A; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  -100370, '2025-08-18',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin8' ORDER BY StorLoc_ID LIMIT 1),
  11.9, 40580, 26420, 252.8571,
  NULL, 3.79, 958.3286, NULL, 'LoadRef=S197B'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  198, '2025-08-19',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin15' ORDER BY StorLoc_ID LIMIT 1),
  12.8, 58370, 24620, 602.6786,
  NULL, 3.79, 2284.1518, NULL, 'LoadRef=S198'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  199, '2025-08-21',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin15' ORDER BY StorLoc_ID LIMIT 1),
  12.8, 54780, 25690, 519.4643,
  NULL, 3.79, 1968.7696, NULL, 'LoadRef=S199'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  200, '2025-08-22',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin15' ORDER BY StorLoc_ID LIMIT 1),
  12.8, 66070, 28210, 676.0714,
  NULL, 3.79, 2562.3107, NULL, 'LoadRef=S200'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  201, '2025-08-22',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin15' ORDER BY StorLoc_ID LIMIT 1),
  13, 55300, 25670, 529.1071,
  NULL, 3.79, 2005.3161, NULL, 'LoadRef=S201'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  202, '2025-08-25',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin15' ORDER BY StorLoc_ID LIMIT 1),
  12.9, 57720, 24310, 596.6071,
  NULL, 3.79, 2261.1411, NULL, 'LoadRef=S202'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  203, '2025-08-26',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin15' ORDER BY StorLoc_ID LIMIT 1),
  13.3, 60110, 24240, 640.5357,
  NULL, 3.79, 2427.6304, NULL, 'LoadRef=S203'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  204, '2025-08-27',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin15' ORDER BY StorLoc_ID LIMIT 1),
  13.8, 54540, 24270, 540.5357,
  NULL, 3.79, 2048.6304, NULL, 'LoadRef=S204'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  205, '2025-08-28',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin8' ORDER BY StorLoc_ID LIMIT 1),
  13.2, 62440, 24250, 681.9643,
  NULL, 3.79, 2584.6446, NULL, 'LoadRef=S205'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  206, '2025-08-29',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin8' ORDER BY StorLoc_ID LIMIT 1),
  13.6, 58710, 40620, 323.0357,
  NULL, 3.79, 1224.3054, NULL, 'LoadRef=S206'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  207, '2025-08-29',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin8' ORDER BY StorLoc_ID LIMIT 1),
  13.6, 61320, 24440, 658.5714,
  NULL, 3.79, 2495.9857, NULL, 'LoadRef=S207; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  208, '2025-09-03',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin8' ORDER BY StorLoc_ID LIMIT 1),
  13.5, 59720, 24210, 634.1071,
  NULL, 3.81, 2415.9482, NULL, 'LoadRef=S208; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  209, '2025-09-03',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin8' ORDER BY StorLoc_ID LIMIT 1),
  14.1, 58170, 25550, 582.5,
  NULL, 3.81, 2219.325, NULL, 'LoadRef=S209'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  -100383, '2025-09-03',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin8' ORDER BY StorLoc_ID LIMIT 1),
  13.3, 54780, 53020, 31.4286,
  NULL, 3.81, 119.7429, NULL, 'LoadRef=S210A; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  -100384, '2025-09-03',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin8' ORDER BY StorLoc_ID LIMIT 1),
  13.3, 53020, 25520, 491.0714,
  NULL, 3.81, 1870.9821, NULL, 'LoadRef=S210B'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  211, '2025-09-03',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin8' ORDER BY StorLoc_ID LIMIT 1),
  13.7, 55180, 25460, 530.7143,
  NULL, 3.81, 2022.0214, NULL, 'LoadRef=S211'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  212, '2025-09-04',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin8' ORDER BY StorLoc_ID LIMIT 1),
  14.7, 34420, 25460, 160,
  NULL, 3.81, 609.6, NULL, 'LoadRef=S212; HM Recon Last Load Bin 8'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  213, '2025-09-05',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin9' ORDER BY StorLoc_ID LIMIT 1),
  13.9, 53080, 25580, 491.0714,
  NULL, 3.81, 1870.9821, NULL, 'LoadRef=S213; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  214, '2025-09-05',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin9' ORDER BY StorLoc_ID LIMIT 1),
  13.5, 56420, 25620, 550,
  NULL, 3.81, 2095.5, NULL, 'LoadRef=S214; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  215, '2025-09-05',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin9' ORDER BY StorLoc_ID LIMIT 1),
  13.6, 56420, 25590, 550.5357,
  NULL, 3.81, 2097.5411, NULL, 'LoadRef=S215; HM Recon'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  -100390, '2025-09-05',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'Shrink' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin8' ORDER BY StorLoc_ID LIMIT 1),
  NULL, NULL, NULL, -251.1071,
  NULL, 0, 0, NULL, 'LoadRef=Shrink'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  216, '2025-09-18',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin9' ORDER BY StorLoc_ID LIMIT 1),
  13.4, 61250, 27230, 607.5,
  NULL, 3.81, 2314.575, NULL, 'LoadRef=S216'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  217, '2025-09-18',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin9' ORDER BY StorLoc_ID LIMIT 1),
  13.6, 60120, 27280, 586.4286,
  NULL, 3.81, 2234.2929, NULL, 'LoadRef=S217'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  218, '2025-09-18',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin9' ORDER BY StorLoc_ID LIMIT 1),
  13.5, 60250, 27270, 588.9286,
  NULL, 3.81, 2243.8179, NULL, 'LoadRef=S218'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  219, '2025-09-23',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin9' ORDER BY StorLoc_ID LIMIT 1),
  13, 62700, 27350, 631.25,
  NULL, 3.81, 2405.0625, NULL, 'LoadRef=S219'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  220, '2025-09-23',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin9' ORDER BY StorLoc_ID LIMIT 1),
  13.2, 62510, 27370, 627.5,
  NULL, 3.81, 2390.775, NULL, 'LoadRef=S220'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  221, '2025-10-03',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin9' ORDER BY StorLoc_ID LIMIT 1),
  13.3, 63610, 26320, 665.8929,
  NULL, 4.15, 2763.4554, NULL, 'LoadRef=S221'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  222, '2025-10-03',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin9' ORDER BY StorLoc_ID LIMIT 1),
  13.7, 62020, 26320, 637.5,
  NULL, 4.15, 2645.625, NULL, 'LoadRef=S222'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  223, '2025-10-07',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin15' ORDER BY StorLoc_ID LIMIT 1),
  14.2, 36320, 27440, 158.5714,
  NULL, 4.15, 658.0714, NULL, 'LoadRef=S223; Last Load Bin 15'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  224, '2025-10-07',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin9' ORDER BY StorLoc_ID LIMIT 1),
  14.2, 63180, 36220, 481.4286,
  NULL, 4.15, 1997.9286, NULL, 'LoadRef=S224'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  225, '2025-10-07',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANF' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin9' ORDER BY StorLoc_ID LIMIT 1),
  14.1, 63650, 27550, 644.6429,
  NULL, 4.15, 2675.2679, NULL, 'LoadRef=S225'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  226, '2025-10-07',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'ANB' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin9' ORDER BY StorLoc_ID LIMIT 1),
  14, 60790, 27510, 594.2857,
  NULL, 4.15, 2466.2857, NULL, 'LoadRef=S226; Last Load Bin 9'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  -100402, '2025-10-08',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'Shrink' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin15' ORDER BY StorLoc_ID LIMIT 1),
  NULL, NULL, NULL, 534.2379,
  NULL, 0, 0, NULL, 'LoadRef=Shrink'
);

INSERT INTO delivery (
  Ticket_Num, Delivery_Date, Crop_ID, DelLoc_ID, StorLoc_ID,
  MC, Gross_Weight, Tare_Weight, Bushels,
  Delivery_Status, Price, Gross_Sale, Sale_Discounts, Comments
)
VALUES (
  -100403, '2025-10-08',
  (SELECT Crop_ID FROM crop WHERE Crop_Code = 'C' ORDER BY Crop_ID LIMIT 1),
  (SELECT DelLoc_ID FROM delivery_location WHERE DelLoc_code = 'Shrink' ORDER BY DelLoc_ID LIMIT 1),
  (SELECT StorLoc_ID FROM storage_location WHERE Bin_Code = 'Bin9' ORDER BY StorLoc_ID LIMIT 1),
  NULL, NULL, NULL, -626.6551,
  NULL, 0, 0, NULL, 'LoadRef=Shrink'
);

COMMIT;
