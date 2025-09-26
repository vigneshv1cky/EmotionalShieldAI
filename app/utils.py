from __future__ import annotations
from typing import Optional
import numpy as np
from .config import (
    BANKROLL_BASE_PCT,
    BANKROLL_HEALTH_SCALE,
)

try:
    import yfinance as yf  # type: ignore

    _HAS_YF = True
except Exception:
    _HAS_YF = False


# --- Health & bankroll ---
def health_factor(sleep_hours: float, exercise_minutes: int) -> tuple[float, str, str]:
    # --- Sleep score ---
    if sleep_hours >= 7:
        s, s_note = 1.0, "Good Sleep"
    elif 5 <= sleep_hours < 7:
        s, s_note = 0.5, "Moderate Sleep"
    else:  # < 5
        s, s_note = 0.2, "Poor Sleep"

    # --- Exercise score ---
    if exercise_minutes < 60:
        e, e_note = 0.2, "Poor Exercise"
    elif 60 <= exercise_minutes < 90:
        e, e_note = 0.5, "Moderate Exercise"
    else:  # 90+
        e, e_note = 1.0, "Good Exercise"

    # --- Combine into category ---
    sleep_level = s_note
    exercise_level = e_note

    # --- Risk matrix ---
    risk_matrix = {
        "Poor Sleep": {
            "Poor Exercise": (
                "🔴 High Risk",
                "Judgment impaired, stress high, discipline weak — avoid trading.",
            ),
            "Moderate Exercise": (
                "🔴 High Risk",
                "Some physical balance, but fatigue dominates — high chance of costly mistakes.",
            ),
            "Good Exercise": (
                "🟠 Elevated Risk",
                "Good fitness helps, but poor rest still limits focus.",
            ),
        },
        "Moderate Sleep": {
            "Poor Exercise": (
                "🔴 High Risk",
                "Partial rest + inactivity = sluggish, reactive trading.",
            ),
            "Moderate Exercise": (
                "🟠 Moderate Risk",
                "Fair balance, but not peak performance — trade smaller size.",
            ),
            "Good Exercise": (
                "🟡 Caution",
                "Reasonable discipline, but not optimal endurance.",
            ),
        },
        "Good Sleep": {
            "Poor Exercise": (
                "🟠 Moderate Risk",
                "Rested mind, but low fitness = shorter stamina in volatile sessions.",
            ),
            "Moderate Exercise": (
                "🟡 Caution",
                "Balanced state, can trade cautiously with discipline.",
            ),
            "Good Exercise": (
                "🟢 Optimal",
                "Peak focus, strong discipline, reduced stress — ideal trading state.",
            ),
        },
    }

    # --- Trading guidance per alert ---
    trading_guidance = {
        "🟢 Optimal": "Conditions are favorable; trade normally within risk rules.",
        "🟡 Caution": "Conditions are decent; reduce position size slightly.",
        "🟠 Moderate Risk": "Conditions are mixed; reduce trade frequency and size.",
        "🟠 Elevated Risk": "Conditions are imbalanced; limit trades, be defensive.",
        "🔴 High Risk": "Avoid trading; risk of errors and emotional decisions is high.",
    }

    # Final factor = average of sleep & exercise, bounded [0.2, 1.0]
    f = max(0.2, min(1.0, (s + e) / 2))

    try:
        alert, description = risk_matrix[sleep_level][exercise_level]
        guidance = trading_guidance.get(alert, "")
    except KeyError:
        alert, description, guidance = "❓", "Unexpected combination.", ""

    return (
        f,
        f"{alert} | {description} (sleep={s_note}, exercise={e_note}, risk scale x{f:.2f})",
        alert,
        guidance,
    )


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
