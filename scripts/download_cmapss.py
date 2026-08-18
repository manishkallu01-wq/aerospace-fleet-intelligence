"""Download NASA C-MAPSS source data for local development.

The exact source URL can be supplied with CMAPSS_URL so the repository does
not hard-code a mirror that may change over time.
"""
import os
from pathlib import Path
from urllib.request import urlretrieve

url = os.getenv("CMAPSS_URL")
if not url:
    raise SystemExit("Set CMAPSS_URL to the NASA C-MAPSS download URL before running.")

out = Path("data/raw/cmapss_source.zip")
out.parent.mkdir(parents=True, exist_ok=True)
urlretrieve(url, out)
print(f"Downloaded source archive to {out}")
