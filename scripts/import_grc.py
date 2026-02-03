import os
import csv
import re
import pymysql
from decimal import Decimal

# -------------------- DB CONFIG --------------------
DB = {
    "host": "127.0.0.1",   # safer than localhost on Windows
    "port": 3307,
    "user": "gms_user",
    "password": "StrongPassword123!",
    "database": "gms_db",
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
    "autocommit": False,
}

# Folder containing .grc files
GRC_FOLDER = "./data/grc"

# Defaults (used only if a .grc row has empty Destination)
DEFAULT_CART_CODE = "UNKNOWN"
DEFAULT_BIN_CODE  = "UNKNOWN"

DEFAULT_CONTACT = "Unknown"
DEFAULT_MANAGER = "Unknown"

# Only used if Crop_Name from GRC is missing from Crop table
# (you said Crop spec table already has data, so this should rarely be used)
ALLOW_CROP_INSERT = True
CROP_SPECS = {
    "Soybean": ("B", 60.00, 13.0),
    "Corn": ("C", 56.00, 15.5),
    "High Moisture Corn": ("HMC", 56.00, 15.5),
    "Milo": ("M", 56.00, 14.0),
    "Wheat": ("W", 60.00, 13.5),
}

# -------------------- HELPERS --------------------
# def s(x):
#     return (x or "").strip()

# def to_float(x):
#     x = s(x)
#     if x == "":
#         return None
#     try:
#         return float(x)
#     except ValueError:
#         return None
    




def s(x):
    if x is None:
        return ""
    if isinstance(x, str):
        return x.strip()
    return str(x).strip()

def to_float(x):
    if x is None:
        return None
    if isinstance(x, (int, float)):
        return float(x)
    if isinstance(x, Decimal):
        return float(x)
    if isinstance(x, str):
        x = x.strip().replace(",", "")
        if x == "":
            return None
        try:
            return float(x)
        except ValueError:
            return None
    return None




def to_int(x):
    x = s(x)
    if x == "":
        return None
    try:
        return int(float(x))
    except ValueError:
        return None

def normalize_code(x: str) -> str:
    """
    Normalize codes like 'bin-13', 'Bin_13', ' BIN13 ' -> 'BIN13'
    Keeps only A-Z and 0-9, uppercased.
    """
    x = (x or "").strip().upper()
    x = re.sub(r"[^A-Z0-9]", "", x)
    return x

def parse_grc(path):
    """
    Parses a Slingshot .grc file that looks like:
      meta key/value rows...
      units row...
      header row...
      data rows...
    """
    with open(path, newline="", encoding="utf-8", errors="ignore") as f:
        rows = list(csv.reader(f))

    meta = {}
    i = 0
    while i < len(rows) and rows[i] and s(rows[i][0]) != "":
        meta[s(rows[i][0])] = s(rows[i][1]) if len(rows[i]) > 1 else ""
        i += 1

    # next row is units, then header
    header = rows[i + 1]
    loads = []
    for r in rows[i + 2:]:
        if not r or s(r[0]) == "":
            continue
        loads.append({h: (r[idx] if idx < len(r) else "") for idx, h in enumerate(header)})

    return meta, loads

