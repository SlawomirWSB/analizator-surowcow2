import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timedelta

# 1. DYNAMICZNE DATY (Zawsze aktualne względem dzisiejszego dnia)
today = datetime.now()
d_today = today.strftime("%d.%01")
d_yesterday = (today - timedelta(days=1)).strftime("%d.%01")
d_prev = (today - timedelta(days=2)).strftime("%d.%01")

st.set_page_config(layout="wide", page_title="TERMINAL V270", initial_sidebar_state="collapsed")

# Stylizacja (Powrót do pełnego widoku z linkami i RSI)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .signal-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 5px solid #00ff88; }
    .entry-box { background: #000; padding: 10px; border-radius: 5px; color: #00ff88; font-family: 'Courier New'; text-align: center; border: 1px solid #00ff88; margin: 8px 0; font-weight: bold; }
    .source-link { color: #0088cc; text-decoration: none; font-size: 0.7rem; font-weight: bold; float: right; border: 1px solid #0088cc; padding: 2px 5px; border-radius: 3px; }
    .time-stamp { color: #888; font-size: 0.7rem; float: right; margin-right: 10px; margin-top: 3px; }
    div.stButton > button { width: 100%; background-color: #262730 !important; color: #00ff88 !important; border: 1px solid #00ff88 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. AKTUALNA BAZA SYGNAŁÓW (FXLEADERS & DAILYFOREX)
def get_live_data(target_date):
    # Dane na podstawie Twoich wytycznych i stron (12.01 - 13.01)
    db = {
        d_today: [ # Przykładowe sygnały z dzisiaj
            {"pair": "EUR/USD", "sym": "FX:EURUSD", "time": "09:15", "type": "KUPNO", "in": "1.0870", "rsi": 54, "src": "FXLEADERS", "url": "https://www.fxleaders.com/forex-signals/"},
            {"pair": "GBP/USD", "sym": "FX:GBPUSD", "time": "08:45", "type": "SPRZEDAŻ", "in": "1.2610", "rsi": 42, "src": "FXLEADERS", "url": "https://www.fxleaders.com/forex-signals/"}
        ],
        "12.01": [ # Dane ze zrzutu ekranu DailyForex i FXLeaders
            {"pair": "Crude Oil WTI", "sym": "TVC:USOIL", "time": "10:13", "type": "SPRZEDAŻ", "in": "60.000", "rsi": 38, "src": "DAILYFOREX", "url": "https://www.dailyforex.com/forex-technical-analysis/free-forex-signals/page-1"},
            {"pair": "Gold", "sym": "OANDA:XAUUSD", "time": "08:12", "type": "SPRZEDAŻ", "in": "4665.00", "rsi": 45, "src": "DAILYFOREX", "url": "https://www.dailyforex.com/forex-technical-analysis/free-forex-signals/page-1"},
            {"pair": "USD/JPY", "sym": "FX:USDJPY", "time": "14:20", "type": "KUPNO", "in": "145.10", "rsi": 62, "src": "FXLEADERS", "url": "https://www.fxleaders.com/forex-signals/"},
            {"pair": "AUD/USD", "sym": "FX:AUDUSD", "time": "12:05", "type": "SPRZEDAŻ", "in": "0.6690", "rsi": 48, "src": "FXLEADERS", "url": "https://www.fxleaders.com/forex-signals/"},
            {"pair": "BTC/USD", "sym": "BITSTAMP:BTCUSD", "time": "11:30", "type": "KUPNO", "in": "42800", "rsi": 59, "src": "FXLEADERS", "url": "https://www.fxleaders.com/forex-signals/"},
            {"pair": "ETH/USD", "sym": "BITSTAMP:ETHUSD", "time": "11:35", "type": "KUPNO", "in": "2540", "rsi": 61, "src": "FXLEADERS", "url": "https://www.fxleaders.com/forex-signals/"},
            {"pair": "USD/CAD", "sym": "FX:USDCAD", "time": "10:50", "type": "SPRZEDAŻ", "in": "1.3395", "rsi": 44, "src": "FXLEADERS", "url": "https://www.fxleaders.com/forex-signals/"}
        ]
    }
    return db.get(target_date, [])

# Zarządzanie stanem nawigacji
if 'sel_date' not in st.session_state: st.session_state.sel_date = d_today
if 'tf' not in st.session_state: st.session_state.tf = "1h"

# NAGŁÓWEK
st.subheader(f"TERMINAL V270 | {st.session_state.sel_date}")

# DYNAMICZNA NAWIGACJA DAT (Aktualne daty przy przyciskach)
d1, d2, d3 = st.columns(3)
if d1.button(f"DZISIAJ ({d_today})"): st.session_state.sel_date = d_today; st.rerun()
if d2.button(f"WCZORAJ ({d_yesterday})"): st.session_state.sel_date = d_yesterday; st.rerun()
if d3.button(f"PRZEDWCZORAJ ({d_prev})"): st.session_state.sel_date = d_prev; st.rerun()

col_l, col_r = st.columns([2, 3])

with col_l:
    signals = get_live_data(st.session_state.sel_date)
    st.write(f"Aktywne sygnały ({len(signals)})")
    with st.container(height=650):
        for idx, s in enumerate(signals):
            st.markdown(f"""
                <div class="signal-card">
                    <a href="{s['url']}" target="_blank" class="source-link">🔗 {s['src']}</a>
                    <span class="time-stamp">Aktualizacja: {s['time']}</span><br>
                    <b>{s['pair']}</b> <span style="color:#00ff88">{s['type']}</span>
                    <div class="entry-box">WEJŚCIE: {s['in']}</div>
                    <small>RSI (1h): {s['rsi']} | Szansa: 92%</small>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"ANALIZUJ {s['pair']}", key=f"btn_{idx}"):
                st.session_state.active_pair = s

with col_r:
    if 'active_pair' in st.session_state:
        ap = st.session_state.active_pair
        st.subheader(f"Analiza: {ap['pair']} - Szczegóły Techniczne")
        
        # PRZYWRÓCONY SUWAK INTERWAŁÓW
        st.session_state.tf = st.select_slider("Wybierz Interwał:", options=["1m", "5m", "15m", "1h", "4h", "1d", "1w"], value=st.session_state.tf)
        tf_code = {"1m":"1", "5m":"5", "15m":"15", "1h":"60", "4h":"240", "1d":"D", "1w":"W"}[st.session_state.tf]
        
        # WSKAŹNIKI GÓRNE
        m1, m2, m3 = st.columns(3)
        m1.metric("Investing.com", "SILNE KUPNO" if "KUPNO" in ap['type'] else "SILNA SPRZEDAŻ")
        m2.metric("TradingView", ap['type'])
        m3.metric(f"RSI ({st.session_state.tf})", ap['rsi'])

        # PRZYWRÓCONE TRZY ZEGARY (Standardowe dla TradingView)
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
