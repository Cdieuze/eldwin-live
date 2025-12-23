# app.py
# ==========================================
# Eldwin – Market Mood (Centered / No Scroll)
# ==========================================

import streamlit as st
from streamlit_autorefresh import st_autorefresh

from utils import compute_eldwin_score, safe_float, score_to_media

# ------------------------------------------
# PAGE CONFIG
# ------------------------------------------

st.set_page_config(
    page_title="Eldwin",
    page_icon="🟢",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ------------------------------------------
# HARD RESET UI (WHITE ONLY, NO SCROLL)
# ------------------------------------------

st.markdown(
    """
    <style>
    html, body, [data-testid="stApp"] {
        background-color: #ffffff !important;
        color: #000000 !important;
        height: 100%;
        overflow: hidden;
    }

    #MainMenu, footer, header {
        visibility: hidden;
    }

    /* Center everything vertically */
    .block-container {
        max-width: 420px;
        height: 100vh;
        padding: 0;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    video {
        width: 220px;
        height: auto;
        margin: auto;
        border-radius: 0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------
# AUTO REFRESH (1 MINUTE)
# ------------------------------------------

REFRESH_SECONDS = 60
st_autorefresh(interval=REFRESH_SECONDS * 1000, key="eldwin_refresh")

# ------------------------------------------
# COMPUTE SCORE
# ------------------------------------------

result = compute_eldwin_score(lookback_days=60, use_demo=False)
score = safe_float(result.get("score", 50.0), 50.0)
media_path = score_to_media(score)

# ------------------------------------------
# DYNAMIC TEXTS
# ------------------------------------------

if score < 20:
    mood_title = "Markets are calm."
    mood_sub = "Low stress environment"
elif score < 40:
    mood_title = "Markets are stable."
    mood_sub = "Normal risk conditions"
elif score < 60:
    mood_title = "Markets are tense."
    mood_sub = "Rising uncertainty"
elif score < 80:
    mood_title = "Markets are stressed."
    mood_sub = "High risk environment"
else:
    mood_title = "Markets are under pressure."
    mood_sub = "Extreme stress conditions"

# ------------------------------------------
# CONTENT (COMPACT & CENTERED)
# ------------------------------------------

st.markdown(
    """
    <div style="text-align:center;">
        <div style="font-size:24px; font-weight:400;">
            Eldwin
        </div>
        <div style="margin-top:4px; font-size:12px; color:#7a7a7a;">
            <span style="color:#9BCB7A;">●</span>
            Market mood · Live
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

st.video(media_path, autoplay=True, loop=True)

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

st.markdown(
    f"""
    <div style="text-align:center;">
        <div style="font-size:16px; font-weight:400;">
            {mood_title}
        </div>
        <div style="margin-top:4px; font-size:12px; color:#7a7a7a;">
            {mood_sub}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

st.markdown(
    f"""
    <div style="text-align:center;">
        <span style="
            display:inline-block;
            padding:8px 16px;
            background:#f6f1ec;
            border-radius:999px;
            font-size:12px;
            color:#555;
        ">
            Eldwin Index {int(score)} / 100
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)
