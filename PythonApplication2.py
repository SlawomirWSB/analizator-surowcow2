import streamlit as st
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

st.set_page_config(layout="wide", page_title="XTB SIGNAL VERIFIER V48", page_icon="🕵️")
st_autorefresh(interval=60 * 1000, key="data_refresh")

# Baza danych
DB = {
    "SUROWCE": {"GOLD": "TVC:GOLD", "SILVER": "TVC:SILVER", "OIL": "TVC:USOIL"},
    "INDEKSY": {"US100": "TVC:NDX", "DE30": "TVC:DAX"},
    "FOREX": {"EURUSD": "FX:EURUSD", "GBPUSD": "FX:GBPUSD"}
}

def main():
    c1, c2, c3 = st.columns([2, 2, 1])
    with c1: rynek = st.selectbox("Rynek:", list(DB.keys()))
    with c2: inst = st.selectbox("Instrument:", list(DB[rynek].keys()))
    with c3: itv = st.selectbox("Interwał:", ["5", "15", "60", "D"], index=1)

    symbol = DB[rynek][inst]
    tv_int = f"{itv}m" if itv.isdigit() else "1D"

    # --- UKŁAD WERYFIKACYJNY ---
    col_sig, col_conf = st.columns([1, 1.5])

    with col_sig:
        st.error("📡 LIVE SIGNALS FEED (Signals Provider FX)")
        # Osadzenie publicznego podglądu Telegrama w ramce
        tg_url = "https://t.me/s/signalsproviderfx"
        components.iframe(tg_url, height=700, scrolling=True)

    with col_conf:
        st.success(f"⚖️ POTWIERDZENIE TECHNICZNE: {inst}")
        # Zegary weryfikacyjne TradingView
        conf_url = f"https://s.tradingview.com/embed-widget/technical-analysis/?locale=pl#%7B%22interval%22%3A%22{tv_int}%22%2C%22width%22%3A%22100%25%22%2C%22isTransparent%22%3Atrue%2C%22height%22%3A650%2C%22symbol%22%3A%22{symbol}%22%2C%22displayMode%22%3A%22multiple%22%2C%22colorTheme%22%3A%22dark%22%7D"
        components.iframe(conf_url, height=660)

    st.markdown("---")
    st.info("💡 **Instrukcja**: Porównaj ostatni post na Telegramie (lewa) ze wskazaniem zegarów (prawa). Jeśli oba mówią 'Kupuj', prawdopodobieństwo sukcesu wzrasta.")

if __name__ == "__main__":
    main()
