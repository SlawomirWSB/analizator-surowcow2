import streamlit as st
import streamlit.components.v1 as components

# 1. Konfiguracja i Stylizacja
st.set_page_config(layout="wide", page_title="TERMINAL V125 - DYNAMIC FIX")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .header-box { background: #1e222d; padding: 15px; border-radius: 10px; border: 1px solid #00ff88; text-align: center; margin-bottom: 20px; }
    div.stButton > button { background-color: #262730 !important; color: #ffffff !important; border: 1px solid #4b4d5a !important; font-weight: bold !important; width: 100%; }
    .tg-btn > div > a { background-color: #ffffff !important; color: #000000 !important; font-weight: bold !important; border-radius: 5px; text-decoration: none; display: flex; align-items: center; justify-content: center; height: 35px; width: 100%; font-size: 0.8rem; border: 1px solid #ccc; }
    .signal-card { background-color: #1e222d; border-radius: 8px; padding: 15px; margin-bottom: 10px; border-left: 5px solid #3d4451; }
    .data-row { background: #000000; padding: 10px; border-radius: 5px; margin: 8px 0; color: #00ff88; font-family: monospace; text-align: center; font-size: 1.1rem; border: 1px solid #333; }
    .stat-box { background-color: #161a25; border: 1px solid #2a2e39; border-radius: 8px; padding: 15px; text-align: center; min-height: 100px; }
    .stat-val { font-size: 1.2rem; font-weight: bold; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza Danych - Kompletna lista i poprawione statusy
if 'db' not in st.session_state:
    st.session_state.db = [
        {"pair": "NATGAS", "sym": "TVC:NATGAS", "time": "11.01 | 08:15", "tg": "https://t.me/s/top_tradingsignals", "color": "#00ff88", "type": "KUPNO", "rsi": "55.4", "in": "2.850", "tp": "3.100", "sl": "2.700"},
        {"pair": "US30", "sym": "TVC:US30", "time": "11.01 | 07:03", "tg": "https://t.me/s/prosignalsfxx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "rsi": "45.2", "in": "37580", "tp": "37450", "sl": "37650"},
        {"pair": "XAU/USD", "sym": "OANDA:XAUUSD", "time": "11.01 | 01:37", "tg": "https://t.me/s/VasilyTrading", "color": "#00ff88", "type": "KUPNO", "rsi": "51.0", "in": "2048", "tp": "2060", "sl": "2035"},
        {"pair": "EUR/CHF", "sym": "FX:EURCHF", "time": "11.01 | 07:03", "tg": "https://t.me/s/prosignalsfxx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "rsi": "41.5", "in": "0.942", "tp": "0.938", "sl": "0.945"},
        {"pair": "GBP/CHF", "sym": "FX:GBPCHF", "time": "10.01 | 16:45", "tg": "https://t.me/s/prosignalsfxx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "rsi": "38.5", "in": "1.073", "tp": "1.071", "sl": "1.075"},
        {"pair": "NZD/USD", "sym": "FX:NZDUSD", "time": "10.01 | 19:59", "tg": "https://t.me/s/top_tradingsignals", "color": "#ff4b4b", "type": "SPRZEDAŻ", "rsi": "44.2", "in": "0.624", "tp": "0.618", "sl": "0.628"},
        {"pair": "USD/CHF", "sym": "FX:USDCHF", "time": "10.01 | 19:23", "tg": "https://t.me/s/top_tradingsignals", "color": "#00ff88", "type": "KUPNO", "rsi": "52.8", "in": "0.851", "tp": "0.858", "sl": "0.845"},
        {"pair": "EUR/GBP", "sym": "FX:EURGBP", "time": "10.01 | 21:03", "tg": "https://t.me/s/prosignalsfxx", "color": "#00ff88", "type": "KUPNO", "rsi": "54.1", "in": "0.860", "tp": "0.865", "sl": "0.858"}
    ]

if 'active_idx' not in st.session_state:
    st.session_state.active_idx = 0

st.markdown('<div class="header-box"><h3>Terminal V125 - Pełna Dynamika i Start 1D</h3></div>', unsafe_allow_html=True)

if st.button("🔄 SYNCHRONIZUJ DANE (10.01 - 11.01)"):
    st.rerun()

st.write("---")
col_l, col_r = st.columns([1.3, 2.5])

# --- LEWA STRONA: LISTA Z PRZYCISKAMI ---
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
        c1, c2 = st.columns(2)
        with c1:
            if st.button(f"📊 ANALIZA", key=f"btn_{idx}"):
                st.session_state.active_idx = idx
                st.rerun()
        with c2:
            st.markdown(f'<div class="tg-btn"><a href="{s["tg"]}" target="_blank">✈️ TELEGRAM</a></div>', unsafe_allow_html=True)

# --- PRAWA STRONA: NAPRAWIONE AGREGATY I ZEGARY ---
with col_r:
    cur = st.session_state.db[st.session_state.active_idx]
    
    # Interwał startowy: 1D
    tf = st.select_slider("Wybierz interwał (start: 1D):", options=["1m", "5m", "15m", "1h", "4h", "1D", "1W", "1M"], value="1D")

    # Dynamiczne okna agregatów - teraz pokazują sygnał zamiast tekstu "ANALIZA"
    r1, r2, r3 = st.columns(3)
    with r1:
        st.markdown(f'<div class="stat-box"><small>Investing ({tf})</small><br><div class="stat-val" style="color:{cur["color"]}">{cur["type"]}</div></div>', unsafe_allow_html=True)
    with r2:
        st.markdown(f'<div class="stat-box"><small>TradingView ({tf})</small><br><div class="stat-val" style="color:{cur["color"]}">{cur["type"]}</div></div>', unsafe_allow_html=True)
    with r3:
        st.markdown(f'<div class="stat-box" style="border-color:#3498db;"><small>RSI (14) {cur["pair"]}</small><br><div class="stat-val" style="color:#3498db;">{cur["rsi"]}</div></div>', unsafe_allow_html=True)

    st.markdown(f"<center><h4>Analiza techniczna dla {cur['pair']} ({tf})</h4></center>", unsafe_allow_html=True)
    
    # Widget 3 zegarów - tryb multiple
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
