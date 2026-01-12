import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timedelta
import random

# 1. KONFIGURACJA WIZUALNA
st.set_page_config(layout="wide", page_title="TERMINAL V169", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .signal-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 6px solid #00ff88; }
    .entry-box { background: #000; padding: 10px; border-radius: 5px; color: #00ff88; font-family: 'Courier New'; text-align: center; border: 1px solid #00ff88; margin: 10px 0; }
    .tg-btn { background-color: #0088cc !important; color: white !important; display: block; text-align: center; padding: 8px; border-radius: 5px; text-decoration: none; font-weight: bold; margin-top: 5px; }
    div.stButton > button { background-color: #262730 !important; color: #00ff88 !important; border: 2px solid #00ff88 !important; font-weight: bold !important; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# 2. POBIERANIE I PARSOWANIE DAT Z TELEGRAM
@st.cache_data(ttl=300)
def fetch_telegram_data():
    # Symulacja pobierania z https://t.me/s/signalsproviderfx i innych
    assets = [("XAU/USD", "OANDA:XAUUSD"), ("GBP/JPY", "FX:GBPJPY"), ("US30", "TVC:US30"), ("NATGAS", "TVC:NATGAS")]
    db = []
    now = datetime.now()
    
    for day_off in range(3):
        target_date = now - timedelta(days=day_off)
        date_str = target_date.strftime("%d.%m") # Np. 12.01
        
        for name, sym in assets:
            h, m = random.randint(8, 20), random.randint(0, 59)
            db.append({
                "pair": name, "sym": sym, "type": random.choice(["KUPNO", "SPRZEDAŻ"]),
                "date_key": date_str, 
                "full_date": f"{date_str} | {h:02d}:{m:02d}",
                "in": "4498" if "XAU" in name else "211.700",
                "tp": "4540" if "XAU" in name else "208.935",
                "sl": "4470" if "XAU" in name else "212.500",
                "inv": "SILNE KUPNO", "tv": "KUPNO"
            })
    return db

# 3. ZARZĄDZANIE SESJĄ I FILTROWANIEM
if 'db' not in st.session_state: st.session_state.db = fetch_telegram_data()
if 'selected_date' not in st.session_state: st.session_state.selected_date = datetime.now().strftime("%d.%m")
if 'current_tf' not in st.session_state: st.session_state.current_tf = "1h"

# Filtracja sygnałów dla wybranego dnia
filtered_signals = [s for s in st.session_state.db if s['date_key'] == st.session_state.selected_date]

# Bezpieczne ustawienie aktywnej pary (naprawa KeyError)
if 'active_pair' not in st.session_state or st.session_state.active_pair['date_key'] != st.session_state.selected_date:
    st.session_state.active_pair = filtered_signals[0] if filtered_signals else None

# --- UI ---
st.markdown(f'<div style="background:#1e222d; padding:10px; border:1px solid #00ff88; text-align:center; font-weight:bold;">TERMINAL V169 | DATA: {st.session_state.selected_date}</div>', unsafe_allow_html=True)

# Przyciski Dni
c_days = st.columns([1, 1, 1, 1, 2])
labels = ["DZISIAJ", "WCZORAJ", "PRZEDWCZORAJ"]
for i, lab in enumerate(labels):
    d_val = (datetime.now() - timedelta(days=i)).strftime("%d.%m")
    if c_days[i].button(f"{lab}\n({d_val})"):
        st.session_state.selected_date = d_val
        st.rerun()

if c_days[3].button("🔄 SYNC"):
    st.session_state.db = fetch_telegram_data()
    st.rerun()

col_l, col_r = st.columns([1.8, 3.2])

with col_l:
    st.subheader("Lista Sygnałów")
    container = st.container(height=750)
    with container:
        for idx, s in enumerate(filtered_signals):
            clr = "#00ff88" if "KUPNO" in s['type'] else "#ff4b4b"
            st.markdown(f"""
                <div class="signal-card">
                    <div style="display:flex; justify-content:space-between; font-size:0.9rem;">
                        <span><b>{s['pair']}</b> <span style="color:{clr}">{s['type']}</span></span>
                        <span style="color:#888;">{s['full_date']}</span>
                    </div>
                    <div class="entry-box">IN: {s['in']} | TP: {s['tp']} | SL: {s['sl']}</div>
                    <a href="https://t.me/s/VasilyTrading" class="tg-btn">✈ TELEGRAM</a>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"📊 ANALIZUJ {s['pair']}", key=f"btn_{idx}"):
                st.session_state.active_pair = s
                st.rerun()

with col_r:
    if st.session_state.active_pair:
        cur = st.session_state.active_pair
        st.markdown(f"### Analiza Techniczna: {cur['pair']} ({cur['date_key']})")
        st.session_state.current_tf = st.select_slider("Interwał (TF):", options=["1m", "5m", "15m", "1h", "4h", "1D"], value=st.session_state.current_tf)
        
        # Statystyki
        m1, m2, m3 = st.columns(3)
        m1.metric("Investing.com", cur['inv'])
        m2.metric("TradingView", cur['tv'])
        m3.metric("RSI (14)", "64")

        # PRZYWRÓCENIE 3 ZEGARÓW
        components.html(f"""
            <div style="display: flex; justify-content: space-between; gap: 10px;">
                <div style="width: 32%;">
                    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
                    {{ "interval": "{st.session_state.current_tf}", "width": "100%", "isTransparent": true, "height": 380, "symbol": "{cur['sym']}", "locale": "pl", "colorTheme": "dark" }}
                    </script>
                </div>
                <div style="width: 32%;">
                    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
                    {{ "interval": "{st.session_state.current_tf}", "width": "100%", "isTransparent": true, "height": 380, "symbol": "{cur['sym']}", "locale": "pl", "colorTheme": "dark" }}
                    </script>
                </div>
                <div style="width: 32%;">
                    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
                    {{ "interval": "{st.session_state.current_tf}", "width": "100%", "isTransparent": true, "height": 380, "symbol": "{cur['sym']}", "locale": "pl", "colorTheme": "dark" }}
                    </script>
                </div>
            </div>
        """, height=400)
    else:
        st.info("Wybierz instrument, aby wyświetlić zegary analizy.")
