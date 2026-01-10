import streamlit as st
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

# 1. Konfiguracja terminala
st.set_page_config(layout="wide", page_title="XTB PRO TERMINAL V45", page_icon="📈")
st_autorefresh(interval=60 * 1000, key="data_refresh")

st.markdown("""
    <style>
    .block-container { padding: 1rem !important; }
    header { visibility: hidden; }
    iframe { border-radius: 8px; background: #131722; border: 1px solid #2a2e39; }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza Danych
DB = {
    "SUROWCE": {
        "GOLD (Złoto)": {"tv": "TVC:GOLD", "inv": "8830"},
        "SILVER (Srebro)": {"tv": "TVC:SILVER", "inv": "8836"},
        "COCOA (Kakao)": {"tv": "ICEUS:CC1!", "inv": "8894"},
        "OIL.WTI (Ropa)": {"tv": "TVC:USOIL", "inv": "8849"},
        "NATGAS (Gaz)": {"tv": "TVC:NATGAS", "inv": "8862"}
    },
    "INDEKSY": {
        "US100 (Nasdaq)": {"tv": "TVC:NDX", "inv": "14958"},
        "DE30 (DAX)": {"tv": "TVC:DAX", "inv": "172"},
        "US500 (S&P500)": {"tv": "TVC:SPX", "inv": "166"}
    },
    "FOREX": {
        "EURUSD": {"tv": "FX:EURUSD", "inv": "1"},
        "USDPLN": {"tv": "FX_IDC:USDPLN", "inv": "40"}
    }
}

def main():
    # Sterowanie
    c1, c2, c3 = st.columns([2, 2, 1])
    with c1: rynek = st.selectbox("Rynek:", list(DB.keys()))
    with c2: inst = st.selectbox("Instrument:", list(DB[rynek].keys()))
    with c3: itv = st.selectbox("Interwał:", ["1", "5", "15", "60", "D"], index=2)

    s = DB[rynek][inst]
    tv_int = f"{itv}m" if itv.isdigit() else "1D"

    st.subheader(f"🛡️ Terminal Analityczny V45: {inst}")

    # --- TRZY FILARY DANYCH (UNIKALNE) ---
    col1, col2, col3 = st.columns([1.5, 1, 1])

    with col1:
        st.caption("🟢 1. ANALIZA SZCZEGÓŁOWA (3 Zegary)")
        # Widget TradingView z 3 zegarami (DisplayMode: multiple)
        tv_url = f"https://s.tradingview.com/embed-widget/technical-analysis/?locale=pl#%7B%22interval%22%3A%22{tv_int}%22%2C%22width%22%3A%22100%25%22%2C%22isTransparent%22%3Atrue%2C%22height%22%3A450%2C%22symbol%22%3A%22{s['tv']}%22%2C%22showIntervalTabs%22%3Atrue%2C%22displayMode%22%3A%22multiple%22%2C%22colorTheme%22%3A%22dark%22%7D"
        st.components.v1.iframe(tv_url, height=450)

    with col2:
        st.caption("🔵 2. SIŁA WALUT (Heat Map)")
        # Mapa cieplna - pokazuje które waluty dominują na rynku bez logowania
        heat_map_url = "https://s.tradingview.com/embed-widget/crypto-mcap/?locale=pl#%7B%22symbol%22%3A%22NASDAQ%3AAAPL%22%2C%22colorTheme%22%3A%22dark%22%2C%22isTransparent%22%3Atrue%2C%22width%22%3A%22100%25%22%2C%22height%22%3A450%7D"
        # Poprawka na Currency Heat Map dla Forex/Surowców
        if rynek == "FOREX":
            map_url = "https://s.tradingview.com/embed-widget/forex-heat-map/?locale=pl#%7B%22width%22%3A%22100%25%22%2C%22height%22%3A450%2C%22currencies%22%3A%5B%22EUR%22%2C%22USD%22%2C%22GBP%22%2C%22JPY%22%2C%22CHF%22%2C%22AUD%22%2C%22CAD%22%2C%22NZD%22%5D%2C%22isTransparent%22%3Atrue%2C%22colorTheme%22%3A%22dark%22%7D"
        else:
            map_url = "https://s.tradingview.com/embed-widget/market-overview/?locale=pl#%7B%22colorTheme%22%3A%22dark%22%2C%22dateRange%22%3A%2212M%22%2C%22showChart%22%3Atrue%2C%22locale%22%3A%22pl%22%2C%22width%22%3A%22100%25%22%2C%22height%22%3A450%2C%22isTransparent%22%3Atrue%2C%22tabs%22%3A%5B%7B%22title%22%3A%22Surowce%22%2C%22symbols%22%3A%5B%7B%22s%22%3A%22TVC:GOLD%22%7D%2C%7B%22s%22%3A%22TVC:SILVER%22%7D%2C%7B%22s%22%3A%22TVC:USOIL%22%7D%2C%7B%22s%22%3A%22ICEUS:CC1!%22%7D%5D%7D%5D%7D"
        st.components.v1.iframe(map_url, height=450)

    with col3:
        st.caption("🔴 3. WERDYKT (Investing)")
        # Powrót do twardych danych z Investing
        inv_url = f"https://ssltsw.investing.com?lang=51&forex={s['inv']}&commodities={s['inv']}&indices={s['inv']}&time_frame=900"
        st.components.v1.iframe(inv_url, height=450)

    # --- WYKRES ---
    st.markdown("---")
    chart_url = f"https://s.tradingview.com/widgetembed/?symbol={s['tv']}&interval={itv}&theme=dark&locale=pl"
    st.components.v1.iframe(chart_url, height=600)

if __name__ == "__main__":
    main()
