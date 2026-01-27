import os
import csv
import pymysql

DB = {
    "host": "127.0.0.1",
    "port": 3307,
    "user": "gms_user",
    "password": "StrongPassword123!",
    "database": "gms_db",
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
    "autocommit": False,
}

GRC_FOLDER = "./data/grc"

DEFAULT_CART_CODE = "UNKNOWN"
DEFAULT_BIN_CODE = "UNKNOWN"
DEFAULT_CONTACT = "Unknown"
DEFAULT_MANAGER = "Unknown"

# If Crop_Name from GRC is not found in Crop table, you can insert using this mapping.
# If you want to NEVER insert crops, set ALLOW_CROP_INSERT = False
ALLOW_CROP_INSERT = True
CROP_SPECS = {
    "Soybean": ("B", 60.00, 13.0),
    "Corn": ("C", 56.00, 15.5),
    "High Moisture Corn": ("HMC", 56.00, 15.5),
    "Milo": ("M", 56.00, 14.0),
    "Wheat": ("W", 60.00, 13.5),
}

def s(x):
    return (x or "").strip()

def to_float(x):
    x = s(x)
    if x == "":
        return None
    try:
        return float(x)
    except ValueError:
        return None

def to_int(x):
    x = s(x)
    if x == "":
        return None
    try:
        return int(float(x))
    except ValueError:
        return None

def parse_grc(path):
    with open(path, newline="", encoding="utf-8", errors="ignore") as f:
        rows = list(csv.reader(f))

    meta = {}
    i = 0
    # meta section: Key,Value,
    while i < len(rows) and rows[i] and s(rows[i][0]) != "":
        meta[s(rows[i][0])] = s(rows[i][1]) if len(rows[i]) > 1 else ""
        i += 1

    # units row is rows[i], header is rows[i+1]
    header = rows[i + 1]
    loads = []
    for r in rows[i + 2:]:
        if not r or s(r[0]) == "":
            continue
        loads.append({h: (r[idx] if idx < len(r) else "") for idx, h in enumerate(header)})
    return meta, loads

# ---------- get-or-create IDs (no duplicates) ----------
def get_or_create_cart(cur, cart_code):
    cart_code = s(cart_code)
    cur.execute("SELECT Cart_ID FROM Cart WHERE Cart_Code=%s", (cart_code,))
    row = cur.fetchone()
    if row:
        return row["Cart_ID"]
    cur.execute("INSERT INTO Cart (Cart_Code, Cart_Name) VALUES (%s,%s)", (cart_code, "Unknown Cart"))
    return cur.lastrowid

def get_or_create_storloc(cur, bin_code):
    bin_code = s(bin_code)
    cur.execute("SELECT StorLoc_ID FROM Storage_Location WHERE Bin_Code=%s", (bin_code,))
    row = cur.fetchone()
    if row:
        return row["StorLoc_ID"]
    # Bin_Capacity is NOT NULL -> must set 0
    cur.execute(
        "INSERT INTO Storage_Location (Bin_Code, Bin_Name, Bin_Capacity) VALUES (%s,%s,%s)",
        (bin_code, "Unknown Bin", 0),
    )
    return cur.lastrowid

def get_or_create_grower(cur, grower_name):
    grower_name = s(grower_name)
    cur.execute("SELECT Grower_ID FROM Grower WHERE Grower_Name=%s", (grower_name,))
    row = cur.fetchone()
    if row:
        return row["Grower_ID"]
    cur.execute("INSERT INTO Grower (Grower_Name) VALUES (%s)", (grower_name,))
    return cur.lastrowid

def get_or_create_department(cur, grower_id, dpt_name):
    dpt_name = s(dpt_name)
    cur.execute(
        "SELECT Dpt_ID FROM Department WHERE Grower_ID=%s AND Dpt_Name=%s",
        (grower_id, dpt_name),
    )
    row = cur.fetchone()
    if row:
        return row["Dpt_ID"]
    cur.execute(
        "INSERT INTO Department (Dpt_Name, Contact, Manager, Grower_ID) VALUES (%s,%s,%s,%s)",
        (dpt_name, DEFAULT_CONTACT, DEFAULT_MANAGER, grower_id),
    )
    return cur.lastrowid

