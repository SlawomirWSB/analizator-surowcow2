import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime, timedelta
import random
import numpy as np

# 1. KONFIGURACJA WIZUALNA
st.set_page_config(layout="wide", page_title="TERMINAL V5.5", initial_sidebar_state="collapsed")
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

# 2. MANAGER SYGNAŁÓW
class SignalManager:
    @staticmethod
    def generate_signals():
        pairs = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD", "Gold", "Crude Oil WTI", "EUR/GBP", "NZD/USD", "BTC/USD"]
        signals = []
        for p in pairs:
            sig_type = random.choice(["KUPNO", "SPRZEDAŻ"])
            signals.append({
                "pair": p,
                "sym": "FX:EURUSD" if "/" in p else "OANDA:XAUUSD",
                "type": sig_type,
                "price": f"{random.uniform(1, 1.5):.4f}" if "/" in p else f"{random.randint(2000, 2700)}",
                "score": random.randint(85, 99),
                "src": random.choice(["ECONOMIES", "INVESTING", "STPTRADING"]),
                "rsi_base": random.randint(30, 70),
                "inv": random.choice(["KUPNO", "SILNE KUPNO", "SPRZEDAŻ"]),
                "tv": random.choice(["NEUTRALNY", "KUPNO", "SILNE KUPNO"])
            })
        return signals

# 3. ZARZĄDZANIE SESJĄ
if 'signals' not in st.session_state:
    st.session_state.signals = SignalManager.generate_signals()
if 'active_signal' not in st.session_state:
    st.session_state.active_signal = st.session_state.signals[0]
if 'view' not in st.session_state:
    st.session_state.view = "terminal"

# 4. FUNKCJA RANKINGU (NAPRAWIONA)
def render_ranking():
    st.title("🏆 RANKING AI - ANALIZA MULTI")
    if st.button("⬅️ POWRÓT DO TERMINALA"):
        st.session_state.view = "terminal"
        st.rerun()

    # Sortowanie po score
    ranked = sorted(st.session_state.signals, key=lambda x: x['score'], reverse=True)

    # Budowanie tabeli HTML (Kluczowe: dodanie <table> i </table>)
    html_code = """
    <table style="width:100%; border-collapse: collapse; background: #161b22; border-radius: 10px; overflow: hidden;">
        <thead style="background: #21262d;">
            <tr>
                <th style="padding: 15px; text-align: left;">INSTRUMENT</th>
                <th style="padding: 15px; text-align: center;">WYNIK AI</th>
                <th style="padding: 15px; text-align: center;">SYGNAŁ</th>
                <th style="padding: 15px; text-align: right;">ŹRÓDŁO</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for sig in ranked:
        color = "#00ff88" if sig['type'] == "KUPNO" else "#ff4b4b"
        html_code += f"""
        <tr style="border-bottom: 1px solid #30363d;">
            <td style="padding: 12px; font-weight: bold;">{sig['pair']}</td>
            <td style="padding: 12px; text-align: center; color: #00ff88;">{sig['score']}%</td>
            <td style="padding: 12px; text-align: center; color: {color}; font-weight: bold;">{sig['type']}</td>
            <td style="padding: 12px; text-align: right; color: #8b949e; font-size: 0.8rem;">{sig['src']}</td>
        </tr>
        """
    
    html_code += "</tbody></table>"
    
    # Renderowanie jako jeden blok HTML
    st.markdown(html_code, unsafe_allow_html=True)

# 5. WIDOK GŁÓWNY
if st.session_state.view == "ranking":
    render_ranking()
else:
    st.title("🚀 TERMINAL V5.5")
    
    col_nav1, col_nav2 = st.columns([4, 1])
    with col_nav2:
        if st.button("🏆 RANKING AI"):
            st.session_state.view = "ranking"
            st.rerun()

    c1, c2 = st.columns([1, 2])
    
    with c1:
        st.subheader("Sygnały Live")
        for i, sig in enumerate(st.session_state.signals):
            color = "#00ff88" if sig['type'] == "KUPNO" else "#ff4b4b"
            st.markdown(f"""
            <div class="signal-card" style="border-left-color: {color}">
                <div style="display: flex; justify-content: space-between;">
                    <b>{sig['pair']}</b>
                    <span style="color: #8b949e; font-size: 0.7rem;">{sig['src']}</span>
                </div>
                <div style="font-size: 1.2rem; margin: 10px 0; color: {color};">{sig['type']} @ {sig['price']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"ANALIZUJ {sig['pair']}", key=f"btn_{i}"):
                st.session_state.active_signal = sig
                st.rerun()

    with c2:
        curr = st.session_state.active_signal
        st.subheader(f"Analiza: {curr['pair']}")
        
        # NAPRAWIONY SLIDER (Błąd ze screena 5)
        tf = st.select_slider(
            "⏱️ Interwał RSI", 
            options=["1m", "5m", "15m", "30m", "1h", "4h", "1D", "1W"], 
            value="1h"
        )
        
        # Agregaty
        ac1, ac2, ac3 = st.columns(3)
        ac1.markdown(f'<div class="agg-box"><small>INVESTING</small><br><b style="color:#00ff88">{curr["inv"]}</b></div>', unsafe_allow_html=True)
        ac2.markdown(f'<div class="agg-box"><small>TRADINGVIEW</small><br><b style="color:#00ff88">{curr["tv"]}</b></div>', unsafe_allow_html=True)
        ac3.markdown(f'<div class="agg-box"><small>RSI ({tf})</small><br><b>{curr["rsi_base"]}</b></div>', unsafe_allow_html=True)
        
        # Widget TradingView (Placeholder)
        st.info(f"Ładowanie wykresu TradingView dla {curr['pair']} na interwale {tf}...")
        components.html(f"""
            <div style="height:400px; background:#161b22; border: 1px solid #30363d; display:flex; align-items:center; justify-content:center; color:#555;">
                WIDGET TRADINGVIEW [{curr['pair']}]
            </div>
        """, height=400)
