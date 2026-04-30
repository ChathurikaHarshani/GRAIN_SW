from flask import Flask, render_template, jsonify, request, redirect, url_for, session, abort,send_file
from db import get_conn
from datetime import date, timedelta
from decimal import Decimal
import calendar
from functools import wraps
from dotenv import load_dotenv
import os
import bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import pymysql
from io import BytesIO
import pandas as pd
#from slingshot_client import main as run_slingshot_import






app = Flask(__name__)


app.secret_key = os.getenv("SECRET_KEY", "dev-secret-change-me")

@app.route("/")
def landing():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return render_template("landing.html")




login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, row):
        self.id = row["id"]
        self.username = row["username"]
        self.role = row["role"]
        self.password_hash = row["password_hash"]
        self._active = bool(row.get("is_active", 1))

    @property
    def is_admin(self):
        return self.role == "admin"

    def is_active(self):
        return self._active

    


@login_manager.user_loader
def load_user(user_id):
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE id=%s AND is_active=1", (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return User(row) if row else None



@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        conn = get_conn()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE username=%s AND is_active=1", (username,))
        user_row = cur.fetchone()
        cur.close()
        conn.close()

        if not user_row or not bcrypt.checkpw(
            password.encode(), user_row["password_hash"].encode()
        ):
            error = "Invalid username or password"
        else:
            login_user(User(user_row))
            return redirect(url_for("dashboard"))

    return render_template("login.html", error=error)






@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("landing"))



def admin_required(view):
    @wraps(view)
    @login_required
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return view(*args, **kwargs)
    return wrapper





@app.route("/signup", methods=["GET", "POST"])
def signup():
    # if already logged in, go to dashboard
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm  = request.form.get("confirm_password", "")

        if not username:
            error = "Username is required."
        elif password != confirm:
            error = "Passwords do not match."
        elif len(password) < 6:
            error = "Password must be at least 6 characters."
        else:
            pw_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

            conn = get_conn()
            cur = conn.cursor(dictionary=True)
            # check existing user
            cur.execute("SELECT id FROM users WHERE username=%s", (username,))
            exists = cur.fetchone()

            if exists:
                error = "Username already exists. Please choose another."
                cur.close(); conn.close()
            else:
                cur2 = conn.cursor()
                cur2.execute("""
                    INSERT INTO users (username, password_hash, role, is_active)
                    VALUES (%s, %s, 'user', 1)
                """, (username, pw_hash))
                conn.commit()
                cur2.close()
                cur.close()
                conn.close()

                return redirect(url_for("login"))

    return render_template("signup.html", error=error)























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





def calculate_bushels(gross_val, tare_val, mc_val, wpb, base_mc):
    if gross_val is None or wpb is None or wpb == 0:
        return None
    tare_val = tare_val or 0.0
    net_lbs = gross_val - tare_val
    wet_bu = net_lbs / wpb
    if mc_val is not None and base_mc is not None and mc_val > base_mc:
        return round(wet_bu * ((100.0 - mc_val) / (100.0 - base_mc)), 2)
    return round(wet_bu, 2)


def calculated_bushels_sql(weight_alias: str, crop_alias: str) -> str:
    return f"""
        CASE
          WHEN {weight_alias}.Gross_Weight IS NULL
            OR {crop_alias}.Weight_PerBushel IS NULL
            OR {crop_alias}.Weight_PerBushel = 0
            THEN {weight_alias}.Bushels
          WHEN {weight_alias}.MC IS NOT NULL
            AND {crop_alias}.Base_MC IS NOT NULL
            AND {weight_alias}.MC > {crop_alias}.Base_MC
            THEN (
              ((COALESCE({weight_alias}.Gross_Weight, 0) - COALESCE({weight_alias}.Tare_Weight, 0)) / {crop_alias}.Weight_PerBushel)
              * ((100 - {weight_alias}.MC) / (100 - {crop_alias}.Base_MC))
            )
          ELSE (
            (COALESCE({weight_alias}.Gross_Weight, 0) - COALESCE({weight_alias}.Tare_Weight, 0)) / {crop_alias}.Weight_PerBushel
          )
        END
    """









# ----------------- Grower: list + create ----------------- #
@app.route("/growers")
@admin_required
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
@admin_required
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
@admin_required
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
@admin_required
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
@admin_required
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
@admin_required
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
@admin_required
def list_carts():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT Cart_ID, Cart_Code, Cart_Name FROM Cart ORDER BY Cart_Name;")
    carts = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("carts.html", carts=carts)

@app.route("/carts/new", methods=["GET", "POST"])
@admin_required
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
@admin_required
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
@admin_required
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
@admin_required
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
@admin_required
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
@admin_required
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
@admin_required
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
@admin_required
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
@admin_required
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

# @app.route("/harvest-query", methods=["GET", "POST"])
# def harvest_query():
#     conn = get_conn()
#     cur = conn.cursor(dictionary=True)

#     # Dropdown data
#     cur.execute("SELECT Field_ID, Field_Name FROM Field ORDER BY Field_Name;")
#     fields = cur.fetchall()

#     cur.execute("SELECT StorLoc_ID, Bin_Name FROM Storage_Location ORDER BY Bin_Name;")
#     storages = cur.fetchall()

#     cur.execute("SELECT Crop_ID, Crop_Name, Weight_PerBushel FROM Crop ORDER BY Crop_Name;")
#     crops = cur.fetchall()

#     cur.execute("SELECT Cart_ID, Cart_Name FROM Cart ORDER BY Cart_Name;")
#     carts = cur.fetchall()

#     # Filters (from URL query params)
#     selected_field = request.args.get("field_id", "")
#     selected_storage = request.args.get("storloc_id", "")

#     error = None

#     # ----------- POST: insert a new Harvest row -----------
#     if request.method == "POST":
#         load_num = request.form.get("load_num", "").strip()
#         harvest_date = request.form.get("harvest_date", "").strip()
#         field_id = request.form.get("field_id", "").strip()
#         storloc_id = request.form.get("storloc_id", "").strip()
#         crop_id = request.form.get("crop_id", "").strip()
#         cart_id = request.form.get("cart_id", "").strip()
#         bushels_val = request.form.get("Bushels", "").strip()
#         mc = request.form.get("mc", "").strip()
#         gross = request.form.get("gross", "").strip()
#         tare = request.form.get("tare", "").strip()
#         note = request.form.get("note", "").strip()

