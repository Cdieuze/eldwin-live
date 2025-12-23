# app.py
# ==================================================
# Eldwin – Market Mood (FINAL – Stable & Correct)
# ==================================================

import time
import base64
from pathlib import Path

import streamlit as st
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as components

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
# AUTO REFRESH (60s)
# --------------------------------------------------

REFRESH_SECONDS = 60
st_autorefresh(interval=REFRESH_SECONDS * 1000, key="eldwin_refresh")

# --------------------------------------------------
# COMPUTE SCORE
# --------------------------------------------------

result = compute_eldwin_score(lookback_days=60, use_demo=False)
score = safe_float(result.get("score", 50.0), 50.0)
media_file = score_to_media(score)
updated_seconds = int(time.time() - result.get("timestamp", time.time()))

# --------------------------------------------------
# LOAD VIDEO AS BASE64 (CRITICAL FIX)
# --------------------------------------------------

video_bytes = Path(media_file).read_bytes()
video_base64 = base64.b64encode(video_bytes).decode("utf-8")

# --------------------------------------------------
# TEXT LOGIC
# --------------------------------------------------

if score < 20:
    mood_title = "Markets appear unusually calm."
    mood_sub = "Very low stress environment"
    mood_color = "#6FBF8A"
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
# PURE HTML (FULL PAGE, NO CARD)
# --------------------------------------------------

html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
html, body {{
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    background: #ffffff;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}}

.container {{
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
}}

.title {{
    font-size: 36px;
    font-weight: 500;
    color: #4A6FA5;
}}

.subtitle {{
    margin-top: 6px;
    font-size: 14px;
    color: #6f6f6f;
}}

.live-dot {{
    display: inline-block;
    width: 9px;
    height: 9px;
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

.orb {{
    margin: 36px 0;
}}

.orb video {{
    width: 300px;
    border-radius: 50%;
    object-fit: cover;
}}

.mood {{
    font-size: 24px;
    font-weight: 500;
    color: {mood_color};
}}

.sub {{
    margin-top: 6px;
    font-size: 16px;
    color: #7a7a7a;
}}

.pill {{
    margin-top: 22px;
    padding: 14px 26px;
    background: #EEF4FA;
    border-radius: 999px;
    font-size: 16px;
    color: #355C7D;
}}

.footer {{
    margin-top: 24px;
    font-size: 12px;
    color: #9a9a9a;
}}
</style>
</head>

<body>
<div class="container">

    <div class="title">Eldwin</div>
    <div class="subtitle">
        Market mood · Live <span class="live-dot"></span>
    </div>

    <div class="orb">
        <video autoplay muted loop playsinline>
            <source src="data:video/webm;base64,{video_base64}" type="video/webm">
        </video>
    </div>

    <div class="mood">{mood_title}</div>
    <div class="sub">{mood_sub}</div>

    <div class="pill">Eldwin Index · {int(score)} / 100</div>

    <div class="footer">
        Live data — Europe session · Updated {updated_seconds}s ago
    </div>

</div>
</body>
</html>
"""

components.html(html, height=900)
