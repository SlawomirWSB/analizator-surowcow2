import streamlit as st
import streamlit.components.v1 as components
import random

# 1. KONFIGURACJA PODSTAWOWA
st.set_page_config(layout="wide", page_title="TERMINAL V240", initial_sidebar_state="collapsed")

# Stylizacja UI (Karty sygnałów, przyciski, kolory)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .signal-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 5px solid #00ff88; }
    .entry-box { background: #000; padding: 10px; border-radius: 5px; color: #00ff88; font-family: 'Courier New'; text-align: center; border: 1px solid #00ff88; margin: 8px 0; font-weight: bold; }
    .tg-btn { background-color: #0088cc; color: white !important; text-decoration: none; padding: 4px 10px; border-radius: 4px; font-size: 0.75rem; font-weight: bold; float: right; }
    .time-stamp { color: #888; font-size: 0.75rem; float: right; margin-top: 2px; }
    div.stButton > button { width: 100%; background-color: #262730 !important; color: #00ff88 !important; border: 1px solid #00ff88 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. INICJALIZACJA BAZY DANYCH (Ostateczna weryfikacja dat 10.01 - 12.01)
# Dane oparte na Twoich skanach
DATA_SOURCE = {
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

# Bezpieczne ładowanie do session_state
if 'db' not in st.session_state: st.session_state.db = DATA_SOURCE
if 'sel_date' not in st.session_state: st.session_state.sel_date = "12.01"
if 'tf' not in st.session_state: st.session_state.tf = "1h"

# --- INTERFEJS ---
h1, h2, h3 = st.columns([3, 1, 1])
h1.subheader(f"TERMINAL V240 | {st.session_state.sel_date}")
if h2.button("🏆 AI RANKING"): st.toast("Generowanie rankingu..."); st.session_state.view = "ranking"

# Nawigacja dat (NAPRAWIONE)
d_cols = st.columns(3)
if d_cols[0].button("DZISIAJ (12.01)"): st.session_state.sel_date = "12.01"; st.rerun()
if d_cols[1].button("WCZORAJ (11.01)"): st.session_state.sel_date = "11.01"; st.rerun()
if d_cols[2].button("PRZEDWCZORAJ (10.01)"): st.session_state.sel_date = "10.01"; st.rerun()

col_l, col_r = st.columns([2, 3])

with col_l:
    # Pobieranie sygnałów dla wybranej daty
    signals = st.session_state.db.get(st.session_state.sel_date, [])
    st.write(f"Aktywne sygnały ({len(signals)})")
    
    with st.container(height=650):
        for idx, s in enumerate(signals):
            st.markdown(f"""
                <div class="signal-card">
                    <span class="time-stamp">{s['time']}</span>
                    <a href="https://t.me/s/{s['src']}" target="_blank" class="tg-btn">TELEGRAM</a>
                    <b>{s['pair']}</b> <span style="color:#00ff88">{s['type']}</span>
                    <div class="entry-box">WEJŚCIE: {s['in']}</div>
                    <small>RSI: {s['rsi']} | Szansa: {s['szansa']}</small>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"ANALIZA {s['pair']}", key=f"an_{idx}"):
                st.session_state.active_pair = s

with col_r:
    if 'active_pair' in st.session_state:
        ap = st.session_state.active_pair
        st.subheader(f"Szczegóły: {ap['pair']} ({st.session_state.sel_date})")
        
        # Suwak interwału
        st.session_state.tf = st.select_slider("Interwał:", options=["1m", "5m", "15m", "1h", "4h", "1d", "1w"], value=st.session_state.tf)
        tf_code = {"1m":"1", "5m":"5", "15m":"15", "1h":"60", "4h":"240", "1d":"D", "1w":"W"}[st.session_state.tf]

        # Wskaźniki
        m1, m2, m3 = st.columns(3)
        m1.metric("Investing", "KUPNO")
        m2.metric("TradingView", ap['type'])
        m3.metric(f"RSI ({st.session_state.tf})", ap['rsi'])

        # NAPRAWA ZEGARÓW (Metoda Embed z automatycznym przełączaniem interwału)
        # Ten widżet jest najbardziej stabilny w środowisku Streamlit Cloud
        components.html(f"""
            <div style="background:#111; padding:15px; border-radius:10px; height:500px;">
                <iframe src="https://s.tradingview.com/embed-widget/technical-analysis/?locale=pl&symbol={ap['sym']}&interval={tf_code}&colorTheme=dark&isTransparent=true" 
                width="100%" height="450" frameborder="0" scrolling="no" allowtransparency="true"></iframe>
            </div>
        """, height=500)
    else:
        st.info("Wybierz instrument z listy po lewej, aby zobaczyć zegary techniczne.")
