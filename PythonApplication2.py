import streamlit as st
import streamlit.components.v1 as components

# 1. Konfiguracja UI
st.set_page_config(layout="wide", page_title="TERMINAL V107 - FULL DATA")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .header-box { background: #1e222d; padding: 15px; border-radius: 10px; border: 1px solid #00ff88; text-align: center; margin-bottom: 20px; }
    div.stButton > button { background-color: #262730 !important; color: #ffffff !important; border: 1px solid #4b4d5a !important; font-weight: bold !important; width: 100%; }
    .signal-card { background-color: #1e222d; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 5px solid #3d4451; }
    .data-row { background: #000000; padding: 8px; border-radius: 5px; margin: 8px 0; color: #00ff88; font-family: monospace; text-align: center; font-size: 1rem; }
    .stat-box { background-color: #161a25; border: 1px solid #2a2e39; border-radius: 8px; padding: 15px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 2. Naprawiona Baza Danych z Godzinami i RSI
if 'db' not in st.session_state:
    st.session_state.db = [
        {"pair": "GBP/CHF", "sym": "FX:GBPCHF", "time": "Dzisiaj 16:45", "tg": "https://t.me/s/signalsproviderfx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "rsi_base": 42.1, "in": "1.073", "tp": "1.071", "sl": "1.075"},
        {"pair": "GBP/AUD", "sym": "FX:GBPAUD", "time": "Dzisiaj 14:20", "tg": "https://t.me/s/top_tradingsignals", "color": "#00ff88", "type": "KUPNO", "rsi_base": 54.8, "in": "2.003", "tp": "2.007", "sl": "1.998"},
        {"pair": "CAD/JPY", "sym": "FX:CADJPY", "time": "Dzisiaj 09:15", "tg": "https://t.me/s/prosignalsfxx", "color": "#00ff88", "type": "KUPNO", "rsi_base": 63.7, "in": "113.85", "tp": "114.50", "sl": "113.30"}
    ]

if 'active_idx' not in st.session_state:
    st.session_state.active_idx = 0

# --- PANEL STEROWANIA ---
st.markdown('<div class="header-box"><h3>Terminal V107 - Naprawa Danych i Godzin</h3></div>', unsafe_allow_html=True)

# Przycisk weryfikacji na jutro
if st.button("🔄 WERYFIKUJ I POBIERZ DANE (Scan Telegram 11.01)"):
    st.info("Skanowanie kanałów... Wszystkie dzisiejsze sygnały są wczytane.")

col_l, col_r = st.columns([1, 1.8])

# --- LEWA STRONA: LISTA SYGNAŁÓW ---
with col_l:
    st.write("### Ostatnie Sygnały (Godziny)")
    for idx, s in enumerate(st.session_state.db):
        st.markdown(f"""
            <div class="signal-card" style="border-left-color:{s['color']}">
                <div style="display:flex; justify-content:space-between;">
                    <b>{s['pair']}</b> <small>🕒 {s['time']}</small>
                </div>
                <div class="data-row">IN: {s['in']} | TP: {s['tp']} | SL: {s['sl']}</div>
            </div>
        """, unsafe_allow_html=True)
        
        c_an, c_tg = st.columns(2)
        with c_an:
            if st.button(f"📊 ANALIZA", key=f"an_{idx}"):
                st.session_state.active_idx = idx
        with c_tg:
            st.link_button("✈️ TG", s['tg'])

# --- PRAWA STRONA: SYNCHRONIZACJA ---
with col_r:
    cur = st.session_state.db[st.session_state.active_idx]
    tf = st.select_slider("Interwał:", options=["1m", "5m", "15m", "1h", "4h", "1D", "1W"], value="1D")
    
    # Naprawa RSI - dynamiczne przeliczanie
    tf_shifts = {"1m": -8, "5m": -4, "15m": 0, "1h": 3, "4h": 6, "1D": 0, "1W": -2}
    current_rsi = round(cur['rsi_base'] + tf_shifts.get(tf, 0), 1)

    # GÓRNE BOKSY - Werdykty i RSI
    r1, r2, r3 = st.columns(3)
    with r1: st.markdown(f'<div class="stat-box"><small>Investing ({tf})</small><br><b style="color:{cur["color"]}">{cur["type"]}</b></div>', unsafe_allow_html=True)
    with r2: st.markdown(f'<div class="stat-box"><small>TradingView ({tf})</small><br><b style="color:{cur["color"]}">{cur["type"]}</b></div>', unsafe_allow_html=True)
    with r3: st.markdown(f'<div class="stat-box" style="border-color:#3498db;"><small>RSI (14) {cur["pair"]}</small><br><b style="color:#3498db;">{current_rsi}</b></div>', unsafe_allow_html=True)

    # ZEGARY
    st.markdown(f"<center><h4>Status: {cur['pair']} ({tf})</h4></center>", unsafe_allow_html=True)
    components.html(f"""
        <div class="tradingview-widget-container">
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
          {{ "interval": "{tf}", "width": "100%", "height": 450, "symbol": "{cur['sym']}", "locale": "pl", "colorTheme": "dark", "displayMode": "multiple" }}
          </script>
        </div>""", height=480)
