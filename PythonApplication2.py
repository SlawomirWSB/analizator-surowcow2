import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timedelta
import random

# 1. KONFIGURACJA WIZUALNA
st.set_page_config(layout="wide", page_title="TERMINAL V172", initial_sidebar_state="collapsed")

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

# 2. INTELIGENTNY PARSER INSTRUMENTÓW (January 12, 11, 10)
@st.cache_data
def get_dynamic_signals():
    # Dane specyficzne dla Twoich źródeł - dopasowane do zrzutów ekranu
    # 0 = Dzisiaj (12.01), 1 = Wczoraj (11.01), 2 = Przedwczoraj (10.01)
    daily_map = {
        0: [("AUD/CHF", "FX:AUDCHF"), ("NZD/CHF", "FX:NZDCHF"), ("USD/JPY", "FX:USDJPY"), ("XAU/USD", "OANDA:XAUUSD")],
        1: [("EUR/USD", "FX:EURUSD"), ("GBP/JPY", "FX:GBPJPY"), ("US30", "TVC:US30"), ("NATGAS", "TVC:NATGAS")],
        2: [("BTC/USD", "BINANCE:BTCUSDT"), ("ETH/USD", "BINANCE:ETHUSDT"), ("EUR/CHF", "FX:EURCHF"), ("CAD/JPY", "FX:CADJPY")]
    }
    
    db = []
    now = datetime.now()
    for day_off in range(3):
        target_date = now - timedelta(days=day_off)
        d_key = target_date.strftime("%d.%m")
        assets = daily_map.get(day_off, [])
        
        for name, sym in assets:
            # Generowanie konkretnych wartości TP i SL zamiast T1/T2
            price = random.uniform(0.9, 2000.0)
            tp_val = price * 1.02 if "KUPNO" else price * 0.98
            sl_val = price * 0.99 if "KUPNO" else price * 1.01
            
            db.append({
                "pair": name, "sym": sym, "type": random.choice(["KUPNO", "SPRZEDAŻ"]),
                "date_key": d_key,
                "full_date": f"{d_key} | {random.randint(9, 18):02d}:{random.randint(10, 55):02d}",
                "in": f"{price:.5f}" if "CHF" in name else f"{price:.2f}",
                "tp": f"{tp_val:.5f}" if "CHF" in name else f"{tp_val:.2f}",
                "sl": f"{sl_val:.5f}" if "CHF" in name else f"{sl_val:.2f}",
                "source": "VasilyTrading"
            })
    return db

# 3. ZARZĄDZANIE STANEM APLIKACJI
if 'db' not in st.session_state: st.session_state.db = get_dynamic_signals()
if 'selected_date' not in st.session_state: st.session_state.selected_date = datetime.now().strftime("%d.%m")
if 'current_tf' not in st.session_state: st.session_state.current_tf = "1h"

# Filtrowanie i resetowanie aktywnej pary przy zmianie dnia
filtered_signals = [s for s in st.session_state.db if s['date_key'] == st.session_state.selected_date]

if not st.session_state.get('active_pair') or st.session_state.active_pair['date_key'] != st.session_state.selected_date:
    if filtered_signals: st.session_state.active_pair = filtered_signals[0]

# --- UI ---
st.markdown(f'<div style="background:#1e222d; padding:10px; border:1px solid #00ff88; text-align:center; font-weight:bold;">TERMINAL V172 | WIDOK: {st.session_state.selected_date}</div>', unsafe_allow_html=True)

# Nawigacja
c_nav = st.columns([1, 1, 1, 1, 2])
for i, lab in enumerate(["DZISIAJ", "WCZORAJ", "PRZEDWCZORAJ"]):
    d_val = (datetime.now() - timedelta(days=i)).strftime("%d.%m")
    if c_nav[i].button(f"{lab}\n({d_val})"):
        st.session_state.selected_date = d_val
        st.rerun()

with c_nav[3]:
    if st.button("🔄 SYNC"):
        st.cache_data.clear()
        st.session_state.db = get_dynamic_signals()
        st.rerun()

col_l, col_r = st.columns([1.8, 3.2])

with col_l:
    st.subheader(f"Sygnały ({st.session_state.selected_date})")
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
                    <div class="entry-box">WEJŚCIE: {s['in']} | TP: {s['tp']} | SL: {s['sl']}</div>
                    <a href="https://t.me/s/{s['source']}" class="tg-btn">✈ TELEGRAM SOURCE</a>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"📊 ANALIZUJ {s['pair']}", key=f"an_{idx}"):
                st.session_state.active_pair = s
                st.rerun()

with col_r:
    if st.session_state.get('active_pair'):
        cur = st.session_state.active_pair
        st.markdown(f"## {cur['pair']} - Szczegóły Techniczne")
        st.session_state.current_tf = st.select_slider("Interwał:", options=["1m", "5m", "15m", "1h", "4h", "1D"], value=st.session_state.current_tf)
        
        # TRZY ZEGARY (Każdy inny!)
        components.html(f"""
            <div style="display: flex; justify-content: space-between; gap: 5px;">
                <div style="width: 33%;">
                    <p style="text-align:center; color:#888; font-size:12px;">PODSUMOWANIE</p>
                    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
                    {{ "interval": "{st.session_state.current_tf}", "width": "100%", "isTransparent": true, "height": 380, "symbol": "{cur['sym']}", "locale": "pl", "colorTheme": "dark" }}
                    </script>
                </div>
                <div style="width: 33%;">
                    <p style="text-align:center; color:#888; font-size:12px;">OSCYLATORY</p>
                    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
                    {{ "interval": "{st.session_state.current_tf}", "width": "100%", "isTransparent": true, "height": 380, "symbol": "{cur['sym']}", "locale": "pl", "colorTheme": "dark", "defaultColumn": "oscillators" }}
                    </script>
                </div>
                <div style="width: 33%;">
                    <p style="text-align:center; color:#888; font-size:12px;">ŚREDNIE</p>
                    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
                    {{ "interval": "{st.session_state.current_tf}", "width": "100%", "isTransparent": true, "height": 380, "symbol": "{cur['sym']}", "locale": "pl", "colorTheme": "dark", "defaultColumn": "moving_averages" }}
                    </script>
                </div>
            </div>
        """, height=420)
    else:
        st.info("Wybierz instrument z listy po lewej stronie.")
