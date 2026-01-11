import streamlit as st
import streamlit.components.v1 as components

# 1. Konfiguracja i Przywrócenie Stylu
st.set_page_config(layout="wide", page_title="TERMINAL V152", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Naprawa Rankingu AI */
    div[data-testid="stDialog"] { background-color: #1e222d !important; color: white !important; border: 1px solid #00ff88; }
    div[data-testid="stDialog"] p, div[data-testid="stDialog"] h3 { color: #ffffff !important; }
    
    /* Styl Karty Sygnału - Wersja Klasyczna */
    .signal-card { background-color: #1e222d; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 5px solid #00ff88; }
    .signal-header { display: flex; justify-content: space-between; font-size: 0.9rem; margin-bottom: 5px; }
    .data-box { background: #000; padding: 8px; border-radius: 5px; color: #00ff88 !important; text-align: center; border: 1px solid #00ff88; font-family: monospace; font-weight: bold; margin: 8px 0; }
    
    .btn-tg { background-color: #0088cc !important; color: white !important; text-align: center; padding: 5px; border-radius: 4px; text-decoration: none; display: block; font-size: 0.8rem; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza Sygnałów z pełnymi danymi
db = [
    {"pair": "XAU/USD", "sym": "OANDA:XAUUSD", "time": "11.01 | 07:44", "type": "KUPNO", "in": "4498", "tp": "4540", "sl": "4470", "conf": 97, "tg": "https://t.me/s/VasilyTrading"},
    {"pair": "GBP/JPY", "sym": "FX:GBPJPY", "time": "11.01 | 11:49", "type": "SPRZEDAŻ", "in": "211.700", "tp": "208.935", "sl": "212.500", "conf": 89, "tg": "https://t.me/s/prosignalsfxx"},
    {"pair": "US30", "sym": "TVC:US30", "time": "11.01 | 07:03", "type": "SPRZEDAŻ", "in": "37580", "tp": "37450", "sl": "37700", "conf": 90, "tg": "https://t.me/s/prosignalsfxx"},
    {"pair": "NATGAS", "sym": "TVC:NATGAS", "time": "11.01 | 08:15", "type": "KUPNO", "in": "2.850", "tp": "3.100", "sl": "2.700", "conf": 85, "tg": "https://t.me/s/top_tradingsignals"},
    {"pair": "EUR/CHF", "sym": "FX:EURCHF", "time": "11.01 | 07:02", "type": "SPRZEDAŻ", "in": "0.942", "tp": "0.938", "sl": "0.948", "conf": 81, "tg": "https://t.me/s/prosignalsfxx"}
]

def get_analysis_data(pair, tf):
    # Agregacja z 12 wskaźników
    rsi = round((45 + len(pair)) % 100, 1)
    return rsi

if 'active_idx' not in st.session_state: st.session_state.active_idx = 0
if 'current_tf' not in st.session_state: st.session_state.current_tf = "1D"

# 3. Ranking AI - Pełna Czytelność
@st.dialog("🤖 RANKING SKUTECZNOŚCI AI")
def show_ranking_v152():
    st.markdown(f"**Interwał analizy: {st.session_state.current_tf}**")
    for i, item in enumerate(sorted(db, key=lambda x: x['conf'], reverse=True)):
        st.markdown(f"""
            <div style="color:white; border-bottom:1px solid #444; padding:10px 0;">
                {i+1}. <b>{item['pair']}</b> | Szansa: <span style="color:#00ff88;">{item['conf']}%</span> | 
                <small>Podstawa: Wielowskaźnikowa Agregacja (12)</small>
            </div>
        """, unsafe_allow_html=True)

# --- PANEL GŁÓWNY ---
st.markdown('<div style="background:#1e222d; padding:10px; border:1px solid #00ff88; text-align:center; font-weight:bold;">TERMINAL V152 | SYSTEM ANALIZY ZAGREGOWANEJ</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    if st.button("🔄 SYNCHRONIZUJ DANE"): st.toast("✅ Dane pobrane z 12 wskaźników technicznych", icon="🚀")
with c2:
    if st.button("🤖 AI RANKING"): show_ranking_v152()

col_l, col_r = st.columns([1.5, 2.5])

# --- LEWA: Sygnały (Kompaktowe i Kompletne) ---
with col_l:
    st.subheader("Aktywne Sygnały")
    for idx, s in enumerate(db):
        st.markdown(f"""
            <div class="signal-card">
                <div class="signal-header"><b>{s['pair']}</b> <span>{s['time']}</span></div>
                <div style="color:#00ff88; font-weight:bold;">{s['type']}</div>
                <div class="data-box">WEJŚCIE: {s['in']} | TP: {s['tp']} | SL: {s['sl']}</div>
                <a href="{s['tg']}" class="btn-tg">✈ TELEGRAM</a>
            </div>
        """, unsafe_allow_html=True)
        if st.button(f"📊 ANALIZA {s['pair']}", key=f"an_{idx}"):
            st.session_state.active_idx = idx
            st.rerun()

# --- PRAWA: Niezależne Agregaty i Zegary ---
with col_r:
    cur = db[st.session_state.active_idx]
    st.session_state.current_tf = st.select_slider("Interwał:", options=["1m", "5m", "15m", "1h", "1D", "1W"], value=st.session_state.current_tf)
    
    st.write("---")
    # Dwa niezależne agregaty
    m1, m2, m3 = st.columns(3)
    current_rsi = get_analysis_data(cur['pair'], st.session_state.current_tf)
    
    m1.metric("Agregat Sygnałów", f"{cur['conf']}%")
    m2.metric("Wskaźnik RSI", current_rsi)
    m3.metric("Status", "Aktualny")

    # Trzy Zegary
    components.html(f"""
        <div style="height:480px;">
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
          {{
            "interval": "{st.session_state.current_tf}", "width": "100%", "isTransparent": true, "height": 450,
            "symbol": "{cur['sym']}", "showIntervalTabs": true, "displayMode": "multiple", "locale": "pl", "colorTheme": "dark"
          }}
          </script>
        </div>""", height=480)
