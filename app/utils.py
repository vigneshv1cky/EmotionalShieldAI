from __future__ import annotations
from typing import Optional
import numpy as np
from .config import (
    BANKROLL_BASE_PCT,
    BANKROLL_MIN_PCT,
    BANKROLL_MAX_PCT,
    BANKROLL_HEALTH_SCALE,
)

try:
    import yfinance as yf  # type: ignore

    _HAS_YF = True
except Exception:
    _HAS_YF = False

# --- Health & bankroll ---


def health_factor(sleep_hours: float, exercise_minutes: int) -> tuple[float, str]:
    # Sleep score
    if sleep_hours >= 7:
        s, s_note = 1.0, "sleep optimal"
    elif 5 <= sleep_hours < 7:
        s, s_note = 0.5, "sleep slightly off"
    else:  # < 5
        s, s_note = 0.2, "sleep poor"

    # --- Exercise score (new rules) ---
    if exercise_minutes < 60:
        e, e_note = 0.2, "exercise poor"
    elif 60 <= exercise_minutes < 90:
        e, e_note = 0.5, "exercise good"
    else:  # 90+
        e, e_note = 1.0, "exercise best"

    # Final factor = average of sleep & exercise, bounded [0.2, 1.0]
    f = max(0.2, min(1.0, (s + e) / 2))
    return f, f"{s_note}; {e_note}. risk scaled x{f:.2f}"


def compute_dynamic_bankroll(
    total_value: float, h_factor: float
) -> tuple[float, float]:
    """
    Compute bankroll (amount, pct of total_value).
    - Start from BANKROLL_BASE_PCT
    - Optionally scale by health factor
    - Clamp to [BANKROLL_MIN_PCT, BANKROLL_MAX_PCT]
    """
    pct = BANKROLL_BASE_PCT
    if BANKROLL_HEALTH_SCALE:
        pct = pct * h_factor
    # pct = max(BANKROLL_MIN_PCT, min(BANKROLL_MAX_PCT, pct))
    amount = total_value * pct
    return amount, pct


# --- Market data & ATR ---


def fetch_price_and_atr(
    symbol: str, lookback: int
) -> tuple[Optional[float], Optional[float]]:
    if not _HAS_YF:
        return None, None
    try:
        hist = yf.Ticker(symbol).history(period="6mo")
        if hist.empty:
            return None, None
        highs = hist["High"].to_numpy()
        lows = hist["Low"].to_numpy()
        closes = hist["Close"].to_numpy()
        prev_close = np.roll(closes, 1)
        prev_close[0] = closes[0]
        tr = np.maximum(
            highs - lows,
            np.maximum(np.abs(highs - prev_close), np.abs(lows - prev_close)),
        )
        if len(tr) < lookback:
            return float(closes[-1]), None
        atr = float(np.mean(tr[-lookback:]))
        return float(closes[-1]), atr
    except Exception:
        return None, None
