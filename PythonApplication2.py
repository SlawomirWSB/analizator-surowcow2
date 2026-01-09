import streamlit as st
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

# 1. Konfiguracja strony
st.set_page_config(layout="wide", page_title="XTB TERMINAL V34 PRO", page_icon="📈")
st_autorefresh(interval=60 * 1000, key="data_refresh")

# Stylizacja ramek i ukrywanie menu
st.markdown("""
    <style>
    .block-container { padding: 1rem !important; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    iframe { border-radius: 12px; background: #131722; border: 1px solid #2a2e39; }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza Instrumentów
DB = {
    "SUROWCE": {
        "GOLD (Złoto)": "OANDA:XAUUSD",
        "COCOA (Kakao)": "PEPPERSTONE:COCOA",
        "NATGAS (Gaz)": "TVC:NATGAS",
        "OIL.WTI (Ropa)": "TVC:USOIL",
        "SILVER (Srebro)": "TVC:SILVER"
    },
    "INDEKSY": {
        "US100 (Nasdaq)": "NASDAQ:IXIC",
        "DE30 (DAX)": "GLOBALPRIME:GER30",
        "US500 (S&P500)": "VANTAGE:SP500",
        "WIG20 (Polska)": "GPW:WIG20"
    },
    "FOREX": {
        "EURUSD": "FX:EURUSD",
        "USDPLN": "OANDA:USDPLN",
        "EURPLN": "OANDA:EURPLN"
    },
    "KRYPTO": {
        "BITCOIN": "BINANCE:BTCUSDT",
        "ETHEREUM": "BINANCE:ETHUSDT"
    }
}

def main():
    # --- SIDEBAR ---
    with st.sidebar:
        st.title("💰 TERMINAL")
        st.info("### 🚀 REKOMENDACJA\nHandluj na XTB bez prowizji!")
        st.markdown("[👉 Otwórz Darmowe Konto](https://www.xtb.com/pl)") 
        st.markdown("---")
        st.warning("### ☕ WSPARCIE")
        st.markdown("[Postaw kawę](https://buycoffee.to/twoj_nick)")
        st.caption("Wersja: V34 PRO | Multi-Source")

    # --- MENU GŁÓWNE ---
    tab1, tab2, tab3 = st.tabs(["📊 Terminal Analityczny", "📅 Kalendarz Ekonomiczny", "🗺️ Mapa Rynku"])

    with tab1:
        c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
        with c1: rynek = st.selectbox("Rynek:", list(DB.keys()), index=0)
        with c2: inst = st.selectbox("Instrument:", list(DB[rynek].keys()), index=0)
        with c3: itv = st.selectbox("Interwał:", ["1", "5", "15", "60", "D"], index=1)
        with c4: audio = st.checkbox("Dźwięk", value=True)

        symbol = DB[rynek][inst]

        st.subheader("🤖 Analiza Wielu Źródeł")
        col_sig1, col_sig2 = st.columns(2)

        with col_sig1:
            st.markdown("<p style='text-align:center; color:#83888D;'>Źródło 1: TradingView</p>", unsafe_allow_html=True)
            # Zegar TradingView
            tech_tv = f"""
            <div style="height: 450px;">
              <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
              {{
              "interval": "{itv}m" if "{itv}".isdigit() else "1D",
              "width": "100%", "height": 450,
              "isTransparent": true, "symbol": "{symbol}",
              "showIntervalTabs": false, "displayMode": "single",
              "locale": "pl", "colorTheme": "dark"
            }}
              </script>
            </div>
            """
            components.html(tech_tv, height=470)

        with col_sig2:
            st.markdown("<p style='text-align:center; color:#83888D;'>Źródło 2: Investing.com</p>", unsafe_allow_html=True)
            # Stabilny widżet podsumowania od Investing.com
            # Ustawiony na popularne instrumenty, co daje niezależny podgląd
            tech_inv = """
            <iframe src="https://www.widgets.investing.com/top-cryptocurrencies?theme=darkTheme&roundedCorners=true" 
            width="100%" height="450" frameborder="0" allowtransparency="true" marginwidth="0" marginheight="0"></iframe>
            """
            components.html(tech_inv, height=470)

        # Wykres
        st.markdown("---")
        chart_code = f"""
        <div id="tv_chart_main" style="height: 600px;"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget({{
          "autosize": true, "symbol": "{symbol}", "interval": "{itv}",
          "timezone": "Europe/Warsaw", "theme": "dark", "style": "1",
          "locale": "pl", "container_id": "tv_chart_main"
        }});
        </script>
        """
        components.html(chart_code, height=620)

    # ... sekcje tab2 i tab3 zostają bez zmian (Kalendarz i Mapa) ...
    with tab2:
        components.html('<iframe src="https://sslecal2.investing.com?columns=exc_flags,exc_currency,exc_importance,exc_actual,exc_forecast,exc_previous&category=_unemployment,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,255,256,257,258,259,260,261,262,263,264,265,266,267,268,269,270,271,272,273,274,275,276,277,278,279,280,281,282,283,284,285,286,287,288,289,290,291,292,293,294,295,296,297,298,299,300,301,302,303,304,305,306,307,308,309,310,311,312,313,314,315,316,317,318,319,320,321,322,323,324,325,326,327,328,329,330,331,332,333,334,335,336,337,338,339,340,341,342,343,344,345,346,347,348,349,350,351,352,353,354,355,356,357,358,359,360,361,362,363,364,365,366,367,368,369,370,371,372,373,374,375,376,377,378,379,380,381,382,383,384,385,386,387,388,389,390,391,392,393,394,395,396,397,398,399,400&importance=1,2,3&features=datepicker,timezone&countries=25,32,6,37,7,5,22,11,10,35,43,56,36,110,11,26,12,4,12,46,14,12,38,12,17,39,12,12&calType=day&timeZone=58&lang=51" width="100%" height="800" frameborder="0" allowtransparency="true" marginwidth="0" marginheight="0"></iframe>', height=820)

    with tab3:
        components.html('<iframe src="https://s.tradingview.com/embed-widget/crypto-mcap/?locale=pl#%7B%22colorTheme%22%3A%22dark%22%2C%22width%22%3A%22100%25%22%2C%22height%22%3A%22600%22%2C%22isTransparent%22%3Afalse%7D" width="100%" height="600" frameborder="0"></iframe>', height=620)

if __name__ == "__main__":
    main()
