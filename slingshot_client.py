# slingshot_client.py
import os, time, base64, hmac, hashlib
from urllib.parse import urlparse
import requests

BASE = "https://api.ravenslingshot.com"

API_KEY = os.getenv("RAVEN_API_KEY", "")
ACCESS_KEY = os.getenv("RAVEN_ACCESS_KEY", "")
# Docs show the shared secret is Base64-encoded; decode before HMAC use.
# (If yours is plain text, remove base64.b64decode)
_SHARED_SECRET_RAW = os.getenv("RAVEN_SHARED_SECRET", "")
try:
    SHARED_SECRET = base64.b64decode(_SHARED_SECRET_RAW)
except Exception:
    # fallback if secret is plain text (not recommended by docs)
    SHARED_SECRET = _SHARED_SECRET_RAW.encode("utf-8")

def _canonical_block(method: str, host: str, url_path: str, ts: str) -> bytes:
    """
    Per 'Generating a Signature':
    {Method}\r\n{Host}\r\n{URL}\r\n{Unix Timestamp}\r\n{API Key}\r\n{Access Key}\r\n
    - Method: ALL CAPS
    - Host: lower-case (e.g., api.ravenslingshot.com)
    - URL: absolute path (no query), lower-case (e.g., /jobdata)
    """
    block = (
        f"{method.upper()}\r\n"
        f"{host.lower()}\r\n"
        f"{url_path.lower()}\r\n"
        f"{ts}\r\n"
        f"{API_KEY}\r\n"
        f"{ACCESS_KEY}\r\n"
    )
    return block.encode("utf-8")

def _sign(method: str, full_url: str, ts: int) -> str:
    u = urlparse(full_url)
    canonical = _canonical_block(method, u.netloc, u.path, str(ts))
    digest = hmac.new(SHARED_SECRET, canonical, hashlib.sha1).digest()
    return base64.b64encode(digest).decode("ascii")

def _headers(method: str, path: str) -> dict:
    # 120-second lifetime; keep your clock in sync (NTP)
    ts = int(time.time())
    url = f"{BASE}{path}"
    sig = _sign(method, url, ts)
    return {
        "X-SS-APIKey": API_KEY,
        "X-SS-Signature": sig,
        "X-SS-AccessKey": ACCESS_KEY,
        "X-SS-TimeStamp": str(ts),
        "Accept": "application/json",  # request JSON (see docs)
    }

def get_jobdata_summary(pagesize: int | None = None, page: int | None = None, since_iso: str | None = None):
    """
    GET /jobdata with optional paging and date filter.
    - pagesize: int
    - page: int (0-index per docs’ "PageIndex")
    - since_iso: 'YYYY-MM-DD HH:MM:SS' (docs: ISO8601; they show a space separator)
    Returns: dict (JSON)
    """
    path = "/jobdata"
    params = {}
    if pagesize is not None:
        params["pagesize"] = pagesize
    if page is not None:
        params["page"] = page
    if since_iso:
        params["date"] = since_iso

    url = f"{BASE}{path}"
    hdrs = _headers("GET", path)
    r = requests.get(url, headers=hdrs, params=params, timeout=30)
    r.raise_for_status()
    return r.json()
