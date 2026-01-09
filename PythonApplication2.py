import streamlit as st
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

# 1. Konfiguracja strony
st.set_page_config(layout="wide", page_title="XTB TERMINAL V34 PRO", page_icon="📈")
st_autorefresh(interval=60 * 1000, key="data_refresh")

# Stylizacja: Ukrywanie menu Streamlit, zaokrąglanie ramek i kolory
st.markdown("""
    <style>
    .block-container { padding: 1rem !important; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    iframe { border-radius: 12px; background: #131722; border: 1px solid #2a2e39; }
    .stSelectbox label { color: #83888D !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza Instrumentów (Mapowanie nazw na symbole TradingView)
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
    # --- SIDEBAR (Panel boczny) ---
    with st.sidebar:
        st.title("💰 TERMINAL")
        st.info("### 🚀 REKOMENDACJA\nHandluj na XTB bez prowizji! Załóż konto z linku poniżej:")
        st.markdown("[👉 Otwórz Darmowe Konto](https://www.xtb.com/pl)") 
        st.markdown("---")
        
        st.success("### 💎 PREMIUM\nChcesz otrzymywać moje analizy na Telegramie?")
        st.markdown("[Dołącz do Grupy](https://t.me/twoj_link)")
        st.markdown("---")
        
        st.warning("### ☕ WSPARCIE\nPomogłem? Możesz postawić mi symboliczną kawę!")
        st.markdown("[Postaw kawę (BuyCoffee)](https://buycoffee.to/twoj_nick)")
        st.markdown("---")
        st.caption("Wersja: V34 PRO | Dane: Multi-Source")

    # --- MENU GŁÓWNE (ZAKŁADKI) ---
    tab1, tab2, tab3 = st.tabs(["📊 Terminal Analityczny", "📅 Kalendarz Ekonomiczny", "🗺️ Mapa Rynku"])

    with tab1:
        # Panel Wyboru Instrumentu
        c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
        with c1: rynek = st.selectbox("Rynek:", list(DB.keys()), index=0)
        with c2: inst = st.selectbox("Instrument:", list(DB[rynek].keys()), index=0)
        with c3: itv = st.selectbox("Interwał:", ["1", "5", "15", "60", "D"], index=1)
        with c4: audio = st.checkbox("Dźwięk", value=True)

        # Pobranie aktywnego symbolu
        selected_symbol = DB[rynek][inst]

        # --- SEKCJA ANALIZY ---
        st.subheader("🤖 Analiza Wielu Źródeł")
        col_sig1, col_sig2 = st.columns(2)

        with col_sig1:
            st.markdown("<p style='text-align:center; color:#83888D;'>Źródło 1: TradingView (Analiza Techniczna)</p>", unsafe_allow_html=True)
            # Widżet Zegara - Dynamicznie reaguje na wybrany symbol
            tech_tv = f"""
            <div style="height: 450px;">
              <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
              {{
              "interval": "{itv}m" if "{itv}".isdigit() else "1D",
              "width": "100%", "height": 450,
              "isTransparent": true, 
              "symbol": "{selected_symbol}",
              "showIntervalTabs": false, "displayMode": "single",
              "locale": "pl", "colorTheme": "dark"
            }}
              </script>
            </div>
            """
            components.html(tech_tv, height=470)

        with col_sig2:
            st.markdown("<p style='text-align:center; color:#83888D;'>Źródło 2: Investing.com (Kursy Live)</p>", unsafe_allow_html=True)
            # Widżet Investing - Zmodyfikowany na stabilną listę kursów live
            tech_inv = """
            <iframe src="https://www.widgets.investing.com/live-currency-cross-rates?theme=darkTheme&roundedCorners=true&pairs=1,3,2,5,7,9,10" 
            width="100%" height="450" frameborder="0" allowtransparency="true" marginwidth="0" marginheight="0"></iframe>
            """
            components.html(tech_inv, height=470)

        # --- WYKRES GŁÓWNY ---
        st.markdown("---")
        chart_code = f"""
        <div id="tv_chart_main" style="height: 600px;"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget({{
          "autosize": true, 
          "symbol": "{selected_symbol}", 
          "interval": "{itv}",
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
        st.subheader("📅 Kalendarz Wydarzeń Makro")
        cal_code = """
        <iframe src="https://sslecal2.investing.com?columns=exc_flags,exc_currency,exc_importance,exc_actual,exc_forecast,exc_previous&category=_unemployment,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100&importance=1,2,3&features=datepicker,timezone&countries=25,32,6,37,7,5,22,11,10,35,43,56,36&calType=day&timeZone=58&lang=51" 
        width="100%" height="800" frameborder="0" allowtransparency="true"></iframe>
        """
        components.html(cal_code, height=820)

    with tab3:
        st.subheader("🗺️ Mapa Sentymentu Krypto")
        heatmap_code = """
        <iframe src="https://s.tradingview.com/embed-widget/crypto-mcap/?locale=pl#%7B%22colorTheme%22%3A%22dark%22%2C%22width%22%3A%22100%25%22%2C%22height%22%3A%22600%22%2C%22isTransparent%22%3Afalse%7D" 
        width="100%" height="600" frameborder="0"></iframe>
        """
        components.html(heatmap_code, height=620)

    # Ostrzeżenie o ryzyku
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: gray; font-size: 0.8rem;'>OSTRZEŻENIE: Kontrakty CFD są złożonymi instrumentami i wiążą się z wysokim ryzykiem szybkiej utraty pieniędzy z powodu dźwigni finansowej.</p>", unsafe_allow_html=True)

    # Logika Audio Alertów
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