#         if not (load_num and harvest_date and field_id and storloc_id and crop_id and cart_id):
#             error = "Load, Date, Field, Storage, Crop, and Cart are required."
#         else:
#             # Get Dpt_ID from selected field (auto)
#             cur.execute("SELECT Dpt_ID FROM Field WHERE Field_ID=%s;", (field_id,))
#             row = cur.fetchone()
#             if not row:
#                 error = "Selected Field not found."
#             else:
#                 dpt_id = row["Dpt_ID"]

#                 # # Weight per bushel for bushel calculation
#                 # cur.execute("SELECT Weight_PerBushel FROM Crop WHERE Crop_ID=%s;", (crop_id,))
#                 # crop_row = cur.fetchone()
#                 # wpb = float(crop_row["Weight_PerBushel"]) if crop_row and crop_row["Weight_PerBushel"] else None



#                 # Weight per bushel + Base moisture for Excel-like bushels calculation
#                 cur.execute("SELECT Weight_PerBushel, Base_MC FROM Crop WHERE Crop_ID=%s;", (crop_id,))
#                 crop_row = cur.fetchone()
#                 wpb = float(crop_row["Weight_PerBushel"]) if crop_row and crop_row["Weight_PerBushel"] is not None else None
#                 base_mc = float(crop_row["Base_MC"]) if crop_row and crop_row["Base_MC"] is not None else None



#                 gross_val = float(gross) if gross else None
#                 tare_val = float(tare) if tare else 0.0
#                 mc_val = float(mc) if mc else None

#                 # bushels_val = None
#                 # if wpb and gross_val is not None:
#                 #     bushels_val = (gross_val - tare_val) / wpb




#                 cur2 = conn.cursor()
#                 cur2.execute("""
#                     INSERT INTO Harvest
#                       (Cart_ID, Field_ID, Crop_ID, Dpt_ID, StorLoc_ID,
#                        Load_Num, Harvest_Date, MC, Gross_Weight, Tare_Weight, Bushels, Note)
#                     VALUES
#                       (%s, %s, %s, %s, %s,
#                        %s, %s, %s, %s, %s, %s, %s);
#                 """, (
#                     int(cart_id), int(field_id), int(crop_id), int(dpt_id), int(storloc_id),
#                     load_num, harvest_date, mc_val, gross_val, tare_val, bushels_val, (note if note else None)
#                 ))
#                 conn.commit()
#                 cur2.close()

#                 # After insert, keep filters on screen
#                 conn.close()
#                 return redirect(url_for("harvest_query", field_id=field_id, storloc_id=storloc_id))

#     # ----------- GET: show table (filtered) -----------
#     where = []
#     params = []

#     if selected_field:
#         where.append("h.Field_ID = %s")
#         params.append(selected_field)
#     if selected_storage:
#         where.append("h.StorLoc_ID = %s")
#         params.append(selected_storage)

#     where_sql = ("WHERE " + " AND ".join(where)) if where else ""

#     cur.execute(f"""
#         SELECT
#           h.Harvest_ID,
#           h.Load_Num,
#           h.Harvest_Date,
#           f.Field_Name,
#           cr.Crop_Name,
#           h.MC,
#           h.Gross_Weight,
#           h.Tare_Weight,
#           s.Bin_Name AS Storage,
#           h.Bushels,
#           h.Note
#         FROM Harvest h
#         JOIN Field f ON h.Field_ID = f.Field_ID
#         JOIN Crop cr ON h.Crop_ID = cr.Crop_ID
#         JOIN Storage_Location s ON h.StorLoc_ID = s.StorLoc_ID
#         {where_sql}
#         ORDER BY h.Harvest_Date DESC, h.Load_Num DESC;
#     """, tuple(params))

#     loads = cur.fetchall()
#     # ---------- Summary calculations (like Excel SUBTOTAL) ----------
#     mc_values = [float(r["MC"]) for r in loads if r["MC"] is not None]
#     mc_avg = (sum(mc_values) / len(mc_values)) if mc_values else None

#     gross_sum = sum(float(r["Gross_Weight"]) for r in loads if r["Gross_Weight"] is not None)
#     tare_sum = sum(float(r["Tare_Weight"]) for r in loads if r["Tare_Weight"] is not None)
#     lbs_wet = gross_sum - tare_sum

#     bushels_sum = sum(float(r["Bushels"]) for r in loads if r["Bushels"] is not None)

#     # Determine wet bu conversion factor:
#     # if selected crop is Beans ("B") -> 60 else 56
#     # We'll infer from the first row crop name, or default to 56
#     factor = 56
#     if loads:
#         crop_name = (loads[0].get("Crop_Name") or "").lower()
#         if "bean" in crop_name or crop_name in ["b", "beans", "soybean", "soybeans"]:
#             factor = 60

#     bu_wet = (lbs_wet / factor) if factor and lbs_wet is not None else None
    
#     cur.close()
#     conn.close()

#     return render_template(
#         "harvest_query.html",
#         fields=fields,
#         storages=storages,
#         crops=crops,
#         carts=carts,
#         loads=loads,
#         selected_field=selected_field,
#         selected_storage=selected_storage,
#         error=error,
#         mc_avg=mc_avg,
#         lbs_wet=lbs_wet,
#         bu_wet=bu_wet,
#         dry_bushels=bushels_sum
#     )


