import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# 1. KONFIGURACJA WIZUALNA
st.set_page_config(layout="wide", page_title="TERMINAL V10.0 | FULL INTEGRATION")
st.markdown("""
<style>
    .stApp { background: #0e1117; color: #ffffff; }
    .stButton > button { width: 100%; height: 45px; font-weight: 900 !important; border-radius: 8px !important; }
    .btn-sources { background: linear-gradient(45deg, #2196F3, #21CBF3) !important; color: white !important; }
    .btn-ai { background: linear-gradient(45deg, #00ff88, #00cc6a) !important; color: black !important; }
    .signal-card { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 15px; margin-bottom: 12px; border-left: 5px solid #00ff88; }
    .agg-box { background: #1c2128; padding: 10px; border-radius: 8px; text-align: center; border: 1px solid #333; }
    .rsi-val { color: #00ff88; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# 2. POBIERANIE DANYCH ZE ŹRÓDEŁ (FILTR 72H)
def fetch_external_signals():
    now = datetime.now()
    # Symulacja danych z portali: BestFreeSignal, DailyForex, ForeSignal
    raw_data = [
        {"p": "EUR/USD", "type": "SPRZEDAŻ", "in": "1.15998", "tp": "1.15200", "sl": "1.16400", "date": "2026-01-17 22:00:00", "src": "BESTFREESIGNAL"},
        {"p": "GBP/USD", "type": "KUPNO", "in": "1.28450", "tp": "1.29100", "sl": "1.27900", "date": "2026-01-18 10:30:00", "src": "DAILYFOREX"},
        {"p": "NZD/USD", "type": "KUPNO", "in": "0.57480", "tp": "0.58200", "sl": "0.57100", "date": "2026-01-16 09:00:00", "src": "FORESIGNAL"}
    ]
    # Filtr 3 dni
    return [s for s in raw_data if (now - datetime.strptime(s['date'], "%Y-%m-%d %H:%M:%S")).days <= 3]

# 3. GENERATOR AI (MIN 3 KRYPTO W WEEKEND, ŁĄCZNIE 6)
def generate_ai_picks(is_weekend):
    picks = []
    assets = ["BTC/USD", "ETH/USD", "SOL/USD", "ADA/USD", "XRP/USD", "DOT/USD"] if is_weekend else ["GOLD", "US100", "DE30", "OIL.WTI", "EUR/USD", "USD/JPY"]
    
    for a in assets[:6]: # 6 pozycji AI
        score = random.randint(88, 99)
        picks.append({
            "p": a, "type": random.choice(["KUPNO", "SPRZEDAŻ"]), "in": "MARKET", "tp": "AUTO AI", "sl": "AUTO AI",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "src": "AI GENERATOR", "score": score, "rsi": random.randint(25, 75)
        })
    return picks

# 4. INTERFEJS
st.title("🚀 TERMINAL V10.0 | XTB AI & SOURCES")

# Przyciski sterujące
c1, c2, c3 = st.columns([2, 2, 2])
with c1:
    if st.button("🌐 AKTUALIZUJ ZE ŹRÓDEŁ", type="primary"):
        st.session_state.ext_data = fetch_external_signals()
with c2:
    if st.button("🤖 AKTUALIZUJ Z AI"):
        st.session_state.ai_data = generate_ai_picks(datetime.now().weekday() >= 5)

# Inicjalizacja sesji
if 'ext_data' not in st.session_state: st.session_state.ext_data = []
if 'ai_data' not in st.session_state: st.session_state.ai_data = []

col_l, col_r = st.columns([1, 1])

with col_l:
    st.subheader("📡 Wszystkie Sygnały (<72h)")
    combined = st.session_state.ai_data + st.session_state.ext_data
    for s in combined:
        color = "#00ff88" if s['type'] == "KUPNO" else "#ff4b4b"
        st.markdown(f"""
        <div class="signal-card" style="border-left-color: {color}">
            <div style="display: flex; justify-content: space-between;">
                <b>{s['p']}</b> <span style="color:#8b949e">{s['date']}</span>
            </div>
            <div style="font-size: 1.2rem; margin: 8px 0; color: {color}; font-weight: bold;">{s['type']} @ {s['in']}</div>
            <div style="font-size: 0.8rem; margin-bottom: 5px;">
                RSI: <span class="rsi-val">{s.get('rsi', 'N/A')}</span> | Źródło: {s['src']}
            </div>
            <div style="background:rgba(0,0,0,0.3); padding:5px; border-radius:4px; font-size:0.85rem;">TP: {s['tp']} | SL: {s['sl']}</div>
        </div>
        """, unsafe_allow_html=True)

with col_r:
    # Niezależne agregaty
    st.subheader("📊 Niezależne Agregaty")
    ac1, ac2 = st.columns(2)
    ac1.markdown('<div class="agg-box"><small>INVESTING</small><br><b>SILNE KUPNO</b></div>', unsafe_allow_html=True)
    ac2.markdown('<div class="agg-box"><small>TRADINGVIEW</small><br><b>NEUTRALNY</b></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    # Zintegrowany Ranking
    st.subheader("🏆 Ranking Szans (Sources + AI)")
    if combined:
        df = pd.DataFrame(combined).assign(score=lambda x: x['score'].fillna(random.randint(80, 90)))
        st.table(df.sort_values(by="score", ascending=False)[['p', 'score', 'type', 'src']])
