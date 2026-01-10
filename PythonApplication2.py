import streamlit as st
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

# 1. Konfiguracja strony
st.set_page_config(layout="wide", page_title="XTB TERMINAL V43 - ULTRA STABLE", page_icon="📈")
st_autorefresh(interval=60 * 1000, key="data_refresh")

# Stylizacja
st.markdown("""
    <style>
    .block-container { padding: 1rem !important; }
    header { visibility: hidden; }
    iframe { border-radius: 8px; background: #131722; border: 1px solid #2a2e39; }
    </style>
    """, unsafe_allow_html=True)

# 2. BAZA DANYCH (Zoptymalizowana pod darmowe feedy)
DB = {
    "SUROWCE": {
        "GOLD (Złoto)": "TVC:GOLD",
        "SILVER (Srebro)": "TVC:SILVER",
        "COCOA (Kakao)": "ICEUS:CC1!",
        "COFFEE (Kawa)": "ICEUS:KC1!",
        "OIL.WTI (Ropa)": "TVC:USOIL",
        "NATGAS (Gaz)": "TVC:NATGAS"
    },
    "INDEKSY": {
        "US100 (Nasdaq)": "TVC:NDX",
        "US500 (S&P500)": "TVC:SPX",
        "DE30 (DAX)": "TVC:DAX",
        "WIG20 (Polska)": "GPW:WIG20"
    },
    "FOREX": {
        "EURUSD": "FX:EURUSD",
        "USDPLN": "FX_IDC:USDPLN",
        "GBPUSD": "FX:GBPUSD"
    }
}

def main():
    # --- PANEL STEROWANIA ---
    c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
    with c1: rynek = st.selectbox("Rynek:", list(DB.keys()))
    with c2: inst = st.selectbox("Instrument:", list(DB[rynek].keys()))
    with c3: itv = st.selectbox("Interwał:", ["1", "5", "15", "60", "D"], index=2)
    with c4: st.write(""); audio = st.checkbox("Audio Alert", value=True)

    symbol = DB[rynek][inst]
    # Mapowanie interwału dla widgetu (minuty muszą mieć dopisek 'm')
    tv_int = f"{itv}m" if itv.isdigit() else "1D"

    st.subheader(f"🛡️ System Weryfikacji Technicznej: {inst}")

    # --- TWO-PILLAR ANALYSIS (Metoda Iframe Direct) ---
    col1, col2 = st.columns(2)

    with col1:
        st.caption("✅ SYGNAŁ 1: PODSUMOWANIE (Zegar)")
        # Używamy bezpośredniego linku do widgetu Technical Analysis
        widget_url = f"https://s.tradingview.com/embed-widget/technical-analysis/?locale=pl#%7B%22interval%22%3A%22{tv_int}%22%2C%22width%22%3A%22100%25%22%2C%22isTransparent%22%3Atrue%2C%22height%22%3A450%2C%22symbol%22%3A%22{symbol}%22%2C%22showIntervalTabs%22%3Atrue%2C%22displayMode%22%3A%22single%22%2C%22colorTheme%22%3A%22dark%22%7D"
        st.components.v1.iframe(widget_url, height=450)

    with col2:
        st.caption("🔍 SYGNAŁ 2: SZCZEGÓŁY (Wskaźniki)")
        # Ten sam widget, ale w trybie 'multiple'
        detail_url = f"https://s.tradingview.com/embed-widget/technical-analysis/?locale=pl#%7B%22interval%22%3A%22{tv_int}%22%2C%22width%22%3A%22100%25%22%2C%22isTransparent%22%3Atrue%2C%22height%22%3A450%2C%22symbol%22%3A%22{symbol}%22%2C%22showIntervalTabs%22%3Atrue%2C%22displayMode%22%3A%22multiple%22%2C%22colorTheme%22%3A%22dark%22%7D"
        st.components.v1.iframe(detail_url, height=450)

    # --- WYKRES DOLNY ---
    st.markdown("---")
    chart_url = f"https://s.tradingview.com/widgetembed/?symbol={symbol}&interval={itv}&symboledit=1&saveimage=1&toolbarbg=f1f3f6&studies=[]&theme=dark&style=1&timezone=Europe%2FWarsaw&studies_overrides=%7B%7D&overrides=%7B%7D&enabled_features=[]&disabled_features=[]&locale=pl"
    st.components.v1.iframe(chart_url, height=600)

if __name__ == "__main__":
    main()
