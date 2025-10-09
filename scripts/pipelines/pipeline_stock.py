import os, yaml, shutil
from datetime import datetime
from zoneinfo import ZoneInfo

from scripts.common.excelio import write_stock_xlsx
from scripts.common.jsonio import meta_update, now_ar_iso
from scripts.common.hashio import load_last_hash, save_hash

from scripts.providers import tevelam, disco, imsa, ars

CONF = yaml.safe_load(open("config/providers.yml","r",encoding="utf-8"))
OUTS = yaml.safe_load(open("config/outputs.yml","r",encoding="utf-8"))

INPUTS_DIR = "inputs/stock"
AR = ZoneInfo("America/Argentina/Buenos_Aires")
def ts(fmt): return datetime.now(AR).strftime(fmt)

def prov_dir(p):
    d = os.path.join(INPUTS_DIR, p.upper()); os.makedirs(d, exist_ok=True); return d

def process_one(name, mod, cfg):
    print(f"\n== {name.upper()} ==")
    pdir = prov_dir(name)
    # descarga
    path, sha = mod.download_stock(cfg, pdir)
    print(f"descarga: {path}  sha={sha}")
    # hash gate
    last = load_last_hash("stock", name)
    if last and last == sha:
        print("hash igual → skip")
        return (0,0)
    # latest source
    latest_src = os.path.join(INPUTS_DIR, f"{name.upper()}_latest_source.xlsx")
    shutil.copyfile(path, latest_src)
    # extraer y filtrar (solo 2/5)
    rows = [r for r in mod.extract_stock(latest_src, cfg) if r["stock"] in (2,5)]
    if not rows:
        print("0 filas (2/5)")
        save_hash("stock", name, sha); return (0,0)
    # escribir xlsx timestamp + latest público
    pattern = OUTS["stock"]["per_provider_pattern"].replace("{PROV}", name.upper())
    out_ts = datetime.now(AR).strftime(pattern)
    write_stock_xlsx(rows, out_ts)

    latest_pub = OUTS["stock"]["latest_public_path"].replace("{PROV}", name.upper())
    os.makedirs(os.path.dirname(latest_pub), exist_ok=True)
    write_stock_xlsx(rows, latest_pub)

    # opcional JSON per proveedor
    if OUTS["stock"].get("write_json_per_provider", True):
        import json
        jdir = OUTS["stock"]["json_public_dir"]; os.makedirs(jdir, exist_ok=True)
        with open(f"{jdir}/{name.lower()}.json","w",encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, indent=2)

    save_hash("stock", name, sha)
    c5 = sum(1 for r in rows if r["stock"]==5); c2 = len(rows) - c5
    print(f"escrito: {latest_pub}  filas={len(rows)} (5={c5}, 2={c2})")
    return (c5, c2)

def main():
    total5 = total2 = 0
    for name, mod in [("tevelam", tevelam), ("disco", disco), ("imsa", imsa), ("ars", ars)]:
        try:
            c5, c2 = process_one(name, mod, CONF[name]["stock"])
            total5 += c5; total2 += c2
        except Exception as e:
            print(f"[WARN] {name}: {e}")

    # actualizar meta (solo claves de stock)
    meta_path = OUTS["meta"]["path"]
    meta_update(meta_path, {
        "last_update_stock": now_ar_iso(),
        "counts": { "con_stock": total5, "bajo": total2 }
    })
    print(f"\n[STOCK] 5={total5} 2={total2}")

if __name__ == "__main__":
    main()
