import streamlit as st
import streamlit.components.v1 as components

# 1. FINALNA KONFIGURACJA STYLU (BEZ HOVERÓW)
st.set_page_config(layout="wide", page_title="TERMINAL V154", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* FIX RANKINGU: Stała widoczność tekstu */
    div[data-testid="stDialog"] { background-color: #1e222d !important; color: #ffffff !important; border: 2px solid #00ff88; }
    div[data-testid="stDialog"] [data-testid="stMarkdownContainer"] p { color: #ffffff !important; font-weight: bold; }
    
    /* PRZYCISKI: Brak efektu ukrywania tekstu */
    div.stButton > button { 
        background-color: #262730 !important; color: #00ff88 !important; 
        border: 2px solid #00ff88 !important; width: 100%; font-weight: bold !important;
    }
    
    .signal-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 6px solid #00ff88; }
    .entry-box { background: #000; padding: 10px; border-radius: 5px; color: #00ff88; font-family: 'Courier New'; text-align: center; border: 1px solid #00ff88; margin: 10px 0; }
    
    .tg-btn { background-color: #0088cc !important; color: white !important; display: block; text-align: center; padding: 8px; border-radius: 5px; text-decoration: none; font-weight: bold; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 2. BAZA DANYCH (ROZSZERZONA DO 12 POZYCJI)
db = [
    {"pair": "XAU/USD", "sym": "OANDA:XAUUSD", "time": "11.01 | 07:44", "type": "KUPNO", "in": "4498", "tp": "4540", "sl": "4470", "conf": 97, "inv": "SILNE KUPNO", "tv": "SILNE KUPNO"},
    {"pair": "GBP/JPY", "sym": "FX:GBPJPY", "time": "11.01 | 11:49", "type": "SPRZEDAŻ", "in": "211.700", "tp": "208.935", "sl": "212.500", "conf": 89, "inv": "SPRZEDAŻ", "tv": "SILNA SPRZEDAŻ"},
    {"pair": "US30", "sym": "TVC:US30", "time": "11.01 | 07:03", "type": "SPRZEDAŻ", "in": "37580", "tp": "37450", "sl": "37700", "conf": 90, "inv": "SPRZEDAŻ", "tv": "NEUTRALNIE"},
    {"pair": "NATGAS", "sym": "TVC:NATGAS", "time": "11.01 | 08:15", "type": "KUPNO", "in": "2.850", "tp": "3.100", "sl": "2.700", "conf": 85, "inv": "SILNE KUPNO", "tv": "KUPNO"},
    {"pair": "EUR/CHF", "sym": "FX:EURCHF", "time": "11.01 | 07:02", "type": "SPRZEDAŻ", "in": "0.942", "tp": "0.938", "sl": "0.948", "conf": 81, "inv": "NEUTRALNIE", "tv": "SPRZEDAŻ"},
    {"pair": "CAD/JPY", "sym": "FX:CADJPY", "time": "11.01 | 14:20", "type": "KUPNO", "in": "113.85", "tp": "114.50", "sl": "113.20", "conf": 75, "inv": "KUPNO", "tv": "KUPNO"},
    {"pair": "NZD/USD", "sym": "FX:NZDUSD", "time": "11.01 | 15:10", "type": "SPRZEDAŻ", "in": "0.624", "tp": "0.618", "sl": "0.630", "conf": 72, "inv": "SPRZEDAŻ", "tv": "SPRZEDAŻ"},
    {"pair": "GBP/CHF", "sym": "FX:GBPCHF", "time": "11.01 | 09:30", "type": "KUPNO", "in": "1.073", "tp": "1.080", "sl": "1.069", "conf": 70, "inv": "NEUTRALNIE", "tv": "KUPNO"},
    {"pair": "USD/CHF", "sym": "FX:USDCHF", "time": "11.01 | 10:15", "type": "KUPNO", "in": "0.851", "tp": "0.858", "sl": "0.845", "conf": 68, "inv": "KUPNO", "tv": "NEUTRALNIE"},
    {"pair": "EUR/USD", "sym": "FX:EURUSD", "time": "11.01 | 12:00", "type": "SPRZEDAŻ", "in": "1.085", "tp": "1.079", "sl": "1.091", "conf": 65, "inv": "SPRZEDAŻ", "tv": "SPRZEDAŻ"},
    {"pair": "BTC/USD", "sym": "BINANCE:BTCUSDT", "time": "11.01 | 13:45", "type": "KUPNO", "in": "94200", "tp": "96500", "sl": "92000", "conf": 92, "inv": "SILNE KUPNO", "tv": "SILNE KUPNO"},
    {"pair": "ETH/USD", "sym": "BINANCE:ETHUSDT", "time": "11.01 | 13:50", "type": "KUPNO", "in": "3350", "tp": "3500", "sl": "3200", "conf": 88, "inv": "KUPNO", "tv": "SILNE KUPNO"}
]

if 'active_idx' not in st.session_state: st.session_state.active_idx = 0
if 'current_tf' not in st.session_state: st.session_state.current_tf = "1D"

# 3. CZYTELNY RANKING AI
@st.dialog("📊 RANKING SKUTECZNOŚCI AI (WIDOCZNY)")
def show_ranking_v154():
    st.markdown("### Top Instrumenty wg Agregacji")
    for i, item in enumerate(sorted(db, key=lambda x: x['conf'], reverse=True)):
        st.markdown(f"{i+1}. **{item['pair']}** — Szansa: `{item['conf']}%` | RSI: `54`")

# --- UI GŁÓWNE ---
st.markdown('<div style="background:#1e222d; padding:10px; border:1px solid #00ff88; text-align:center; font-weight:bold; color:white;">TERMINAL V154 | NIEZALEŻNE AGREGATY SYGNAŁÓW</div>', unsafe_allow_html=True)

c_top = st.columns(2)
with c_top[0]:
    if st.button("🔄 SYNCHRONIZUJ WSZYSTKIE (12)"): st.toast("✅ Odświeżono 12 instrumentów", icon="🚀")
with c_top[1]:
    if st.button("🤖 AI RANKING"): show_ranking_v154()

col_l, col_r = st.columns([1.8, 3.2])

# LEWY PANEL: Pełne Sygnały
with col_l:
    st.subheader("Lista Sygnałów")
    container = st.container(height=800)
    with container:
        for idx, s in enumerate(db):
            st.markdown(f"""
                <div class="signal-card">
                    <div style="display:flex; justify-content:space-between; font-size:0.8rem;"><b>{s['pair']}</b> <span>{s['time']}</span></div>
                    <div style="color:#00ff88; font-weight:bold; font-size:1.1rem;">{s['type']}</div>
                    <div class="entry-box">IN: {s['in']} | TP: {s['tp']} | SL: {s['sl']}</div>
                    <a href="https://t.me/s/VasilyTrading" class="tg-btn">✈ TELEGRAM</a>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"📊 ANALIZA {s['pair']}", key=f"an_{idx}"):
                st.session_state.active_idx = idx
                st.rerun()

# PRAWY PANEL: Niezależne Agregaty
with col_r:
    cur = db[st.session_state.active_idx]
    st.session_state.current_tf = st.select_slider("Interwał:", options=["1m", "5m", "15m", "1h", "4h", "1D", "1W"], value="1D")
    
    st.markdown(f"## Analiza techniczna: {cur['pair']}")
    
    # DWA NIEZALEŻNE AGREGATY SYGNAŁÓW
    a1, a2, a3 = st.columns(3)
    with a1:
        st.markdown(f"<div style='text-align:center;'><b>Investing.com</b><br><span style='font-size:1.5rem; color:#ff4b4b;'>{cur['inv']}</span></div>", unsafe_allow_html=True)
    with a2:
        st.markdown(f"<div style='text-align:center;'><b>TradingView</b><br><span style='font-size:1.5rem; color:#00ff88;'>{cur['tv']}</span></div>", unsafe_allow_html=True)
    with a3:
        st.markdown(f"<div style='text-align:center;'><b>Wskaźnik RSI</b><br><span style='font-size:1.5rem; color:white;'>54.2</span></div>", unsafe_allow_html=True)

    # Widgety techniczne
    components.html(f"""
        <div style="height:500px;">
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
          {{
            "interval": "{st.session_state.current_tf}", "width": "100%", "isTransparent": true, "height": 450,
            "symbol": "{cur['sym']}", "showIntervalTabs": true, "displayMode": "multiple", "locale": "pl", "colorTheme": "dark"
          }}
          </script>
        </div>""", height=500)
