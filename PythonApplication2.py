import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timedelta
import random

# 1. KONFIGURACJA STYLU (BEZ ZMIAN)
st.set_page_config(layout="wide", page_title="TERMINAL V164", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    div[data-testid="stDialog"] { background-color: #1e222d !important; color: #ffffff !important; border: 2px solid #00ff88; }
    div.stButton > button { 
        background-color: #262730 !important; color: #00ff88 !important; 
        border: 2px solid #00ff88 !important; width: 100%; font-weight: bold !important;
    }
    .signal-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 6px solid #00ff88; }
    .entry-box { background: #000; padding: 10px; border-radius: 5px; color: #00ff88; font-family: 'Courier New'; text-align: center; border: 1px solid #00ff88; margin: 10px 0; }
    .tg-btn { background-color: #0088cc !important; color: white !important; display: block; text-align: center; padding: 8px; border-radius: 5px; text-decoration: none; font-weight: bold; margin-top: 5px; }
    .header-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px; font-size: 0.95rem; }
    .reasoning-dialog { font-size: 0.85rem; color: #00ff88; margin-top: 4px; font-style: italic; }
    </style>
    """, unsafe_allow_html=True)

# 2. GENEROWANIE DANYCH (MAX 3 DNI)
def fetch_latest_data():
    base_assets = [
        ("XAU/USD", "OANDA:XAUUSD", "KUPNO", "4498", "4540", "4470", "EMA Cross + RSI Support"),
        ("GBP/JPY", "FX:GBPJPY", "SPRZEDAŻ", "211.700", "208.935", "212.500", "RSI Overbought"),
        ("US30", "TVC:US30", "SPRZEDAŻ", "37580", "37450", "37700", "Bearish Divergence"),
        ("NATGAS", "TVC:NATGAS", "KUPNO", "2.850", "3.100", "2.700", "Trendline Support"),
        ("EUR/CHF", "FX:EURCHF", "SPRZEDAŻ", "0.942", "0.938", "0.948", "CCI Breakout"),
        ("CAD/JPY", "FX:CADJPY", "KUPNO", "113.85", "114.50", "113.20", "MA 200 Support"),
        ("NZD/USD", "FX:NZDUSD", "SPRZEDAŻ", "0.624", "0.618", "0.630", "Fibo Retest"),
        ("GBP/CHF", "FX:GBPCHF", "KUPNO", "1.073", "1.080", "1.069", "EMA 50 Bounce"),
        ("USD/CHF", "FX:USDCHF", "KUPNO", "0.851", "0.858", "0.845", "MACD Golden Cross"),
        ("EUR/USD", "FX:EURUSD", "SPRZEDAŻ", "1.085", "1.079", "1.091", "BB Rejection"),
        ("BTC/USD", "BINANCE:BTCUSDT", "KUPNO", "94200", "96500", "92000", "Volume Spike"),
        ("ETH/USD", "BINANCE:ETHUSDT", "KUPNO", "3350", "3500", "3200", "Ichimoku Breakout")
    ]
    full_db = []
    now = datetime.now()
    for day_offset in range(3):
        target_date = now - timedelta(days=day_offset)
        for asset in base_assets:
            sig_time = target_date.replace(hour=random.randint(8, 20), minute=random.randint(0, 59))
            full_db.append({
                "pair": asset[0], "sym": asset[1], "type": asset[2],
                "date_key": sig_time.strftime("%d.%m"),
                "time": sig_time.strftime("%H:%M"),
                "in": asset[3], "tp": asset[4], "sl": asset[5],
                "inv": asset[2], "tv": asset[2], "base": asset[6]
            })
    return full_db

# 3. BEZPIECZNA INICJALIZACJA (NAPRAWA KEYERROR)
if 'db' not in st.session_state: 
    st.session_state.db = fetch_latest_data()
if 'selected_date' not in st.session_state: 
    st.session_state.selected_date = datetime.now().strftime("%d.%m")
if 'active_idx' not in st.session_state: 
    st.session_state.active_idx = 0
if 'current_tf' not in st.session_state: 
    st.session_state.current_tf = "1h"

# Filtrowanie po upewnieniu się, że klucze istnieją
filtered_signals = [s for s in st.session_state.db if s.get('date_key') == st.session_state.selected_date]

def get_advanced_metrics(pair_data, tf):
    tf_rsi_base = {"1m": 35, "5m": 42, "15m": 48, "1h": 55, "4h": 62, "1D": 68, "1W": 75}
    rsi = round((tf_rsi_base.get(tf, 50) + len(pair_data['pair'])) % 92, 1)
    tf_weight = {"1m": 60, "5m": 65, "15m": 72, "1h": 80, "4h": 85, "1D": 92, "1W": 95}
    chance = tf_weight.get(tf, 70) + (len(pair_data['pair']) % 5)
    return rsi, min(chance, 99)

@st.dialog("📊 RANKING AI: " + st.session_state.selected_date)
def show_ranking():
    st.markdown(f"Interwał: **{st.session_state.current_tf}**")
    for i, item in enumerate(filtered_signals):
        rsi, chance = get_advanced_metrics(item, st.session_state.current_tf)
        st.markdown(f"""
            {i+1}. **{item['pair']}** | Szansa: `{chance}%` | RSI: `{rsi}`
            <div class='reasoning-dialog'>Baza: {item['base']}</div>
            <hr style='margin:8px 0; border:0.2px solid #444;'>
        """, unsafe_allow_html=True)

# --- INTERFEJS ---
st.markdown(f'<div style="background:#1e222d; padding:10px; border:1px solid #00ff88; text-align:center; font-weight:bold; color:white;">TERMINAL V164 | DZIEŃ: {st.session_state.selected_date}</div>', unsafe_allow_html=True)

c_top = st.columns([1, 1, 1, 1, 2])
dates = [(datetime.now() - timedelta(days=i)).strftime("%d.%m") for i in range(2, -1, -1)]

for i, d in enumerate(dates):
    with c_top[i]:
        if st.button(d, key=f"d_{d}"):
            st.session_state.selected_date = d
            st.rerun()

with c_top[3]:
    if st.button("🔄 SYNC"):
        st.session_state.db = fetch_latest_data()
        st.session_state.selected_date = datetime.now().strftime("%d.%m")
        st.rerun()

with c_top[4]:
    if st.button("🤖 AI RANKING"): show_ranking()

col_l, col_r = st.columns([1.8, 3.2])

with col_l:
    st.subheader(f"Sygnały ({st.session_state.selected_date})")
    container = st.container(height=800)
    with container:
        for idx, s in enumerate(filtered_signals):
            type_color = "#00ff88" if "KUPNO" in s['type'] else "#ff4b4b"
            st.markdown(f"""
                <div class="signal-card">
                    <div class="header-row">
                        <span><b>{s['pair']}</b> <span style="color:{type_color}; margin-left:10px;">{s['type']}</span></span>
                        <span style="font-size:0.75rem; color:#888;">{s['time']}</span>
                    </div>
                    <div class="entry-box">IN: {s['in']} | TP: {s['tp']} | SL: {s['sl']}</div>
                    <a href="https://t.me/s/VasilyTrading" class="tg-btn">✈ TELEGRAM</a>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"📊 ANALIZA {s['pair']}", key=f"an_{idx}"):
                st.session_state.active_idx = st.session_state.db.index(s)
                st.rerun()

with col_r:
    cur = st.session_state.db[st.session_state.active_idx]
    st.markdown(f"## Analiza: {cur['pair']} ({cur['date_key']})")
    new_tf = st.select_slider("TF:", options=["1m", "5m", "15m", "1h", "4h", "1D", "1W"], value=st.session_state.current_tf)
    if new_tf != st.session_state.current_tf:
        st.session_state.current_tf = new_tf
        st.rerun()
    
    rsi, _ = get_advanced_metrics(cur, st.session_state.current_tf)
    a1, a2, a3 = st.columns(3)
    with a1: st.metric("Investing", cur['inv'])
    with a2: st.metric("TradingView", cur['tv'])
    with a3: st.metric(f"RSI ({st.session_state.current_tf})", rsi)

    components.html(f"""
        <div style="height:500px;">
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
          {{ "interval": "{st.session_state.current_tf}", "width": "100%", "isTransparent": true, "height": 450, "symbol": "{cur['sym']}", "locale": "pl", "colorTheme": "dark" }}
          </script>
        </div>""", height=500)
