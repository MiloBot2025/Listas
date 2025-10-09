import json, os
from datetime import datetime
from zoneinfo import ZoneInfo

kind = os.getenv("KIND", "stock")   # "stock" | "prices"
force = os.getenv("INPUT_FORCE", "false").lower() == "true"
if force:
    print("FRESH=1"); raise SystemExit(0)

meta_path = "docs/data/meta.json"
if not os.path.exists(meta_path):
    print("FRESH=1"); raise SystemExit(0)

with open(meta_path, "r", encoding="utf-8") as f:
    meta = json.load(f)

key = "last_update_stock" if kind == "stock" else "last_update_db"
val = meta.get(key)

if not val:
    print("FRESH=1"); raise SystemExit(0)

ar = datetime.now(ZoneInfo("America/Argentina/Buenos_Aires")).date()
try:
    d = datetime.fromisoformat(val).astimezone(ZoneInfo("America/Argentina/Buenos_Aires")).date()
except Exception:
    print("FRESH=1"); raise SystemExit(0)

print("FRESH=1" if d != ar else "FRESH=0")