@app.route("/harvest-query", methods=["GET", "POST"])
@login_required
def harvest_query():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)

    # ---------------- Filters ----------------
    selected_field_id = request.args.get("field_id", "").strip()
    selected_field = request.args.get("field_name", "").strip()
    selected_storage = request.args.get("storloc_id", "").strip()
    selected_year = request.args.get("crop_year", "").strip()
    selected_edit_id = request.args.get("edit_id", "").strip()

    # ---------------- Dropdown data ----------------
    field_filter_where = []
    field_filter_params = []

    if selected_year:
        field_filter_where.append("f.Crop_Year = %s")
        field_filter_params.append(selected_year)

    field_filter_sql = ("WHERE " + " AND ".join(field_filter_where)) if field_filter_where else ""

    cur.execute("""
        SELECT DISTINCT
            f.Field_ID,
            f.Field_Name,
            f.Crop_Year
        FROM Harvest h
        JOIN Field f ON h.Field_ID = f.Field_ID
        {field_filter_sql}
        ORDER BY f.Field_Name, f.Crop_Year DESC, f.Field_ID;
    """.format(field_filter_sql=field_filter_sql), tuple(field_filter_params))
    fields = cur.fetchall()

    if selected_field_id and selected_year:
        selected_field_matches_year = any(str(f["Field_ID"]) == selected_field_id for f in fields)
        if not selected_field_matches_year:
            selected_field_id = ""

    cur.execute("SELECT StorLoc_ID, Bin_Name FROM Storage_Location ORDER BY Bin_Name;")
    storages = cur.fetchall()



    cur.execute("""
    SELECT Field_ID, Field_Name, Crop_Year
    FROM Field
    ORDER BY Field_Name, Crop_Year DESC;
    """)
    entry_fields = cur.fetchall()

    # Distinct years for filter dropdown
    cur.execute("""
        SELECT DISTINCT Crop_Year
        FROM Field
        WHERE Crop_Year IS NOT NULL
        ORDER BY Crop_Year DESC;
    """)
    years = cur.fetchall()

    cur.execute("SELECT Crop_ID, Crop_Name, Weight_PerBushel FROM Crop ORDER BY Crop_Name;")
    crops = cur.fetchall()

    cur.execute("SELECT Cart_ID, Cart_Name FROM Cart ORDER BY Cart_Name;")
    carts = cur.fetchall()

    error = None
    edit_load = None

    if selected_edit_id:
        cur.execute("""
            SELECT
              Harvest_ID,
              Cart_ID,
              Field_ID,
              Crop_ID,
              StorLoc_ID,
              Load_Num,
              Harvest_Date,
              MC,
              Gross_Weight,
              Tare_Weight,
              Note
            FROM Harvest
            WHERE Harvest_ID = %s;
        """, (selected_edit_id,))
        edit_load = cur.fetchone()
        if not edit_load:
            selected_edit_id = ""


    # ---------------- POST: insert a new Harvest row ----------------
    if request.method == "POST":
        harvest_id = request.form.get("harvest_id", "").strip()
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

        if not (load_num and harvest_date and field_id and crop_id and cart_id):
            error = "Load, Date, Field, Crop, and Cart are required."
        elif not harvest_id and not storloc_id:
            error = "Storage is required for new loads."
        else:
            cur.execute("SELECT Dpt_ID FROM Field WHERE Field_ID=%s;", (field_id,))
            row = cur.fetchone()
            if not row:
                error = "Selected Field not found."
            else:
                dpt_id = row["Dpt_ID"]

                cur.execute("SELECT Weight_PerBushel, Base_MC FROM Crop WHERE Crop_ID=%s;", (crop_id,))
                crop_row = cur.fetchone()
                wpb = float(crop_row["Weight_PerBushel"]) if crop_row and crop_row["Weight_PerBushel"] is not None else None
                base_mc = float(crop_row["Base_MC"]) if crop_row and crop_row["Base_MC"] is not None else None

                gross_val = float(gross) if gross else None
                tare_val = float(tare) if tare else 0.0
                mc_val = float(mc) if mc else None
                storloc_val = int(storloc_id) if storloc_id else None
                bushels_val = calculate_bushels(
                    gross_val,
                    tare_val,
                    mc_val,
                    wpb,
                    base_mc,
                )

                cur2 = conn.cursor()
                if harvest_id:
                    cur2.execute("""
                        UPDATE Harvest
                        SET Cart_ID = %s,
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
                            Note = %s
                        WHERE Harvest_ID = %s;
                    """, (
                        int(cart_id), int(field_id), int(crop_id), int(dpt_id), storloc_val,
                        load_num, harvest_date, mc_val, gross_val, tare_val, bushels_val,
                        (note if note else None), int(harvest_id)
                    ))
                else:
                    cur2.execute("""
                        INSERT INTO Harvest
                          (Cart_ID, Field_ID, Crop_ID, Dpt_ID, StorLoc_ID,
                           Load_Num, Harvest_Date, MC, Gross_Weight, Tare_Weight, Bushels, Note)
                        VALUES
                          (%s, %s, %s, %s, %s,
                           %s, %s, %s, %s, %s, %s, %s);
                    """, (
                        int(cart_id), int(field_id), int(crop_id), int(dpt_id), storloc_val,
                        load_num, harvest_date, mc_val, gross_val, tare_val, bushels_val, (note if note else None)
                    ))
                conn.commit()
                cur2.close()

                return redirect(url_for(
                    "harvest_query",
                    field_id=selected_field_id,
                    field_name=selected_field,
                    storloc_id=selected_storage,
                    crop_year=selected_year
                ))

    # ---------------- GET: show filtered loads ----------------
    where = []
    params = []

    if selected_field_id:
        where.append("h.Field_ID = %s")
        params.append(selected_field_id)
    elif selected_field:
        where.append("f.Field_Name = %s")
        params.append(selected_field)

    if selected_storage:
        where.append("h.StorLoc_ID = %s")
        params.append(selected_storage)

    if selected_year:
        where.append("f.Crop_Year = %s")
        params.append(selected_year)

    where_sql = ("WHERE " + " AND ".join(where)) if where else ""

    cur.execute(f"""
        SELECT
          h.Harvest_ID,
          h.Load_Num,
          h.Harvest_Date,
          f.Field_Name,
          f.Crop_Year,
          cr.Crop_Name,
          cr.Crop_Code,
          cr.Weight_PerBushel,
          cr.Base_MC,
          h.MC,
          h.Gross_Weight,
          h.Tare_Weight,
          s.Bin_Name AS Storage,
          h.Bushels,
          h.Note
        FROM Harvest h
        JOIN Field f ON h.Field_ID = f.Field_ID
        JOIN Crop cr ON h.Crop_ID = cr.Crop_ID
        LEFT JOIN Storage_Location s ON h.StorLoc_ID = s.StorLoc_ID
        {where_sql}
        ORDER BY h.Harvest_Date DESC, h.Load_Num DESC;
    """, tuple(params))

    loads = cur.fetchall()

    for row in loads:
        calculated_bushels = calculate_bushels(
            float(row["Gross_Weight"]) if row["Gross_Weight"] is not None else None,
            float(row["Tare_Weight"]) if row["Tare_Weight"] is not None else 0.0,
            float(row["MC"]) if row["MC"] is not None else None,
            float(row["Weight_PerBushel"]) if row["Weight_PerBushel"] is not None else None,
            float(row["Base_MC"]) if row["Base_MC"] is not None else None,
        )
        row["Calculated_Bushels"] = calculated_bushels if calculated_bushels is not None else row["Bushels"]

    # ---------------- Summary ----------------
    mc_values = [float(r["MC"]) for r in loads if r["MC"] is not None]
    mc_avg = (sum(mc_values) / len(mc_values)) if mc_values else None

    gross_sum = sum(float(r["Gross_Weight"]) for r in loads if r["Gross_Weight"] is not None)
    tare_sum = sum(float(r["Tare_Weight"]) for r in loads if r["Tare_Weight"] is not None)
    lbs_wet = gross_sum - tare_sum

    bushels_sum = sum(float(r["Calculated_Bushels"]) for r in loads if r["Calculated_Bushels"] is not None)

    factor = 56
    if loads:
        crop_code = (loads[0].get("Crop_Code") or "").lower()
        crop_name = (loads[0].get("Crop_Name") or "").lower()
        if crop_code == "b" or "bean" in crop_name or crop_name in ["beans", "soybean", "soybeans"]:
            factor = 60

    bu_wet = (lbs_wet / factor) if factor and lbs_wet is not None else None

    cur.close()
    conn.close()

    return render_template(
        "harvest_query.html",
        fields=fields,
        entry_fields=entry_fields,
        storages=storages,
        years=years,
        crops=crops,
        carts=carts,
        loads=loads,
        selected_field=selected_field,
        selected_field_id=selected_field_id,
        selected_storage=selected_storage,
        selected_year=selected_year,
        error=error,
        mc_avg=mc_avg,
        lbs_wet=lbs_wet,
        bu_wet=bu_wet,
        dry_bushels=bushels_sum,
        edit_load=edit_load
    )




