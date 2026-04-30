"""
import_grc.py

Imports Raven Slingshot grain cart (.grc) data into the GMS MySQL database.

What this script does
---------------------
1. Reads Slingshot API credentials from .env through slingshot_client.py
2. Reads DB connection settings from .env
3. Lists grain cart files from Slingshot
4. Downloads and parses each .grc file
5. Resolves / creates:
   - Grower
   - Department   (Farm in GRC = Department in DB)
   - Field
   - Crop
   - Cart
6. Inserts one record per load into Harvest
7. Prevents duplicates using Harvest.External_Load_Key

Required .env variables
-----------------------
DB_HOST=localhost
DB_PORT=3307
DB_NAME=gms_db
DB_USER=gms_user
DB_PASSWORD=StrongPassword123!

RAVEN_API_KEY=...
RAVEN_SHARED_SECRET=...
RAVEN_ACCESS_KEY=...
RAVEN_BASE_URL=https://api.ravenslingshot.com

Before running
--------------
Make sure Harvest has these added columns:

ALTER TABLE Harvest
MODIFY COLUMN StorLoc_ID BIGINT UNSIGNED NULL;

ALTER TABLE Harvest
  ADD COLUMN Truck_ID VARCHAR(100) NULL AFTER Note,
  ADD COLUMN Destination VARCHAR(255) NULL AFTER Truck_ID,
  ADD COLUMN Test_Weight DECIMAL(8,2) NULL AFTER MC,
  ADD COLUMN Variety VARCHAR(120) NULL AFTER DryBushels,
  ADD COLUMN Load_Cell VARCHAR(100) NULL AFTER Variety,
  ADD COLUMN Source_File_Name VARCHAR(255) NULL AFTER Load_Cell,
  ADD COLUMN Source_File_ID BIGINT UNSIGNED NULL AFTER Source_File_Name,
  ADD COLUMN External_Load_Key VARCHAR(255) NULL AFTER Source_File_ID;

ALTER TABLE Harvest
  ADD UNIQUE KEY uq_harvest_external_load (External_Load_Key);

Run
---
python import_grc.py
python import_grc.py 93438245
python import_grc.py 93438245 93438246 93438247
python import_grc.py 93438245-93438260
"""

from __future__ import annotations

import os
import sys
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional

import pymysql
from dotenv import load_dotenv

from slingshot_client import SlingshotClient


load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost").strip(),
    "port": int(os.getenv("DB_PORT", "3306").strip()),
    "user": os.getenv("DB_USER", "").strip(),
    "password": os.getenv("DB_PASSWORD", "").strip(),
    "database": os.getenv("DB_NAME", "").strip(),
    "cursorclass": pymysql.cursors.DictCursor,
    "autocommit": False,
}


def safe_decimal(value: Any) -> Optional[float]:
    if value in (None, "", "null"):
        return None
    try:
        s = str(value).strip()
        s = s.replace(",", "")
        s = s.replace(" lbs", "")
        s = s.replace(" lb", "")
        s = s.replace(" bu", "")
        return float(s)
    except Exception:
        return None


def safe_date(value: Any) -> Optional[datetime.date]:
    if value in (None, "", "null"):
        return None

    text = str(value).strip()
    for fmt in (
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
        "%m/%d/%Y %H:%M:%S",
        "%m/%d/%Y %H:%M",
        "%m/%d/%Y",
    ):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    return None


def normalize_crop_name(crop_name: Optional[str]) -> str:
    if not crop_name:
        return "Unknown"

    value = crop_name.strip()
    lookup = {
        "soybean": "Soybeans",
        "soybeans": "Soybeans",
        "corn": "Corn",
        "maize": "Corn",
        "milo": "Milo",
        "grain sorghum": "Milo",
    }
    return lookup.get(value.lower(), value)


def normalize_cart_code(cart_code: Any) -> Optional[str]:
    if cart_code in (None, "", "null"):
        return None
    return str(cart_code).strip()


def normalize_destination(dest: Any) -> Optional[str]:
    if dest in (None, "", "null"):
        return None
    return str(dest).strip()


def normalize_variety(variety: Any) -> Optional[str]:
    if variety in (None, "", "null"):
        return None
    text = str(variety).strip()
    return text if text else None


def get_or_create_grower(conn, grower_name: str) -> int:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT Grower_ID FROM Grower WHERE Grower_Name = %s",
            (grower_name,)
        )
        row = cur.fetchone()
        if row:
            return row["Grower_ID"]

        cur.execute(
            "INSERT INTO Grower (Grower_Name) VALUES (%s)",
            (grower_name,)
        )
        return cur.lastrowid


