


# ╭──────────────────────────────────────────────────────────────╮
# │ File: src/utils/timezone.py                                  │
# │ Module: timezone                                            │
# │ Doel: Helpermodule voor tijdstempel-formattering           │
# │ Auteur: DeveloperGPT                                        │
# │ Laatste wijziging: 2025-07-04                               │
# │ Status: stable                                              │
# ╰──────────────────────────────────────────────────────────────╯

from datetime import datetime, timezone, timedelta
try:
    # Python 3.9+ standaard
    from zoneinfo import ZoneInfo
except ImportError:
    # Fallback: gebruik timezone-functie
    ZoneInfo = None

def format_cet_ts(utc_ts: float) -> str:
    """
    🧠 Functie: format_cet_ts
    Converteert een UNIX-timestamp (UTC) naar ISO8601-string met CET+02:00 offset.

    ▶️ In:
        - utc_ts (float): seconds since epoch in UTC
    ⏺ Out:
        - str: ISO-format string, b.v. '2021-06-23T16:44:00+02:00'

    💡 Gebruikt:
        - datetime, ZoneInfo of timezone
    """
    # 🔹 Maak datetime in UTC
    dt_utc = datetime.fromtimestamp(utc_ts, tz=timezone.utc)
    # 🔹 Converteer naar CET
    if ZoneInfo:
        cet = ZoneInfo("Europe/Amsterdam")
    else:
        cet = timezone(timedelta(hours=2))
    dt_cet = dt_utc.astimezone(cet)
    # 🔹 Retourneer ISO string met offset
    return dt_cet.isoformat()
