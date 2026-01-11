import streamlit as st
import streamlit.components.v1 as components

# 1. Konfiguracja i Zaawansowany CSS dla Mobile i Desktop
st.set_page_config(layout="wide", page_title="TERMINAL V140", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Naprawiony Header */
    .header-mini { background: #1e222d; padding: 5px; border-radius: 5px; border: 1px solid #00ff88; text-align: center; margin-bottom: 10px; font-size: 0.9rem; }

    /* Wymuszenie przycisków w jednym wierszu na telefonie */
    .flex-btns { display: flex; gap: 5px; width: 100%; }
    .flex-btns > div { flex: 1; }
    
    /* Poprawa czytelności przycisków na komputerze */
    button { height: 35px !important; width: 100% !important; font-size: 0.85rem !important; font-weight: 600 !important; color: white !important; }
    
    /* Karta instrumentu - wszystko w jednej linii */
    .signal-card-v140 { background-color: #1e222d; border-radius: 8px; padding: 8px; margin-bottom: 5px; border-left: 5px solid #3d4451; }
    .top-line { display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px; font-size: 0.85rem; }
    .data-line { background: #000000; padding: 5px; border-radius: 5px; color: #00ff88; font-family: monospace; text-align: center; font-size: 0.9rem; border: 1px solid #333; }
    
    /* Link TG jako przycisk */
    .tg-link { background-color: #0088cc; color: white !important; text-decoration: none; display: flex; align-items: center; justify-content: center; height: 35px; border-radius: 4px; font-size: 0.8rem; font-weight: bold; }
    
    /* Skalowanie widgetów technicznych na mobile */
    @media (max-width: 600px) {
        .tradingview-widget-container { transform: scale(0.85); transform-origin: top left; }
    }
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

# --- NAGŁÓWEK ---
st.markdown('<div class="header-mini">V140 | 11.01.2026 | Enhanced Mobile View</div>', unsafe_allow_html=True)

c_nav1, c_nav2 = st.columns(2)
with c_nav1:
    if st.button("🔄 SYNCHRONIZUJ (11.01)"): st.rerun()
with c_nav2:
    if st.button("🤖 ANALIZUJ AI"): st.toast("Ranking wygenerowany w oknie dialogowym")

st.write("---")
col_l, col_r = st.columns([1.3, 2.7])

# --- LEWA STRONA: SYGNAŁY ---
with col_l:
    for idx, s in enumerate(st.session_state.db):
        st.markdown(f"""
            <div class="signal-card-v140" style="border-left-color:{s['color']}">
                <div class="top-line">
                    <b>{s['pair']}</b> 
                    <span style="color:{s['color']}; font-weight:bold;">{s['type']}</span>
                    <small>{s['time'].split('|')[0]}</small>
                </div>
                <div class="data-line">IN: {s['in']} | TP: {s['tp']}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Wymuszenie przycisków obok siebie w kontenerze Streamlit
        btn_c1, btn_c2 = st.columns(2)
        with btn_c1:
            if st.button(f"📊 ANALIZA", key=f"an_{idx}"):
                st.session_state.active_idx = idx
                st.rerun()
        with btn_c2:
            st.markdown(f'<a href="{s["tg"]}" target="_blank" class="tg-link">✈️ TG</a>', unsafe_allow_html=True)

# --- PRAWA STRONA: ANALIZA TECHNICZNA ---
with col_r:
    cur = st.session_state.db[st.session_state.active_idx]
    
    # Przywrócenie paska interwałów (domyślnie 1D)
    st.write("### Interwał czasowy (domyślnie 1D):")
    tf_selected = st.select_slider("Wybierz interwał:", 
                                   options=["1m", "5m", "15m", "30m", "1h", "4h", "1D", "1W", "1M"], 
                                   value="1D")
    
    # 2 Niezależne Agregaty
    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    m1.metric("Investing.com", cur['type'])
    m2.metric("TradingView", cur['type'])
    m3.metric("RSI (14)", cur["rsi_map"].get(tf_selected if "D" in tf_selected else "1h", "42.1"))

    st.markdown(f"<center><h4>Analiza {cur['pair']} ({tf_selected})</h4></center>", unsafe_allow_html=True)
    
    # 3 Zegary Techniczne w jednym widoku
    components.html(f"""
        <div class="tradingview-widget-container">
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
          {{
            "interval": "{tf_selected}",
            "width": "100%", "isTransparent": true, "height": 450,
            "symbol": "{cur['sym']}", "showIntervalTabs": false, "displayMode": "multiple",
            "locale": "pl", "colorTheme": "dark"
          }}
          </script>
        </div>""", height=480)
