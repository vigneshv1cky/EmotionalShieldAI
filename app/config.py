from __future__ import annotations
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///tradefit.db")


# --- Bankroll policy (internal only) ---
def _get_bool(name: str, default: bool) -> bool:
    v = os.getenv(name)
    if v is None:
        return default
    return v.strip().lower() in {"1", "true", "yes", "y"}


BANKROLL_BASE_PCT = float(os.getenv("BANKROLL_BASE_PCT", 0.1))  # base fraction
BANKROLL_MIN_PCT = float(os.getenv("BANKROLL_MIN_PCT", 0.1))  # clamp min
BANKROLL_MAX_PCT = float(os.getenv("BANKROLL_MAX_PCT", 0.1))  # clamp max
BANKROLL_HEALTH_SCALE = _get_bool("BANKROLL_HEALTH_SCALE", True)  # scale by health?
