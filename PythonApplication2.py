import streamlit as st
import streamlit.components.v1 as components
import random

# 1. KONFIGURACJA WIDOKU
st.set_page_config(layout="wide", page_title="TERMINAL V220", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .signal-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 5px solid #00ff88; }
    .entry-box { background: #000; padding: 10px; border-radius: 5px; color: #00ff88; font-family: 'Courier New'; text-align: center; border: 1px solid #00ff88; margin: 8px 0; font-weight: bold; }
    .tg-btn { background-color: #0088cc; color: white !important; text-decoration: none; padding: 3px 10px; border-radius: 4px; font-size: 0.7rem; font-weight: bold; float: right; }
    .time-stamp { color: #888; font-size: 0.7rem; float: right; margin-top: 2px; }
    div.stButton > button { width: 100%; background-color: #262730 !important; color: #00ff88 !important; border: 1px solid #00ff88 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. KOMPLETNA BAZA DANYCH (10.01 - 12.01)
if 'db' not in st.session_state:
    st.session_state.db = [
        # 12.01 (DZISIAJ)
        {"pair": "AUD/CHF", "sym": "FX:AUDCHF", "time": "18:33", "date": "12.01", "type": "KUPNO", "in": "0.5344", "rsi": 50, "szansa": "88%"},
        {"pair": "NZD/CHF", "sym": "FX:NZDCHF", "time": "14:42", "date": "12.01", "type": "SPRZEDAŻ", "in": "0.5412", "rsi": 42, "szansa": "96%"},
        {"pair": "XAU/USD", "sym": "OANDA:XAUUSD", "time": "18:34", "date": "12.01", "type": "KUPNO", "in": "2397.56", "rsi": 60, "szansa": "94%"},
        # 11.01 (WCZORAJ)
        {"pair": "GBP/JPY", "sym": "FX:GBPJPY", "time": "11:46", "date": "11.01", "type": "SPRZEDAŻ", "in": "211.700", "rsi": 62, "szansa": "91%"},
        {"pair": "US30", "sym": "TVC:US30", "time": "20:45", "date": "11.01", "type": "SPRZEDAŻ", "in": "37580", "rsi": 55, "szansa": "89%"},
        {"pair": "NATGAS", "sym": "TVC:NATGAS", "time": "14:18", "date": "11.01", "type": "KUPNO", "in": "2.850", "rsi": 48, "szansa": "92%"},
        # 10.01 (PRZEDWCZORAJ)
        {"pair": "EUR/USD", "sym": "FX:EURUSD", "time": "20:46", "date": "10.01", "type": "KUPNO", "in": "1.0945", "rsi": 57, "szansa": "93%"},
        {"pair": "GBP/JPY", "sym": "FX:GBPJPY", "time": "20:40", "date": "10.01", "type": "SPRZEDAŻ", "in": "210.500", "rsi": 65, "szansa": "87%"},
        {"pair": "US30", "sym": "TVC:US30", "time": "16:37", "date": "10.01", "type": "SPRZEDAŻ", "in": "37400", "rsi": 52, "szansa": "90%"}
    ]

# Inicjalizacja stanu
if 'sel_date' not in st.session_state: st.session_state.sel_date = "12.01"
if 'tf' not in st.session_state: st.session_state.tf = "4h"

# --- NAGŁÓWEK ---
h1, h2, h3 = st.columns([3, 1, 1])
h1.subheader(f"TERMINAL V220 | WIDOK: {st.session_state.sel_date}")
if h2.button("🏆 AI RANKING"): st.info("Ranking Top 12 aktywny"); st.rerun()

# Nawigacja dat (Naprawa braku instrumentów)
n1, n2, n3 = st.columns(3)
if n1.button("12.01 (DZISIAJ)"): st.session_state.sel_date = "12.01"; st.rerun()
if n2.button("11.01 (WCZORAJ)"): st.session_state.sel_date = "11.01"; st.rerun()
if n3.button("10.01 (PRZEDWCZORAJ)"): st.session_state.sel_date = "10.01"; st.rerun()

col_l, col_r = st.columns([2, 3])

with col_l:
    # Filtrowanie bezpieczne (naprawa KeyError)
    filtered = [s for s in st.session_state.db if s['date'] == st.session_state.sel_date]
    st.write(f"Sygnały dla {st.session_state.sel_date} ({len(filtered)})")
    
    with st.container(height=650):
        for idx, s in enumerate(filtered):
            st.markdown(f"""
                <div class="signal-card">
                    <span class="time-stamp">{s['time']}</span>
                    <a href="#" class="tg-btn">TELEGRAM</a>
                    <b>{s['pair']}</b> <span style="color:#00ff88">{s['type']}</span>
                    <div class="entry-box">WEJŚCIE: {s['in']}</div>
                    <small>RSI: {s['rsi']} | Szansa: {s['szansa']}</small>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"ANALIZUJ {s['pair']}", key=f"btn_{idx}"):
                st.session_state.active_pair = s

with col_r:
    if 'active_pair' in st.session_state:
        ap = st.session_state.active_pair
        st.subheader(f"Analiza techniczna: {ap['pair']}")
        
        st.session_state.tf = st.select_slider("Interwał:", options=["1m", "5m", "15m", "1h", "4h", "1d", "1w"], value=st.session_state.tf)
        tf_code = {"1m":"1", "5m":"5", "15m":"15", "1h":"60", "4h":"240", "1d":"D", "1w":"W"}[st.session_state.tf]

        # Stabilny widżet techniczny (Naprawa zegarów)
        components.html(f"""
            <div class="tradingview-widget-container">
              <div class="tradingview-widget-container__widget"></div>
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
        """, height=600)
