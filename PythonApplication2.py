import streamlit as st
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

# 1. Konfiguracja strony
st.set_page_config(layout="wide", page_title="XTB TERMINAL V34 PRO", page_icon="📈")
st_autorefresh(interval=60 * 1000, key="data_refresh")

# Stylizacja ramek
st.markdown("""
    <style>
    .block-container { padding: 1rem !important; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    iframe { border-radius: 12px; background: #131722; border: 1px solid #2a2e39; }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza Instrumentów (Mapowanie TradingView)
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
        st.success("### 💎 PREMIUM\nAnalizy na Telegramie:")
        st.markdown("[Dołącz do Grupy](https://t.me/twoj_link)")
        st.markdown("---")
        st.warning("### ☕ WSPARCIE")
        st.markdown("[Postaw kawę](https://buycoffee.to/twoj_nick)")
        st.caption("Wersja: V34 PRO | Independent Sources")

    # --- MENU GŁÓWNE ---
    tab1, tab2, tab3 = st.tabs(["📊 Terminal Analityczny", "📅 Kalendarz Ekonomiczny", "🗺️ Mapa Rynku"])

    with tab1:
        # Panel Wyboru
        c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
        with c1: rynek = st.selectbox("Rynek:", list(DB.keys()), index=0)
        with c2: inst = st.selectbox("Instrument:", list(DB[rynek].keys()), index=0)
        with c3: itv = st.selectbox("Interwał:", ["1", "5", "15", "60", "D"], index=1)
        with c4: audio = st.checkbox("Dźwięk", value=True)

        symbol = DB[rynek][inst]
        tv_interval = f"{itv}" if itv != "D" else "1D"

        st.subheader(f"🛡️ Weryfikacja Dwuźródłowa: {inst}")
        col_sig1, col_sig2 = st.columns(2)

        with col_sig1:
            st.markdown("<p style='text-align:center; color:#83888D;'>Źródło 1: Trading Economics (Niezależne)</p>", unsafe_allow_html=True)
            # Widżet Trading Economics - Niezależne źródło danych i prognoz
            te_symbol = symbol.lower().replace("oanda:", "").replace("tvc:", "")
            tech_te = f"""
            <iframe src="https://it.tradingeconomics.com/embed/?s={te_symbol}&d1=20230101&d2=20261231&h=450&w=100%" 
            width="100%" height="450" frameborder="0" scrolling="no"></iframe>
            """
            components.html(tech_te, height=470)

        with col_sig2:
            st.markdown("<p style='text-align:center; color:#00FFA2;'>Źródło 2: TradingView (Szczegóły Techniczne)</p>", unsafe_allow_html=True)
            # Twój ulubiony widżet "multiple" pokazujący wszystko naraz
            tech_tv2 = f"""
            <div style="height: 450px;">
              <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
              {{
              "interval": "{tv_interval if tv_interval == '1D' else tv_interval+'m'}",
              "width": "100%", "height": 450,
              "isTransparent": true, 
              "symbol": "OANDA:{symbol}" if "{rynek}" == "FOREX" or "{symbol}" == "XAUUSD" else "TVC:{symbol}",
              "showIntervalTabs": true, "displayMode": "multiple",
              "locale": "pl", "colorTheme": "dark"
            }}
              </script>
            </div>
            """
            # Uwaga: w tech_tv2 dodałem logikę dopasowania prefixu OANDA/TVC dla stabilności
            components.html(tech_tv2, height=470)

        # Wykres Główny
        st.markdown("---")
        chart_code = f"""
        <div id="tv_chart_main" style="height: 600px;"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget({{
          "autosize": true, 
          "symbol": "OANDA:{symbol}" if "{rynek}" == "FOREX" or "{symbol}" == "XAUUSD" else "TVC:{symbol}", 
          "interval": "{itv}",
          "theme": "dark", "style": "1",
          "locale": "pl", "container_id": "tv_chart_main"
        }});
        </script>
        """
        components.html(chart_code, height=620)

    with tab2:
        st.subheader("📅 Kalendarz Ekonomiczny (Investing)")
        components.html('<iframe src="https://sslecal2.investing.com?importance=2,3&countries=25,32,6,37,7,5&calType=day&timeZone=58&lang=51" width="100%" height="800" frameborder="0"></iframe>', height=820)

    with tab3:
        st.subheader("🗺️ Mapa Rynku")
        components.html('<iframe src="https://s.tradingview.com/embed-widget/crypto-mcap/?locale=pl#%7B%22colorTheme%22%3A%22dark%22%2C%22width%22%3A%22100%25%22%2C%22height%22%3A%22600%22%7D" width="100%" height="600" frameborder="0"></iframe>', height=620)

    # Logika Audio
    if audio:
        audio_js = """
        <script>
        setInterval(() => {
            if (document.body.innerText.includes('Kupno') || document.body.innerText.includes('Silne kupno')) {
                const ctx = new (window.AudioContext || window.webkitAudioContext)();
                const osc = ctx.createOscillator();
                osc.connect(ctx.destination);
                osc.start(); osc.stop(ctx.currentTime + 0.1);
            }
        }, 30000);
        </script>
        """
        components.html(audio_js, height=0)

if __name__ == "__main__":
    main()
