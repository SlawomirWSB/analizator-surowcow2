import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime, timedelta
import random

# 1. KONFIGURACJA
st.set_page_config(layout="wide", page_title="TERMINAL V5.5 FINAL", initial_sidebar_state="collapsed")
st.markdown("""
<style>
.stApp { background: #0e1117; color: #ffffff; }
div.stButton > button { 
    width: 100%; background: linear-gradient(45deg, #00ff88, #00cc6a); color: #000; 
    font-weight: bold; border-radius: 8px; border: none; height: 45px;
}
.signal-card { 
    background: #161b22; border: 1px solid #30363d; border-radius: 12px; 
    padding: 15px; margin-bottom: 10px; border-left: 5px solid #00ff88; 
}
.agg-box { background: #1c2128; padding: 10px; border-radius: 8px; text-align: center; border: 1px solid #30363d; }
</style>
""", unsafe_allow_html=True)

class SignalManager:
    @staticmethod
    def generate_signals():
        pairs = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", "Gold", "Crude Oil WTI", "EUR/GBP", "NZD/USD", "BTC/USD"]
        symbols = {"Gold": "OANDA:XAUUSD", "Crude Oil WTI": "TVC:USOIL", "BTC/USD": "BINANCE:BTCUSDT"}
        signals = []
        for p in pairs:
            sig_type = random.choice(["KUPNO", "SPRZEDAŻ"])
            # Używamy klucza 'in' zamiast 'price', aby uniknąć KeyError
            price = f"{random.uniform(1, 1.1):.4f}" if "/" in p else f"{random.randint(2500, 60000)}"
            signals.append({
                "pair": p,
                "sym": symbols.get(p, f"FX:{p.replace('/', '')}"),
                "type": sig_type,
                "in": price, 
                "score": random.randint(85, 99),
                "src": random.choice(["ECONOMIES", "INVESTING", "STPTRADING"]),
                "rsi_base": random.randint(30, 70),
                "inv": random.choice(["KUPNO", "SILNE KUPNO", "SPRZEDAŻ"]),
                "tv": random.choice(["NEUTRALNY", "KUPNO", "SILNE KUPNO"]),
                "date": datetime.now().strftime("%d.%m"),
                "hour": datetime.now().strftime("%H:%M")
            })
        return signals

# SESJA
if 'signals' not in st.session_state:
    st.session_state.signals = SignalManager.generate_signals()
if 'active_signal' not in st.session_state:
    st.session_state.active_signal = st.session_state.signals[0]
if 'view' not in st.session_state:
    st.session_state.view = "terminal"

# WIDOK RANKINGU (NAPRAWIONY HTML)
def render_ranking():
    st.title("🏆 RANKING AI - MULTI-INDYKATOROWY")
    if st.button("⬅️ POWRÓT DO TERMINALA"):
        st.session_state.view = "terminal"
        st.rerun()

    ranked = sorted(st.session_state.signals, key=lambda x: x['score'], reverse=True)
    
    # Budujemy tabelę jako jeden ciąg HTML, aby Streamlit ją wyrenderował poprawnie
    html_table = """
    <table style="width:100%; border-collapse: collapse; background: #161b22; border-radius: 10px; overflow: hidden;">
        <tr style="background: #21262d; color: #8b949e; text-align: left;">
            <th style="padding: 15px;">ASSET</th><th style="padding: 15px;">SCORE</th>
            <th style="padding: 15px;">TYP</th><th style="padding: 15px;">ŹRÓDŁO</th>
        </tr>
    """
    for sig in ranked:
        color = "#00ff88" if sig['type'] == "KUPNO" else "#ff4b4b"
        html_table += f"""
        <tr style="border-bottom: 1px solid #30363d;">
            <td style="padding: 12px; font-weight: bold;">{sig['pair']}</td>
            <td style="padding: 12px; color: #00ff88;">{sig['score']}%</td>
            <td style="padding: 12px; color: {color}; font-weight: bold;">{sig['type']}</td>
            <td style="padding: 12px; color: #8b949e;">{sig['src']}</td>
        </tr>
        """
    html_table += "</table>"
    st.markdown(html_table, unsafe_allow_html=True)

# WIDOK TERMINALA
if st.session_state.view == "terminal":
    st.title("🚀 TERMINAL V5.5")
    col_nav1, col_nav2 = st.columns([4, 1])
    with col_nav2:
        if st.button("🏆 RANKING AI"):
            st.session_state.view = "ranking"
            st.rerun()

    c1, c2 = st.columns([1, 2])
    with c1:
        for i, sig in enumerate(st.session_state.signals):
            color = "#00ff88" if sig['type'] == "KUPNO" else "#ff4b4b"
            st.markdown(f"""
            <div class="signal-card" style="border-left-color: {color}">
                <div style="display: flex; justify-content: space-between; font-size: 0.8rem;">
                    <b>{sig['pair']}</b><span>{sig['src']}</span>
                </div>
                <div style="font-size: 1.1rem; margin: 5px 0; color: {color};">
                    {sig['type']} @ {sig['in']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"ANALIZUJ {sig['pair']}", key=f"btn_{i}"):
                st.session_state.active_signal = sig
                st.rerun()

    with c2:
        curr = st.session_state.active_signal
        st.subheader(f"Analiza: {curr['pair']} ({curr['src']})")
        
        # Poprawiony slider (domknięte nawiasy)
        tf = st.select_slider("⏱️ Interwał", options=["1m", "5m", "15m", "1h", "1D"], value="1h")
        
        ac1, ac2, ac3 = st.columns(3)
        ac1.markdown(f'<div class="agg-box"><small>INVESTING</small><br><b style="color:#00ff88">{curr["inv"]}</b></div>', unsafe_allow_html=True)
        ac2.markdown(f'<div class="agg-box"><small>TRADINGVIEW</small><br><b style="color:#00ff88">{curr["tv"]}</b></div>', unsafe_allow_html=True)
        ac3.markdown(f'<div class="agg-box"><small>RSI</small><br><b>{curr["rsi_base"]}</b></div>', unsafe_allow_html=True)
        
        components.html(f"""
            <div style="background:#161b22; height:400px; border-radius:10px; border:1px solid #30363d; display:flex; align-items:center; justify-content:center; color:#555;">
                <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
                <script type="text/javascript">
                new TradingView.widget({{"width": "100%", "height": 400, "symbol": "{curr['sym']}", "interval": "H", "theme": "dark", "style": "1", "locale": "pl"}});
                </script>
            </div>
        """, height=420)
else:
    render_ranking()
