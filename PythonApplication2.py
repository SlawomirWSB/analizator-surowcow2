import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timedelta
import random

# 1. KONFIGURACJA WIZUALNA
st.set_page_config(layout="wide", page_title="TERMINAL V170", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .signal-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 6px solid #00ff88; }
    .entry-box { background: #000; padding: 10px; border-radius: 5px; color: #00ff88; font-family: 'Courier New'; text-align: center; border: 1px solid #00ff88; margin: 10px 0; }
    .tg-btn { background-color: #0088cc !important; color: white !important; display: block; text-align: center; padding: 8px; border-radius: 5px; text-decoration: none; font-weight: bold; margin-top: 5px; }
    div.stButton > button { background-color: #262730 !important; color: #00ff88 !important; border: 2px solid #00ff88 !important; font-weight: bold !important; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# 2. GENERATOR DANYCH ZMIENNYCH DLA KAŻDEGO DNIA
@st.cache_data
def fetch_telegram_data():
    # Definiujemy różne pule instrumentów dla różnych dni
    pools = {
        0: [("XAU/USD", "OANDA:XAUUSD"), ("US30", "TVC:US30"), ("GBP/JPY", "FX:GBPJPY"), ("EUR/USD", "FX:EURUSD")],
        1: [("BTC/USD", "BINANCE:BTCUSDT"), ("ETH/USD", "BINANCE:ETHUSDT"), ("NATGAS", "TVC:NATGAS"), ("US100", "TVC:NDX")],
        2: [("EUR/CHF", "FX:EURCHF"), ("CAD/JPY", "FX:CADJPY"), ("AUD/USD", "FX:AUDUSD"), ("OIL", "TVC:USOIL")]
    }
    
    db = []
    now = datetime.now()
    for day_off in range(3):
        target_date = now - timedelta(days=day_off)
        d_str = target_date.strftime("%d.%m")
        # Wybieramy pulę na podstawie przesunięcia dnia
        current_pool = pools.get(day_off, pools[0])
        
        for name, sym in current_pool:
            sig_time = f"{random.randint(8, 21):02d}:{random.randint(0, 59):02d}"
            db.append({
                "pair": name, "sym": sym, "type": random.choice(["KUPNO", "SPRZEDAŻ"]),
                "date_key": d_str, 
                "full_date": f"{d_str} | {sig_time}",
                "in": str(random.randint(1000, 5000) / 10),
                "tp": "PROFIT ZONE", "sl": "STOP LOSS",
                "inv": "SILNE KUPNO", "tv": "NEUTRALNIE"
            })
    return db

# 3. SESJA I LOGIKA FILTROWANIA
if 'db' not in st.session_state: st.session_state.db = fetch_telegram_data()
if 'selected_date' not in st.session_state: st.session_state.selected_date = datetime.now().strftime("%d.%m")
if 'current_tf' not in st.session_state: st.session_state.current_tf = "1h"

# Pobieranie sygnałów dla WYBRANEGO dnia
filtered_signals = [s for s in st.session_state.db if s['date_key'] == st.session_state.selected_date]

# Automatyczny wybór pierwszej pary z nowej listy po zmianie dnia
if not st.session_state.get('active_pair') or st.session_state.active_pair['date_key'] != st.session_state.selected_date:
    if filtered_signals:
        st.session_state.active_pair = filtered_signals[0]

# --- UI ---
st.markdown(f'<div style="background:#1e222d; padding:10px; border:1px solid #00ff88; text-align:center; font-weight:bold;">TERMINAL V170 | DZIEŃ: {st.session_state.selected_date}</div>', unsafe_allow_html=True)

# Przyciski Dni
c_days = st.columns([1, 1, 1, 1, 2])
labels = ["DZISIAJ", "WCZORAJ", "PRZEDWCZORAJ"]
for i, lab in enumerate(labels):
    d_val = (datetime.now() - timedelta(days=i)).strftime("%d.%m")
    if c_days[i].button(f"{lab}\n({d_val})", key=f"d_{i}"):
        st.session_state.selected_date = d_val
        st.rerun()

with c_days[3]:
    if st.button("🔄 SYNC"):
        st.cache_data.clear()
        st.session_state.db = fetch_telegram_data()
        st.rerun()

col_l, col_r = st.columns([1.8, 3.2])

with col_l:
    st.subheader(f"Sygnały z dnia {st.session_state.selected_date}")
    container = st.container(height=750)
    with container:
        for idx, s in enumerate(filtered_signals):
            t_clr = "#00ff88" if "KUPNO" in s['type'] else "#ff4b4b"
            st.markdown(f"""
                <div class="signal-card">
                    <div style="display:flex; justify-content:space-between;">
                        <span><b>{s['pair']}</b> <span style="color:{t_clr}">{s['type']}</span></span>
                        <span style="font-size:0.75rem; color:#888;">{s['full_date']}</span>
                    </div>
                    <div class="entry-box">WEJŚCIE: {s['in']} | {s['tp']} | {s['sl']}</div>
                    <a href="https://t.me/s/VasilyTrading" class="tg-btn">✈ TELEGRAM</a>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"📊 ANALIZA {s['pair']}", key=f"an_{idx}_{s['pair']}"):
                st.session_state.active_pair = s
                st.rerun()

with col_r:
    if st.session_state.get('active_pair'):
        cur = st.session_state.active_pair
        st.markdown(f"## {cur['pair']} - Analiza Dnia {cur['date_key']}")
        st.session_state.current_tf = st.select_slider("Interwał:", options=["1m", "5m", "15m", "1h", "4h", "1D"], value=st.session_state.current_tf)
        
        # Statystyki tekstowe
        m1, m2, m3 = st.columns(3)
        m1.metric("Investing", cur['inv'])
        m2.metric("TradingView", cur['tv'])
        m3.metric("RSI (14)", "58")

        # TRZY RÓŻNE ZEGARY (Techniczne)
        components.html(f"""
            <div style="display: flex; justify-content: space-between; gap: 5px;">
                <div style="width: 33%;">
                    <p style="text-align:center; color:#888; margin-bottom:0;">PODSUMOWANIE</p>
                    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
                    {{ "interval": "{st.session_state.current_tf}", "width": "100%", "isTransparent": true, "height": 380, "symbol": "{cur['sym']}", "showIntervalTabs": false, "locale": "pl", "colorTheme": "dark" }}
                    </script>
                </div>
                <div style="width: 33%;">
                    <p style="text-align:center; color:#888; margin-bottom:0;">OSCYLATORY</p>
                    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
                    {{ "interval": "{st.session_state.current_tf}", "width": "100%", "isTransparent": true, "height": 380, "symbol": "{cur['sym']}", "showIntervalTabs": false, "locale": "pl", "colorTheme": "dark", "defaultColumn": "oscillators" }}
                    </script>
                </div>
                <div style="width: 33%;">
                    <p style="text-align:center; color:#888; margin-bottom:0;">ŚREDNIE KROCZĄCE</p>
                    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
                    {{ "interval": "{st.session_state.current_tf}", "width": "100%", "isTransparent": true, "height": 380, "symbol": "{cur['sym']}", "showIntervalTabs": false, "locale": "pl", "colorTheme": "dark", "defaultColumn": "moving_averages" }}
                    </script>
                </div>
            </div>
        """, height=420)
    else:
        st.warning("Brak danych dla wybranego dnia. Kliknij SYNC.")
