"""
slingshot_client.py

Raven Slingshot API client + GRC parser

What this file does
-------------------
- Authenticates to Raven Slingshot
- Lists grain cart files
- Downloads original .grc file content using ?format=bin
- Parses the text-based .grc file into:
    - header
    - loads

Required .env variables
-----------------------
RAVEN_API_KEY=...
RAVEN_SHARED_SECRET=...
RAVEN_ACCESS_KEY=...
RAVEN_BASE_URL=https://api.ravenslingshot.com

Optional:
RAVEN_TIMEOUT=120
RAVEN_VERIFY_SSL=true
"""

from __future__ import annotations

import base64
import csv
import hashlib
import hmac
import json
import os
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


class SlingshotClientError(Exception):
    pass


class SlingshotAuthError(SlingshotClientError):
    pass


class SlingshotHTTPError(SlingshotClientError):
    pass


@dataclass
class SlingshotConfig:
    api_key: str
    shared_secret: str
    access_key: str
    base_url: str = "https://api.ravenslingshot.com"
    timeout: int = 120
    verify_ssl: bool = True

    @classmethod
    def from_env(cls) -> "SlingshotConfig":
        load_dotenv()

        api_key = (os.getenv("RAVEN_API_KEY") or "").strip()
        shared_secret = (os.getenv("RAVEN_SHARED_SECRET") or "").strip()
        access_key = (os.getenv("RAVEN_ACCESS_KEY") or "").strip()
        base_url = (os.getenv("RAVEN_BASE_URL") or "https://api.ravenslingshot.com").strip().rstrip("/")
        timeout = int((os.getenv("RAVEN_TIMEOUT") or "120").strip())
        verify_ssl = (os.getenv("RAVEN_VERIFY_SSL") or "true").strip().lower() in {"1", "true", "yes", "y"}

        missing = []
        if not api_key:
            missing.append("RAVEN_API_KEY")
        if not shared_secret:
            missing.append("RAVEN_SHARED_SECRET")
        if not access_key:
            missing.append("RAVEN_ACCESS_KEY")

        if missing:
            raise SlingshotClientError(
                "Missing required environment variables: " + ", ".join(missing)
            )

        return cls(
            api_key=api_key,
            shared_secret=shared_secret,
            access_key=access_key,
            base_url=base_url,
            timeout=timeout,
            verify_ssl=verify_ssl,
        )


