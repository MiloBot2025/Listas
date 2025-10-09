from datetime import datetime
from zoneinfo import ZoneInfo
import os

event = os.getenv("GITHUB_EVENT_NAME", "")
force = os.getenv("INPUT_FORCE", "false").lower() == "true"
if force:
    print("RUN=1"); raise SystemExit(0)

now = datetime.now(ZoneInfo("America/Argentina/Buenos_Aires"))
is_weekday = now.weekday() < 5      # 0-4 = lun-vie
in_window = 7 <= now.hour < 18      # 07:00–17:59
run = (event != "schedule") or (is_weekday and in_window)
print(f"RUN={'1' if run else '0'}")
