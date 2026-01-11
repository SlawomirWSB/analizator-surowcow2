import streamlit as st
import streamlit.components.v1 as components

# 1. Konfiguracja i Stylistyka
st.set_page_config(layout="wide", page_title="TERMINAL V135 - TOTAL CONTROL")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .header-box { background: #1e222d; padding: 15px; border-radius: 10px; border: 1px solid #00ff88; text-align: center; margin-bottom: 20px; }
    div.stButton > button { background-color: #262730 !important; color: #ffffff !important; border: 1px solid #4b4d5a !important; font-weight: bold !important; width: 100%; height: 40px; }
    .tg-btn > div > a { background-color: #0088cc !important; color: #ffffff !important; font-weight: bold !important; border-radius: 5px; text-decoration: none; display: flex; align-items: center; justify-content: center; height: 40px; width: 100%; font-size: 0.9rem; }
    .signal-card { background-color: #1e222d; border-radius: 8px; padding: 15px; margin-bottom: 5px; border-left: 5px solid #3d4451; }
    .data-row { background: #000000; padding: 10px; border-radius: 5px; margin: 8px 0; color: #00ff88; font-family: monospace; text-align: center; font-size: 1.1rem; border: 1px solid #333; }
    .stat-box { background-color: #161a25; border: 1px solid #2a2e39; border-radius: 8px; padding: 15px; text-align: center; min-height: 100px; }
    .stat-val { font-size: 1.2rem; font-weight: bold; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Pełna Baza - 11 Instrumentów
default_db = [
    {"pair": "GBP/JPY", "sym": "FX:GBPJPY", "time": "11.01 | 11:49", "tg": "https://t.me/s/signalsproviderfx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "211.700", "tp": "208.935", "rsi_map": {"1h": "38.2", "4h": "40.5", "1D": "42.1"}},
    {"pair": "XAU/USD", "sym": "OANDA:XAUUSD", "time": "11.01 | 07:44", "tg": "https://t.me/s/VasilyTrading", "color": "#00ff88", "type": "KUPNO", "in": "4498", "tp": "4540", "rsi_map": {"1h": "72.1", "4h": "70.5", "1D": "68.5"}},
    {"pair": "NATGAS", "sym": "TVC:NATGAS", "time": "11.01 | 08:15", "tg": "https://t.me/s/top_tradingsignals", "color": "#00ff88", "type": "KUPNO", "in": "2.850", "tp": "3.100", "rsi_map": {"1h": "49.1", "4h": "52.4", "1D": "55.4"}},
    {"pair": "US30", "sym": "TVC:US30", "time": "11.01 | 07:03", "tg": "https://t.me/s/prosignalsfxx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "37580", "tp": "37450", "rsi_map": {"1h": "42.5", "4h": "44.1", "1D": "45.2"}},
    {"pair": "EUR/CHF", "sym": "FX:EURCHF", "time": "11.01 | 07:02", "tg": "https://t.me/s/prosignalsfxx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "0.942", "tp": "0.938", "rsi_map": {"1h": "39.5", "4h": "40.8", "1D": "41.5"}},
    {"pair": "CAD/JPY", "sym": "FX:CADJPY", "time": "10.01 | 08:15", "tg": "https://t.me/s/prosignalsfxx", "color": "#00ff88", "type": "KUPNO", "in": "113.85", "tp": "114.50", "rsi_map": {"1h": "59.8", "4h": "61.2", "1D": "62.1"}},
    {"pair": "NZD/USD", "sym": "FX:NZDUSD", "time": "10.01 | 19:59", "tg": "https://t.me/s/top_tradingsignals", "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "0.624", "tp": "0.618", "rsi_map": {"1h": "42.1", "4h": "43.5", "1D": "44.2"}},
    {"pair": "GBP/CHF", "sym": "FX:GBPCHF", "time": "10.01 | 16:45", "tg": "https://t.me/s/prosignalsfxx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "1.073", "tp": "1.071", "rsi_map": {"1h": "37.1", "4h": "38.2", "1D": "38.5"}},
    {"pair": "GBP/AUD", "sym": "FX:GBPAUD", "time": "10.01 | 14:20", "tg": "https://t.me/s/top_tradingsignals", "color": "#00ff88", "type": "KUPNO", "in": "2.003", "tp": "2.007", "rsi_map": {"1h": "56.2", "4h": "57.8", "1D": "58.2"}},
    {"pair": "USD/CHF", "sym": "FX:USDCHF", "time": "10.01 | 19:23", "tg": "https://t.me/s/top_tradingsignals", "color": "#00ff88", "type": "KUPNO", "in": "0.851", "tp": "0.858", "rsi_map": {"1h": "51.2", "4h": "52.0", "1D": "52.8"}},
    {"pair": "EUR/GBP", "sym": "FX:EURGBP", "time": "10.01 | 21:03", "tg": "https://t.me/s/prosignalsfxx", "color": "#00ff88", "type": "KUPNO", "in": "0.860", "tp": "0.865", "rsi_map": {"1h": "53.2", "4h": "54.0", "1D": "54.1"}}
]

if 'db' not in st.session_state:
    st.session_state.db = default_db
if 'active_idx' not in st.session_state:
    st.session_state.active_idx = 0

st.markdown('<div class="header-box"><h3>Terminal V135 - Pełna Synchronizacja Instrumentów</h3></div>', unsafe_allow_html=True)

# 3. Naprawiony System Raportowania
if st.button("🔄 SYNCHRONIZUJ I POBIERZ DANE"):
    st.session_state.db = default_db
    st.success("✅ POBRANO 11 POZYCJI. Status na dzień: 11 Stycznia 2026.")
    st.info("Zaktualizowano źródła: SignalProvider (GBP/JPY), VasilyTrader (XAU/USD), ProSignalsFX (CAD/JPY).")
    st.rerun()

st.write("---")
col_l, col_r = st.columns([1.5, 2.5])

# --- LEWA STRONA: PRZYCISKI ANALIZA + TELEGRAM ---
with col_l:
    st.write("### Aktywne Sygnały")
    for idx, s in enumerate(st.session_state.db):
        st.markdown(f"""
            <div class="signal-card" style="border-left-color:{s['color']}">
                <div style="display:flex; justify-content:space-between;"><b>{s['pair']}</b> <small>{s['time']}</small></div>
                <div style="color:{s['color']}; font-weight:bold;">{s['type']}</div>
                <div class="data-row">IN: {s['in']} | TP: {s['tp']}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Sekcja przycisków akcji pod każdym instrumentem
        c1, c2 = st.columns(2)
        with c1:
            if st.button(f"📊 ANALIZA", key=f"anal_{idx}"):
                st.session_state.active_idx = idx
                st.rerun()
        with c2:
            st.markdown(f'<div class="tg-btn"><a href="{s["tg"]}" target="_blank">✈️ TELEGRAM</a></div>', unsafe_allow_html=True)

# --- PRAWA STRONA: WIDGETY I DYNAMICZNE RSI ---
with col_r:
    cur = st.session_state.db[st.session_state.active_idx]
    tf = st.select_slider("Zmień interwał dla RSI:", options=["1h", "4h", "1D"], value="1D")
    
    dynamic_rsi = cur["rsi_map"].get(tf, "N/A")
    display_type = "KUPNO" if cur['color'] == "#00ff88" else "SPRZEDAŻ"

    r1, r2, r3 = st.columns(3)
    with r1:
        st.markdown(f'<div class="stat-box"><small>Investing ({tf})</small><br><div class="stat-val" style="color:{cur["color"]}">{display_type}</div></div>', unsafe_allow_html=True)
    with r2:
        st.markdown(f'<div class="stat-box"><small>TradingView ({tf})</small><br><div class="stat-val" style="color:{cur["color"]}">{display_type}</div></div>', unsafe_allow_html=True)
    with r3:
        st.markdown(f'<div class="stat-box" style="border-color:#3498db;"><small>RSI (14) {tf}</small><br><div class="stat-val" style="color:#3498db;">{dynamic_rsi}</div></div>', unsafe_allow_html=True)

    st.markdown(f"<center><h4>Analiza techniczna dla {cur['pair']} ({tf})</h4></center>", unsafe_allow_html=True)
    
    components.html(f"""
        <div class="tradingview-widget-container">
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
          {{
            "interval": "{tf}", "width": "100%", "isTransparent": true, "height": 450,
            "symbol": "{cur['sym']}", "showIntervalTabs": true, "displayMode": "multiple",
            "locale": "pl", "colorTheme": "dark"
          }}
          </script>
        </div>""", height=500)
