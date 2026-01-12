import streamlit as st
import streamlit.components.v1 as components
import random

# 1. KONFIGURACJA GŁÓWNA
st.set_page_config(layout="wide", page_title="TERMINAL V250", initial_sidebar_state="collapsed")

# Stylizacja interfejsu
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .signal-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 5px solid #00ff88; }
    .entry-box { background: #000; padding: 10px; border-radius: 5px; color: #00ff88; font-family: 'Courier New'; text-align: center; border: 1px solid #00ff88; margin: 8px 0; font-weight: bold; font-size: 1.1rem; }
    .tg-btn { background-color: #0088cc; color: white !important; text-decoration: none; padding: 4px 12px; border-radius: 4px; font-size: 0.75rem; font-weight: bold; float: right; }
    .time-stamp { color: #888; font-size: 0.75rem; float: right; margin-top: 2px; margin-right: 10px; }
    div.stButton > button { width: 100%; background-color: #262730 !important; color: #00ff88 !important; border: 1px solid #00ff88 !important; font-weight: bold; height: 45px; }
    </style>
    """, unsafe_allow_html=True)

# 2. BAZA DANYCH (Zdefiniowana poza session_state, aby uniknąć błędów AttributeError)
def get_signals_for_date(target_date):
    db = {
        "12.01": [
            {"pair": "AUD/CHF", "sym": "FX:AUDCHF", "time": "18:33", "type": "KUPNO", "in": "0.5344", "rsi": 50, "szansa": "88%"},
            {"pair": "NZD/CHF", "sym": "FX:NZDCHF", "time": "14:42", "type": "SPRZEDAŻ", "in": "0.5412", "rsi": 42, "szansa": "96%"},
            {"pair": "XAU/USD", "sym": "OANDA:XAUUSD", "time": "18:34", "type": "KUPNO", "in": "2397.56", "rsi": 60, "szansa": "94%"},
            {"pair": "USD/JPY", "sym": "FX:USDJPY", "time": "16:25", "type": "KUPNO", "in": "144.50", "rsi": 45, "szansa": "90%"}
        ],
        "11.01": [
            {"pair": "XAU/USD", "sym": "OANDA:XAUUSD", "time": "15:46", "type": "KUPNO", "in": "2380.10", "rsi": 62, "szansa": "91%"},
            {"pair": "GBP/JPY", "sym": "FX:GBPJPY", "time": "11:46", "type": "SPRZEDAŻ", "in": "211.70", "rsi": 68, "szansa": "89%"},
            {"pair": "US30", "sym": "TVC:US30", "time": "20:45", "type": "SPRZEDAŻ", "in": "37580", "rsi": 55, "szansa": "92%"},
            {"pair": "NATGAS", "sym": "TVC:NATGAS", "time": "14:18", "type": "KUPNO", "in": "2.85", "rsi": 48, "szansa": "87%"}
        ],
        "10.01": [
            {"pair": "EUR/USD", "sym": "FX:EURUSD", "time": "20:46", "type": "KUPNO", "in": "1.0945", "rsi": 57, "szansa": "93%"},
            {"pair": "GBP/JPY", "sym": "FX:GBPJPY", "time": "20:40", "type": "SPRZEDAŻ", "in": "210.50", "rsi": 65, "szansa": "88%"},
            {"pair": "US30", "sym": "TVC:US30", "time": "16:37", "type": "SPRZEDAŻ", "in": "37400", "rsi": 52, "szansa": "90%"}
        ]
    }
    return db.get(target_date, [])

# Inicjalizacja domyślnych wartości
if 'sel_date' not in st.session_state: st.session_state.sel_date = "12.01"
if 'tf' not in st.session_state: st.session_state.tf = "1h"

# --- NAGŁÓWEK ---
h1, h2 = st.columns([4, 1])
h1.subheader(f"TERMINAL V250 | WIDOK: {st.session_state.sel_date}")
if h2.button("🏆 AI RANKING"): st.toast("Ranking załadowany!")

# Nawigacja dat (Naprawione działanie przycisku Przedwczoraj)
d1, d2, d3 = st.columns(3)
if d1.button("DZISIAJ (12.01)"): st.session_state.sel_date = "12.01"; st.rerun()
if d2.button("WCZORAJ (11.01)"): st.session_state.sel_date = "11.01"; st.rerun()
if d3.button("PRZEDWCZORAJ (10.01)"): st.session_state.sel_date = "10.01"; st.rerun()

col_l, col_r = st.columns([2, 3])

with col_l:
    signals = get_signals_for_date(st.session_state.sel_date)
    st.write(f"Lista sygnałów ({len(signals)})")
    
    with st.container(height=650):
        for idx, s in enumerate(signals):
            st.markdown(f"""
                <div class="signal-card">
                    <span class="time-stamp">{s['time']}</span>
                    <a href="#" class="tg-btn">TELEGRAM</a>
                    <b>{s['pair']}</b> <span style="color:#00ff88">{s['type']}</span>
                    <div class="entry-box">WEJŚCIE: {s['in']}</div>
                    <small>RSI: {s['rsi']} | Szansa: {s['szansa']}</small>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"ANALIZUJ {s['pair']}", key=f"btn_{idx}_{st.session_state.sel_date}"):
                st.session_state.active_pair = s

with col_r:
    if 'active_pair' in st.session_state:
        ap = st.session_state.active_pair
        st.subheader(f"Analiza techniczna: {ap['pair']}")
        
        # Wybór interwału
        st.session_state.tf = st.select_slider("Wybierz TF:", options=["1m", "5m", "15m", "1h", "4h", "1d", "1w"], value=st.session_state.tf)
        tf_code = {"1m":"1", "5m":"5", "15m":"15", "1h":"60", "4h":"240", "1d":"D", "1w":"W"}[st.session_state.tf]

        # Wskaźniki górne
        m1, m2, m3 = st.columns(3)
        m1.metric("Investing", "KUPNO")
        m2.metric("TradingView", ap['type'])
        m3.metric(f"RSI ({st.session_state.tf})", ap['rsi'])

        # OFICJALNY WIDŻET TECHNICZNY (Naprawa czarnych pól)
        components.html(f"""
            <div class="tradingview-widget-container" style="height:550px;">
                <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
                {{
                    "interval": "{tf_code}",
                    "width": "100%",
                    "isTransparent": true,
                    "height": 530,
                    "symbol": "{ap['sym']}",
                    "showIntervalTabs": true,
                    "displayMode": "multiple",
                    "locale": "pl",
                    "colorTheme": "dark"
                }}
                </script>
            </div>
        """, height=550)
    else:
        st.info("Wybierz instrument z listy po lewej stronie, aby wyświetlić analizę.")