# -------------------- LOOKUPS (NO DUPLICATES) --------------------
def get_or_create_cart(cur, cart_code):
    cart_code = s(cart_code) or DEFAULT_CART_CODE
    cur.execute("SELECT Cart_ID FROM Cart WHERE Cart_Code=%s", (cart_code,))
    row = cur.fetchone()
    if row:
        return row["Cart_ID"]
    cur.execute("INSERT INTO Cart (Cart_Code, Cart_Name) VALUES (%s,%s)", (cart_code, "Unknown Cart"))
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
        raise ValueError("Crop_Year missing/invalid in .grc meta")

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
    """
    You said crop spec table already has data, so we primarily map by Crop_Name.
    """
    crop_name = s(crop_name)
    cur.execute("SELECT Crop_ID FROM Crop WHERE Crop_Name=%s", (crop_name,))
    row = cur.fetchone()
    if row:
        return row["Crop_ID"]

    if not ALLOW_CROP_INSERT:
        raise ValueError(f"Crop '{crop_name}' not found in Crop table (ALLOW_CROP_INSERT=False).")

    if crop_name not in CROP_SPECS:
        raise ValueError(f"Crop '{crop_name}' not in CROP_SPECS mapping. Add it or set ALLOW_CROP_INSERT=False.")

    code, wt, base_mc = CROP_SPECS[crop_name]
    cur.execute(
        "INSERT INTO Crop (Crop_Code, Crop_Name, Weight_PerBushel, Base_MC) VALUES (%s,%s,%s,%s)",
        (code, crop_name, wt, base_mc),
    )
    return cur.lastrowid

def get_or_create_storloc_from_destination(cur, destination):
    """
    Destination -> Storage_Location mapping:
      - destination may be 'Bin13' or 'bin-13' etc.
      - Try match by normalized Bin_Code
      - Then try exact Bin_Name
      - If not found, insert new Storage_Location row:
            Bin_Code = normalized destination
            Bin_Name = original destination text
            Bin_Capacity = 0 (required NOT NULL)
    """
    dest_raw = s(destination)
    if not dest_raw:
        dest_raw = DEFAULT_BIN_CODE

    dest_code = normalize_code(dest_raw) or normalize_code(DEFAULT_BIN_CODE) or "UNKNOWN"

    # 1) Match normalized Bin_Code
    cur.execute(
        """
        SELECT StorLoc_ID
        FROM Storage_Location
        WHERE UPPER(REPLACE(REPLACE(REPLACE(Bin_Code,'-',''),'_',''),' ','')) = %s
        LIMIT 1
        """,
        (dest_code,),
    )
    row = cur.fetchone()
    if row:
        return row["StorLoc_ID"]

    # 2) Match by Bin_Name (exact)
    cur.execute(
        "SELECT StorLoc_ID FROM Storage_Location WHERE Bin_Name=%s LIMIT 1",
        (dest_raw,),
    )
    row = cur.fetchone()
    if row:
        return row["StorLoc_ID"]

    # 3) Insert new storage location
    cur.execute(
        """
        INSERT INTO Storage_Location (Bin_Code, Bin_Name, Bin_Capacity)
        VALUES (%s, %s, 0)
        """,
        (dest_code, dest_raw),
    )
    return cur.lastrowid

# -------------------- BUSHELS CALC (EXCEL LOGIC) --------------------
def calc_bushels_excel(net_lbs, mc, base_mc, wt_per_bu):
    """
    Excel formula equivalent:
      wet_bu = net_lbs / wt_per_bu
      if mc > base_mc:
         wet_bu * ((100 - mc) / (100 - base_mc))
      else:
         wet_bu
    """
    if net_lbs is None or wt_per_bu is None or wt_per_bu == 0:
        return None

    wet_bu = net_lbs / wt_per_bu

    if mc is not None and base_mc is not None and mc > base_mc:
        denom = (100.0 - base_mc)
        if denom == 0:
            return None
        return wet_bu * ((100.0 - mc) / denom)

    return wet_bu

