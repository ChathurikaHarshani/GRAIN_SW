"""Persistent, single-server Raven jobs, executed outside Gunicorn requests."""
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import threading
import time
import uuid
from contextlib import contextmanager
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")
DATA = Path(os.environ.get("GMS_JOB_DIR", ROOT / "data" / "raven_jobs"))


@contextmanager
def database():
    DATA.mkdir(parents=True, exist_ok=True, mode=0o700)
    db = sqlite3.connect(str(DATA / "jobs.sqlite3"), timeout=15)
    db.row_factory = sqlite3.Row
    db.execute("""CREATE TABLE IF NOT EXISTS jobs (
        id TEXT PRIMARY KEY, grower INTEGER, options TEXT, status TEXT,
        heartbeat REAL, created REAL)""")
    try:
        with db:
            yield db
    finally:
        db.close()


def expire(db):
    db.execute("""UPDATE jobs SET status='interrupted'
        WHERE status IN ('queued','running') AND heartbeat < ?""",
               (time.time() - 180,))


def start(grower, options):
    with database() as db:
        db.execute("BEGIN IMMEDIATE")
        expire(db)
        if db.execute("SELECT 1 FROM jobs WHERE status IN ('queued','running')").fetchone():
            raise ValueError("An import is already running. Wait for it to finish.")
        job_id = uuid.uuid4().hex
        now = time.time()
        db.execute("INSERT INTO jobs VALUES (?,?,?,?,?,?)",
                   (job_id, grower, json.dumps(options), "queued", now, now))
    try:
        flags = {"creationflags": subprocess.CREATE_NO_WINDOW} if os.name == "nt" else {"start_new_session": True}
        # No shell, passwords, or API keys in the command line.
        with open(DATA / (job_id + ".log"), "ab", buffering=0) as log:
            subprocess.Popen([sys.executable, "-u", str(Path(__file__).resolve()), job_id],
                             cwd=str(ROOT), stdin=subprocess.DEVNULL,
                             stdout=log, stderr=log, close_fds=True, **flags)
    except Exception:
        with database() as db:
            db.execute("UPDATE jobs SET status='failed' WHERE id=?", (job_id,))
        raise
    return job_id


def latest(grower):
    with database() as db:
        expire(db)
        row = db.execute("SELECT * FROM jobs WHERE grower=? ORDER BY created DESC LIMIT 1",
                         (grower,)).fetchone()
    if not row:
        return None
    result = dict(row)
    result["options"] = json.loads(result["options"])
    path = DATA / (result["id"] + ".log")
    try:
        with path.open("rb") as log:
            log.seek(max(0, path.stat().st_size - 20000))
            result["output"] = log.read().decode("utf-8", errors="replace")
    except FileNotFoundError:
        result["output"] = "Preparing import…"
    # Do not expose configured credentials in upstream error messages.
    for key in ("DB_PASSWORD", "RAVEN_API_KEY", "RAVEN_SHARED_SECRET", "RAVEN_ACCESS_KEY"):
        secret = os.environ.get(key)
        if secret:
            result["output"] = result["output"].replace(secret, "[redacted]")
    return result


def run(job_id):
    with database() as db:
        row = db.execute("SELECT * FROM jobs WHERE id=? AND status='queued'", (job_id,)).fetchone()
        if not row:
            return
        db.execute("UPDATE jobs SET status='running', heartbeat=? WHERE id=?", (time.time(), job_id))
    stop = threading.Event()

    def heartbeat():
        while not stop.wait(5):
            with database() as db:
                db.execute("UPDATE jobs SET heartbeat=? WHERE id=?", (time.time(), job_id))

    thread = threading.Thread(target=heartbeat, daemon=True)
    thread.start()
    status = "failed"
    try:
        from import_grc import import_all_graincart_files, import_graincart_files_by_ids, safe_date
        options = json.loads(row["options"])
        kwargs = {"filter_year": options["year"], "from_date": safe_date(options["from_date"])}
        print("Import started. Progress appears below.", flush=True)
        if options["file_ids"]:
            import_graincart_files_by_ids(options["file_ids"], **kwargs)
            status = "completed"
        else:
            errors = import_all_graincart_files(**kwargs)
            status = "completed_with_errors" if errors else "completed"
        print("Import finished.", flush=True)
    except Exception as exc:
        print("Import failed: " + str(exc), flush=True)
    finally:
        stop.set()
        thread.join(timeout=10)
        with database() as db:
            db.execute("UPDATE jobs SET status=?, heartbeat=? WHERE id=?",
                       (status, time.time(), job_id))


if __name__ == "__main__":
    run(sys.argv[1])