def get_or_create_field(cur, dpt_id, field_name, crop_year):
    field_name = s(field_name)
    crop_year = to_int(crop_year)
    if crop_year is None:
        raise ValueError("Crop_Year missing/invalid in .grc")

    cur.execute(
        "SELECT Field_ID FROM Field WHERE Dpt_ID=%s AND Field_Name=%s AND Crop_Year=%s",
        (dpt_id, field_name, crop_year),
    )
    row = cur.fetchone()
    if row:
        return row["Field_ID"]

    cur.execute(
        """
        INSERT INTO Field (Field_Name, Acres, Crop_Year, Irr_Type, Hybrid_Variety, Note, Dpt_ID)
        VALUES (%s, NULL, %s, NULL, NULL, NULL, %s)
        """,
        (field_name, crop_year, dpt_id),
    )
    return cur.lastrowid

def get_or_create_crop_id(cur, crop_name):
    """Prefer mapping to existing Crop table (since Crop spec already loaded)."""
    crop_name = s(crop_name)

    cur.execute("SELECT Crop_ID FROM Crop WHERE Crop_Name=%s", (crop_name,))
    row = cur.fetchone()
    if row:
        return row["Crop_ID"]

    if not ALLOW_CROP_INSERT:
        raise ValueError(f"Crop '{crop_name}' not found in Crop table (and ALLOW_CROP_INSERT=False).")

    if crop_name not in CROP_SPECS:
        raise ValueError(f"Crop '{crop_name}' not in CROP_SPECS mapping. Add it or set ALLOW_CROP_INSERT=False.")

    code, wt, base_mc = CROP_SPECS[crop_name]
    cur.execute(
        "INSERT INTO Crop (Crop_Code, Crop_Name, Weight_PerBushel, Base_MC) VALUES (%s,%s,%s,%s)",
        (code, crop_name, wt, base_mc),
    )
    return cur.lastrowid

# ---------- Harvest insert/update (no duplicates) ----------
def upsert_harvest(cur, payload):
    """
    payload keys:
      Cart_ID, Field_ID, Crop_ID, Dpt_ID, StorLoc_ID,
      Load_Num, Harvest_Date, MC, Gross_Weight, WetBushels, DryBushels,
      JobNumber, Note
    """
    cur.execute(
        "SELECT Harvest_ID FROM Harvest WHERE JobNumber=%s AND Load_Num=%s LIMIT 1",
        (payload["JobNumber"], payload["Load_Num"]),
    )
    row = cur.fetchone()

    if row:
        # UPDATE existing row
        cur.execute(
            """
            UPDATE Harvest
            SET
              Cart_ID=%s,
              Field_ID=%s,
              Crop_ID=%s,
              Dpt_ID=%s,
              StorLoc_ID=%s,
              Harvest_Date=%s,
              MC=%s,
              Gross_Weight=%s,
              WetBushels=%s,
              DryBushels=%s,
              Note=%s,
              Updated_At=CURRENT_TIMESTAMP
            WHERE Harvest_ID=%s
            """,
            (
                payload["Cart_ID"],
                payload["Field_ID"],
                payload["Crop_ID"],
                payload["Dpt_ID"],
                payload["StorLoc_ID"],
                payload["Harvest_Date"],
                payload["MC"],
                payload["Gross_Weight"],
                payload["WetBushels"],
                payload["DryBushels"],
                payload["Note"],
                row["Harvest_ID"],
            ),
        )
        return "updated"
    else:
        # INSERT new row
        cur.execute(
            """
            INSERT INTO Harvest
              (Cart_ID, Field_ID, Crop_ID, Dpt_ID, StorLoc_ID,
               Load_Num, Harvest_Date, MC, Gross_Weight,
               WetBushels, DryBushels,
               JobNumber, Note)
            VALUES
              (%s,%s,%s,%s,%s,
               %s,%s,%s,%s,
               %s,%s,
               %s,%s)
            """,
            (
                payload["Cart_ID"],
                payload["Field_ID"],
                payload["Crop_ID"],
                payload["Dpt_ID"],
                payload["StorLoc_ID"],
                payload["Load_Num"],
                payload["Harvest_Date"],
                payload["MC"],
                payload["Gross_Weight"],
                payload["WetBushels"],
                payload["DryBushels"],
                payload["JobNumber"],
                payload["Note"],
            ),
        )
        return "inserted"

