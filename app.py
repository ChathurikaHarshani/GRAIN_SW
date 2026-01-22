from flask import Flask, render_template, jsonify, request, redirect, url_for , session
from db import get_conn
from datetime import date, timedelta
from decimal import Decimal
import calendar
from functools import wraps
from dotenv import load_dotenv
import os
# from slingshot_client import get_jobdata_summary   # keep commented for now

app = Flask(__name__)


app.secret_key = os.getenv("SECRET_KEY", "dev-secret-change-me")

@app.route("/")
def landing():
    # If already logged in, go to dashboard
    if session.get("logged_in"):
        return redirect(url_for("dashboard"))
    return render_template("landing.html")




def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)
    return wrapper



@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("logged_in"):
        return redirect(url_for("dashboard"))

    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if username == os.getenv("APP_USERNAME") and password == os.getenv("APP_PASSWORD"):
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid username or password."

    return render_template("loging.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))








# ----------------- Health check ----------------- #
@app.route("/health")
def health():
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.fetchone()
        cur.close()
        conn.close()
        status = "ok"
    except Exception as e:
        status = f"db-error: {e}"
    return {"status": status}



@app.route("/app")
@login_required
def dashboard():
    return render_template("index.html", app_name="GMS")



# ----------------- Grower: list + create ----------------- #
@app.route("/growers")
#@login_required
def list_growers():
    """Show all growers in a table."""
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT Grower_ID, Grower_Name FROM Grower ORDER BY Grower_Name;")
    growers = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("growers.html", growers=growers)


@app.route("/growers/new", methods=["GET", "POST"])
#@login_required
def new_grower():
    """Form to add a new grower."""
    if request.method == "POST":
        grower_name = request.form.get("grower_name", "").strip()

        if grower_name:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO Grower (Grower_Name) VALUES (%s);",
                (grower_name,)
            )
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for("list_growers"))
        else:
            # No name entered; redisplay form with error
            return render_template("grower_form.html", error="Grower name is required")

    # GET: show empty form
    return render_template("grower_form.html", error=None)



# ----------------- Department: list + create ----------------- #

@app.route("/departments")
@login_required
def list_departments():
    """Show all departments."""
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT d.Dpt_ID, d.Dpt_Name, d.Contact, d.Manager,
               g.Grower_Name
        FROM Department d
        JOIN Grower g ON d.Grower_ID = g.Grower_ID
        ORDER BY d.Dpt_Name;
    """)
    departments = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("departments.html", departments=departments)


@app.route("/departments/new", methods=["GET", "POST"])
@login_required
def new_department():
    """Create a new department with Grower dropdown."""
    conn = get_conn()

    # Fetch growers for the dropdown
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT Grower_ID, Grower_Name FROM Grower ORDER BY Grower_Name;")
    growers = cur.fetchall()
    cur.close()

    if request.method == "POST":
        dpt_name = request.form.get("dpt_name", "").strip()
        contact = request.form.get("contact", "").strip()
        manager = request.form.get("manager", "").strip()
        grower_id = request.form.get("grower_id")

        if dpt_name and contact and manager and grower_id:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO Department (Dpt_Name, Contact, Manager, Grower_ID)
                VALUES (%s, %s, %s, %s);
            """, (dpt_name, contact, manager, grower_id))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for("list_departments"))

        return render_template(
            "department_form.html",
            growers=growers,
            error="All fields are required."
        )

    conn.close()
    return render_template("department_form.html", growers=growers, error=None)



# ----------------- Field: list + create ----------------- #

