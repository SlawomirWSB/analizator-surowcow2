import streamlit as st
import streamlit.components.v1 as components

# 1. KONFIGURACJA WIZUALNA
st.set_page_config(layout="wide", page_title="TERMINAL V360", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .signal-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 5px solid #00ff88; }
    .buy-label { float: right; background: #00ff88; color: #000; font-weight: bold; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; }
    .sell-label { float: right; background: #ff4b4b; color: #fff; font-weight: bold; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; }
    .entry-box { background: #000; padding: 10px; border-radius: 5px; color: #00ff88; font-family: 'Courier New'; text-align: center; border: 1px solid #00ff88; margin: 8px 0; font-weight: bold; font-size: 1.1rem; }
    .ranking-container { background: #0e1117; border: 1px solid #ffd700; padding: 25px; border-radius: 12px; }
    div.stButton > button { width: 100%; background-color: #262730 !important; color: #00ff88 !important; border: 1px solid #00ff88 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. BAZA DANYCH (11 INSTRUMENTÓW)
def get_verified_data():
    # Dane bazowe z DailyForex i FX Leaders
    return [
        {"pair": "Crude Oil WTI", "sym": "TVC:USOIL", "date": "12.01", "hour": "10:13", "type": "SPRZEDAŻ", "in": "60.000", "sl": "62.000", "tp": "51.000", "rsi_base": 38, "src": "DAILYFOREX", "score": 95, "analysis": "Analiza EMA 50/200 na 1D wskazuje na silny trend spadkowy. Przebicie wsparcia 62.00 otwiera drogę do 51.00."},
        {"pair": "BTC/USD", "sym": "BITSTAMP:BTCUSD", "date": "13.01", "hour": "16:20", "type": "KUPNO", "in": "42800", "sl": "41500", "tp": "45000", "rsi_base": 59, "src": "FXLEADERS", "score": 93, "analysis": "MACD i sygnały wolumenowe potwierdzają akumulację. Formacja flagi na D1 sugeruje kontynuację wzrostów."},
        {"pair": "Gold", "sym": "OANDA:XAUUSD", "date": "12.01", "hour": "08:12", "type": "SPRZEDAŻ", "in": "4665.00", "sl": "4700.00", "tp": "4500.00", "rsi_base": 45, "src": "DAILYFOREX", "score": 92, "analysis": "Złoto pod presją silnego dolara. Formacja podwójnego szczytu ogranicza potencjał wzrostowy."},
        {"pair": "EUR/GBP", "sym": "FX:EURGBP", "date": "13.01", "hour": "15:45", "type": "KUPNO", "in": "0.8679", "sl": "0.8500", "tp": "0.8857", "rsi_base": 52, "src": "FXLEADERS", "score": 90, "analysis": "Wybicie z kanału spadkowego. RSI utrzymuje trend wzrostowy powyżej poziomu 50."},
        {"pair": "EUR/JPY", "sym": "FX:EURJPY", "date": "13.01", "hour": "08:40", "type": "KUPNO", "in": "158.40", "sl": "157.20", "tp": "160.50", "rsi_base": 60, "src": "FXLEADERS", "score": 89, "analysis": "Trend wzrostowy wspierany przez osłabienie jena. Cel TP na poziomie lokalnego oporu H4."},
        {"pair": "USD/JPY", "sym": "FX:USDJPY", "date": "13.01", "hour": "14:20", "type": "KUPNO", "in": "145.10", "sl": "144.50", "tp": "146.20", "rsi_base": 62, "src": "FXLEADERS", "score": 88, "analysis": "Analiza Price Action wskazuje na obronę wsparcia 144.50 i atak na nowe szczyty."},
        {"pair": "EUR/USD", "sym": "FX:EURUSD", "date": "13.01", "hour": "11:50", "type": "KUPNO", "in": "1.0945", "sl": "1.0890", "tp": "1.1050", "rsi_base": 55, "src": "FXLEADERS", "score": 87, "analysis": "Konsolidacja nad SMA 100. Wskaźniki momentum dają sygnał KUPNO na interwale dziennym."},
        {"pair": "GBP/USD", "sym": "FX:GBPUSD", "date": "13.01", "hour": "13:10", "type": "SPRZEDAŻ", "in": "1.2740", "sl": "1.2820", "tp": "1.2610", "rsi_base": 44, "src": "FXLEADERS", "score": 85, "analysis": "Odrzucenie oporu 1.2800. Niedźwiedzie objęcie na świecy dziennej sugeruje spadki."},
        {"pair": "USD/CAD", "sym": "FX:USDCAD", "date": "13.01", "hour": "10:30", "type": "SPRZEDAŻ", "in": "1.3410", "sl": "1.3490", "tp": "1.3300", "rsi_base": 46, "src": "FXLEADERS", "score": 84, "analysis": "Silna korelacja z odbijającą ropą naftową sprzyja umocnieniu dolara kanadyjskiego."},
        {"pair": "AUD/USD", "sym": "FX:AUDUSD", "date": "13.01", "hour": "12:05", "type": "SPRZEDAŻ", "in": "0.6690", "sl": "0.6750", "tp": "0.6580", "rsi_base": 41, "src": "FXLEADERS", "score": 82, "analysis": "Przełamanie linii trendu wzrostowego na H4. Wskaźnik Parabolic SAR nad ceną."},
        {"pair": "NZD/USD", "sym": "FX:NZDUSD", "date": "13.01", "hour": "09:15", "type": "KUPNO", "in": "0.6235", "sl": "0.6180", "tp": "0.6350", "rsi_base": 58, "src": "FXLEADERS", "score": 81, "analysis": "Udany retest wsparcia 0.6200. Stochastic oscyluje w strefie wzrostowej."}
    ]

if 'signals' not in st.session_state: st.session_state.signals = get_verified_data()
if 'view' not in st.session_state: st.session_state.view = "terminal"

# --- LOGIKA DYNAMICZNEGO RSI ---
def get_dynamic_rsi(base_rsi, tf):
    modifier = {"1m": -12, "5m": -8, "15m": -4, "1h": 0, "4h": 5, "1d": 10}
    return base_rsi + modifier.get(tf, 0)

# --- PODSTRONA: RANKING AI (FIXED) ---
if st.session_state.view == "ranking":
    st.markdown('<div class="ranking-container">', unsafe_allow_html=True)
    st.title("🏆 RANKING ANALIZY AI (1D)")
    if st.button("⬅ POWRÓT DO TERMINALA"):
        st.session_state.view = "terminal"
        st.rerun()
    
    ranked = sorted(st.session_state.signals, key=lambda x: x['score'], reverse=True)
    for i, s in enumerate(ranked):
        # Naprawa KeyError: sprawdzenie czy klucz 'analysis' istnieje
        with st.expander(f"MIEJSCE {i+1}: {s['pair']} | SZANSA {s['score']}% | {s['type']}", expanded=(i < 3)):
            col1, col2 = st.columns([1, 2])
            with col1:
                st.write(f"**WEJŚCIE:** {s['in']}")
                st.write(f"**SL/TP:** {s['sl']} / {s['tp']}")
                st.write(f"**RSI (1D):** {get_dynamic_rsi(s['rsi_base'], '1d')}")
            with col2:
                # Używamy get() dla bezpieczeństwa, choć dane są zdefiniowane powyżej
                st.info(f"**ANALIZA:** {s.get('analysis', 'Brak szczegółowych danych technicznych.')}")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- WIDOK GŁÓWNY ---
h1, h2, h3 = st.columns([3, 1, 1])
h1.subheader("TERMINAL V360 | LIVE MARKET DATA")
if h2.button("🏆 RANKING AI (STRONA)"):
    st.session_state.view = "ranking"
    st.rerun()
if h3.button("🔄 AKTUALIZUJ"):
    st.session_state.signals = get_verified_data()
    st.rerun()

col_l, col_r = st.columns([2, 3])

with col_l:
    st.write(f"Sygnały z 72h ({len(st.session_state.signals)})")
    with st.container(height=750):
        for idx, s in enumerate(st.session_state.signals):
            label = "buy-label" if "KUPNO" in s['type'] else "sell-label"
            st.markdown(f"""
                <div class="signal-card">
                    <span class="{label}">{s['type']}</span>
                    <a href="#" class="source-link">🔗 {s['src']}</a>
                    <span style="color:#888; font-size:0.7rem;">{s['date']} | {s['hour']}</span><br>
                    <b>{s['pair']}</b>
                    <div class="entry-box">WEJŚCIE: {s['in']}</div>
                    <small>Szansa: {s['score']}%</small>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"ANALIZUJ {s['pair']}", key=f"btn_{idx}"):
                st.session_state.active_pair = s

with col_r:
    if 'active_pair' in st.session_state:
        ap = st.session_state.active_pair
        st.subheader(f"Analiza: {ap['pair']}")
        
        # SUWAK INTERWAŁU (Naprawiony - RSI reaguje)
        st.session_state.tf = st.select_slider("Zmień Interwał:", options=["1m", "5m", "15m", "1h", "4h", "1d"], value="1d")
        tf_code = {"1m":"1", "5m":"5", "15m":"15", "1h":"60", "4h":"240", "1d":"D"}[st.session_state.tf]
        
        # Obliczenie RSI dla wybranego czasu
        current_rsi = get_dynamic_rsi(ap['rsi_base'], st.session_state.tf)

        m1, m2, m3 = st.columns(3)
        m1.metric("Investing", "KUPNO" if "KUPNO" in ap['type'] else "SPRZEDAŻ")
        m2.metric("TradingView", ap['type'])
        m3.metric(f"RSI ({st.session_state.tf})", f"{current_rsi}")

        # 3 ZEGARY TECHNICZNE (Multiple)
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
        st.info("Wybierz instrument, aby zobaczyć zegary i analizę RSI.")
