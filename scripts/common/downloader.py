import os, requests
from pathlib import Path

def ensure_dir(p): Path(p).mkdir(parents=True, exist_ok=True)

def http_download(url: str, out_path: str, headers: dict | None = None) -> str:
    ensure_dir(os.path.dirname(out_path))
    with requests.get(url, headers=headers or {}, stream=True, timeout=120) as r:
        r.raise_for_status()
        with open(out_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024*1024):
                if chunk: f.write(chunk)
    return out_path
