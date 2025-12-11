from flask import Flask, render_template, jsonify, request, redirect, url_for
from db import get_conn
# from slingshot_client import get_jobdata_summary   # keep commented for now

app = Flask(__name__)

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

# ----------------- Home page ----------------- #
@app.route("/")
def index():
    # You can add more data later if needed
    return render_template("index.html", app_name="GMS")

# ----------------- Grower: list + create ----------------- #
@app.route("/growers")
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

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)






























# @app.route("/slingshot/jobdata")
# def slingshot_jobdata():
#     data = get_jobdata_summary(pagesize=20)  # try small page first
#     return jsonify(data)


