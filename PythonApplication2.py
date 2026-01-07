import streamlit as st
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

# 1. Konfiguracja strony
st.set_page_config(layout="wide", page_title="XTB TERMINAL V34", page_icon="📈")
st_autorefresh(interval=60 * 1000, key="data_refresh")

# Ukrycie zbędnych elementów interfejsu
st.markdown("""
    <style>
    .block-container { padding: 1rem !important; }
    header { visibility: hidden; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    /* Usunięcie marginesów dla komponentów html */
    iframe { display: block; margin: 0 auto; }
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
    # --- SIDEBAR: TYLKO REKOMENDACJA I WSPARCIE ---
    with st.sidebar:
        st.title("💰 TERMINAL TRADERA")
        
        # Sekcja Afiliacyjna
        st.info("### 🚀 REKOMENDACJA\nHandluj na XTB bez prowizji! Załóż konto z linku poniżej:")
        st.markdown("[👉 Otwórz Darmowe Konto](https://www.twoj-link-afiliacyjny.pl)")
        
        st.markdown("---")
        
        # Sekcja Donacji
        st.warning("### ☕ WSPARCIE\nPomogłem? Możesz postawić mi symboliczną kawę!")
        st.markdown("[Postaw kawę (BuyCoffee)](https://buycoffee.to/twoj_nick)")
        
        st.markdown("---")
        st.caption("Wersja: V34 Professional")

    # --- PANEL GŁÓWNY ---
    c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
    with c1: rynek = st.selectbox("Rynek:", list(DB.keys()), index=0)
    with c2: inst = st.selectbox("Instrument:", list(DB[rynek].keys()), index=0)
    with c3: itv = st.selectbox("Interwał:", ["1", "5", "15", "60", "D"], index=1)
    with c4: audio = st.checkbox("Dźwięk", value=True)

    symbol = DB[rynek][inst]

    # --- WIDGET ANALIZY (Zwiększona wysokość, by nie zasłaniać liczb) ---
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
    # Zwiększyliśmy height z 390 na 470, aby zmieściły się liczby pod zegarem
    components.html(tech_code, height=470)

    # --- WYKRES GŁÓWNY ---
    chart_code = f"""
    <div id="tv_chart_main" style="height: 600px;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({{
      "autosize": true,
      "symbol": "{symbol}",
      "interval": "{itv}",
      "timezone": "Europe/Warsaw",
      "theme": "dark",
      "style": "1",
      "locale": "pl",
      "enable_publishing": false,
      "hide_side_toolbar": false,
      "allow_symbol_change": true,
      "container_id": "tv_chart_main",
      "studies": [
        "RSI@tv-basicstudies",
        "EMA@tv-basicstudies"
      ]
    }});
    </script>
    """
    components.html(chart_code, height=620)

    # Stopka
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: gray; font-size: 0.8rem;'>OSTRZEŻENIE O RYZYKU: Kontrakty CFD wiążą się z wysokim ryzykiem utraty kapitału.</p>", unsafe_allow_html=True)

    # Obsługa Audio
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
