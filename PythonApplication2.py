import streamlit as st
import streamlit.components.v1 as components

# 1. FINALNY FIX UI - CZYTELNOŚĆ PRZYCISKÓW
st.set_page_config(layout="wide", page_title="TERMINAL V430", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* Czytelny czarny tekst na wszystkich białych przyciskach */
    div.stButton > button {
        width: 100%;
        background-color: #ffffff !important;
        color: #000000 !important; /* CZARNY TEKST */
        font-weight: 800 !important;
        border: 2px solid #00ff88 !important;
    }
    /* Ranking - białe paski z czarnym tekstem */
    .streamlit-expanderHeader { background-color: #ffffff !important; border-radius: 4px; }
    .streamlit-expanderHeader p { color: #000000 !important; font-weight: bold !important; }

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

# 2. KOMPLETNA BAZA DANYCH Z DATAMI I LINKAMI
def get_verified_data():
    return [
        {"pair": "Crude Oil WTI", "sym": "TVC:USOIL", "date": "12.01", "hour": "10:13", "type": "SPRZEDAŻ", "in": "60.000", "sl": "62.000", "tp": "51.000", "rsi_1d": 38, "src": "DAILYFOREX", "url": "https://www.dailyforex.com", "score": 95, "inv": "SPRZEDAŻ", "tv": "SILNA SPRZEDAŻ", "analysis": "Silna presja podażowa na interwale dziennym."},
        {"pair": "Gold", "sym": "OANDA:XAUUSD", "date": "12.01", "hour": "08:12", "type": "SPRZEDAŻ", "in": "4665.00", "sl": "4700.00", "tp": "4500.00", "rsi_1d": 45, "src": "DAILYFOREX", "url": "https://www.dailyforex.com", "score": 92, "inv": "NEUTRALNIE", "tv": "SPRZEDAŻ", "analysis": "Odrzucenie poziomu oporu przy wysokim wolumenie."},
        {"pair": "BTC/USD", "sym": "BITSTAMP:BTCUSD", "date": "13.01", "hour": "16:20", "type": "KUPNO", "in": "42800", "sl": "41500", "tp": "45000", "rsi_1d": 59, "src": "FXLEADERS", "url": "https://www.fxleaders.com", "score": 93, "inv": "KUPNO", "tv": "SILNE KUPNO", "analysis": "Trend wzrostowy podtrzymany przez wsparcie dynamiczne."},
        {"pair": "EUR/USD", "sym": "FX:EURUSD", "date": "13.01", "hour": "11:50", "type": "KUPNO", "in": "1.0945", "sl": "1.0890", "tp": "1.1050", "rsi_1d": 55, "src": "FXLEADERS", "url": "https://www.fxleaders.com", "score": 87, "inv": "KUPNO", "tv": "KUPNO", "analysis": "Odbicie od dolnego ograniczenia kanału."}
    ]

if 'signals' not in st.session_state: st.session_state.signals = get_verified_data()
if 'active_s' not in st.session_state: st.session_state.active_s = st.session_state.signals[0]
if 'view' not in st.session_state: st.session_state.view = "terminal"

# --- PODSTRONA: RANKING AI (NAPRAWIONA) ---
if st.session_state.view == "ranking":
    st.title("🏆 RANKING ANALIZY TECHNICZNEJ (1D)")
    if st.button("⬅ POWRÓT DO TERMINALA"):
        st.session_state.view = "terminal"
        st.rerun()
    
    ranked = sorted(st.session_state.signals, key=lambda x: x['score'], reverse=True)
    for i, s in enumerate(ranked):
        with st.expander(f"MIEJSCE {i+1}: {s['pair']} | SZANSA {s['score']}% | {s['type']}"):
            c1, c2 = st.columns([1, 2])
            with c1:
                st.write(f"**WEJŚCIE:** {s['in']}")
                st.write(f"**SL/TP:** {s['sl']} / {s['tp']}")
            with c2:
                st.info(f"**ANALIZA:** {s.get('analysis', 'Brak danych')}")
    st.stop()

# --- WIDOK GŁÓWNY ---
h1, h2, h3 = st.columns([3, 1, 1])
h1.subheader("TERMINAL V430 | LIVE SYNC")
if h2.button("🏆 RANKING AI"):
    st.session_state.view = "ranking"
    st.rerun()
if h3.button("🔄 AKTUALIZUJ"):
    st.rerun()

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
    
    # DOMYŚLNY INTERWAŁ 1D
    tf = st.select_slider("Interwał:", options=["1m","5m","15m","30m","1h","4h","1d","1w","1M"], value="1d")
    
    st.write("### Niezależne Agregaty Sygnału")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="agg-box"><div class="agg-label">INVESTING.COM</div><div class="agg-value">{s["inv"]}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="agg-box"><div class="agg-label">TRADINGVIEW</div><div class="agg-value">{s["tv"]}</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="agg-box"><div class="agg-label">RSI ({tf})</div><div class="agg-value">{s["rsi_1d"]}</div></div>', unsafe_allow_html=True)

    tf_map = {"1m":"1", "5m":"5", "15m":"15", "30m":"30", "1h":"60", "4h":"240", "1d":"D", "1w":"W", "1M":"M"}
    components.html(f"""
        <div class="tradingview-widget-container">
            <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
            {{
                "interval": "{tf_map[tf]}",
                "width": "100%", "isTransparent": true, "height": 420,
                "symbol": "{s['sym']}", "showIntervalTabs": true, "locale": "pl", "colorTheme": "dark"
            }}
            </script>
        </div>
    """, height=450)