def main():
    conn = pymysql.connect(**DB)
    try:
        with conn.cursor() as cur:
            # Defaults
            cart_id = get_or_create_cart(cur, DEFAULT_CART_CODE)
            stor_id = get_or_create_storloc(cur, DEFAULT_BIN_CODE)
            conn.commit()

            files = [fn for fn in os.listdir(GRC_FOLDER) if fn.lower().endswith(".grc")]
            if not files:
                print(f"No .grc files found in {GRC_FOLDER}")
                return

            for fn in files:
                meta, loads = parse_grc(os.path.join(GRC_FOLDER, fn))

                # Meta mapping
                job_number = to_int(meta.get("JobNumber"))
                grower_name = s(meta.get("Grower"))
                farm_name = s(meta.get("Farm"))
                field_name = s(meta.get("Field"))
                crop_name = s(meta.get("Crop"))
                crop_year = meta.get("Year")

                if job_number is None:
                    print(f"[SKIP] Missing JobNumber in {fn}")
                    continue
                if not (grower_name and farm_name and field_name and crop_name and s(crop_year)):
                    print(f"[SKIP] Missing required meta in {fn}")
                    continue

                # Lookup table mapping (insert only if missing)
                grower_id = get_or_create_grower(cur, grower_name)
                dpt_id = get_or_create_department(cur, grower_id, farm_name)
                field_id = get_or_create_field(cur, dpt_id, field_name, crop_year)
                crop_id = get_or_create_crop_id(cur, crop_name)

                inserted = 0
                updated = 0

                for l in loads:
                    load_num = s(l.get("LoadNumber"))
                    if not load_num:
                        continue

                    # Your required mapping:
                    # LoadDate -> Harvest_Date
                    harvest_date = s(l.get("LoadDate"))  # not LocalDate (per your instruction)

                    # Weight -> Gross_Weight
                    gross_weight = to_float(l.get("Weight"))

                    # WetBushels / DryBushels -> Harvest WetBushels / DryBushels
                    wet_bu = to_float(l.get("WetBushels"))
                    dry_bu = to_float(l.get("DryBushels"))

                    # Comment -> MC (per your instruction)
                    mc = to_float(l.get("Comment"))  # if Comment is not numeric, becomes None

                    # Note can store truck/destination/etc.
                    note_parts = []
                    truck = s(l.get("TruckID"))
                    dest = s(l.get("Destination"))
                    if truck:
                        note_parts.append(f"TruckID={truck}")
                    if dest:
                        note_parts.append(f"Destination={dest}")
                    note = " | ".join(note_parts) if note_parts else None

                    payload = {
                        "Cart_ID": cart_id,
                        "Field_ID": field_id,
                        "Crop_ID": crop_id,
                        "Dpt_ID": dpt_id,
                        "StorLoc_ID": stor_id,
                        "Load_Num": load_num,
                        "Harvest_Date": harvest_date if harvest_date else None,
                        "MC": mc,
                        "Gross_Weight": gross_weight,
                        "WetBushels": wet_bu,
                        "DryBushels": dry_bu,
                        "JobNumber": job_number,
                        "Note": note,
                    }

                    action = upsert_harvest(cur, payload)
                    if action == "inserted":
                        inserted += 1
                    else:
                        updated += 1

                conn.commit()
                print(f"✔ {fn}: inserted={inserted}, updated={updated}")

    finally:
        conn.close()

if __name__ == "__main__":
    main()