@app.route("/harvest-summary", methods=["GET"])
@login_required
def harvest_summary():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)

    selected_field_id = request.args.get("field_id", "").strip()
    selected_field = request.args.get("field_name", "").strip()
    selected_storage = request.args.get("storloc_id", "").strip()
    selected_year = request.args.get("crop_year", "").strip()

    where = []
    params = []

    if selected_field_id:
        where.append("h.Field_ID = %s")
        params.append(selected_field_id)
    elif selected_field:
        where.append("f.Field_Name = %s")
        params.append(selected_field)

    if selected_storage:
        where.append("h.StorLoc_ID = %s")
        params.append(selected_storage)

    if selected_year:
        where.append("f.Crop_Year = %s")
        params.append(selected_year)

    where_sql = ("WHERE " + " AND ".join(where)) if where else ""

    cur.execute(f"""
        SELECT
          f.Field_ID,
          f.Field_Name,
          f.Acres,
          f.Crop_Year,
          SUM(COALESCE(h.Gross_Weight,0) - COALESCE(h.Tare_Weight,0)) AS total_lbs_wet,
          SUM(
            CASE
              WHEN h.Gross_Weight IS NULL OR c.Weight_PerBushel IS NULL OR c.Weight_PerBushel = 0 THEN 0
              WHEN h.MC IS NOT NULL AND c.Base_MC IS NOT NULL AND h.MC > c.Base_MC
                THEN (
                  ((COALESCE(h.Gross_Weight, 0) - COALESCE(h.Tare_Weight, 0)) / c.Weight_PerBushel)
                  * ((100 - h.MC) / (100 - c.Base_MC))
                )
              ELSE (
                (COALESCE(h.Gross_Weight, 0) - COALESCE(h.Tare_Weight, 0)) / c.Weight_PerBushel
              )
            END
          ) AS total_dry_bushels,
          AVG(h.MC) AS avg_mc
        FROM Harvest h
        JOIN Field f ON h.Field_ID = f.Field_ID
        JOIN Crop c ON h.Crop_ID = c.Crop_ID
        {where_sql}
        GROUP BY f.Field_ID, f.Field_Name, f.Acres, f.Crop_Year
        ORDER BY f.Field_Name, f.Crop_Year;
    """, tuple(params))

    rows = cur.fetchall()

    for r in rows:
        acres = r.get("Acres")
        dry_bu = r.get("total_dry_bushels") or 0
        if acres and float(acres) > 0:
            r["bu_per_acre"] = float(dry_bu) / float(acres)
        else:
            r["bu_per_acre"] = None

    totals = {
        "total_lbs_wet": sum(_to_float(r.get("total_lbs_wet")) for r in rows),
        "total_dry_bushels": sum(_to_float(r.get("total_dry_bushels")) for r in rows),
    }
    mc_vals = [r.get("avg_mc") for r in rows if r.get("avg_mc") is not None]
    totals["avg_mc"] = (sum(_to_float(x) for x in mc_vals) / len(mc_vals)) if mc_vals else None

    cur.close()
    conn.close()

    return render_template(
        "harvest_summary.html",
        rows=rows,
        totals=totals,
        selected_field=selected_field,
        selected_field_id=selected_field_id,
        selected_storage=selected_storage,
        selected_year=selected_year
    )


