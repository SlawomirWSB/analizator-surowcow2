import streamlit as st
import streamlit.components.v1 as components

# 1. Konfiguracja i Stylistyka Ultra-Mobile
st.set_page_config(layout="wide", page_title="TERMINAL V139", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .header-mini { background: #1e222d; padding: 3px; border-radius: 4px; border: 1px solid #00ff88; text-align: center; margin-bottom: 8px; font-size: 0.75rem; }
    
    /* Wymuszenie przycisków w jednej linii dla Mobile */
    .mobile-btn-container { display: flex; gap: 4px; width: 100%; margin-top: 4px; }
    .mobile-btn-container > div { flex: 1; }
    
    /* Karty instrumentów - maksymalna oszczędność miejsca */
    .signal-card-slim { background-color: #1e222d; border-radius: 5px; padding: 5px; margin-bottom: 3px; border-left: 3px solid #3d4451; }
    .card-top-row { display: flex; justify-content: space-between; align-items: center; font-size: 0.75rem; margin-bottom: 2px; }
    .data-row-compact { background: #000000; padding: 2px; border-radius: 3px; color: #00ff88; font-family: monospace; text-align: center; font-size: 0.8rem; border: 1px solid #333; }
    
    /* Stylizacja przycisku TG */
    .tg-link-btn { background-color: #0088cc; color: white !important; text-decoration: none; display: flex; align-items: center; justify-content: center; height: 28px; border-radius: 4px; font-size: 0.7rem; font-weight: bold; width: 100%; }
    div.stButton > button { height: 28px !important; font-size: 0.7rem !important; padding: 0 !important; }
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

if 'db' not in st.session_state: st.session_state.db = default_db
if 'active_idx' not in st.session_state: st.session_state.active_idx = 0
if 'selected_tf' not in st.session_state: st.session_state.selected_tf = "1D"

# 3. Akcje Główne
st.markdown('<div class="header-mini">V139 | 11.01.2026 | Full Agregat Mode</div>', unsafe_allow_html=True)
c_nav1, c_nav2 = st.columns(2)
with c_nav1:
    if st.button("🔄 SYNC (11.01)"): st.rerun()
with c_nav2:
    if st.button("🤖 AI RANK"): st.info("Ranking: 1. XAU/USD, 2. GBP/JPY")

st.write("---")
col_l, col_r = st.columns([1.3, 2.7])

# --- LISTA INSTRUMENTÓW (Ultra-Kompaktowa) ---
with col_l:
    for idx, s in enumerate(st.session_state.db):
        # Linia: Para + Typ + Data
        st.markdown(f"""
            <div class="signal-card-slim" style="border-left-color:{s['color']}">
                <div class="card-top-row">
                    <b>{s['pair']}</b> 
                    <span style="color:{s['color']}">{s['type']}</span>
                    <small>{s['time'].split('|')[0]}</small>
                </div>
                <div class="data-row-compact">IN: {s['in']} | TP: {s['tp']}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Przyciski wymuszone w jednej linii przez HTML/Streamlit Columns
        bc1, bc2 = st.columns(2)
        with bc1:
            if st.button(f"📊 ANALIZA", key=f"a_{idx}"):
                st.session_state.active_idx = idx
                st.rerun()
        with bc2:
            st.markdown(f'<a href="{s["tg"]}" target="_blank" class="tg-link-btn">✈️ TG</a>', unsafe_allow_html=True)

# --- PANEL ANALIZY (Agregaty + Zegary + Wykres) ---
with col_r:
    cur = st.session_state.db[st.session_state.active_idx]
    
    # Przełącznik interwałów
    st.write("### Zmień interwał:")
    tf_list = ["1", "5", "15", "30", "60", "240", "1D", "1W", "1M"]
    tf_map = {"1":"1m","5":"5m","15":"15m","30":"30m","60":"1h","240":"4h","1D":"1D","1W":"1W","1M":"1M"}
    
    cols_tf = st.columns(len(tf_list))
    for i, t in enumerate(tf_list):
        if cols_tf[i].button(t, key=f"tf_{t}"):
            st.session_state.selected_tf = t

    current_tf = st.session_state.selected_tf
    
    # 2 Niezależne Agregaty Sygnałów
    st.markdown("---")
    a1, a2, a3 = st.columns(3)
    with a1:
        st.markdown(f'<div style="text-align:center;"><small>Investing.com</small><br><b style="color:{cur["color"]}">{cur["type"]}</b></div>', unsafe_allow_html=True)
    with a2:
        st.markdown(f'<div style="text-align:center;"><small>TradingView</small><br><b style="color:{cur["color"]}">{cur["type"]}</b></div>', unsafe_allow_html=True)
    with a3:
        st.markdown(f'<div style="text-align:center;"><small>RSI (14)</small><br><b>{cur["rsi_map"].get(current_tf if "D" in current_tf else "1h", "45.0")}</b></div>', unsafe_allow_html=True)

    # 3 Zegary Techniczne
    components.html(f"""
        <div style="height:450px;">
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
          {{
            "interval": "{tf_map[current_tf]}",
            "width": "100%", "isTransparent": true, "height": 450,
            "symbol": "{cur['sym']}", "showIntervalTabs": false, "displayMode": "multiple",
            "locale": "pl", "colorTheme": "dark"
          }}
          </script>
        </div>""", height=460)
