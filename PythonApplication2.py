import streamlit as st
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

# 1. Konfiguracja
st.set_page_config(layout="wide", page_title="XTB ULTIMATE SIGNAL V49", page_icon="🎯")
st_autorefresh(interval=60 * 1000, key="data_refresh")

st.markdown("""
    <style>
    .block-container { padding: 1rem !important; }
    header { visibility: hidden; }
    iframe { border-radius: 10px; background: #131722; border: 1px solid #2a2e39 !important; }
    .signal-box { background-color: #1e222d; padding: 15px; border-radius: 10px; border-left: 5px solid #00ff88; }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza Instrumentów
DB = {
    "SUROWCE": {"GOLD": "TVC:GOLD", "SILVER": "TVC:SILVER", "COCOA": "ICEUS:CC1!", "OIL": "TVC:USOIL"},
    "INDEKSY": {"US100": "TVC:NDX", "DE30": "TVC:DAX", "US500": "TVC:SPX"},
    "FOREX": {"EURUSD": "FX:EURUSD", "USDPLN": "FX_IDC:USDPLN"}
}

def main():
    # Sterowanie
    c_nav1, c_nav2, c_nav3 = st.columns([2, 2, 1])
    with c_nav1: rynek = st.selectbox("Rynek:", list(DB.keys()))
    with c_nav2: inst = st.selectbox("Instrument:", list(DB[rynek].keys()))
    with c_nav3: itv = st.selectbox("Interwał:", ["5", "15", "60", "D"], index=1)

    symbol = DB[rynek][inst]
    tv_int = f"{itv}m" if itv.isdigit() else "1D"

    st.subheader(f"🚀 Signal Center: {inst} ({itv}m)")

    # --- UKŁAD TRZECH FILARÓW ---
    col1, col2, col3 = st.columns([1.5, 1, 1.2])

    with col1:
        st.info("✅ 1. POTWIERDZENIE (3 Zegary)")
        # Widget z 3 zegarami - Twój ulubiony
        tv_url = f"https://s.tradingview.com/embed-widget/technical-analysis/?locale=pl#%7B%22interval%22%3A%22{tv_int}%22%2C%22width%22%3A%22100%25%22%2C%22isTransparent%22%3Atrue%2C%22height%22%3A450%2C%22symbol%22%3A%22{symbol}%22%2C%22displayMode%22%3A%22multiple%22%2C%22colorTheme%22%3A%22dark%22%7D"
        components.iframe(tv_url, height=460)

    with col2:
        st.error("📡 2. ALERTY TECHNICZNE (Sygnały)")
        # Widget Timeline - pokazuje darmowe sygnały techniczne (np. przecięcia średnich)
        sig_url = f"https://s.tradingview.com/embed-widget/timeline/?locale=pl#%7B%22colorTheme%22%3A%22dark%22%2C%22isTransparent%22%3Atrue%2C%22displayMode%22%3A%22regular%22%2C%22width%22%3A%22100%25%22%2C%22height%22%3A450%2C%22symbol%22%3A%22{symbol}%22%7D"
        components.iframe(sig_url, height=460)

    with col3:
        st.warning("📅 3. KALENDARZ (Ryzyko)")
        # Kalendarz ekonomiczny - klucz do darmowych sygnałów
        econ_url = "https://s.tradingview.com/embed-widget/events/?locale=pl#%7B%22colorTheme%22%3A%22dark%22%2C%22isTransparent%22%3Atrue%2C%22width%22%3A%22100%25%22%2C%22height%22%3A450%2C%22importanceFilter%22%3A%220%2C1%22%2C%22currencyFilter%22%3A%22USD%2CEUR%2CPLN%22%7D"
        components.iframe(econ_url, height=460)

    # --- WYKRES NA DOLE ---
    st.markdown("---")
    chart_url = f"https://s.tradingview.com/widgetembed/?symbol={symbol}&interval={itv}&theme=dark&locale=pl"
    components.iframe(chart_url, height=550)

if __name__ == "__main__":
    main()
