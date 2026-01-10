import streamlit as st
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

# 1. Konfiguracja strony
st.set_page_config(layout="wide", page_title="XTB TERMINAL PRO", page_icon="📈")
st_autorefresh(interval=60 * 1000, key="data_refresh")

# Stylizacja ramek i tła
st.markdown("""
    <style>
    .block-container { padding: 1rem !important; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    iframe { border-radius: 12px; background: #131722; border: 1px solid #2a2e39; }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza Instrumentów (Mapowanie dla różnych źródeł)
DB = {
    "SUROWCE": {
        "GOLD (Złoto)": {"tv": "OANDA:XAUUSD", "te": "xauusd:cur"},
        "SILVER (Srebro)": {"tv": "OANDA:XAGUSD", "te": "xagusd:cur"},
        "OIL.WTI (Ropa)": {"tv": "TVC:USOIL", "te": "cl1:com"},
        "NATGAS (Gaz)": {"tv": "TVC:NATGAS", "te": "ng1:com"}
    },
    "INDEKSY": {
        "US100 (Nasdaq)": {"tv": "NASDAQ:IXIC", "te": "ndx:ind"},
        "US500 (S&P500)": {"tv": "TVC:SPX", "te": "spx:ind"},
        "DE30 (DAX)": {"tv": "GLOBALPRIME:GER30", "te": "dax:ind"}
    },
    "FOREX": {
        "EURUSD": {"tv": "FX:EURUSD", "te": "eurusd:cur"},
        "USDPLN": {"tv": "OANDA:USDPLN", "te": "usdpln:cur"},
        "GBPUSD": {"tv": "FX:GBPUSD", "te": "gbpusd:cur"}
    },
    "KRYPTO": {
        "BITCOIN": {"tv": "BINANCE:BTCUSDT", "te": "btcusd:cur"},
        "ETHEREUM": {"tv": "BINANCE:ETHUSDT", "te": "ethusd:cur"}
    }
}

def main():
    # --- SIDEBAR ---
    with st.sidebar:
        st.title("💰 TERMINAL")
        st.info("### 🚀 REKOMENDACJA\nHandluj na XTB bez prowizji!")
        st.markdown("[👉 Otwórz Darmowe Konto](https://www.xtb.com/pl)") 
        st.markdown("---")
        st.caption("Wersja: V35 | Dual-Signal Independence")

    # --- PANEL WYBORU ---
    c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
    with c1: rynek = st.selectbox("Wybierz rynek:", list(DB.keys()))
    with c2: inst = st.selectbox("Instrument:", list(DB[rynek].keys()))
    with c3: itv = st.selectbox("Interwał:", ["1", "5", "15", "60", "D"], index=1)
    with c4: audio = st.checkbox("Dźwięk", value=True)

    tv_symbol = DB[rynek][inst]["tv"]
    te_symbol = DB[rynek][inst]["te"]
    tv_interval = f"{itv}" if itv != "D" else "1D"

    st.subheader(f"🛡️ Porównanie Sygnałów: {inst}")
    
    col_sig1, col_sig2 = st.columns(2)

    with col_sig1:
        # SYGNAŁ 1: TRADING ECONOMICS (Niezależne źródło)
        st.markdown("<p style='text-align:center; color:#5DADE2;'>ŹRÓDŁO 1: TRADING ECONOMICS (Analiza Wskaźnikowa)</p>", unsafe_allow_html=True)
        # Widget Trading Economics pokazuje sentyment i statystyki techniczne
        te_widget = f"""
        <iframe src="https://it.tradingeconomics.com/embed/?s={te_symbol.split(':')[0]}&d1=20240101&h=450&w=100%" 
        width="100%" height="450" frameborder="0" scrolling="no"></iframe>
        """
        components.html(te_widget, height=470)

    with col_sig2:
        # SYGNAŁ 2: TRADING VIEW (Twój ulubiony zegar z detalami)
        st.markdown("<p style='text-align:center; color:#00FFA2;'>ŹRÓDŁO 2: TRADING VIEW (Agregat Techniczny)</p>", unsafe_allow_html=True)
        tech_tv = f"""
        <div style="height: 450px;">
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
          {{
          "interval": "{tv_interval if tv_interval == '1D' else tv_interval+'m'}",
          "width": "100%", "height": 450,
          "isTransparent": true, 
          "symbol": "{tv_symbol}",
          "showIntervalTabs": true, "displayMode": "multiple",
          "locale": "pl", "colorTheme": "dark"
        }}
          </script>
        </div>
        """
        components.html(tech_tv, height=470)

    # --- WYKRES DOLNY (ŚWIECZKI) ---
    st.markdown("---")
    st.markdown(f"**Wykres Interaktywny: {inst}**")
    chart_code = f"""
    <div id="tv_chart_container" style="height: 600px;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({{
      "width": "100%", "height": 600,
      "symbol": "{tv_symbol}", 
      "interval": "{itv}",
      "timezone": "Europe/Warsaw", "theme": "dark", "style": "1",
      "locale": "pl", "toolbar_bg": "#f1f3f6",
      "enable_publishing": false, "hide_side_toolbar": false,
      "allow_symbol_change": true, "container_id": "tv_chart_container"
    }});
    </script>
    """
    components.html(chart_code, height=620)

    # Logika Audio Alertu
    if audio:
        audio_js = """<script>setInterval(() => {if (document.body.innerText.includes('Kupno') || document.body.innerText.includes('Strong Buy')) {const ctx = new AudioContext(); const o = ctx.createOscillator(); o.connect(ctx.destination); o.start(); o.stop(ctx.currentTime + 0.1);}}, 30000);</script>"""
        components.html(audio_js, height=0)

if __name__ == "__main__":
    main()
