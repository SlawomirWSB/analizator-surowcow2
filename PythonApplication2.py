import streamlit as st
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

# 1. Konfiguracja
st.set_page_config(layout="wide", page_title="XTB SIGNAL TERMINAL V47", page_icon="🎯")
st_autorefresh(interval=60 * 1000, key="data_refresh")

st.markdown("""
    <style>
    .block-container { padding: 1rem !important; }
    iframe { border-radius: 10px; background: #131722; border: 1px solid #2a2e39; }
    .signal-header { color: #FF4B4B; font-weight: bold; font-size: 20px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

DB = {
    "SUROWCE": {"GOLD": "TVC:GOLD", "SILVER": "TVC:SILVER", "COCOA": "ICEUS:CC1!", "OIL": "TVC:USOIL"},
    "INDEKSY": {"US100": "TVC:NDX", "DE30": "TVC:DAX", "US500": "TVC:SPX"},
    "FOREX": {"EURUSD": "FX:EURUSD", "USDPLN": "FX_IDC:USDPLN"}
}

def main():
    # Sterowanie
    col_nav1, col_nav2, col_nav3 = st.columns([2, 2, 1])
    with col_nav1: rynek = st.selectbox("Rynek:", list(DB.keys()))
    with col_nav2: inst = st.selectbox("Instrument:", list(DB[rynek].keys()))
    with col_nav3: itv = st.selectbox("Interwał:", ["5", "15", "60", "D"], index=1)

    symbol = DB[rynek][inst]
    tv_int = f"{itv}m" if itv.isdigit() else "1D"

    st.markdown(f"### 🎯 Signal & Verification Hub: {inst}")

    # --- UKŁAD 3 KOLUMN ---
    c1, c2, c3 = st.columns([1.2, 1.5, 1])

    with c1:
        st.markdown('<p class="signal-header">🚀 DARMOWE SYGNAŁY LIVE</p>', unsafe_allow_html=True)
        # Widget z listą sygnałów technicznych i alertów
        sig_url = f"https://s.tradingview.com/embed-widget/events/?locale=pl#%7B%22colorTheme%22%3A%22dark%22%2C%22isTransparent%22%3Atrue%2C%22width%22%3A%22100%25%22%2C%22height%22%3A500%2C%22symbol%22%3A%22{symbol}%22%2C%22importanceFilter%22%3A%22-1%2C0%2C1%22%7D"
        components.iframe(sig_url, height=500)

    with c2:
        st.markdown('<p class="signal-header">⚖️ POTWIERDZENIE (ZEGARY)</p>', unsafe_allow_html=True)
        # Twój widget z 3 zegarami
        conf_url = f"https://s.tradingview.com/embed-widget/technical-analysis/?locale=pl#%7B%22interval%22%3A%22{tv_int}%22%2C%22width%22%3A%22100%25%22%2C%22isTransparent%22%3Atrue%2C%22height%22%3A500%2C%22symbol%22%3A%22{symbol}%22%2C%22displayMode%22%3A%22multiple%22%2C%22colorTheme%22%3A%22dark%22%7D"
        components.iframe(conf_url, height=500)

    with c3:
        st.markdown('<p class="signal-header">📉 TREND DŁUGOTERMINOWY</p>', unsafe_allow_html=True)
        # Mini wykres z trendem, aby widzieć czy sygnał nie idzie pod prąd
        trend_url = f"https://s.tradingview.com/embed-widget/mini-symbol-overview/?locale=pl#%7B%22symbol%22%3A%22{symbol}%22%2C%22width%22%3A%22100%25%22%2C%22height%22%3A500%2C%22dateRange%22%3A%221D%22%2C%22colorTheme%22%3A%22dark%22%2C%22trendLineColor%22%3A%22%2337a6ef%22%2C%22underLineColor%22%3A%22rgba(55%2C%20166%2C%20239%2C%200.15)%22%2C%22isTransparent%22%3Atrue%2C%22autosize%22%3Afalse%7D"
        components.iframe(trend_url, height=500)

    # --- GŁÓWNY WYKRES DO EGZEKUCJI ---
    st.markdown("---")
    st.markdown('<p class="signal-header">⌨️ PANEL EGZEKUCJI (XTB/TV)</p>', unsafe_allow_html=True)
    main_chart = f"https://s.tradingview.com/widgetembed/?symbol={symbol}&interval={itv}&theme=dark&locale=pl"
    components.iframe(main_chart, height=550)

if __name__ == "__main__":
    main()
