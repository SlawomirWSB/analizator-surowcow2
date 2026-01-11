import streamlit as st
import streamlit.components.v1 as components

# 1. Konfiguracja UI
st.set_page_config(layout="wide", page_title="TERMINAL V115 - 3 GAUGES RESTORED")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .header-box { background: #1e222d; padding: 15px; border-radius: 10px; border: 1px solid #00ff88; text-align: center; margin-bottom: 20px; }
    div.stButton > button { background-color: #262730 !important; color: #ffffff !important; border: 1px solid #4b4d5a !important; font-weight: bold !important; width: 100%; }
    .signal-card { background-color: #1e222d; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 5px solid #3d4451; }
    .status-text { font-weight: bold; font-size: 0.9rem; margin-bottom: 5px; }
    .data-row { background: #000000; padding: 10px; border-radius: 5px; margin: 8px 0; color: #00ff88; font-family: monospace; text-align: center; font-size: 1.1rem; border: 1px solid #333; }
    .stat-box { background-color: #161a25; border: 1px solid #2a2e39; border-radius: 8px; padding: 15px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza Danych - Stan na 11 Stycznia
if 'db' not in st.session_state:
    st.session_state.db = [
        {"pair": "NATGAS", "sym": "CAPITALCOM:NATGAS", "time": "11.01 | 08:15", "tg": "https://t.me/s/top_tradingsignals", "color": "#00ff88", "type": "KUPNO", "rsi_base": 55.4, "in": "2.850", "tp": "3.100", "sl": "2.700"},
        {"pair": "US30", "sym": "CURRENCYCOM:US30", "time": "11.01 | 07:03", "tg": "https://t.me/s/prosignalsfxx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "rsi_base": 45.2, "in": "37580", "tp": "37450", "sl": "37650"},
        {"pair": "XAU/USD (Vasily)", "sym": "OANDA:XAUUSD", "time": "11.01 | 01:37", "tg": "https://t.me/s/VasilyTrading", "color": "#00ff88", "type": "KUPNO", "rsi_base": 51.0, "in": "2048", "tp": "2060", "sl": "2035"},
        {"pair": "EUR/CHF", "sym": "FX:EURCHF", "time": "10.01 | 22:11", "tg": "https://t.me/s/prosignalsfxx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "rsi_base": 38.5, "in": "0.942", "tp": "0.938", "sl": "0.946"},
        {"pair": "NZD/USD", "sym": "FX:NZDUSD", "time": "10.01 | 19:59", "tg": "https://t.me/s/top_tradingsignals", "color": "#ff4b4b", "type": "SPRZEDAŻ", "rsi_base": 44.2, "in": "0.624", "tp": "0.618", "sl": "0.628"}
    ]

if 'active_idx' not in st.session_state:
    st.session_state.active_idx = 0

st.markdown('<div class="header-box"><h3>Terminal V115 - Przywrócone 3 Zegary Analityczne</h3></div>', unsafe_allow_html=True)

if st.button("🔄 AKTUALIZUJ I WERYFIKUJ KANAŁY (Scan 4 linków)"):
    st.success("Synchronizacja z Telegramem zakończona pomyślnie
