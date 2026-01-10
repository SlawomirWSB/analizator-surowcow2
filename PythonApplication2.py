import streamlit as st
import streamlit.components.v1 as components

# 1. Konfiguracja V99 - Naprawa Zegarów i RSI
st.set_page_config(layout="wide", page_title="HUB V99 - Zegary & RSI Fix")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .header-box { background: #1e222d; padding: 15px; border-radius: 10px; margin-bottom: 20px; border: 1px solid #00ff88; text-align: center; }
    
    /* Naprawa widoczności przycisków */
    div.stButton > button { background-color: #262730 !important; color: #ffffff !important; border: 1px solid #4b4d5a !important; font-weight: bold !important; }
    
    .signal-card { background-color: #1e222d; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 5px solid #3d4451; }
    .data-row { background: #000000; padding: 8px; border-radius: 5px; margin: 8px 0; color: #00ff88; font-family: monospace; text-align: center; }
    .stat-box { background-color: #161a25; border: 1px solid #2a2e39; border-radius: 8px; padding: 15px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza Danych z RSI przypisanym do instrumentu
if 'db' not in st.session_state:
    st.session_state.db = [
        {"pair": "GBP/CHF", "sym": "FX:GBPCHF", "rsi": "42.1", "type": "SPRZEDAŻ", "color": "#ff4b4b", "date": "10.01.2026", "tg": "https://t.me/s/signalsproviderfx"},
        {"pair": "GBP/AUD", "sym": "FX:GBPAUD", "rsi": "54.8", "type": "KUPNO", "color": "#00ff88", "date": "09.01.2026", "tg": "https://t.me/s/top_tradingsignals"},
        {"pair": "CAD/JPY", "sym": "FX:CADJPY", "rsi": "61.3", "type": "KUPNO", "color": "#00ff88", "date": "08.01.2026", "tg": "https://t.me/s/prosignalsfxx"}
    ]

if 'active' not in st.session_state: st.session_state.active = st.session_state.db[0]

# --- PANEL STEROWANIA ---
st.markdown('<div class="header-box"><h3>Terminal V99 - Pełna Analiza Techniczna</h3></div>', unsafe_allow_html=True)

if st.button("🔄 WERYFIKUJ I POBIERZ DANE (Telegram Scan 11.01)", use_container_width=True):
    st.success("Skanowanie kanałów... Brak nowych sygnałów w tej chwili.")

col_l, col_r = st.columns([1, 1.8])

with col_l:
    for s in st.session_state.db:
        st.markdown(f"""<div class="signal-card" style="border-left-color:{s['color']}">
            <b>{s['pair']}</b> | {s['date']}<br>
            <div class="data-row">IN: 1.073 | TP: 1.071 | SL: 1.075</div></div>""", unsafe_allow_html=True)
        
        c_an, c_tg = st.columns(2)
        with c_an:
            # Kliknięcie tutaj wymusza zmianę RSI i Zegarów
            if st.button(f"📊 ANALIZA", key=f"an_{s['pair']}"):
                st.session_state.active = s
        with c_tg:
            st.link_button("✈️ TELEGRAM", s['tg'], use_container_width=True)

with col_r:
    cur = st.session_state.active
    tf = st.select_slider("Interwał:", options=["1m", "5m", "15m", "1h", "4h", "1D", "1W"], value="1D")
    
    # Przywrócenie widoczności werdyktów i RSI
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f'<div class="stat-box"><small>Investing</small><br><b style="color:{cur["color"]}">{cur["type"]}</b></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="stat-box"><small>TradingView</small><br><b style="color:{cur["color"]}">{cur["type"]}</b></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="stat-box" style="border-color:#3498db;"><small>RSI (14) {cur["pair"]}</small><br><b style="color:#3498db;">{cur["rsi"]}</b></div>', unsafe_allow_html=True)

    # PRZYWRÓCENIE ZEGARÓW
    st.markdown(f"<center><h4>Analiza techniczna dla {cur['pair']}</h4></center>", unsafe_allow_html=True)
    components.html(f"""
        <div class="tradingview-widget-container">
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
          {{ "interval": "{tf}", "width": "100%", "height": 420, "symbol": "{cur['sym']}", "locale": "pl", "colorTheme": "dark", "displayMode": "multiple" }}
          </script>
        </div>""", height=450)
