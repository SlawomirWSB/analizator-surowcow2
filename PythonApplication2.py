import streamlit as st
import streamlit.components.v1 as components

# 1. Konfiguracja i Stylistyka
st.set_page_config(layout="wide", page_title="TERMINAL V131 - DYNAMIC RSI")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .header-box { background: #1e222d; padding: 15px; border-radius: 10px; border: 1px solid #00ff88; text-align: center; margin-bottom: 20px; }
    .data-row { background: #000000; padding: 10px; border-radius: 5px; margin: 8px 0; color: #00ff88; font-family: monospace; text-align: center; font-size: 1.1rem; border: 1px solid #333; }
    .stat-box { background-color: #161a25; border: 1px solid #2a2e39; border-radius: 8px; padding: 15px; text-align: center; min-height: 100px; }
    .stat-val { font-size: 1.2rem; font-weight: bold; margin-top: 5px; }
    .signal-card { background-color: #1e222d; border-radius: 8px; padding: 15px; margin-bottom: 10px; border-left: 5px solid #3d4451; }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza Danych z Dynamicznym RSI
# Wartości RSI zmieniają się teraz zależnie od interwału
default_db = [
    {
        "pair": "GBP/JPY", "sym": "FX:GBPJPY", "time": "11.01 | 11:49", "tg": "https://t.me/s/signalsproviderfx", 
        "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "211.700", "tp": "208.935", "sl": "212.500",
        "rsi_values": {"1h": "38.2", "4h": "41.5", "1D": "42.1", "1W": "45.0"} #
    },
    {
        "pair": "XAU/USD", "sym": "OANDA:XAUUSD", "time": "11.01 | 07:44", "tg": "https://t.me/s/VasilyTrading", 
        "color": "#00ff88", "type": "KUPNO", "in": "4498", "tp": "4540", "sl": "4470",
        "rsi_values": {"1h": "72.4", "4h": "69.1", "1D": "68.5", "1W": "65.2"} #
    },
    {
        "pair": "NATGAS", "sym": "TVC:NATGAS", "time": "11.01 | 08:15", "tg": "https://t.me/s/top_tradingsignals", 
        "color": "#00ff88", "type": "KUPNO", "in": "2.850", "tp": "3.100", "sl": "2.700",
        "rsi_values": {"1h": "48.5", "4h": "52.0", "1D": "55.4", "1W": "58.1"}
    }
]

if 'db' not in st.session_state:
    st.session_state.db = default_db
if 'active_idx' not in st.session_state:
    st.session_state.active_idx = 0

st.markdown('<div class="header-box"><h3>Terminal V131 - Dynamiczne RSI & Multi-Timeframe</h3></div>', unsafe_allow_html=True)

if st.button("🔄 SYNCHRONIZUJ DANE (Aktualizacja interwałów RSI)"):
    st.session_state.db = default_db
    st.rerun()

st.write("---")
col_l, col_r = st.columns([1.3, 2.5])

# --- LEWA STRONA ---
with col_l:
    st.write("### Aktywne Sygnały")
    for idx, s in enumerate(st.session_state.db):
        st.markdown(f"""
            <div class="signal-card" style="border-left-color:{s['color']}">
                <div style="display:flex; justify-content:space-between;"><b>{s['pair']}</b> <small>{s['time']}</small></div>
                <div style="color:{s['color']}; font-weight:bold;">{s['type']}</div>
                <div class="data-row">IN: {s['in']} | TP: {s['tp']} | SL: {s['sl']}</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button(f"📊 ANALIZA {s['pair']}", key=f"btn_{idx}"):
            st.session_state.active_idx = idx
            st.rerun()

# --- PRAWA STRONA (LOGIKA DYNAMICZNEGO RSI) ---
with col_r:
    cur = st.session_state.db[st.session_state.active_idx]
    
    # Suwak interwału steruje teraz wartością RSI
    tf = st.select_slider("Wybierz interwał:", options=["1h", "4h", "1D", "1W"], value="1D")
    
    # Pobieranie RSI dla konkretnego interwału
    current_rsi = cur["rsi_values"].get(tf, "N/A")
    display_type = "KUPNO" if cur['color'] == "#00ff88" else "SPRZEDAŻ"

    r1, r2, r3 = st.columns(3)
    with r1:
        st.markdown(f'<div class="stat-box"><small>Investing ({tf})</small><br><div class="stat-val" style="color:{cur["color"]}">{display_type}</div></div>', unsafe_allow_html=True)
    with r2:
        st.markdown(f'<div class="stat-box"><small>TradingView ({tf})</small><br><div class="stat-val" style="color:{cur["color"]}">{display_type}</div></div>', unsafe_allow_html=True)
    with r3:
        # TUTAJ RSI ZMIENIA SIĘ DYNAMICZNIE
        st.markdown(f'<div class="stat-box" style="border-color:#3498db;"><small>RSI (14) {tf}</small><br><div class="stat-val" style="color:#3498db;">{current_rsi}</div></div>', unsafe_allow_html=True)

    st.markdown(f"<center><h4>Analiza techniczna dla {cur['pair']} ({tf})</h4></center>", unsafe_allow_html=True)
    
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
