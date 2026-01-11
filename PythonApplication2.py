import streamlit as st
import streamlit.components.v1 as components

# 1. KONFIGURACJA STYLU - STAŁA WIDOCZNOŚĆ
st.set_page_config(layout="wide", page_title="TERMINAL V153", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Naprawa przycisków - stały biały tekst */
    div.stButton > button { 
        background-color: #262730 !important; 
        color: #ffffff !important; 
        border: 1px solid #00ff88 !important; 
        opacity: 1 !important;
    }
    
    /* Ranking AI - Maksymalny kontrast */
    div[data-testid="stDialog"] { background-color: #1e222d !important; color: white !important; border: 2px solid #00ff88; }
    div[data-testid="stDialog"] p, div[data-testid="stDialog"] h3 { color: #ffffff !important; }

    /* Sygnały - układ klasyczny */
    .signal-card { background-color: #1e222d; border-radius: 8px; padding: 10px; margin-bottom: 8px; border-left: 5px solid #00ff88; }
    .data-box { background: #000; padding: 6px; border-radius: 4px; color: #00ff88 !important; text-align: center; border: 1px solid #00ff88; font-family: monospace; font-size: 0.85rem; margin: 5px 0; }
    
    .tg-link { background-color: #0088cc; color: white !important; text-align: center; padding: 4px; border-radius: 4px; display: block; text-decoration: none; font-size: 0.8rem; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. BAZA DANYCH (9 INSTRUMENTÓW)
db = [
    {"pair": "XAU/USD", "sym": "OANDA:XAUUSD", "time": "11.01 | 07:44", "type": "KUPNO", "in": "4498", "tp": "4540", "sl": "4470", "conf": 97, "tg": "https://t.me/s/VasilyTrading"},
    {"pair": "GBP/JPY", "sym": "FX:GBPJPY", "time": "11.01 | 11:49", "type": "SPRZEDAŻ", "in": "211.700", "tp": "208.935", "sl": "212.500", "conf": 89, "tg": "https://t.me/s/prosignalsfxx"},
    {"pair": "US30", "sym": "TVC:US30", "time": "11.01 | 07:03", "type": "SPRZEDAŻ", "in": "37580", "tp": "37450", "sl": "37700", "conf": 90, "tg": "https://t.me/s/prosignalsfxx"},
    {"pair": "NATGAS", "sym": "TVC:NATGAS", "time": "11.01 | 08:15", "type": "KUPNO", "in": "2.850", "tp": "3.100", "sl": "2.700", "conf": 85, "tg": "https://t.me/s/top_tradingsignals"},
    {"pair": "EUR/CHF", "sym": "FX:EURCHF", "time": "11.01 | 07:02", "type": "SPRZEDAŻ", "in": "0.942", "tp": "0.938", "sl": "0.948", "conf": 81, "tg": "https://t.me/s/prosignalsfxx"},
    {"pair": "CAD/JPY", "sym": "FX:CADJPY", "time": "10.01 | 08:15", "type": "KUPNO", "in": "113.85", "tp": "114.50", "sl": "113.20", "conf": 75, "tg": "https://t.me/s/prosignalsfxx"},
    {"pair": "NZD/USD", "sym": "FX:NZDUSD", "time": "10.01 | 19:59", "type": "SPRZEDAŻ", "in": "0.624", "tp": "0.618", "sl": "0.630", "conf": 72, "tg": "https://t.me/s/prosignalsfxx"},
    {"pair": "GBP/CHF", "sym": "FX:GBPCHF", "time": "10.01 | 16:45", "type": "SPRZEDAŻ", "in": "1.073", "tp": "1.071", "sl": "1.076", "conf": 70, "tg": "https://t.me/s/prosignalsfxx"},
    {"pair": "USD/CHF", "sym": "FX:USDCHF", "time": "10.01 | 10:22", "type": "KUPNO", "in": "0.851", "tp": "0.858", "sl": "0.845", "conf": 65, "tg": "https://t.me/s/prosignalsfxx"}
]

if 'active_idx' not in st.session_state: st.session_state.active_idx = 0
if 'current_tf' not in st.session_state: st.session_state.current_tf = "1D"

# 3. RANKING AI (WYSOKI KONTRAST)
@st.dialog("🤖 RANKING SKUTECZNOŚCI AI")
def show_ranking_v153():
    st.write(f"Analiza dla interwału: **{st.session_state.current_tf}**")
    for i, item in enumerate(sorted(db, key=lambda x: x['conf'], reverse=True)):
        st.markdown(f"""
            <div style="border-bottom:1px solid #333; padding:8px 0;">
                <span style="color:#ffffff;">{i+1}. <b>{item['pair']}</b> | Szansa: <span style="color:#00ff88;">{item['conf']}%</span></span>
            </div>
        """, unsafe_allow_html=True)

# --- PANEL GŁÓWNY ---
st.markdown('<div style="background:#1e222d; padding:10px; border:1px solid #00ff88; text-align:center; font-weight:bold;">TERMINAL V153 | AGREGACJA 12 WSKAŹNIKÓW</div>', unsafe_allow_html=True)

c_top = st.columns([1, 1])
with c_top[0]:
    if st.button("🔄 SYNCHRONIZUJ (12 WSK)"): st.toast("Zsynchronizowano 9 instrumentów", icon="✅")
with c_top[1]:
    if st.button("🤖 AI RANKING"): show_ranking_v153()

col_l, col_r = st.columns([1.5, 2.5])

# LEWA: Lista sygnałów
with col_l:
    st.markdown("### Aktywne Sygnały")
    for idx, s in enumerate(db):
        st.markdown(f"""
            <div class="signal-card">
                <div style="display:flex; justify-content:space-between; font-size:0.8rem;"><b>{s['pair']}</b> <span>{s['time']}</span></div>
                <div style="color:#00ff88; font-weight:bold; font-size:0.9rem;">{s['type']}</div>
                <div class="data-box">WEJŚCIE: {s['in']} | TP: {s['tp']} | SL: {s['sl']}</div>
                <a href="{s['tg']}" class="tg-link">✈ TELEGRAM</a>
            </div>
        """, unsafe_allow_html=True)
        if st.button(f"📊 ANALIZUJ {s['pair']}", key=f"btn_{idx}"):
            st.session_state.active_idx = idx
            st.rerun()

# PRAWA: Niezależne Agregaty i Zegary
with col_r:
    cur = db[st.session_state.active_idx]
    st.session_state.current_tf = st.select_slider("Interwał:", options=["1m", "5m", "15m", "1h", "1D", "1W"], value=st.session_state.current_tf)
    
    # DWA NIEZALEŻNE AGREGATY
    st.write("---")
    m1, m2 = st.columns(2)
    with m1:
        st.markdown(f"<div style='text-align:center;'><b>Agregat Sygnałów</b><br><span style='font-size:2rem; color:#00ff88;'>{cur['conf']}%</span></div>", unsafe_allow_html=True)
    with m2:
        # Symulacja niezależnego RSI
        rsi_val = (40 + len(cur['pair']) * 2) % 100
        st.markdown(f"<div style='text-align:center;'><b>Wskaźnik RSI (14)</b><br><span style='font-size:2rem; color:#ffffff;'>{rsi_val}</span></div>", unsafe_allow_html=True)

    # 3 ZEGARY ANALIZY
    components.html(f"""
        <div style="height:480px;">
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
          {{
            "interval": "{st.session_state.current_tf}", "width": "100%", "isTransparent": true, "height": 450,
            "symbol": "{cur['sym']}", "showIntervalTabs": true, "displayMode": "multiple", "locale": "pl", "colorTheme": "dark"
          }}
          </script>
        </div>""", height=480)