@app.route("/fields")
@login_required
def list_fields():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT f.Field_ID, f.Field_Name, f.Acres, f.Crop_Year, f.Irr_Type, f.Hybrid_Variety, f.Note,
               d.Dpt_Name
        FROM Field f
        JOIN Department d ON f.Dpt_ID = d.Dpt_ID
        ORDER BY f.Field_Name;
    """)
    fields = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("fields.html", fields=fields)

@app.route("/fields/new", methods=["GET", "POST"])
@login_required
def new_field():
    conn = get_conn()

    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT Dpt_ID, Dpt_Name FROM Department ORDER BY Dpt_Name;")
    departments = cur.fetchall()
    cur.close()

    if request.method == "POST":
        field_name = request.form.get("field_name", "").strip()
        acres = request.form.get("acres", "").strip()
        crop_year = request.form.get("crop_year", "").strip()
        irr_type = request.form.get("irr_type", "").strip()
        hybrid = request.form.get("hybrid_variety", "").strip()
        note = request.form.get("note", "").strip()
        dpt_id = request.form.get("dpt_id", "").strip()

        if field_name and crop_year and dpt_id:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO Field (Field_Name, Acres, Crop_Year, Irr_Type, Hybrid_Variety, Note, Dpt_ID)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """, (
                field_name,
                float(acres) if acres else None,
                int(crop_year),
                irr_type if irr_type else None,
                hybrid if hybrid else None,
                note if note else None,
                int(dpt_id)
            ))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for("list_fields"))

        conn.close()
        return render_template("field_form.html", departments=departments, error="Field Name, Crop Year, and Department are required.")

    conn.close()
    return render_template("field_form.html", departments=departments, error=None)


# ----------------- Cart: list + create ----------------- #

@app.route("/carts")
@login_required
def list_carts():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT Cart_ID, Cart_Code, Cart_Name FROM Cart ORDER BY Cart_Name;")
    carts = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("carts.html", carts=carts)

@app.route("/carts/new", methods=["GET", "POST"])
@login_required
def new_cart():
    if request.method == "POST":
        cart_code = request.form.get("cart_code", "").strip()
        cart_name = request.form.get("cart_name", "").strip()

        if cart_code and cart_name:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO Cart (Cart_Code, Cart_Name) VALUES (%s, %s);",
                (cart_code, cart_name)
            )
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for("list_carts"))

        return render_template("cart_form.html", error="Cart Code and Cart Name are required.")

    return render_template("cart_form.html", error=None)



# ----------------- Crop: list + create ----------------- #

@app.route("/crops")
@login_required
def list_crops():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT Crop_ID, Crop_Code, Crop_Name, Weight_PerBushel, Base_MC
        FROM Crop
        ORDER BY Crop_Name;
    """)
    crops = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("crops.html", crops=crops)

@app.route("/crops/new", methods=["GET", "POST"])
def new_crop():
    if request.method == "POST":
        crop_code = request.form.get("crop_code", "").strip()
        crop_name = request.form.get("crop_name", "").strip()
        weight = request.form.get("weight_per_bushel", "").strip()
        base_mc = request.form.get("base_mc", "").strip()

        if crop_code and crop_name and weight and base_mc:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO Crop (Crop_Code, Crop_Name, Weight_PerBushel, Base_MC)
                VALUES (%s, %s, %s, %s);
            """, (crop_code, crop_name, float(weight), float(base_mc)))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for("list_crops"))

        return render_template("crop_form.html", error="All fields are required.")

    return render_template("crop_form.html", error=None)


# ----------------- Storage Location: list + create ----------------- #

@app.route("/storage")
@login_required
def list_storage():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT StorLoc_ID, Bin_Code, Bin_Name, Bin_Capacity, Diameter, Install_Date,
               Legal_Desc, Lattitude, Lontitude, Manufacture
        FROM Storage_Location
        ORDER BY Bin_Name;
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("storage.html", storage=rows)

