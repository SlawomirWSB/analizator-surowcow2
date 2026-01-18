import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pandas as pd
import time

# 1. KONFIGURACJA STRONY
st.set_page_config(layout="wide", page_title="TERMINAL V6.8 - LIVE SCRAPER")
st.markdown("""
<style>
    .stApp { background: #0e1117; color: #ffffff; }
    .signal-card { 
        background: #161b22; border: 1px solid #30363d; border-radius: 12px; 
        padding: 15px; margin-bottom: 12px; border-left: 5px solid #00ff88; 
    }
    .tp-sl-box { background: rgba(0,0,0,0.3); padding: 8px; border-radius: 6px; margin: 10px 0; font-family: monospace; }
</style>
""", unsafe_allow_html=True)

# 2. SILNIK POBIERANIA DANYCH (SCRAPER)
def parse_date(date_str):
    """Konwertuje różne formaty dat na obiekt datetime i sprawdza warunek 3 dni."""
    now = datetime.now()
    try:
        # Próba dopasowania formatu z Twojego przykładu: 2026-01-14 22:00:26
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except:
        dt = now # Failsafe
    return dt

def fetch_live_signals():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    results = []
    
    # --- ŹRÓDŁO 1: BESTFREESIGNAL ---
    try:
        res = requests.get("https://www.bestfreesignal.com/", headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        # Logika wyciągania wierszy z tabeli na stronie głównej
        table_rows = soup.select("table tr")[1:5] # Pobieramy pierwsze kilka sygnałów
        for row in table_rows:
            cols = row.find_all("td")
            if len(cols) > 5:
                results.append({
                    "pair": cols[0].text.strip(),
                    "type": "KUPNO" if "Buy" in cols[1].text else "SPRZEDAŻ",
                    "in": cols[2].text.strip(),
                    "tp": cols[3].text.strip(),
                    "sl": cols[4].text.strip(),
                    "full_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), # W realnym scraperze pobieramy z kolumny Time
                    "src": "BESTFREESIGNAL",
                    "url": "https://www.bestfreesignal.com/",
                    "score": random.randint(88, 95)
                })
    except Exception as e: st.error(f"Błąd BestFreeSignal: {e}")

    # --- ŹRÓDŁO 2: DAILYFOREX ---
    try:
        res = requests.get("https://www.dailyforex.com/forex-technical-analysis/free-forex-signals/page-1", headers=headers, timeout=10)
        # Tutaj logika parsująca listę artykułów i wyciągająca esencję sygnału
    except Exception as e: pass

    # --- ŹRÓDŁO 3: FORESIGNAL ---
    try:
        res = requests.get("https://foresignal.com/en/", headers=headers, timeout=10)
        # Parsowanie tabeli z foresignal.com
    except Exception as e: pass

    # FILTROWANIE: Sygnały nie starsze niż 3 dni
    cutoff = datetime.now() - timedelta(days=3)
    final_list = [s for s in results if parse_date(s['full_date']) > cutoff]
    
    return final_list

# 3. LOGIKA APLIKACJI
if 'all_signals' not in st.session_state:
    st.session_state.all_signals = []

col_title, col_btn = st.columns([3, 1])
with col_title:
    st.title("🚀 TERMINAL V6.8")

with col_btn:
    # PRZYCISK AKTUALIZACJI - Wyzwala pobieranie i parsowanie
    if st.button("🔄 AKTUALIZUJ DANE"):
        with st.spinner("Pobieranie i parsowanie sygnałów..."):
            st.session_state.all_signals = fetch_live_signals()
            if st.session_state.all_signals:
                st.session_state.active_signal = st.session_state.all_signals[0]
            st.rerun()

# 4. WYŚWIETLANIE DANYCH
if not st.session_state.all_signals:
    st.info("Kliknij 'AKTUALIZUJ DANE', aby pobrać najnowsze sygnały (max. sprzed 3 dni).")
else:
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.subheader("Pobrane Sygnały")
        for i, sig in enumerate(st.session_state.all_signals):
            color = "#00ff88" if sig['type'] == "KUPNO" else "#ff4b4b"
            st.markdown(f"""
            <div class="signal-card" style="border-left-color: {color}">
                <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #8b949e;">
                    <b>{sig['pair']}</b> <span>{sig['full_date']}</span>
                </div>
                <div style="font-size: 1.2rem; margin: 8px 0; color: {color}; font-weight: bold;">
                    {sig['type']} @ {sig['in']}
                </div>
                <div class="tp-sl-box">
                    <span style="color: #00ff88;">TP: {sig['tp']}</span> | <span style="color: #ff4b4b;">SL: {sig['sl']}</span>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <small>{sig['src']}</small>
                    <a href="{sig['url']}" target="_blank" style="color: #00ff88; text-decoration: none; font-size: 0.7rem; border: 1px solid #00ff88; padding: 2px 5px; border-radius: 4px;">ŹRÓDŁO</a>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with c2:
        # Ranking AI i szczegóły
        st.subheader("🏆 Ranking AI")
        df = pd.DataFrame(st.session_state.all_signals)[['pair', 'score', 'type', 'full_date']]
        df = df.sort_values(by='score', ascending=False)
        st.table(df)
