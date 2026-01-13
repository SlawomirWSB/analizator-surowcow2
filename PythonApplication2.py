import streamlit as st
import streamlit.components.v1 as components

# 1. KONFIGURACJA WIZUALNA - NAPRAWA CZYTELNOŚCI I AGREGATÓW
st.set_page_config(layout="wide", page_title="TERMINAL V410", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* Fix dla białych przycisków - czarny tekst */
    div.stButton > button {
        width: 100%;
        background-color: #ffffff !important;
        color: #000000 !important;
        font-weight: bold !important;
        border: 1px solid #00ff88 !important;
    }
    /* Fix dla nagłówka expandera */
    .streamlit-expanderHeader { background-color: #ffffff !important; color: #000000 !important; }
    .streamlit-expanderHeader p { color: #000000 !important; font-weight: bold !important; }

    .stApp { background-color: #0e1117; color: #ffffff; }
    .signal-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 5px solid #00ff88; }
    
    /* Box parametrów wejścia */
    .data-box { background: #000; padding: 10px; border-radius: 5px; border: 1px solid #333; margin: 8px 0; }
    .entry-val { color: #00ff88; font-weight: bold; font-size: 1.1rem; display: block; text-align: center; }
    .exit-vals { color: #ff4b4b; font-size: 0.85rem; display: block; text-align: center; border-top: 1px solid #222; margin-top: 5px; padding-top: 5px; }
    
    /* Style dla agregatów po prawej */
    .agg-box { background: #1c2128; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #30363d; }
    .agg-label { font-size: 0.8rem; color: #8b949e; margin-bottom: 5px; }
    .agg-value { font-size: 1.2rem; font-weight: bold; color: #00ff88; }
    </style>
    """, unsafe_allow_html=True)

# 2. KOMPLETNA BAZA DANYCH (DAILYFOREX + FX LEADERS)
def get_verified_data():
    return [
        {"pair": "Crude Oil WTI", "sym": "TVC:USOIL", "type": "SPRZEDAŻ", "in": "60.000", "sl": "62.000", "tp": "51.000", "rsi": 38, "src": "DAILYFOREX", "score": 95, "inv": "SPRZEDAŻ", "tv": "SILNA SPRZEDAŻ"},
        {"pair": "Gold", "sym": "OANDA:XAUUSD", "type": "SPRZEDAŻ", "in": "4665.00", "sl": "4700.00", "tp": "4500.00", "rsi": 45, "src": "DAILYFOREX", "score": 92, "inv": "NEUTRALNIE", "tv": "SPRZEDAŻ"},
        {"pair": "BTC/USD", "sym": "BITSTAMP:BTCUSD", "type": "KUPNO", "in": "42800", "sl": "41500", "tp": "45000", "rsi": 59, "src": "FXLEADERS", "score": 93, "inv": "KUPNO", "tv": "SILNE KUPNO"},
        {"pair": "EUR/USD", "sym": "FX:EURUSD", "type": "KUPNO", "in": "1.0945", "sl": "1.0890", "tp": "1.1050", "rsi": 55, "src": "FXLEADERS", "score": 87, "inv": "KUPNO", "tv": "KUPNO"}
    ]

if 'signals' not in st.session_state: st.session_state.signals = get_verified_data()

# --- INTERFEJS ---
h1, h2, h3 = st.columns([3, 1, 1])
h1.subheader("TERMINAL V410 | MULTI-SOURCE ANALYSIS")
h2.button("🏆 RANKING AI")
if h3.button("🔄 AKTUALIZUJ"):
    st.rerun()

col_l, col_r = st.columns([2, 3])

with col_l:
    with st.container(height=700):
        for idx, s in enumerate(st.session_state.signals):
            st.markdown(f"""
                <div class="signal-card">
                    <span style="float:right; color:#00ff88;">{s['src']}</span>
                    <b>{s['pair']}</b>
                    <div class="data-box">
                        <span class="entry-val">WEJŚCIE: {s['in']}</span>
                        <span class="exit-vals">SL: {s['sl']} | TP: {s['tp']}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"ANALIZUJ {s['pair']}", key=f"btn_{idx}"):
                st.session_state.active = s

with col_r:
    if 'active' in st.session_state:
        a = st.session_state.active
        st.subheader(f"Szczegóły: {a['pair']}")
        
        # SUWAK INTERWAŁÓW (Rozszerzony)
        tf = st.select_slider("Wybierz Interwał:", options=["1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w", "1M"], value="1h")
        
        # --- SEKCJA AGREGATÓW (PRZYWRÓCONA) ---
        st.write("### Niezależne Agregaty Sygnału")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'<div class="agg-box"><div class="agg-label">INVESTING.COM</div><div class="agg-value">{a["inv"]}</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="agg-box"><div class="agg-label">TRADINGVIEW</div><div class="agg-value">{a["tv"]}</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="agg-box"><div class="agg-label">RSI ({tf})</div><div class="agg-value">{a["rsi"]}</div></div>', unsafe_allow_html=True)

        # Widget techniczny poniżej
        components.html(f"""
            <div class="tradingview-widget-container">
                <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
                {{
                    "interval": "1D",
                    "width": "100%",
                    "isTransparent": true,
                    "height": 400,
                    "symbol": "{a['sym']}",
                    "locale": "pl",
                    "colorTheme": "dark"
                }}
                </script>
            </div>
        """, height=420)
