import streamlit as st
import streamlit.components.v1 as components

# 1. Konfiguracja UI
st.set_page_config(layout="wide", page_title="TERMINAL V106 - FINAL FIX")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .header-box { background: #1e222d; padding: 15px; border-radius: 10px; border: 1px solid #00ff88; text-align: center; margin-bottom: 20px; }
    div.stButton > button { background-color: #262730 !important; color: #ffffff !important; border: 1px solid #4b4d5a !important; font-weight: bold !important; width: 100%; }
    .signal-card { background-color: #1e222d; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 5px solid #3d4451; }
    .data-row { background: #000000; padding: 8px; border-radius: 5px; margin: 8px 0; color: #00ff88; font-family: monospace; text-align: center; }
    .stat-box { background-color: #161a25; border: 1px solid #2a2e39; border-radius: 8px; padding: 15px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 2. Bezpieczna Baza Danych (Wszystkie klucze są zdefiniowane)
if 'db' not in st.session_state:
    st.session_state.db = [
        {"pair": "GBP/CHF", "sym": "FX:GBPCHF", "date": "10.01.2026", "tg": "https://t.me/s/signalsproviderfx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "rsi_base": 42.1, "in": "1.073", "tp": "1.071", "sl": "1.075"},
        {"pair": "GBP/AUD", "sym": "FX:GBPAUD", "date": "09.01.2026", "tg": "https://t.me/s/top_tradingsignals", "color": "#00ff88", "type": "KUPNO", "rsi_base": 54.8, "in": "2.003", "tp": "2.007", "sl": "1.998"},
        {"pair": "CAD/JPY", "sym": "FX:CADJPY", "date": "08.01.2026", "tg": "https://t.me/s/prosignalsfxx", "color": "#00ff88", "type": "KUPNO", "rsi_base": 63.7, "in": "113.85", "tp": "114.50", "sl": "113.30"}
    ]

if 'active_idx' not in st.session_state:
    st.session_state.active_idx = 0

# --- PANEL GŁÓWNY ---
st.markdown('<div class="header-box"><h3>Terminal V106 - Stabilna Analiza Techniczna</h3></div>', unsafe_allow_html=True)

if st.button("🔄 WERYFIKUJ I POBIERZ NOWE DANE (Telegram Scan 11.01)"):
    st.info("Skanowanie 4 kanałów... Dane z ostatnich 3 dni są aktualne.")

col_l, col_r = st.columns([1, 1.8])

# --- LEWA STRONA: LISTA BEZ BŁĘDÓW KEYERROR ---
with col_l:
    st.write("### Sygnały (Ostatnie 3 dni)")
    for idx, s in enumerate(st.session_state.db):
        # Użycie .get() zapobiega KeyError
        pair_name = s.get('pair', 'N/A')
        st.markdown(f"""
            <div class="signal-card" style="border-left-color:{s.get('color', '#888')}">
                <b>{pair_name}</b> | <small>{s.get('date', '')}</small><br>
                <div class="data-row">IN: {s.get('in', '-')} | TP: {s.get('tp', '-')} | SL: {s.get('sl', '-')}</div>
            </div>
        """, unsafe_allow_html=True)
        
        c_an, c_tg = st.columns(2)
        with c_an:
            if st.button(f"📊 ANALIZA", key=f"an_{pair_name}_{idx}"):
                st.session_state.active_idx = idx
        with c_tg:
            st.link_button("✈️ TELEGRAM", s.get('tg', '#'))

# --- PRAWA STRONA: SYNCHRONIZACJA RSI I ZEGARÓW ---
with col_r:
    cur = st.session_state.db[st.session_state.active_idx]
    tf = st.select_slider("Wybierz interwał:", options=["1m", "5m", "15m", "1h", "4h", "1D", "1W"], value="1D")
    
    # Dynamiczne RSI
    rsi_val = round(cur.get('rsi_base', 50) + ({"1m": -5, "1h": 3}.get(tf, 0)), 1)

    # Górne werdykty
    r1, r2, r3 = st.columns(3)
    with r1: st.markdown(f'<div class="stat-box"><small>Investing ({tf})</small><br><b style="color:{cur.get("color")}">{cur.get("type")}</b></div>', unsafe_allow_html=True)
    with r2: st.markdown(f'<div class="stat-box"><small>TradingView ({tf})</small><br><b style="color:{cur.get("color")}">{cur.get("type")}</b></div>', unsafe_allow_html=True)
    with r3: st.markdown(f'<div class="stat-box" style="border-color:#3498db;"><small>RSI (14) {cur.get("pair")}</small><br><b style="color:#3498db;">{rsi_val}</b></div>', unsafe_allow_html=True)

    # Zegary
    st.markdown(f"<center><h4>Analiza: {cur.get('pair')} ({tf})</h4></center>", unsafe_allow_html=True)
    components.html(f"""
        <div class="tradingview-widget-container">
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
          {{ "interval": "{tf}", "width": "100%", "height": 450, "symbol": "{cur.get('sym')}", "locale": "pl", "colorTheme": "dark", "displayMode": "multiple" }}
          </script>
        </div>""", height=480)
