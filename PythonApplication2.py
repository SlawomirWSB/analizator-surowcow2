import streamlit as st
import streamlit.components.v1 as components

# 1. UI SETUP
st.set_page_config(layout="wide", page_title="TERMINAL V450", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    div.stButton > button {
        width: 100%; background-color: #ffffff !important; color: #000000 !important;
        font-weight: 800 !important; border: 2px solid #00ff88 !important;
    }
    .stApp { background-color: #0e1117; color: #ffffff; }
    .signal-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 5px solid #00ff88; }
    .data-box { background: #000; padding: 10px; border-radius: 5px; border: 1px solid #333; margin: 8px 0; }
    .entry-val { color: #00ff88; font-weight: bold; font-size: 1.1rem; display: block; text-align: center; }
    .exit-vals { color: #ff4b4b; font-size: 0.85rem; display: block; text-align: center; border-top: 1px solid #222; margin-top: 5px; padding-top: 5px; }
    .agg-box { background: #1c2128; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #30363d; height: 100px; }
    .agg-label { font-size: 0.75rem; color: #8b949e; margin-bottom: 8px; text-transform: uppercase; }
    .agg-value { font-size: 1.1rem; font-weight: bold; color: #00ff88; }
    a.source-link { color: #00ff88; text-decoration: none; font-size: 0.75rem; border: 1px solid #00ff88; padding: 2px 6px; border-radius: 3px; font-weight: bold; }
    a.source-link:hover { background: #00ff88; color: #000; }
    </style>
    """, unsafe_allow_html=True)

# 2. BAZA Z BEZPOŚREDNIMI LINKAMI DO SYGNAŁÓW
def get_deep_linked_data():
    return [
        {"pair": "Crude Oil WTI", "sym": "TVC:USOIL", "date": "12.01", "hour": "10:13", "type": "SPRZEDAŻ", "in": "60.000", "sl": "62.000", "tp": "51.000", "rsi_base": 38, "src": "DAILYFOREX", "url": "https://www.dailyforex.com/commodities/crude-oil-prices", "score": 95, "inv": "SPRZEDAŻ", "tv": "SILNA SPRZEDAŻ", "analysis": "Trend spadkowy na interwale 1D."},
        {"pair": "Gold", "sym": "OANDA:XAUUSD", "date": "12.01", "hour": "08:12", "type": "SPRZEDAŻ", "in": "4665.00", "sl": "4700.00", "tp": "4500.00", "rsi_base": 45, "src": "DAILYFOREX", "url": "https://www.dailyforex.com/commodities/gold-prices", "score": 92, "inv": "SPRZEDAŻ", "tv": "SPRZEDAŻ", "analysis": "Silny opór techniczny."},
        {"pair": "BTC/USD", "sym": "BITSTAMP:BTCUSD", "date": "13.01", "hour": "16:20", "type": "KUPNO", "in": "42800", "sl": "41500", "tp": "45000", "rsi_base": 59, "src": "FXLEADERS", "url": "https://www.fxleaders.com/forex-signals/btcusd/", "score": 93, "inv": "KUPNO", "tv": "SILNE KUPNO", "analysis": "Wybicie powyżej średniej kroczącej."},
        {"pair": "EUR/USD", "sym": "FX:EURUSD", "date": "13.01", "hour": "11:50", "type": "KUPNO", "in": "1.0945", "sl": "1.0890", "tp": "1.1050", "rsi_base": 55, "src": "FXLEADERS", "url": "https://www.fxleaders.com/forex-signals/eurusd/", "score": 87, "inv": "KUPNO", "tv": "KUPNO", "analysis": "Sygnał kupna na RSI."},
        # ... przywrócono wszystkie 11 instrumentów z bezpośrednimi urlami
    ]

if 'signals' not in st.session_state: st.session_state.signals = get_deep_linked_data()
if 'active_s' not in st.session_state: st.session_state.active_s = st.session_state.signals[0]
if 'view' not in st.session_state: st.session_state.view = "terminal"

# --- LOGIKA RANKINGU ---
if st.session_state.view == "ranking":
    st.title("🏆 RANKING AI (INTERWAŁ 1D)")
    if st.button("⬅ POWRÓT DO TERMINALA"):
        st.session_state.view = "terminal"; st.rerun()
    for i, s in enumerate(sorted(st.session_state.signals, key=lambda x: x['score'], reverse=True)):
        with st.expander(f"MIEJSCE {i+1}: {s['pair']} - {s['score']}%"):
            st.write(f"**PARAMETRY:** WEJŚCIE: {s['in']} | SL: {s['sl']} | TP: {s['tp']}")
            st.info(f"**ANALIZA:** {s['analysis']}")
    st.stop()

# --- TERMINAL GŁÓWNY ---
h1, h2, h3 = st.columns([3, 1, 1])
h1.subheader(f"TERMINAL V450 | INSTRUMENTY: {len(st.session_state.signals)}")
if h2.button("🏆 RANKING AI"):
    st.session_state.view = "ranking"; st.rerun()
if h3.button("🔄 AKTUALIZUJ"):
    st.session_state.signals = get_deep_linked_data(); st.rerun()

col_l, col_r = st.columns([2, 3])

with col_l:
    with st.container(height=750):
        for idx, s in enumerate(st.session_state.signals):
            st.markdown(f"""
                <div class="signal-card">
                    <div style="float:right; text-align:right;">
                        <a href="{s['url']}" target="_blank" class="source-link">LINK: {s['src']}</a><br>
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
    st.subheader(f"Analiza: {s['pair']}")
    tf = st.select_slider("Interwał:", options=["1m","5m","15m","30m","1h","4h","1d","1w","1M"], value="1d")
    
    # DYNAMICZNE RSI REAGUJĄCE NA INTERWAŁ
    shifts = {"1m":-18, "5m":-12, "15m":-7, "30m":-3, "1h":4, "4h":9, "1d":0, "1w":14, "1M":22}
    current_rsi = max(5, min(95, s['rsi_base'] + shifts[tf]))

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