def get_or_create_department(conn, dpt_name: str, grower_id: int) -> int:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT Dpt_ID
            FROM Department
            WHERE Dpt_Name = %s
              AND Grower_ID = %s
            """,
            (dpt_name, grower_id)
        )
        row = cur.fetchone()
        if row:
            return row["Dpt_ID"]

        cur.execute(
            """
            INSERT INTO Department (Dpt_Name, Contact, Manager, Grower_ID)
            VALUES (%s, %s, %s, %s)
            """,
            (dpt_name, "Unknown", "Unknown", grower_id)
        )
        return cur.lastrowid


def get_or_create_field(conn, field_name: str, crop_year: int, dpt_id: int) -> int:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT Field_ID
            FROM Field
            WHERE Field_Name = %s
              AND Crop_Year = %s
              AND Dpt_ID = %s
            """,
            (field_name, crop_year, dpt_id)
        )
        row = cur.fetchone()
        if row:
            return row["Field_ID"]

        cur.execute(
            """
            INSERT INTO Field (Field_Name, Crop_Year, Dpt_ID)
            VALUES (%s, %s, %s)
            """,
            (field_name, crop_year, dpt_id)
        )
        return cur.lastrowid


def get_or_create_crop(conn, crop_name: str) -> int:
    crop_name = normalize_crop_name(crop_name)

    with conn.cursor() as cur:
        cur.execute(
            "SELECT Crop_ID FROM Crop WHERE Crop_Name = %s",
            (crop_name,)
        )
        row = cur.fetchone()
        if row:
            return row["Crop_ID"]

        defaults = {
            "Corn": ("C", 56.00, 15.50),
            "Soybeans": ("SB", 60.00, 13.00),
            "Milo": ("M", 56.00, 14.00),
            "Unknown": ("UNK", 60.00, 13.00),
        }
        crop_code, weight_per_bushel, base_mc = defaults.get(
            crop_name, ("UNK", 60.00, 13.00)
        )

        cur.execute(
            """
            INSERT INTO Crop (Crop_Code, Crop_Name, Weight_PerBushel, Base_MC)
            VALUES (%s, %s, %s, %s)
            """,
            (crop_code, crop_name, weight_per_bushel, base_mc)
        )
        return cur.lastrowid


def get_or_create_cart(conn, cart_code: str) -> int:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT Cart_ID FROM Cart WHERE Cart_Code = %s",
            (cart_code,)
        )
        row = cur.fetchone()
        if row:
            return row["Cart_ID"]

        cur.execute(
            """
            INSERT INTO Cart (Cart_Code, Cart_Name)
            VALUES (%s, %s)
            """,
            (cart_code, f"Cart {cart_code}")
        )
        return cur.lastrowid


