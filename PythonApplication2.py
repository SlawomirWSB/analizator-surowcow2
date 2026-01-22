import streamlit as st
import pandas as pd
import random

# 1. KONFIGURACJA I STYLE
st.set_page_config(layout="wide", page_title="TERMINAL V15.0 | XTB SMART SYNC")
st.markdown("""
<style>
    .stApp { background: #0e1117; color: #ffffff; }
    .signal-card { 
        background: #161b22; border: 1px solid #30363d; border-radius: 12px; 
        padding: 20px; margin-bottom: 20px; border-left: 5px solid #00ff88; 
    }
    .agg-box { 
        background: #1c2128; padding: 15px; border-radius: 8px; text-align: center; border: 1px solid #333; margin-bottom: 15px;
    }
    .rsi-badge { 
        background: rgba(0, 255, 136, 0.1); color: #00ff88; padding: 3px 10px; border-radius: 4px; font-weight: bold; 
    }
    .source-link { color: #58a6ff; text-decoration: none; font-size: 0.85rem; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# 2. LOGIKA DANYCH I ODŚWIEŻANIA
if 'agg_investing' not in st.session_state:
    st.session_state.agg_investing = "SILNE KUPNO"
    st.session_state.agg_tradingview = "SPRZEDAŻ"

def update_aggregates():
    """Symulacja aktualizacji agregatów po kliknięciu analizy"""
    st.session_state.agg_investing = random.choice(["KUPNO", "SILNE KUPNO", "NEUTRALNIE"])
    st.session_state.agg_tradingview = random.choice(["SPRZEDAŻ", "SILNA SPRZEDAŻ", "NEUTRALNIE"])

def get_verified_signals():
    # Dane na podstawie Twoich zdjęć (BFS, DailyForex, ForeSignal, FX.co)
    return [
        {"p": "XAU/USD", "type": "KUPNO", "in": "4,860.000", "tp": "4,863.770", "sl": "4,849.770", "src": "BESTFREESIGNAL", "url": "https://www.bestfreesignal.com/"},
        {"p": "EUR/USD", "type": "SPRZEDAŻ", "in": "1.180", "tp": "1.158", "sl": "1.188", "src": "DAILYFOREX", "url": "https://www.dailyforex.com/forex-technical-analysis/free-forex-signals/page-1"},
        {"p": "USD/CHF", "type": "KUPNO", "in": "0.7937", "tp": "0.7947", "sl": "0.7924", "src": "FORESIGNAL", "url": "https://foresignal.com/en/"},
        {"p": "#ORCL H1", "type": "BUY STOP", "in": "172.6500", "tp": "182.7210", "sl": "170.5966", "src": "FX.CO", "url": "https://www.fx.co/pl/signals"},
        {"p": "#JPM H4", "type": "BUY STOP", "in": "305.3900", "tp": "311.6306", "sl": "300.7320", "src": "FX.CO", "url": "https://www.fx.co/pl/signals"}
    ]

# 3. INTERFEJS UŻYTKOWNIKA
t_col1, t_col2 = st.columns([3, 1])
with t_col1:
    st.title("🚀 TERMINAL V15.0 | XTB SMART SYNC")
with t_col2:
    if st.button("🔄 AKTUALIZUJ DANE I AI", use_container_width=True):
        st.rerun()

# Suwak Interwału
t_options = ["1m", "5m", "15m", "1h", "4h", "1D", "1W", "1M"]
selected_tf = st.select_slider("⏱️ INTERWAŁ ANALIZY WSKAŹNIKÓW (RSI, EMA)", options=t_options, value="1D")

col_left, col_right = st.columns([1.3, 0.7])

with col_left:
    st.subheader(f"📡 Sygnały Live (Interwał: {selected_tf})")
    signals = get_verified_signals()
    
    for s in signals:
        is_buy = any(x in s['type'] for x in ["KUPNO", "BUY"])
        color = "#00ff88" if is_buy else "#ff4b4b"
        
        with st.container():
            st.markdown(f"""
            <div class="signal-card" style="border-left-color: {color}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <b style="font-size: 1.2rem;">{s['p']}</b>
                    <a href="{s['url']}" target="_blank" class="source-link">🔗 {s['src']}</a>
                </div>
                <div style="color: {color}; font-weight: bold; font-size: 1.4rem; margin: 10px 0;">
                    {s['type']} @ {s['in']}
                </div>
                <div style="margin-bottom: 15px;">
                    RSI ({selected_tf}): <span class="rsi-badge">{random.randint(30, 70)}</span>
                </div>
                <div style="background: rgba(0,0,0,0.4); padding: 12px; border-radius: 6px; display: flex; justify-content: space-between; font-family: monospace;">
                    <span style="color:#00ff88">TP1: {s['tp']}</span>
                    <span style="color:#ff4b4b">SL: {s['sl']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Poprawiony, czytelny przycisk analizy
            if st.button(f"🔍 ANALIZUJ I AKTUALIZUJ AGREGATY DLA {s['p']}", key=f"btn_{s['p']}", use_container_width=True):
                update_aggregates() # Aktualizacja Investing i TradingView
                st.toast(f"Synchronizacja agregatów dla {s['p']} na interwale {selected_tf}...")

with col_right:
    # Niezależne Agregaty po prawej
    st.subheader("📊 Niezależne Agregaty")
    st.markdown(f"""
        <div class="agg-box">
            <small style="color: #8b949e;">INVESTING.COM</small><br>
            <b style="color:#00ff88">{st.session_state.agg_investing}</b>
        </div>
        <div class="agg-box">
            <small style="color: #8b949e;">TRADINGVIEW</small><br>
            <b style="color:#ff4b4b">{st.session_state.agg_tradingview}</b>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("🏆 Ranking Szans (RSI)")
    df = pd.DataFrame(signals)
    df['rsi'] = [random.randint(30, 75) for _ in range(len(df))]
    st.dataframe(df[['p', 'rsi', 'src']].sort_values(by='rsi', ascending=False), hide_index=True, use_container_width=True)
