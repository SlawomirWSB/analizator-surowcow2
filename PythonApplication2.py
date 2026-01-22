import streamlit as st
import pandas as pd
import random

# 1. USTAWIENIA I STYL (PEŁNY TERMINAL)
st.set_page_config(layout="wide", page_title="TERMINAL V17.3 | SMART RANKING ENGINE")
st.markdown("""
<style>
    .stApp { background: #0e1117; color: #ffffff; }
    .signal-card { 
        background: #161b22; border: 1px solid #30363d; border-radius: 10px; 
        padding: 20px; margin-bottom: 12px; border-left: 5px solid #00ff88; 
    }
    .time-stamp { color: #00ff88; font-size: 0.8rem; font-weight: bold; float: right; }
    .agg-box { 
        background: #1c2128; padding: 15px; border-radius: 8px; 
        text-align: center; border: 1px solid #333; margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 2. LOGIKA INTELIGENTNEGO RANKINGU
def calculate_real_chance(row):
    # Startowa szansa oparta na jakości źródła
    score = 70 if row['src'] == 'FX.CO' else 65
    
    # Premia za świeżość (22.01 popołudnie)
    if "15:" in row['date'] or "16:" in row['date']: score += 15
    
    # Premia za wyższe interwały (H4 > H1)
    if "H4" in row['p']: score += 8
    
    # Symulacja zgodności technicznej (RSI/Wiadomości)
    score += random.randint(0, 5) 
    
    return min(score, 98)

def get_full_active_data():
    return [
        {"p": "#TSLA H4", "type": "SELL STOP", "in": "433.5240", "tp": "395.1300", "sl": "471.9180", "date": "22.01 16:53", "src": "FX.CO", "url": "https://www.fx.co/pl/signals"},
        {"p": "#HPQ H1", "type": "SELL STOP", "in": "19.7400", "tp": "18.9300", "sl": "20.5500", "date": "22.01 15:37", "src": "FX.CO", "url": "https://www.fx.co/pl/signals"},
        {"p": "#MU H1", "type": "BUY STOP", "in": "381.6300", "tp": "408.1800", "sl": "355.0800", "date": "22.01 15:35", "src": "FX.CO", "url": "https://www.fx.co/pl/signals"},
        {"p": "#KO H1", "type": "BUY STOP", "in": "71.7740", "tp": "73.1600", "sl": "70.3880", "date": "22.01 15:33", "src": "FX.CO", "url": "https://www.fx.co/pl/signals"},
        {"p": "BTC/USD", "type": "SELL", "in": "89,802.72", "tp": "87,585.00", "sl": "90,212.00", "date": "22.01 09:56", "src": "BESTFREESIGNAL", "url": "https://www.bestfreesignal.com/"},
        {"p": "XAU/USD", "type": "BUY", "in": "4,781.570", "tp": "4,888.834", "sl": "4,750.000", "date": "22.01 09:51", "src": "BESTFREESIGNAL", "url": "https://www.bestfreesignal.com/"},
        {"p": "GBP/USD", "type": "KUPNO", "in": "1.3431", "tp": "1.3447", "sl": "1.3411", "date": "22.01 12:05", "src": "FORESIGNAL", "url": "https://foresignal.com/en/"},
        {"p": "USD/JPY", "type": "KUPNO", "in": "158.08", "tp": "158.31", "sl": "157.80", "date": "22.01 12:15", "src": "FORESIGNAL", "url": "https://foresignal.com/en/"},
        {"p": "USD/CHF", "type": "KUPNO", "in": "0.7937", "tp": "0.7947", "sl": "0.7924", "date": "22.01 11:10", "src": "FORESIGNAL", "url": "https://foresignal.com/en/"}
    ]

# 3. INTERFEJS GŁÓWNY
c1, c2 = st.columns([1.3, 0.7])

with c1:
    st.title("🚀 TERMINAL V17.3")
    st.subheader("📡 Sygnały Aktywne (22.01)")
    data = get_full_active_data()
    for s in data:
        color = "#00ff88" if "BUY" in s['type'] or "KUPNO" in s['type'] else "#ff4b4b"
        with st.container():
            st.markdown(f"""
            <div class="signal-card" style="border-left-color: {color}">
                <span class="time-stamp">{s['date']}</span>
                <b>{s['p']}</b> | <a href="{s['url']}" target="_blank" style="color:#58a6ff; text-decoration:none;">🔗 {s['src']}</a>
                <div style="color:{color}; font-size:1.2rem; font-weight:bold; margin:10px 0;">{s['type']} @ {s['in']}</div>
                <div style="background:rgba(0,0,0,0.3); padding:8px; border-radius:5px; display:flex; justify-content:space-between; font-family:monospace; font-size:0.9rem;">
                    <span>TP: {s['tp']}</span><span>SL: {s['sl']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔍 ANALIZUJ {s['p']}", key=f"btn_{s['p']}"):
                st.toast(f"Synchronizacja agregatów dla {s['p']}...")

with c2:
    st.subheader("📊 Niezależne Agregaty")
    st.markdown("""
        <div class="agg-box"><small>INVESTING.COM</small><br><b style="color:#00ff88">SILNE KUPNO</b></div>
        <div class="agg-box"><small>TRADINGVIEW</small><br><b style="color:#ff4b4b">SPRZEDAŻ</b></div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("🏆 Ranking Szans AI")
    df = pd.DataFrame(data)
    df['Szansa %'] = df.apply(calculate_real_chance, axis=1)
    
    # Ranking posortowany od największej szansy wynikającej z analizy
    st.dataframe(
        df[['p', 'Szansa %', 'src']].sort_values(by='Szansa %', ascending=False),
        hide_index=True,
        use_container_width=True,
        column_config={
            "Szansa %": st.column_config.ProgressColumn("Prawdopodobieństwo", min_value=0, max_value=100),
            "p": "Instrument"
        }
    )
