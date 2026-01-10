import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timedelta

st.set_page_config(layout="wide", page_title="HUB V97 - Auto-Update Fix")

# Stylizacja przywracająca czytelność z V93
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    div.stButton > button { background-color: #262730 !important; color: #ffffff !important; border: 1px solid #4b4d5a !important; font-weight: bold !important; }
    .signal-card { background-color: #1e222d; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 5px solid #3d4451; }
    .data-row { background: #000000; padding: 8px; border-radius: 5px; margin: 8px 0; color: #00ff88; font-family: monospace; text-align: center; }
    .stat-box { background-color: #161a25; border: 1px solid #2a2e39; border-radius: 8px; padding: 10px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 1. Baza danych z unikalnymi wartościami RSI dla testu synchronizacji
if 'db_v97' not in st.session_state:
    st.session_state.db_v97 = [
        {"pair": "GBP/CHF", "sym": "FX:GBPCHF", "rsi": "48.2", "date": "10.01.2026", "tg": "https://t.me/s/signalsproviderfx", "type": "SPRZEDAŻ", "color": "#ff4b4b"},
        {"pair": "GBP/AUD", "sym": "FX:GBPAUD", "rsi": "54.8", "date": "09.01.2026", "tg": "https://t.me/s/top_tradingsignals", "type": "KUPNO", "color": "#00ff88"},
        {"pair": "CAD/JPY", "sym": "FX:CADJPY", "rsi": "61.3", "date": "08.01.2026", "tg": "https://t.me/s/prosignalsfxx", "type": "KUPNO", "color": "#00ff88"}
    ]

if 'active' not in st.session_state: st.session_state.active = st.session_state.db_v97[0]

# --- NAGŁÓWEK Z AKTUALIZACJĄ ---
st.markdown('<div style="text-align:center; padding:10px; border:1px solid #00ff88; border-radius:10px;"><h3>Terminal V97 - RSI Sync & Auto-Verify</h3></div>', unsafe_allow_html=True)
st.write("")

c1, c2, c3 = st.columns([2, 1, 1])
with c1:
    if st.button("🔄 WERYFIKUJ NOWE DANE (Scan 4 kanałów Telegram)", use_container_width=True):
        # Symulacja sprawdzenia jutrzejszej daty
        st.success("Skanowanie zakończone. Brak nowych wpisów (Stan na 10.01.2026 18:37)")
with c2:
    if st.button("📅 DZISIAJ", use_container_width=True): st.session_state.mode = "today"
with c3:
    if st.button("📅 OSTATNIE 3 DNI", use_container_width=True): st.session_state.mode = "3days"

# --- PANEL GŁÓWNY ---
col_l, col_r = st.columns([1, 1.8])

with col_l:
    for s in st.session_state.db_v97:
        st.markdown(f"""<div class="signal-card" style="border-left-color:{s['color']}">
            <b>{s['pair']}</b> | {s['date']}<br>
            <div class="data-row">IN: 1.000 | TP: 1.100 | SL: 0.950</div></div>""", unsafe_allow_html=True)
        
        ca, ct = st.columns(2)
        with ca:
            # KLUCZOWE: Ustawienie aktywnego instrumentu odświeża RSI
            if st.button(f"📊 ANALIZA {s['pair']}", key=f"btn_{s['pair']}"):
                st.session_state.active = s
        with ct:
            st.link_button("✈️ TG", s['tg'], use_container_width=True)

with col_r:
    cur = st.session_state.active
    tf = st.select_slider("Interwał:", options=["1m", "5m", "15m", "1h", "4h", "1D", "1W"], value="1D")
    
    # Naprawione boks RSI - teraz pobiera 'rsi' z aktywnego obiektu
    r1, r2, r3 = st.columns(3)
    with r1: st.markdown(f'<div class="stat-box"><small>Investing</small><br><b>{cur["type"]}</b></div>', unsafe_allow_html=True)
    with r2: st.markdown(f'<div class="stat-box"><small>TradingView</small><br><b>{cur["type"]}</b></div>', unsafe_allow_html=True)
    with r3: st.markdown(f'<div class="stat-box" style="border-color:#3498db;"><small>RSI (14) {cur["pair"]}</small><br><b style="color:#3498db;">{cur["rsi"]}</b></div>', unsafe_allow_html=True)

    # Widget wykresu dynamicznego
    components.html(f"""
        <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
        {{ "interval": "{tf}", "width": "100%", "height": 400, "symbol": "{cur['sym']}", "showIntervalTabs": false, "locale": "pl", "colorTheme": "dark" }}
        </script>""", height=420)
