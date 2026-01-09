import streamlit as st
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

# 1. Konfiguracja strony
st.set_page_config(layout="wide", page_title="XTB TERMINAL V34 PRO", page_icon="📈")
st_autorefresh(interval=60 * 1000, key="data_refresh")

# Stylizacja i ukrywanie zbędnych elementów
st.markdown("""
    <style>
    .block-container { padding: 1rem !important; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    iframe { border-radius: 10px; background: #131722; }
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
    # --- SIDEBAR (Strefa Zarobku) ---
    with st.sidebar:
        st.title("💰 TERMINAL")
        st.info("### 🚀 REKOMENDACJA\nHandluj na XTB bez prowizji! Załóż konto z linku poniżej:")
        # Tu wklej swój link afiliacyjny, gdy go otrzymasz
        st.markdown("[👉 Otwórz Darmowe Konto](https://www.xtb.com/pl)") 
        st.markdown("---")
        st.warning("### ☕ WSPARCIE\nPodoba Ci się terminal? Postaw mi kawę!")
        st.markdown("[Postaw kawę (BuyCoffee)](https://buycoffee.to/twoj_nick)")
        st.markdown("---")
        st.caption("Wersja: V34 PRO | Dane: Multi-Source")

    # --- MENU GŁÓWNE (ZAKŁADKI) ---
    tab1, tab2, tab3 = st.tabs(["📊 Terminal Analityczny", "📅 Kalendarz Ekonomiczny", "🗺️ Mapa Rynku"])

    with tab1:
        # Panel Wyboru
        c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
        with c1: rynek = st.selectbox("Wybierz rynek:", list(DB.keys()), index=0)
        with c2: inst = st.selectbox("Instrument:", list(DB[rynek].keys()), index=0)
        with c3: itv = st.selectbox("Interwał:", ["1", "5", "15", "60", "D"], index=1)
        with c4: audio = st.checkbox("Dźwięk", value=True)

        symbol = DB[rynek][inst]

        # --- DWA ŹRÓDŁA SYGNAŁÓW OBOK SIEBIE ---
        st.subheader("🤖 Analiza Wielu Źródeł")
        col_sig1, col_sig2 = st.columns(2)

        with col_sig1:
            st.markdown("<p style='text-align:center; color:gray;'>Źródło 1: TradingView (Analiza Techniczna)</p>", unsafe_allow_html=True)
            tech_code = f"""
            <div style="display: flex; justify-content: center; background: #131722; padding: 10px; border-radius: 10px;">
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
            components.html(tech_code, height=480)

        with col_sig2:
            st.markdown("<p style='text-align:center; color:gray;'>Źródło 2: Investing.com (Sentyment i Podsumowanie)</p>", unsafe_allow_html=True)
            # Widget Investing.com - Podsumowanie Techniczne
            investing_code = """
            <div style="border-radius: 10px; overflow: hidden;">
              <iframe src="https://it.widgets.investing.com/technical-summary?theme=darkTheme&pairs=1,2,3,5,7,8,9,10" 
              width="100%" height="450" frameborder="0" allowtransparency="true" marginwidth="0" marginheight="0"></iframe>
            </div>
            """
            components.html(investing_code, height=480)

        # Wykres Główny
        st.markdown("---")
        chart_code = f"""
        <div id="tv_chart_main" style="height: 600px;"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget({{
          "autosize": true, "symbol": "{symbol}", "interval": "{itv}",
          "timezone": "Europe/Warsaw", "theme": "dark", "style": "1",
          "locale": "pl", "enable_publishing": false,
          "hide_side_toolbar": false, "allow_symbol_change": true,
          "container_id": "tv_chart_main",
          "studies": ["RSI@tv-basicstudies", "EMA@tv-basicstudies"]
        }});
        </script>
        """
        components.html(chart_code, height=620)

    with tab2:
        st.subheader("📅 Kalendarz Ekonomiczny")
        cal_code = """
        <div style="height: 800px;">
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-events.js" async>
          { "colorTheme": "dark", "isTransparent": true, "width": "100%", "height": "800", "locale": "pl", "importanceFilter": "-1,0,1" }
          </script>
        </div>
        """
        components.html(cal_code, height=820)

    with tab3:
        st.subheader("🗺️ Mapa Cieplna Rynku")
        heatmap_code = """
        <div style="height: 600px;">
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-crypto-coins-heatmap.js" async>
          { "symbolGroups": [ { "name": "Surowce", "symbols": [ { "name": "TVC:GOLD" }, { "name": "TVC:SILVER" }, { "name": "TVC:USOIL" }, { "name": "TVC:NATGAS" } ] } ], 
            "colorTheme": "dark", "isTransparent": true, "width": "100%", "height": "600", "locale": "pl" }
          </script>
        </div>
        """
        components.html(heatmap_code, height=620)

    # Stopka
    st.markdown("---")
    st.caption("🚨 Kontrakty CFD wiążą się z wysokim ryzykiem utraty kapitału. Narzędzie ma charakter wyłącznie edukacyjny.")

    # Logika Audio
    if audio:
        audio_js = """
        <script>
        setInterval(() => {
            if (document.body.innerText.includes('MOCNE KUP') || document.body.innerText.includes('MOCNE SPRZEDAJ')) {
                const ctx = new (window.AudioContext || window.webkitAudioContext)();
                const osc = ctx.createOscillator();
                osc.connect(ctx.destination);
                osc.start(); osc.stop(ctx.currentTime + 0.2);
            }
        }, 30000);
        </script>
        """
        components.html(audio_js, height=0)

if __name__ == "__main__":
    main()
