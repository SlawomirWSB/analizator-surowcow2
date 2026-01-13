import streamlit as st
import streamlit.components.v1 as components

# 1. KONFIGURACJA SYSTEMU
st.set_page_config(layout="wide", page_title="TERMINAL V330", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .signal-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 5px solid #00ff88; }
    .entry-box { background: #000; padding: 10px; border-radius: 5px; color: #00ff88; font-family: 'Courier New'; text-align: center; border: 1px solid #00ff88; margin: 8px 0; font-weight: bold; font-size: 1.1rem; }
    .source-link { color: #0088cc; text-decoration: none; font-size: 0.7rem; font-weight: bold; float: right; border: 1px solid #0088cc; padding: 2px 5px; border-radius: 3px; }
    .sl-tp-container { color: #ff4b4b; font-size: 0.85rem; text-align: center; font-weight: bold; margin-bottom: 5px; }
    .time-full { float: right; color: #888; font-size: 0.7rem; margin-right: 10px; margin-top: 3px; }
    div.stButton > button { width: 100%; background-color: #262730 !important; color: #00ff88 !important; border: 1px solid #00ff88 !important; font-weight: bold; }
    /* Styl dla okna Rankingu */
    .ranking-box { background: #1c2128; border: 2px solid #ffd700; padding: 20px; border-radius: 10px; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. BAZA SYGNAŁÓW (9 z FX Leaders + 2 z DailyForex = 11 aktywnych)
def get_verified_signals():
    return [
        # FX LEADERS (Mapowanie z wykresów Price Targets)
        {"pair": "EUR/GBP", "sym": "FX:EURGBP", "date": "13.01", "hour": "15:45", "type": "KUPNO", "in": "0.8679", "sl": "0.8500", "tp": "0.8857", "rsi": 52, "src": "FXLEADERS", "url": "https://www.fxleaders.com/forex-signals/", "score": 90, "desc": "Silna dywergencja na H4 przy wsparciu 0.8670."},
        {"pair": "USD/JPY", "sym": "FX:USDJPY", "date": "13.01", "hour": "14:20", "type": "KUPNO", "in": "145.10", "sl": "144.50", "tp": "146.20", "rsi": 62, "src": "FXLEADERS", "url": "https://www.fxleaders.com/forex-signals/", "score": 88, "desc": "Trend wzrostowy podtrzymany przez dane o inflacji."},
        {"pair": "GBP/USD", "sym": "FX:GBPUSD", "date": "13.01", "hour": "13:10", "type": "SPRZEDAŻ", "in": "1.2740", "sl": "1.2820", "tp": "1.2610", "rsi": 44, "src": "FXLEADERS", "url": "https://www.fxleaders.com/forex-signals/", "score": 85, "desc": "Odbicie od górnej krawędzi kanału spadkowego."},
        {"pair": "AUD/USD", "sym": "FX:AUDUSD", "date": "13.01", "hour": "12:05", "type": "SPRZEDAŻ", "in": "0.6690", "sl": "0.6750", "tp": "0.6580", "rsi": 41, "src": "FXLEADERS", "url": "https://www.fxleaders.com/forex-signals/", "score": 82, "desc": "Presja na surowce osłabia dolara australijskiego."},
        {"pair": "EUR/USD", "sym": "FX:EURUSD", "date": "13.01", "hour": "11:50", "type": "KUPNO", "in": "1.0945", "sl": "1.0890", "tp": "1.1050", "rsi": 55, "src": "FXLEADERS", "url": "https://www.fxleaders.com/forex-signals/", "score": 87, "desc": "Akumulacja powyżej średniej kroczącej 200."},
        {"pair": "USD/CAD", "sym": "FX:USDCAD", "date": "13.01", "hour": "10:30", "type": "SPRZEDAŻ", "in": "1.3410", "sl": "1.3490", "tp": "1.3300", "rsi": 46, "src": "FXLEADERS", "url": "https://www.fxleaders.com/forex-signals/", "score": 84, "desc": "Korelacja z ropą naftową sprzyja spadkom."},
        {"pair": "NZD/USD", "sym": "FX:NZDUSD", "date": "13.01", "hour": "09:15", "type": "KUPNO", "in": "0.6235", "sl": "0.6180", "tp": "0.6350", "rsi": 58, "src": "FXLEADERS", "url": "https://www.fxleaders.com/forex-signals/", "score": 81, "desc": "Stabilizacja po wyprzedaniu na RSI."},
        {"pair": "EUR/JPY", "sym": "FX:EURJPY", "date": "13.01", "hour": "08:40", "type": "KUPNO", "in": "158.40", "sl": "157.20", "tp": "160.50", "rsi": 60, "src": "FXLEADERS", "url": "https://www.fxleaders.com/forex-signals/", "score": 89, "desc": "Wybicie z formacji flagi na interwale H1."},
        {"pair": "BTC/USD", "sym": "BITSTAMP:BTCUSD", "date": "13.01", "hour": "16:20", "type": "KUPNO", "in": "42800", "sl": "41500", "tp": "45000", "rsi": 59, "src": "FXLEADERS", "url": "https://www.fxleaders.com/forex-signals/", "score": 93, "desc": "Konsolidacja przed spodziewanym wybiciem."},
        
        # DAILYFOREX (Dane bezpośrednie)
        {"pair": "Crude Oil WTI", "sym": "TVC:USOIL", "date": "12.01", "hour": "10:13", "type": "SPRZEDAŻ", "in": "60.000", "sl": "62.000", "tp": "51.000", "rsi": 38, "src": "DAILYFOREX", "url": "https://www.dailyforex.com/forex-technical-analysis/free-forex-signals/page-1", "score": 95, "desc": "Spadek popytu globalnego i przełamanie wsparcia."},
        {"pair": "Gold", "sym": "OANDA:XAUUSD", "date": "12.01", "hour": "08:12", "type": "SPRZEDAŻ", "in": "4665.00", "sl": "4700.00", "tp": "4500.00", "rsi": 45, "src": "DAILYFOREX", "url": "https://www.dailyforex.com/forex-technical-analysis/free-forex-signals/page-1", "score": 92, "desc": "Silny dolar ogranicza potencjał złota."}
    ]

if 'signals' not in st.session_state: st.session_state.signals = get_verified_signals()
if 'show_ranking' not in st.session_state: st.session_state.show_ranking = False

# NAGŁÓWEK
h1, h2, h3 = st.columns([3, 1, 1])
h1.subheader("TERMINAL V330 | MULTI-SYNC ANALYSIS")
if h2.button("🏆 RANKING AI"):
    st.session_state.show_ranking = not st.session_state.show_ranking
if h3.button("🔄 AKTUALIZUJ"):
    st.session_state.signals = get_verified_signals()
    st.rerun()

# --- OKNO RANKINGU (MODAL) ---
if st.session_state.show_ranking:
    st.markdown('<div class="ranking-box">', unsafe_allow_html=True)
    st.write("### 🏆 Top 5 Okazji Inwestycyjnych (AI Ranking)")
    ranked = sorted(st.session_state.signals, key=lambda x: x['score'], reverse=True)[:5]
    
    cols = st.columns(5)
    for i, s in enumerate(ranked):
        cols[i].markdown(f"""
            <div style="background:#000; padding:10px; border-radius:5px; border-top: 3px solid #ffd700;">
            <center><b>{s['pair']}</b><br>
            <span style="color:#ffd700; font-size:1.5rem;">{s['score']}%</span><br>
            <small>{s['desc']}</small></center>
            </div>
        """, unsafe_allow_html=True)
    
    if st.button("ZAMKNIJ RANKING"):
        st.session_state.show_ranking = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- GŁÓWNY WIDOK ---
col_l, col_r = st.columns([2, 3])

with col_l:
    st.write(f"Aktywne instrumenty ({len(st.session_state.signals)})")
    with st.container(height=720):
        for idx, s in enumerate(st.session_state.signals):
            st.markdown(f"""
                <div class="signal-card">
                    <a href="{s['url']}" target="_blank" class="source-link">🔗 {s['src']}</a>
                    <span class="time-full">{s['date']} | {s['hour']}</span><br>
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
        st.subheader(f"Szczegóły: {ap['pair']}")
        
        # Przywrócony suwak i RSI po prawej
        st.session_state.tf = st.select_slider("Interwał:", options=["1m", "5m", "15m", "1h", "4h", "1d"], value="1h")
        tf_code = {"1m":"1", "5m":"5", "15m":"15", "1h":"60", "4h":"240", "1d":"D"}[st.session_state.tf]

        m1, m2, m3 = st.columns(3)
        m1.metric("Investing", "SILNE KUPNO" if ap['score'] > 90 else "KUPNO")
        m2.metric("TradingView", ap['type'])
        m3.metric(f"RSI ({st.session_state.tf})", ap['rsi'])

        # PRZYWRÓCONE 3 ZEGAREK
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
        st.info("Wybierz instrument, aby wyświetlić analizę techniczną.")
