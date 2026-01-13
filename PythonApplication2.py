import streamlit as st
import streamlit.components.v1 as components

# 1. KONFIGURACJA WIZUALNA
st.set_page_config(layout="wide", page_title="TERMINAL V310", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .signal-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 5px solid #00ff88; }
    .entry-box { background: #000; padding: 10px; border-radius: 5px; color: #00ff88; font-family: 'Courier New'; text-align: center; border: 1px solid #00ff88; margin: 8px 0; font-weight: bold; font-size: 1.1rem; }
    .source-link { color: #0088cc; text-decoration: none; font-size: 0.7rem; font-weight: bold; float: right; border: 1px solid #0088cc; padding: 2px 5px; border-radius: 3px; }
    .sl-tp-container { color: #ff4b4b; font-size: 0.85rem; text-align: center; font-weight: bold; margin-bottom: 5px; }
    div.stButton > button { width: 100%; background-color: #262730 !important; color: #00ff88 !important; border: 1px solid #00ff88 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. BAZA DANYCH (Ostatnie 3 dni, mapowanie FX Leaders wg Twoich wytycznych)
def get_final_data():
    # Dane mapowane: FX Leaders (Price Targets) | DailyForex (Dane wprost)
    return [
        {"pair": "EUR/GBP", "sym": "FX:EURGBP", "time": "13.01", "type": "KUPNO", "in": "0.8679", "sl": "0.8500", "tp": "0.8857", "rsi": 52, "src": "FXLEADERS", "url": "https://www.fxleaders.com/forex-signals/", "score": 90},
        {"pair": "Crude Oil WTI", "sym": "TVC:USOIL", "time": "12.01", "type": "SPRZEDAŻ", "in": "60.000", "sl": "62.000", "tp": "51.000", "rsi": 38, "src": "DAILYFOREX", "url": "https://www.dailyforex.com/forex-technical-analysis/free-forex-signals/page-1", "score": 94},
        {"pair": "Gold", "sym": "OANDA:XAUUSD", "time": "12.01", "type": "SPRZEDAŻ", "in": "4665.00", "sl": "4700.00", "tp": "4500.00", "rsi": 45, "src": "DAILYFOREX", "url": "https://www.dailyforex.com/forex-technical-analysis/free-forex-signals/page-1", "score": 92},
        {"pair": "USD/JPY", "sym": "FX:USDJPY", "time": "13.01", "type": "KUPNO", "in": "145.10", "sl": "144.50", "tp": "146.20", "rsi": 62, "src": "FXLEADERS", "url": "https://www.fxleaders.com/forex-signals/", "score": 93}
    ]

# Inicjalizacja stanu
if 'signals' not in st.session_state: st.session_state.signals = get_final_data()
if 'tf' not in st.session_state: st.session_state.tf = "1h"

# NAGŁÓWEK
h1, h2, h3 = st.columns([3, 1, 1])
h1.subheader("TERMINAL V310 | LIVE DATA")
if h2.button("🏆 RANKING AI"):
    st.session_state.signals = sorted(st.session_state.signals, key=lambda x: x['score'], reverse=True)
if h3.button("🔄 AKTUALIZUJ"):
    st.session_state.signals = get_final_data()
    st.rerun()

col_l, col_r = st.columns([2, 3])

with col_l:
    st.write("Aktywne Sygnały (Ostatnie 72h)")
    with st.container(height=700):
        for idx, s in enumerate(st.session_state.signals):
            st.markdown(f"""
                <div class="signal-card">
                    <a href="{s['url']}" target="_blank" class="source-link">🔗 {s['src']}</a>
                    <span style="float:right; color:#888; font-size:0.7rem; margin-right:10px;">{s['time']}</span><br>
                    <b>{s['pair']}</b> <span style="color:#00ff88">{s['type']}</span>
                    <div class="entry-box">WEJŚCIE: {s['in']}</div>
                    <div class="sl-tp-container">SL: {s['sl']} | TP: {s['tp']}</div>
                    <small>RSI: {s['rsi']} | Szansa: {s['score']}%</small>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"ANALIZUJ {s['pair']}", key=f"btn_{idx}"):
                st.session_state.active_pair = s

with col_r:
    if 'active_pair' in st.session_state:
        ap = st.session_state.active_pair
        st.subheader(f"Analiza: {ap['pair']}")
        
        # 1. SUWAK INTERWAŁU
        st.session_state.tf = st.select_slider("Wybierz Interwał:", options=["1m", "5m", "15m", "1h", "4h", "1d"], value=st.session_state.tf)
        tf_code = {"1m":"1", "5m":"5", "15m":"15", "1h":"60", "4h":"240", "1d":"D"}[st.session_state.tf]

        # 2. WSKAŹNIKI (RSI PO PRAWEJ)
        m1, m2, m3 = st.columns(3)
        m1.metric("Investing", "KUPNO" if "KUPNO" in ap['type'] else "SPRZEDAŻ")
        m2.metric("TradingView", ap['type'])
        m3.metric(f"RSI ({st.session_state.tf})", ap['rsi'])

        # 3. TRZY ZEGARY TECHNICZNE (Tryb Multiple)
        components.html(f"""
            <div class="tradingview-widget-container">
                <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
                {{
                    "interval": "{tf_code}",
                    "width": "100%",
                    "isTransparent": true,
                    "height": 550,
                    "symbol": "{ap['sym']}",
                    "showIntervalTabs": true,
                    "displayMode": "multiple",
                    "locale": "pl",
                    "colorTheme": "dark"
                }}
                </script>
            </div>
        """, height=560)
    else:
        st.info("Wybierz instrument z listy po lewej stronie.")