@app.route("/pace")
@login_required
def pace():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    harvest_bu_sql = calculated_bushels_sql("h", "c")

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

    # Pace logic (matches the workbook intent):
    # Bushels = SUM(Bushels) by Date
    # Corn = corn/HMC rows
    # Soybean = soybean rows, regardless of whether Crop_Name is Soybean or Soybeans
    # Milo = milo/sorghum rows
    cur.execute("""
        SELECT
          h.Harvest_Date AS Date,
          SUM(COALESCE(""" + harvest_bu_sql + """, 0)) AS Bushels,
          SUM(
            CASE
              WHEN UPPER(COALESCE(c.Crop_Code, '')) IN ('C', 'HMC')
                   OR LOWER(COALESCE(c.Crop_Name, '')) IN ('corn', 'hmc')
              THEN COALESCE(""" + harvest_bu_sql + """, 0)
              ELSE 0
            END
          ) AS Corn,
          SUM(
            CASE
              WHEN UPPER(COALESCE(c.Crop_Code, '')) IN ('B', 'SB', 'SOY', 'SOYBEAN', 'SOYBEANS')
                   OR LOWER(COALESCE(c.Crop_Name, '')) IN ('soybean', 'soybeans', 'beans')
              THEN COALESCE(""" + harvest_bu_sql + """, 0)
              ELSE 0
            END
          ) AS Soybean,
          SUM(
            CASE
              WHEN UPPER(COALESCE(c.Crop_Code, '')) IN ('M', 'MILO')
                   OR LOWER(COALESCE(c.Crop_Name, '')) IN ('milo', 'grain sorghum', 'sorghum')
              THEN COALESCE(""" + harvest_bu_sql + """, 0)
              ELSE 0
            END
          ) AS Milo
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

    for r in rows:
        if r["Date"]:
            r["DateStr"] = r["Date"].strftime("%m/%d/%Y")   # or "%b %d, %Y"
        else:
            r["DateStr"] = ""

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


def build_reconcile_context(start_date, end_date, crop_id=""):
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    harvest_bu_sql = calculated_bushels_sql("h", "c")
    delivery_bu_sql = calculated_bushels_sql("d", "c")

    cur.execute("SELECT Crop_ID, Crop_Code, Crop_Name FROM Crop ORDER BY Crop_Code;")
    crops = cur.fetchall()

    crop_filter_sql_h = ""
    crop_filter_sql_d = ""
    params_h = [start_date, end_date]
    params_d = [start_date, end_date]

    if crop_id:
        crop_filter_sql_h = " AND h.Crop_ID = %s "
        crop_filter_sql_d = " AND d.Crop_ID = %s "
        params_h.append(crop_id)
        params_d.append(crop_id)

    cur.execute(f"""
        SELECT
          COUNT(*) AS harvest_rows,
          AVG(h.MC) AS harvest_avg_mc,
          SUM(COALESCE(h.Gross_Weight,0) - COALESCE(h.Tare_Weight,0)) AS harvest_lbs_wet,
          SUM(COALESCE({harvest_bu_sql},0)) AS harvest_bushels
        FROM Harvest h
        JOIN Crop c ON h.Crop_ID = c.Crop_ID
        WHERE h.Harvest_Date BETWEEN %s AND %s
        {crop_filter_sql_h}
    """, tuple(params_h))
    harvest_sum = cur.fetchone() or {}

    cur.execute(f"""
        SELECT
          COUNT(*) AS delivery_rows,
          AVG(d.MC) AS delivery_avg_mc,
          SUM(COALESCE(d.Gross_Weight,0) - COALESCE(d.Tare_Weight,0)) AS delivery_lbs_wet,
          SUM(COALESCE({delivery_bu_sql},0)) AS delivery_bushels,
          SUM(COALESCE(d.Gross_Sale,0)) AS delivery_gross_sale,
          SUM(COALESCE(d.Sale_Discounts,0)) AS delivery_discounts,
          SUM(COALESCE(d.Gross_Sale,0) - COALESCE(d.Sale_Discounts,0)) AS delivery_net_sale
        FROM Delivery d
        JOIN Crop c ON d.Crop_ID = c.Crop_ID
        WHERE d.Delivery_Date BETWEEN %s AND %s
        {crop_filter_sql_d}
    """, tuple(params_d))
    delivery_sum = cur.fetchone() or {}

    diff = {
        "bushels": _f(delivery_sum.get("delivery_bushels")) - _f(harvest_sum.get("harvest_bushels")),
        "lbs_wet": _f(delivery_sum.get("delivery_lbs_wet")) - _f(harvest_sum.get("harvest_lbs_wet")),
        "avg_mc": _f(delivery_sum.get("delivery_avg_mc")) - _f(harvest_sum.get("harvest_avg_mc")),
        "rows": _f(delivery_sum.get("delivery_rows")) - _f(harvest_sum.get("harvest_rows")),
    }

    cur.execute(f"""
        SELECT
          COALESCE(h_crop.Crop_Code, d_crop.Crop_Code, '-') AS crop_code,
          COALESCE(h_crop.Crop_Name, d_crop.Crop_Name, '-') AS crop_name,
          COALESCE(hv.harvest_rows, 0) AS harvest_rows,
          COALESCE(hv.harvest_bushels, 0) AS harvest_bushels,
          COALESCE(dv.delivery_rows, 0) AS delivery_rows,
          COALESCE(dv.delivery_bushels, 0) AS delivery_bushels
        FROM (
          SELECT
            h.Crop_ID,
            COUNT(*) AS harvest_rows,
            SUM(COALESCE({harvest_bu_sql},0)) AS harvest_bushels
          FROM Harvest h
          JOIN Crop c ON h.Crop_ID = c.Crop_ID
          WHERE h.Harvest_Date BETWEEN %s AND %s
          {crop_filter_sql_h}
          GROUP BY h.Crop_ID
        ) hv
        LEFT JOIN Crop h_crop ON hv.Crop_ID = h_crop.Crop_ID
        LEFT JOIN (
          SELECT
            d.Crop_ID,
            COUNT(*) AS delivery_rows,
            SUM(COALESCE({delivery_bu_sql},0)) AS delivery_bushels
          FROM Delivery d
          JOIN Crop c ON d.Crop_ID = c.Crop_ID
          WHERE d.Delivery_Date BETWEEN %s AND %s
          {crop_filter_sql_d}
          GROUP BY d.Crop_ID
        ) dv ON hv.Crop_ID = dv.Crop_ID
        LEFT JOIN Crop d_crop ON dv.Crop_ID = d_crop.Crop_ID
        UNION
        SELECT
          COALESCE(h_crop.Crop_Code, d_crop.Crop_Code, '-') AS crop_code,
          COALESCE(h_crop.Crop_Name, d_crop.Crop_Name, '-') AS crop_name,
          COALESCE(hv.harvest_rows, 0) AS harvest_rows,
          COALESCE(hv.harvest_bushels, 0) AS harvest_bushels,
          COALESCE(dv.delivery_rows, 0) AS delivery_rows,
          COALESCE(dv.delivery_bushels, 0) AS delivery_bushels
        FROM (
          SELECT
            d.Crop_ID,
            COUNT(*) AS delivery_rows,
            SUM(COALESCE({delivery_bu_sql},0)) AS delivery_bushels
          FROM Delivery d
          JOIN Crop c ON d.Crop_ID = c.Crop_ID
          WHERE d.Delivery_Date BETWEEN %s AND %s
          {crop_filter_sql_d}
          GROUP BY d.Crop_ID
        ) dv
        LEFT JOIN Crop d_crop ON dv.Crop_ID = d_crop.Crop_ID
        LEFT JOIN (
          SELECT
            h.Crop_ID,
            COUNT(*) AS harvest_rows,
            SUM(COALESCE({harvest_bu_sql},0)) AS harvest_bushels
          FROM Harvest h
          JOIN Crop c ON h.Crop_ID = c.Crop_ID
          WHERE h.Harvest_Date BETWEEN %s AND %s
          {crop_filter_sql_h}
          GROUP BY h.Crop_ID
        ) hv ON hv.Crop_ID = dv.Crop_ID
        LEFT JOIN Crop h_crop ON hv.Crop_ID = h_crop.Crop_ID
        WHERE hv.Crop_ID IS NULL
        ORDER BY crop_code, crop_name
    """, tuple(params_h + params_d + params_d + params_h))
    crop_rows = cur.fetchall()

    for row in crop_rows:
        row["bushel_diff"] = _f(row.get("delivery_bushels")) - _f(row.get("harvest_bushels"))
        row["row_diff"] = _f(row.get("delivery_rows")) - _f(row.get("harvest_rows"))

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
            {harvest_bu_sql} AS harvest_bushels,
            d.Delivery_Date AS delivery_date,
            dl.DelLoc_code AS delivered_to,
            d.MC AS delivery_mc,
            d.Gross_Weight AS delivery_gross,
            d.Tare_Weight AS delivery_tare,
            {delivery_bu_sql} AS delivery_bushels,
            d.Price AS price,
            d.Gross_Sale AS gross_sale,
            d.Sale_Discounts AS discounts,
            (COALESCE(d.Gross_Sale,0) - COALESCE(d.Sale_Discounts,0)) AS net_sale
          FROM Harvest h
          JOIN Field f ON h.Field_ID = f.Field_ID
          JOIN Crop c ON h.Crop_ID = c.Crop_ID
          LEFT JOIN Storage_Location sl ON h.StorLoc_ID = sl.StorLoc_ID
          LEFT JOIN Delivery d ON CAST(d.Ticket_Num AS CHAR) = h.Load_Num
          LEFT JOIN Delivery_Location dl ON d.DelLoc_ID = dl.DelLoc_ID
          WHERE h.Harvest_Date BETWEEN %s AND %s
          {crop_filter_sql_h}
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
            {delivery_bu_sql} AS delivery_bushels,
            d.Price AS price,
            d.Gross_Sale AS gross_sale,
            d.Sale_Discounts AS discounts,
            (COALESCE(d.Gross_Sale,0) - COALESCE(d.Sale_Discounts,0)) AS net_sale
          FROM Delivery d
          JOIN Crop c ON d.Crop_ID = c.Crop_ID
          LEFT JOIN Delivery_Location dl ON d.DelLoc_ID = dl.DelLoc_ID
          LEFT JOIN Harvest h ON h.Load_Num = CAST(d.Ticket_Num AS CHAR)
          WHERE d.Delivery_Date BETWEEN %s AND %s
          {crop_filter_sql_d}
            AND h.Harvest_ID IS NULL
        )
        ORDER BY load_key, harvest_date, delivery_date
    """, tuple(params_h + params_d))
    rows = cur.fetchall()

    matched_count = 0
    harvest_only_count = 0
    delivery_only_count = 0

    for row in rows:
        row["bushel_diff"] = _f(row.get("delivery_bushels")) - _f(row.get("harvest_bushels"))
        row["lbs_diff"] = (
            (_f(row.get("delivery_gross")) - _f(row.get("delivery_tare")))
            - (_f(row.get("harvest_gross")) - _f(row.get("harvest_tare")))
        )

        if row.get("delivery_date") is None:
            row["status"] = "Harvest Only"
            harvest_only_count += 1
        elif row.get("harvest_date") is None:
            row["status"] = "Delivery Only"
            delivery_only_count += 1
        else:
            row["status"] = "Matched"
            matched_count += 1

    cur.close()
    conn.close()

    return {
        "crops": crops,
        "selected_crop_id": crop_id,
        "start_date": start_date,
        "end_date": end_date,
        "harvest_sum": harvest_sum,
        "delivery_sum": delivery_sum,
        "diff": diff,
        "crop_rows": crop_rows,
        "rows": rows,
        "status_counts": {
            "matched": matched_count,
            "harvest_only": harvest_only_count,
            "delivery_only": delivery_only_count,
        },
    }


