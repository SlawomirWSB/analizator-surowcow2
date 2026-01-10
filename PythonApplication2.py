import streamlit as st
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

st.set_page_config(layout="wide", page_title="XTB PRO TERMINAL V46", page_icon="📉")
st_autorefresh(interval=60 * 1000, key="data_refresh")

# Baza danych z ujednoliconymi ID
DB = {
    "SUROWCE": {
        "GOLD (Złoto)": {"tv": "TVC:GOLD", "inv": "8830"},
        "SILVER (Srebro)": {"tv": "TVC:SILVER", "inv": "8836"},
        "COCOA (Kakao)": {"tv": "ICEUS:CC1!", "inv": "8894"},
        "OIL.WTI (Ropa)": {"tv": "TVC:USOIL", "inv": "8849"}
    },
    "INDEKSY": {
        "US100 (Nasdaq)": {"tv": "TVC:NDX", "inv": "14958"},
        "DE30 (DAX)": {"tv": "TVC:DAX", "inv": "172"}
    },
    "FOREX": {
        "EURUSD": {"tv": "FX:EURUSD", "inv": "1"},
        "USDPLN": {"tv": "FX_IDC:USDPLN", "inv": "40"}
    }
}

def main():
    c1, c2, c3 = st.columns([2, 2, 1])
    with c1: rynek = st.selectbox("Rynek:", list(DB.keys()))
    with c2: inst = st.selectbox("Instrument:", list(DB[rynek].keys()))
    with c3: itv = st.selectbox("Interwał:", ["1", "5", "15", "60", "D"], index=2)

    s = DB[rynek][inst]
    tv_int = f"{itv}m" if itv.isdigit() else "1D"

    st.subheader(f"🔍 System Potrójnej Weryfikacji: {inst}")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.caption("📊 1. PEŁNA TECHNIKA (TV)")
        # Widget z 3 zegarami
        url1 = f"https://s.tradingview.com/embed-widget/technical-analysis/?locale=pl#%7B%22interval%22%3A%22{tv_int}%22%2C%22width%22%3A%22100%25%22%2C%22isTransparent%22%3Atrue%2C%22height%22%3A450%2C%22symbol%22%3A%22{s['tv']}%22%2C%22displayMode%22%3A%22multiple%22%2C%22colorTheme%22%3A%22dark%22%7D"
        st.components.v1.iframe(url1, height=450)

    with col2:
        st.caption("📈 2. SENTYMENT OGÓLNY")
        # Widget "Single Gauge" jako szybki sentyment
        url2 = f"https://s.tradingview.com/embed-widget/technical-analysis/?locale=pl#%7B%22interval%22%3A%22{tv_int}%22%2C%22width%22%3A%22100%25%22%2C%22isTransparent%22%3Atrue%2C%22height%22%3A450%2C%22symbol%22%3A%22{s['tv']}%22%2C%22displayMode%22%3A%22single%22%2C%22colorTheme%22%3A%22dark%22%7D"
        st.components.v1.iframe(url2, height=450)

    with col3:
        st.caption("🔴 3. WERDYKT INVESTING")
        # Niezależne źródło Investing
        url3 = f"https://ssltsw.investing.com?lang=51&forex={s['inv']}&commodities={s['inv']}&indices={s['inv']}&time_frame=900"
        st.components.v1.iframe(url3, height=450)

    st.markdown("---")
    # Wykres interaktywny
    chart_url = f"https://s.tradingview.com/widgetembed/?symbol={s['tv']}&interval={itv}&theme=dark&locale=pl"
    st.components.v1.iframe(chart_url, height=550)

if __name__ == "__main__":
    main()
