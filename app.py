# app.py
# ==================================================
# Eldwin – Market Mood (FINAL / HTML STABLE)
# ==================================================

import time
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
# PURE HTML RENDER (NO STREAMLIT MARKDOWN)
# --------------------------------------------------

html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
html, body {{
    margin: 0;
    padding: 0;
    background: #ffffff;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}}

.container {{
    width: 100%;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}}

.card {{
    width: 360px;
    text-align: center;
}}

.title {{
    font-size: 30px;
    font-weight: 500;
    color: #4A6FA5;
}}

.subtitle {{
    margin-top: 6px;
    font-size: 13px;
    color: #6f6f6f;
}}

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

.orb {{
    margin: 28px auto;
}}

.orb video {{
    width: 260px;
    border-radius: 50%;
    object-fit: cover;
}}

.mood {{
    font-size: 20px;
    font-weight: 500;
    color: {mood_color};
}}

.sub {{
    margin-top: 6px;
    font-size: 14px;
    color: #7a7a7a;
}}

.pill {{
    display: inline-block;
    margin-top: 18px;
    padding: 12px 22px;
    background: #EEF4FA;
    border-radius: 999px;
    font-size: 15px;
    color: #355C7D;
}}

.footer {{
    margin-top: 20px;
    font-size: 11px;
    color: #9a9a9a;
}}
</style>
</head>

<body>
<div class="container">
    <div class="card">

        <div class="title">Eldwin</div>

        <div class="subtitle">
            Market mood · Live <span class="live-dot"></span>
        </div>

        <div class="orb">
            <video autoplay muted loop playsinline>
                <source src="{media_path}" type="video/webm">
            </video>
        </div>

        <div class="mood">{mood_title}</div>
        <div class="sub">{mood_sub}</div>

        <div class="pill">Eldwin Index · {int(score)} / 100</div>

        <div class="footer">
            Live data — Europe session · Updated {updated_seconds}s ago
        </div>

    </div>
</div>
</body>
</html>
"""

components.html(html, height=700)
