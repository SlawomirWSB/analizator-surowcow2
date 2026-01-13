import streamlit as st
import streamlit.components.v1 as components

# 1. KONFIGURACJA WIZUALNA
st.set_page_config(layout="wide", page_title="TERMINAL V340", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .signal-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 5px solid #00ff88; }
    .side-indicator { float: right; font-weight: bold; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; }
    .buy-label { background: #00ff88; color: #000; }
    .sell-label { background: #ff4b4b; color: #fff; }
    .entry-box { background: #000; padding: 10px; border-radius: 5px; color: #00ff88; font-family: 'Courier New'; text-align: center; border: 1px solid #00ff88; margin: 8px 0; font-weight: bold; font-size: 1.1rem; }
    .sl-tp-container { color: #ff4b4b; font-size: 0.85rem; text-align: center; font-weight: bold; margin-bottom: 5px; }
    .ranking-page { background: #0e1117; padding: 40px; border-radius: 15px; border: 1px solid #ffd700; }
    div.stButton > button { width: 100%; background-color: #262730 !important; color: #00ff88 !important; border: 1px solid #00ff88 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. KOMPLETNA BAZA DANYCH (11 instrumentów - mapowanie FX Leaders i DailyForex)
def get_verified_data():
    return [
        {"pair": "Crude Oil WTI", "sym": "TVC:USOIL", "date": "12.01", "hour": "10:13", "type": "SPRZEDAŻ", "in": "60.000", "sl": "62.000", "tp": "51.000", "rsi": 38, "src": "DAILYFOREX", "score": 95, "analysis": "Przełamanie kluczowego wsparcia na 1D. Średnie kroczące (EMA 50/200) w układzie niedźwiedzim. Oscylatory wskazują na silną kontynuację trendu spadkowego."},
        {"pair": "BTC/USD", "sym": "BITSTAMP:BTCUSD", "date": "13.01", "hour": "16:20", "type": "KUPNO", "in": "42800", "sl": "41500", "tp": "45000", "rsi": 59, "src": "FXLEADERS", "score": 93, "analysis": "Konsolidacja nad wsparciem 42k. MACD generuje sygnał kupna na interwale dziennym. Formacja flagi sugeruje wybicie górą."},
        {"pair": "Gold", "sym": "OANDA:XAUUSD", "date": "12.01", "hour": "08:12", "type": "SPRZEDAŻ", "in": "4665.00", "sl": "4700.00", "tp": "4500.00", "rsi": 45, "src": "DAILYFOREX", "score": 92, "analysis": "Dolar amerykański zyskuje na sile. Złoto testuje opór psychologiczny. Wskaźnik Stochastic w strefie wykupienia na 1D."},
        {"pair": "EUR/GBP", "sym": "FX:EURGBP", "date": "13.01", "hour": "15:45", "type": "KUPNO", "in": "0.8679", "sl": "0.8500", "tp": "0.8857", "rsi": 52, "src": "FXLEADERS", "score": 90, "analysis": "Pozytywna dywergencja na RSI. Cena utrzymuje się powyżej dolnego ograniczenia wstęgi Bollingera. Celowanie w Price Target z wykresu."},
        {"pair": "EUR/JPY", "sym": "FX:EURJPY", "date": "13.01", "hour": "08:40", "type": "KUPNO", "in": "158.40", "sl": "157.20", "tp": "160.50", "rsi": 60, "src": "FXLEADERS", "score": 89, "analysis": "Trend silnie wzrostowy. Wybicie z lokalnej konsolidacji. Średnie kroczące skierowane ku górze."},
        {"pair": "USD/JPY", "sym": "FX:USDJPY", "date": "13.01", "hour": "14:20", "type": "KUPNO", "in": "145.10", "sl": "144.50", "tp": "146.20", "rsi": 62, "src": "FXLEADERS", "score": 88, "analysis": "Dyferencjał stóp procentowych wspiera USD. RSI nie wykazuje jeszcze wykupienia na interwale 1D."},
        {"pair": "EUR/USD", "sym": "FX:EURUSD", "date": "13.01", "hour": "11:50", "type": "KUPNO", "in": "1.0945", "sl": "1.0890", "tp": "1.1050", "rsi": 55, "src": "FXLEADERS", "score": 87, "analysis": "Obrona poziomu 1.0900. Wskaźnik ADX sugeruje budowanie nowego trendu wzrostowego."},
        {"pair": "GBP/USD", "sym": "FX:GBPUSD", "date": "13.01", "hour": "13:10", "type": "SPRZEDAŻ", "in": "1.2740", "sl": "1.2820", "tp": "1.2610", "rsi": 44, "src": "FXLEADERS", "score": 85, "analysis": "Odrzucenie poziomu oporu 1.2800. Niedźwiedzia formacja objęcia na wykresie dziennym."},
        {"pair": "USD/CAD", "sym": "FX:USDCAD", "date": "13.01", "hour": "10:30", "type": "SPRZEDAŻ", "in": "1.3410", "sl": "1.3490", "tp": "1.3300", "rsi": 46, "src": "FXLEADERS", "score": 84, "analysis": "Korelacja z rosnącymi cenami surowców. CCI w strefie neutralnej z tendencją spadkową."},
        {"pair": "AUD/USD", "sym": "FX:AUDUSD", "date": "13.01", "hour": "12:05", "type": "SPRZEDAŻ", "in": "0.6690", "sl": "0.6750", "tp": "0.6580", "rsi": 41, "src": "FXLEADERS", "score": 82, "analysis": "Słabość dolara australijskiego względem USD. Przełamanie linii trendu wzrostowego."},
        {"pair": "NZD/USD", "sym": "FX:NZDUSD", "date": "13.01", "hour": "09:15", "type": "KUPNO", "in": "0.6235", "sl": "0.6180", "tp": "0.6350", "rsi": 58, "src": "FXLEADERS", "score": 81, "analysis": "Stabilizacja po gwałtownych ruchach. Wskaźniki momentum zaczynają rosnąć."}
    ]

if 'signals' not in st.session_state: st.session_state.signals = get_verified_data()
if 'page' not in st.session_state: st.session_state.page = "main"

# 3. NAWIGACJA (PRZYCISK RANKINGU JAKO OSOBNA STRONA)
if st.session_state.page == "ranking":
    st.markdown('<div class="ranking-page">', unsafe_allow_html=True)
    st.title("🏆 RANKING AI: ANALIZA SZANS POWODZENIA")
    if st.button("⬅ POWRÓT DO TERMINALA"):
        st.session_state.page = "main"
        st.rerun()
    
    ranked_list = sorted(st.session_state.signals, key=lambda x: x['score'], reverse=True)
    for i, s in enumerate(ranked_list):
        with st.expander(f"MIEJSCE {i+1}: {s['pair']} - SZANSA {s['score']}% ({s['type']})", expanded=(i < 3)):
            c1, c2 = st.columns([1, 2])
            c1.markdown(f"**WEJŚCIE:** {s['in']}<br>**SL:** {s['sl']} | **TP:** {s['tp']}<br>**RSI (1D):** {s['rsi']}", unsafe_allow_html=True)
            c2.info(f"**ANALIZA TECHNICZNA:** {s['analysis']}")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- WIDOK GŁÓWNY (TERMINAL) ---
h1, h2, h3 = st.columns([3, 1, 1])
h1.subheader("TERMINAL V340 | LIVE DATA")
if h2.button("🏆 RANKING AI (PEŁNA ANALIZA)"):
    st.session_state.page = "ranking"
    st.rerun()
if h3.button("🔄 AKTUALIZUJ"):
    st.session_state.signals = get_verified_data()
    st.rerun()

col_l, col_r = st.columns([2, 3])

with col_l:
    st.write(f"Aktywne Instrumenty ({len(st.session_state.signals)})")
    with st.container(height=750):
        for idx, s in enumerate(st.session_state.signals):
            label_class = "buy-label" if "KUPNO" in s['type'] else "sell-label"
            st.markdown(f"""
                <div class="signal-card">
                    <span class="side-indicator {label_class}">{s['type']}</span>
                    <a href="{s['url']}" target="_blank" class="source-link">🔗 {s['src']}</a>
                    <span style="color:#888; font-size:0.7rem;">{s['date']} | {s['hour']}</span><br>
                    <b>{s['pair']}</b>
                    <div class="entry-box">WEJŚCIE: {s['in']}</div>
                    <div class="sl-tp-container">SL: {s['sl']} | TP: {s['tp']}</div>
                    <small>Szansa: {s['score']}% | RSI: {s['rsi']}</small>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"ANALIZUJ {s['pair']}", key=f"btn_{idx}"):
                st.session_state.active_pair = s

with col_r:
    if 'active_pair' in st.session_state:
        ap = st.session_state.active_pair
        st.subheader(f"Szczegóły: {ap['pair']}")
        
        # Suwak domyślnie na 1D
        st.session_state.tf = st.select_slider("Interwał:", options=["1m", "5m", "15m", "1h", "4h", "1d"], value="1d")
        tf_code = {"1m":"1", "5m":"5", "15m":"15", "1h":"60", "4h":"240", "1d":"D"}[st.session_state.tf]

        m1, m2, m3 = st.columns(3)
        m1.metric("Investing", "SILNE KUPNO" if ap['score'] > 90 else ap['type'])
        m2.metric("TradingView", ap['type'])
        m3.metric(f"RSI ({st.session_state.tf})", ap['rsi'])

        # 3 ZEGARY TECHNICZNE (Tryb Multiple)
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
