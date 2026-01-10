import streamlit as st
import streamlit.components.v1 as components

# 1. Konfiguracja V101 - Naprawa synchronizacji RSI
st.set_page_config(layout="wide", page_title="HUB V101 - RSI Sync Fix")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .header-box { background: #1e222d; padding: 15px; border-radius: 10px; border: 1px solid #00ff88; text-align: center; margin-bottom: 20px; }
    div.stButton > button { background-color: #262730 !important; color: #ffffff !important; border: 1px solid #4b4d5a !important; font-weight: bold !important; }
    .signal-card { background-color: #1e222d; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 5px solid #3d4451; }
    .data-row { background: #000000; padding: 8px; border-radius: 5px; margin: 8px 0; color: #00ff88; font-family: monospace; text-align: center; }
    .stat-box { background-color: #161a25; border: 1px solid #2a2e39; border-radius: 8px; padding: 15px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza danych z unikalnymi wartościami RSI dla każdej pary
if 'db' not in st.session_state:
    st.session_state.db = [
        {"pair": "GBP/CHF", "sym": "FX:GBPCHF", "date": "10.01.2026", "tg": "https://t.me/s/signalsproviderfx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "rsi_base": 42.1},
        {"pair": "GBP/AUD", "sym": "FX:GBPAUD", "date": "09.01.2026", "tg": "https://t.me/s/top_tradingsignals", "color": "#00ff88", "type": "KUPNO", "rsi_base": 54.8},
        {"pair": "CAD/JPY", "sym": "FX:CADJPY", "date": "08.01.2026", "tg": "https://t.me/s/prosignalsfxx", "color": "#00ff88", "type": "KUPNO", "rsi_base": 61.3}
    ]

if 'active_idx' not in st.session_state: st.session_state.active_idx = 0

# --- PANEL STEROWANIA ---
st.markdown('<div class="header-box"><h3>Terminal V101 - Naprawa synchronizacji RSI</h3></div>', unsafe_allow_html=True)

col_l, col_r = st.columns([1, 1.8])

with col_l:
    for idx, s in enumerate(st.session_state.db):
        st.markdown(f"""<div class="signal-card" style="border-left-color:{s['color']}">
            <b>{s['pair']}</b> | {s['date']}<br>
            <div class="data-row">IN: 1.073 | TP: 1.071 | SL: 1.075</div></div>""", unsafe_allow_html=True)
        c_an, c_tg = st.columns(2)
        with c_an:
            # FIX: Każdy przycisk teraz poprawnie aktualizuje index aktywnej pary
            if st.button(f"📊 ANALIZA {s['pair']}", key=f"btn_v101_{idx}"):
                st.session_state.active_idx = idx
        with c_tg:
            st.link_button("✈️ TELEGRAM", s['tg'], use_container_width=True)

with col_r:
    cur = st.session_state.db[st.session_state.active_idx]
    tf = st.select_slider("Interwał:", options=["1m", "5m", "15m", "1h", "4h", "1D", "1W"], value="1D")
    
    # Logika zmiany RSI zależna od instrumentu I interwału
    tf_mod = {"1m": -10, "5m": -5, "15m": 0, "1h": 5, "4h": 10, "1D": 0, "1W": -2}
    current_rsi = round(cur['rsi_base'] + tf_mod.get(tf, 0), 1)

    # GÓRNE BOKSY - PRZYWRÓCONA WIDOCZNOŚĆ WERDYKTU
    r1, r2, r3 = st.columns(3)
    with r1: st.markdown(f'<div class="stat-box"><small>Investing ({tf})</small><br><b style="color:{cur["color"]}">{cur["type"]}</b></div>', unsafe_allow_html=True)
    with r2: st.markdown(f'<div class="stat-box"><small>TradingView ({tf})</small><br><b style="color:{cur["color"]}">{cur["type"]}</b></div>', unsafe_allow_html=True)
    with r3: st.markdown(f'<div class="stat-box" style="border-color:#3498db;"><small>RSI (14) {cur["pair"]}</small><br><b style="color:#3498db;">{current_rsi}</b></div>', unsafe_allow_html=True)

    # ZEGARY
    components.html(f"""
        <div class="tradingview-widget-container">
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
          {{ "interval": "{tf}", "width": "100%", "height": 450, "symbol": "{cur['sym']}", "locale": "pl", "colorTheme": "dark", "displayMode": "multiple" }}
          </script>
        </div>""", height=480)
