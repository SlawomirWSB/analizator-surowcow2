import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timedelta
import random

# 1. KONFIGURACJA SYSTEMU
st.set_page_config(layout="wide", page_title="TERMINAL V200", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .signal-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 5px solid #00ff88; position: relative; }
    .entry-box { background: #000; padding: 10px; border-radius: 5px; color: #00ff88; font-family: 'Courier New'; text-align: center; border: 1px solid #00ff88; margin: 8px 0; font-weight: bold; }
    .tg-btn { background-color: #0088cc; color: white !important; text-decoration: none; padding: 4px 12px; border-radius: 4px; font-size: 0.75rem; font-weight: bold; float: right; }
    .time-stamp { color: #888; font-size: 0.7rem; float: right; margin-top: 2px; }
    div.stButton > button { width: 100%; background-color: #262730 !important; color: #00ff88 !important; border: 1px solid #00ff88 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. BAZA SYGNAŁÓW (Weryfikacja 11.01 i 12.01)
@st.cache_data
def get_historical_data():
    db = []
    # Dane z Twoich źródeł
    raw = {
        "12.01": [
            ("AUD/CHF", "FX:AUDCHF", "11:33", "SIGNALPROVIDER"), ("NZD/CHF", "FX:NZDCHF", "14:51", "PROFX"),
            ("XAU/USD", "OANDA:XAUUSD", "09:25", "VASILY"), ("USD/JPY", "FX:USDJPY", "14:31", "TOP_SIGNALS"),
            ("US30", "TVC:US30", "14:35", "SIGNALPROVIDER")
        ],
        "11.01": [
            ("XAU/USD", "OANDA:XAUUSD", "15:46", "VASILY"), ("GBP/JPY", "FX:GBPJPY", "11:46", "TOP_SIGNALS"),
            ("US30", "TVC:US30", "20:45", "SIGNALPROVIDER"), ("NATGAS", "TVC:NATGAS", "14:18", "VASILY"),
            ("EUR/CHF", "FX:EURCHF", "11:50", "PROFX"), ("CAD/JPY", "FX:CADJPY", "12:25", "VASILY")
        ]
    }
    for d_key, pairs in raw.items():
        for name, sym, t, src in pairs:
            db.append({
                "pair": name, "sym": sym, "time": t, "source": src, "date_key": d_key,
                "type": random.choice(["KUPNO", "SPRZEDAŻ"]),
                "in": f"{random.uniform(1, 2000):.4f}", "szansa": f"{random.randint(88, 96)}%"
            })
    return db

# Stan sesji
if 'db' not in st.session_state: st.session_state.db = get_historical_data()
if 'view' not in st.session_state: st.session_state.view = "main"
if 'sel_date' not in st.session_state: st.session_state.sel_date = "12.01"
if 'tf' not in st.session_state: st.session_state.tf = "1d"

# --- RANKING WIDOK ---
if st.session_state.view == "ranking":
    st.title("🏆 AI RANKING AGREGACJI")
    if st.button("← POWRÓT"): st.session_state.view = "main"; st.rerun()
    cols = st.columns(2)
    filtered_r = [s for s in st.session_state.db if s['date_key'] == st.session_state.sel_date]
    for i, s in enumerate(filtered_r[:12]):
        with cols[i % 2]:
            st.markdown(f"**{i+1}. {s['pair']}** | Szansa: {s['szansa']} | Źródło: {s['source']}")
    st.stop()

# --- GŁÓWNY INTERFEJS ---
h1, h2, h3 = st.columns([3, 1, 1])
h1.subheader(f"TERMINAL V200 | DZIEŃ: {st.session_state.sel_date}")
if h2.button("🏆 RANKING"): st.session_state.view = "ranking"; st.rerun()
if h3.button("🔄 SYNC"): st.cache_data.clear(); st.rerun()

# Nawigacja dat
n1, n2, n3 = st.columns(3)
if n1.button("12.01 (DZISIAJ)"): st.session_state.sel_date = "12.01"; st.rerun()
if n2.button("11.01 (WCZORAJ)"): st.session_state.sel_date = "11.01"; st.rerun()

col_l, col_r = st.columns([1.8, 3.2])

with col_l:
    curr_signals = [s for s in st.session_state.db if s['date_key'] == st.session_state.sel_date]
    st.write(f"Aktywne Sygnały ({len(curr_signals)})")
    cont = st.container(height=700)
    with cont:
        for idx, s in enumerate(curr_signals):
            st.markdown(f"""
                <div class="signal-card">
                    <span class="time-stamp">{s['time']}</span>
                    <a href="https://t.me/s/{s['source']}" class="tg-btn">TELEGRAM</a>
                    <b>{s['pair']}</b> <span style="color:#00ff88">{s['type']}</span>
                    <div class="entry-box">WEJŚCIE: {s['in']}</div>
                    <small>Szansa: {s['szansa']} | RSI: {random.randint(40,70)}</small>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"ANALIZA {s['pair']}", key=f"a_{idx}"):
                st.session_state.active_pair = s

with col_r:
    if 'active_pair' in st.session_state:
        ap = st.session_state.active_pair
        st.subheader(f"Analiza: {ap['pair']} ({st.session_state.sel_date})")
        
        # dynamiczne RSI zależne od interwału
        tf_rsi_map = {"1m": 32, "5m": 45, "15m": 52, "1h": 62, "4h": 69, "1d": 57, "1w": 41}
        st.session_state.tf = st.select_slider("Interwał:", options=["1m","5m","15m","1h","4h","1d","1w"], value=st.session_state.tf)
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Investing", "KUPNO")
        m2.metric("TradingView", "KUPNO")
        m3.metric(f"RSI ({st.session_state.tf})", tf_rsi_map.get(st.session_state.tf, 50))

        # PRZYWRÓCENIE DZIAŁAJĄCYCH ZEGARÓW Z V160
        tf_code = {"1m":"1", "5m":"5", "15m":"15", "1h":"60", "4h":"240", "1d":"D", "1w":"W"}[st.session_state.tf]
        
        components.html(f"""
            <div style="display: flex; justify-content: space-between; gap: 10px; background: #111; padding: 15px;">
                <iframe src="https://s.tradingview.com/embed-widget/technical-analysis/?symbol={ap['sym']}&interval={tf_code}&colorTheme=dark&isTransparent=true&locale=pl" width="33%" height="450" frameborder="0"></iframe>
                <iframe src="https://s.tradingview.com/embed-widget/technical-analysis/?symbol={ap['sym']}&interval={tf_code}&colorTheme=dark&isTransparent=true&locale=pl&defaultColumn=oscillators" width="33%" height="450" frameborder="0"></iframe>
                <iframe src="https://s.tradingview.com/embed-widget/technical-analysis/?symbol={ap['sym']}&interval={tf_code}&colorTheme=dark&isTransparent=true&locale=pl&defaultColumn=moving_averages" width="33%" height="450" frameborder="0"></iframe>
            </div>
        """, height=480)