def build_inventory_snapshot(crop_year="", crop_name=""):
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    harvest_bu_sql = calculated_bushels_sql("h", "c")
    delivery_bu_sql = calculated_bushels_sql("d", "c")

    harvest_q = """
        SELECT
            s.StorLoc_ID,
            s.Bin_Name,
            c.Crop_Name,
            SUM(COALESCE(""" + harvest_bu_sql + """, 0)) AS Harvest_Bu,
            CASE
              WHEN SUM(COALESCE(""" + harvest_bu_sql + """, 0)) = 0 THEN NULL
              ELSE SUM(COALESCE(""" + harvest_bu_sql + """, 0) * COALESCE(h.MC, 0))
                   / SUM(COALESCE(""" + harvest_bu_sql + """, 0))
            END AS Avg_MC
        FROM Storage_Location s
        LEFT JOIN Harvest h ON h.StorLoc_ID = s.StorLoc_ID
        LEFT JOIN Crop c ON c.Crop_ID = h.Crop_ID
        LEFT JOIN Field fi ON fi.Field_ID = h.Field_ID
        WHERE 1=1
    """
    params = []

    if crop_year:
        harvest_q += " AND fi.Crop_Year = %s"
        params.append(crop_year)

    if crop_name:
        harvest_q += " AND c.Crop_Name LIKE %s"
        params.append(f"%{crop_name}%")

    harvest_q += """
        GROUP BY s.StorLoc_ID, s.Bin_Name, c.Crop_Name
        ORDER BY s.Bin_Name, c.Crop_Name
    """
    cur.execute(harvest_q, params)
    harvest_rows = cur.fetchall()

    delivery_q = """
        SELECT
            s.StorLoc_ID,
            s.Bin_Name,
            c.Crop_Name,
            SUM(COALESCE(""" + delivery_bu_sql + """, 0)) AS Delivered_Bu
        FROM Storage_Location s
        LEFT JOIN Delivery d ON d.StorLoc_ID = s.StorLoc_ID
        LEFT JOIN Crop c ON c.Crop_ID = d.Crop_ID
        WHERE 1=1
    """
    delivery_params = []

    if crop_name:
        delivery_q += " AND c.Crop_Name LIKE %s"
        delivery_params.append(f"%{crop_name}%")

    delivery_q += """
        GROUP BY s.StorLoc_ID, c.Crop_Name
    """
    cur.execute(delivery_q, delivery_params)
    delivery_rows = cur.fetchall()

    cur.close()
    conn.close()

    delivered_map = {}
    for row in delivery_rows:
        key = (row["StorLoc_ID"], row["Crop_Name"] or "-")
        delivered_map[key] = float(row["Delivered_Bu"] or 0)

    inventory_rows = []
    seen_keys = set()

    for row in harvest_rows:
        crop_label = row["Crop_Name"] or "-"
        key = (row["StorLoc_ID"], crop_label)
        seen_keys.add(key)
        harvest_bu = float(row["Harvest_Bu"] or 0)
        delivered_bu = delivered_map.get(key, 0.0)
        inventory_rows.append({
            "Bin_Name": row["Bin_Name"],
            "Note": None,
            "Crop_Name": crop_label,
            "Harvest_Bu": round(harvest_bu, 2),
            "Avg_MC": None if row["Avg_MC"] is None else round(float(row["Avg_MC"]), 2),
            "Delivered_Bu": round(delivered_bu, 2),
            "Current_Bu": round(harvest_bu - delivered_bu, 2),
        })

    for row in delivery_rows:
        crop_label = row["Crop_Name"] or "-"
        key = (row["StorLoc_ID"], crop_label)
        if key in seen_keys:
            continue
        delivered_bu = float(row["Delivered_Bu"] or 0)
        inventory_rows.append({
            "Bin_Name": row["Bin_Name"],
            "Note": None,
            "Crop_Name": crop_label,
            "Harvest_Bu": 0.0,
            "Avg_MC": None,
            "Delivered_Bu": round(delivered_bu, 2),
            "Current_Bu": round(-delivered_bu, 2),
        })

    inventory_rows.sort(key=lambda x: ((x["Bin_Name"] or ""), (x["Crop_Name"] or "")))

    summary = {}
    for row in inventory_rows:
        crop = row["Crop_Name"] or "-"
        summary.setdefault(crop, {"Harvest": 0.0, "Delivered": 0.0, "Inventory": 0.0})
        summary[crop]["Harvest"] += row["Harvest_Bu"]
        summary[crop]["Delivered"] += row["Delivered_Bu"]
        summary[crop]["Inventory"] += row["Current_Bu"]

    corn_split = {
        "Dry": {"Harvest": 0.0, "Delivered": 0.0, "Inventory": 0.0},
        "HMC": {"Harvest": 0.0, "Delivered": 0.0, "Inventory": 0.0},
    }
    for row in inventory_rows:
        crop_name_lower = (row["Crop_Name"] or "").lower()
        if "corn" not in crop_name_lower:
            continue
        mc = row["Avg_MC"]
        label = "Dry" if (mc is not None and mc <= 15.5) else "HMC"
        corn_split[label]["Harvest"] += row["Harvest_Bu"]
        corn_split[label]["Delivered"] += row["Delivered_Bu"]
        corn_split[label]["Inventory"] += row["Current_Bu"]

    return inventory_rows, summary, corn_split

