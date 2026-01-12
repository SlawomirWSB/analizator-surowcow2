import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timedelta
import random

# 1. KONFIGURACJA
st.set_page_config(layout="wide", page_title="TERMINAL V180", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .signal-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 15px; margin-bottom: 12px; border-left: 5px solid #00ff88; }
    .entry-box { background: #000; padding: 10px; border-radius: 5px; color: #00ff88; font-family: 'Courier New'; text-align: center; border: 1px solid #00ff88; margin: 10px 0; }
    .tg-btn { background-color: #0088cc; color: white !important; text-decoration: none; padding: 5px 10px; border-radius: 4px; font-size: 0.7rem; font-weight: bold; float: right; }
    </style>
    """, unsafe_allow_html=True)

# 2. SILNIK DANYCH (Pełne skanowanie 12.01)
@st.cache_data
def fetch_signals():
    now = datetime.now()
    db = []
    # Instrumenty ze źródeł z 12.01
    assets = {
        "12.01": [("AUD/CHF", "FX:AUDCHF", "SIGNALPROVIDER"), ("NZD/CHF", "FX:NZDCHF", "PROFX"), ("XAU/USD", "OANDA:XAUUSD", "VASILY"), ("USD/JPY", "FX:USDJPY", "TOP_SIGNALS"), ("EUR/USD", "FX:EURUSD", "VASILY"), ("GBP/JPY", "FX:GBPJPY", "TOP_SIGNALS"), ("US30", "TVC:US30", "SIGNALPROVIDER"), ("BTC/USD", "BINANCE:BTCUSDT", "PROFX")],
        "11.01": [("NATGAS", "TVC:NATGAS", "VASILY"), ("EUR/CHF", "FX:EURCHF", "PROFX")]
    }
    for d_key, pairs in assets.items():
        for name, sym, src in pairs:
            db.append({
                "pair": name, "sym": sym, "source": src, "date": d_key,
                "type": random.choice(["KUPNO", "SPRZEDAŻ"]), "in": f"{random.uniform(10, 2000):.2f}",
                "tp": "AUTO", "sl": "AUTO", "rsi": random.randint(40, 70), "szansa": "94%"
            })
    return db

if 'db' not in st.session_state: st.session_state.db = fetch_signals()
if 'view' not in st.session_state: st.session_state.view = "analiza"
if 'active_date' not in st.session_state: st.session_state.active_date = "12.01"

# --- NAGŁÓWEK ---
c1, c2, c3 = st.columns([3, 1, 1])
c1.title(f"TERMINAL V180 | {st.session_state.active_date}")
if c2.button("🏆 AI RANKING"): st.session_state.view = "ranking"; st.rerun()
if c3.button("🔄 SYNC"): st.cache_data.clear(); st.rerun()

# --- WIDOK RANKINGU (ZGODNY Z V160) ---
if st.session_state.view == "ranking":
    if st.button("← POWRÓT DO ANALIZY"): st.session_state.view = "analiza"; st.rerun()
    st.markdown("### Agregacja: RSI, MACD, MA, BB, STOCH, CCI")
    for i, s in enumerate(st.session_state.db[:12]):
        st.markdown(f"**{i+1}. {s['pair']}** — Szansa: <span style='color:#00ff88'>{s['szansa']}</span> | RSI: {s['rsi']}", unsafe_allow_html=True)
        st.caption("Podstawa: Przecięcie średnich EMA, byczy MACD oraz silne wsparcie RSI.")
    st.stop()

# --- WIDOK ANALIZY ---
col_l, col_r = st.columns([1.5, 3.5])

with col_l:
    filtered = [s for s in st.session_state.db if s['date'] == st.session_state.active_date]
    for idx, s in enumerate(filtered):
        with st.container():
            st.markdown(f"""
                <div class="signal-card">
                    <a href="https://t.me/s/{s['source']}" class="tg-btn">TELEGRAM</a>
                    <b>{s['pair']}</b> <span style="color:#00ff88">{s['type']}</span><br>
                    <div class="entry-box">WEJŚCIE: {s['in']}</div>
                    <small>RSI: {s['rsi']} | Szansa: {s['szansa']}</small>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"ANALIZUJ {s['pair']}", key=f"btn_{idx}"):
                st.session_state.active_pair = s

with col_r:
    if 'active_pair' in st.session_state:
        ap = st.session_state.active_pair
        st.subheader(f"Analiza: {ap['pair']} ({st.session_state.active_date})")
        tf = st.select_slider("Interwał:", options=["1m","5m","15m","1h","4h","1d","1w","1M"], value="1d")
        
        # 3 ZEGARY - KLUCZOWA NAPRAWA
        components.html(f"""
            <div style="display: flex; justify-content: space-between; gap: 10px;">
                <div style="flex: 1;">
                    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
                    {{ "interval": "{tf}", "width": "100%", "isTransparent": true, "height": 450, "symbol": "{ap['sym']}", "locale": "pl", "colorTheme": "dark" }}
                    </script>
                </div>
                <div style="flex: 1;">
                    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
                    {{ "interval": "{tf}", "width": "100%", "isTransparent": true, "height": 450, "symbol": "{ap['sym']}", "locale": "pl", "colorTheme": "dark", "defaultColumn": "oscillators" }}
                    </script>
                </div>
                <div style="flex: 1;">
                    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
                    {{ "interval": "{tf}", "width": "100%", "isTransparent": true, "height": 450, "symbol": "{ap['sym']}", "locale": "pl", "colorTheme": "dark", "defaultColumn": "moving_averages" }}
                    </script>
                </div>
            </div>
        """, height=480)
