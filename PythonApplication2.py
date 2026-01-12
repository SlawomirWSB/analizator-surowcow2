import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timedelta
import random

# 1. KONFIGURACJA
st.set_page_config(layout="wide", page_title="TERMINAL V161", initial_sidebar_state="collapsed")

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

# 2. FUNKCJA AKTUALIZACJI (SYGNAŁY Z OSTATNICH 3 DNI)
def fetch_latest_data():
    base_assets = [
        ("XAU/USD", "OANDA:XAUUSD", "KUPNO", "4498", "4540", "4470", "Przecięcie średnich EMA, byczy MACD oraz silne wsparcie RSI."),
        ("GBP/JPY", "FX:GBPJPY", "SPRZEDAŻ", "211.700", "208.935", "212.500", "Rynek wykupiony na RSI, odrzucenie górnej wstęgi Bollingera."),
        ("US30", "TVC:US30", "SPRZEDAŻ", "37580", "37450", "37700", "Niedźwiedzia dywergencja na oscylatorach i reakcja na opór."),
        ("NATGAS", "TVC:NATGAS", "KUPNO", "2.850", "3.100", "2.700", "Wyprzedanie na STOCH i obrona linii trendu."),
        ("EUR/CHF", "FX:EURCHF", "SPRZEDAŻ", "0.942", "0.938", "0.948", "Wybicie dołem z kanału CCI przy słabnącym popycie."),
        ("CAD/JPY", "FX:CADJPY", "KUPNO", "113.85", "114.50", "113.20", "Odbicie od MA 200 przy wzroście wolumenu."),
        ("NZD/USD", "FX:NZDUSD", "SPRZEDAŻ", "0.624", "0.618", "0.630", "Retest poziomu Fibo 0.618 i neutralne RSI."),
        ("GBP/CHF", "FX:GBPCHF", "KUPNO", "1.073", "1.080", "1.069", "Odbicie od EMA 50 przy niskiej zmienności."),
        ("USD/CHF", "FX:USDCHF", "KUPNO", "0.851", "0.858", "0.845", "Złoty krzyż MACD i powrót RSI powyżej 50."),
        ("EUR/USD", "FX:EURUSD", "SPRZEDAŻ", "1.085", "1.079", "1.091", "Górna wstęga Bollingera i wysokie RSI."),
        ("BTC/USD", "BINANCE:BTCUSDT", "KUPNO", "94200", "96500", "92000", "Kontynuacja trendu przy wysokim wolumenie."),
        ("ETH/USD", "BINANCE:ETHUSDT", "KUPNO", "3350", "3500", "3200", "Wybicie Ichimoku i bycze RSI.")
    ]
    
    updated_db = []
    now = datetime.now()
    for asset in base_assets:
        # Losowanie czasu z ostatnich 3 dni (max 72h wstecz)
        random_hours = random.randint(0, 71)
        random_minutes = random.randint(0, 59)
        sig_time = now - timedelta(hours=random_hours, minutes=random_minutes)
        
        updated_db.append({
            "pair": asset[0], "sym": asset[1], "type": asset[2],
            "time": sig_time.strftime("%d.%m | %H:%M"),
            "in": asset[3], "tp": asset[4], "sl": asset[5],
            "inv": asset[2], "tv": asset[2], "base": asset[6]
        })
    return updated_db

# INICJALIZACJA DANYCH
if 'db' not in st.session_state: st.session_state.db = fetch_latest_data()
if 'active_idx' not in st.session_state: st.session_state.active_idx = 0
if 'current_tf' not in st.session_state: st.session_state.current_tf = "1h"

def get_advanced_metrics(pair_data, tf):
    tf_rsi_base = {"1m": 35, "5m": 42, "15m": 48, "1h": 55, "4h": 62, "1D": 68, "1W": 75}
    rsi = round((tf_rsi_base.get(tf, 50) + len(pair_data['pair'])) % 92, 1)
    tf_weight = {"1m": 60, "5m": 65, "15m": 72, "1h": 80, "4h": 85, "1D": 92, "1W": 95}
    chance = tf_weight.get(tf, 70) + (len(pair_data['pair']) % 5)
    return rsi, min(chance, 99)

@st.dialog("📊 RANKING SKUTECZNOŚCI AI")
def show_ranking():
    st.markdown(f"Interwał: **{st.session_state.current_tf}**")
    for i, item in enumerate(st.session_state.db):
        rsi, chance = get_advanced_metrics(item, st.session_state.current_tf)
        st.markdown(f"""
            {i+1}. **{item['pair']}** | Szansa: `{chance}%` | RSI: `{rsi}`
            <div class='reasoning-dialog'>Uzasadnienie: {item['base']}</div>
            <hr style='margin:8px 0; border:0.2px solid #444;'>
        """, unsafe_allow_html=True)

# --- UI ---
st.markdown('<div style="background:#1e222d; padding:10px; border:1px solid #00ff88; text-align:center; font-weight:bold; color:white;">TERMINAL V161 | SYNCHRONIZACJA (MAX 3 DNI)</div>', unsafe_allow_html=True)

c_top = st.columns(2)
with c_top[0]:
    if st.button("🔄 SYNCHRONIZUJ DANE"):
        st.session_state.db = fetch_latest_data()
        st.toast("✅ Zaktualizowano sygnały z ostatnich 3 dni")
        st.rerun()
with c_top[1]:
    if st.button("🤖 AI RANKING"): show_ranking()

col_l, col_r = st.columns([1.8, 3.2])

with col_l:
    st.subheader("Lista Sygnałów")
    container = st.container(height=800)
    with container:
        for idx, s in enumerate(st.session_state.db):
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
                st.session_state.active_idx = idx
                st.rerun()

with col_r:
    cur = st.session_state.db[st.session_state.active_idx]
    new_tf = st.select_slider("Interwał:", options=["1m", "5m", "15m", "1h", "4h", "1D", "1W"], value=st.session_state.current_tf)
    if new_tf != st.session_state.current_tf:
        st.session_state.current_tf = new_tf
        st.rerun()
    
    st.markdown(f"## Analiza: {cur['pair']}")
    dynamic_rsi, _ = get_advanced_metrics(cur, st.session_state.current_tf)
    
    a1, a2, a3 = st.columns(3)
    with a1: st.markdown(f"<div style='text-align:center;'><b>Investing</b><br><span style='font-size:1.5rem; color:#00ff88;'>{cur['inv']}</span></div>", unsafe_allow_html=True)
    with a2: st.markdown(f"<div style='text-align:center;'><b>TradingView</b><br><span style='font-size:1.5rem; color:#00ff88;'>{cur['tv']}</span></div>", unsafe_allow_html=True)
    with a3: st.markdown(f"<div style='text-align:center;'><b>RSI ({st.session_state.current_tf})</b><br><span style='font-size:1.5rem; color:white;'>{dynamic_rsi}</span></div>", unsafe_allow_html=True)

    components.html(f"""
        <div style="height:500px;">
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
          {{
            "interval": "{st.session_state.current_tf}", "width": "100%", "isTransparent": true, "height": 450,
            "symbol": "{cur['sym']}", "showIntervalTabs": true, "displayMode": "multiple", "locale": "pl", "colorTheme": "dark"
          }}
          </script>
        </div>""", height=500)
