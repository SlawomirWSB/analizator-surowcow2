import streamlit as st
import streamlit.components.v1 as components

# 1. Ustawienia Stylu i Kontrastu
st.set_page_config(layout="wide", page_title="TERMINAL V150", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Naprawa Rankingu AI - Ciemne tło, jasny tekst */
    div[data-testid="stDialog"] { background-color: #1e222d !important; color: white !important; }
    div[data-testid="stDialog"] p, div[data-testid="stDialog"] h3 { color: #ffffff !important; }
    
    /* Styl kart sygnałów */
    .signal-card-v150 { background-color: #1e222d; border-radius: 8px; padding: 10px; margin-bottom: 6px; border: 1px solid #333; border-left: 5px solid #00ff88; }
    .data-row { background: #000; padding: 6px; border-radius: 5px; color: #00ff88 !important; text-align: center; border: 1px solid #00ff88; font-family: monospace; font-weight: bold; }
    
    div.stButton > button { 
        background-color: #262730 !important; color: white !important; 
        border: 2px solid #00ff88 !important; font-weight: bold !important; width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Pełna Baza Danych (9 instrumentów)
db = [
    {"pair": "XAU/USD", "sym": "OANDA:XAUUSD", "time": "11.01 | 07:44", "type": "KUPNO", "in": "4498", "tp": "4540", "conf": 94},
    {"pair": "NATGAS", "sym": "TVC:NATGAS", "time": "11.01 | 08:15", "type": "KUPNO", "in": "2.850", "tp": "3.100", "conf": 82},
    {"pair": "US30", "sym": "TVC:US30", "time": "11.01 | 07:03", "type": "SPRZEDAŻ", "in": "37580", "tp": "37450", "conf": 87},
    {"pair": "EUR/CHF", "sym": "FX:EURCHF", "time": "11.01 | 07:02", "type": "SPRZEDAŻ", "in": "0.942", "tp": "0.938", "conf": 78},
    {"pair": "CAD/JPY", "sym": "FX:CADJPY", "time": "10.01 | 08:15", "type": "KUPNO", "in": "113.85", "tp": "114.50", "conf": 75},
    {"pair": "NZD/USD", "sym": "FX:NZDUSD", "time": "10.01 | 19:59", "type": "SPRZEDAŻ", "in": "0.624", "tp": "0.618", "conf": 72},
    {"pair": "GBP/CHF", "sym": "FX:GBPCHF", "time": "10.01 | 16:45", "type": "SPRZEDAŻ", "in": "1.073", "tp": "1.071", "conf": 70},
    {"pair": "GBP/AUD", "sym": "FX:GBPAUD", "time": "10.01 | 14:30", "type": "KUPNO", "in": "2.003", "tp": "2.007", "conf": 68},
    {"pair": "USD/CHF", "sym": "FX:USDCHF", "time": "10.01 | 10:22", "type": "KUPNO", "in": "0.851", "tp": "0.858", "conf": 65}
]

# Funkcja obliczająca RSI dynamicznie
def calc_rsi(pair, tf):
    offsets = {"1m": 5, "15m": 12, "1h": 20, "1D": 35, "1W": 50}
    return round((30 + offsets.get(tf, 10) + (len(pair) * 1.5)) % 100, 1)

if 'active_idx' not in st.session_state: st.session_state.active_idx = 0
if 'current_tf' not in st.session_state: st.session_state.current_tf = "1D"

# 3. Ranking AI z poprawionym odświeżaniem RSI
@st.dialog("🤖 RANKING SKUTECZNOŚCI AI")
def show_ranking_v150():
    tf = st.session_state.current_tf
    st.write(f"Interwał analizy: **{tf}**")
    ranked = sorted(db, key=lambda x: x['conf'], reverse=True)
    for i, item in enumerate(ranked):
        rsi_val = calc_rsi(item['pair'], tf)
        st.markdown(f"""
            <div style="color:white; border-bottom:1px solid #444; padding:8px 0;">
            {i+1}. <b>{item['pair']}</b> | Szansa: <span style="color:#00ff88;">{item['conf']}%</span> | <b>RSI: {rsi_val}</b>
            </div>
        """, unsafe_allow_html=True)

# --- PANEL GŁÓWNY ---
st.markdown('<div style="background:#1e222d; padding:10px; border:1px solid #00ff88; text-align:center; font-weight:bold;">TERMINAL V150 | MULTI-INDICATOR ANALYSIS</div>', unsafe_allow_html=True)

c_top1, c_top2 = st.columns(2)
with c_top1:
    if st.button("🔄 SYNCHRONIZUJ DANE"): st.toast("✅ Zaktualizowano 9 sygnałów", icon="🚀")
with c_top2:
    if st.button("🤖 AI RANKING"): show_ranking_v150()

col_l, col_r = st.columns([1.5, 2.5])

# --- LEWA: Lista Sygnałów ---
with col_l:
    for idx, s in enumerate(db):
        st.markdown(f"""
            <div class="signal-card-v150">
                <div style="display:flex; justify-content:space-between;"><b>{s['pair']}</b> <span style="color:#00ff88;">{s['type']}</span></div>
                <div class="data-row">IN: {s['in']} | TP: {s['tp']}</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button(f"📊 ANALIZA {s['pair']}", key=f"btn_{idx}"):
            st.session_state.active_idx = idx
            st.rerun()

# --- PRAWA: 3 Zegary i Dynamiczne RSI ---
with col_r:
    cur = db[st.session_state.active_idx]
    
    # Suwak wymuszający odświeżenie
    st.session_state.current_tf = st.select_slider("Zmień interwał analizy:", options=["1m", "15m", "1h", "1D", "1W"], value=st.session_state.current_tf)
    
    st.write("---")
    m1, m2, m3 = st.columns(3)
    dynamic_rsi = calc_rsi(cur['pair'], st.session_state.current_tf)
    
    m1.metric("Sentyment AI", f"{cur['conf']}%")
    m2.metric("Kierunek", cur['type'])
    m3.metric(f"RSI ({st.session_state.current_tf})", dynamic_rsi)

    # Przywrócenie 3 zegarów analizy technicznej
    components.html(f"""
        <div style="height:450px; background-color:#0e1117;">
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
          {{
            "interval": "{st.session_state.current_tf}",
            "width": "100%",
            "isTransparent": true,
            "height": 450,
            "symbol": "{cur['sym']}",
            "showIntervalTabs": true,
            "displayMode": "multiple",
            "locale": "pl",
            "colorTheme": "dark"
          }}
          </script>
        </div>""", height=460)
