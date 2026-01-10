import streamlit as st
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

# 1. Konfiguracja
st.set_page_config(layout="wide", page_title="XTB TERMINAL V44 - UNIQUE DATA", page_icon="🚀")
st_autorefresh(interval=60 * 1000, key="data_refresh")

st.markdown("""
    <style>
    .block-container { padding: 1rem !important; }
    header { visibility: hidden; }
    iframe { border-radius: 8px; background: #131722; border: 1px solid #2a2e39; }
    </style>
    """, unsafe_allow_html=True)

# 2. Precyzyjna Baza Danych (Dopasowana pod 3 różne źródła)
DB = {
    "SUROWCE": {
        "GOLD (Złoto)": {"tv": "TVC:GOLD", "inv": "8830", "sent": "gold"},
        "SILVER (Srebro)": {"tv": "TVC:SILVER", "inv": "8836", "sent": "silver"},
        "COCOA (Kakao)": {"tv": "ICEUS:CC1!", "inv": "8894", "sent": "cocoa"},
        "OIL.WTI (Ropa)": {"tv": "TVC:USOIL", "inv": "8849", "sent": "oil"},
        "NATGAS (Gaz)": {"tv": "TVC:NATGAS", "inv": "8862", "sent": "natural-gas"}
    },
    "INDEKSY": {
        "US100 (Nasdaq)": {"tv": "TVC:NDX", "inv": "14958", "sent": "nasdaq-100"},
        "DE30 (DAX)": {"tv": "TVC:DAX", "inv": "172", "sent": "germany-30"},
        "US500 (S&P500)": {"tv": "TVC:SPX", "inv": "166", "sent": "sp-500"}
    },
    "FOREX": {
        "EURUSD": {"tv": "FX:EURUSD", "inv": "1", "sent": "eur-usd"},
        "USDPLN": {"tv": "FX_IDC:USDPLN", "inv": "40", "sent": "usd-pln"}
    }
}

def main():
    c1, c2, c3 = st.columns([2, 2, 1])
    with c1: rynek = st.selectbox("Rynek:", list(DB.keys()))
    with c2: inst = st.selectbox("Instrument:", list(DB[rynek].keys()))
    with c3: itv = st.selectbox("Interwał:", ["1", "5", "15", "60", "D"], index=2)

    s = DB[rynek][inst]
    tv_int = f"{itv}m" if itv.isdigit() else "1D"

    st.subheader(f"🛡️ Triple-Source Verification: {inst}")

    # --- TRZY RÓŻNE WIDGETY ---
    col1, col2, col3 = st.columns(3)

    with col1:
        st.caption("🔴 ŹRÓDŁO 1: SYGNAŁ INVESTING")
        # Direct Iframe do Investing.com (Sygnały Techniczne)
        inv_url = f"https://ssltsw.investing.com?lang=51&forex={s['inv']}&commodities={s['inv']}&indices={s['inv']}&time_frame=900"
        st.components.v1.iframe(inv_url, height=450)

    with col2:
        st.caption("🔵 ŹRÓDŁO 2: SENTYMENT TŁUMU (IG)")
        # Sentyment rynkowy (Kupujący vs Sprzedający)
        if s['sent']:
            sent_url = f"https://www.dailyfx.com/sentiment-widget/{s['sent']}"
            st.components.v1.iframe(sent_url, height=450)
        else:
            st.warning("Sentyment niedostępny")

    with col3:
        st.caption("🟢 ŹRÓDŁO 3: ZEGARY TRADINGVIEW")
        # Zegar zbiorczy z TradingView
        tv_url = f"https://s.tradingview.com/embed-widget/technical-analysis/?locale=pl#%7B%22interval%22%3A%22{tv_int}%22%2C%22width%22%3A%22100%25%22%2C%22isTransparent%22%3Atrue%2C%22height%22%3A450%2C%22symbol%22%3A%22{s['tv']}%22%2C%22showIntervalTabs%22%3Afalse%2C%22displayMode%22%3A%22single%22%2C%22colorTheme%22%3A%22dark%22%7D"
        st.components.v1.iframe(tv_url, height=450)

    # --- WYKRES ---
    st.markdown("---")
    chart_url = f"https://s.tradingview.com/widgetembed/?symbol={s['tv']}&interval={itv}&theme=dark&locale=pl"
    st.components.v1.iframe(chart_url, height=600)

if __name__ == "__main__":
    main()
