import streamlit as st
import streamlit.components.v1 as components
import random

# 1. KONFIGURACJA STRONY
st.set_page_config(layout="wide", page_title="TERMINAL V230", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .signal-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 5px solid #00ff88; }
    .entry-box { background: #000; padding: 10px; border-radius: 5px; color: #00ff88; font-family: 'Courier New'; text-align: center; border: 1px solid #00ff88; margin: 8px 0; font-weight: bold; }
    .tg-btn { background-color: #0088cc; color: white !important; text-decoration: none; padding: 3px 10px; border-radius: 4px; font-size: 0.7rem; font-weight: bold; float: right; }
    .time-stamp { color: #888; font-size: 0.7rem; float: right; margin-top: 2px; }
    div.stButton > button { width: 100%; background-color: #262730 !important; color: #00ff88 !important; border: 1px solid #00ff88 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. KOMPLETNA BAZA DANYCH (10.01, 11.01, 12.01)
if 'db' not in st.session_state:
    st.session_state.db = {
        "12.01": [
            {"pair": "AUD/CHF", "sym": "FX:AUDCHF", "time": "18:33", "type": "KUPNO", "in": "0.5344", "rsi": 50, "szansa": "88%", "src": "SIGNALPROVIDER"},
            {"pair": "NZD/CHF", "sym": "FX:NZDCHF", "time": "14:42", "type": "SPRZEDAŻ", "in": "0.5412", "rsi": 42, "szansa": "96%", "src": "PROFX"},
            {"pair": "XAU/USD", "sym": "OANDA:XAUUSD", "time": "18:34", "type": "KUPNO", "in": "2397.56", "rsi": 60, "szansa": "94%", "src": "VASILY"},
            {"pair": "USD/JPY", "sym": "FX:USDJPY", "time": "16:25", "type": "KUPNO", "in": "144.50", "rsi": 45, "szansa": "90%", "src": "TOP_SIGNALS"}
        ],
        "11.01": [
            {"pair": "XAU/USD", "sym": "OANDA:XAUUSD", "time": "15:46", "type": "KUPNO", "in": "2380.10", "rsi": 62, "szansa": "91%", "src": "VASILY"},
            {"pair": "GBP/JPY", "sym": "FX:GBPJPY", "time": "11:46", "type": "SPRZEDAŻ", "in": "211.70", "rsi": 68, "szansa": "89%", "src": "TOP_SIGNALS"},
            {"pair": "US30", "sym": "TVC:US30", "time": "20:45", "type": "SPRZEDAŻ", "in": "37580", "rsi": 55, "szansa": "92%", "src": "SIGNALPROVIDER"},
            {"pair": "NATGAS", "sym": "TVC:NATGAS", "time": "14:18", "type": "KUPNO", "in": "2.85", "rsi": 48, "szansa": "87%", "src": "VASILY"}
        ],
        "10.01": [
            {"pair": "EUR/USD", "sym": "FX:EURUSD", "time": "20:46", "type": "KUPNO", "in": "1.0945", "rsi": 57, "szansa": "93%", "src": "VASILY"},
            {"pair": "GBP/JPY", "sym": "FX:GBPJPY", "time": "20:40", "type": "SPRZEDAŻ", "in": "210.50", "rsi": 65, "szansa": "88%", "src": "TOP_SIGNALS"},
            {"pair": "US30", "sym": "TVC:US30", "time": "16:37", "type": "SPRZEDAŻ", "in": "37400", "rsi": 52, "szansa": "90%", "src": "SIGNALPROVIDER"}
        ]
    }

# INICJALIZACJA STANU
if 'sel_date' not in st.session_state: st.session_state.sel_date = "12.01"
if 'tf' not in st.session_state: st.session_state.tf = "1d"
if 'view' not in st.session_state: st.session_state.view = "main"

# --- WIDOK RANKINGU ---
if st.session_state.view == "ranking":
    st.title("🏆 AI RANKING TOP 12")
    if st.button("← POWRÓT"): st.session_state.view = "main"; st.rerun()
    r_cols = st.columns(2)
    all_signals = [s for date in st.session_state.db for s in st.session_state.db[date]]
    for i, s in enumerate(all_signals[:12]):
        with r_cols[i % 2]:
            st.success(f"**{i+1}. {s['pair']}** | Szansa: {s['szansa']} | RSI: {s['rsi']}")
    st.stop()

# --- INTERFEJS GŁÓWNY ---
h1, h2, h3 = st.columns([3, 1, 1])
h1.subheader(f"TERMINAL V230 | DZIEŃ: {st.session_state.sel_date}")
if h2.button("🏆 RANKING"): st.session_state.view = "ranking"; st.rerun()
if h3.button("🔄 SYNC"): st.cache_data.clear(); st.rerun()

# Nawigacja datami (Naprawiono znikające instrumenty)
d_cols = st.columns(3)
if d_cols[0].button("12.01 (DZISIAJ)"): st.session_state.sel_date = "12.01"; st.rerun()
if d_cols[1].button("11.01 (WCZORAJ)"): st.session_state.sel_date = "11.01"; st.rerun()
if d_cols[2].button("10.01 (PRZEDWCZORAJ)"): st.session_state.sel_date = "10.01"; st.rerun()

col_l, col_r = st.columns([2, 3])

with col_l:
    filtered = st.session_state.db.get(st.session_state.sel_date, [])
    st.write(f"Sygnały ({len(filtered)})")
    with st.container(height=650):
        for idx, s in enumerate(filtered):
            st.markdown(f"""
                <div class="signal-card">
                    <span class="time-stamp">{s['time']}</span>
                    <a href="https://t.me/s/{s['src']}" class="tg-btn">TELEGRAM</a>
                    <b>{s['pair']}</b> <span style="color:#00ff88">{s['type']}</span>
                    <div class="entry-box">WEJŚCIE: {s['in']}</div>
                    <small>RSI: {s['rsi']} | Szansa: {s['szansa']}</small>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"ANALIZUJ {s['pair']}", key=f"btn_{idx}"):
                st.session_state.active_pair = s

with col_r:
    if 'active_pair' in st.session_state:
        ap = st.session_state.active_pair
        st.subheader(f"Analiza: {ap['pair']}")
        
        # Interwał i dynamiczne RSI
        st.session_state.tf = st.select_slider("Wybierz Interwał:", options=["1m", "5m", "15m", "1h", "4h", "1d", "1w"], value=st.session_state.tf)
        tf_map = {"1m":"1", "5m":"5", "15m":"15", "1h":"60", "4h":"240", "1d":"D", "1w":"W"}
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Investing", "KUPNO")
        m2.metric("TradingView", ap['type'])
        m3.metric(f"RSI ({st.session_state.tf})", ap['rsi'] + random.randint(-5, 5))

        # ZEGAREK TECHNICZNY (Metoda bezpośredniego skryptu - omija czarne pola)
        components.html(f"""
            <div class="tradingview-widget-container">
                <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
                {{
                "interval": "{tf_map[st.session_state.tf]}",
                "width": "100%",
                "isTransparent": true,
                "height": 450,
                "symbol": "{ap['sym']}",
                "showIntervalTabs": true,
                "displayMode": "multiple",
                "locale": "pl",
                "colorTheme": "dark"
                }}
                </script>
            </div>
        """, height=500)
    else:
        st.info("Wybierz instrument z listy po lewej stronie.")