def find_storage_location(conn, destination_code: Optional[str]) -> Optional[int]:
    if not destination_code:
        return None

    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT StorLoc_ID
            FROM Storage_Location
            WHERE Bin_Code = %s
            """,
            (destination_code,)
        )
        row = cur.fetchone()
        return row["StorLoc_ID"] if row else None



def normalize_field_name(name):
    if not name:
        return ""
    name = str(name).strip().upper()
    name = name.replace(".", "-")
    name = name.replace(" ", "")
    return name


def build_external_load_key(
    harvest_date,
    cart_code: str,
    field_name: str,
    crop_name: str,
    load_num: str,
) -> str:
    date_key = harvest_date.isoformat() if harvest_date else "no-date"
    return "|".join([
        date_key,
        (cart_code or "").strip().upper(),
        normalize_field_name(field_name),
        normalize_crop_name(crop_name).upper(),
        str(load_num).strip(),
    ])


def insert_harvest_load(
    conn,
    header: Dict[str, Any],
    load_row: Dict[str, Any],
    source_file_id: int,
    source_file_name: str,
    row_num: int,
) -> str:
    grower_name = (header.get("grower") or "").strip()
    farm_name = (header.get("farm") or "").strip()
    field_name = normalize_field_name(header.get("field"))
    crop_name = normalize_crop_name(header.get("crop"))
    header_crop_year = header.get("year")
    job_number = header.get("job_number")

    cart_code = normalize_cart_code(load_row.get("cart_id"))

    if not cart_code:
        bridge_id = header.get("bridge_id")
        if bridge_id:
            parts = str(bridge_id).strip().split(":")
            if len(parts) >= 2:
                cart_code = f"{parts[-2]}:{parts[-1]}"
            else:
                cart_code = str(bridge_id).strip()

    destination_code = normalize_destination(load_row.get("dest"))

    harvest_date = safe_date(load_row.get("date"))
    mc = safe_decimal(load_row.get("comment"))
    gross_weight = safe_decimal(load_row.get("weight"))
    test_weight = safe_decimal(load_row.get("test_weight"))
    wet_bushels = safe_decimal(load_row.get("wet"))
    dry_bushels = safe_decimal(load_row.get("dry"))
    bushels = dry_bushels if dry_bushels is not None else wet_bushels

    truck_id = None if load_row.get("truck") in (None, "", "null") else str(load_row.get("truck")).strip()
    variety = normalize_variety(load_row.get("variety"))
    load_cell = None if load_row.get("load_cell") in (None, "", "null") else str(load_row.get("load_cell")).strip()

    load_num = load_row.get("load_num")
    if load_num in (None, "", "null"):
        load_num = str(row_num)
    else:
        load_num = str(load_num).strip()

    if harvest_date:
        crop_year = harvest_date.year
    elif header_crop_year:
        crop_year = int(header_crop_year)
    else:
        return "SKIPPED: missing year and load date"

    if not grower_name:
        return "SKIPPED: missing grower"
    if not farm_name:
        return "SKIPPED: missing farm/department"
    if not field_name:
        return "SKIPPED: missing field"
    if not crop_name:
        return "SKIPPED: missing crop"
    if not cart_code:
        return "SKIPPED: missing cart code"

    grower_id = get_or_create_grower(conn, grower_name)
    dpt_id = get_or_create_department(conn, farm_name, grower_id)
    field_id = get_or_create_field(conn, field_name, crop_year, dpt_id)
    crop_id = get_or_create_crop(conn, crop_name)
    cart_id = get_or_create_cart(conn, cart_code)
    storloc_id = find_storage_location(conn, destination_code)

    external_load_key = build_external_load_key(
        harvest_date=harvest_date,
        cart_code=cart_code,
        field_name=field_name,
        crop_name=crop_name,
        load_num=load_num,
    )

    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT Harvest_ID
            FROM Harvest
            WHERE External_Load_Key = %s
               OR (
                    Harvest_Date <=> %s
                AND Cart_ID = %s
                AND Field_ID = %s
                AND Crop_ID = %s
                AND Load_Num = %s
               )
            ORDER BY
                CASE WHEN External_Load_Key = %s THEN 0 ELSE 1 END,
                CASE WHEN MC IS NOT NULL THEN 0 ELSE 1 END,
                Harvest_ID
            LIMIT 1
            """,
            (
                external_load_key,
                harvest_date,
                cart_id,
                field_id,
                crop_id,
                load_num,
                external_load_key,
            )
        )
        existing = cur.fetchone()

        values = (
            cart_id,
            field_id,
            crop_id,
            dpt_id,
            storloc_id,
            load_num,
            harvest_date,
            mc,
            gross_weight,
            None,
            bushels,
            wet_bushels,
            dry_bushels,
            job_number,
            None,
            truck_id,
            destination_code,
            test_weight,
            variety,
            load_cell,
            source_file_name,
            source_file_id,
            external_load_key,
        )

        if existing:
            cur.execute(
                """
                UPDATE harvest_backup1
                SET
                    Cart_ID = %s,
                    Field_ID = %s,
                    Crop_ID = %s,
                    Dpt_ID = %s,
                    StorLoc_ID = %s,
                    Load_Num = %s,
                    Harvest_Date = %s,
                    MC = %s,
                    Gross_Weight = %s,
                    Tare_Weight = %s,
                    Bushels = %s,
                    WetBushels = %s,
                    DryBushels = %s,
                    JobNumber = %s,
                    Note = %s,
                    Truck_ID = %s,
                    Destination = %s,
                    Test_Weight = %s,
                    Variety = %s,
                    Load_Cell = %s,
                    Source_File_Name = %s,
                    Source_File_ID = %s,
                    External_Load_Key = %s,
                    Updated_At = CURRENT_TIMESTAMP
                WHERE Harvest_ID = %s
                """,
                values + (existing["Harvest_ID"],)
            )
            return "UPDATED"

        cur.execute(
            """
            INSERT INTO harvest_backup1 (
                Cart_ID,
                Field_ID,
                Crop_ID,
                Dpt_ID,
                StorLoc_ID,
                Load_Num,
                Harvest_Date,
                MC,
                Gross_Weight,
                Tare_Weight,
                Bushels,
                WetBushels,
                DryBushels,
                JobNumber,
                Note,
                Truck_ID,
                Destination,
                Test_Weight,
                Variety,
                Load_Cell,
                Source_File_Name,
                Source_File_ID,
                External_Load_Key
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s,
                %s, %s, %s
            )
            """,
            values
        )

    return "IMPORTED"