# -------------------- HARVEST UPSERT (NO DUPLICATES) --------------------
def upsert_harvest(cur, payload):
    """
    Uses (JobNumber, Load_Num) as the identity.
    Works even without a UNIQUE key because it SELECTs first.
    """
    cur.execute(
        "SELECT Harvest_ID FROM Harvest WHERE JobNumber=%s AND Load_Num=%s LIMIT 1",
        (payload["JobNumber"], payload["Load_Num"]),
    )
    row = cur.fetchone()

    if row:
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
              Tare_Weight=%s,
              Bushels=%s,
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
                payload["Tare_Weight"],
                payload["Bushels"],
                payload["Note"],
                row["Harvest_ID"],
            ),
        )
        return "updated"

    cur.execute(
        """
        INSERT INTO Harvest
          (Cart_ID, Field_ID, Crop_ID, Dpt_ID, StorLoc_ID,
           Load_Num, Harvest_Date, MC, Gross_Weight, Tare_Weight, Bushels,
           JobNumber, Note)
        VALUES
          (%s,%s,%s,%s,%s,
           %s,%s,%s,%s,%s,%s,
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
            payload["Tare_Weight"],
            payload["Bushels"],
            payload["JobNumber"],
            payload["Note"],
        ),
    )
    return "inserted"

# -------------------- MAIN --------------------
def main():
    conn = pymysql.connect(**DB)
    try:
        with conn.cursor() as cur:
            cart_id = get_or_create_cart(cur, DEFAULT_CART_CODE)
            conn.commit()

            files = [fn for fn in os.listdir(GRC_FOLDER) if fn.lower().endswith(".grc")]
            if not files:
                print(f"No .grc files found in {GRC_FOLDER}")
                return

            for fn in files:
                meta, loads = parse_grc(os.path.join(GRC_FOLDER, fn))

                job_number = to_int(meta.get("JobNumber"))
                grower_name = s(meta.get("Grower"))
                farm_name = s(meta.get("Farm"))
                field_name = s(meta.get("Field"))
                crop_name = s(meta.get("Crop"))
                crop_year = meta.get("Year")

                if job_number is None or not (grower_name and farm_name and field_name and crop_name and s(crop_year)):
                    print(f"[SKIP] Missing required meta in {fn}")
                    continue

                grower_id = get_or_create_grower(cur, grower_name)
                dpt_id = get_or_create_department(cur, grower_id, farm_name)
                field_id = get_or_create_field(cur, dpt_id, field_name, crop_year)
                crop_id = get_or_create_crop_id(cur, crop_name)

                # pull crop specs for bushels calc
                cur.execute("SELECT Weight_PerBushel, Base_MC FROM Crop WHERE Crop_ID=%s", (crop_id,))
                crop_row = cur.fetchone() or {}
                wt_per_bu = to_float(crop_row.get("Weight_PerBushel"))
                base_mc = to_float(crop_row.get("Base_MC"))

                inserted = 0
                updated = 0

                for l in loads:
                    load_num = s(l.get("LoadNumber"))
                    if not load_num:
                        continue

                    # Destination -> Storage Location mapping (per your latest requirement)
                    dest = s(l.get("Destination"))
                    storloc_id = get_or_create_storloc_from_destination(cur, dest)

                    # Required mapping from GRC -> Harvest
                    harvest_date = s(l.get("LoadDate")) or None
                    gross_weight = to_float(l.get("Weight"))  # Slingshot Weight -> Gross_Weight
                    tare_weight = to_float(l.get("TareWeight"))  # if column exists; usually blank
                    if tare_weight is None:
                        tare_weight = 0.0

                    # Moisture for bushels formula:
                    # prefer Moisture column (it exists in your sample)
                    mc = to_float(l.get("Comment"))  # if Comment is not numeric, becomes None
                    if mc is None:
                        mc = to_float(l.get("MeasuredMoisture"))

                    # Excel-equivalent bushels calculation
                    bushels = None
                    if gross_weight is not None:
                        net_lbs = gross_weight - tare_weight
                        bushels = calc_bushels_excel(net_lbs, mc, base_mc, wt_per_bu)
                        if bushels is not None:
                            bushels = round(bushels, 2)

                    # Note: store extra info without breaking schema
                    truck = s(l.get("TruckID"))
                    note_parts = []
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
                        "StorLoc_ID": storloc_id,
                        "Load_Num": load_num,
                        "Harvest_Date": harvest_date,
                        "MC": mc,
                        "Gross_Weight": gross_weight,
                        "Tare_Weight": tare_weight,
                        "Bushels": bushels,
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