@app.route("/billing", methods=["GET"])
@admin_required
def billing():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    delivery_bu_sql = calculated_bushels_sql("d", "c")

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
          """ + delivery_bu_sql + """ AS Bushels,
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


@app.route("/reconcile")
@login_required
def reconcile():
    start = request.args.get("start")
    end = request.args.get("end")
    crop_id = request.args.get("crop_id", "")

    start_date = date.fromisoformat(start) if start else (date.today() - timedelta(days=30))
    end_date = date.fromisoformat(end) if end else date.today()

    context = build_reconcile_context(start_date, end_date, crop_id)
    return render_template("reconcile.html", **context)




def _f(x):
    if x is None:
        return 0.0
    if isinstance(x, Decimal):
        return float(x)
    return float(x)

@app.route("/delivery", methods=["GET"])
@login_required
def delivery():
    start = request.args.get("start")
    end = request.args.get("end")
    crop_id = request.args.get("crop_id", "")
    start_date = date.fromisoformat(start) if start else (date.today() - timedelta(days=30))
    end_date = date.fromisoformat(end) if end else date.today()

    context = build_reconcile_context(start_date, end_date, crop_id)
    return render_template("delivery.html", **context)



# -------------------------
# Yield Report (Excel-like)
# -------------------------
@app.route("/yield", methods=["GET"])
@login_required
def yield_report():
    # Filters
    crop_year   = request.args.get("crop_year", "").strip()   # Field.Crop_Year
    grower      = request.args.get("grower", "").strip()
    department  = request.args.get("department", "").strip()
    field       = request.args.get("field", "").strip()
    crop        = request.args.get("crop", "").strip()

    harvest_bu_sql = calculated_bushels_sql("h", "c")
    query = """
        SELECT
            fi.Crop_Year AS Crop_Year,
            g.Grower_Name,
            d.Dpt_Name AS Department_Name,
            fi.Field_Name,
            c.Crop_Name,
            fi.Acres,

            SUM(COALESCE(""" + harvest_bu_sql + """, 0)) AS Total_Bushels,
            ROUND(SUM(COALESCE(""" + harvest_bu_sql + """, 0)) / NULLIF(fi.Acres, 0), 2) AS Yield_bu_per_acre,

            ROUND(AVG(h.MC), 2) AS Avg_MC,

            SUM(COALESCE(""" + harvest_bu_sql + """, 0)) AS Total_WetBushels,
            SUM(COALESCE(""" + harvest_bu_sql + """, 0)) AS Total_DryBushels,
            ROUND(SUM(COALESCE(""" + harvest_bu_sql + """, 0)) / NULLIF(fi.Acres, 0), 2) AS Dry_Yield_bu_per_acre

        FROM Harvest h
        JOIN Field fi       ON h.Field_ID = fi.Field_ID
        JOIN Department d   ON fi.Dpt_ID = d.Dpt_ID
        JOIN Grower g       ON d.Grower_ID = g.Grower_ID
        JOIN Crop c         ON h.Crop_ID = c.Crop_ID

        WHERE 1=1
    """

    params = []

    # Apply filters
    if crop_year:
        query += " AND fi.Crop_Year = %s"
        params.append(crop_year)

    if grower:
        query += " AND g.Grower_Name LIKE %s"
        params.append(f"%{grower}%")

    if department:
        query += " AND d.Dpt_Name LIKE %s"
        params.append(f"%{department}%")

    if field:
        query += " AND fi.Field_Name LIKE %s"
        params.append(f"%{field}%")

    if crop:
        query += " AND c.Crop_Name LIKE %s"
        params.append(f"%{crop}%")

    query += """
        GROUP BY
            fi.Crop_Year, g.Grower_Name, d.Dpt_Name, fi.Field_Name, c.Crop_Name, fi.Acres
        ORDER BY
            fi.Crop_Year DESC, g.Grower_Name, d.Dpt_Name, fi.Field_Name
    """

    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute(query, params)
    results = cur.fetchall()
    cur.close()
    conn.close()

    active_filters = {
        "crop_year": crop_year,
        "grower": grower,
        "department": department,
        "field": field,
        "crop": crop
    }

    return render_template("yield.html", results=results, active_filters=active_filters)


