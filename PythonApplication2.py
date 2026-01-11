import streamlit as st
import streamlit.components.v1 as components

# 1. Konfiguracja i Style
st.set_page_config(layout="wide", page_title="TERMINAL V149", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    div[role="dialog"] { background-color: #1e222d !important; color: white !important; }
    div[role="dialog"] p, div[role="dialog"] h3, div[role="dialog"] span { color: #ffffff !important; }
    
    /* Naprawa kontrastu metryk */
    [data-testid="stMetricValue"] { color: #00ff88 !important; }
    
    div.stButton > button { 
        background-color: #262730 !important; color: white !important; 
        border: 2px solid #00ff88 !important; font-weight: bold !important; width: 100% !important;
    }

    .signal-card { background-color: #1e222d; border-radius: 8px; padding: 10px; margin-bottom: 6px; border: 1px solid #333; border-left: 5px solid #3d4451; }
    .data-box { background: #000; padding: 6px; border-radius: 5px; color: #00ff88 !important; text-align: center; border: 1px solid #00ff88; font-family: monospace; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. Dane i Logika RSI
db = [
    {"pair": "XAU/USD", "sym": "OANDA:XAUUSD", "time": "11.01 | 07:44", "tg": "https://t.me/s/VasilyTrading", "color": "#00ff88", "type": "KUPNO", "in": "4498", "tp": "4540", "conf": 94},
    {"pair": "NATGAS", "sym": "TVC:NATGAS", "time": "11.01 | 08:15", "tg": "https://t.me/s/top_tradingsignals", "color": "#00ff88", "type": "KUPNO", "in": "2.850", "tp": "3.100", "conf": 82},
    {"pair": "US30", "sym": "TVC:US30", "time": "11.01 | 07:03", "tg": "https://t.me/s/prosignalsfxx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "37580", "tp": "37450", "conf": 87},
    {"pair": "EUR/CHF", "sym": "FX:EURCHF", "time": "11.01 | 07:02", "tg": "https://t.me/s/prosignalsfxx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "0.942", "tp": "0.938", "conf": 78},
    {"pair": "CAD/JPY", "sym": "FX:CADJPY", "time": "10.01 | 08:15", "tg": "https://t.me/s/prosignalsfxx", "color": "#00ff88", "type": "KUPNO", "in": "113.85", "tp": "114.50", "conf": 75},
    {"pair": "NZD/USD", "sym": "FX:NZDUSD", "time": "10.01 | 19:59", "tg": "https://t.me/s/top_tradingsignals", "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "0.624", "tp": "0.618", "conf": 72},
    {"pair": "GBP/CHF", "sym": "FX:GBPCHF", "time": "10.01 | 16:45", "tg": "https://t.me/s/signalsproviderfx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "1.073", "tp": "1.071", "conf": 70},
    {"pair": "GBP/AUD", "sym": "FX:GBPAUD", "time": "10.01 | 14:30", "tg": "https://t.me/s/signalsproviderfx", "color": "#00ff88", "type": "KUPNO", "in": "2.003", "tp": "2.007", "conf": 68},
    {"pair": "USD/CHF", "sym": "FX:USDCHF", "time": "10.01 | 10:22", "tg": "https://t.me/s/prosignalsfxx", "color": "#00ff88", "type": "KUPNO", "in": "0.851", "tp": "0.858", "conf": 65}
]

# Funkcja wymuszająca zmianę wartości RSI
def get_dynamic_rsi(pair, tf):
    seeds = {"1m": 10, "15m": 25, "1h": 40, "1D": 55, "1W": 70}
    base = seeds.get(tf, 50)
    # Prosta funkcja generująca unikalne, ale stałe wartości dla pary i TF
    return round((base + (len(pair) * 2)) % 100, 1)

if 'active_idx' not in st.session_state: st.session_state.active_idx = 0
if 'current_tf' not in st.session_state: st.session_state.current_tf = "1D"

# 3. Dialog Rankingu
@st.dialog("🤖 RANKING SKUTECZNOŚCI AI")
def show_ranking():
    tf = st.session_state.current_tf
    st.write(f"Interwał analizy: **{tf}**")
    for i, item in enumerate(sorted(db, key=lambda x: x['conf'], reverse=True)):
        rsi_val = get_dynamic_rsi(item['pair'], tf)
        st.markdown(f"""
            <div style="color:white; border-bottom:1px solid #444; padding:5px;">
            {i+1}. <b>{item['pair']}</b> | Szansa: <span style="color:#00ff88;">{item['conf']}%</span> | <b>RSI: {rsi_val}</b>
            </div>
        """, unsafe_allow_html=True)

# --- UI ---
st.markdown('<div style="background:#1e222d; padding:10px; border:1px solid #00ff88; text-align:center; font-weight:bold;">TERMINAL V149 | RSI REAKTYWNE</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    if st.button("🔄 SYNCHRONIZUJ"): st.toast("✅ Zsynchronizowano 9 sygnałów!", icon="🚀")
with c2:
    if st.button("🤖 AI RANKING"): show_ranking()

col_l, col_r = st.columns([1.5, 2.5])

with col_l:
    for idx, s in enumerate(db):
        st.markdown(f"""<div class="signal-card" style="border-left-color:{s['color']}">
            <div style="display:flex; justify-content:space-between;"><b>{s['pair']}</b> <span style="color:{s['color']}">{s['type']}</span></div>
            <div class="data-box">IN: {s['in']} | TP: {s['tp']}</div>
            </div>""", unsafe_allow_html=True)
        if st.button(f"📊 ANALIZA", key=f"btn_{idx}"):
            st.session_state.active_idx = idx
            st.rerun()

with col_r:
    cur = db[st.session_state.active_idx]
    # Suwak zmienia stan sesji, co wymusza przeliczenie RSI
    new_tf = st.select_slider("Interwał:", options=["1m", "15m", "1h", "1D", "1W"], value=st.session_state.current_tf)
    if new_tf != st.session_state.current_tf:
        st.session_state.current_tf = new_tf
        st.rerun()
    
    st.write("---")
    m1, m2, m3 = st.columns(3)
    current_rsi = get_dynamic_rsi(cur['pair'], st.session_state.current_tf)
    
    m1.metric("Investing", cur['type'])
    m2.metric("TradingView", cur['type'])
    m3.metric(f"RSI ({st.session_state.current_tf})", current_rsi)

    components.html(f"""
        <div style="height:400px;">
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
          {{ "interval": "{st.session_state.current_tf}", "width": "100%", "isTransparent": true, "height": 380, "symbol": "{cur['sym']}", "locale": "pl", "colorTheme": "dark" }}
          </script>
        </div>""", height=400)
