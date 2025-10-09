import json, os
from datetime import datetime
from zoneinfo import ZoneInfo

def read_json(path, default):
    if not os.path.exists(path): return default
    with open(path, "r", encoding="utf-8") as f: return json.load(f)

def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def now_ar_iso():
    return datetime.now(ZoneInfo("America/Argentina/Buenos_Aires")).isoformat()

def meta_update(path, patch: dict):
    meta = read_json(path, {})
    meta.update(patch)
    write_json(path, meta)
