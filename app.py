from flask import Flask, render_template, jsonify, request, redirect, url_for, session, abort, send_file, flash
from db import get_conn
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP
import calendar
import math
import re
from functools import wraps
from dotenv import load_dotenv
import os
import bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from mysql.connector import IntegrityError
from io import BytesIO
import pandas as pd
#from slingshot_client import main as run_slingshot_import






app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
from invitations import bp as invitations_bp, ensure_schema as ensure_invitation_schema, csrf_token as access_csrf_token, check_csrf as check_access_csrf, email_ready
app.register_blueprint(invitations_bp)
from password_reset import bp as password_reset_bp, ensure_schema as ensure_password_reset_schema, password_version
app.register_blueprint(password_reset_bp)
from email_verification import bp as email_verification_bp, ensure_schema as ensure_email_verification_schema, issue_verification
from invitations import unl_email
app.register_blueprint(email_verification_bp)
app.jinja_env.globals['access_csrf_token'] = access_csrf_token
_access_schema_ready = False


app.secret_key = os.getenv("SECRET_KEY", "dev-secret-change-me")

@app.route("/")
def landing():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    ensure_access_schema()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM grower_memberships WHERE role='admin' AND status='active'")
    needs_setup = cur.fetchone()[0] == 0
    cur.close(); conn.close()
    if needs_setup:
        return redirect(url_for("first_run_setup"))
    return render_template("landing.html")




login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@app.before_request
def protect_pending_accounts():
    if request.endpoint in ("password_reset.forgot", "password_reset.reset", "email_verification.account", "email_verification.verify"):
        ensure_access_schema()
    if not current_user.is_authenticated:
        return None
    allowed = {"access_pending", "logout", "static", "invitations.accept", "password_reset.forgot", "password_reset.reset", "email_verification.account", "email_verification.verify"}
    if current_user.membership_status != "active" and request.endpoint not in allowed:
        return redirect(url_for("access_pending"))


@app.context_processor
def access_context():
    return {
        "can_edit": bool(current_user.is_authenticated and getattr(current_user, "can_edit", False)),
    }


class User(UserMixin):
    def __init__(self, row, membership=None):
        self.id = row["id"]
        self.username = row["username"]
        self.role = row["role"]
        self.password_hash = row["password_hash"]
        self._active = bool(row.get("is_active", 1))
        membership = membership or {}
        self.grower_id = membership.get("Grower_ID")
        self.grower_name = membership.get("Grower_Name")
        self.grower_role = membership.get("membership_role")
        self.membership_status = membership.get("membership_status")

    @property
    def is_admin(self):
        return self.grower_role == "admin" and self.membership_status == "active"

    @property
    def can_edit(self):
        return self.grower_role in ("editor", "admin") and self.membership_status == "active"

    @property
    def is_active(self):
        return self._active

    


def ensure_access_schema():
    """Create the access-control tables and preserve access for existing installs."""
    global _access_schema_ready
    if _access_schema_ready:
        return
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS grower_memberships (
          id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
          user_id BIGINT UNSIGNED NOT NULL,
          Grower_ID BIGINT UNSIGNED NOT NULL,
          role ENUM('viewer','editor','admin') NOT NULL DEFAULT 'viewer',
          status ENUM('pending','active','rejected') NOT NULL DEFAULT 'pending',
          created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
          approved_at TIMESTAMP NULL,
          approved_by BIGINT UNSIGNED NULL,
          PRIMARY KEY (id),
          UNIQUE KEY uq_grower_membership (user_id, Grower_ID),
          CONSTRAINT fk_membership_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
          CONSTRAINT fk_membership_grower FOREIGN KEY (Grower_ID) REFERENCES Grower(Grower_ID) ON DELETE CASCADE,
          CONSTRAINT fk_membership_approver FOREIGN KEY (approved_by) REFERENCES users(id) ON DELETE SET NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)
    ensure_invitation_schema(cur)
    ensure_password_reset_schema(cur)
    ensure_email_verification_schema(cur)
    # Tables without an existing Department/Field path need an explicit owner.
    tenant_tables = ("Cart", "Storage_Location", "Delivery_Location", "MarketPriceMonthly", "Delivery")
    for table_name in tenant_tables:
        cur.execute("""SELECT COUNT(*) FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME=%s AND COLUMN_NAME='Grower_ID'""", (table_name,))
        if not cur.fetchone()[0]:
            cur.execute(f"ALTER TABLE `{table_name}` ADD COLUMN Grower_ID BIGINT UNSIGNED NULL")
    # Backward-compatible migration: existing accounts were already trusted. Attach
    # them to the first existing Grower; legacy admins become Grower admins.
    cur.execute("SELECT COUNT(*) FROM grower_memberships")
    membership_count = cur.fetchone()[0]
    if membership_count == 0:
        cur.execute("SELECT Grower_ID FROM Grower ORDER BY Grower_ID LIMIT 1")
        grower = cur.fetchone()
        if grower:
            cur.execute("""
                INSERT INTO grower_memberships (user_id, Grower_ID, role, status, approved_at)
                SELECT id, %s, IF(role='admin','admin','editor'), 'active', NOW()
                FROM users WHERE is_active=1
            """, (grower[0],))
    cur.execute("SELECT Grower_ID FROM Grower ORDER BY Grower_ID LIMIT 1")
    first_grower = cur.fetchone()
    if first_grower:
        for table_name in tenant_tables:
            cur.execute(f"UPDATE `{table_name}` SET Grower_ID=%s WHERE Grower_ID IS NULL", (first_grower[0],))
    conn.commit()
    cur.close()
    conn.close()
    _access_schema_ready = True


