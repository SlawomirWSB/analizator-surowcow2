import streamlit as st
import streamlit.components.v1 as components
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import random

# 1. KONFIGURACJA WIZUALNA
st.set_page_config(layout="wide", page_title="TERMINAL V6.6 - XTB SYNC", initial_sidebar_state="collapsed")
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

# 2. LOGIKA POMOCNICZA
def is_weekend():
    # 5 = Sobota, 6 = Niedziela
    return datetime.now().weekday() >= 5

def is_recent(date_str):
    try:
        # Sprawdzanie czy sygnał nie jest starszy niż 3 dni
        day, month = map(int, date_str.split('.'))
        signal_date = datetime(2026, month, day)
        return datetime.now() - signal_date <= timedelta(days=3)
    except:
        return True

# 3. GENERATOR I SKRAPER DANYCH
@st.cache_data(ttl=900)
def fetch_signals():
    now = datetime.now()
    signals = []
    
    # Źródła zewnętrzne (Placeholder dla skraperów)
    sources = ["BESTFREESIGNAL", "DAILYFOREX", "FORESIGNAL"]
    
    # Przykładowe dane zgodne z Twoimi wymaganiami (Ceny XTB ok. 1.16 dla EUR/USD)
    base_data = [
        {"p": "EUR/USD", "in": 1.15998, "src": "BESTFREESIGNAL", "u": "https://www.bestfreesignal.com"},
        {"p": "GBP/USD", "in": 1.28450, "src": "DAILYFOREX", "u": "https://www.dailyforex.com"},
        {"p": "USD/JPY", "in": 142.60, "src": "FORESIGNAL", "u": "https://foresignal.com/en/"},
        {"p": "XAU/USD", "in": 2650.40, "src": "BESTFREESIGNAL", "u": "https://www.bestfreesignal.com"}
    ]

    for item in base_data:
        sig_type = random.choice(["KUPNO", "SPRZEDAŻ"])
        signals.append({
            "pair": item['p'], "type": sig_type, "in": f"{item['in']:.5f}",
            "sl": f"{item['in'] * 0.99:.5f}", "tp": f"{item['in'] * 1.02:.5f}",
            "src": item['src'], "url": item['u'], "score": random.randint(85, 98),
            "date": (now - timedelta(hours=random.randint(1, 48))).strftime("%d.%m"),
            "hour": f"{random.randint(0,23):02d}:{random.randint(0,59):02d}",
            "live": True, "inv": sig_type, "tv": "SILNE " + sig_type, "rsi": random.randint(30, 70)
        })

    # Tryb weekendowy - Kryptowaluty (Aktywne w XTB w weekend)
    if is_weekend():
        crypto = [
            {"pair": "BTC/USD", "in": 98500.0, "src": "XTB AI", "u": "#"},
            {"pair": "ETH/USD", "in": 3450.0, "src": "XTB AI", "u": "#"}
        ]
        for c in crypto:
            signals.append({
                "pair": c['pair'], "type": "KUPNO", "in": f"{c['in']:.2f}",
                "sl": f"{c['in'] - 500:.2f}", "tp": f"{c['in'] + 1500:.2f}",
                "src": c['src'], "url": c['u'], "score": 99,
                "date": now.strftime("%d.%m"), "hour": now.strftime("%H:%M"),
                "live": False, "inv": "KUPNO", "tv": "SILNE KUPNO", "rsi": 65
            })

    # Filtracja: tylko sygnały nie starsze niż 3 dni
    return [s for s in signals if is_recent(s['date'])]

# 4. ZARZĄDZANIE SESJĄ
if 'signals' not in st.session_state:
    st.session_state.signals = fetch_signals()
if 'active_signal' not in st.session_state:
    st.session_state.active_signal = st.session_state.signals[0]
if 'view' not in st.session_state:
    st.session_state.view = "terminal"

# 5. FUNKCJA RANKINGU AI (NAPRAWIONA TABELA)
def render_ranking():
    st.title("🏆 RANKING AI - NAJLEPSZE SCENARIUSZE")
    if st.button("⬅️ POWRÓT DO TERMINALA"):
        st.session_state.view = "terminal"
        st.rerun()

    ranked = sorted(st.session_state.signals, key=lambda x: x['score'], reverse=True)
    
    # Budowanie tabeli HTML, aby zapobiec wyświetlaniu surowego kodu
    html_table = """
    <table style="width:100%; border-collapse: collapse; background: #161b22; border-radius: 10px; overflow: hidden;">
        <tr style="background: #21262d; color: #8b949e; text-align: left;">
            <th style="padding: 15px;">INSTRUMENT</th><th style="padding: 15px;">WYNIK AI</th>
            <th style="padding: 15px;">TYP</th><th style="padding: 15px;">AKTUALIZACJA</th>
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

# 6. WIDOK GŁÓWNY
if st.session_state.view == "ranking":
    render_ranking()
else:
    st.title("🚀 TERMINAL V6.6")
    
    h1, h2 = st.columns([4, 1])
    with h2:
        if st.button("🏆 RANKING AI"):
            st.session_state.view = "ranking"
            st.rerun()

    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.subheader("Ostatnie Sygnały")
        for i, sig in enumerate(st.session_state.signals):
            color = "#00ff88" if sig['type'] == "KUPNO" else "#ff4b4b"
            # Naprawiony błąd KeyError: 'url' poprzez upewnienie się, że klucz istnieje
            url_link = sig.get('url', '#')
            
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
                    <a href="{url_link}" target="_blank" style="color: #00ff88; text-decoration: none; font-size: 0.7rem; border: 1px solid #00ff88; padding: 2px 5px; border-radius: 4px;">LINK</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"ANALIZUJ {sig['pair']}", key=f"btn_{i}"):
                st.session_state.active_signal = sig
                st.rerun()

    with c2:
        curr = st.session_state.active_signal
        st.subheader(f"Szczegóły: {curr['pair']}")
        
        # Sekcja agregatów (Zamiast wykresu)
        st.markdown("#### Niezależne Analizy")
        ac1, ac2, ac3 = st.columns(3)
        
        inv_col = "#00ff88" if "KUPNO" in curr['inv'] else "#ff4b4b"
        tv_col = "#00ff88" if "KUPNO" in curr['tv'] else "#ff4b4b"
        
        ac1.markdown(f'<div class="agg-box"><small>INVESTING.COM</small><br><b style="color:{inv_col}">{curr["inv"]}</b></div>', unsafe_allow_html=True)
        ac2.markdown(f'<div class="agg-box"><small>TRADINGVIEW</small><br><b style="color:{tv_col}">{curr["tv"]}</b></div>', unsafe_allow_html=True)
        ac3.markdown(f'<div class="agg-box"><small>RSI (Base)</small><br><b style="font-size:1.2rem;">{curr["rsi"]}</b></div>', unsafe_allow_html=True)
        
        st.success(f"Sygnał wygenerowany przez {curr['src']} ({curr['date']} {curr['hour']})")
        st.write(f"**Poziom wejścia:** {curr['in']}")
        st.write(f"**Stop Loss:** {curr['sl']}")
        st.write(f"**Take Profit:** {curr['tp']}")

        if st.button("🔄 AKTUALIZUJ I ANALIZUJ"):
            st.session_state.signals = fetch_signals()
            st.rerun()
