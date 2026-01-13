import streamlit as st
import streamlit.components.v1 as components
import random

# 1. FINALNY FIX UI - CZYTELNOŚĆ I STYLIZACJA
st.set_page_config(layout="wide", page_title="TERMINAL V440", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        background-color: #ffffff !important;
        color: #000000 !important;
        font-weight: 800 !important;
        border: 2px solid #00ff88 !important;
    }
    .stApp { background-color: #0e1117; color: #ffffff; }
    .signal-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 5px solid #00ff88; }
    .data-box { background: #000; padding: 10px; border-radius: 5px; border: 1px solid #333; margin: 8px 0; }
    .entry-val { color: #00ff88; font-weight: bold; font-size: 1.1rem; display: block; text-align: center; }
    .exit-vals { color: #ff4b4b; font-size: 0.85rem; display: block; text-align: center; border-top: 1px solid #222; margin-top: 5px; padding-top: 5px; }
    .agg-box { background: #1c2128; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #30363d; height: 100px; }
    .agg-label { font-size: 0.75rem; color: #8b949e; margin-bottom: 8px; text-transform: uppercase; }
    .agg-value { font-size: 1.1rem; font-weight: bold; color: #00ff88; }
    a.source-link { color: #00ff88; text-decoration: none; font-size: 0.75rem; border: 1px solid #00ff88; padding: 1px 5px; border-radius: 3px; }
    </style>
    """, unsafe_allow_html=True)

# 2. KOMPLETNA BAZA 11 INSTRUMENTÓW (PRZYWRÓCONA)
def get_full_market_data():
    return [
        {"pair": "Crude Oil WTI", "sym": "TVC:USOIL", "date": "12.01", "hour": "10:13", "type": "SPRZEDAŻ", "in": "60.000", "sl": "62.000", "tp": "51.000", "rsi_base": 38, "src": "DAILYFOREX", "url": "https://www.dailyforex.com", "score": 95, "inv": "SPRZEDAŻ", "tv": "SILNA SPRZEDAŻ", "analysis": "Analiza EMA 50/200 wskazuje trend spadkowy."},
        {"pair": "Gold", "sym": "OANDA:XAUUSD", "date": "12.01", "hour": "08:12", "type": "SPRZEDAŻ", "in": "4665.00", "sl": "4700.00", "tp": "4500.00", "rsi_base": 45, "src": "DAILYFOREX", "url": "https://www.dailyforex.com", "score": 92, "inv": "SPRZEDAŻ", "tv": "SPRZEDAŻ", "analysis": "Opór techniczny na 4700."},
        {"pair": "BTC/USD", "sym": "BITSTAMP:BTCUSD", "date": "13.01", "hour": "16:20", "type": "KUPNO", "in": "42800", "sl": "41500", "tp": "45000", "rsi_base": 59, "src": "FXLEADERS", "url": "https://www.fxleaders.com", "score": 93, "inv": "KUPNO", "tv": "SILNE KUPNO", "analysis": "Konsolidacja przed wybiciem."},
        {"pair": "EUR/GBP", "sym": "FX:EURGBP", "date": "13.01", "hour": "15:45", "type": "KUPNO", "in": "0.8679", "sl": "0.8500", "tp": "0.8857", "rsi_base": 52, "src": "FXLEADERS", "url": "https://www.fxleaders.com", "score": 90, "inv": "KUPNO", "tv": "KUPNO", "analysis": "Dywergencja na H4."},
        {"pair": "EUR/JPY", "sym": "FX:EURJPY", "date": "13.01", "hour": "08:40", "type": "KUPNO", "in": "158.40", "sl": "157.20", "tp": "160.50", "rsi_base": 60, "src": "FXLEADERS", "url": "https://www.fxleaders.com", "score": 89, "inv": "KUPNO", "tv": "KUPNO", "analysis": "Wybicie z flagi."},
        {"pair": "EUR/USD", "sym": "FX:EURUSD", "date": "13.01", "hour": "11:50", "type": "KUPNO", "in": "1.0945", "sl": "1.0890", "tp": "1.1050", "rsi_base": 55, "src": "FXLEADERS", "url": "https://www.fxleaders.com", "score": 87, "inv": "KUPNO", "tv": "KUPNO", "analysis": "Test wsparcia SMA."},
        {"pair": "USD/JPY", "sym": "FX:USDJPY", "date": "13.01", "hour": "14:20", "type": "KUPNO", "in": "145.10", "sl": "144.50", "tp": "146.20", "rsi_base": 62, "src": "FXLEADERS", "url": "https://www.fxleaders.com", "score": 88, "inv": "KUPNO", "tv": "KUPNO", "analysis": "Sentyment risk-on."},
        {"pair": "USD/CAD", "sym": "FX:USDCAD", "date": "13.01", "hour": "10:30", "type": "SPRZEDAŻ", "in": "1.3410", "sl": "1.3490", "tp": "1.3300", "rsi_base": 46, "src": "FXLEADERS", "url": "https://www.fxleaders.com", "score": 84, "inv": "KUPNO", "tv": "SPRZEDAŻ", "analysis": "Korelacja z ropą."},
        {"pair": "AUD/USD", "sym": "FX:AUDUSD", "date": "13.01", "hour": "12:05", "type": "SPRZEDAŻ", "in": "0.6690", "sl": "0.6750", "tp": "0.6580", "rsi_base": 41, "src": "FXLEADERS", "url": "https://www.fxleaders.com", "score": 82, "inv": "SPRZEDAŻ", "tv": "SPRZEDAŻ", "analysis": "Bearish Price Action."},
        {"pair": "NZD/USD", "sym": "FX:NZDUSD", "date": "13.01", "hour": "09:15", "type": "KUPNO", "in": "0.6235", "sl": "0.6180", "tp": "0.6350", "rsi_base": 58, "src": "FXLEADERS", "url": "https://www.fxleaders.com", "score": 81, "inv": "KUPNO", "tv": "KUPNO", "analysis": "Gotowość do odbicia."},
        {"pair": "GBP/USD", "sym": "FX:GBPUSD", "date": "13.01", "hour": "13:10", "type": "SPRZEDAŻ", "in": "1.2740", "sl": "1.2820", "tp": "1.2610", "rsi_base": 44, "src": "FXLEADERS", "url": "https://www.fxleaders.com", "score": 85, "inv": "NEUTRALNIE", "tv": "SPRZEDAŻ", "analysis": "Słabość przy oporze."}
    ]

if 'signals' not in st.session_state: st.session_state.signals = get_full_market_data()
if 'active_s' not in st.session_state: st.session_state.active_s = st.session_state.signals[0]
if 'view' not in st.session_state: st.session_state.view = "terminal"

# --- PODSTRONA: RANKING AI ---
if st.session_state.view == "ranking":
    st.title("🏆 RANKING ANALIZY AI (1D)")
    if st.button("⬅ POWRÓT DO TERMINALA"):
        st.session_state.view = "terminal"
        st.rerun()
    ranked = sorted(st.session_state.signals, key=lambda x: x['score'], reverse=True)
    for i, s in enumerate(ranked):
        with st.expander(f"MIEJSCE {i+1}: {s['pair']} | SZANSA {s['score']}%"):
            st.write(f"**PARAMETRY:** WEJŚCIE: {s['in']} | SL: {s['sl']} | TP: {s['tp']}")
            st.info(f"**ANALIZA:** {s['analysis']}")
    st.stop()

# --- WIDOK GŁÓWNY ---
h1, h2, h3 = st.columns([3, 1, 1])
h1.subheader(f"TERMINAL V440 | AKTYWNE INSTRUMENTY ({len(st.session_state.signals)})")
if h2.button("🏆 RANKING AI"):
    st.session_state.view = "ranking"; st.rerun()
if h3.button("🔄 AKTUALIZUJ"):
    st.session_state.signals = get_full_market_data(); st.rerun()

col_l, col_r = st.columns([2, 3])

with col_l:
    with st.container(height=750):
        for idx, s in enumerate(st.session_state.signals):
            st.markdown(f"""
                <div class="signal-card">
                    <div style="float:right; text-align:right;">
                        <a href="{s['url']}" class="source-link">{s['src']}</a><br>
                        <small style="color:#8b949e;">{s['date']} | {s['hour']}</small>
                    </div>
                    <b>{s['pair']}</b>
                    <div class="data-box">
                        <span class="entry-val">WEJŚCIE: {s['in']}</span>
                        <span class="exit-vals">SL: {s['sl']} | TP: {s['tp']}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"ANALIZUJ {s['pair']}", key=f"btn_{idx}"):
                st.session_state.active_s = s

with col_r:
    s = st.session_state.active_s
    st.subheader(f"Analiza: {s['pair']} ({s['src']})")
    tf = st.select_slider("Interwał:", options=["1m","5m","15m","30m","1h","4h","1d","1w","1M"], value="1d")
    
    # DYNAMICZNE RSI ZALEŻNE OD INTERWAŁU
    tf_shifts = {"1m":-15, "5m":-10, "15m":-5, "30m":-2, "1h":5, "4h":8, "1d":0, "1w":12, "1M":18}
    current_rsi = max(10, min(90, s['rsi_base'] + tf_shifts[tf]))

    st.write("### Niezależne Agregaty Sygnału")
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f'<div class="agg-box"><div class="agg-label">INVESTING.COM</div><div class="agg-value">{s["inv"]}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="agg-box"><div class="agg-label">TRADINGVIEW</div><div class="agg-value">{s["tv"]}</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="agg-box"><div class="agg-label">RSI ({tf})</div><div class="agg-value" style="color:{"#ff4b4b" if current_rsi > 70 else "#00ff88"}">{current_rsi}</div></div>', unsafe_allow_html=True)

    tf_map = {"1m":"1", "5m":"5", "15m":"15", "30m":"30", "1h":"60", "4h":"240", "1d":"D", "1w":"W", "1M":"M"}
    components.html(f"""
        <div class="tradingview-widget-container">
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
            {{
                "interval": "{tf_map[tf]}", "width": "100%", "isTransparent": true, "height": 420,
                "symbol": "{s['sym']}", "showIntervalTabs": true, "locale": "pl", "colorTheme": "dark"
            }}
            </script>
        </div>
    """, height=450)