def get_membership(user_id):
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT gm.Grower_ID, g.Grower_Name,
               gm.role AS membership_role, gm.status AS membership_status
        FROM grower_memberships gm
        JOIN Grower g ON g.Grower_ID=gm.Grower_ID
        WHERE gm.user_id=%s
        ORDER BY (gm.status='active') DESC, (gm.Grower_ID=%s) DESC, gm.id
        LIMIT 1
    """, (user_id, session.get('active_grower_id', 0)))
    membership = cur.fetchone()
    cur.close()
    conn.close()
    return membership


@login_manager.user_loader
def load_user(user_id):
    ensure_access_schema()
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE id=%s AND is_active=1", (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row and session.get('password_version') != password_version(row['password_hash']):
        return None
    return User(row, get_membership(user_id)) if row else None



@app.route("/login", methods=["GET", "POST"])
def login():
    ensure_access_schema()
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

        if not user_row or len(password.encode()) > 72 or not bcrypt.checkpw(
            password.encode(), user_row["password_hash"].encode()
        ):
            error = "Invalid username or password"
        else:
            user = User(user_row, get_membership(user_row["id"]))
            login_user(user)
            session["password_version"] = password_version(user_row["password_hash"])
            return redirect(url_for("dashboard") if user.membership_status == "active" else url_for("access_pending"))

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


def membership_required(view):
    @wraps(view)
    @login_required
    def wrapper(*args, **kwargs):
        if current_user.membership_status != "active" or not current_user.grower_id:
            return redirect(url_for("access_pending"))
        return view(*args, **kwargs)
    return wrapper


def editor_required(view):
    @wraps(view)
    @membership_required
    def wrapper(*args, **kwargs):
        if not current_user.can_edit:
            abort(403)
        return view(*args, **kwargs)
    return wrapper


@app.route("/access-pending")
@login_required
def access_pending():
    if current_user.membership_status == "active":
        return redirect(url_for("dashboard"))
    return render_template("access_pending.html")


@app.route("/setup", methods=["GET", "POST"])
def first_run_setup():
    """Bootstrap the first Grower administrator on a truly empty install."""
    ensure_access_schema()
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT COUNT(*) AS n FROM grower_memberships WHERE role='admin' AND status='active'")
    if cur.fetchone()["n"]:
        cur.close(); conn.close()
        abort(404)
    error = None
    if request.method == "POST":
        grower_name = request.form.get("grower_name", "").strip()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")
        if not grower_name or not username:
            error = "Grower name and username are required."
        elif password != confirm or len(password) < 8:
            error = "Passwords must match and contain at least 8 characters."
        else:
            cur.execute("SELECT id FROM users WHERE username=%s", (username,))
            if cur.fetchone():
                error = "Username already exists."
            else:
                pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                try:
                    cur.execute("INSERT INTO Grower (Grower_Name) VALUES (%s)", (grower_name,))
                    grower_id = cur.lastrowid
                    cur.execute("INSERT INTO users (username,password_hash,role,is_active) VALUES (%s,%s,'admin',1)", (username, pw_hash))
                    user_id = cur.lastrowid
                    cur.execute("""INSERT INTO grower_memberships
                        (user_id,Grower_ID,role,status,approved_at) VALUES (%s,%s,'admin','active',NOW())""", (user_id, grower_id))
                    conn.commit()
                    cur.close(); conn.close()
                    return redirect(url_for("login"))
                except Exception:
                    conn.rollback()
                    raise
    cur.close(); conn.close()
    return render_template("setup.html", error=error)





@app.route("/signup", methods=["GET", "POST"])
def signup():
    ensure_access_schema()
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    error = None
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    try:
        if request.method == "POST":
            check_access_csrf()
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")
            confirm = request.form.get("confirm_password", "")
            grower_id = request.form.get("grower_id", type=int)
            try:
                email = unl_email(request.form.get("email", ""))
                if not username or len(username)>80 or not grower_id:
                    raise ValueError("Username (up to 80 characters) and Grower are required.")
                if password != confirm or len(password)<8 or len(password.encode())>72:
                    raise ValueError("Passwords must match and contain at least eight characters (maximum 72 bytes).")
                cur.execute("SELECT Grower_ID FROM Grower WHERE Grower_ID=%s", (grower_id,))
                if not cur.fetchone():
                    raise ValueError("Select a valid Grower.")
                cur.execute("SELECT user_id FROM user_emails WHERE email=%s", (email,))
                if cur.fetchone():
                    raise ValueError("This email is already registered. Sign in or contact your administrator.")
                pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                cur.execute("INSERT INTO users (username,password_hash,role,is_active) VALUES (%s,%s,'user',1)", (username,pw_hash))
                user_id = cur.lastrowid
                cur.execute("""INSERT INTO grower_memberships (user_id,Grower_ID,role,status)
                    VALUES (%s,%s,'viewer','pending')""", (user_id,grower_id))
                conn.commit()
                login_user(User({'id':user_id,'username':username,'role':'user','password_hash':pw_hash,'is_active':1},get_membership(user_id)))
                session['password_version'] = password_version(pw_hash)
                try:
                    notice=issue_verification(user_id,email)
                except ValueError as exc:
                    notice=str(exc)
                flash("Account created. Administrator approval is still required. " + notice, "info")
                return redirect(url_for('email_verification.account'))
            except ValueError as exc:
                conn.rollback()
                error = str(exc)
            except IntegrityError:
                conn.rollback()
                error = "This username is already registered. Choose another or sign in."
        cur.execute("SELECT Grower_ID, Grower_Name FROM Grower ORDER BY Grower_Name")
        growers=cur.fetchall()
    finally:
        cur.close();conn.close()
    return render_template("signup.html", error=error, growers=growers)


@app.route("/users", methods=["GET", "POST"])
@admin_required
def manage_users():
    if request.method == "POST":
        check_access_csrf()
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    if request.method == "POST":
        membership_id = request.form.get("membership_id", type=int)
        action = request.form.get("action", "")
        action_map = {
            "approve_viewer": ("viewer", "active"),
            "approve_editor": ("editor", "active"),
            "approve_admin": ("admin", "active"),
            "reject": ("viewer", "rejected"),
            "suspend": ("viewer", "pending"),
        }
        if not membership_id or action not in action_map:
            abort(400)
        role, status = action_map[action]
        cur.execute("SELECT user_id, role, status FROM grower_memberships WHERE id=%s AND Grower_ID=%s", (membership_id, current_user.grower_id))
        existing = cur.fetchone()
        if not existing:
            abort(404)
        if existing["user_id"] == int(current_user.id) and (role != "admin" or status != "active"):
            flash("You cannot remove your own active administrator access.", "danger")
        else:
            cur.execute("""UPDATE grower_memberships SET role=%s,status=%s,
                approved_at=IF(%s='active',NOW(),approved_at), approved_by=IF(%s='active',%s,approved_by)
                WHERE id=%s AND Grower_ID=%s""",
                (role, status, status, status, current_user.id, membership_id, current_user.grower_id))
            conn.commit()
            messages = {
                "approve_viewer": "User approved as Viewer.",
                "approve_editor": "User approved as Editor.",
                "approve_admin": "User approved as Admin.",
                "reject": "Access request rejected.",
                "suspend": "User access suspended.",
            }
            flash(messages[action], "success")
        cur.close(); conn.close()
        return redirect(url_for("manage_users"))
    cur.execute("""
        SELECT gm.id, u.username, u.full_name, gm.role, gm.status, gm.created_at
        FROM grower_memberships gm JOIN users u ON u.id=gm.user_id
        WHERE gm.Grower_ID=%s ORDER BY (gm.status='pending') DESC, u.username
    """, (current_user.grower_id,))
    memberships = cur.fetchall()
    cur.execute("""SELECT id,email,role,status,created_at,expires_at,
        (expires_at <= UTC_TIMESTAMP()) AS expired FROM user_invitations
        WHERE Grower_ID=%s ORDER BY created_at DESC""", (current_user.grower_id,))
    invitations = cur.fetchall()
    cur.close(); conn.close()
    return render_template("users.html", memberships=memberships, invitations=invitations, email_ready=email_ready())


@app.route("/season-setup", methods=["GET", "POST"])
@admin_required
def season_setup():
    default_target = date.today().year
    target_year = request.values.get("target_year", str(default_target)).strip()
    try:
        target_year_int = int(target_year)
        source_year = request.values.get("source_year", str(target_year_int - 1)).strip()
        source_year_int = int(source_year)
        if not 1900 <= target_year_int <= 2100 or not 1900 <= source_year_int <= 2100:
            raise ValueError
    except ValueError:
        abort(400)

    conn = get_conn(); cur = conn.cursor(dictionary=True)
    if request.method == "POST":
        if source_year_int == target_year_int:
            flash("Source and target crop years must be different.", "danger")
        else:
            cur.execute("""
                INSERT INTO Field (Field_Name, Acres, Silage_Bu_Per_Acre, Crop_Year, Irr_Type, Hybrid_Variety, Note, Dpt_ID)
                SELECT src.Field_Name, src.Acres, src.Silage_Bu_Per_Acre, %s, src.Irr_Type, src.Hybrid_Variety,
                       CONCAT('Copied from ', %s, IF(src.Note IS NULL OR src.Note='', '', CONCAT(' — ', src.Note))),
                       src.Dpt_ID
                FROM Field src JOIN Department d ON d.Dpt_ID=src.Dpt_ID
                WHERE d.Grower_ID=%s AND src.Crop_Year=%s
                  AND NOT EXISTS (
                    SELECT 1 FROM Field existing
                    WHERE existing.Dpt_ID=src.Dpt_ID AND existing.Field_Name=src.Field_Name
                      AND existing.Crop_Year=%s
                  )
            """, (target_year_int, source_year_int, current_user.grower_id, source_year_int, target_year_int))
            copied = cur.rowcount
            conn.commit()
            flash(f"Copied {copied} field{'s' if copied != 1 else ''} into crop year {target_year_int}. Existing fields were skipped.", "success")
        cur.close(); conn.close()
        return redirect(url_for("season_setup", target_year=target_year_int, source_year=source_year_int))

    counts = {}
    checks = {
        "departments": ("SELECT COUNT(*) AS n FROM Department WHERE Grower_ID=%s", (current_user.grower_id,)),
        "source_fields": ("""SELECT COUNT(*) AS n FROM Field f JOIN Department d ON d.Dpt_ID=f.Dpt_ID WHERE d.Grower_ID=%s AND f.Crop_Year=%s""", (current_user.grower_id, source_year_int)),
        "target_fields": ("""SELECT COUNT(*) AS n FROM Field f JOIN Department d ON d.Dpt_ID=f.Dpt_ID WHERE d.Grower_ID=%s AND f.Crop_Year=%s""", (current_user.grower_id, target_year_int)),
        "carts": ("SELECT COUNT(*) AS n FROM Cart WHERE Grower_ID=%s", (current_user.grower_id,)),
        "storage": ("SELECT COUNT(*) AS n FROM Storage_Location WHERE Grower_ID=%s", (current_user.grower_id,)),
        "active_users": ("SELECT COUNT(*) AS n FROM grower_memberships WHERE Grower_ID=%s AND status='active'", (current_user.grower_id,)),
        "test_loads": ("""SELECT COUNT(*) AS n FROM Harvest h JOIN Field f ON f.Field_ID=h.Field_ID JOIN Department d ON d.Dpt_ID=f.Dpt_ID WHERE d.Grower_ID=%s AND f.Crop_Year=%s""", (current_user.grower_id, target_year_int)),
    }
    for key, (sql, params) in checks.items():
        cur.execute(sql, params); counts[key] = int((cur.fetchone() or {}).get("n") or 0)
    cur.execute("""SELECT DISTINCT f.Crop_Year FROM Field f JOIN Department d ON d.Dpt_ID=f.Dpt_ID WHERE d.Grower_ID=%s ORDER BY f.Crop_Year DESC""", (current_user.grower_id,))
    available_years = [int(row["Crop_Year"]) for row in cur.fetchall()]
    cur.close(); conn.close()
    checklist = [
        {"label": "Departments available", "done": counts["departments"] > 0, "detail": f'{counts["departments"]} departments'},
        {"label": f"Fields created for {target_year_int}", "done": counts["target_fields"] > 0, "detail": f'{counts["target_fields"]} fields'},
        {"label": "Grain carts reviewed", "done": counts["carts"] > 0, "detail": f'{counts["carts"]} carts'},
        {"label": "Storage bins reviewed", "done": counts["storage"] > 0, "detail": f'{counts["storage"]} locations'},
        {"label": "Users approved", "done": counts["active_users"] > 0, "detail": f'{counts["active_users"]} active users'},
        {"label": "Test harvest load entered", "done": counts["test_loads"] > 0, "detail": f'{counts["test_loads"]} loads'},
    ]
    return render_template("season_setup.html", target_year=target_year_int, source_year=source_year_int,
                           available_years=available_years, counts=counts, checklist=checklist)























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
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    harvest_bu_sql = calculated_bushels_sql("h", "c")
    delivery_bu_sql = calculated_bushels_sql("d", "c")

    cur.execute("""
        SELECT MAX(Crop_Year) AS crop_year
        FROM Field f JOIN Department d ON d.Dpt_ID=f.Dpt_ID
        WHERE f.Crop_Year IS NOT NULL AND d.Grower_ID=%s;
    """, (current_user.grower_id,))
    year_row = cur.fetchone() or {}
    dashboard_year = year_row.get("crop_year") or date.today().year

    cur.execute(f"""
        SELECT COALESCE(SUM(COALESCE({harvest_bu_sql}, 0)), 0) AS total_bushels,
               COUNT(*) AS load_count
        FROM Harvest h
        JOIN Crop c ON h.Crop_ID = c.Crop_ID
        JOIN Field f ON h.Field_ID = f.Field_ID JOIN Department d ON d.Dpt_ID=f.Dpt_ID
        WHERE f.Crop_Year = %s AND d.Grower_ID=%s;
    """, (dashboard_year, current_user.grower_id))
    harvest_totals = cur.fetchone() or {}

    cur.execute("""
        SELECT COUNT(DISTINCT g.Grower_ID) AS active_growers
        FROM Grower g
        JOIN Department d ON d.Grower_ID = g.Grower_ID
        JOIN Field f ON f.Dpt_ID = d.Dpt_ID
        JOIN Harvest h ON h.Field_ID = f.Field_ID
        WHERE f.Crop_Year = %s AND g.Grower_ID=%s;
    """, (dashboard_year, current_user.grower_id))
    grower_totals = cur.fetchone() or {}

    cur.execute("""
        SELECT COUNT(*) AS user_count,
               SUM(CASE WHEN gm.role = 'admin' THEN 1 ELSE 0 END) AS admin_count
        FROM users u JOIN grower_memberships gm ON gm.user_id=u.id
        WHERE u.is_active = 1 AND gm.status='active' AND gm.Grower_ID=%s;
    """, (current_user.grower_id,))
    user_totals = cur.fetchone() or {}

    cur.execute(f"""
        SELECT
            MONTH(d.Delivery_Date) AS delivery_month,
            COALESCE(SUM(COALESCE({delivery_bu_sql}, 0)), 0) AS bushels
        FROM Delivery d
        JOIN Crop c ON d.Crop_ID = c.Crop_ID
        WHERE YEAR(d.Delivery_Date) = %s AND d.Grower_ID=%s
        GROUP BY MONTH(d.Delivery_Date)
        ORDER BY MONTH(d.Delivery_Date);
    """, (dashboard_year, current_user.grower_id))
    monthly_rows = cur.fetchall()

    cur.execute(f"""
        SELECT COALESCE(SUM(COALESCE({delivery_bu_sql}, 0)), 0) AS delivered_bushels,
               COUNT(*) AS delivery_count
        FROM Delivery d
        JOIN Crop c ON d.Crop_ID = c.Crop_ID
        WHERE YEAR(d.Delivery_Date) = %s AND d.Grower_ID=%s;
    """, (dashboard_year, current_user.grower_id))
    delivery_totals = cur.fetchone() or {}

    cur.execute("""
        SELECT COUNT(*) AS n FROM Harvest h
        JOIN Field f ON f.Field_ID=h.Field_ID JOIN Department d ON d.Dpt_ID=f.Dpt_ID
        WHERE d.Grower_ID=%s AND h.Harvest_Date=%s
    """, (current_user.grower_id, date.today()))
    today_loads = int((cur.fetchone() or {}).get("n") or 0)

    cur.execute("""SELECT COUNT(*) AS n FROM grower_memberships
        WHERE Grower_ID=%s AND status='pending'""", (current_user.grower_id,))
    pending_users = int((cur.fetchone() or {}).get("n") or 0)

    cur.execute("""
        SELECT COUNT(*) AS n FROM Harvest h
        JOIN Field f ON f.Field_ID=h.Field_ID JOIN Department d ON d.Dpt_ID=f.Dpt_ID
        WHERE d.Grower_ID=%s AND f.Crop_Year=%s
          AND (h.Gross_Weight IS NULL OR h.MC IS NULL OR h.StorLoc_ID IS NULL)
    """, (current_user.grower_id, dashboard_year))
    incomplete_loads = int((cur.fetchone() or {}).get("n") or 0)

    cur.close()
    conn.close()

    _, inventory_summary, _ = build_inventory_snapshot(crop_year=str(dashboard_year))
    for crop in ("Corn", "Soybeans", "High Moisture Corn"):
        inventory_summary.setdefault(crop, {"Harvest": 0.0, "Delivered": 0.0, "Inventory": 0.0})
    month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly_bushels = [0.0] * 12
    for row in monthly_rows:
        month_index = int(row["delivery_month"]) - 1
        if 0 <= month_index < 12:
            monthly_bushels[month_index] = round(_to_float(row.get("bushels")), 1)

    dashboard_data = {
        "year": dashboard_year,
        "total_bushels": _to_float(harvest_totals.get("total_bushels")),
        "load_count": int(harvest_totals.get("load_count") or 0),
        "active_growers": int(grower_totals.get("active_growers") or 0),
        "inventory_by_crop": inventory_summary,
        "unassigned_deliveries": count_unassigned_deliveries(),
        "delivered_bushels": _to_float(delivery_totals.get("delivered_bushels")),
        "delivery_count": int(delivery_totals.get("delivery_count") or 0),
        "user_count": int(user_totals.get("user_count") or 0),
        "admin_count": int(user_totals.get("admin_count") or 0),
        "today_loads": today_loads,
        "pending_users": pending_users,
        "incomplete_loads": incomplete_loads,
        "monthly_delivery_labels": month_labels,
        "monthly_delivery_bushels": monthly_bushels,
        "inventory_labels": list(inventory_summary),
        "inventory_bushels": [round(item["Inventory"], 1) for item in inventory_summary.values()],
    }

    return render_template("index.html", app_name="GMS", dashboard_data=dashboard_data)





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
    cur.execute("SELECT Grower_ID, Grower_Name FROM Grower WHERE Grower_ID=%s", (current_user.grower_id,))
    growers = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("growers.html", growers=growers)


@app.route("/growers/new", methods=["GET", "POST"])
@admin_required
def new_grower():
    """Form to add a new grower."""
    abort(403)
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
            flash("Grower created successfully.", "success")
            return redirect(url_for("list_growers"))
        else:
            # No name entered; redisplay form with error
            return render_template("grower_form.html", error="Grower name is required")

    # GET: show empty form
    return render_template("grower_form.html", error=None)


@app.route("/growers/<int:grower_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_grower(grower_id):
    if grower_id != int(current_user.grower_id):
        abort(404)
    conn = get_conn(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT Grower_ID, Grower_Name FROM Grower WHERE Grower_ID=%s", (grower_id,))
    grower = cur.fetchone()
    if not grower: abort(404)
    error = None
    if request.method == "POST":
        name = request.form.get("grower_name", "").strip()
        if name:
            cur.execute("UPDATE Grower SET Grower_Name=%s WHERE Grower_ID=%s", (name, grower_id)); conn.commit()
            cur.close(); conn.close(); flash("Grower updated successfully.", "success"); return redirect(url_for("list_growers"))
        error = "Grower name is required."
    cur.close(); conn.close()
    return render_template("grower_form.html", grower=grower, error=error)



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
        WHERE d.Grower_ID=%s ORDER BY d.Dpt_Name;
    """, (current_user.grower_id,))
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
    cur.execute("SELECT Grower_ID, Grower_Name FROM Grower WHERE Grower_ID=%s", (current_user.grower_id,))
    growers = cur.fetchall()
    cur.close()

    if request.method == "POST":
        dpt_name = request.form.get("dpt_name", "").strip()
        contact = request.form.get("contact", "").strip()
        manager = request.form.get("manager", "").strip()
        grower_id = current_user.grower_id

        if dpt_name and contact and manager and grower_id:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO Department (Dpt_Name, Contact, Manager, Grower_ID)
                VALUES (%s, %s, %s, %s);
            """, (dpt_name, contact, manager, grower_id))
            conn.commit()
            cur.close()
            conn.close()
            flash("Department created successfully.", "success")
            return redirect(url_for("list_departments"))

        return render_template(
            "department_form.html",
            growers=growers,
            error="All fields are required."
        )

    conn.close()
    return render_template("department_form.html", growers=growers, error=None)


@app.route("/departments/<int:dpt_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_department(dpt_id):
    conn = get_conn(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM Department WHERE Dpt_ID=%s AND Grower_ID=%s", (dpt_id, current_user.grower_id))
    department = cur.fetchone()
    if not department: abort(404)
    if request.method == "POST":
        name=request.form.get("dpt_name","").strip(); contact=request.form.get("contact","").strip(); manager=request.form.get("manager","").strip()
        if name and contact and manager:
            cur.execute("UPDATE Department SET Dpt_Name=%s,Contact=%s,Manager=%s WHERE Dpt_ID=%s AND Grower_ID=%s", (name,contact,manager,dpt_id,current_user.grower_id)); conn.commit()
            cur.close(); conn.close(); flash("Department updated successfully.", "success"); return redirect(url_for("list_departments"))
        error="All fields are required."
    else: error=None
    cur.execute("SELECT Grower_ID,Grower_Name FROM Grower WHERE Grower_ID=%s", (current_user.grower_id,)); growers=cur.fetchall()
    cur.close(); conn.close(); return render_template("department_form.html",department=department,growers=growers,error=error)



# ----------------- Field: list + create ----------------- #

@app.route("/fields")
@admin_required
def list_fields():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT f.Field_ID, f.Field_Name, f.Acres, f.Silage_Bu_Per_Acre, f.Crop_Year, f.Irr_Type, f.Hybrid_Variety, f.Note,
               d.Dpt_Name
        FROM Field f
        JOIN Department d ON f.Dpt_ID = d.Dpt_ID
        WHERE d.Grower_ID=%s ORDER BY f.Field_Name;
    """, (current_user.grower_id,))
    fields = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("fields.html", fields=fields)

