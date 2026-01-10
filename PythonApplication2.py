import streamlit as st
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

# 1. Konfiguracja i Autorefresh
st.set_page_config(layout="wide", page_title="XTB TERMINAL V42 - STABLE", page_icon="⚡")
st_autorefresh(interval=60 * 1000, key="data_refresh")

# Stylizacja - Eliminacja marginesów
st.markdown("""
    <style>
    .block-container { padding: 1rem !important; }
    header { visibility: hidden; }
    iframe { border-radius: 10px; border: 1px solid #2a2e39 !important; background: #131722; }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza danych instrumentów
DB = {
    "SUROWCE": {
        "GOLD (Złoto)": "OANDA:XAUUSD",
        "SILVER (Srebro)": "OANDA:XAGUSD",
        "COCOA (Kakao)": "ICEUS:CC1!",
        "COFFEE (Kawa)": "ICEUS:KC1!",
        "OIL.WTI (Ropa)": "TVC:USOIL",
        "NATGAS (Gaz)": "TVC:NATGAS"
    },
    "INDEKSY": {
        "US100 (Nasdaq)": "NASDAQ:NDX",
        "US500 (S&P500)": "TVC:SPX",
        "DE30 (DAX)": "GLOBALPRIME:GER30",
        "WIG20 (Polska)": "GPW:WIG20"
    },
    "FOREX": {
        "EURUSD": "FX:EURUSD",
        "USDPLN": "OANDA:USDPLN",
        "GBPUSD": "FX:GBPUSD"
    }
}

def create_tv_widget(symbol, interval, mode="multiple"):
    # Konwersja interwału dla Widgetu TV
    adj_int = interval if interval == "D" else f"{interval}"
    return f"""
    <div class="tradingview-widget-container">
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
      {{
      "interval": "{adj_int}",
      "width": "100%",
      "isTransparent": true,
      "height": 450,
      "symbol": "{symbol}",
      "showIntervalTabs": true,
      "displayMode": "{mode}",
      "locale": "pl",
      "colorTheme": "dark"
    }}
      </script>
    </div>
    """

def main():
    # MENU
    c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
    with c1: rynek = st.selectbox("Rynek:", list(DB.keys()))
    with c2: inst = st.selectbox("Instrument:", list(DB[rynek].keys()))
    with c3: itv = st.selectbox("Interwał:", ["1", "5", "15", "60", "D"], index=2)
    with c4: st.write(""); st.checkbox("Audio", value=True)

    symbol = DB[rynek][inst]
    
    st.subheader(f"📊 Analiza Techniczna Live: {inst}")

    # --- TRZY PANELE ANALIZY ---
    col1, col2 = st.columns([1, 1]) # Dwie główne sekcje analizy dla lepszej czytelności

    with col1:
        st.caption("⏱️ Podsumowanie Sygnałów (Zegar)")
        components.html(create_tv_widget(symbol, itv, mode="single"), height=460)

    with col2:
        st.caption("📈 Szczegóły Wskaźników (Oscylatory i Średnie)")
        components.html(create_tv_widget(symbol, itv, mode="multiple"), height=460)

    # --- GŁÓWNY WYKRES ---
    st.markdown("---")
    st.caption("🕒 Wykres Interaktywny (XTB Feed)")
    chart_html = f"""
    <div id="chart_v42" style="height: 600px;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({{
      "width": "100%", "height": 600,
      "symbol": "{symbol}", "interval": "{itv}",
      "theme": "dark", "style": "1", "locale": "pl",
      "container_id": "chart_v42", "withdateranges": true,
      "hide_side_toolbar": false, "allow_symbol_change": true,
      "save_image": false
    }});
    </script>
    """
    components.html(chart_html, height=620)

if __name__ == "__main__":
    main()
