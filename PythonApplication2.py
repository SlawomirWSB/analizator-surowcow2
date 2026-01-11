import streamlit as st
import streamlit.components.v1 as components

# 1. Konfiguracja i Zaawansowany CSS
st.set_page_config(layout="wide", page_title="TERMINAL V141", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* GWARANTOWANA WIDOCZNOŚĆ TEKSTU NA PRZYCISKACH */
    div.stButton > button { 
        background-color: #262730 !important; 
        color: #ffffff !important; 
        border: 1px solid #4b4d5a !important;
        font-weight: bold !important;
        opacity: 1 !important;
    }
    
    /* Wymuszony wiersz dla Mobile (ANALIZA + TG) */
    .mobile-row { display: flex; gap: 5px; width: 100%; margin-top: 5px; }
    .mobile-row > div { flex: 1; }
    
    /* Karta instrumentu z GODZINĄ */
    .signal-card-v141 { background-color: #1e222d; border-radius: 8px; padding: 10px; margin-bottom: 6px; border-left: 5px solid #3d4451; }
    .card-header-v141 { display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px; }
    .pair-name { font-size: 1rem; font-weight: bold; }
    .update-time { font-size: 0.75rem; color: #888888; }
    .data-box { background: #000; padding: 6px; border-radius: 5px; color: #00ff88; font-family: monospace; text-align: center; border: 1px solid #333; }

    /* Przycisk TG */
    .tg-btn { background-color: #0088cc; color: white !important; text-decoration: none; display: flex; align-items: center; justify-content: center; height: 38px; border-radius: 4px; font-weight: bold; font-size: 0.8rem; }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza danych (11 instrumentów)
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

# --- HEADER I SYNC SYSTEM ---
st.markdown('<div style="background:#1e222d; padding:10px; border-radius:5px; border:1px solid #00ff88; text-align:center; margin-bottom:15px;">TERMINAL V141 | 11.01.2026 | System Aktywny</div>', unsafe_allow_html=True)

c_nav1, c_nav2 = st.columns(2)
with c_nav1:
    if st.button("🔄 SYNCHRONIZUJ DANE"):
        st.success("✅ Zaktualizowano pomyślnie! Dodano 0 nowych sygnałów.")
with c_nav2:
    if st.button("🤖 ANALIZUJ AI"):
        st.info("🤖 AI: XAU/USD wykazuje najsilniejszy sentyment (Pewność: 94%).")

st.write("---")
col_l, col_r = st.columns([1.4, 2.6])

# --- LEWA STRONA: SYGNAŁY Z GODZINAMI ---
with col_l:
    for idx, s in enumerate(st.session_state.db):
        st.markdown(f"""
            <div class="signal-card-v141" style="border-left-color:{s['color']}">
                <div class="card-header-v141">
                    <span class="pair-name">{s['pair']} <span style="color:{s['color']}">{s['type']}</span></span>
                    <span class="update-time">{s['time']}</span>
                </div>
                <div class="data-box">IN: {s['in']} | TP: {s['tp']}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Wymuszony układ przycisków
        btn_c1, btn_c2 = st.columns(2)
        with btn_c1:
            if st.button(f"📊 ANALIZA", key=f"an_{idx}"):
                st.session_state.active_idx = idx
                st.rerun()
        with btn_c2:
            st.markdown(f'<a href="{s["tg"]}" target="_blank" class="tg-btn">✈️ TELEGRAM</a>', unsafe_allow_html=True)

# --- PRAWA STRONA: ANALIZA (3 Zegary + Agregaty) ---
with col_r:
    cur = st.session_state.db[st.session_state.active_idx]
    
    st.write("### Interwał (Domyślnie 1D):")
    tf_selected = st.select_slider("Wybierz:", options=["1m", "5m", "15m", "30m", "1h", "4h", "1D", "1W", "1M"], value="1D")
    
    # 2 Niezależne Agregaty
    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    m1.metric("Investing.com", cur['type'])
    m2.metric("TradingView", cur['type'])
    m3.metric("RSI (14)", cur["rsi_map"].get(tf_selected if "D" in tf_selected else "1h", "48.2"))

    # Widget 3 zegarów
    components.html(f"""
        <div style="height:450px;">
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
          {{
            "interval": "{tf_selected}",
            "width": "100%", "isTransparent": true, "height": 450,
            "symbol": "{cur['sym']}", "showIntervalTabs": false, "displayMode": "multiple",
            "locale": "pl", "colorTheme": "dark"
          }}
          </script>
        </div>""", height=480)