@app.route("/fields/new", methods=["GET", "POST"])
@admin_required
def new_field():
    conn = get_conn()

    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT Dpt_ID, Dpt_Name FROM Department WHERE Grower_ID=%s ORDER BY Dpt_Name;", (current_user.grower_id,))
    departments = cur.fetchall()
    cur.execute("""
        SELECT f.Field_ID, f.Field_Name, f.Acres, f.Crop_Year, f.Irr_Type,
               f.Hybrid_Variety, f.Dpt_ID, d.Dpt_Name
        FROM Field f
        JOIN Department d ON f.Dpt_ID=d.Dpt_ID
        WHERE d.Grower_ID=%s AND LOWER(f.Field_Name) NOT LIKE %s
        ORDER BY f.Crop_Year DESC, f.Field_Name
    """, (current_user.grower_id, "%silage%"))
    base_fields = cur.fetchall()
    base_field_years = sorted({field["Crop_Year"] for field in base_fields}, reverse=True)
    cur.close()

    if request.method == "POST":
        field_name = request.form.get("field_name", "").strip()
        acres = request.form.get("acres", "").strip()
        crop_year = request.form.get("crop_year", "").strip()
        irr_type = request.form.get("irr_type", "").strip()
        hybrid = request.form.get("hybrid_variety", "").strip()
        note = request.form.get("note", "").strip()
        dpt_id = request.form.get("dpt_id", "").strip()
        base_field_id = request.form.get("base_field_id", "").strip()
        silage_crop_year = request.form.get("silage_crop_year", "").strip()
        silage_bu_per_acre = request.form.get("silage_bu_per_acre", "").strip()

        if base_field_id:
            acres = request.form.get("silage_acres", "").strip()
            base_cur = conn.cursor(dictionary=True)
            base_cur.execute("""
                SELECT f.Field_Name, f.Crop_Year, f.Irr_Type, f.Hybrid_Variety, f.Dpt_ID
                FROM Field f JOIN Department d ON f.Dpt_ID=d.Dpt_ID
                WHERE f.Field_ID=%s AND d.Grower_ID=%s
                  AND LOWER(f.Field_Name) NOT LIKE %s
            """, (base_field_id, current_user.grower_id, "%silage%"))
            base_field = base_cur.fetchone()
            base_cur.close()
            if not base_field:
                conn.close()
                abort(400)
            if not silage_crop_year or str(base_field["Crop_Year"]) != silage_crop_year:
                conn.close()
                return render_template(
                    "field_form.html", departments=departments, base_fields=base_fields,
                    base_field_years=base_field_years,
                    error="Select a grain field from the chosen crop year."
                )
            field_name = f"{base_field['Field_Name']}-silage"
            crop_year = str(base_field["Crop_Year"])
            irr_type = base_field.get("Irr_Type") or ""
            hybrid = base_field.get("Hybrid_Variety") or ""
            dpt_id = str(base_field["Dpt_ID"])

        if field_name and crop_year and dpt_id and (not base_field_id or (acres and silage_bu_per_acre)):
            check = conn.cursor()
            check.execute("SELECT 1 FROM Department WHERE Dpt_ID=%s AND Grower_ID=%s", (dpt_id, current_user.grower_id))
            allowed_department = check.fetchone()
            check.close()
            if not allowed_department:
                conn.close()
                abort(400)
            duplicate_cur = conn.cursor()
            duplicate_cur.execute(
                "SELECT 1 FROM Field WHERE Field_Name=%s AND Crop_Year=%s AND Dpt_ID=%s LIMIT 1",
                (field_name, crop_year, dpt_id)
            )
            duplicate = duplicate_cur.fetchone()
            duplicate_cur.close()
            if duplicate:
                conn.close()
                return render_template(
                    "field_form.html", departments=departments, base_fields=base_fields,
                    base_field_years=base_field_years,
                    error=f"{field_name} already exists for crop year {crop_year}."
                )
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO Field (Field_Name, Acres, Silage_Bu_Per_Acre, Crop_Year, Irr_Type, Hybrid_Variety, Note, Dpt_ID)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """, (
                field_name,
                float(acres) if acres else None,
                float(silage_bu_per_acre) if silage_bu_per_acre else None,
                int(crop_year),
                irr_type if irr_type else None,
                hybrid if hybrid else None,
                note if note else None,
                int(dpt_id)
            ))
            conn.commit()
            cur.close()
            conn.close()
            flash("Field created successfully.", "success")
            return redirect(url_for("list_fields"))

        conn.close()
        error = "Silage acres and Silage Bu/ac are required." if base_field_id else "Field Name, Crop Year, and Department are required."
        return render_template("field_form.html", departments=departments, base_fields=base_fields, base_field_years=base_field_years, error=error)

    conn.close()
    return render_template("field_form.html", departments=departments, base_fields=base_fields, base_field_years=base_field_years, error=None)


@app.route("/fields/<int:field_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_field(field_id):
    conn=get_conn(); cur=conn.cursor(dictionary=True)
    cur.execute("""SELECT f.* FROM Field f JOIN Department d ON d.Dpt_ID=f.Dpt_ID WHERE f.Field_ID=%s AND d.Grower_ID=%s""",(field_id,current_user.grower_id)); field=cur.fetchone()
    if not field: abort(404)
    cur.execute("SELECT Dpt_ID,Dpt_Name FROM Department WHERE Grower_ID=%s ORDER BY Dpt_Name",(current_user.grower_id,)); departments=cur.fetchall()
    error=None
    if request.method=="POST":
        name=request.form.get("field_name","").strip(); year=request.form.get("crop_year","").strip(); dpt=request.form.get("dpt_id","").strip()
        cur.execute("SELECT 1 FROM Department WHERE Dpt_ID=%s AND Grower_ID=%s",(dpt,current_user.grower_id)); allowed=cur.fetchone()
        if name and year and dpt and allowed:
            acres=request.form.get("acres","").strip(); silage_bu_per_acre=request.form.get("silage_bu_per_acre","").strip(); irr=request.form.get("irr_type","").strip(); hybrid=request.form.get("hybrid_variety","").strip(); note=request.form.get("note","").strip()
            cur.execute("""UPDATE Field SET Field_Name=%s,Acres=%s,Silage_Bu_Per_Acre=%s,Crop_Year=%s,Irr_Type=%s,Hybrid_Variety=%s,Note=%s,Dpt_ID=%s WHERE Field_ID=%s""",(name,float(acres) if acres else None,float(silage_bu_per_acre) if silage_bu_per_acre else None,int(year),irr or None,hybrid or None,note or None,int(dpt),field_id)); conn.commit()
            cur.close(); conn.close(); flash("Field updated successfully.", "success"); return redirect(url_for("list_fields"))
        error="Field Name, Crop Year, and a valid Department are required."
    cur.close(); conn.close(); return render_template("field_form.html",field=field,departments=departments,error=error)


# ----------------- Cart: list + create ----------------- #

@app.route("/carts")
@admin_required
def list_carts():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT Cart_ID, Cart_Code, Cart_Name, Load_Cell FROM Cart WHERE Grower_ID=%s ORDER BY Cart_Name;", (current_user.grower_id,))
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
        load_cell = request.form.get("load_cell", "").strip()
        if len(load_cell) > 100:
            return render_template("cart_form.html", error="Load Cell must be at most 100 characters.")

        if cart_code and cart_name:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO Cart (Cart_Code, Cart_Name, Load_Cell, Grower_ID) VALUES (%s, %s, %s, %s);",
                (cart_code, cart_name, load_cell or None, current_user.grower_id)
            )
            conn.commit()
            cur.close()
            conn.close()
            flash("Cart created successfully.", "success")
            return redirect(url_for("list_carts"))

        return render_template("cart_form.html", error="Cart Code and Cart Name are required.")

    return render_template("cart_form.html", error=None)


@app.route("/carts/<int:cart_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_cart(cart_id):
    conn=get_conn(); cur=conn.cursor(dictionary=True); cur.execute("SELECT * FROM Cart WHERE Cart_ID=%s AND Grower_ID=%s",(cart_id,current_user.grower_id)); cart=cur.fetchone()
    if not cart: abort(404)
    error=None
    if request.method=="POST":
        code=request.form.get("cart_code","").strip(); name=request.form.get("cart_name","").strip()
        load_cell=request.form.get("load_cell", "").strip()
        if not code or not name:
            error="Cart Code and Cart Name are required."
        elif len(load_cell) > 100:
            error="Load Cell must be at most 100 characters."
        else:
            cur.execute("UPDATE Cart SET Cart_Code=%s,Cart_Name=%s,Load_Cell=%s WHERE Cart_ID=%s AND Grower_ID=%s",(code,name,load_cell or None,cart_id,current_user.grower_id)); conn.commit(); cur.close(); conn.close(); flash("Cart updated successfully.", "success"); return redirect(url_for("list_carts"))
    cur.close(); conn.close(); return render_template("cart_form.html",cart=cart,error=error)



# ----------------- Vehicles ----------------- #

@app.get("/vehicles")
@admin_required
def list_vehicles():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute("SELECT * FROM Vehicles WHERE Grower_ID=%s ORDER BY Vehicle_Code", (current_user.grower_id,))
        vehicles = cur.fetchall()
    finally:
        cur.close()
        conn.close()
    return render_template("vehicles.html", vehicles=vehicles)


@app.route("/vehicles/new", methods=["GET", "POST"])
@app.route("/vehicles/<int:vehicle_id>/edit", methods=["GET", "POST"])
@admin_required
def vehicle_form(vehicle_id=None):
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    vehicle = {}
    error = None
    try:
        if vehicle_id is not None:
            cur.execute("SELECT * FROM Vehicles WHERE Vehicle_ID=%s AND Grower_ID=%s",
                        (vehicle_id, current_user.grower_id))
            vehicle = cur.fetchone()
            if not vehicle:
                abort(404)
        if request.method == "POST":
            vehicle = {key: request.form.get(key, "").strip()
                       for key in ("Vehicle_Code", "Vehicle_Name")}
            if not vehicle["Vehicle_Code"] or not vehicle["Vehicle_Name"]:
                error = "Vehicle Code and Vehicle Name are required."
            elif any(len(vehicle[key]) > limit for key, limit in
                     (("Vehicle_Code", 120), ("Vehicle_Name", 120))):
                error = "Vehicle code/name must be at most 120 characters."
            else:
                values = (vehicle["Vehicle_Code"], vehicle["Vehicle_Name"])
                try:
                    if vehicle_id is None:
                        cur.execute("""INSERT INTO Vehicles (Vehicle_Code, Vehicle_Name, Grower_ID)
                            VALUES (%s,%s,%s)""", values + (current_user.grower_id,))
                    else:
                        cur.execute("""UPDATE Vehicles SET Vehicle_Code=%s, Vehicle_Name=%s
                            WHERE Vehicle_ID=%s AND Grower_ID=%s""", values + (vehicle_id, current_user.grower_id))
                    conn.commit()
                    flash("Vehicle saved successfully.", "success")
                    return redirect(url_for("list_vehicles"))
                except IntegrityError as exc:
                    conn.rollback()
                    if exc.errno != 1062:
                        raise
                    error = "This Vehicle Code already exists. Choose a different code."
    finally:
        cur.close()
        conn.close()
    return render_template("vehicle_form.html", vehicle=vehicle, vehicle_id=vehicle_id, error=error)


@app.post("/vehicles/<int:vehicle_id>/delete")
@admin_required
def delete_vehicle(vehicle_id):
    return _delete_setup_record("DELETE FROM Vehicles WHERE Vehicle_ID=%s AND Grower_ID=%s",
                                (vehicle_id, current_user.grower_id), "Vehicle", "list_vehicles")


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
            flash("Crop created successfully.", "success")
            return redirect(url_for("list_crops"))

        return render_template("crop_form.html", error="All fields are required.")

    return render_template("crop_form.html", error=None)


@app.route("/crops/<int:crop_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_crop(crop_id):
    conn=get_conn(); cur=conn.cursor(dictionary=True); cur.execute("SELECT * FROM Crop WHERE Crop_ID=%s",(crop_id,)); crop=cur.fetchone()
    if not crop: abort(404)
    error=None
    if request.method=="POST":
        code=request.form.get("crop_code","").strip(); name=request.form.get("crop_name","").strip(); weight=request.form.get("weight_per_bushel","").strip(); mc=request.form.get("base_mc","").strip()
        if code and name and weight and mc:
            cur.execute("UPDATE Crop SET Crop_Code=%s,Crop_Name=%s,Weight_PerBushel=%s,Base_MC=%s WHERE Crop_ID=%s",(code,name,float(weight),float(mc),crop_id)); conn.commit(); cur.close(); conn.close(); flash("Crop updated successfully.", "success"); return redirect(url_for("list_crops"))
        error="All fields are required."
    cur.close(); conn.close(); return render_template("crop_form.html",crop=crop,error=error)


# ----------------- Storage Location: list + create ----------------- #

def storage_sort_key(code):
    """Sort numeric portions as numbers, so Bin2 precedes Bin10."""
    return tuple((1, int(part)) if part.isdigit() else (0, part)
                 for part in re.split(r"(\d+)", (code or "").strip().casefold()))


@app.route("/storage")
@admin_required
def list_storage():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT StorLoc_ID, Bin_Code, Bin_Name, Bin_Capacity, Diameter, Install_Date,
               Legal_Desc, Lattitude, Lontitude, Manufacture
        FROM Storage_Location WHERE Grower_ID=%s ORDER BY Bin_Name;
    """, (current_user.grower_id,))
    rows = sorted(cur.fetchall(), key=lambda row: storage_sort_key(row.get("Bin_Code") or row.get("Bin_Name")))
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
                   Legal_Desc, Lattitude, Lontitude, Manufacture, Grower_ID)
                VALUES
                  (%s, %s, %s, %s, %s,
                   %s, %s, %s, %s, %s);
            """, (
                bin_code,
                bin_name,
                float(bin_capacity),
                float(diameter) if diameter else None,
                install_date if install_date else None,
                legal_desc if legal_desc else None,
                float(lattitude) if lattitude else None,
                float(lontitude) if lontitude else None,
                manufacture if manufacture else None,
                current_user.grower_id
            ))
            conn.commit()
            cur.close()
            conn.close()
            flash("Storage location created successfully.", "success")
            return redirect(url_for("list_storage"))

        return render_template("storage_form.html", error="Bin Code, Bin Name, and Bin Capacity are required.")

    return render_template("storage_form.html", error=None)


@app.route("/storage/<int:storage_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_storage(storage_id):
    conn=get_conn(); cur=conn.cursor(dictionary=True); cur.execute("SELECT * FROM Storage_Location WHERE StorLoc_ID=%s AND Grower_ID=%s",(storage_id,current_user.grower_id)); storage_item=cur.fetchone()
    if not storage_item: abort(404)
    error=None
    if request.method=="POST":
        code=request.form.get("bin_code","").strip(); name=request.form.get("bin_name","").strip(); capacity=request.form.get("bin_capacity","").strip()
        if code and name and capacity:
            diameter=request.form.get("diameter","").strip(); installed=request.form.get("install_date","").strip(); legal=request.form.get("legal_desc","").strip(); lat=request.form.get("lattitude","").strip(); lon=request.form.get("lontitude","").strip(); manufacturer=request.form.get("manufacture","").strip()
            cur.execute("""UPDATE Storage_Location SET Bin_Code=%s,Bin_Name=%s,Bin_Capacity=%s,Diameter=%s,Install_Date=%s,Legal_Desc=%s,Lattitude=%s,Lontitude=%s,Manufacture=%s WHERE StorLoc_ID=%s AND Grower_ID=%s""",(code,name,float(capacity),float(diameter) if diameter else None,installed or None,legal or None,float(lat) if lat else None,float(lon) if lon else None,manufacturer or None,storage_id,current_user.grower_id)); conn.commit(); cur.close(); conn.close(); flash("Storage location updated successfully.", "success"); return redirect(url_for("list_storage"))
        error="Bin Code, Bin Name, and Bin Capacity are required."
    cur.close(); conn.close(); return render_template("storage_form.html",storage_item=storage_item,error=error)


# ----------------- Delivery Location: list + create ----------------- #

@app.route("/delivery-locations")
@admin_required
def list_delivery_locations():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT DelLoc_ID, DelLoc_code, Location
        FROM Delivery_Location WHERE Grower_ID=%s ORDER BY DelLoc_code;
    """, (current_user.grower_id,))
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
                INSERT INTO Delivery_Location (DelLoc_code, Location, Grower_ID)
                VALUES (%s, %s, %s);
            """, (code, location if location else None, current_user.grower_id))
            conn.commit()
            cur.close()
            conn.close()
            flash("Delivery location created successfully.", "success")
            return redirect(url_for("list_delivery_locations"))

        return render_template("delivery_location_form.html", error="Delivery Location code is required.")

    return render_template("delivery_location_form.html", error=None)


@app.route("/delivery-locations/<int:location_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_delivery_location(location_id):
    conn=get_conn(); cur=conn.cursor(dictionary=True); cur.execute("SELECT * FROM Delivery_Location WHERE DelLoc_ID=%s AND Grower_ID=%s",(location_id,current_user.grower_id)); location_item=cur.fetchone()
    if not location_item: abort(404)
    error=None
    if request.method=="POST":
        code=request.form.get("delloc_code","").strip(); location=request.form.get("location","").strip()
        if code:
            cur.execute("UPDATE Delivery_Location SET DelLoc_code=%s,Location=%s WHERE DelLoc_ID=%s AND Grower_ID=%s",(code,location or None,location_id,current_user.grower_id)); conn.commit(); cur.close(); conn.close(); flash("Delivery location updated successfully.", "success"); return redirect(url_for("list_delivery_locations"))
        error="Delivery Location code is required."
    cur.close(); conn.close(); return render_template("delivery_location_form.html",location_item=location_item,error=error)



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
        WHERE mp.Grower_ID=%s ORDER BY mp.Year DESC, mp.Month DESC, mp.ID DESC;
    """, (current_user.grower_id,))
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
                INSERT INTO MarketPriceMonthly (Crop, Year, Month, Day, Market_Price, Grower_ID)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (int(crop_id), int(year), int(month), day, float(price), current_user.grower_id))
            conn.commit()
            cur.close()
            conn.close()
            flash("Market price created successfully.", "success")
            return redirect(url_for("list_market_prices"))

        conn.close()
        return render_template("market_price_form.html", crops=crops, error="All fields are required.")

    conn.close()
    return render_template("market_price_form.html", crops=crops, error=None)


