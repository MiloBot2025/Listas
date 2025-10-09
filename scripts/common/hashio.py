import os, json, hashlib
from datetime import datetime
from zoneinfo import ZoneInfo

BASE = "state/hashdb"

def _path(kind, provider):
    d = os.path.join(BASE, kind); os.makedirs(d, exist_ok=True)
    return os.path.join(d, f"{provider.lower()}.json")

def sha256_of_file(path, block=1048576):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(block), b""): h.update(chunk)
    return h.hexdigest()

def load_last_hash(kind, provider):
    p = _path(kind, provider)
    if not os.path.exists(p): return None
    with open(p, "r", encoding="utf-8") as f: return json.load(f).get("sha256")

def save_hash(kind, provider, sha):
    p = _path(kind, provider)
    with open(p, "w", encoding="utf-8") as f:
        json.dump({"sha256": sha, "updated": datetime.now(ZoneInfo("America/Argentina/Buenos_Aires")).isoformat()}, f, ensure_ascii=False, indent=2)
