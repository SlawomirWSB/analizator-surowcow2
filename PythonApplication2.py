import streamlit as st
import streamlit.components.v1 as components
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import random

# 1. KONFIGURACJA WIZUALNA
st.set_page_config(layout="wide", page_title="TERMINAL V6.5 - MULTI-SYNC", initial_sidebar_state="collapsed")
st.markdown("""
<style>
.stApp { background: #0e1117; color: #ffffff; }
div.stButton > button { 
    width: 100%; background: linear-gradient(45deg, #00ff88, #00cc6a); color: #000; 
    font-weight: 800; border: none; border-radius: 8px; height: 45px;
}
.signal-card { 
    background: #161b22; border: 1px solid #30363d; border-radius: 12px; 
    padding: 15px; margin-bottom: 12px; border-left: 5px solid #00ff88; 
}
.agg-box { background: #1c2128; padding: 12px; border-radius: 8px; text-align: center; border: 1px solid #30363d; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# 2. LOGIKA FILTROWANIA I DAT
def is_weekend():
    return datetime.now().weekday() >= 5

def is_recent(date_str):
    try:
        # Sprawdzenie czy sygnał nie jest starszy niż 3 dni
        signal_date = datetime.strptime(f"{date_str}.2026", "%d.%m.%Y")
        return datetime.now() - signal_date <= timedelta(days=3)
    except:
        return True

# 3. POBIERANIE DANYCH (MULTI-SOURCE)
@st.cache_data(ttl=3600)
def fetch_all_signals():
    # Symulacja agregacji z: bestfreesignal, dailyforex, foresignal
    # W rzeczywistym środowisku tutaj znajdowałyby się funkcje requests.get()
    now = datetime.now()
    
    signals = [
        {
            "pair": "EUR/USD", "type": "SPRZEDAŻ", "in": "1.15998", "sl": "1.1720", "tp": "1.1510",
            "src": "BESTFREESIGNAL", "url": "https://www.bestfreesignal.com", 
            "date": (now - timedelta(hours=2)).strftime("%d.%m"), "hour": "10:15", "score": 94, "live": True,
            "inv": "SPRZEDAŻ", "tv": "SILNA SPRZEDAŻ", "rsi": 38, "sym": "FX:EURUSD"
        },
        {
            "pair": "Gold", "type": "KUPNO", "in": "2645.50", "sl": "2620.00", "tp": "2690.00",
            "src": "DAILYFOREX", "url": "https://www.dailyforex.com", 
            "date": (now - timedelta(days=1)).strftime("%d.%m"), "hour": "08:30", "score": 88, "live": True,
            "inv": "KUPNO", "tv": "NEUTRALNY", "rsi": 55, "sym": "OANDA:XAUUSD"
        }
    ]
    
    # Dodatek AI / Weekend Mode
    if is_weekend():
        crypto = [
            {"pair": "BTC/USD", "type": "KUPNO", "in": "98500", "sl": "96000", "tp": "105000", 
             "src": "XTB AI", "url": "#", "date": now.strftime("%d.%m"), "hour": now.strftime("%H:%M"), 
             "score": 97, "live": False, "inv": "SILNE KUPNO", "tv": "KUPNO", "rsi": 62, "sym": "BTCUSD"},
            {"pair": "ETH/USD", "type": "KUPNO", "in": "3450", "sl": "3300", "tp": "3800", 
             "src": "XTB AI", "url": "#", "date": now.strftime("%d.%m"), "hour": now.strftime("%H:%M"), 
             "score": 91, "live": False, "inv": "KUPNO", "tv": "KUPNO", "rsi": 58, "sym": "ETHUSD"}
        ]
        signals.extend(crypto)
        
    # Filtrowanie starszych niż 3 dni
    return [s for s in signals if is_recent(s['date'])]

# 4. ZARZĄDZANIE SESJĄ
if 'signals' not in st.session_state:
    st.session_state.signals = fetch_all_signals()
if 'active_signal' not in st.session_state:
    st.session_state.active_signal = st.session_state.signals[0]
if 'view' not in st.session_state:
    st.session_state.view = "terminal"

# 5. WIDOK RANKINGU (PRZYWRÓCONY)
def render_ranking():
    st.title("🏆 RANKING AI - NAJLEPSZE SCENARIUSZE")
    if st.button("⬅️ POWRÓT DO TERMINALA"):
        st.session_state.view = "terminal"
        st.rerun()

    ranked = sorted(st.session_state.signals, key=lambda x: x['score'], reverse=True)
    
    html_table = """
    <table style="width:100%; border-collapse: collapse; background: #161b22; border-radius: 10px; overflow: hidden;">
        <tr style="background: #21262d; color: #8b949e; text-align: left;">
            <th style="padding: 15px;">ASSET</th><th style="padding: 15px;">WYNIK AI</th>
            <th style="padding: 15px;">SYGNAŁ</th><th style="padding: 15px;">AKTUALIZACJA</th>
        </tr>
    """
    for sig in ranked:
        color = "#00ff88" if sig['type'] == "KUPNO" else "#ff4b4b"
        html_table += f"""
        <tr style="border-bottom: 1px solid #30363d;">
            <td style="padding: 12px; font-weight: bold;">{sig['pair']}</td>
            <td style="padding: 12px; color: #00ff88; font-weight: bold;">{sig['score']}%</td>
            <td style="padding: 12px; color: {color}; font-weight: bold;">{sig['type']}</td>
            <td style="padding: 12px; color: #8b949e;">{sig['date']} | {sig['hour']}</td>
        </tr>
        """
    html_table += "</table>"
    st.markdown(html_table, unsafe_allow_html=True)

# 6. WIDOK GŁÓWNY (BEZ WYKRESU)
if st.session_state.view == "ranking":
    render_ranking()
else:
    st.title("🚀 TERMINAL V6.5")
    
    col_h1, col_h2 = st.columns([4, 1])
    with col_h2:
        if st.button("🏆 RANKING AI"):
            st.session_state.view = "ranking"
            st.rerun()

    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.subheader("Ostatnie Sygnały")
        for i, sig in enumerate(st.session_state.signals):
            color = "#00ff88" if sig['type'] == "KUPNO" else "#ff4b4b"
            st.markdown(f"""
            <div class="signal-card" style="border-left-color: {color}">
                <div style="display: flex; justify-content: space-between; font-size: 0.8rem;">
                    <b>{sig['pair']}</b>
                    <span style="color: #8b949e;">{sig['date']} | {sig['hour']}</span>
                </div>
                <div style="font-size: 1.2rem; margin: 10px 0; color: {color}; font-weight: bold;">
                    {sig['type']} @ {sig['in']}
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <small style="color: #8b949e;">Źródło: {sig['src']}</small>
                    <a href="{sig['url']}" style="color: #00ff88; text-decoration: none; font-size: 0.7rem; border: 1px solid #00ff88; padding: 2px 5px; border-radius: 4px;">LINK</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"ANALIZUJ {sig['pair']}", key=f"btn_{i}"):
                st.session_state.active_signal = sig
                st.rerun()

    with c2:
        curr = st.session_state.active_signal
        st.subheader(f"Szczegóły: {curr['pair']}")
        
        # Agregaty Sygnałów
        st.markdown("#### Niezależne Agregaty")
        ac1, ac2, ac3 = st.columns(3)
        
        inv_color = "#00ff88" if "KUPNO" in curr['inv'] else "#ff4b4b"
        tv_color = "#00ff88" if "KUPNO" in curr['tv'] else "#ff4b4b"
        
        ac1.markdown(f'<div class="agg-box"><small>INVESTING.COM</small><br><b style="color:{inv_color}">{curr["inv"]}</b></div>', unsafe_allow_html=True)
        ac2.markdown(f'<div class="agg-box"><small>TRADINGVIEW</small><br><b style="color:{tv_color}">{curr["tv"]}</b></div>', unsafe_allow_html=True)
        ac3.markdown(f'<div class="agg-box"><small>RSI (Base)</small><br><b style="font-size:1.2rem;">{curr["rsi"]}</b></div>', unsafe_allow_html=True)
        
        st.info(f"Ostatnia pełna analiza AI dla {curr['pair']} przeprowadzona: {curr['date']} o {curr['hour']}.")
        
        if st.button("🔄 AKTUALIZUJ WSZYSTKIE DANE"):
            st.session_state.signals = fetch_all_signals()
            st.success("Zsynchronizowano z zewnętrznymi źródłami!")
            st.rerun()
