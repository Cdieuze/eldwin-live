# utils.py
# ==========================================
# Eldwin Live – Core computation & mappings
# ==========================================

from __future__ import annotations

import math
import time
from typing import Dict, Any

import numpy as np

# Optional live data
try:
    import yfinance as yf
except Exception:
    yf = None


# ------------------------------------------
# Helpers
# ------------------------------------------

def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def safe_float(x, default: float = 0.0) -> float:
    try:
        v = float(x)
        if math.isnan(v) or math.isinf(v):
            return default
        return v
    except Exception:
        return default


# ------------------------------------------
# Labels & colors
# ------------------------------------------

def score_to_label(score: float) -> str:
    s = clamp(score, 0, 100)

    if s < 10:
        return "Anesthetized 🫧"
    if s < 20:
        return "Very Calm 😌"
    if s < 30:
        return "Calm 🙂"
    if s < 40:
        return "Neutral ⚖️"
    if s < 50:
        return "Slight Tension 😐"
    if s < 60:
        return "Tense 😬"
    if s < 70:
        return "Stressed 🔥"
    if s < 80:
        return "High Stress 🚨"
    if s < 90:
        return "Extreme Stress 🧨"
    return "Panic ⚠️"


def score_to_color(score: float) -> str:
    """
    Green → Yellow → Red gradient
    """
    s = clamp(score, 0, 100)

    if s <= 50:
        t = s / 50
        r = int(0 + t * 255)
        g = int(200 + t * 20)
        b = int(80 - t * 80)
    else:
        t = (s - 50) / 50
        r = 255
        g = int(220 - t * 170)
        b = 0

    return f"#{r:02x}{g:02x}{b:02x}"


# ------------------------------------------
# MEDIA MAPPING (IMPORTANT)
# ------------------------------------------

def score_to_media(score: float) -> str:
    """
    Maps Eldwin score (0–100) to animation files:

    s0.webm → 0–10
    s1.webm → 10–20
    ...
    s9.webm → 90–100
    """
    s = clamp(score, 0, 100)
    index = int(s // 10)

    if index >= 10:
        index = 9

    return f"media/s{index}.webm"


# ------------------------------------------
# DEMO (offline-safe) inputs
# ------------------------------------------

def _demo_inputs() -> Dict[str, float]:
    t = time.time()

    wave1 = math.sin(t / 40)
    wave2 = math.sin(t / 13) * 0.4
    stress = clamp((wave1 + wave2 + 2) / 4, 0, 1)

    return {
        "vix": 12 + stress * 28,                      # 12 → 40
        "spx_ret_1d": math.sin(t / 9) * -0.004,       # ±0.4%
        "realized_vol": 0.12 + stress * 0.25,         # 12% → 37%
        "credit_stress": 0.2 + stress * 0.8,          # 0.2 → 1.0
        "risk_off": stress                            # 0 → 1
    }


# ------------------------------------------
# LIVE inputs (market proxies)
# ------------------------------------------

def _live_inputs(lookback_days: int) -> Dict[str, float] | None:
    if yf is None:
        return None

    try:
        vix = yf.download("^VIX", period="10d", progress=False)["Close"].dropna().iloc[-1]

        spy = yf.download(
            "SPY",
            period=f"{max(lookback_days, 60)}d",
            progress=False
        )["Close"].dropna()

        ret_1d = spy.pct_change().iloc[-1]
        realized_vol = spy.pct_change().tail(20).std() * math.sqrt(252)

        hyg = yf.download("HYG", period="60d", progress=False)["Close"].dropna()
        ief = yf.download("IEF", period="60d", progress=False)["Close"].dropna()

        credit_stress = clamp((ief.pct_change().mean() - hyg.pct_change().mean()) * 40 + 0.5, 0, 1)

        ma20 = spy.rolling(20).mean().iloc[-1]
        ma50 = spy.rolling(50).mean().iloc[-1]
        risk_off = clamp(1 - (ma20 / ma50), 0, 1)

        return {
            "vix": float(vix),
            "spx_ret_1d": float(ret_1d),
            "realized_vol": float(realized_vol),
            "credit_stress": float(credit_stress),
            "risk_off": float(risk_off),
        }

    except Exception:
        return None


# ------------------------------------------
# MAIN SCORE ENGINE
# ------------------------------------------

def compute_eldwin_score(
    lookback_days: int = 60,
    use_demo: bool = False
) -> Dict[str, Any]:

    if use_demo:
        data = _demo_inputs()
        mode = "demo"
    else:
        live = _live_inputs(lookback_days)
        if live is None:
            data = _demo_inputs()
            mode = "demo_fallback"
        else:
            data = live
            mode = "live"

    # Normalize stress components (0 → calm, 1 → panic)
    vix_s = clamp((data["vix"] - 10) / 30, 0, 1)
    vol_s = clamp((data["realized_vol"] - 0.10) / 0.30, 0, 1)
    ret_s = clamp((-data["spx_ret_1d"]) / 0.02, 0, 1)

    credit_s = clamp(data["credit_stress"], 0, 1)
    risk_off_s = clamp(data["risk_off"], 0, 1)

    weights = {
        "vix": 0.30,
        "vol": 0.25,
        "ret": 0.15,
        "credit": 0.20,
        "risk_off": 0.10,
    }

    stress = (
        weights["vix"] * vix_s
        + weights["vol"] * vol_s
        + weights["ret"] * ret_s
        + weights["credit"] * credit_s
        + weights["risk_off"] * risk_off_s
    )

    score = clamp(stress * 100, 0, 100)

    return {
        "score": score,
        "mode": mode,
        "inputs": data,
        "components": {
            "vix": vix_s,
            "vol": vol_s,
            "ret": ret_s,
            "credit": credit_s,
            "risk_off": risk_off_s,
        },
        "timestamp": time.time(),
    }
