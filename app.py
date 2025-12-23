# app.py
# ==========================================
# Eldwin Live – Full Screen Visual App
# ==========================================

import streamlit as st
from streamlit_autorefresh import st_autorefresh

from utils import (
    compute_eldwin_score,
    safe_float,
    score_to_label,
    score_to_color,
    score_to_media,
)

# ------------------------------------------
# PAGE CONFIG (FULL SCREEN / CLEAN)
# ------------------------------------------

st.set_page_config(
    page_title="Eldwin Live",
    page_icon="🟣",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ------------------------------------------
# AUTO REFRESH (every 15s)
# ------------------------------------------

REFRESH_SECONDS = 15
st_autorefresh(interval=REFRESH_SECONDS * 1000, key="eldwin_refresh")

# ------------------------------------------
# COMPUTE SCORE (LIVE with fallback)
# ------------------------------------------

result = compute_eldwin_score(
    lookback_days=60,
    use_demo=False,   # auto fallback if live fails
)

score = safe_float(result.get("score", 50.0), 50.0)
label = score_to_label(score)
color = score_to_color(score)
media_path = score_to_media(score)
mode = result.get("mode", "unknown")

# ------------------------------------------
# HIDE STREAMLIT UI (MAX IMMERSION)
# ------------------------------------------

st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------
# MAIN VISUAL (ANIMATION)
# ------------------------------------------

st.video(
    media_path,
    autoplay=True,
    loop=True,
)

# ------------------------------------------
# SCORE DISPLAY
# ------------------------------------------

st.markdown(
    f"""
    <div style="text-align:center; margin-top: -10px;">
        <div style="
            font-size: 56px;
            font-weight: 900;
            color: {color};
            line-height: 1;
        ">
            {score:.1f}
        </div>

        <div style="
            font-size: 16px;
            margin-top: 6px;
            opacity: 0.9;
        ">
            {label}
        </div>

        <div style="
            font-size: 11px;
            margin-top: 10px;
            opacity: 0.5;
        ">
            auto-refresh {REFRESH_SECONDS}s · mode: {mode}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------
# OPTIONAL: DISCLAIMER (VERY LIGHT)
# ------------------------------------------

st.markdown(
    """
    <div style="
        text-align:center;
        font-size:10px;
        opacity:0.35;
        margin-top:12px;
    ">
        Experimental market stress signal · Not investment advice
    </div>
    """,
    unsafe_allow_html=True,
)
