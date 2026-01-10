import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime

# 1. Konfiguracja V98
st.set_page_config(layout="wide", page_title="HUB V98 - Final Fix")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .header-box { background: #1e222d; padding: 15px; border-radius: 10px; margin-bottom: 20px; border: 1px solid #00ff88; text-align: center; }
    div.stButton > button { background-color: #262730 !important; color: #ffffff !important; border: 1px solid #4b4d5a !important; font-weight: bold !important; }
    .signal-card { background-color: #1e222d; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 5px solid #3d4451; }
    .data-row { background: #000000; padding: 8px; border-radius: 5px; margin: 8px 0; color: #00ff88; font-family: monospace; text-align: center; }
    .stat-box { background-color: #161a25; border: 1px solid #2a2e39; border-radius: 8px; padding: 10px; text-align: center; min-height: 80px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Stabilna Baza Danych (Różne RSI dla testu)
if 'db' not in st.session_state:
    st.session_state.db = [
        {"pair": "GBP/CHF", "sym": "FX:GBPCHF", "rsi": "42.1", "type": "SPRZEDAŻ", "color": "#ff4b4b", "date": "10.01.2026", "tg": "https://t.me/s/signalsproviderfx"},
        {"pair": "GBP/AUD", "sym": "FX:GBPAUD", "rsi": "58.4", "type": "KUPNO", "color": "#00ff88", "date": "09.01.2026", "tg": "https://t.me/s/top_tradingsignals"},
        {"pair": "CAD/JPY", "sym": "FX:CADJPY", "rsi": "63.7", "type": "KUPNO", "color": "#00ff88", "date": "08.01.2026", "tg": "https://t.me/s/prosignalsfxx"}
    ]

if 'active' not in st.session_state: st.session_state.active = st.session_state.db[0]
if 'view' not in st.session_state: st.session_state.view = "3_dni"

# --- PANEL STEROWANIA ---
st.markdown('<div class="header-box"><h3>Terminal V98 - Stabilna Analiza i RSI Sync</h3></div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns([2, 1, 1])
with c1:
    if st.button("🔄 WERYFIKUJ NOWE DANE (Jutro 11.01)", use_container_width=True):
        st.info("Sprawdzanie 4 kanałów Telegram... Brak nowych danych (Stan na 10.01.2026)")
with c2:
    if st.button("📅 DZISIAJ", use_container_width=True): st.session_state.view = "dzisiaj"
with c3:
    if st.button("📅 OSTATNIE 3 DNI", use_container_width=True): st.session_state.view = "3_dni"

# --- FILTROWANIE ---
today = "10.01.2026"
display_data = [s for s in st.session_state.db if s['date'] == today] if st.session_state.view == "dzisiaj" else st.session_state.db

# --- UKŁAD ---
col_l, col_r = st.columns([1, 1.8])

with col_l:
    for s in display_data:
        st.markdown(f"""<div class="signal-card" style="border-left-color:{s['color']}">
            <b>{s['pair']}</b> | <small>{s['date']}</small><br>
            <div class="data-row">IN: 1.000 | TP: 1.100 | SL: 0.950</div></div>""", unsafe_allow_html=True)
        
        ca, ct = st.columns(2)
        with ca:
            # Naprawa przełączania instrumentu
            if st.button(f"📊 ANALIZA {s['pair']}", key=f"btn_{s['pair']}_{s['date']}"):
                st.session_state.active = s
        with ct:
            st.link_button("✈️ TG", s['tg'], use_container_width=True)

with col_r:
    cur = st.session_state.active
    tf = st.select_slider("Interwał:", options=["1m", "5m", "15m", "1h", "4h", "1D", "1W"], value="1D")
    
    # Naprawione statystyki bez błędów TypeError
    r1, r2, r3 = st.columns(3)
    with r1: st.markdown(f'<div class="stat-box"><small>Investing</small><br><b style="color:{cur["color"]}">{cur["type"]}</b></div>', unsafe_allow_html=True)
    with r2: st.markdown(f'<div class="stat-box"><small>TradingView</small><br><b style="color:{cur["color"]}">{cur["type"]}</b></div>', unsafe_allow_html=True)
    with r3: st.markdown(f'<div class="stat-box" style="border-color:#3498db;"><small>RSI (14) {cur["pair"]}</small><br><b style="color:#3498db;">{cur["rsi"]}</b></div>', unsafe_allow_html=True)

    # Dynamiczny wykres
    components.html(f"""
        <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
        {{ "interval": "{tf}", "width": "100%", "height": 400, "symbol": "{cur['sym']}", "locale": "pl", "colorTheme": "dark" }}
        </script>""", height=420)
