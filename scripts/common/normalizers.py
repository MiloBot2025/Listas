def normalize_stock_026(x):
    s = str(x).strip().lower()
    if s in {"", "none", "na", "nan"}: return 0
    if s.replace(".", "", 1).isdigit():
        try:
            n = float(s); return 0 if n <= 0 else (6 if n >= 5 else 2)
        except: return 2
    if any(k in s for k in ["sin", "no", "agotado", "0"]): return 0
    if any(k in s for k in ["consult", "poco", "<5", "bajo"]): return 2
    if any(k in s for k in ["con", "sí", "si", "dispon", "stock", "alto"]): return 6
    return 2

def map_026_to_25(v):
    return 5 if v == 6 else (2 if v == 2 else None)