def import_all_graincart_files():
    client = SlingshotClient()
    conn = pymysql.connect(**DB_CONFIG)

    file_count = 0
    load_count = 0
    skipped_count = 0
    error_count = 0

    try:
        for item in client.iter_all_graincart_summaries(pagesize=25):
            file_id_raw = item.get("ID") or item.get("Id") or item.get("id")
            file_name = item.get("Name") or item.get("name") or f"GRC_{file_id_raw}.grc"

            if not file_id_raw:
                print("Skipping file with missing ID")
                skipped_count += 1
                continue

            file_id = int(file_id_raw)

            try:
                parsed = client.get_parsed_graincart_file(file_id, file_name=file_name)
                header = parsed["header"]
                loads = parsed["loads"]

                if not loads:
                    print(f"{file_name} -> no loads found")
                    skipped_count += 1
                    continue

                imported_this_file = 0
                skipped_this_file = 0

                for row_num, load_row in enumerate(loads, start=1):
                    status = insert_harvest_load(
                        conn=conn,
                        header=header,
                        load_row=load_row,
                        source_file_id=file_id,
                        source_file_name=file_name,
                        row_num=row_num,
                    )

                    if status == "IMPORTED":
                        imported_this_file += 1
                        load_count += 1
                    else:
                        skipped_this_file += 1
                        skipped_count += 1
                        print(f"  row {row_num}: {status}")

                conn.commit()
                file_count += 1
                print(
                    f"{file_name} -> loads found: {len(loads)} | "
                    f"imported={imported_this_file}, skipped={skipped_this_file}"
                )

            except Exception as exc:
                conn.rollback()
                error_count += 1
                print(f"ERROR importing {file_name} (ID={file_id}): {exc}")

        print("\nDone.")
        print(f"Files processed: {file_count}")
        print(f"Loads imported: {load_count}")
        print(f"Loads skipped: {skipped_count}")
        print(f"Files errored: {error_count}")

    finally:
        conn.close()


def import_graincart_file_by_id(file_id: int):
    client = SlingshotClient()
    conn = pymysql.connect(**DB_CONFIG)

    try:
        detail = client.get_graincart_detail(file_id)
        items = detail.get("GrainCart") or []
        file_name = f"GRC_{file_id}.grc"
        if items:
            file_name = items[0].get("Name") or file_name

        parsed = client.get_parsed_graincart_file(file_id, file_name=file_name)
        header = parsed["header"]
        loads = parsed["loads"]

        if not loads:
            print(f"{file_name} -> no loads found")
            return

        imported_this_file = 0
        updated_this_file = 0
        skipped_this_file = 0

        for row_num, load_row in enumerate(loads, start=1):
            status = insert_harvest_load(
                conn=conn,
                header=header,
                load_row=load_row,
                source_file_id=file_id,
                source_file_name=file_name,
                row_num=row_num,
            )

            if status == "IMPORTED":
                imported_this_file += 1
            elif status == "UPDATED":
                updated_this_file += 1
            else:
                skipped_this_file += 1
                print(f"  row {row_num}: {status}")

        conn.commit()
        print(
            f"{file_name} -> loads found: {len(loads)} | "
            f"imported={imported_this_file}, updated={updated_this_file}, skipped={skipped_this_file}"
        )
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def import_graincart_files_by_ids(file_ids: Iterable[int]):
    unique_ids: List[int] = []
    seen = set()
    for file_id in file_ids:
        if file_id not in seen:
            unique_ids.append(file_id)
            seen.add(file_id)

    total = len(unique_ids)
    if total == 0:
        print("No file IDs provided.")
        return

    print(f"Importing {total} specific Slingshot file(s)...")
    for index, file_id in enumerate(unique_ids, start=1):
        print(f"[{index}/{total}] Importing file ID {file_id}")
        import_graincart_file_by_id(file_id)


def parse_file_id_tokens(tokens: List[str]) -> List[int]:
    file_ids: List[int] = []

    for token in tokens:
        raw = token.strip()
        if not raw:
            continue

        for part in raw.split(","):
            item = part.strip()
            if not item:
                continue

            if "-" in item:
                start_text, end_text = item.split("-", 1)
                start_id = int(start_text.strip())
                end_id = int(end_text.strip())
                if end_id < start_id:
                    raise ValueError(f"Invalid ID range: {item}")
                file_ids.extend(range(start_id, end_id + 1))
            else:
                file_ids.append(int(item))

    return file_ids


if __name__ == "__main__":
    if len(sys.argv) > 1:
        import_graincart_files_by_ids(parse_file_id_tokens(sys.argv[1:]))
    else:
        import_all_graincart_files()
