import streamlit as st
import streamlit.components.v1 as components

# 1. Konfiguracja V100
st.set_page_config(layout="wide", page_title="HUB V100 - Dynamic Full Sync")

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

# 2. Baza danych z danymi zależnymi od interwału (Przykładowe RSI)
if 'db' not in st.session_state:
    st.session_state.db = [
        {"pair": "GBP/CHF", "sym": "FX:GBPCHF", "date": "10.01.2026", "tg": "https://t.me/s/signalsproviderfx", "color": "#ff4b4b", "type": "SPRZEDAŻ"},
        {"pair": "GBP/AUD", "sym": "FX:GBPAUD", "date": "09.01.2026", "tg": "https://t.me/s/top_tradingsignals", "color": "#00ff88", "type": "KUPNO"},
        {"pair": "CAD/JPY", "sym": "FX:CADJPY", "date": "08.01.2026", "tg": "https://t.me/s/prosignalsfxx", "color": "#00ff88", "type": "KUPNO"}
    ]

if 'active' not in st.session_state: st.session_state.active = st.session_state.db[0]

# --- PANEL STEROWANIA ---
st.markdown('<div class="header-box"><h3>Terminal V100 - Pełna Synchronizacja Interwałów</h3></div>', unsafe_allow_html=True)

if st.button("🔄 WERYFIKUJ I POBIERZ NOWE DANE (Skanowanie 11.01)", use_container_width=True):
    st.success("Skanowanie kanałów... Jutro tutaj pojawią się nowe sygnały.")

col_l, col_r = st.columns([1, 1.8])

with col_l:
    for s in st.session_state.db:
        st.markdown(f"""<div class="signal-card" style="border-left-color:{s['color']}">
            <b>{s['pair']}</b> | {s['date']}<br>
            <div class="data-row">IN: 1.073 | TP: 1.071 | SL: 1.075</div></div>""", unsafe_allow_html=True)
        c_an, c_tg = st.columns(2)
        with c_an:
            if st.button(f"📊 ANALIZA", key=f"an_{s['pair']}_{s['date']}"):
                st.session_state.active = s
        with c_tg:
            st.link_button("✈️ TELEGRAM", s['tg'], use_container_width=True)

with col_r:
    cur = st.session_state.active
    # SUWAK WYMUSZAJĄCY ODŚWIEŻENIE
    tf = st.select_slider("Wybierz interwał dla całej analizy:", options=["1m", "5m", "15m", "1h", "4h", "1D", "1W"], value="1D")
    
    # Logika zmiany RSI i werdyktów zależnie od TF
    mock_rsi = {"1m": "32.1", "5m": "45.5", "15m": "51.2", "1h": "58.9", "4h": "62.3", "1D": "42.1", "1W": "38.5"}
    current_rsi = mock_rsi[tf] if cur['pair'] == "GBP/CHF" else "55.0"

    # GÓRNE BOKSY - NAPRAWA WIDOCZNOŚCI KIERUNKU
    r1, r2, r3 = st.columns(3)
    with r1: st.markdown(f'<div class="stat-box"><small>Investing ({tf})</small><br><b style="color:{cur["color"]}">{cur["type"]}</b></div>', unsafe_allow_html=True)
    with r2: st.markdown(f'<div class="stat-box"><small>TradingView ({tf})</small><br><b style="color:{cur["color"]}">{cur["type"]}</b></div>', unsafe_allow_html=True)
    with r3: st.markdown(f'<div class="stat-box" style="border-color:#3498db;"><small>RSI (14) {tf}</small><br><b style="color:#3498db;">{current_rsi}</b></div>', unsafe_allow_html=True)

    # ZEGYRY I WYKRESY
    st.markdown(f"<center><h4>Analiza techniczna: {cur['pair']} ({tf})</h4></center>", unsafe_allow_html=True)
    components.html(f"""
        <div class="tradingview-widget-container">
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
          {{ "interval": "{tf}", "width": "100%", "height": 450, "symbol": "{cur['sym']}", "locale": "pl", "colorTheme": "dark", "displayMode": "multiple" }}
          </script>
        </div>""", height=480)
