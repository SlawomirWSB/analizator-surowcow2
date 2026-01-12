import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timedelta
import random

# 1. KONFIGURACJA WIZUALNA
st.set_page_config(layout="wide", page_title="TERMINAL V168", initial_sidebar_state="collapsed")

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
    </style>
    """, unsafe_allow_html=True)

# 2. GENEROWANIE DANYCH
@st.cache_data
def fetch_latest_data():
    base_assets = [
        ("XAU/USD", "OANDA:XAUUSD"), ("GBP/JPY", "FX:GBPJPY"), 
        ("US30", "TVC:US30"), ("NATGAS", "TVC:NATGAS"),
        ("EUR/CHF", "FX:EURCHF"), ("CAD/JPY", "FX:CADJPY")
    ]
    full_db = []
    now = datetime.now()
    for day_offset in range(3):
        target_date = now - timedelta(days=day_offset)
        d_str = target_date.strftime("%d.%m")
        for name, sym in base_assets:
            sig_time = f"{random.randint(8, 20):02d}:{random.randint(0, 59):02d}"
            full_db.append({
                "pair": name, "sym": sym, "type": random.choice(["KUPNO", "SPRZEDAŻ"]),
                "date_key": d_str, "full_date": f"{d_str} | {sig_time}",
                "in": f"{random.randint(100, 2000)}", "tp": "PROFIT", "sl": "LOSS",
                "inv": "SILNE KUPNO", "tv": "SILNE KUPNO", "base": "Technicals"
            })
    return full_db

# 3. LOGIKA SESJI
if 'db' not in st.session_state: st.session_state.db = fetch_latest_data()
if 'selected_date' not in st.session_state: st.session_state.selected_date = datetime.now().strftime("%d.%m")
if 'current_tf' not in st.session_state: st.session_state.current_tf = "1h"

# KLUCZOWE: Filtrowanie sygnałów na podstawie wybranej daty
filtered_signals = [s for s in st.session_state.db if s['date_key'] == st.session_state.selected_date]

if 'active_pair' not in st.session_state or st.session_state.active_pair['date_key'] != st.session_state.selected_date:
    st.session_state.active_pair = filtered_signals[0] if filtered_signals else None

# --- UI GŁÓWNE ---
st.markdown(f'<div style="background:#1e222d; padding:10px; border:1px solid #00ff88; text-align:center; font-weight:bold; color:white;">TERMINAL V168 | WIDOK: {st.session_state.selected_date}</div>', unsafe_allow_html=True)

c_top = st.columns([1, 1, 1, 1, 2])
day_labels = ["DZISIAJ", "WCZORAJ", "PRZEDWCZORAJ"]
for i, label in enumerate(day_labels):
    d_val = (datetime.now() - timedelta(days=i)).strftime("%d.%m")
    with c_top[i]:
        if st.button(f"{label}\n({d_val})", key=f"day_btn_{i}"):
            st.session_state.selected_date = d_val
            # Resetujemy aktywną parę przy zmianie dnia
            st.rerun()

with c_top[3]:
    if st.button("🔄 SYNC"):
        st.session_state.db = fetch_latest_data()
        st.rerun()

with c_top[4]:
    if st.button("🤖 AI RANKING"):
        @st.dialog("AI RANKING")
        def rnk():
            for s in filtered_signals: st.write(f"**{s['pair']}** - Szansa: 85%")
        rnk()

col_l, col_r = st.columns([1.8, 3.2])

with col_l:
    st.subheader(f"Sygnały")
    container = st.container(height=800)
    with container:
        for idx, s in enumerate(filtered_signals):
            t_clr = "#00ff88" if "KUPNO" in s['type'] else "#ff4b4b"
            st.markdown(f"""
                <div class="signal-card">
                    <div class="header-row">
                        <span><b>{s['pair']}</b> <span style="color:{t_clr}; margin-left:10px;">{s['type']}</span></span>
                        <span style="font-size:0.75rem; color:#888;">{s['full_date']}</span>
                    </div>
                    <div class="entry-box">IN: {s['in']} | TP: {s['tp']} | SL: {s['sl']}</div>
                    <a href="https://t.me/s/VasilyTrading" class="tg-btn">✈ TELEGRAM</a>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"📊 ANALIZA {s['pair']}", key=f"an_{idx}"):
                st.session_state.active_pair = s
                st.rerun()

with col_r:
    if st.session_state.active_pair:
        cur = st.session_state.active_pair
        st.markdown(f"## Analiza: {cur['pair']} ({cur['date_key']})")
        st.session_state.current_tf = st.select_slider("Interwał:", options=["1m", "5m", "15m", "1h", "4h", "1D"], value=st.session_state.current_tf)
        
        # Statystyki tekstowe
        a, b, c = st.columns(3)
        a.metric("Investing", cur['inv'])
        b.metric("TradingView", cur['tv'])
        c.metric("RSI (14)", "62")

        # PRZYWRÓCONE 3 ZEGARY (Widgety Techniczne)
        components.html(f"""
            <div style="display: flex; justify-content: space-between;">
                <div style="width: 32%;">
                    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
                    {{ "interval": "{st.session_state.current_tf}", "width": "100%", "isTransparent": true, "height": 400, "symbol": "{cur['sym']}", "locale": "pl", "colorTheme": "dark" }}
                    </script>
                </div>
                <div style="width: 32%;">
                    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
                    {{ "interval": "{st.session_state.current_tf}", "width": "100%", "isTransparent": true, "height": 400, "symbol": "{cur['sym']}", "locale": "pl", "colorTheme": "dark" }}
                    </script>
                </div>
                <div style="width: 32%;">
                    <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
                    {{ "interval": "{st.session_state.current_tf}", "width": "100%", "isTransparent": true, "height": 400, "symbol": "{cur['sym']}", "locale": "pl", "colorTheme": "dark" }}
                    </script>
                </div>
            </div>
        """, height=420)
    else:
        st.info("Wybierz instrument z listy.")
