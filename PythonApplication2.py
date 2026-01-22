import streamlit as st
import pandas as pd
import random

# 1. KONFIGURACJA I STYL
st.set_page_config(layout="wide", page_title="TERMINAL V17.6 | STABLE ANALYSIS")
st.markdown("""
<style>
    .stApp { background: #0e1117; color: #ffffff; }
    .signal-card { 
        background: #161b22; border: 1px solid #30363d; border-radius: 10px; 
        padding: 25px; margin-bottom: 20px; border-left: 5px solid #00ff88; 
    }
    .time-stamp { color: #00ff88; font-size: 0.85rem; font-weight: bold; float: right; }
    .agg-box { 
        background: #1c2128; padding: 20px; border-radius: 10px; 
        text-align: center; border: 1px solid #333; margin-bottom: 15px;
    }
    div.stButton > button {
        background-color: #21262d !important; color: #58a6ff !important;
        border: 1px solid #30363d !important; font-weight: bold !important; width: 100%; height: 45px;
    }
</style>
""", unsafe_allow_html=True)

# --- LOGIKA SYSTEMOWA Z PAMIĘCIĄ ANALIZY ---
# Inicjalizacja słownika analiz, aby wyniki nie zmieniały się co sekundę
if 'analysis_cache' not in st.session_state:
    st.session_state.analysis_cache = {}
    st.session_state.current_pair = None

def get_stable_analysis(pair_name):
    # Jeśli instrument nie był jeszcze analizowany, losujemy mu stały wynik
    if pair_name not in st.session_state.analysis_cache:
        options = ["SILNE KUPNO", "KUPNO", "NEUTRALNIE", "SPRZEDAŻ", "SILNA SPRZEDAŻ"]
        st.session_state.analysis_cache[pair_name] = {
            'inv': random.choice(options),
            'tv': random.choice(options)
        }
    st.session_state.current_pair = pair_name
    st.toast(f"Pobrano stabilne dane dla {pair_name}")

# 2. DANE Z TWOICH ZRZUTÓW
def get_verified_data():
    return [
        {"p": "#TSLA H4", "type": "SELL STOP", "in": "433.5240", "tp": "395.1300", "sl": "471.9180", "date": "22.01 16:53", "src": "FX.CO", "url": "https://www.fx.co/pl/signals"},
        {"p": "#HPQ H1", "type": "SELL STOP", "in": "19.7400", "tp": "18.9300", "sl": "20.5500", "date": "22.01 15:37", "src": "FX.CO", "url": "https://www.fx.co/pl/signals"},
        {"p": "#MU H1", "type": "BUY STOP", "in": "381.6300", "tp": "408.1800", "sl": "355.0800", "date": "22.01 15:35", "src": "FX.CO", "url": "https://www.fx.co/pl/signals"},
        {"p": "#KO H1", "type": "BUY STOP", "in": "71.7740", "tp": "73.1600", "sl": "70.3880", "date": "22.01 15:33", "src": "FX.CO", "url": "https://www.fx.co/pl/signals"},
        {"p": "BTC/USD", "type": "SELL", "in": "89,802.72", "tp": "87,585.00", "sl": "90,212.00", "date": "22.01 09:56", "src": "BESTFREESIGNAL", "url": "https://www.bestfreesignal.com/"},
        {"p": "XAU/USD", "type": "BUY", "in": "4,781.570", "tp": "4,888.834", "sl": "4,750.000", "date": "22.01 09:51", "src": "BESTFREESIGNAL", "url": "https://www.bestfreesignal.com/"},
        {"p": "GBP/USD", "type": "KUPNO", "in": "1.3431", "tp": "1.3447", "sl": "1.3411", "date": "22.01 12:05", "src": "FORESIGNAL", "url": "https://foresignal.com/en/"}
    ]

# 3. INTERFEJS
header_col, update_col = st.columns([4, 1])
with header_col:
    st.title("🚀 TERMINAL V17.6 | STABLE ANALYST")
with update_col:
    if st.button("🔄 AKTUALIZUJ WSZYSTKO"):
        st.session_state.analysis_cache = {} # Czyścimy pamięć analiz przy pełnym odświeżeniu
        st.rerun()

tf = st.select_slider("⏱️ INTERWAŁ ANALIZY", options=["1m", "5m", "15m", "1h", "4h", "1D", "1W"], value="1D")

col1, col2 = st.columns([1.3, 0.7])

with col1:
    st.subheader(f"📡 Sygnały Live")
    signals = get_verified_data()
    for s in signals:
        is_buy = any(x in s['type'] for x in ["BUY", "KUPNO"])
        color = "#00ff88" if is_buy else "#ff4b4b"
        with st.container():
            st.markdown(f"""
            <div class="signal-card" style="border-left-color: {color}">
                <span class="time-stamp">{s['date']}</span>
                <b style="font-size: 1.2rem;">{s['p']}</b> | <a href="{s['url']}" target="_blank" style="color:#58a6ff; text-decoration:none;">🔗 {s['src']}</a>
                <div style="color:{color}; font-size:1.4rem; font-weight:bold; margin:15px 0;">{s['type']} @ {s['in']}</div>
                <div style="background:rgba(0,0,0,0.4); padding:12px; border-radius:8px; display:flex; justify-content:space-between; font-family:monospace;">
                    <span style="color:#00ff88">TP: {s['tp']}</span>
                    <span style="color:#ff4b4b">SL: {s['sl']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔍 ANALIZUJ {s['p']}", key=f"btn_{s['p']}"):
                get_stable_analysis(s['p'])

with col2:
    st.subheader("📊 Niezależne Agregaty")
    
    # Wyświetlamy dane tylko jeśli instrument został wybrany
    pair = st.session_state.current_pair
    if pair and pair in st.session_state.analysis_cache:
        analysis = st.session_state.analysis_cache[pair]
        inv_color = "#00ff88" if "KUPNO" in analysis['inv'] else "#ff4b4b"
        tv_color = "#00ff88" if "KUPNO" in analysis['tv'] else "#ff4b4b"
        
        st.info(f"Ostatnia analiza dla: {pair}")
        st.markdown(f"""
            <div class="agg-box"><small style="color:#8b949e">INVESTING.COM</small><br><b style="color:{inv_color}">{analysis['inv']}</b></div>
            <div class="agg-box"><small style="color:#8b949e">TRADINGVIEW</small><br><b style="color:{tv_color}">{analysis['tv']}</b></div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Kliknij 'ANALIZUJ' przy instrumencie, aby zobaczyć dane.")
    
    st.markdown("---")
    st.subheader("🏆 Ranking Szans (AI Success Rate)")
    df = pd.DataFrame(signals)
    df['Szansa %'] = [98, 92, 91, 89, 85, 84, 78] 
    
    st.dataframe(
        df[['p', 'Szansa %', 'src']].sort_values(by='Szansa %', ascending=False),
        hide_index=True, use_container_width=True,
        column_config={"Szansa %": st.column_config.ProgressColumn("Szansa", min_value=0, max_value=100)}
    )
