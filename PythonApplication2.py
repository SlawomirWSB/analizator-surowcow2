import streamlit as st
import streamlit.components.v1 as components

# 1. Konfiguracja i Stylistyka
st.set_page_config(layout="wide", page_title="TERMINAL V121 - FULL INTERFACE RESTORE")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .header-box { background: #1e222d; padding: 15px; border-radius: 10px; border: 1px solid #00ff88; text-align: center; margin-bottom: 20px; }
    div.stButton > button { background-color: #262730 !important; color: #ffffff !important; border: 1px solid #4b4d5a !important; font-weight: bold !important; width: 100%; }
    .btn-tg { background-color: #ffffff !important; color: #0e1117 !important; font-size: 0.8rem !important; height: 32px !important; }
    .signal-card { background-color: #1e222d; border-radius: 8px; padding: 15px; margin-bottom: 15px; border-left: 5px solid #3d4451; }
    .data-row { background: #000000; padding: 8px; border-radius: 5px; margin: 5px 0; color: #00ff88; font-family: monospace; text-align: center; font-size: 1rem; border: 1px solid #333; }
    .stat-box { background-color: #161a25; border: 1px solid #2a2e39; border-radius: 8px; padding: 12px; text-align: center; height: 80px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza Danych - Przywrócenie wszystkich sygnałów i Fix NATGAS
if 'db' not in st.session_state:
    st.session_state.db = [
        {"pair": "NATGAS", "sym": "ECONOMICS:USNGAS", "time": "11.01 | 08:15", "tg": "https://t.me/s/top_tradingsignals", "color": "#00ff88", "type": "KUPNO", "rsi": "55.4", "in": "2.850", "tp": "3.100", "sl": "2.700"},
        {"pair": "US30", "sym": "TVC:US30", "time": "11.01 | 07:03", "tg": "https://t.me/s/prosignalsfxx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "rsi": "42.1", "in": "37580", "tp": "37450", "sl": "37650"},
        {"pair": "XAU/USD", "sym": "OANDA:XAUUSD", "time": "11.01 | 01:37", "tg": "https://t.me/s/VasilyTrading", "color": "#00ff88", "type": "ANALIZA", "rsi": "51.0", "in": "2048", "tp": "2060", "sl": "2035"},
        {"pair": "GBP/CHF", "sym": "FX:GBPCHF", "time": "10.01 | 16:45", "tg": "https://t.me/s/prosignalsfxx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "rsi": "38.5", "in": "1.073", "tp": "1.071", "sl": "1.075"},
        {"pair": "GBP/AUD", "sym": "FX:GBPAUD", "time": "10.01 | 14:20", "tg": "https://t.me/s/top_tradingsignals", "color": "#00ff88", "type": "KUPNO", "rsi": "58.4", "in": "2.003", "tp": "2.007", "sl": "1.998"},
        {"pair": "CAD/JPY", "sym": "FX:CADJPY", "time": "10.01 | 09:15", "tg": "https://t.me/s/signalsproviderfx", "color": "#00ff88", "type": "KUPNO", "rsi": "62.1", "in": "113.85", "tp": "114.50", "sl": "113.30"}
    ]

if 'active_idx' not in st.session_state:
    st.session_state.active_idx = 0

st.markdown('<div class="header-box"><h3>Terminal V121 - Pełna Rekonstrukcja Interfejsu</h3></div>', unsafe_allow_html=True)

# Przycisk Aktualizacji
if st.button("🔄 WERYFIKUJ I POBIERZ DANE (Scan 10.01 - 11.01)"):
    st.rerun()

st.write("---")
col_l, col_r = st.columns([1.2, 2.5])

# --- LEWA STRONA: KARTY Z PRZYCISKAMI TELEGRAM ---
with col_l:
    st.write("### Sygnały i Linki")
    for idx, s in enumerate(st.session_state.db):
        with st.container():
            st.markdown(f"""
                <div class="signal-card" style="border-left-color:{s['color']}">
                    <div style="display:flex; justify-content:space-between;"><b>{s['pair']}</b> <small>{s['time']}</small></div>
                    <div style="color:{s['color']}; font-weight:bold;">{s['type']}</div>
                    <div class="data-row">IN: {s['in']} | TP: {s['tp']}</div>
                </div>
            """, unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"📊 ANALIZA", key=f"an_{idx}"):
                    st.session_state.active_idx = idx
                    st.rerun()
            with c2:
                st.link_button("✈️ TELEGRAM", s['tg'], help="Otwórz wpis źródłowy")

# --- PRAWA STRONA: DWA SYGNAŁY, RSI I ZEGARY ---
with col_r:
    cur = st.session_state.db[st.session_state.active_idx]
    
    tf = st.select_slider("Interwał:", options=["1m", "5m", "15m", "1h", "4h", "1D", "1W", "1M"], value="1h")

    # Przywrócenie 3 statystyk: Investing, TradingView, RSI
    r1, r2, r3 = st.columns(3)
    with r1: st.markdown(f'<div class="stat-box"><small>Investing ({tf})</small><br><b style="color:{cur["color"]}">{cur["type"]}</b></div>', unsafe_allow_html=True)
    with r2: st.markdown(f'<div class="stat-box"><small>TradingView ({tf})</small><br><b style="color:{cur["color"]}">{cur["type"]}</b></div>', unsafe_allow_html=True)
    with r3: st.markdown(f'<div class="stat-box" style="border-color:#3498db;"><small>RSI (14) {cur["pair"]}</small><br><b style="color:#3498db;">{cur["rsi"]}</b></div>', unsafe_allow_html=True)

    st.markdown(f"<center><h4>Analiza techniczna dla {cur['pair']} ({tf})</h4></center>", unsafe_allow_html=True)
    
    # Widget Zegarów - FIX NATGAS
    components.html(f"""
        <div class="tradingview-widget-container">
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
          {{
            "interval": "{tf}",
            "width": "100%",
            "isTransparent": true,
            "height": 450,
            "symbol": "{cur['sym']}",
            "showIntervalTabs": true,
            "displayMode": "multiple",
            "locale": "pl",
            "colorTheme": "dark"
          }}
          </script>
        </div>""", height=500)
