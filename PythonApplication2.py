import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timedelta
import random

# 1. KONFIGURACJA
st.set_page_config(layout="wide", page_title="TERMINAL V171", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .signal-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 6px solid #00ff88; }
    .entry-box { background: #000; padding: 10px; border-radius: 5px; color: #00ff88; font-family: 'Courier New'; text-align: center; border: 1px solid #00ff88; margin: 10px 0; font-size: 0.85rem; }
    .tg-btn { background-color: #0088cc !important; color: white !important; display: block; text-align: center; padding: 8px; border-radius: 5px; text-decoration: none; font-weight: bold; margin-top: 5px; font-size: 0.8rem; }
    div.stButton > button { background-color: #262730 !important; color: #00ff88 !important; border: 2px solid #00ff88 !important; font-weight: bold !important; width: 100%; }
    .header-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 2. SYMULACJA SCRAPERA Z PODANYCH ŹRÓDEŁ (January 12, 11, 10)
@st.cache_data
def scrape_all_sources():
    sources = ["signalsproviderfx", "top_tradingsignals", "VasilyTrading", "prosignalsfxx"]
    db = []
    now = datetime.now()
    
    # Dane specyficzne dla Twoich źródeł (np. AUD/CHF z 12.01)
    data_map = {
        0: [("AUD/CHF", "FX:AUDCHF"), ("NZD/CHF", "FX:NZDCHF"), ("XAU/USD", "OANDA:XAUUSD"), ("USD/JPY", "FX:USDJPY")], # DZISIAJ
        1: [("EUR/USD", "FX:EURUSD"), ("GBP/USD", "FX:GBPUSD"), ("US30", "TVC:US30"), ("BTC/USD", "BINANCE:BTCUSDT")], # WCZORAJ
        2: [("ETH/USD", "BINANCE:ETHUSDT"), ("GER40", "CAPITALCOM:GER40"), ("SOL/USD", "BINANCE:SOLUSDT"), ("WTI OIL", "TVC:USOIL")] # PRZEDWCZORAJ
    }

    for day_off in range(3):
        target_date = now - timedelta(days=day_off)
        d_key = target_date.strftime("%d.%m")
        
        # Pobieramy zestaw instrumentów dla konkretnego dnia
        daily_assets = data_map.get(day_off, [])
        
        for name, sym in daily_assets:
            h, m = random.randint(9, 19), random.randint(10, 50)
            db.append({
                "pair": name, "sym": sym, "type": random.choice(["KUPNO", "SPRZEDAŻ"]),
                "date_key": d_key,
                "full_date": f"{d_key} | {h:02d}:{m:02d}",
                "in": str(round(random.uniform(0.8, 100.0), 5)),
                "tp": "T1/T2", "sl": "STOP",
                "source": random.choice(sources)
            })
    return db

# 3. LOGIKA SESJI
if 'db' not in st.session_state: st.session_state.db = scrape_all_sources()
if 'selected_date' not in st.session_state: st.session_state.selected_date = datetime.now().strftime("%d.%m")
if 'current_tf' not in st.session_state: st.session_state.current_tf = "1h"

# Filtrowanie Danych
filtered_signals = [s for s in st.session_state.db if s['date_key'] == st.session_state.selected_date]

# Automatyczna zmiana aktywnej pary przy zmianie dnia
if not st.session_state.get('active_pair') or st.session_state.active_pair['date_key'] != st.session_state.selected_date:
    if filtered_signals: st.session_state.active_pair = filtered_signals[0]

# --- UI GŁÓWNE ---
st.markdown(f'<div style="background:#1e222d; padding:10px; border:1px solid #00ff88; text-align:center; font-weight:bold;">TERMINAL V171 | FILTR: {st.session_state.selected_date}</div>', unsafe_allow_html=True)

# Nawigacja Dniami
c_nav = st.columns([1, 1, 1, 1, 2])
labels = ["DZISIAJ", "WCZORAJ", "PRZEDWCZORAJ"]
for i, lab in enumerate(labels):
    d_val = (datetime.now() - timedelta(days=i)).strftime("%d.%m")
    if c_nav[i].button(f"{lab}\n{d_val}", key=f"btn_d_{i}"):
        st.session_state.selected_date = d_val
        st.rerun()

with c_nav[3]:
    if st.button("🔄 SYNC"):
        st.cache_data.clear()
        st.session_state.db = scrape_all_sources()
        st.rerun()

# Kolumny
col_l, col_r = st.columns([1.8, 3.2])

with col_l:
    st.subheader(f"Źródła: Telegram")
    container = st.container(height=750)
    with container:
        for idx, s in enumerate(filtered_signals):
            t_clr = "#00ff88" if "KUPNO" in s['type'] else "#ff4b4b"
            st.markdown(f"""
                <div class="signal-card">
                    <div class="header-row">
                        <span><b>{s['pair']}</b> <span style="color:{t_clr}">{s['type']}</span></span>
                        <span style="font-size:0.75rem; color:#888;">{s['full_date']}</span>
                    </div>
                    <div class="entry-box">WEJŚCIE: {s['in']} | {s['tp']} | {s['sl']}</div>
                    <a href="https://t.me/s/{s['source']}" class="tg-btn">✈ OTWÓRZ {s['source'].upper()}</a>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"📊 ANALIZA {s['pair']}", key=f"an_{idx}"):
                st.session_state.active_pair = s
                st.rerun()

with col_r:
    if st.session_state.get('active_pair'):
        cur = st.session_state.active_pair
        st.markdown(f"## {cur['pair']} - Analiza ({cur['date_key']})")
        st.session_state.current_tf = st.select_slider("Interwał:", options=["1m", "5m", "15m", "1h", "4h", "1D"], value=st.session_state.current_tf)
        
        # 3 ZEGARY TECHNICZNE (TradingView)
        components.html(f"""
            <div style="display: flex; justify-content: space-between; gap: 5px;">
                <div style="width: 33%;">
                    <p style="text-align:center; color:#888; font-size:12px; margin-bottom:0;">PODSUMOWANIE</p>
                    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
                    {{ "interval": "{st.session_state.current_tf}", "width": "100%", "isTransparent": true, "height": 380, "symbol": "{cur['sym']}", "locale": "pl", "colorTheme": "dark" }}
                    </script>
                </div>
                <div style="width: 33%;">
                    <p style="text-align:center; color:#888; font-size:12px; margin-bottom:0;">OSCYLATORY</p>
                    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
                    {{ "interval": "{st.session_state.current_tf}", "width": "100%", "isTransparent": true, "height": 380, "symbol": "{cur['sym']}", "locale": "pl", "colorTheme": "dark", "defaultColumn": "oscillators" }}
                    </script>
                </div>
                <div style="width: 33%;">
                    <p style="text-align:center; color:#888; font-size:12px; margin-bottom:0;">ŚREDNIE</p>
                    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
                    {{ "interval": "{st.session_state.current_tf}", "width": "100%", "isTransparent": true, "height": 380, "symbol": "{cur['sym']}", "locale": "pl", "colorTheme": "dark", "defaultColumn": "moving_averages" }}
                    </script>
                </div>
            </div>
        """, height=420)
    else:
        st.warning("Brak aktywnych sygnałów. Spróbuj zmienić dzień.")
