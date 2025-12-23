# app.py
# ==========================================
# Eldwin – Market Mood (Clean Final UI)
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
# FORCE LIGHT THEME + CLEAN UI
# ------------------------------------------

st.markdown(
    """
    <style>
    html, body, [class*="css"]  {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    #MainMenu, footer, header {
        visibility: hidden;
    }

    .block-container {
        max-width: 420px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Orb container */
    .orb-wrapper {
        width: 260px;
        height: 260px;
        margin: auto;
        border-radius: 50%;
        overflow: hidden;
        background: #ffffff;
    }

    video {
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 50%;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------
# AUTO REFRESH
# ------------------------------------------

REFRESH_SECONDS = 15
st_autorefresh(interval=REFRESH_SECONDS * 1000, key="eldwin_refresh")

# ------------------------------------------
# COMPUTE SCORE
# ------------------------------------------

result = compute_eldwin_score(lookback_days=60, use_demo=False)
score = safe_float(result.get("score", 50.0), 50.0)
media_path = score_to_media(score)

# ------------------------------------------
# DYNAMIC TEXT LOGIC
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
# TOP STATIC TEXT
# ------------------------------------------

st.markdown(
    """
    <div style="text-align:center;">
        <div style="font-size:26px; font-weight:500;">
            Eldwin
        </div>
        <div style="margin-top:6px; font-size:13px; color:#6b6b6b;">
            <span style="color:#9BCB7A;">●</span>
            Market mood · Live
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

# ------------------------------------------
# ORB VIDEO (CIRCULAR, CLEAN)
# ------------------------------------------

st.markdown("<div class='orb-wrapper'>", unsafe_allow_html=True)
st.video(media_path, autoplay=True, loop=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

# ------------------------------------------
# BOTTOM DYNAMIC TEXTS (SAFE HTML)
# ------------------------------------------

st.markdown(
    f"""
    <div style="text-align:center;">
        <div style="font-size:18px; font-weight:500;">
            {mood_title}
        </div>
        <div style="margin-top:6px; font-size:13px; color:#7a7a7a;">
            {mood_sub}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

# ------------------------------------------
# INDEX PILL
# ------------------------------------------

st.markdown(
    f"""
    <div style="text-align:center;">
        <span style="
            display:inline-block;
            padding:10px 18px;
            background:#f3f3f3;
            border-radius:999px;
            font-size:13px;
            color:#555;
        ">
            Eldwin Index {score:.0f}/100
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)
