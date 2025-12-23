# app.py
# ==================================================
# Eldwin – Market Mood (Premium UI – Photo 8 Match)
# ==================================================

import time
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from utils import compute_eldwin_score, safe_float, score_to_media

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Eldwin",
    page_icon="🟢",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --------------------------------------------------
# AUTO REFRESH (1 MINUTE)
# --------------------------------------------------

REFRESH_SECONDS = 60
st_autorefresh(interval=REFRESH_SECONDS * 1000, key="eldwin_refresh")

# --------------------------------------------------
# COMPUTE SCORE
# --------------------------------------------------

result = compute_eldwin_score(lookback_days=60, use_demo=False)
score = safe_float(result.get("score", 50.0), 50.0)
media_path = score_to_media(score)
updated_seconds = int(time.time() - result.get("timestamp", time.time()))

# --------------------------------------------------
# TEXT LOGIC
# --------------------------------------------------

if score < 20:
    mood_title = "Markets appear unusually calm."
    mood_sub = "Very low stress environment"
    mood_color = "#7FBF7F"
elif score < 40:
    mood_title = "Markets are stable."
    mood_sub = "Normal risk conditions"
    mood_color = "#9BCB7A"
elif score < 60:
    mood_title = "Markets are tense."
    mood_sub = "Rising uncertainty"
    mood_color = "#E0B36A"
elif score < 80:
    mood_title = "Markets are stressed."
    mood_sub = "High risk environment"
    mood_color = "#E58B6B"
else:
    mood_title = "Markets are under pressure."
    mood_sub = "Extreme stress conditions"
    mood_color = "#D96A6A"

# --------------------------------------------------
# GLOBAL CSS (NO SCROLL, WHITE, PREMIUM)
# --------------------------------------------------

st.markdown(
    f"""
    <style>
    html, body, [data-testid="stApp"] {{
        background: #ffffff;
        height: 100%;
        overflow: hidden;
        color: #000;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}

    #MainMenu, footer, header {{
        visibility: hidden;
    }}

    .block-container {{
        max-width: 420px;
        height: 100vh;
        padding: 0;
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: center;
    }}

    /* Pulsing live dot */
    .live-dot {{
        display: inline-block;
        width: 8px;
        height: 8px;
        background: #4CAF50;
        border-radius: 50%;
        margin-left: 6px;
        animation: pulse 1.5s infinite;
    }}

    @keyframes pulse {{
        0% {{ opacity: 1; }}
        50% {{ opacity: 0.3; }}
        100% {{ opacity: 1; }}
    }}

    /* Orb video */
    .orb {{
        width: 260px;
        margin: 28px auto;
        transition: opacity 0.6s ease-in-out;
    }}

    .orb video {{
        width: 100%;
        border-radius: 50%;
        object-fit: cover;
        pointer-events: none;
    }}

    /* Index pill */
    .pill {{
        display: inline-block;
        padding: 12px 22px;
        background: #EEF4FA;
        border-radius: 999px;
        font-size: 15px;
        color: #355C7D;
        margin-top: 18px;
    }}

    .footer {{
        margin-top: 22px;
        font-size: 11px;
        color: #9a9a9a;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# HTML STRUCTURE
# --------------------------------------------------

st.markdown(
    f"""
    <div>
        <div style="font-size:30px; font-weight:500; color:#4A6FA5;">
            Eldwin
        </div>

        <div style="margin-top:6px; font-size:13px; color:#6f6f6f;">
            Market mood · Live <span class="live-dot"></span>
        </div>

        <div class="orb">
            <video autoplay muted loop playsinline>
                <source src="{media_path}" type="video/webm">
            </video>
        </div>

        <div style="font-size:20px; font-weight:500; color:{mood_color};">
            {mood_title}
        </div>

        <div style="margin-top:6px; font-size:14px; color:#7a7a7a;">
            {mood_sub}
        </div>

        <div class="pill">
            Eldwin Index · {int(score)} / 100
        </div>

        <div class="footer">
            Live data — Europe session · Updated {updated_seconds}s ago
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
