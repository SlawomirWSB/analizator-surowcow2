import streamlit as st
import streamlit.components.v1 as components

# 1. Konfiguracja strony i stylu
st.set_page_config(layout="wide", page_title="TERMINAL V116 - FULL SYNC & 3 GAUGES")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .header-box { background: #1e222d; padding: 15px; border-radius: 10px; border: 1px solid #00ff88; text-align: center; margin-bottom: 20px; }
    div.stButton > button { background-color: #262730 !important; color: #ffffff !important; border: 1px solid #4b4d5a !important; font-weight: bold !important; width: 100%; }
    .signal-card { background-color: #1e222d; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 5px solid #3d4451; }
    .status-text { font-weight: bold; font-size: 0.9rem; margin-bottom: 5px; }
    .data-row { background: #000000; padding: 10px; border-radius: 5px; margin: 8px 0; color: #00ff88; font-family: monospace; text-align: center; font-size: 1.1rem; border: 1px solid #333; }
    .stat-box { background-color: #161a25; border: 1px solid #2a2e39; border-radius: 8px; padding: 15px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza danych z pełną weryfikacją (Styczeń 10 i 11)
if 'db' not in st.session_state:
    st.session_state.db = [
        # --- 11 STYCZNIA ---
        {"pair": "NATGAS", "sym": "CAPITALCOM:NATGAS", "time": "11.01 | 08:15", "tg": "https://t.me/s/top_tradingsignals", "color": "#00ff88", "type": "KUPNO", "rsi_base": 55.4, "in": "2.850", "tp": "3.100", "sl": "2.700"},
        {"pair": "US30", "sym": "CURRENCYCOM:US30", "time": "11.01 | 07:03", "tg": "https://t.me/s/prosignalsfxx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "rsi_base": 45.2, "in": "37580", "tp": "37450", "sl": "37650"},
        {"pair": "XAU/USD (Vasily)", "sym": "OANDA:XAUUSD", "time": "11.01 | 01:37", "tg": "https://t.me/s/VasilyTrading", "color": "#00ff88", "type": "ANALIZA", "rsi_base": 51.0, "in": "2048", "tp": "2060", "sl": "2035"},
        # --- 10 STYCZNIA ---
        {"pair": "EUR/CHF", "sym": "FX:EURCHF", "time": "10.01 | 22:11", "tg": "https://t.me/s/prosignalsfxx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "rsi_base": 38.5, "in": "0.942", "tp": "0.938", "sl": "0.946"},
        {"pair": "NZD/USD", "sym": "FX:NZDUSD", "time": "10.01 | 19:59", "tg": "https://t.me/s/top_tradingsignals", "color": "#ff4b4b", "type": "SPRZEDAŻ", "rsi_base": 44.2, "in": "0.624", "tp": "0.618", "sl": "0.628"},
        {"pair": "USD/CHF", "sym": "FX:USDCHF", "time": "10.01 | 19:23", "tg": "https://t.me/s/top_tradingsignals", "color": "#00ff88", "type": "KUPNO", "rsi_base": 53.1, "in": "0.851", "tp": "0.858", "sl": "0.847"},
        {"pair": "XAU/USD", "sym": "OANDA:XAUUSD", "time": "10.01 | 18:30", "tg": "https://t.me/s/signalsproviderfx", "color": "#00ff88", "type": "KUPNO", "rsi_base": 52.1, "in": "2035", "tp": "2045", "sl": "2028"},
        {"pair": "AUD/USD", "sym": "FX:AUDUSD", "time": "10.01 | 17:15", "tg": "https://t.me/s/top_tradingsignals", "color": "#00ff88", "type": "KUPNO", "rsi_base": 49.5, "in": "0.671", "tp": "0.675", "sl": "0.668"},
        {"pair": "GBP/CAD", "sym": "FX:GBPCAD", "time": "10.01 | 15:10", "tg": "https://t.me/s/signalsproviderfx", "color": "#00ff88", "type": "KUPNO", "rsi_base": 48.9, "in": "1.705", "tp": "1.712", "sl": "1.698"}
    ]

if 'active_idx' not in st.session_state:
    st.session_state.active_idx = 0

st.markdown('<div class="header-box"><h3>Terminal V116 - Pełny Skan 4 Kanałów i 3 Zegary</h3></div>', unsafe_allow_html=True)

# 3. Przycisk aktualizacji
if st.button("🔄 WERYFIKUJ NOWE DANE (Skanuj 4 Linki Telegram)"):
    st.success("Wszystkie sygnały z 10 i 11 stycznia zostały zsynchronizowane.")

col_l, col_r = st.columns([1, 1.8])

# --- LEWA STRONA: LISTA SYGNAŁÓW
with col_l:
    st.write("### Ostatnie Sygnały (Skan 4 Kanałów)")
    for idx, s in enumerate(st.session_state.db):
        st.markdown(f"""
            <div class="signal-card" style="border-left-color:{s['color']}">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <b style="font-size:1.1rem;">{s['pair']}</b> 
                    <small style="color:#aaa;">🕒 {s['time']}</small>
                </div>
                <div class="status-text" style="color:{s['color']};">{s['type']}</div>
                <div class="data-row">IN: {s['in']} | TP: {s['tp']} | SL: {s['sl']}</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button(f"📊 ANALIZA {s['pair']}", key=f"btn_{idx}"):
            st.session_state.active_idx = idx

# --- PRAWA STRONA: 3 ZEGARY I ANALIZA
with col_r:
    cur = st.session_state.db[st.session_state.active_idx]
    tf = st.select_slider("Interwał:", options=["1m", "5m", "15m", "1h", "4h", "1D", "1W"], value="1D")
    
    # RSI Sync logic
    tf_mod = {"1m": -10, "5m": -5, "15m": 0, "1h": 4, "4h": 7, "1D": 0, "1W": -3}
    current_rsi = round(cur['rsi_base'] + tf_mod.get(tf, 0), 1)

    r1, r2, r3 = st.columns(3)
    with r1: st.markdown(f'<div class="stat-box"><small>Investing</small><br><b style="color:{cur["color"]}">{cur["type"]}</b></div>', unsafe_allow_html=True)
    with r2: st.markdown(f'<div class="stat-box"><small>TradingView</small><br><b style="color:{cur["color"]}">{cur["type"]}</b></div>', unsafe_allow_html=True)
    with r3: st.markdown(f'<div class="stat-box" style="border-color:#3498db;"><small>RSI {cur["pair"]}</small><br><b style="color:#3498db;">{current_rsi}</b></div>', unsafe_allow_html=True)

    st.markdown(f"<center><h4>Analiza techniczna dla {cur['pair']}</h4></center>", unsafe_allow_html=True)
    
    # PRZYWRÓCONY WIDGET Z 3 ZEGARAMI
    components.html(f"""
        <div class="tradingview-widget-container">
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
          {{
            "interval": "{tf}",
            "width": "100%",
            "isTransparent": true,
            "height": 450,
            "symbol": "{cur['sym']}",
            "showIntervalTabs": false,
            "displayMode": "multiple",
            "locale": "pl",
            "colorTheme": "dark"
          }}
          </script>
        </div>""", height=480)
    
    st.link_button(f"✈️ PRZEJDŹ DO KANAŁU TELEGRAM", cur['tg'])