# -------------------------
# Export Yield Report Excel
# -------------------------
@app.route("/yield/export", methods=["GET"])
@login_required
def yield_export():
    crop_year   = request.args.get("crop_year", "").strip()
    grower      = request.args.get("grower", "").strip()
    department  = request.args.get("department", "").strip()
    field       = request.args.get("field", "").strip()
    crop        = request.args.get("crop", "").strip()

    harvest_bu_sql = calculated_bushels_sql("h", "c")
    query = """
        SELECT
            fi.Crop_Year AS Crop_Year,
            g.Grower_Name,
            d.Dpt_Name AS Department_Name,
            fi.Field_Name,
            c.Crop_Name,
            fi.Acres,

            SUM(COALESCE(""" + harvest_bu_sql + """, 0)) AS Total_Bushels,
            ROUND(SUM(COALESCE(""" + harvest_bu_sql + """, 0)) / NULLIF(fi.Acres, 0), 2) AS Yield_bu_per_acre,

            ROUND(AVG(h.MC), 2) AS Avg_MC,

            SUM(COALESCE(""" + harvest_bu_sql + """, 0)) AS Total_WetBushels,
            SUM(COALESCE(""" + harvest_bu_sql + """, 0)) AS Total_DryBushels,
            ROUND(SUM(COALESCE(""" + harvest_bu_sql + """, 0)) / NULLIF(fi.Acres, 0), 2) AS Dry_Yield_bu_per_acre

        FROM Harvest h
        JOIN Field fi       ON h.Field_ID = fi.Field_ID
        JOIN Department d   ON fi.Dpt_ID = d.Dpt_ID
        JOIN Grower g       ON d.Grower_ID = g.Grower_ID
        JOIN Crop c         ON h.Crop_ID = c.Crop_ID

        WHERE 1=1
    """

    params = []

    if crop_year:
        query += " AND fi.Crop_Year = %s"
        params.append(crop_year)
    if grower:
        query += " AND g.Grower_Name LIKE %s"
        params.append(f"%{grower}%")
    if department:
        query += " AND d.Dpt_Name LIKE %s"
        params.append(f"%{department}%")
    if field:
        query += " AND fi.Field_Name LIKE %s"
        params.append(f"%{field}%")
    if crop:
        query += " AND c.Crop_Name LIKE %s"
        params.append(f"%{crop}%")

    query += """
        GROUP BY
            fi.Crop_Year, g.Grower_Name, d.Dpt_Name, fi.Field_Name, c.Crop_Name, fi.Acres
        ORDER BY
            fi.Crop_Year DESC, g.Grower_Name, d.Dpt_Name, fi.Field_Name
    """

    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    df = pd.DataFrame(rows)

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Yields")
        ws = writer.sheets["Yields"]
        ws.freeze_panes = "A2"

    output.seek(0)
    return send_file(output, as_attachment=True, download_name="Yield_Report.xlsx")


@app.route("/inventory", methods=["GET"])
@login_required
def inventory_report():
    # Filters (optional)
    crop_year = request.args.get("crop_year", "").strip()   # from Field.Crop_Year
    crop_name = request.args.get("crop", "").strip()        # Crop.Crop_Name (contains search)
    inventory_rows, summary, corn_split = build_inventory_snapshot(
        crop_year=crop_year,
        crop_name=crop_name,
    )

    active_filters = {"crop_year": crop_year, "crop": crop_name}

    return render_template(
        "inventory.html",
        rows=inventory_rows,
        summary=summary,
        corn_split=corn_split,
        active_filters=active_filters
    )


@app.route("/inventory/export", methods=["GET"])
@login_required
def inventory_export():
    # same filters
    crop_year = request.args.get("crop_year", "").strip()
    crop_name = request.args.get("crop", "").strip()
    rows, _, _ = build_inventory_snapshot(crop_year=crop_year, crop_name=crop_name)
    df = pd.DataFrame([
        {
            "BIN LOCATION": row["Bin_Name"],
            "Note": row["Note"] or "",
            "CROP": row["Crop_Name"],
            "HARVEST": row["Harvest_Bu"],
            "MC": row["Avg_MC"],
            "DELIVERED": row["Delivered_Bu"],
            "CURRENT": row["Current_Bu"],
        }
        for row in rows
    ])
    if not df.empty:
        df = df.sort_values(["BIN LOCATION", "CROP"])

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Inventory")
        writer.sheets["Inventory"].freeze_panes = "A2"
    output.seek(0)

    return send_file(output, as_attachment=True, download_name="Inventory_Report.xlsx")


# @app.route("/slingshot/import")
# @login_required
# def slingshot_import():
#     try:
#         run_slingshot_import()
#         return {"status": "ok", "message": "Slingshot import completed"}
#     except Exception as e:
#         return {"status": "error", "message": str(e)}, 500

















if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

# @app.route("/slingshot/jobdata")
# def slingshot_jobdata():
#     data = get_jobdata_summary(pagesize=20)  # try small page first
#     return jsonify(data)


