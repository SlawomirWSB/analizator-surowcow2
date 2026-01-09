import streamlit as st
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

# 1. Konfiguracja strony
st.set_page_config(layout="wide", page_title="XTB TERMINAL V34 PRO", page_icon="📈")
st_autorefresh(interval=60 * 1000, key="data_refresh")

# Stylizacja
st.markdown("""
    <style>
    .block-container { padding: 1rem !important; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    iframe { border-radius: 12px; background: #131722; border: 1px solid #2a2e39; }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza Instrumentów (Ujednolicone symbole)
DB = {
    "SUROWCE": {
        "GOLD (Złoto)": "XAUUSD",
        "COCOA (Kakao)": "COCOA",
        "NATGAS (Gaz)": "NATGAS",
        "OIL.WTI (Ropa)": "USOIL",
        "SILVER (Srebro)": "SILVER"
    },
    "INDEKSY": {
        "US100 (Nasdaq)": "IXIC",
        "DE30 (DAX)": "GER30",
        "US500 (S&P500)": "SP500",
        "WIG20 (Polska)": "WIG20"
    },
    "FOREX": {
        "EURUSD": "EURUSD",
        "USDPLN": "USDPLN",
        "EURPLN": "EURPLN"
    },
    "KRYPTO": {
        "BITCOIN": "BTCUSDT",
        "ETHEREUM": "ETHUSDT"
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
        st.caption("Wersja: V34 PRO | Dual-Engine Analysis")

    # --- MENU GŁÓWNE ---
    tab1, tab2, tab3 = st.tabs(["📊 Terminal Analityczny", "📅 Kalendarz Ekonomiczny", "🗺️ Mapa Rynku"])

    with tab1:
        c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
        with c1: rynek = st.selectbox("Rynek:", list(DB.keys()), index=0)
        with c2: inst = st.selectbox("Instrument:", list(DB[rynek].keys()), index=0)
        with c3: itv = st.selectbox("Interwał:", ["1", "5", "15", "60", "D"], index=1)
        with c4: audio = st.checkbox("Dźwięk", value=True)

        # Logika symboli
        symbol = DB[rynek][inst]
        full_symbol = f"OANDA:{symbol}" if rynek in ["FOREX", "SUROWCE"] else f"TVC:{symbol}"
        if rynek == "KRYPTO": full_symbol = f"BINANCE:{symbol}"
        
        tv_interval = f"{itv}" if itv != "D" else "1D"

        st.subheader(f"🛡️ Strategia Dual-Signal dla {inst}")
        col_sig1, col_sig2 = st.columns(2)

        with col_sig1:
            st.markdown("<p style='text-align:center; color:#83888D;'>Sygnał 1: Trend i Dynamika Ceny</p>", unsafe_allow_html=True)
            # Widżet 1: Mini Chart (Inne źródło wizualne sygnału)
            tech_mini = f"""
            <div style="height: 450px;">
              <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-mini-symbol-overview.js" async>
              {{
              "symbol": "{full_symbol}",
              "width": "100%", "height": 450,
              "locale": "pl", "dateRange": "12M",
              "colorTheme": "dark", "isTransparent": true,
              "autosize": false, "largeChartUrl": ""
              }}
              </script>
            </div>
            """
            components.html(tech_mini, height=470)

        with col_sig2:
            st.markdown("<p style='text-align:center; color:#00FFA2;'>Sygnał 2: Szczegółowa Analiza Techniczna</p>", unsafe_allow_html=True)
            # Widżet 2: Ten, który Ci się podobał (Multiple) - TERAZ DYNAMICZNY
            tech_tv_main = f"""
            <div style="height: 450px;">
              <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
              {{
              "interval": "{tv_interval if tv_interval == '1D' else tv_interval+'m'}",
              "width": "100%", "height": 450,
              "isTransparent": true, 
              "symbol": "{full_symbol}",
              "showIntervalTabs": true, "displayMode": "multiple",
              "locale": "pl", "colorTheme": "dark"
            }}
              </script>
            </div>
            """
            components.html(tech_tv_main, height=470)

        # --- WYKRES NA DOLE (NAPRAWIONY) ---
        st.markdown("---")
        chart_code = f"""
        <div id="tv_chart_container" style="height: 600px;"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget({{
          "width": "100%", "height": 600,
          "symbol": "{full_symbol}", 
          "interval": "{itv}",
          "timezone": "Europe/Warsaw", "theme": "dark", "style": "1",
          "locale": "pl", "enable_publishing": false,
          "hide_side_toolbar": false, "allow_symbol_change": true,
          "container_id": "tv_chart_container"
        }});
        </script>
        """
        components.html(chart_code, height=620)

    # Pozostałe zakładki bez zmian
    with tab2:
        components.html('<iframe src="https://sslecal2.investing.com?importance=2,3&countries=25,32,6,37,7,5&calType=day&timeZone=58&lang=51" width="100%" height="800" frameborder="0"></iframe>', height=820)
    with tab3:
        components.html('<iframe src="https://s.tradingview.com/embed-widget/crypto-mcap/?locale=pl#%7B%22colorTheme%22%3A%22dark%22%2C%22width%22%3A%22100%25%22%2C%22height%22%3A%22600%22%7D" width="100%" height="600" frameborder="0"></iframe>', height=620)

    if audio:
        audio_js = """<script>setInterval(() => {if (document.body.innerText.includes('Kupno')) {const ctx = new AudioContext(); const o = ctx.createOscillator(); o.connect(ctx.destination); o.start(); o.stop(ctx.currentTime + 0.1);}}, 30000);</script>"""
        components.html(audio_js, height=0)

if __name__ == "__main__":
    main()