@app.route("/storage/new", methods=["GET", "POST"])
@login_required
def new_storage():
    if request.method == "POST":
        bin_code = request.form.get("bin_code", "").strip()
        bin_name = request.form.get("bin_name", "").strip()
        bin_capacity = request.form.get("bin_capacity", "").strip()
        diameter = request.form.get("diameter", "").strip()
        install_date = request.form.get("install_date", "").strip()  # YYYY-MM-DDTHH:MM from input
        legal_desc = request.form.get("legal_desc", "").strip()
        lattitude = request.form.get("lattitude", "").strip()
        lontitude = request.form.get("lontitude", "").strip()
        manufacture = request.form.get("manufacture", "").strip()

        # required fields in your schema: Bin_Code, Bin_Name, Bin_Capacity
        if bin_code and bin_name and bin_capacity:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO Storage_Location
                  (Bin_Code, Bin_Name, Bin_Capacity, Diameter, Install_Date,
                   Legal_Desc, Lattitude, Lontitude, Manufacture)
                VALUES
                  (%s, %s, %s, %s, %s,
                   %s, %s, %s, %s);
            """, (
                bin_code,
                bin_name,
                float(bin_capacity),
                float(diameter) if diameter else None,
                install_date if install_date else None,
                legal_desc if legal_desc else None,
                float(lattitude) if lattitude else None,
                float(lontitude) if lontitude else None,
                manufacture if manufacture else None
            ))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for("list_storage"))

        return render_template("storage_form.html", error="Bin Code, Bin Name, and Bin Capacity are required.")

    return render_template("storage_form.html", error=None)


# ----------------- Delivery Location: list + create ----------------- #

@app.route("/delivery-locations")
@login_required
def list_delivery_locations():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT DelLoc_ID, DelLoc_code, Location
        FROM Delivery_Location
        ORDER BY DelLoc_code;
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("delivery_locations.html", locations=rows)

@app.route("/delivery-locations/new", methods=["GET", "POST"])
@login_required
def new_delivery_location():
    if request.method == "POST":
        code = request.form.get("delloc_code", "").strip()
        location = request.form.get("location", "").strip()

        if code:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO Delivery_Location (DelLoc_code, Location)
                VALUES (%s, %s);
            """, (code, location if location else None))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for("list_delivery_locations"))

        return render_template("delivery_location_form.html", error="Delivery Location code is required.")

    return render_template("delivery_location_form.html", error=None)



# ----------------- Market Price Monthly: list + create ----------------- #

@app.route("/market-prices")
@login_required
def list_market_prices():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT mp.ID, mp.Crop, c.Crop_Name, mp.Year, mp.Month, mp.Day, mp.Market_Price
        FROM MarketPriceMonthly mp
        LEFT JOIN Crop c ON mp.Crop = c.Crop_ID
        ORDER BY mp.Year DESC, mp.Month DESC, mp.ID DESC;
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("market_prices.html", prices=rows)