@app.route("/market-prices/<int:price_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_market_price(price_id):
    conn=get_conn(); cur=conn.cursor(dictionary=True); cur.execute("SELECT * FROM MarketPriceMonthly WHERE ID=%s AND Grower_ID=%s",(price_id,current_user.grower_id)); price_item=cur.fetchone()
    if not price_item: abort(404)
    cur.execute("SELECT Crop_ID,Crop_Name FROM Crop ORDER BY Crop_Name"); crops=cur.fetchall(); error=None
    if request.method=="POST":
        crop=request.form.get("crop_id","").strip(); year=request.form.get("year","").strip(); month=request.form.get("month","").strip(); day=request.form.get("day","").strip(); price=request.form.get("market_price","").strip()
        if crop and year and month and day and price:
            cur.execute("UPDATE MarketPriceMonthly SET Crop=%s,Year=%s,Month=%s,Day=%s,Market_Price=%s WHERE ID=%s AND Grower_ID=%s",(int(crop),int(year),int(month),day,float(price),price_id,current_user.grower_id)); conn.commit(); cur.close(); conn.close(); flash("Market price updated successfully.", "success"); return redirect(url_for("list_market_prices"))
        error="All fields are required."
    cur.close(); conn.close(); return render_template("market_price_form.html",price_item=price_item,crops=crops,error=error)


# ----------------- Farm Setup: safe deletes ----------------- #

def _delete_setup_record(delete_sql, params, label, redirect_endpoint):
    """Delete one setup record, preserving records referenced by operational data."""
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute(delete_sql, params)
        if cur.rowcount == 0:
            conn.rollback()
            abort(404)
        conn.commit()
        flash(f"{label} deleted successfully.", "success")
    except IntegrityError:
        conn.rollback()
        flash(
            f"{label} cannot be deleted because it is used by other records. "
            "Remove or reassign those records first.",
            "danger"
        )
    finally:
        cur.close()
        conn.close()
    return redirect(url_for(redirect_endpoint))


@app.post("/departments/<int:dpt_id>/delete")
@admin_required
def delete_department(dpt_id):
    return _delete_setup_record(
        "DELETE FROM Department WHERE Dpt_ID=%s AND Grower_ID=%s",
        (dpt_id, current_user.grower_id), "Department", "list_departments"
    )


@app.post("/fields/<int:field_id>/delete")
@admin_required
def delete_field(field_id):
    return _delete_setup_record(
        """DELETE f FROM Field f JOIN Department d ON d.Dpt_ID=f.Dpt_ID
           WHERE f.Field_ID=%s AND d.Grower_ID=%s""",
        (field_id, current_user.grower_id), "Field", "list_fields"
    )


@app.post("/carts/<int:cart_id>/delete")
@admin_required
def delete_cart(cart_id):
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(
            """SELECT c.Cart_ID, COUNT(h.Harvest_ID) AS harvest_uses
               FROM Cart c
               LEFT JOIN Harvest h ON h.Cart_ID=c.Cart_ID
               WHERE c.Cart_ID=%s AND c.Grower_ID=%s
               GROUP BY c.Cart_ID""",
            (cart_id, current_user.grower_id)
        )
        cart = cur.fetchone()
    finally:
        cur.close()
        conn.close()

    if not cart:
        abort(404)
    if cart["harvest_uses"]:
        flash(
            f"Cart cannot be deleted because it is used by "
            f"{cart['harvest_uses']} harvest record(s). Reassign those records first.",
            "danger"
        )
        return redirect(url_for("list_carts"))

    return _delete_setup_record(
        "DELETE FROM Cart WHERE Cart_ID=%s AND Grower_ID=%s",
        (cart_id, current_user.grower_id), "Cart", "list_carts"
    )


@app.post("/crops/<int:crop_id>/delete")
@admin_required
def delete_crop(crop_id):
    return _delete_setup_record(
        "DELETE FROM Crop WHERE Crop_ID=%s",
        (crop_id,), "Crop", "list_crops"
    )


@app.post("/storage/<int:storage_id>/delete")
@admin_required
def delete_storage(storage_id):
    return _delete_setup_record(
        "DELETE FROM Storage_Location WHERE StorLoc_ID=%s AND Grower_ID=%s",
        (storage_id, current_user.grower_id), "Storage bin", "list_storage"
    )


@app.post("/delivery-locations/<int:location_id>/delete")
@admin_required
def delete_delivery_location(location_id):
    return _delete_setup_record(
        "DELETE FROM Delivery_Location WHERE DelLoc_ID=%s AND Grower_ID=%s",
        (location_id, current_user.grower_id), "Delivery location", "list_delivery_locations"
    )


@app.post("/market-prices/<int:price_id>/delete")
@admin_required
def delete_market_price(price_id):
    return _delete_setup_record(
        "DELETE FROM MarketPriceMonthly WHERE ID=%s AND Grower_ID=%s",
        (price_id, current_user.grower_id), "Market price", "list_market_prices"
    )





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


def harvest_extra_filters():
    """Validate filters shared by the loads and summary pages."""
    filters = {key: request.args.get(key, "").strip()
               for key in ("truck_id", "crop_id", "date_from", "date_to")}
    try:
        for key in ("date_from", "date_to"):
            if filters[key]:
                filters[key] = date.fromisoformat(filters[key]).isoformat()
        if filters["date_from"] and filters["date_to"] and filters["date_from"] > filters["date_to"]:
            raise ValueError
    except ValueError:
        abort(400, description="Choose valid dates with From date on or before To date.")
    return filters


def append_harvest_filters(where, params, filters):
    for key, expression in (("truck_id", "h.Truck_ID = %s"),
                            ("crop_id", "h.Crop_ID = %s"),
                            ("date_from", "h.Harvest_Date >= %s"),
                            ("date_to", "h.Harvest_Date <= %s")):
        if filters[key]:
            where.append(expression)
            params.append(filters[key])


def harvest_cart_label(load, carts):
    """Prefer a unique load-cell match, then the historical/manual cart link."""
    cell = str(load.get("Load_Cell") or "").strip().lower()
    if cell not in ("", "null", "none"):
        matches = [cart for cart in carts
                   if str(cart.get("Load_Cell") or "").strip().lower() == cell]
        if len(matches) > 1:
            return "Ambiguous cart"
        if matches:
            return matches[0].get("Cart_Name") or matches[0].get("Cart_Code") or "Unassigned"
    linked = next((cart for cart in carts if cart["Cart_ID"] == load.get("Cart_ID")), None)
    return (linked.get("Cart_Name") or linked.get("Cart_Code") or "Unassigned") if linked else "Unassigned"


@app.route("/harvest-query", methods=["GET", "POST"])
@login_required
def harvest_query():
    if request.method == "POST" and not current_user.can_edit:
        abort(403)
    extra_filters = harvest_extra_filters()
    conn = get_conn()
    cur = conn.cursor(dictionary=True)

    # ---------------- Filters ----------------
    selected_field_id = request.args.get("field_id", "").strip()
    selected_field = request.args.get("field_name", "").strip()
    selected_storage = request.args.get("storloc_id", "").strip()
    selected_year = request.args.get("crop_year", "").strip()
    selected_edit_id = request.args.get("edit_id", "").strip()
    if request.method == "POST":
        selected_edit_id = request.form.get("harvest_id", "").strip()
    if selected_edit_id and not selected_edit_id.isdigit():
        abort(400, description="Choose a valid harvest load.")
    needs_attention = request.args.get("needs_attention", "") == "1"

    # ---------------- Dropdown data ----------------
    field_filter_where = ["d.Grower_ID = %s"]
    field_filter_params = [current_user.grower_id]

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
        JOIN Department d ON d.Dpt_ID=f.Dpt_ID
        {field_filter_sql}
        ORDER BY f.Field_Name, f.Crop_Year DESC, f.Field_ID;
    """.format(field_filter_sql=field_filter_sql), tuple(field_filter_params))
    fields = cur.fetchall()

    if selected_field_id and selected_year:
        selected_field_matches_year = any(str(f["Field_ID"]) == selected_field_id for f in fields)
        if not selected_field_matches_year:
            selected_field_id = ""

    cur.execute("SELECT StorLoc_ID, Bin_Code, Bin_Name FROM Storage_Location WHERE Grower_ID=%s ORDER BY Bin_Code;", (current_user.grower_id,))
    storages = sorted(cur.fetchall(), key=lambda row: storage_sort_key(row.get("Bin_Code") or row.get("Bin_Name")))



    cur.execute("""
    SELECT Field_ID, Field_Name, Crop_Year
    FROM Field f JOIN Department d ON d.Dpt_ID=f.Dpt_ID
    WHERE d.Grower_ID=%s
    ORDER BY Field_Name, Crop_Year DESC;
    """, (current_user.grower_id,))
    entry_fields = cur.fetchall()

    # Distinct years for filter dropdown
    cur.execute("""
        SELECT DISTINCT Crop_Year
        FROM Field f JOIN Department d ON d.Dpt_ID=f.Dpt_ID
        WHERE Crop_Year IS NOT NULL AND d.Grower_ID=%s
        ORDER BY Crop_Year DESC;
    """, (current_user.grower_id,))
    years = cur.fetchall()

    cur.execute("SELECT Crop_ID, Crop_Name, Weight_PerBushel, Base_MC FROM Crop ORDER BY Crop_Name;")
    crops = cur.fetchall()

    cur.execute("SELECT Cart_ID, Cart_Code, Cart_Name, Load_Cell FROM Cart WHERE Grower_ID=%s ORDER BY Cart_Name;", (current_user.grower_id,))
    carts = cur.fetchall()
    cur.execute("""SELECT DISTINCT h.Truck_ID FROM Harvest h
        JOIN Field f ON f.Field_ID=h.Field_ID
        JOIN Department d ON d.Dpt_ID=f.Dpt_ID
        WHERE d.Grower_ID=%s AND h.Truck_ID IS NOT NULL AND TRIM(h.Truck_ID) <> ''
        ORDER BY h.Truck_ID""", (current_user.grower_id,))
    trucks = cur.fetchall()

    error = None
    edit_load = None

    if selected_edit_id:
        cur.execute("""
            SELECT
              h.Harvest_ID,
              h.Cart_ID,
              h.Field_ID,
              h.Crop_ID,
              h.StorLoc_ID,
              h.Load_Num,
              h.Harvest_Date,
              h.MC,
              h.Gross_Weight,
              h.Tare_Weight,
              h.Note
            FROM Harvest h JOIN Field f ON f.Field_ID=h.Field_ID JOIN Department d ON d.Dpt_ID=f.Dpt_ID
            WHERE h.Harvest_ID = %s AND d.Grower_ID=%s;
        """, (selected_edit_id, current_user.grower_id))
        edit_load = cur.fetchone()
        if not edit_load:
            cur.close()
            conn.close()
            abort(404)


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

        try:
            for value in (field_id, storloc_id, crop_id, cart_id):
                if value and int(value) <= 0:
                    raise ValueError
            if harvest_date:
                date.fromisoformat(harvest_date)
            for value in (mc, gross, tare):
                if value and not math.isfinite(float(value)):
                    raise ValueError
        except ValueError:
            error = "Choose valid field, storage, crop, and cart values, a valid date, and finite numeric weights and moisture."

        duplicate_load = False
        if not error and load_num and harvest_date and field_id and cart_id:
            cur.execute("""
                SELECT h.Harvest_ID FROM Harvest h
                JOIN Field f ON f.Field_ID=h.Field_ID
                JOIN Department d ON d.Dpt_ID=f.Dpt_ID
                WHERE d.Grower_ID=%s AND h.Load_Num=%s AND h.Harvest_Date=%s
                  AND h.Field_ID=%s AND h.Cart_ID=%s AND h.Harvest_ID<>%s
                LIMIT 1
            """, (current_user.grower_id, load_num, harvest_date, field_id, cart_id, int(harvest_id or 0)))
            duplicate_load = cur.fetchone() is not None

        if error:
            pass
        elif not (load_num and harvest_date and field_id and crop_id and cart_id):
            error = "Load, Date, Field, Crop, and Cart are required."
        elif not harvest_id and not storloc_id:
            error = "Storage is required for new loads."
        elif duplicate_load:
            error = "A load with this number, date, field, and cart already exists. Review the existing load instead of saving a duplicate."
        else:
            cur.execute("""SELECT f.Dpt_ID FROM Field f JOIN Department d ON d.Dpt_ID=f.Dpt_ID
                WHERE f.Field_ID=%s AND d.Grower_ID=%s""", (field_id, current_user.grower_id))
            row = cur.fetchone()
            if not row:
                error = "Selected Field not found."
            else:
                dpt_id = row["Dpt_ID"]

                cur.execute("SELECT Cart_ID FROM Cart WHERE Cart_ID=%s AND Grower_ID=%s", (cart_id, current_user.grower_id))
                if not cur.fetchone():
                    abort(400)
                if storloc_id:
                    cur.execute("SELECT StorLoc_ID FROM Storage_Location WHERE StorLoc_ID=%s AND Grower_ID=%s", (storloc_id, current_user.grower_id))
                    if not cur.fetchone():
                        abort(400)

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
                        WHERE Harvest_ID = %s AND Field_ID IN (
                          SELECT f.Field_ID FROM Field f JOIN Department d ON d.Dpt_ID=f.Dpt_ID WHERE d.Grower_ID=%s
                        );
                    """, (
                        int(cart_id), int(field_id), int(crop_id), int(dpt_id), storloc_val,
                        load_num, harvest_date, mc_val, gross_val, tare_val, bushels_val,
                        (note if note else None), int(harvest_id), current_user.grower_id
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
                cur.close()
                conn.close()

                session["harvest_entry_defaults"] = {
                    "field_id": field_id,
                    "storloc_id": storloc_id,
                    "crop_id": crop_id,
                    "cart_id": cart_id,
                }
                flash(f"Harvest load {load_num} {'updated' if harvest_id else 'saved'} successfully.", "success")

                return redirect(url_for(
                    "harvest_query",
                    field_id=selected_field_id,
                    field_name=selected_field,
                    storloc_id=selected_storage,
                    crop_year=selected_year,
                    **extra_filters,
                    needs_attention="1" if needs_attention else ""
                ))

    # ---------------- GET: show filtered loads ----------------
    where = ["d.Grower_ID = %s"]
    params = [current_user.grower_id]

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

    if needs_attention:
        where.append("(h.Gross_Weight IS NULL OR h.MC IS NULL OR h.StorLoc_ID IS NULL)")

    append_harvest_filters(where, params, extra_filters)
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
          COALESCE(NULLIF(s.Bin_Code, ''), s.Bin_Name) AS Storage,
          h.Truck_ID,
          h.Load_Cell,
          h.Cart_ID,
          h.Bushels,
          h.Note
        FROM Harvest h
        JOIN Field f ON h.Field_ID = f.Field_ID
        JOIN Department d ON d.Dpt_ID=f.Dpt_ID
        JOIN Crop cr ON h.Crop_ID = cr.Crop_ID
        LEFT JOIN Storage_Location s ON h.StorLoc_ID = s.StorLoc_ID
        {where_sql}
        ORDER BY h.Harvest_Date DESC, h.Load_Num DESC;
    """, tuple(params))

    loads = cur.fetchall()

    entry_defaults = dict(session.get("harvest_entry_defaults", {}))
    if request.method == "POST" and error:
        if edit_load:
            for column, form_key in (("Load_Num", "load_num"), ("Harvest_Date", "harvest_date"),
                                     ("Field_ID", "field_id"), ("StorLoc_ID", "storloc_id"),
                                     ("Crop_ID", "crop_id"), ("Cart_ID", "cart_id"),
                                     ("MC", "mc"), ("Gross_Weight", "gross"),
                                     ("Tare_Weight", "tare"), ("Note", "note")):
                edit_load[column] = request.form.get(form_key, "")
        entry_defaults.update({
            "field_id": request.form.get("field_id", ""),
            "storloc_id": request.form.get("storloc_id", ""),
            "crop_id": request.form.get("crop_id", ""),
            "cart_id": request.form.get("cart_id", ""),
            "load_num": request.form.get("load_num", ""),
            "harvest_date": request.form.get("harvest_date", ""),
        })

    cur.execute("""
        SELECT MAX(CAST(h.Load_Num AS UNSIGNED)) AS max_load
        FROM Harvest h JOIN Field f ON f.Field_ID=h.Field_ID
        JOIN Department d ON d.Dpt_ID=f.Dpt_ID
        WHERE d.Grower_ID=%s AND h.Harvest_Date=%s AND h.Load_Num REGEXP '^[0-9]+$'
    """, (current_user.grower_id, date.today()))
    max_load = (cur.fetchone() or {}).get("max_load")
    next_load_num = str(int(max_load or 0) + 1)

    for row in loads:
        row["Cart_Display"] = harvest_cart_label(row, carts)
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
        trucks=trucks,
        extra_filters=extra_filters,
        loads=loads,
        selected_field=selected_field,
        selected_field_id=selected_field_id,
        selected_storage=selected_storage,
        selected_year=selected_year,
        needs_attention=needs_attention,
        error=error,
        mc_avg=mc_avg,
        lbs_wet=lbs_wet,
        bu_wet=bu_wet,
        dry_bushels=bushels_sum,
        edit_load=edit_load,
        entry_defaults=entry_defaults,
        today=date.today().isoformat(),
        next_load_num=next_load_num
    )




@app.route("/harvest-summary", methods=["GET"])
@login_required
def harvest_summary():
    extra_filters = harvest_extra_filters()
    conn = get_conn()
    cur = conn.cursor(dictionary=True)

    selected_field_id = request.args.get("field_id", "").strip()
    selected_field = request.args.get("field_name", "").strip()
    selected_storage = request.args.get("storloc_id", "").strip()
    selected_year = request.args.get("crop_year", "").strip()

    where = ["d.Grower_ID = %s"]
    params = [current_user.grower_id]

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

    if request.args.get("needs_attention", "") == "1":
        where.append("(h.Gross_Weight IS NULL OR h.MC IS NULL OR h.StorLoc_ID IS NULL)")
    append_harvest_filters(where, params, extra_filters)
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
        JOIN Department d ON d.Dpt_ID=f.Dpt_ID
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
        extra_filters=extra_filters,
        needs_attention=request.args.get("needs_attention", "") == "1",
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

    # Start with the latest crop year that has harvest activity for this grower.
    today = date.today()
    cur.execute("""SELECT MIN(h.Harvest_Date) AS first_date FROM Harvest h
        JOIN Field f ON f.Field_ID=h.Field_ID JOIN Department d ON d.Dpt_ID=f.Dpt_ID
        WHERE d.Grower_ID=%s AND h.Harvest_Date <= %s
        GROUP BY f.Crop_Year
        ORDER BY f.Crop_Year DESC
        LIMIT 1""", (current_user.grower_id, today))
    first_date = (cur.fetchone() or {}).get("first_date")

    # Date controls can override either default independently.
    start = request.args.get("start")
    end = request.args.get("end")

    start_date, end_date = report_date_range(
        start, end, first_date or today, today)

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
        JOIN Field f ON f.Field_ID=h.Field_ID JOIN Department d ON d.Dpt_ID=f.Dpt_ID
        WHERE h.Harvest_Date BETWEEN %s AND %s AND d.Grower_ID=%s
        GROUP BY h.Harvest_Date
        ORDER BY h.Harvest_Date;
    """, (start_date, end_date, current_user.grower_id))

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



def report_date_range(start, end, default_start, default_end=None, days=0):
    """Handle empty date controls and reject invalid/reversed report ranges."""
    try:
        start_date = date.fromisoformat(start) if start else default_start
        end_date = (date.fromisoformat(end) if end else
                    default_end if default_end is not None else start_date + timedelta(days=days))
        if start_date > end_date:
            raise ValueError
    except (ValueError, OverflowError):
        abort(400, description="Choose valid dates with Start on or before End.")
    return start_date, end_date


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
    params_h = [start_date, end_date, current_user.grower_id]
    params_d = [start_date, end_date, current_user.grower_id]

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
        JOIN Field f ON f.Field_ID=h.Field_ID JOIN Department dept ON dept.Dpt_ID=f.Dpt_ID
        WHERE h.Harvest_Date BETWEEN %s AND %s AND dept.Grower_ID=%s
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
        WHERE d.Delivery_Date BETWEEN %s AND %s AND d.Grower_ID=%s
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
          JOIN Field f ON f.Field_ID=h.Field_ID JOIN Department dept ON dept.Dpt_ID=f.Dpt_ID
          WHERE h.Harvest_Date BETWEEN %s AND %s AND dept.Grower_ID=%s
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
          WHERE d.Delivery_Date BETWEEN %s AND %s AND d.Grower_ID=%s
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
          WHERE d.Delivery_Date BETWEEN %s AND %s AND d.Grower_ID=%s
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
          JOIN Field f ON f.Field_ID=h.Field_ID JOIN Department dept ON dept.Dpt_ID=f.Dpt_ID
          WHERE h.Harvest_Date BETWEEN %s AND %s AND dept.Grower_ID=%s
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
            CONVERT(h.Load_Num USING utf8mb4) COLLATE utf8mb4_unicode_ci AS load_key,
            h.Harvest_Date AS harvest_date,
            CONVERT(f.Field_Name USING utf8mb4) COLLATE utf8mb4_unicode_ci AS field_name,
            CONVERT(COALESCE(NULLIF(sl.Bin_Code, ''), sl.Bin_Name) USING utf8mb4) COLLATE utf8mb4_unicode_ci AS harvest_storage,
            CONVERT(c.Crop_Code USING utf8mb4) COLLATE utf8mb4_unicode_ci AS crop_code,
            h.MC AS harvest_mc,
            h.Gross_Weight AS harvest_gross,
            h.Tare_Weight AS harvest_tare,
            {harvest_bu_sql} AS harvest_bushels,
            d.Delivery_Date AS delivery_date,
            CONVERT(dl.DelLoc_code USING utf8mb4) COLLATE utf8mb4_unicode_ci AS delivered_to,
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
          JOIN Department dept ON dept.Dpt_ID=f.Dpt_ID
          JOIN Crop c ON h.Crop_ID = c.Crop_ID
          LEFT JOIN Storage_Location sl ON h.StorLoc_ID = sl.StorLoc_ID
          LEFT JOIN Delivery d ON CAST(d.Ticket_Num AS BINARY) = CAST(h.Load_Num AS BINARY) AND d.Grower_ID=dept.Grower_ID
          LEFT JOIN Delivery_Location dl ON d.DelLoc_ID = dl.DelLoc_ID
          WHERE h.Harvest_Date BETWEEN %s AND %s AND dept.Grower_ID=%s
          {crop_filter_sql_h}
        )
        UNION
        (
          SELECT
            CONVERT(CAST(d.Ticket_Num AS CHAR) USING utf8mb4) COLLATE utf8mb4_unicode_ci AS load_key,
            NULL AS harvest_date,
            NULL AS field_name,
            NULL AS harvest_storage,
            CONVERT(c.Crop_Code USING utf8mb4) COLLATE utf8mb4_unicode_ci AS crop_code,
            NULL AS harvest_mc,
            NULL AS harvest_gross,
            NULL AS harvest_tare,
            NULL AS harvest_bushels,
            d.Delivery_Date AS delivery_date,
            CONVERT(dl.DelLoc_code USING utf8mb4) COLLATE utf8mb4_unicode_ci AS delivered_to,
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
          LEFT JOIN Harvest h ON CAST(h.Load_Num AS BINARY) = CAST(d.Ticket_Num AS BINARY)
          WHERE d.Delivery_Date BETWEEN %s AND %s AND d.Grower_ID=%s
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


INVENTORY_CROP_SQL = """CASE
    WHEN LOWER(TRIM(c.Crop_Name)) IN ('soybean', 'soybeans')
         OR UPPER(TRIM(c.Crop_Code)) IN ('B', 'SB') THEN 'Soybeans'
    WHEN LOWER(TRIM(c.Crop_Name)) IN ('hmc', 'high moisture corn')
         OR UPPER(TRIM(c.Crop_Code)) = 'HMC' THEN 'High Moisture Corn'
    WHEN LOWER(TRIM(c.Crop_Name)) = 'corn'
         OR UPPER(TRIM(c.Crop_Code)) = 'C' THEN 'Corn'
    ELSE NULLIF(TRIM(c.Crop_Name), '') END"""


def build_inventory_snapshot(crop_year="", crop_name=""):
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    harvest_bu_sql = calculated_bushels_sql("h", "c")
    delivery_bu_sql = calculated_bushels_sql("d", "c")

    harvest_q = """
        SELECT
            s.StorLoc_ID,
            s.Bin_Code,
            s.Bin_Name,
            """ + INVENTORY_CROP_SQL + """ AS Crop_Name,
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
        WHERE s.Grower_ID=%s
    """
    params = [current_user.grower_id]

    if crop_year:
        harvest_q += " AND fi.Crop_Year = %s"
        params.append(crop_year)

    if crop_name:
        harvest_q += " AND (" + INVENTORY_CROP_SQL + ") = %s"
        params.append(crop_name)

    harvest_q += """
        GROUP BY s.StorLoc_ID, s.Bin_Code, s.Bin_Name, """ + INVENTORY_CROP_SQL + """
        ORDER BY s.Bin_Code, Crop_Name
    """
    cur.execute(harvest_q, params)
    harvest_rows = cur.fetchall()

    delivery_q = """
        SELECT
            s.StorLoc_ID,
            s.Bin_Code,
            s.Bin_Name,
            """ + INVENTORY_CROP_SQL + """ AS Crop_Name,
            SUM(COALESCE(""" + delivery_bu_sql + """, 0)) AS Delivered_Bu
        FROM Storage_Location s
        LEFT JOIN Delivery d ON d.StorLoc_ID = s.StorLoc_ID
        LEFT JOIN Crop c ON c.Crop_ID = d.Crop_ID
        WHERE s.Grower_ID=%s AND (d.Grower_ID=%s OR d.Delivery_ID IS NULL)
    """
    delivery_params = [current_user.grower_id, current_user.grower_id]

    # Attribute sales to the original harvest year, including later deliveries.
    if crop_year:
        delivery_q += " AND d.Crop_Year = %s"
        delivery_params.append(crop_year)

    if crop_name:
        delivery_q += " AND (" + INVENTORY_CROP_SQL + ") = %s"
        delivery_params.append(crop_name)

    delivery_q += """
        GROUP BY s.StorLoc_ID, s.Bin_Code, s.Bin_Name, """ + INVENTORY_CROP_SQL + """
    """
    cur.execute(delivery_q, delivery_params)
    # A left join emits an empty placeholder for bins with no deliveries.
    # Harvest already supplies empty-bin rows; do not add a duplicate crop row.
    delivery_rows = [r for r in cur.fetchall()
                     if r["Crop_Name"] is not None or r["Delivered_Bu"]]

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
            "Bin_Code": row["Bin_Code"],
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
            "Bin_Code": row["Bin_Code"],
            "Bin_Name": row["Bin_Name"],
            "Note": None,
            "Crop_Name": crop_label,
            "Harvest_Bu": 0.0,
            "Avg_MC": None,
            "Delivered_Bu": round(delivered_bu, 2),
            "Current_Bu": round(-delivered_bu, 2),
        })

    inventory_rows.sort(key=lambda x: (storage_sort_key(x["Bin_Code"] or x["Bin_Name"]), (x["Crop_Name"] or "")))

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

