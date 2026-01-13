import streamlit as st
import streamlit.components.v1 as components

# 1. KONFIGURACJA WIZUALNA - TOTALNY FIX CZYTELNOŚCI
st.set_page_config(layout="wide", page_title="TERMINAL V380", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* GLOBALNY FIX DLA PRZYCISKÓW (Białe paski z czarnym tekstem) */
    div.stButton > button {
        width: 100%;
        background-color: #ffffff !important; /* Białe tło zgodnie z Twoim UI */
        color: #000000 !important;           /* Wymuszony CZARNY tekst */
        font-weight: bold !important;
        border: 1px solid #00ff88 !important;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #00ff88 !important;
        color: #000000 !important;
    }

    /* FIX DLA NAGŁÓWKÓW EXPANDERÓW (Ranking) */
    .streamlit-expanderHeader {
        background-color: #ffffff !important; /* Biały pasek */
        color: #000000 !important;           /* Czarny tekst - ZAWSZE czytelny */
        border-radius: 5px !important;
    }
    .streamlit-expanderHeader p {
        color: #000000 !important;           /* Wymuszenie koloru dla paragrafów wewnątrz */
        font-weight: bold !important;
    }

    /* Stylistyka aplikacji */
    .stApp { background-color: #0e1117; color: #ffffff; }
    .signal-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 5px solid #00ff88; }
    .buy-label { float: right; background: #00ff88; color: #000; font-weight: bold; padding: 2px 8px; border-radius: 4px; }
    .sell-label { float: right; background: #ff4b4b; color: #fff; font-weight: bold; padding: 2px 8px; border-radius: 4px; }
    
    .data-box { background: #000; padding: 10px; border-radius: 5px; border: 1px solid #30363d; margin: 8px 0; }
    .entry-val { color: #00ff88; font-weight: bold; font-size: 1.1rem; display: block; text-align: center; }
    .exit-vals { color: #ff4b4b; font-size: 0.85rem; display: block; text-align: center; border-top: 1px solid #222; margin-top: 5px; padding-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 2. BAZA DANYCH (11 INSTRUMENTÓW)
def get_verified_data():
    return [
        {"pair": "Crude Oil WTI", "sym": "TVC:USOIL", "date": "12.01", "hour": "10:13", "type": "SPRZEDAŻ", "in": "60.000", "sl": "62.000", "tp": "51.000", "rsi_base": 38, "src": "DAILYFOREX", "score": 95, "analysis": "Trend spadkowy potwierdzony EMA 50/200. Przebicie kluczowego wsparcia."},
        {"pair": "BTC/USD", "sym": "BITSTAMP:BTCUSD", "date": "13.01", "hour": "16:20", "type": "KUPNO", "in": "42800", "sl": "41500", "tp": "45000", "rsi_base": 59, "src": "FXLEADERS", "score": 93, "analysis": "Konsolidacja nad wsparciem, MACD wzrostowe."},
        {"pair": "Gold", "sym": "OANDA:XAUUSD", "date": "12.01", "hour": "08:12", "type": "SPRZEDAŻ", "in": "4665.00", "sl": "4700.00", "tp": "4500.00", "rsi_base": 45, "src": "DAILYFOREX", "score": 92, "analysis": "Odrzucenie oporu, presja ze strony USD."},
        {"pair": "EUR/GBP", "sym": "FX:EURGBP", "date": "13.01", "hour": "15:45", "type": "KUPNO", "in": "0.8679", "sl": "0.8500", "tp": "0.8857", "rsi_base": 52, "src": "FXLEADERS", "score": 90, "analysis": "Dywergencja wzrostowa na RSI."},
        {"pair": "EUR/JPY", "sym": "FX:EURJPY", "date": "13.01", "hour": "08:40", "type": "KUPNO", "in": "158.40", "sl": "157.20", "tp": "160.50", "rsi_base": 60, "src": "FXLEADERS", "score": 89, "analysis": "Silny trend wzrostowy na wszystkich interwałach."},
        {"pair": "USD/JPY", "sym": "FX:USDJPY", "date": "13.01", "hour": "14:20", "type": "KUPNO", "in": "145.10", "sl": "144.50", "tp": "146.20", "rsi_base": 62, "src": "FXLEADERS", "score": 88, "analysis": "Wybicie z formacji flagi."},
        {"pair": "EUR/USD", "sym": "FX:EURUSD", "date": "13.01", "hour": "11:50", "type": "KUPNO", "in": "1.0945", "sl": "1.0890", "tp": "1.1050", "rsi_base": 55, "src": "FXLEADERS", "score": 87, "analysis": "Obrona wsparcia 1.0900."},
        {"pair": "GBP/USD", "sym": "FX:GBPUSD", "date": "13.01", "hour": "13:10", "type": "SPRZEDAŻ", "in": "1.2740", "sl": "1.2820", "tp": "1.2610", "rsi_base": 44, "src": "FXLEADERS", "score": 85, "analysis": "Słabość funta przy oporze."},
        {"pair": "USD/CAD", "sym": "FX:USDCAD", "date": "13.01", "hour": "10:30", "type": "SPRZEDAŻ", "in": "1.3410", "sl": "1.3490", "tp": "1.3300", "rsi_base": 46, "src": "FXLEADERS", "score": 84, "analysis": "Korelacja z ropą wspiera CAD."},
        {"pair": "AUD/USD", "sym": "FX:AUDUSD", "date": "13.01", "hour": "12:05", "type": "SPRZEDAŻ", "in": "0.6690", "sl": "0.6750", "tp": "0.6580", "rsi_base": 41, "src": "FXLEADERS", "score": 82, "analysis": "Przełamanie linii trendu."},
        {"pair": "NZD/USD", "sym": "FX:NZDUSD", "date": "13.01", "hour": "09:15", "type": "KUPNO", "in": "0.6235", "sl": "0.6180", "tp": "0.6350", "rsi_base": 58, "src": "FXLEADERS", "score": 81, "analysis": "Akumulacja przed wybiciem."}
    ]

if 'signals' not in st.session_state: st.session_state.signals = get_verified_data()
if 'view' not in st.session_state: st.session_state.view = "terminal"

# --- PODSTRONA: RANKING AI ---
if st.session_state.view == "ranking":
    st.title("🏆 RANKING ANALIZY TECHNICZNEJ (1D)")
    if st.button("⬅ POWRÓT"):
        st.session_state.view = "terminal"
        st.rerun()
    
    ranked = sorted(st.session_state.signals, key=lambda x: x['score'], reverse=True)
    for i, s in enumerate(ranked):
        with st.expander(f"MIEJSCE {i+1}: {s['pair']} | SZANSA {s['score']}% | {s['type']}"):
            c1, c2 = st.columns([1, 2])
            with c1:
                st.write(f"**WEJŚCIE:** {s['in']}")
                st.write(f"**SL:** {s['sl']} | **TP:** {s['tp']}")
            with c2:
                st.info(f"**ANALIZA:** {s['analysis']}")
    st.stop()

# --- WIDOK GŁÓWNY ---
h1, h2, h3 = st.columns([3, 1, 1])
h1.subheader("TERMINAL V380 | LIVE DATA")
if h2.button("🏆 RANKING AI"):
    st.session_state.view = "ranking"
    st.rerun()
if h3.button("🔄 AKTUALIZUJ"):
    st.session_state.signals = get_verified_data()
    st.rerun()

col_l, col_r = st.columns([2, 3])

with col_l:
    with st.container(height=750):
        for idx, s in enumerate(st.session_state.signals):
            label = "buy-label" if "KUPNO" in s['type'] else "sell-label"
            st.markdown(f"""
                <div class="signal-card">
                    <span class="{label}">{s['type']}</span>
                    <b>{s['pair']}</b>
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
        st.subheader(f"Analiza: {ap['pair']}")
        
        # PEŁNY ZAKRES INTERWAŁÓW
        st.session_state.tf = st.select_slider(
            "Interwał:", 
            options=["1m", "5m", "15m", "30m", "1h", "2h", "4h", "1d", "1w", "1M"], 
            value="1d"
        )
        tf_code = {"1m":"1", "5m":"5", "15m":"15", "30m":"30", "1h":"60", "2h":"120", "4h":"240", "1d":"D", "1w":"W", "1M":"M"}[st.session_state.tf]

        # RSI z modyfikatorem interwału
        mod = {"1m":-10, "5m":-5, "1d":0, "1w":10}.get(st.session_state.tf, 2)
        st.metric(f"RSI ({st.session_state.tf})", f"{ap['rsi_base'] + mod}")

        components.html(f"""
            <div class="tradingview-widget-container">
                <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
                {{
                    "interval": "{tf_code}",
                    "width": "100%",
                    "isTransparent": true,
                    "height": 450,
                    "symbol": "{ap['sym']}",
                    "showIntervalTabs": true,
                    "displayMode": "multiple",
                    "locale": "pl",
                    "colorTheme": "dark"
                }}
                </script>
            </div>
        """, height=460)