@app.route("/market-prices/new", methods=["GET", "POST"])
@login_required
def new_market_price():
    conn = get_conn()

    # dropdown crops
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT Crop_ID, Crop_Name FROM Crop ORDER BY Crop_Name;")
    crops = cur.fetchall()
    cur.close()

    if request.method == "POST":
        crop_id = request.form.get("crop_id", "").strip()
        year = request.form.get("year", "").strip()
        month = request.form.get("month", "").strip()
        day = request.form.get("day", "").strip()
        price = request.form.get("market_price", "").strip()

        if crop_id and year and month and day and price:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO MarketPriceMonthly (Crop, Year, Month, Day, Market_Price)
                VALUES (%s, %s, %s, %s, %s);
            """, (int(crop_id), int(year), int(month), day, float(price)))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for("list_market_prices"))

        conn.close()
        return render_template("market_price_form.html", crops=crops, error="All fields are required.")

    conn.close()
    return render_template("market_price_form.html", crops=crops, error=None)





# ----------------- Harvest Query: filter + add ----------------- #

@app.route("/harvest-query", methods=["GET", "POST"])
@login_required
def harvest_query():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)

    # Dropdown data
    cur.execute("SELECT Field_ID, Field_Name FROM Field ORDER BY Field_Name;")
    fields = cur.fetchall()

    cur.execute("SELECT StorLoc_ID, Bin_Name FROM Storage_Location ORDER BY Bin_Name;")
    storages = cur.fetchall()

    cur.execute("SELECT Crop_ID, Crop_Name, Weight_PerBushel FROM Crop ORDER BY Crop_Name;")
    crops = cur.fetchall()

    cur.execute("SELECT Cart_ID, Cart_Name FROM Cart ORDER BY Cart_Name;")
    carts = cur.fetchall()

    # Filters (from URL query params)
    selected_field = request.args.get("field_id", "")
    selected_storage = request.args.get("storloc_id", "")

    error = None

    # ----------- POST: insert a new Harvest row -----------
    if request.method == "POST":
        load_num = request.form.get("load_num", "").strip()
        harvest_date = request.form.get("harvest_date", "").strip()
        field_id = request.form.get("field_id", "").strip()
        storloc_id = request.form.get("storloc_id", "").strip()
        crop_id = request.form.get("crop_id", "").strip()
        cart_id = request.form.get("cart_id", "").strip()

        mc = request.form.get("mc", "").strip()
        gross = request.form.get("gross", "").strip()
        tare = request.form.get("tare", "").strip()
        note = request.form.get("note", "").strip()

        if not (load_num and harvest_date and field_id and storloc_id and crop_id and cart_id):
            error = "Load, Date, Field, Storage, Crop, and Cart are required."
        else:
            # Get Dpt_ID from selected field (auto)
            cur.execute("SELECT Dpt_ID FROM Field WHERE Field_ID=%s;", (field_id,))
            row = cur.fetchone()
            if not row:
                error = "Selected Field not found."
            else:
                dpt_id = row["Dpt_ID"]

                # Weight per bushel for bushel calculation
                cur.execute("SELECT Weight_PerBushel FROM Crop WHERE Crop_ID=%s;", (crop_id,))
                crop_row = cur.fetchone()
                wpb = float(crop_row["Weight_PerBushel"]) if crop_row and crop_row["Weight_PerBushel"] else None

                gross_val = float(gross) if gross else None
                tare_val = float(tare) if tare else 0.0
                mc_val = float(mc) if mc else None

                bushels_val = None
                if wpb and gross_val is not None:
                    bushels_val = (gross_val - tare_val) / wpb

                cur2 = conn.cursor()
                cur2.execute("""
                    INSERT INTO Harvest
                      (Cart_ID, Field_ID, Crop_ID, Dpt_ID, StorLoc_ID,
                       Load_Num, Harvest_Date, MC, Gross_Weight, Tare_Weight, Bushels, Note)
                    VALUES
                      (%s, %s, %s, %s, %s,
                       %s, %s, %s, %s, %s, %s, %s);
                """, (
                    int(cart_id), int(field_id), int(crop_id), int(dpt_id), int(storloc_id),
                    load_num, harvest_date, mc_val, gross_val, tare_val, bushels_val, (note if note else None)
                ))
                conn.commit()
                cur2.close()

                # After insert, keep filters on screen
                conn.close()
                return redirect(url_for("harvest_query", field_id=field_id, storloc_id=storloc_id))

    # ----------- GET: show table (filtered) -----------
    where = []
    params = []

    if selected_field:
        where.append("h.Field_ID = %s")
        params.append(selected_field)
    if selected_storage:
        where.append("h.StorLoc_ID = %s")
        params.append(selected_storage)

    where_sql = ("WHERE " + " AND ".join(where)) if where else ""

    cur.execute(f"""
        SELECT
          h.Harvest_ID,
          h.Load_Num,
          h.Harvest_Date,
          f.Field_Name,
          cr.Crop_Name,
          h.MC,
          h.Gross_Weight,
          h.Tare_Weight,
          s.Bin_Name AS Storage,
          h.Bushels,
          h.Note
        FROM Harvest h
        JOIN Field f ON h.Field_ID = f.Field_ID
        JOIN Crop cr ON h.Crop_ID = cr.Crop_ID
        JOIN Storage_Location s ON h.StorLoc_ID = s.StorLoc_ID
        {where_sql}
        ORDER BY h.Harvest_Date DESC, h.Load_Num DESC;
    """, tuple(params))

    loads = cur.fetchall()
    # ---------- Summary calculations (like Excel SUBTOTAL) ----------
    mc_values = [float(r["MC"]) for r in loads if r["MC"] is not None]
    mc_avg = (sum(mc_values) / len(mc_values)) if mc_values else None

    gross_sum = sum(float(r["Gross_Weight"]) for r in loads if r["Gross_Weight"] is not None)
    tare_sum = sum(float(r["Tare_Weight"]) for r in loads if r["Tare_Weight"] is not None)
    lbs_wet = gross_sum - tare_sum

    bushels_sum = sum(float(r["Bushels"]) for r in loads if r["Bushels"] is not None)

    # Determine wet bu conversion factor:
    # if selected crop is Beans ("B") -> 60 else 56
    # We'll infer from the first row crop name, or default to 56
    factor = 56
    if loads:
        crop_name = (loads[0].get("Crop_Name") or "").lower()
        if "bean" in crop_name or crop_name in ["b", "beans", "soybean", "soybeans"]:
            factor = 60

    bu_wet = (lbs_wet / factor) if factor and lbs_wet is not None else None
    
    cur.close()
    conn.close()

    return render_template(
        "harvest_query.html",
        fields=fields,
        storages=storages,
        crops=crops,
        carts=carts,
        loads=loads,
        selected_field=selected_field,
        selected_storage=selected_storage,
        error=error,
        mc_avg=mc_avg,
        lbs_wet=lbs_wet,
        bu_wet=bu_wet,
        dry_bushels=bushels_sum
    )



@app.route("/pace")
@login_required
def pace():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)

    # Optional: earliest harvest date (like "1st Harvest Date" in Excel)
    cur.execute("SELECT MIN(Harvest_Date) AS first_date FROM Harvest;")
    first_date = cur.fetchone()["first_date"]

    # Build a date window (Excel shows lots of days; we can default to 60 days)
    # You can also pass ?start=YYYY-MM-DD&end=YYYY-MM-DD
    start = request.args.get("start")
    end = request.args.get("end")

    if not start:
        start_date = first_date if first_date else date.today()
    else:
        start_date = date.fromisoformat(start)

    if not end:
        end_date = start_date + timedelta(days=60)
    else:
        end_date = date.fromisoformat(end)

    # Pace logic (matches your Excel formulas):
    # Bushels = SUM(Bushels) by Date
    # Corn = SUM(Bushels) where Crop is C or HMC
    # Soybean = SUM(Bushels) where Crop is B
    # Milo = SUM(Bushels) where Crop is M
    #
    # IMPORTANT: Your Harvest table stores Crop_ID, so we join Crop to read Crop_Code.
    cur.execute("""
        SELECT
          h.Harvest_Date AS Date,
          SUM(h.Bushels) AS Bushels,
          SUM(CASE WHEN c.Crop_Code IN ('C','HMC') THEN h.Bushels ELSE 0 END) AS Corn,
          SUM(CASE WHEN c.Crop_Code = 'B' THEN h.Bushels ELSE 0 END) AS Soybean,
          SUM(CASE WHEN c.Crop_Code = 'M' THEN h.Bushels ELSE 0 END) AS Milo
        FROM Harvest h
        JOIN Crop c ON h.Crop_ID = c.Crop_ID
        WHERE h.Harvest_Date BETWEEN %s AND %s
        GROUP BY h.Harvest_Date
        ORDER BY h.Harvest_Date;
    """, (start_date, end_date))

    rows = cur.fetchall()
    cur.close()
    conn.close()

    # Format numbers safely
    def fnum(x):
        if x is None:
            return 0
        if isinstance(x, Decimal):
            return float(x)
        return float(x)

    # Totals row (optional but helpful)
    totals = {
        "Bushels": sum(fnum(r["Bushels"]) for r in rows),
        "Corn": sum(fnum(r["Corn"]) for r in rows),
        "Soybean": sum(fnum(r["Soybean"]) for r in rows),
        "Milo": sum(fnum(r["Milo"]) for r in rows),
    }

    return render_template(
        "pace.html",
        first_date=first_date,
        start_date=start_date,
        end_date=end_date,
        rows=rows,
        totals=totals
    )



def _to_float(x):
    if x is None:
        return 0.0
    if isinstance(x, Decimal):
        return float(x)
    return float(x)

def _month_name_to_num(name: str) -> int:
    name = (name or "").strip().lower()
    months = {m.lower(): i for i, m in enumerate(calendar.month_name) if m}
    return months.get(name, 0)

@app.route("/billing", methods=["GET"])
@login_required
def billing():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)

    # Dropdown options
    cur.execute("SELECT DelLoc_ID, DelLoc_code, Location FROM Delivery_Location ORDER BY DelLoc_code;")
    locations = cur.fetchall()

    cur.execute("SELECT Crop_ID, Crop_Code, Crop_Name FROM Crop ORDER BY Crop_Code;")
    crops = cur.fetchall()

    # ---- Read user inputs (Excel-like) ----
    today = date.today()

    # Default: current month
    default_month_name = calendar.month_name[today.month]

    month_name = request.args.get("month", default_month_name)
    delivered_to_code = request.args.get("to", (locations[0]["DelLoc_code"] if locations else ""))
    crop_code = request.args.get("crop", (crops[0]["Crop_Code"] if crops else ""))

    # Default start/end = selected month range (same idea as Excel)
    month_num = _month_name_to_num(month_name) or today.month
    year = today.year

    start_default = date(year, month_num, 1)
    end_default = date(year, month_num, calendar.monthrange(year, month_num)[1])

    start_str = request.args.get("start", start_default.isoformat())
    end_str = request.args.get("end", end_default.isoformat())

    start_date = date.fromisoformat(start_str)
    end_date = date.fromisoformat(end_str)

    # Resolve IDs from codes (for SQL filtering)
    del_loc_id = None
    crop_id = None

    for loc in locations:
        if loc["DelLoc_code"] == delivered_to_code:
            del_loc_id = loc["DelLoc_ID"]
            break

    for c in crops:
        if c["Crop_Code"] == crop_code:
            crop_id = c["Crop_ID"]
            break

    # ---- Query delivery rows (table like Excel) ----
    # Map Excel columns:
    # Load -> Ticket_Num
    # To -> Delivery_Location code
    # Storage -> Bin_Name
    cur.execute("""
        SELECT
          d.Ticket_Num        AS Load_Num,
          d.Delivery_Date     AS Delivery_Date,
          c.Crop_Code         AS Crop,
          dl.DelLoc_code      AS ToCode,
          d.MC                AS MC,
          d.Gross_Weight      AS Gross,
          d.Tare_Weight       AS Tare,
          sl.Bin_Name         AS Storage,
          d.Bushels           AS Bushels,
          d.Price             AS Price
        FROM Delivery d
        JOIN Crop c ON d.Crop_ID = c.Crop_ID
        JOIN Delivery_Location dl ON d.DelLoc_ID = dl.DelLoc_ID
        LEFT JOIN Storage_Location sl ON d.StorLoc_ID = sl.StorLoc_ID
        WHERE d.Delivery_Date BETWEEN %s AND %s
          AND (%s IS NULL OR d.DelLoc_ID = %s)
          AND (%s IS NULL OR d.Crop_ID = %s)
        ORDER BY d.Delivery_Date, d.Ticket_Num;
    """, (start_date, end_date, del_loc_id, del_loc_id, crop_id, crop_id))

    rows = cur.fetchall()

    # Compute Total column like Excel: Total = Bushels * Price
    for r in rows:
        bus = _to_float(r.get("Bushels"))
        price = r.get("Price")
        price_val = _to_float(price) if price is not None else None
        r["Total"] = (bus * price_val) if price_val is not None else None

    # Summary (Excel: Total & Avg Price)
    totals_sum = sum(_to_float(r["Total"]) for r in rows if r["Total"] is not None)
    price_vals = [_to_float(r["Price"]) for r in rows if r.get("Price") is not None]
    avg_price = (sum(price_vals) / len(price_vals)) if price_vals else None

    cur.close()
    conn.close()

    return render_template(
        "billing.html",
        invoice_date=today,
        month_name=month_name,
        delivered_to_code=delivered_to_code,
        crop_code=crop_code,
        start_date=start_date,
        end_date=end_date,
        locations=locations,
        crops=crops,
        rows=rows,
        totals_sum=totals_sum,
        avg_price=avg_price
    )



@app.route("/reports")
@login_required
def reports():
    return render_template("reports.html")





def _f(x):
    if x is None:
        return 0.0
    if isinstance(x, Decimal):
        return float(x)
    return float(x)

@app.route("/reconcile", methods=["GET"])
@login_required
def reconcile():
    # filters
    start = request.args.get("start")
    end = request.args.get("end")
    crop_id = request.args.get("crop_id", "")  # optional

    if start:
        start_date = date.fromisoformat(start)
    else:
        start_date = date.today() - timedelta(days=30)

    if end:
        end_date = date.fromisoformat(end)
    else:
        end_date = date.today()

    conn = get_conn()
    cur = conn.cursor(dictionary=True)

    # dropdown crops
    cur.execute("SELECT Crop_ID, Crop_Code, Crop_Name FROM Crop ORDER BY Crop_Code;")
    crops = cur.fetchall()

    crop_filter_sql = ""
    params_h = [start_date, end_date]
    params_d = [start_date, end_date]

    if crop_id:
        crop_filter_sql = " AND h.Crop_ID = %s "
        params_h.append(crop_id)

        crop_filter_sql_d = " AND d.Crop_ID = %s "
        params_d.append(crop_id)
    else:
        crop_filter_sql_d = ""

    # ------------------ SUMMARY TOTALS ------------------
    # Harvest totals
    cur.execute(f"""
        SELECT
          COUNT(*) AS harvest_rows,
          AVG(h.MC) AS harvest_avg_mc,
          SUM(COALESCE(h.Gross_Weight,0) - COALESCE(h.Tare_Weight,0)) AS harvest_lbs_wet,
          SUM(COALESCE(h.Bushels,0)) AS harvest_bushels
        FROM Harvest h
        WHERE h.Harvest_Date BETWEEN %s AND %s
        {crop_filter_sql}
    """, tuple(params_h))
    harvest_sum = cur.fetchone() or {}

    # Delivery totals
    cur.execute(f"""
        SELECT
          COUNT(*) AS delivery_rows,
          AVG(d.MC) AS delivery_avg_mc,
          SUM(COALESCE(d.Gross_Weight,0) - COALESCE(d.Tare_Weight,0)) AS delivery_lbs_wet,
          SUM(COALESCE(d.Bushels,0)) AS delivery_bushels,
          SUM(COALESCE(d.Gross_Sale,0)) AS delivery_gross_sale,
          SUM(COALESCE(d.Sale_Discounts,0)) AS delivery_discounts,
          SUM(COALESCE(d.Gross_Sale,0) - COALESCE(d.Sale_Discounts,0)) AS delivery_net_sale
        FROM Delivery d
        WHERE d.Delivery_Date BETWEEN %s AND %s
        {crop_filter_sql_d}
    """, tuple(params_d))
    delivery_sum = cur.fetchone() or {}

    # Differences (Delivery - Harvest)
    diff = {
        "bushels": _f(delivery_sum.get("delivery_bushels")) - _f(harvest_sum.get("harvest_bushels")),
        "lbs_wet": _f(delivery_sum.get("delivery_lbs_wet")) - _f(harvest_sum.get("harvest_lbs_wet")),
        "avg_mc":  (_f(delivery_sum.get("delivery_avg_mc")) - _f(harvest_sum.get("harvest_avg_mc")))
    }

    # ------------------ LOAD-LEVEL RECONCILIATION ------------------
    # Full outer join simulation using UNION:
    # match Harvest.Load_Num (varchar) with Delivery.Ticket_Num (int cast to char)
    cur.execute(f"""
        (
          SELECT
            h.Load_Num AS load_key,
            h.Harvest_Date AS harvest_date,
            f.Field_Name AS field_name,
            sl.Bin_Name AS harvest_storage,
            c.Crop_Code AS crop_code,
            h.MC AS harvest_mc,
            h.Gross_Weight AS harvest_gross,
            h.Tare_Weight AS harvest_tare,
            h.Bushels AS harvest_bushels,

            d.Delivery_Date AS delivery_date,
            dl.DelLoc_code AS delivered_to,
            d.MC AS delivery_mc,
            d.Gross_Weight AS delivery_gross,
            d.Tare_Weight AS delivery_tare,
            d.Bushels AS delivery_bushels,
            d.Price AS price,
            d.Gross_Sale AS gross_sale,
            d.Sale_Discounts AS discounts,
            (COALESCE(d.Gross_Sale,0) - COALESCE(d.Sale_Discounts,0)) AS net_sale,

            'MATCH/LEFT' AS side
          FROM Harvest h
          JOIN Field f ON h.Field_ID = f.Field_ID
          JOIN Crop c ON h.Crop_ID = c.Crop_ID
          LEFT JOIN Storage_Location sl ON h.StorLoc_ID = sl.StorLoc_ID
          LEFT JOIN Delivery d ON CAST(d.Ticket_Num AS CHAR) = h.Load_Num
          LEFT JOIN Delivery_Location dl ON d.DelLoc_ID = dl.DelLoc_ID
          WHERE h.Harvest_Date BETWEEN %s AND %s
          {crop_filter_sql}
        )
        UNION
        (
          SELECT
            CAST(d.Ticket_Num AS CHAR) AS load_key,
            NULL AS harvest_date,
            NULL AS field_name,
            NULL AS harvest_storage,
            c.Crop_Code AS crop_code,
            NULL AS harvest_mc,
            NULL AS harvest_gross,
            NULL AS harvest_tare,
            NULL AS harvest_bushels,

            d.Delivery_Date AS delivery_date,
            dl.DelLoc_code AS delivered_to,
            d.MC AS delivery_mc,
            d.Gross_Weight AS delivery_gross,
            d.Tare_Weight AS delivery_tare,
            d.Bushels AS delivery_bushels,
            d.Price AS price,
            d.Gross_Sale AS gross_sale,
            d.Sale_Discounts AS discounts,
            (COALESCE(d.Gross_Sale,0) - COALESCE(d.Sale_Discounts,0)) AS net_sale,

            'RIGHT-ONLY' AS side
          FROM Delivery d
          JOIN Crop c ON d.Crop_ID = c.Crop_ID
          LEFT JOIN Delivery_Location dl ON d.DelLoc_ID = dl.DelLoc_ID
          LEFT JOIN Harvest h ON h.Load_Num = CAST(d.Ticket_Num AS CHAR)
          WHERE d.Delivery_Date BETWEEN %s AND %s
          {crop_filter_sql_d}
          AND h.Harvest_ID IS NULL
        )
        ORDER BY load_key;
    """, tuple(params_h + params_d))

    rows = cur.fetchall()

    # compute per-row diffs in python (easier than SQL)
    for r in rows:
        hb = r.get("harvest_bushels")
        db = r.get("delivery_bushels")
        r["bushel_diff"] = ( _f(db) - _f(hb) ) if (hb is not None or db is not None) else None

        hg = r.get("harvest_gross")
        ht = r.get("harvest_tare")
        dg = r.get("delivery_gross")
        dt = r.get("delivery_tare")
        r["lbs_diff"] = (_f(dg) - _f(dt)) - (_f(hg) - _f(ht)) if (hg is not None or dg is not None) else None

    cur.close()
    conn.close()

    return render_template(
        "reconcile.html",
        crops=crops,
        selected_crop_id=crop_id,
        start_date=start_date,
        end_date=end_date,
        harvest_sum=harvest_sum,
        delivery_sum=delivery_sum,
        diff=diff,
        rows=rows
    )



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

# @app.route("/slingshot/jobdata")
# def slingshot_jobdata():
#     data = get_jobdata_summary(pagesize=20)  # try small page first
#     return jsonify(data)