def invoice_unit_price(monthly_average, is_hmc=False):
    if monthly_average is None:
        return None
    price = Decimal(str(monthly_average)) + Decimal("0.04")
    if is_hmc:
        price *= Decimal("0.95")
    return price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


@app.route("/billing", methods=["GET"])
@admin_required
def billing():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    delivery_bu_sql = calculated_bushels_sql("d", "c")

    # Dropdown options
    cur.execute("SELECT DelLoc_ID, DelLoc_code, Location FROM Delivery_Location WHERE Grower_ID=%s ORDER BY DelLoc_code;", (current_user.grower_id,))
    locations = cur.fetchall()

    cur.execute("SELECT Crop_ID, Crop_Code, Crop_Name FROM Crop ORDER BY Crop_Code;")
    crops = cur.fetchall()

    # ---- Read user inputs (Excel-like) ----
    today = date.today()

    # Default: current month
    default_month_name = calendar.month_name[today.month]

    delivered_to_code = request.args.get("to", (locations[0]["DelLoc_code"] if locations else ""))
    crop_code = request.args.get("crop", (crops[0]["Crop_Code"] if crops else ""))

    # Default start/end = selected month range (same idea as Excel)
    month_num = _month_name_to_num(default_month_name) or today.month
    year = today.year

    start_default = date(year, month_num, 1)
    end_default = date(year, month_num, calendar.monthrange(year, month_num)[1])

    start_str = request.args.get("start", start_default.isoformat())
    end_str = request.args.get("end", end_default.isoformat())

    start_date, end_date = report_date_range(start_str, end_str, start_default, end_default)
    month_name = calendar.month_name[start_date.month]

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
          c.Crop_ID           AS Crop_ID,
          c.Crop_Name         AS Crop_Name,
          dl.DelLoc_code      AS ToCode,
          d.MC                AS MC,
          d.Gross_Weight      AS Gross,
          d.Tare_Weight       AS Tare,
          COALESCE(NULLIF(sl.Bin_Code, ''), sl.Bin_Name) AS Storage,
          """ + delivery_bu_sql + """ AS Bushels,
          d.Price             AS Price
        FROM Delivery d
        JOIN Crop c ON d.Crop_ID = c.Crop_ID
        JOIN Delivery_Location dl ON d.DelLoc_ID = dl.DelLoc_ID
        LEFT JOIN Storage_Location sl ON d.StorLoc_ID = sl.StorLoc_ID
        WHERE d.Delivery_Date BETWEEN %s AND %s AND d.Grower_ID=%s
          AND (%s IS NULL OR d.DelLoc_ID = %s)
          AND (%s IS NULL OR d.Crop_ID = %s)
        ORDER BY d.Delivery_Date, d.Ticket_Num;
    """, (start_date, end_date, current_user.grower_id, del_loc_id, del_loc_id, crop_id, crop_id))

    rows = cur.fetchall()

    # Use unadjusted market averages, not previously billed delivery prices.
    cur.execute("""
        SELECT Crop, Year, Month, AVG(Market_Price) AS average_price
        FROM MarketPriceMonthly
        WHERE Grower_ID=%s
          AND (Year * 100 + Month) BETWEEN %s AND %s
        GROUP BY Crop, Year, Month
    """, (current_user.grower_id, start_date.year * 100 + start_date.month,
          end_date.year * 100 + end_date.month))
    market_prices = {
        (r["Crop"], int(r["Year"]), int(r["Month"])): r["average_price"]
        for r in cur.fetchall()
    }
    corn_id = next((c["Crop_ID"] for c in crops
                    if (c.get("Crop_Code") or "").upper() == "C"
                    or (c.get("Crop_Name") or "").lower() == "corn"), None)
    for r in rows:
        is_hmc = ((r.get("Crop") or "").upper() == "HMC"
                  or (r.get("Crop_Name") or "").lower() in ("hmc", "high moisture corn"))
        price_crop_id = corn_id if is_hmc else r["Crop_ID"]
        delivery_date = r["Delivery_Date"]
        monthly_average = market_prices.get((price_crop_id, delivery_date.year, delivery_date.month))
        r["Uses_Stored_Price"] = monthly_average is None and r.get("Price") is not None
        # Historical delivery prices may already include billing adjustments.
        # Preserve them when no source average exists; never apply the markup twice.
        r["Price"] = (Decimal(str(r["Price"])) if r["Uses_Stored_Price"]
                      else invoice_unit_price(monthly_average, is_hmc))
        r["Total"] = (
            (Decimal(str(r.get("Bushels") or 0)) * r["Price"]).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP)
            if r["Price"] is not None else None
        )

    totals_sum = sum((r["Total"] for r in rows if r["Total"] is not None), Decimal("0"))
    price_vals = [r["Price"] for r in rows if r["Price"] is not None]
    avg_price = (sum(price_vals) / len(price_vals)) if price_vals else None
    missing_price_count = sum(r["Price"] is None for r in rows)
    total_bushels = sum(_to_float(r.get("Bushels")) for r in rows)
    delivered_to_name = next(
        (loc.get("Location") for loc in locations if loc["DelLoc_code"] == delivered_to_code),
        ""
    )
    crop_name = next(
        (crop.get("Crop_Name") for crop in crops if crop["Crop_Code"] == crop_code),
        crop_code
    )

    cur.close()
    conn.close()

    return render_template(
        "billing.html",
        invoice_date=today,
        invoice_date_display=f"{today.month}/{today.day}/{today.year}",
        month_name=month_name,
        delivered_to_code=delivered_to_code,
        crop_code=crop_code,
        start_date=start_date,
        end_date=end_date,
        locations=locations,
        crops=crops,
        rows=rows,
        totals_sum=totals_sum,
        avg_price=avg_price,
        missing_price_count=missing_price_count,
        stored_price_count=sum(r["Uses_Stored_Price"] for r in rows),
        total_bushels=total_bushels,
        delivered_to_name=delivered_to_name,
        crop_name=crop_name,
        billing_year=start_date.year
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

    start_date, end_date = report_date_range(
        start, end, date.today() - timedelta(days=30), date.today())

    context = build_reconcile_context(start_date, end_date, crop_id)
    return render_template("reconcile.html", **context)




def _f(x):
    if x is None:
        return 0.0
    if isinstance(x, Decimal):
        return float(x)
    return float(x)


def _canonical_crop_name(value):
    """Normalize equivalent crop labels used by legacy records."""
    name = (value or "").strip()
    if name.lower() in ("soybean", "soybeans"):
        return "Soybeans"
    return name


def _silage_base_field_name(value):
    """Return the grain field represented by a companion '-silage' field."""
    name = (value or "").strip()
    marker_index = name.lower().find("silage")
    if marker_index < 0:
        return name
    return name[:marker_index].rstrip(" -_/").strip()

@app.route("/delivery", methods=["GET"])
@login_required
def delivery():
    start = request.args.get("start")
    end = request.args.get("end")
    crop_id = request.args.get("crop_id", "")
    start_date, end_date = report_date_range(
        start, end, date.today() - timedelta(days=30), date.today())

    context = build_reconcile_context(start_date, end_date, crop_id)
    return render_template("delivery.html", **context)


def count_unassigned_deliveries():
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM Delivery WHERE Grower_ID=%s AND Crop_Year IS NULL",
                    (current_user.grower_id,))
        return cur.fetchone()[0]
    finally:
        cur.close()
        conn.close()


@app.route("/delivery/crop-years", methods=["GET", "POST"])
@login_required
@editor_required
def delivery_crop_years():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    try:
        if request.method == "POST":
            check_access_csrf()
            year = request.form.get("crop_year", "").strip()
            delivery_id = request.form.get("delivery_id", "")
            if not year.isdigit() or not 1900 <= int(year) <= 9999 or not delivery_id.isdigit():
                abort(400)
            cur.execute("UPDATE Delivery SET Crop_Year=%s WHERE Delivery_ID=%s AND Grower_ID=%s",
                        (int(year), int(delivery_id), current_user.grower_id))
            conn.commit()
            flash("Delivery crop year saved.", "success")
            return redirect(url_for("delivery_crop_years"))
        cur.execute("""SELECT d.Delivery_ID, d.Ticket_Num, d.Delivery_Date, d.Crop_Year,
                              c.Crop_Name, s.Bin_Code
                       FROM Delivery d JOIN Crop c ON c.Crop_ID=d.Crop_ID
                       LEFT JOIN Storage_Location s ON s.StorLoc_ID=d.StorLoc_ID
                       WHERE d.Grower_ID=%s
                       ORDER BY d.Crop_Year IS NULL DESC, d.Delivery_Date DESC, d.Delivery_ID DESC""",
                    (current_user.grower_id,))
        return render_template("delivery_crop_years.html", rows=cur.fetchall())
    finally:
        cur.close()
        conn.close()



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
    crop        = _canonical_crop_name(request.args.get("crop", ""))

    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT DISTINCT
            fi.Crop_Year,
            g.Grower_Name,
            d.Dpt_Name AS Department_Name,
            fi.Field_Name,
            c.Crop_Name
        FROM Harvest h
        JOIN Field fi ON h.Field_ID = fi.Field_ID
        JOIN Department d ON fi.Dpt_ID = d.Dpt_ID
        JOIN Grower g ON d.Grower_ID = g.Grower_ID
        JOIN Crop c ON h.Crop_ID = c.Crop_ID
        WHERE g.Grower_ID=%s
        ORDER BY fi.Crop_Year DESC, g.Grower_Name, d.Dpt_Name, fi.Field_Name, c.Crop_Name
    """, (current_user.grower_id,))
    filter_rows = cur.fetchall()

    filter_options = {
        "crop_years": sorted({r["Crop_Year"] for r in filter_rows if r["Crop_Year"] is not None}, reverse=True),
        "growers": sorted({r["Grower_Name"] for r in filter_rows if r["Grower_Name"]}),
        "departments": sorted({
            r["Department_Name"] for r in filter_rows
            if r["Department_Name"] and (not crop_year or str(r["Crop_Year"]) == crop_year)
        }),
        "fields": sorted({
            r["Field_Name"] for r in filter_rows
            if r["Field_Name"]
            and (not crop_year or str(r["Crop_Year"]) == crop_year)
            and (not department or r["Department_Name"] == department)
        }),
        "crops": sorted({
            _canonical_crop_name(r["Crop_Name"]) for r in filter_rows
            if r["Crop_Name"]
            and (not crop_year or str(r["Crop_Year"]) == crop_year)
            and (not department or r["Department_Name"] == department)
            and (not field or r["Field_Name"] == field)
        })
    }

    harvest_bu_sql = calculated_bushels_sql("h", "c")
    yield_crop_sql = "'Corn/HMC'" if crop == "Corn/HMC" else """CASE
                WHEN LOWER(TRIM(c.Crop_Name)) IN ('soybean', 'soybeans') THEN 'Soybeans'
                ELSE c.Crop_Name
            END"""
    query = """
        SELECT
            fi.Crop_Year AS Crop_Year,
            g.Grower_Name,
            d.Dpt_Name AS Department_Name,
            fi.Field_Name,
            """ + yield_crop_sql + """ AS Crop_Name,
            fi.Acres,
            fi.Irr_Type,
            fi.Hybrid_Variety,
            fi.Note,

            ROUND(SUM(COALESCE(""" + harvest_bu_sql + """, 0)), 1) AS Total_Bushels,
            ROUND(SUM(COALESCE(""" + harvest_bu_sql + """, 0)) / NULLIF(fi.Acres, 0), 2) AS Yield_bu_per_acre,

            ROUND(AVG(h.MC), 2) AS Avg_MC,

            ROUND(SUM(COALESCE(""" + harvest_bu_sql + """, 0)), 1) AS Total_WetBushels,
            ROUND(SUM(COALESCE(""" + harvest_bu_sql + """, 0)), 1) AS Total_DryBushels,
            ROUND(SUM(COALESCE(""" + harvest_bu_sql + """, 0)) / NULLIF(fi.Acres, 0), 2) AS Dry_Yield_bu_per_acre

        FROM Harvest h
        JOIN Field fi       ON h.Field_ID = fi.Field_ID
        JOIN Department d   ON fi.Dpt_ID = d.Dpt_ID
        JOIN Grower g       ON d.Grower_ID = g.Grower_ID
        JOIN Crop c         ON h.Crop_ID = c.Crop_ID

        WHERE g.Grower_ID=%s
    """

    params = [current_user.grower_id]

    # Apply filters
    if crop_year:
        query += " AND fi.Crop_Year = %s"
        params.append(crop_year)

    if grower:
        query += " AND g.Grower_Name = %s"
        params.append(grower)

    if department:
        query += " AND d.Dpt_Name = %s"
        params.append(department)

    if field:
        query += " AND fi.Field_Name = %s"
        params.append(field)

    if crop:
        if crop == "Corn/HMC":
            query += " AND (UPPER(TRIM(c.Crop_Code)) IN ('C', 'HMC') OR LOWER(TRIM(c.Crop_Name)) IN ('corn', 'hmc', 'high moisture corn'))"
        elif crop == "Soybeans":
            query += " AND LOWER(TRIM(c.Crop_Name)) IN ('soybean', 'soybeans')"
        else:
            query += " AND c.Crop_Name = %s"
            params.append(crop)

    query += """
        GROUP BY
            fi.Field_ID, fi.Crop_Year, g.Grower_Name, d.Dpt_Name, fi.Field_Name,
            """ + yield_crop_sql + """,
            fi.Acres,
            fi.Irr_Type, fi.Hybrid_Variety, fi.Note
        ORDER BY
            fi.Crop_Year DESC, g.Grower_Name, d.Dpt_Name, fi.Field_Name
    """

    cur.execute(query, params)
    results = cur.fetchall()

    silage_query = """
        SELECT fi.Field_Name, fi.Acres, fi.Silage_Bu_Per_Acre, fi.Crop_Year, fi.Irr_Type
        FROM Field fi
        JOIN Department d ON fi.Dpt_ID=d.Dpt_ID
        WHERE d.Grower_ID=%s AND LOWER(fi.Field_Name) LIKE %s
    """
    silage_params = [current_user.grower_id, "%silage%"]
    if crop_year:
        silage_query += " AND fi.Crop_Year=%s"
        silage_params.append(crop_year)
    if department:
        silage_query += " AND d.Dpt_Name=%s"
        silage_params.append(department)
    silage_query += " ORDER BY fi.Crop_Year DESC, fi.Field_Name"
    cur.execute(silage_query, silage_params)
    silage_fields = cur.fetchall()
    cur.close()
    conn.close()

    def irrigation_group(value):
        text = (value or "").strip().lower()
        if not text:
            return "Unspecified"
        return "Irrigated" if text.startswith("i") else "Dryland"

    yield_sections = []
    section_keys = sorted(
        {(r["Crop_Year"], _canonical_crop_name(r["Crop_Name"])) for r in results if r.get("Crop_Name")},
        key=lambda item: (-int(item[0]), item[1])
    )
    for section_year, crop_name in section_keys:
        crop_rows = [
            r for r in results
            if r["Crop_Year"] == section_year and _canonical_crop_name(r["Crop_Name"]) == crop_name
        ]
        total_acres = sum(_f(r.get("Acres")) for r in crop_rows)
        total_bushels = sum(_f(r.get("Total_Bushels")) for r in crop_rows)

        type_summary = []
        for group_name in ("Irrigated", "Dryland"):
            grouped = [r for r in crop_rows if irrigation_group(r.get("Irr_Type")) == group_name]
            acres = sum(_f(r.get("Acres")) for r in grouped)
            bushels = sum(_f(r.get("Total_Bushels")) for r in grouped)
            type_summary.append({
                "name": group_name,
                "acres": acres,
                "bushels": bushels,
                "avg_yield": (bushels / acres) if acres else None,
            })

        hybrid_summary = []
        hybrids = sorted({(r.get("Hybrid_Variety") or "Unspecified").strip() for r in crop_rows})
        for hybrid in hybrids:
            hybrid_rows = [
                r for r in crop_rows
                if (r.get("Hybrid_Variety") or "Unspecified").strip() == hybrid
            ]
            averages = {}
            for group_name in ("Dryland", "Irrigated"):
                grouped = [r for r in hybrid_rows if irrigation_group(r.get("Irr_Type")) == group_name]
                acres = sum(_f(r.get("Acres")) for r in grouped)
                bushels = sum(_f(r.get("Total_Bushels")) for r in grouped)
                averages[group_name] = (bushels / acres) if acres else None
            hybrid_summary.append({"name": hybrid, **averages})

        silage_rows = []
        if crop_name.lower() in ("corn", "corn/hmc"):
            for silage_field in silage_fields:
                if silage_field["Crop_Year"] != section_year:
                    continue
                base_name = _silage_base_field_name(silage_field["Field_Name"])
                silage_acres = _f(silage_field.get("Acres"))
                silage_yield = _f(silage_field.get("Silage_Bu_Per_Acre")) if silage_field.get("Silage_Bu_Per_Acre") is not None else None
                if silage_acres > 0:
                    silage_rows.append({
                        "field_name": silage_field["Field_Name"],
                        "base_field_name": base_name,
                        "acres": silage_acres,
                        "yield": silage_yield,
                        "bushels": silage_acres * silage_yield if silage_yield is not None else None,
                        "type": irrigation_group(silage_field.get("Irr_Type")),
                        "status": None if silage_yield is not None else f"Add Silage Bu/ac to {silage_field['Field_Name']}",
                    })

        yield_sections.append({
            "crop_name": crop_name,
            "crop_year": section_year,
            "rows": crop_rows,
            "total_acres": total_acres,
            "total_bushels": total_bushels,
            "avg_yield": (total_bushels / total_acres) if total_acres else None,
            "type_summary": type_summary,
            "hybrid_summary": hybrid_summary,
            "silage_rows": silage_rows,
            "silage_irrigated_bushels": sum(r["bushels"] for r in silage_rows if r["type"] == "Irrigated" and r["bushels"] is not None),
            "silage_dryland_bushels": sum(r["bushels"] for r in silage_rows if r["type"] == "Dryland" and r["bushels"] is not None),
            "silage_unspecified_bushels": sum(r["bushels"] for r in silage_rows if r["type"] == "Unspecified" and r["bushels"] is not None),
            "silage_has_irrigated": any(r["type"] == "Irrigated" and r["bushels"] is not None for r in silage_rows),
            "silage_has_dryland": any(r["type"] == "Dryland" and r["bushels"] is not None for r in silage_rows),
            "silage_has_unspecified": any(r["type"] == "Unspecified" and r["bushels"] is not None for r in silage_rows),
            "notes": sorted({r["Note"].strip() for r in crop_rows if r.get("Note") and r["Note"].strip()}),
        })

    active_filters = {
        "crop_year": crop_year,
        "grower": grower,
        "department": department,
        "field": field,
        "crop": crop
    }

    return render_template(
        "yield.html",
        results=results,
        yield_sections=yield_sections,
        active_filters=active_filters,
        filter_options=filter_options
    )


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
    crop        = _canonical_crop_name(request.args.get("crop", ""))

    harvest_bu_sql = calculated_bushels_sql("h", "c")
    yield_crop_sql = "'Corn/HMC'" if crop == "Corn/HMC" else """CASE
                WHEN LOWER(TRIM(c.Crop_Name)) IN ('soybean', 'soybeans') THEN 'Soybeans'
                ELSE c.Crop_Name
            END"""
    query = """
        SELECT
            fi.Crop_Year AS Crop_Year,
            g.Grower_Name,
            d.Dpt_Name AS Department_Name,
            fi.Field_Name,
            """ + yield_crop_sql + """ AS Crop_Name,
            fi.Acres,

            ROUND(SUM(COALESCE(""" + harvest_bu_sql + """, 0)), 1) AS Total_Bushels,
            ROUND(SUM(COALESCE(""" + harvest_bu_sql + """, 0)) / NULLIF(fi.Acres, 0), 2) AS Yield_bu_per_acre,

            ROUND(AVG(h.MC), 2) AS Avg_MC,

            ROUND(SUM(COALESCE(""" + harvest_bu_sql + """, 0)), 1) AS Total_WetBushels,
            ROUND(SUM(COALESCE(""" + harvest_bu_sql + """, 0)), 1) AS Total_DryBushels,
            ROUND(SUM(COALESCE(""" + harvest_bu_sql + """, 0)) / NULLIF(fi.Acres, 0), 2) AS Dry_Yield_bu_per_acre

        FROM Harvest h
        JOIN Field fi       ON h.Field_ID = fi.Field_ID
        JOIN Department d   ON fi.Dpt_ID = d.Dpt_ID
        JOIN Grower g       ON d.Grower_ID = g.Grower_ID
        JOIN Crop c         ON h.Crop_ID = c.Crop_ID

        WHERE g.Grower_ID=%s
    """

    params = [current_user.grower_id]

    if crop_year:
        query += " AND fi.Crop_Year = %s"
        params.append(crop_year)
    if grower:
        query += " AND g.Grower_Name = %s"
        params.append(grower)
    if department:
        query += " AND d.Dpt_Name = %s"
        params.append(department)
    if field:
        query += " AND fi.Field_Name = %s"
        params.append(field)
    if crop:
        if crop == "Corn/HMC":
            query += " AND (UPPER(TRIM(c.Crop_Code)) IN ('C', 'HMC') OR LOWER(TRIM(c.Crop_Name)) IN ('corn', 'hmc', 'high moisture corn'))"
        elif crop == "Soybeans":
            query += " AND LOWER(TRIM(c.Crop_Name)) IN ('soybean', 'soybeans')"
        else:
            query += " AND c.Crop_Name = %s"
            params.append(crop)

    query += """
        GROUP BY
            fi.Field_ID, fi.Crop_Year, g.Grower_Name, d.Dpt_Name, fi.Field_Name,
            """ + yield_crop_sql + """,
            fi.Acres
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

    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("""SELECT DISTINCT fi.Crop_Year
        FROM Field fi JOIN Department d ON fi.Dpt_ID=d.Dpt_ID
        WHERE d.Grower_ID=%s AND fi.Crop_Year IS NOT NULL
        UNION SELECT Crop_Year FROM Delivery WHERE Grower_ID=%s AND Crop_Year IS NOT NULL
        ORDER BY Crop_Year DESC""", (current_user.grower_id, current_user.grower_id))
    crop_years = [r["Crop_Year"] for r in cur.fetchall()]
    cur.execute("""SELECT DISTINCT """ + INVENTORY_CROP_SQL + """ AS Crop_Name
        FROM Crop c
        WHERE EXISTS (SELECT 1 FROM Harvest h
            JOIN Field fi ON h.Field_ID=fi.Field_ID
            JOIN Department d ON fi.Dpt_ID=d.Dpt_ID
            WHERE h.Crop_ID=c.Crop_ID AND d.Grower_ID=%s)
           OR EXISTS (SELECT 1 FROM Delivery d
            WHERE d.Crop_ID=c.Crop_ID AND d.Grower_ID=%s)
        ORDER BY Crop_Name""", (current_user.grower_id, current_user.grower_id))
    crop_options = [r["Crop_Name"] for r in cur.fetchall() if r["Crop_Name"]]
    cur.close()
    conn.close()

    active_filters = {"crop_year": crop_year, "crop": crop_name}

    return render_template(
        "inventory.html",
        rows=inventory_rows,
        summary=summary,
        corn_split=corn_split,
        crop_years=crop_years,
        crop_options=crop_options,
        active_filters=active_filters,
        unassigned_deliveries=count_unassigned_deliveries()
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
            "BIN LOCATION": row["Bin_Code"] or row["Bin_Name"],
            "Note": row["Note"] or "",
            "CROP": row["Crop_Name"],
            "HARVEST": row["Harvest_Bu"],
            "MC": row["Avg_MC"],
            "DELIVERED": row["Delivered_Bu"],
            "CURRENT": row["Current_Bu"],
        }
        for row in rows
    ])
    # Keep the natural bin order from build_inventory_snapshot.

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Inventory")
        writer.sheets["Inventory"].freeze_panes = "A2"
        unassigned = count_unassigned_deliveries()
        pd.DataFrame([{
            "Crop year": crop_year or "All years",
            "Unassigned deliveries": unassigned,
            "Status": "Incomplete: assign delivery crop years" if crop_year and unassigned else "",
        }]).to_excel(writer, index=False, sheet_name="Report Notes")
    output.seek(0)

    return send_file(output, as_attachment=True, download_name="Inventory_Report.xlsx")


@app.route("/raven/import", methods=["GET", "POST"])
@admin_required
def raven_import():
    from raven_jobs import start, latest
    form = {key: request.form.get(key, "").strip() for key in ("year", "from_date", "file_ids")}
    if request.method == "POST":
        try:
            from import_grc import parse_file_id_tokens, safe_date
            year = int(form["year"]) if form["year"] else None
            if year is not None and not 2000 <= year <= 2100:
                raise ValueError("Crop/load year must be between 2000 and 2100.")
            if form["from_date"] and safe_date(form["from_date"]) is None:
                raise ValueError("From date must be a valid date.")
            ids = parse_file_id_tokens([form["file_ids"]]) if form["file_ids"] else []
            if form["file_ids"] and not ids:
                raise ValueError("Enter valid Raven file IDs.")
            start(current_user.grower_id, {"year": year, "from_date": form["from_date"], "file_ids": ids})
            flash("Import started. You can leave this page and return to check progress.", "success")
            return redirect(url_for("raven_import"))
        except ValueError as exc:
            flash(str(exc), "danger")
        except Exception:
            app.logger.exception("Could not start Raven import")
            flash("Could not start the import. Check the server log for details.", "danger")
    job = latest(current_user.grower_id)
    if request.method == "GET" and job:
        form = {"year": job["options"]["year"] or "", "from_date": job["options"]["from_date"],
                "file_ids": ",".join(map(str, job["options"]["file_ids"]))}
    return render_template("raven_import.html", form=form, job=job)


@app.get("/raven/import/status")
@admin_required
def raven_import_status():
    from raven_jobs import latest
    response = jsonify(job=latest(current_user.grower_id))
    response.headers["Cache-Control"] = "no-store"
    return response


















if __name__ == "__main__":
    app.run(
        host=os.getenv("FLASK_RUN_HOST", "127.0.0.1"),
        port=int(os.getenv("FLASK_RUN_PORT", "5000")),
    )

# @app.route("/slingshot/jobdata")
# def slingshot_jobdata():
#     data = get_jobdata_summary(pagesize=20)  # try small page first
#     return jsonify(data)


