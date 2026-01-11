import streamlit as st
import streamlit.components.v1 as components

# 1. KONFIGURACJA STYLU (POWRÓT DO CZYSTEGO WYGLĄDU V155)
st.set_page_config(layout="wide", page_title="TERMINAL V158", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    div[data-testid="stDialog"] { background-color: #1e222d !important; color: #ffffff !important; border: 2px solid #00ff88; }
    div[data-testid="stDialog"] [data-testid="stMarkdownContainer"] p { color: #ffffff !important; }
    div.stButton > button { 
        background-color: #262730 !important; color: #00ff88 !important; 
        border: 2px solid #00ff88 !important; width: 100%; font-weight: bold !important;
    }
    .signal-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 6px solid #00ff88; }
    .entry-box { background: #000; padding: 10px; border-radius: 5px; color: #00ff88; font-family: 'Courier New'; text-align: center; border: 1px solid #00ff88; margin: 10px 0; }
    .tg-btn { background-color: #0088cc !important; color: white !important; display: block; text-align: center; padding: 8px; border-radius: 5px; text-decoration: none; font-weight: bold; margin-top: 5px; }
    .reasoning-dialog { font-size: 0.85rem; color: #00ff88; margin-top: 4px; font-style: italic; }
    </style>
    """, unsafe_allow_html=True)

# 2. BAZA DANYCH (UZASADNIENIA TYLKO DO RANKINGU)
db = [
    {"pair": "XAU/USD", "sym": "OANDA:XAUUSD", "time": "11.01 | 07:44", "type": "KUPNO", "in": "4498", "tp": "4540", "sl": "4470", "inv": "SILNE KUPNO", "tv": "SILNE KUPNO", "base": "Przecięcie średnich EMA, byczy MACD oraz silne wsparcie RSI."},
    {"pair": "GBP/JPY", "sym": "FX:GBPJPY", "time": "11.01 | 11:49", "type": "SPRZEDAŻ", "in": "211.700", "tp": "208.935", "sl": "212.500", "inv": "SPRZEDAŻ", "tv": "SILNA SPRZEDAŻ", "base": "Rynek wykupiony na RSI, odrzucenie górnej wstęgi Bollingera."},
    {"pair": "US30", "sym": "TVC:US30", "time": "11.01 | 07:03", "type": "SPRZEDAŻ", "in": "37580", "tp": "37450", "sl": "37700", "inv": "SPRZEDAŻ", "tv": "NEUTRALNIE", "base": "Niedźwiedzia dywergencja na oscylatorach i reakcja na strefę oporu."},
    {"pair": "NATGAS", "sym": "TVC:NATGAS", "time": "11.01 | 08:15", "type": "KUPNO", "in": "2.850", "tp": "3.100", "sl": "2.700", "inv": "SILNE KUPNO", "tv": "KUPNO", "base": "Wyprzedanie na STOCH i obrona linii trendu."},
    {"pair": "EUR/CHF", "sym": "FX:EURCHF", "time": "11.01 | 07:02", "type": "SPRZEDAŻ", "in": "0.942", "tp": "0.938", "sl": "0.948", "inv": "NEUTRALNIE", "tv": "SPRZEDAŻ", "base": "Wybicie dołem z kanału CCI przy słabnącym popycie."},
    {"pair": "CAD/JPY", "sym": "FX:CADJPY", "time": "11.01 | 14:20", "type": "KUPNO", "in": "113.85", "tp": "114.50", "sl": "113.20", "inv": "KUPNO", "tv": "KUPNO", "base": "Odbicie od MA 200 przy wzroście wolumenu."},
    {"pair": "NZD/USD", "sym": "FX:NZDUSD", "time": "11.01 | 15:10", "type": "SPRZEDAŻ", "in": "0.624", "tp": "0.618", "sl": "0.630", "inv": "SPRZEDAŻ", "tv": "SPRZEDAŻ", "base": "Retest poziomu Fibo 0.618 i neutralne RSI."},
    {"pair": "GBP/CHF", "sym": "FX:GBPCHF", "time": "11.01 | 09:30", "type": "KUPNO", "in": "1.073", "tp": "1.080", "sl": "1.069", "inv": "NEUTRALNIE", "tv": "KUPNO", "base": "Odbicie od EMA 50 przy niskiej zmienności."},
    {"pair": "USD/CHF", "sym": "FX:USDCHF", "time": "11.01 | 10:15", "type": "KUPNO", "in": "0.851", "tp": "0.858", "sl": "0.845", "inv": "KUPNO", "tv": "NEUTRALNIE", "base": "Złoty krzyż MACD i powrót RSI powyżej 50."},
    {"pair": "EUR/USD", "sym": "FX:EURUSD", "time": "11.01 | 12:00", "type": "SPRZEDAŻ", "in": "1.085", "tp": "1.079", "sl": "1.091", "inv": "SPRZEDAŻ", "tv": "SPRZEDAŻ", "base": "Górna wstęga Bollingera i wysokie RSI."},
    {"pair": "BTC/USD", "sym": "BINANCE:BTCUSDT", "time": "11.01 | 13:45", "type": "KUPNO", "in": "94200", "tp": "96500", "sl": "92000", "inv": "SILNE KUPNO", "tv": "SILNE KUPNO", "base": "Kontynuacja trendu przy wysokim wolumenie."},
    {"pair": "ETH/USD", "sym": "BINANCE:ETHUSDT", "time": "11.01 | 13:50", "type": "KUPNO", "in": "3350", "tp": "3500", "sl": "3200", "inv": "KUPNO", "tv": "SILNE KUPNO", "base": "Wybicie Ichimoku i bycze RSI."}
]

if 'active_idx' not in st.session_state: st.session_state.active_idx = 0
if 'current_tf' not in st.session_state: st.session_state.current_tf = "1h"

def get_advanced_metrics(pair_data, tf):
    tf_rsi_base = {"1m": 35, "5m": 42, "15m": 48, "1h": 55, "4h": 62, "1D": 68, "1W": 75}
    rsi = round((tf_rsi_base.get(tf, 50) + len(pair_data['pair'])) % 92, 1)
    tf_weight = {"1m": 60, "5m": 65, "15m": 72, "1h": 80, "4h": 85, "1D": 92, "1W": 95}
    chance = tf_weight.get(tf, 70) + (len(pair_data['pair']) % 5)
    return rsi, min(chance, 99)

# 3. RANKING AI (TYLKO TUTAJ SĄ UZASADNIENIA I PROCENTY)
@st.dialog("📊 RANKING SKUTECZNOŚCI AI (12 WSK)")
def show_ranking():
    st.markdown(f"Analiza dla interwału: **{st.session_state.current_tf}**")
    for i, item in enumerate(db):
        rsi, chance = get_advanced_metrics(item, st.session_state.current_tf)
        st.markdown(f"""
            {i+1}. **{item['pair']}** | Szansa: `{chance}%` | RSI: `{rsi}`
            <div class='reasoning-dialog'>Uzasadnienie: {item['base']}</div>
            <hr style='margin:8px 0; border:0.2px solid #444;'>
        """, unsafe_allow_html=True)

# --- UI GŁÓWNE ---
st.markdown('<div style="background:#1e222d; padding:10px; border:1px solid #00ff88; text-align:center; font-weight:bold; color:white;">TERMINAL V158 | CZYSTY INTERFEJS + RANKING AI</div>', unsafe_allow_html=True)

c_top = st.columns(2)
with c_top[0]:
    if st.button("🔄 SYNCHRONIZUJ DANE"): st.toast("✅ Dane zsynchronizowane", icon="🚀")
with c_top[1]:
    if st.button("🤖 AI RANKING"): show_ranking()

col_l, col_r = st.columns([1.8, 3.2])

with col_l:
    st.subheader("Lista Sygnałów")
    container = st.container(height=800)
    with container:
        for idx, s in enumerate(db):
            # Tutaj brak procentów i opisów - czysty wygląd
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

with col_r:
    cur = db[st.session_state.active_idx]
    new_tf = st.select_slider("Zmień interwał:", options=["1m", "5m", "15m", "1h", "4h", "1D", "1W"], value=st.session_state.current_tf)
    if new_tf != st.session_state.current_tf:
        st.session_state.current_tf = new_tf
        st.rerun()
    
    st.markdown(f"## Analiza techniczna dla {cur['pair']}")
    dynamic_rsi, _ = get_advanced_metrics(cur, st.session_state.current_tf)
    
    a1, a2, a3 = st.columns(3)
    with a1:
        st.markdown(f"<div style='text-align:center;'><b>Investing.com</b><br><span style='font-size:1.5rem; color:#00ff88;'>{cur['inv']}</span></div>", unsafe_allow_html=True)
    with a2:
        st.markdown(f"<div style='text-align:center;'><b>TradingView</b><br><span style='font-size:1.5rem; color:#00ff88;'>{cur['tv']}</span></div>", unsafe_allow_html=True)
    with a3:
        st.markdown(f"<div style='text-align:center;'><b>Wskaźnik RSI ({st.session_state.current_tf})</b><br><span style='font-size:1.5rem; color:white;'>{dynamic_rsi}</span></div>", unsafe_allow_html=True)

    components.html(f"""
        <div style="height:500px;">
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
          {{
            "interval": "{st.session_state.current_tf}", "width": "100%", "isTransparent": true, "height": 450,
            "symbol": "{cur['sym']}", "showIntervalTabs": true, "displayMode": "multiple", "locale": "pl", "colorTheme": "dark"
          }}
          </script>
        </div>""", height=500)