class SlingshotClient:
    def __init__(self, config: Optional[SlingshotConfig] = None) -> None:
        self.config = config or SlingshotConfig.from_env()
        self.session = requests.Session()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def get_access_key_summary(self) -> Dict[str, Any]:
        return self._get_json("/accesskey")

    def list_graincart_files(self, page: int = 0, pagesize: int = 100) -> Dict[str, Any]:
        return self._get_json("/graincart", params={"page": page, "pagesize": pagesize})

    def get_graincart_detail(self, graincart_id: int) -> Dict[str, Any]:
        return self._get_json(f"/graincart/{graincart_id}")

    def download_graincart_bin(self, graincart_id: int) -> bytes:
        return self._get_bytes(f"/graincart/{graincart_id}", params={"format": "bin"})
    
    def _extract_cart_code_from_bridge_id_or_file(self, row: Dict[str, Any]) -> Any:
        """
        GRC load rows do not have a Cart ID column.
        The cart identifier is usually represented by BridgeId in the file header,
        such as 00:00:00:00:58:95 -> cart code 58:95.

        Since _normalize_load_row only receives the row, this returns None here.
        The importer should fall back to header['bridge_id'] when cart_id is missing.
        """
        return self._get_first(row, ["Cart ID", "CartID", "Cart"])

    def download_graincart_text(self, graincart_id: int) -> str:
        raw = self.download_graincart_bin(graincart_id)
        for encoding in ("utf-8", "utf-8-sig", "latin-1"):
            try:
                return raw.decode(encoding)
            except UnicodeDecodeError:
                continue
        return raw.decode("utf-8", errors="replace")

    def get_parsed_graincart_file(self, graincart_id: int, file_name: Optional[str] = None) -> Dict[str, Any]:
        text = self.download_graincart_text(graincart_id)
        return self.parse_grc_text(text=text, graincart_id=graincart_id, file_name=file_name)

    def iter_all_graincart_summaries(self, pagesize: int = 100):
        page = 0
        while True:
            payload = self.list_graincart_files(page=page, pagesize=pagesize)
            items = self._extract_summary_items(payload)

            if not items:
                break

            for item in items:
                yield item

            if not payload.get("IsNextPage"):
                break

            page += 1

    # ------------------------------------------------------------------
    # HTTP helpers
    # ------------------------------------------------------------------
    def _get_json(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        response = self._request("GET", path, params=params, accept="application/json")
        try:
            return response.json()
        except Exception as exc:
            raise SlingshotHTTPError(
                f"Expected JSON response from {path}, but parsing failed. "
                f"HTTP {response.status_code}. Body starts with: {response.text[:500]}"
            ) from exc

    def _get_bytes(self, path: str, params: Optional[Dict[str, Any]] = None) -> bytes:
        response = self._request("GET", path, params=params, accept="*/*")
        return response.content

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        accept: str = "application/json",
    ) -> requests.Response:
        method = method.upper()
        path = self._normalize_path(path)

        url = f"{self.config.base_url}{path}"

        max_attempts = 6
        for attempt in range(max_attempts):
            timestamp = self._unix_timestamp()
            signature = self._build_signature(method=method, path=path, timestamp=timestamp)

            headers = {
                "X-SS-APIKey": self.config.api_key,
                "X-SS-AccessKey": self.config.access_key,
                "X-SS-TimeStamp": timestamp,
                "X-SS-Signature": signature,
                "Accept": accept,
            }

            response = self.session.request(
                method=method,
                url=url,
                params=params,
                headers=headers,
                timeout=self.config.timeout,
                verify=self.config.verify_ssl,
            )

            if response.status_code == 401:
                raise SlingshotAuthError(
                    "Slingshot returned 401 Unauthorized.\n"
                    f"Signed path: {path}\n"
                    f"Response body: {response.text[:1000]}"
                )

            if response.status_code == 429:
                wait_seconds = min(60, 5 * (attempt + 1))
                print(f"Slingshot throttled {method} {path}. Waiting {wait_seconds}s and retrying...")
                time.sleep(wait_seconds)
                continue

            if not response.ok:
                raise SlingshotHTTPError(
                    f"Slingshot request failed: {method} {url} -> HTTP {response.status_code}\n"
                    f"Response body: {response.text[:2000]}"
                )

            return response

        raise SlingshotHTTPError(
            f"Slingshot request failed after retries: {method} {url} -> HTTP 429\n"
            "Response body: Exceeded maximum requests."
        )

    # ------------------------------------------------------------------
    # Signature
    # ------------------------------------------------------------------
    def _build_signature(self, method: str, path: str, timestamp: str) -> str:
        parsed = urlparse(self.config.base_url)
        host = parsed.netloc.lower()
        url_to_sign = path.lower()

        block_to_sign = (
            f"{method.upper()}\r\n"
            f"{host}\r\n"
            f"{url_to_sign}\r\n"
            f"{timestamp}\r\n"
            f"{self.config.api_key}\r\n"
            f"{self.config.access_key}\r\n"
        )

        try:
            secret_bytes = base64.b64decode(self.config.shared_secret, validate=True)
        except Exception as exc:
            raise SlingshotClientError(
                "RAVEN_SHARED_SECRET is not valid base64."
            ) from exc

        digest = hmac.new(
            secret_bytes,
            block_to_sign.encode("utf-8"),
            hashlib.sha1,
        ).digest()

        return base64.b64encode(digest).decode("utf-8")

    # ------------------------------------------------------------------
    # GRC parser
    # ------------------------------------------------------------------
    def parse_grc_text(self, text: str, graincart_id: Optional[int] = None, file_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Parse text-based .grc file.

        Format observed:
        - header key/value rows
        - one units row
        - one actual load header row
        - load data rows
        """
        lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")

        parsed_rows: List[List[str]] = []
        for line in lines:
            line = line.strip()
            if not line:
                continue

            row = next(csv.reader([line]))
            row = [cell.strip() for cell in row]

            while row and row[-1] == "":
                row.pop()

            if row:
                parsed_rows.append(row)

        header_map: Dict[str, str] = {}
        load_columns: List[str] = []
        loads: List[Dict[str, Any]] = []

        i = 0
        while i < len(parsed_rows):
            row = parsed_rows[i]

            # Detect the real load header row
            if self._looks_like_load_header(row):
                load_columns = row
                i += 1

                # All following rows are load rows until file ends
                while i < len(parsed_rows):
                    data_row = parsed_rows[i]

                    # skip blank/separator-like rows
                    if not data_row:
                        i += 1
                        continue

                    load_row = {}
                    for col_idx, col_name in enumerate(load_columns):
                        value = data_row[col_idx] if col_idx < len(data_row) else None
                        load_row[col_name] = value

                    loads.append(load_row)
                    i += 1

                break

            # Before load section, collect simple key/value header rows
            if len(row) >= 2:
                key = row[0]
                value = row[1]
                if key:
                    header_map[key] = value

            i += 1

        parsed = {
            "graincart_id": graincart_id,
            "header": {
                "grc_version": header_map.get("GrcVersion"),
                "software_version": header_map.get("SoftwareVersion"),
                "job_number": self._safe_int(header_map.get("JobNumber")),
                "grower": header_map.get("Grower"),
                "farm": header_map.get("Farm"),
                "field": header_map.get("Field"),
                "year": self._safe_int(header_map.get("Year")),
                "crop": header_map.get("Crop"),
                "bridge_id": header_map.get("BridgeId"),
                "date_created": header_map.get("DateCreated"),
                "time_created": header_map.get("TimeCreated"),
                "file_name": file_name,
            },
            "loads": [self._normalize_load_row(r) for r in loads],
            "raw_header": header_map,
            "load_columns": load_columns,
        }

        return parsed

    def _looks_like_load_header(self, row: List[str]) -> bool:
        row_lower = [c.strip().lower() for c in row]

        required = {
            "loadnumber",
            "weight",
            "truckid",
            "destination",
            "moisture",
            "testweight",
            "wetbushels",
            "drybushels",
        }

        return required.issubset(set(r.replace(" ", "") for r in row_lower))

    def _normalize_load_row(self, row: Dict[str, Any]) -> Dict[str, Any]:
        load_date = self._get_first(row, ["LocalDate", "LoadDate"])
        load_time = self._get_first(row, ["LocalTime", "LoadTime"])

        combined_dt = None
        if load_date and load_time:
            combined_dt = f"{load_date} {load_time}"

        return {
            "load_num": self._get_first(row, ["LoadNumber"]),
            "cart_id": self._extract_cart_code_from_bridge_id_or_file(row),
            "weight": self._safe_decimal(self._get_first(row, ["Weight"])),
            "truck": self._get_first(row, ["TruckID", "Truck"]),
            "dest": self._get_first(row, ["Destination", "Dest"]),
            "moisture": self._safe_decimal(self._get_first(row, ["Moisture", "MeasuredMoisture"])),
            "comment": self._get_first(row, ["Comment", "Comments"]),
            "test_weight": self._safe_decimal(self._get_first(row, ["TestWeight", "Test Weight"])),
            "wet": self._safe_decimal(self._get_first(row, ["WetBushels", "Wet"])),
            "dry": self._safe_decimal(self._get_first(row, ["DryBushels", "Dry"])),
            "variety": self._get_first(row, ["Variety"]),
            "date": combined_dt or load_date,
            "load_cell": self._get_first(row, ["LoadCellCAL", "LoadCell", "Load Cell"]),
            "raw": row,
        }

    # ------------------------------------------------------------------
    # Response helpers
    # ------------------------------------------------------------------
    def _extract_summary_items(self, payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        for key in ("GrainCart", "GrainCarts", "Items", "Result", "results", "items"):
            value = payload.get(key)
            if isinstance(value, list):
                return value

        for outer_val in payload.values():
            if isinstance(outer_val, dict):
                for key in ("GrainCart", "GrainCarts", "Items", "Result", "results", "items"):
                    value = outer_val.get(key)
                    if isinstance(value, list):
                        return value

        return []

    # ------------------------------------------------------------------
    # Utility helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _normalize_path(path: str) -> str:
        if not path.startswith("/"):
            return "/" + path
        return path

    @staticmethod
    def _unix_timestamp() -> str:
        return str(int(time.time()))

    @staticmethod
    def _safe_int(value: Any) -> Optional[int]:
        if value in (None, "", "null"):
            return None
        try:
            return int(str(value).strip())
        except Exception:
            return None

    @staticmethod
    def _safe_decimal(value: Any) -> Optional[float]:
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

    @staticmethod
    def _get_first(data: Dict[str, Any], keys: List[str]) -> Any:
        for key in keys:
            if key in data and data[key] not in (None, ""):
                return data[key]
        return None


def pretty_print_json(data: Any) -> None:
    print(json.dumps(data, indent=2, default=str))


if __name__ == "__main__":
    client = SlingshotClient()

    print("Testing /accesskey ...")
    pretty_print_json(client.get_access_key_summary())

    print("\nListing first page of grain cart files ...")
    summary = client.list_graincart_files(page=1, pagesize=5)
    pretty_print_json(summary)

    items = client._extract_summary_items(summary)
    if not items:
        print("\nNo grain cart files found.")
    else:
        first = items[0]
        first_id = int(first["ID"])
        first_name = first.get("Name")

        print(f"\nDownloading and parsing original GRC file for ID={first_id} ...")
        parsed = client.get_parsed_graincart_file(first_id, file_name=first_name)
        pretty_print_json(parsed)
