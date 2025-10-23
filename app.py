from flask import Flask, render_template
from db import get_conn

app = Flask(__name__)

@app.route("/health")
def health():
    # optional DB ping for sanity
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

@app.route("/")
def index():
    return render_template("index.html", app_name="GMS")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
