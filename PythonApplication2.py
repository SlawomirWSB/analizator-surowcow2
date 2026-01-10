import streamlit as st

st.set_page_config(layout="wide", page_title="Sygnały 10 Stycznia")

st.markdown("""
    <style>
    .card { background-color: #1e222d; padding: 15px; border-radius: 10px; border-left: 5px solid #00ff88; margin-bottom: 10px; color: white; }
    .sell-card { border-left-color: #ff4b4b; }
    .label { font-weight: bold; color: #8f94a1; }
    </style>
    """, unsafe_allow_html=True)

st.title("📡 Aktywne Sygnały: 10 Stycznia 2026")

# Sygnał 1
st.markdown("""
<div class="card">
    <h3>🥇 ZŁOTO (GOLD) - VasilyTrader / ProSignals</h3>
    <p><span class="label">Kierunek:</span> 🟢 KUPNO (BUY)</p>
    <p><span class="label">Cena wejścia:</span> ok. 4509.00</p>
    <p><span class="label">Take Profit:</span> 4525.00</p>
    <p><span class="label">Stop Loss:</span> 4495.00</p>
    <p><i>Notatka: Silne wsparcie na poziomie 4500. Zegary TradingView potwierdzają kupno.</i></p>
</div>
""", unsafe_allow_html=True)

# Sygnał 2
st.markdown("""
<div class="card sell-card">
    <h3>📉 GBP/CHF - SignalProvider (Free Forecast)</h3>
    <p><span class="label">Kierunek:</span> 🔴 SPRZEDAŻ (SELL)</p>
    <p><span class="label">Cena wejścia:</span> 1.073</p>
    <p><span class="label">Cel (TP):</span> 1.071</p>
    <p><i>Notatka: Rynek testuje opór. Spodziewany spadek do poziomu 1.071.</i></p>
</div>
""", unsafe_allow_html=True)
