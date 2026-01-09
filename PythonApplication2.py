import streamlit as st
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

# 1. Konfiguracja strony
st.set_page_config(layout="wide", page_title="XTB TERMINAL V34 PRO", page_icon="📈")
st_autorefresh(interval=60 * 1000, key="data_refresh")

# Stylizacja: Ukrywanie menu Streamlit i estetyka ramek
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
        st.success("### 💎 PREMIUM\nAnalizy na Telegramie:")
        st.markdown("[Dołącz do Grupy](https://t.me/twoj_link)")
        st.markdown("---")
        st.warning("### ☕ WSPARCIE")
        st.markdown("[Postaw kawę](https://buycoffee.to/twoj_nick)")
        st.caption("Wersja: V34 PRO | Dual-Signal System")

    # --- MENU GŁÓWNE ---
    tab1, tab2, tab3 = st.tabs(["📊 Terminal Analityczny", "📅 Kalendarz Ekonomiczny", "🗺️ Mapa Rynku"])

    with tab1:
        # Panel Wyboru
        c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
        with c1: rynek = st.selectbox("Rynek:", list(DB.keys()), index=0)
        with c2: inst = st.selectbox("Instrument:", list(DB[rynek].keys()), index=0)
        with c3: itv = st.selectbox("Interwał:", ["1", "5", "15", "60", "D"], index=1)
        with c4: audio = st.checkbox("Dźwięk", value=True)

        selected_symbol = DB[rynek][inst]
        tv_interval = f"{itv}" if itv != "D" else "1D"

        st.subheader(f"🤖 Strategia Dual-Signal: {inst}")
        col_sig1, col_sig2 = st.columns(2)

        with col_sig1:
            st.markdown("<p style='text-align:center; color:#FF4B4B;'>Sygnał 1: Agregat Techniczny (Zegar)</p>", unsafe_allow_html=True)
            # Widżet 1: Zegar (Werdykt)
            tech_tv1 = f"""
            <div style="height: 450px;">
              <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
              {{
              "interval": "{tv_interval if tv_interval == '1D' else tv_interval+'m'}",
              "width": "100%", "height": 450,
              "isTransparent": true, 
              "symbol": "{selected_symbol}",
              "showIntervalTabs": false, "displayMode": "single",
              "locale": "pl", "colorTheme": "dark"
            }}
              </script>
            </div>
            """
            components.html(tech_tv1, height=480)

        with col_sig2:
            st.markdown("<p style='text-align:center; color:#00FFA2;'>Sygnał 2: Analiza Wskaźników (Szczegóły)</p>", unsafe_allow_html=True)
            # Widżet 2: Pełna lista techniczna (Inny widok analityczny)
            # Używamy trybu "multiple", który wymusza tabelaryczne zestawienie RSI, MACD itd.
            tech_tv2 = f"""
            <div style="height: 450px;">
              <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
              {{
              "interval": "{tv_interval if tv_interval == '1D' else tv_interval+'m'}",
              "width": "100%", "height": 450,
              "isTransparent": true, 
              "symbol": "{selected_symbol}",
              "showIntervalTabs": true, "displayMode": "multiple",
              "locale": "pl", "colorTheme": "dark"
            }}
              </script>
            </div>
            """
            components.html(tech_tv2, height=480)

        # Wykres Główny
        st.markdown("---")
        chart_code = f"""
        <div id="tv_chart_main" style="height: 600px;"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget({{
          "autosize": true, 
          "symbol": "{selected_symbol}", 
          "interval": "{itv}",
          "theme": "dark", "style": "1",
          "locale": "pl", "container_id": "tv_chart_main",
          "studies": ["RSI@tv-basicstudies", "MACD@tv-basicstudies"]
        }});
        </script>
        """
        components.html(chart_code, height=620)

    # Tab 2 i Tab 3 (Działające i sprawdzone)
    with tab2:
        components.html('<iframe src="https://sslecal2.investing.com?importance=2,3&countries=25,32,6,37,7,5&calType=day&timeZone=58&lang=51" width="100%" height="800" frameborder="0"></iframe>', height=820)
    with tab3:
        components.html('<iframe src="https://s.tradingview.com/embed-widget/crypto-mcap/?locale=pl#%7B%22colorTheme%22%3A%22dark%22%2C%22width%22%3A%22100%25%22%2C%22height%22%3A%22600%22%7D" width="100%" height="600" frameborder="0"></iframe>', height=620)

    # Logika Audio Alertu (pika, gdy pojawi się MOCNE KUPNO)
    if audio:
        audio_js = """
        <script>
        setInterval(() => {
            if (document.body.innerText.includes('Mocne kup') || document.body.innerText.includes('Mocne sprzedaj')) {
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
