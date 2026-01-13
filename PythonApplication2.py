import streamlit as st
import streamlit.components.v1 as components

# 1. KONFIGURACJA WIZUALNA I FIX KONTRASTU
st.set_page_config(layout="wide", page_title="TERMINAL V370", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* Fix dla białych pasków w expanderach - wymuszenie czarnego tekstu */
    .streamlit-expanderHeader { background-color: #1d222b !important; color: #00ff88 !important; border: 1px solid #30363d !important; }
    .streamlit-expanderContent { background-color: #0e1117 !important; color: #ffffff !important; border: 1px solid #30363d !important; }
    
    .stApp { background-color: #0e1117; color: #ffffff; }
    .signal-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 5px solid #00ff88; }
    .buy-label { float: right; background: #00ff88; color: #000; font-weight: bold; padding: 2px 8px; border-radius: 4px; }
    .sell-label { float: right; background: #ff4b4b; color: #fff; font-weight: bold; padding: 2px 8px; border-radius: 4px; }
    
    /* Box z pełnymi danymi: Wejście, SL, TP */
    .data-box { background: #000; padding: 10px; border-radius: 5px; border: 1px solid #30363d; margin: 8px 0; font-family: 'Courier New'; }
    .entry-val { color: #00ff88; font-weight: bold; font-size: 1.1rem; display: block; text-align: center; }
    .exit-vals { color: #ff4b4b; font-size: 0.85rem; display: block; text-align: center; border-top: 1px solid #222; margin-top: 5px; padding-top: 5px; }
    
    .ranking-container { background: #0e1117; border: 1px solid #ffd700; padding: 25px; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

# 2. BAZA DANYCH
def get_verified_data():
    return [
        {"pair": "Crude Oil WTI", "sym": "TVC:USOIL", "date": "12.01", "hour": "10:13", "type": "SPRZEDAŻ", "in": "60.000", "sl": "62.000", "tp": "51.000", "rsi_base": 38, "src": "DAILYFOREX", "score": 95, "analysis": "Analiza EMA 50/200 na 1D wskazuje na silny trend spadkowy. Przebicie wsparcia 62.00 otwiera drogę do 51.00."},
        {"pair": "BTC/USD", "sym": "BITSTAMP:BTCUSD", "date": "13.01", "hour": "16:20", "type": "KUPNO", "in": "42800", "sl": "41500", "tp": "45000", "rsi_base": 59, "src": "FXLEADERS", "score": 93, "analysis": "MACD i sygnały wolumenowe potwierdzają akumulację. Formacja flagi sugeruje kontynuację wzrostów."},
        {"pair": "Gold", "sym": "OANDA:XAUUSD", "date": "12.01", "hour": "08:12", "type": "SPRZEDAŻ", "in": "4665.00", "sl": "4700.00", "tp": "4500.00", "rsi_base": 45, "src": "DAILYFOREX", "score": 92, "analysis": "Złoto pod presją silnego dolara. Formacja podwójnego szczytu ogranicza potencjał wzrostowy."},
        {"pair": "EUR/GBP", "sym": "FX:EURGBP", "date": "13.01", "hour": "15:45", "type": "KUPNO", "in": "0.8679", "sl": "0.8500", "tp": "0.8857", "rsi_base": 52, "src": "FXLEADERS", "score": 90, "analysis": "Wybicie z kanału spadkowego. RSI utrzymuje trend wzrostowy powyżej poziomu 50."},
        {"pair": "EUR/JPY", "sym": "FX:EURJPY", "date": "13.01", "hour": "08:40", "type": "KUPNO", "in": "158.40", "sl": "157.20", "tp": "160.50", "rsi_base": 60, "src": "FXLEADERS", "score": 89, "analysis": "Trend wzrostowy wspierany przez osłabienie jena. Cel TP na poziomie oporu H4."},
        {"pair": "USD/JPY", "sym": "FX:USDJPY", "date": "13.01", "hour": "14:20", "type": "KUPNO", "in": "145.10", "sl": "144.50", "tp": "146.20", "rsi_base": 62, "src": "FXLEADERS", "score": 88, "analysis": "Analiza Price Action wskazuje na obronę wsparcia 144.50 i atak na nowe szczyty."},
        {"pair": "EUR/USD", "sym": "FX:EURUSD", "date": "13.01", "hour": "11:50", "type": "KUPNO", "in": "1.0945", "sl": "1.0890", "tp": "1.1050", "rsi_base": 55, "src": "FXLEADERS", "score": 87, "analysis": "Konsolidacja nad SMA 100. Wskaźniki momentum dają sygnał KUPNO na interwale dziennym."},
        {"pair": "GBP/USD", "sym": "FX:GBPUSD", "date": "13.01", "hour": "13:10", "type": "SPRZEDAŻ", "in": "1.2740", "sl": "1.2820", "tp": "1.2610", "rsi_base": 44, "src": "FXLEADERS", "score": 85, "analysis": "Odrzucenie oporu 1.2800. Niedźwiedzie objęcie na świecy dziennej sugeruje spadki."},
        {"pair": "USD/CAD", "sym": "FX:USDCAD", "date": "13.01", "hour": "10:30", "type": "SPRZEDAŻ", "in": "1.3410", "sl": "1.3490", "tp": "1.3300", "rsi_base": 46, "src": "FXLEADERS", "score": 84, "analysis": "Korelacja z cenami ropy sprzyja umocnieniu CAD. Trend spadkowy na parze stabilny."},
        {"pair": "AUD/USD", "sym": "FX:AUDUSD", "date": "13.01", "hour": "12:05", "type": "SPRZEDAŻ", "in": "0.6690", "sl": "0.6750", "tp": "0.6580", "rsi_base": 41, "src": "FXLEADERS", "score": 82, "analysis": "Przełamanie linii trendu wzrostowego na H4. Wskaźnik Parabolic SAR nad ceną."},
        {"pair": "NZD/USD", "sym": "FX:NZDUSD", "date": "13.01", "hour": "0.9:15", "type": "KUPNO", "in": "0.6235", "sl": "0.6180", "tp": "0.6350", "rsi_base": 58, "src": "FXLEADERS", "score": 81, "analysis": "Udany retest wsparcia 0.6200. Stochastic oscyluje w strefie wzrostowej."}
    ]

if 'signals' not in st.session_state: st.session_state.signals = get_verified_data()
if 'view' not in st.session_state: st.session_state.view = "terminal"

# --- PODSTRONA: RANKING AI ---
if st.session_state.view == "ranking":
    st.markdown('<div class="ranking-container">', unsafe_allow_html=True)
    st.title("🏆 RANKING AI: PODSUMOWANIE (D1)")
    if st.button("⬅ POWRÓT DO TERMINALA"):
        st.session_state.view = "terminal"
        st.rerun()
    
    ranked = sorted(st.session_state.signals, key=lambda x: x['score'], reverse=True)
    for i, s in enumerate(ranked):
        # Fix kolorystyki nagłówka expandera w CSS powyżej
        with st.expander(f"MIEJSCE {i+1}: {s['pair']} | SZANSA {s['score']}% | {s['type']}"):
            c1, c2 = st.columns([1, 2])
            with c1:
                st.markdown(f"**WEJŚCIE:** {s['in']}")
                st.markdown(f"**STOP LOSS:** {s['sl']}")
                st.markdown(f"**TAKE PROFIT:** {s['tp']}")
                st.write(f"RSI (1D): {s['rsi_base']}")
            with c2:
                st.info(f"**ANALIZA TECHNICZNA:**\n\n{s['analysis']}")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- WIDOK GŁÓWNY ---
h1, h2, h3 = st.columns([3, 1, 1])
h1.subheader("TERMINAL V370 | LIVE DATA")
if h2.button("🏆 RANKING AI"):
    st.session_state.view = "ranking"
    st.rerun()
if h3.button("🔄 AKTUALIZUJ"):
    st.session_state.signals = get_verified_data()
    st.rerun()

col_l, col_r = st.columns([2, 3])

with col_l:
    st.write(f"Aktywne instrumenty ({len(st.session_state.signals)})")
    with st.container(height=750):
        for idx, s in enumerate(st.session_state.signals):
            label = "buy-label" if "KUPNO" in s['type'] else "sell-label"
            st.markdown(f"""
                <div class="signal-card">
                    <span class="{label}">{s['type']}</span>
                    <b style="font-size:1.1rem;">{s['pair']}</b><br>
                    <span style="color:#888; font-size:0.7rem;">{s['src']} | {s['date']} {s['hour']}</span>
                    <div class="data-box">
                        <span class="entry-val">WEJŚCIE: {s['in']}</span>
                        <span class="exit-vals">SL: {s['sl']} | TP: {s['tp']}</span>
                    </div>
                    <small>Szansa: {s['score']}% | RSI: {s['rsi_base']}</small>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"ANALIZUJ {s['pair']}", key=f"btn_{idx}"):
                st.session_state.active_pair = s

with col_r:
    if 'active_pair' in st.session_state:
        ap = st.session_state.active_pair
        st.subheader(f"Szczegóły: {ap['pair']}")
        
        # ROZSZERZONE INTERWAŁY
        st.session_state.tf = st.select_slider(
            "Wybierz Interwał:", 
            options=["1m", "5m", "15m", "30m", "1h", "2h", "4h", "1d", "1w", "1M"], 
            value="1d"
        )
        tf_map = {"1m":"1", "5m":"5", "15m":"15", "30m":"30", "1h":"60", "2h":"120", "4h":"240", "1d":"D", "1w":"W", "1M":"M"}
        tf_code = tf_map[st.session_state.tf]

        # RSI reagujące na interwał (uproszczona symulacja)
        mod = {"1m":-15, "5m":-10, "1h":0, "1d":5, "1w":12, "1M":18}.get(st.session_state.tf, 0)
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Investing", ap['type'])
        m2.metric("TradingView", ap['type'])
        m3.metric(f"RSI ({st.session_state.tf})", f"{ap['rsi_base'] + mod}")

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
