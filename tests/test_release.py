import sqlite3
import unittest
from contextlib import redirect_stdout
from io import StringIO
from scripts.deploy_account_updates import apply_schema
from generate_delivery_import_sql import build_insert_sql, DeliveryRow
import test_invitations as invitation_tests

class MigrationTest(invitation_tests.InvitationsTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.tables=('Delivery','password_resets','email_verifications')+cls.tables
    def setUp(self):
        for table in ('Delivery','password_resets','email_verifications'):
            self.sql('DROP TABLE IF EXISTS '+table)
        super().setUp()
    def test_apply_and_rerun_preserves_delivery(self):
        self.sql('CREATE TABLE Delivery (Delivery_ID INT PRIMARY KEY, Grower_ID BIGINT UNSIGNED, Bushels DECIMAL(10,2))')
        self.sql('INSERT INTO Delivery VALUES (1,1,123.45)')
        conn=self.connect()
        try:
            with redirect_stdout(StringIO()):apply_schema(conn)
            self.sql('UPDATE Delivery SET Crop_Year=2025 WHERE Delivery_ID=1')
            with redirect_stdout(StringIO()):apply_schema(conn)
        finally:conn.close()
        row=self.sql('SELECT * FROM Delivery')[0]
        self.assertEqual(row['Crop_Year'],2025)
        self.assertEqual(float(row['Bushels']),123.45)
        self.assertEqual(len(self.sql('SELECT * FROM users')),2)
    def test_long_password_returns_login_error(self):
        self.client.get('/logout')
        result=self.client.post('/login',data=dict(username='admin',password='x'*100))
        self.assertEqual(result.status_code,200)
        self.assertIn(b'Invalid username or password',result.data)

for name in dir(invitation_tests.InvitationsTest):
    if name.startswith('test_') and name not in MigrationTest.__dict__:
        setattr(MigrationTest,name,None)

class DeliveryGeneratorTest(unittest.TestCase):
    def test_generated_sql_targets_selected_grower(self):
        db=sqlite3.connect(':memory:')
        self.addCleanup(db.close)
        db.executescript("""CREATE TABLE Crop(Crop_ID,Crop_Code);
            CREATE TABLE Storage_Location(StorLoc_ID,Bin_Code,Grower_ID);
            CREATE TABLE Delivery_Location(DelLoc_ID INTEGER PRIMARY KEY,DelLoc_code,Location,Grower_ID);
            CREATE TABLE Delivery(Grower_ID,Ticket_Num,Delivery_Date,Crop_Year,Crop_ID,DelLoc_ID,StorLoc_ID,
            MC,Gross_Weight,Tare_Weight,Bushels,Delivery_Status,Price,Gross_Sale,Sale_Discounts,Comments);
            INSERT INTO Crop VALUES(1,'C');
            INSERT INTO Storage_Location VALUES(1,'Bin1',1),(2,'Bin1',2);
            INSERT INTO Delivery_Location VALUES(1,'ANF','Other grower',1);""")
        row=DeliveryRow('1',1,'2026-01-01','C','ANF','Bin1',15,5600,0,100,None,None,None,None,None)
        sql=build_insert_sql([row],2025,2)
        db.executescript(sql.replace('START TRANSACTION;','BEGIN;'))
        self.assertEqual(db.execute('SELECT Grower_ID,Crop_Year,StorLoc_ID FROM Delivery').fetchone(),(2,2025,2))
        self.assertEqual(db.execute('SELECT l.Grower_ID FROM Delivery d JOIN Delivery_Location l ON l.DelLoc_ID=d.DelLoc_ID').fetchone(),(2,))
    def test_invalid_grower_rejected(self):
        with self.assertRaises(ValueError):build_insert_sql([],2025,0)
