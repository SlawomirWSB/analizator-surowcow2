import streamlit as st
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

# 1. Konfiguracja strony
st.set_page_config(layout="wide", page_title="XTB TERMINAL V38", page_icon="📈")
st_autorefresh(interval=60 * 1000, key="data_refresh")

# Stylizacja - poprawka odstępów i wyrównania
st.markdown("""
    <style>
    .block-container { padding: 1rem !important; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    iframe { border-radius: 8px; background: #131722; border: 1px solid #2a2e39; }
    </style>
    """, unsafe_allow_html=True)

# 2. KOMPLETNA BAZA INSTRUMENTÓW (XTB / INVESTING / TV)
DB = {
    "SUROWCE": {
        "GOLD (Złoto)": {"tv": "OANDA:XAUUSD", "inv": "8830"},
        "SILVER (Srebro)": {"tv": "OANDA:XAGUSD", "inv": "8836"},
        "OIL.WTI (Ropa)": {"tv": "TVC:USOIL", "inv": "8849"},
        "NATGAS (Gaz)": {"tv": "TVC:NATGAS", "inv": "8862"},
        "COCOA (Kakao)": {"tv": "ICEUS:CC1!", "inv": "8894"},
        "COFFEE (Kawa)": {"tv": "ICEUS:KC1!", "inv": "8832"},
        "SUGAR (Cukier)": {"tv": "ICEUS:SB1!", "inv": "8869"},
        "COPPER (Miedź)": {"tv": "COMEX:HG1!", "inv": "8831"},
        "PLATINUM (Platyna)": {"tv": "NYMEX:PL1!", "inv": "8831"},
        "ALUMINUM (Aluminium)": {"tv": "LME:ALI1!", "inv": "13568"}
    },
    "INDEKSY": {
        "US100 (Nasdaq)": {"tv": "NASDAQ:NDX", "inv": "14958"},
        "US500 (S&P500)": {"tv": "TVC:SPX", "inv": "166"},
        "DE30 (DAX)": {"tv": "GLOBALPRIME:GER30", "inv": "172"},
        "WIG20 (Polska)": {"tv": "GPW:WIG20", "inv": "10668"},
        "FRA40 (CAC40)": {"tv": "EURONEXT:CAC40", "inv": "167"}
    },
    "FOREX": {
        "EURUSD": {"tv": "FX:EURUSD", "inv": "1"},
        "USDPLN": {"tv": "OANDA:USDPLN", "inv": "40"},
        "EURPLN": {"tv": "OANDA:EURPLN", "inv": "45"},
        "GBPUSD": {"tv": "FX:GBPUSD", "inv": "2"}
    },
    "KRYPTO": {
        "BITCOIN": {"tv": "BINANCE:BTCUSDT", "inv": "945629"},
        "ETHEREUM": {"tv": "BINANCE:ETHUSDT", "inv": "945610"},
        "SOLANA": {"tv": "BINANCE:SOLUSDT", "inv": "1057391"}
    }
}

def main():
    # --- SIDEBAR ---
    with st.sidebar:
        st.title("💰 XTB TERMINAL")
        st.info("### 🚀 REKOMENDACJA\nHandluj na XTB")
        st.markdown("[👉 Otwórz Konto XTB](https://www.xtb.com/pl)") 
        st.markdown("---")
        st.caption("Wersja: V38 | Fixed Cocoa & Width")

    # --- PANEL WYBORU ---
    c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
    with c1: rynek = st.selectbox("Rynek:", list(DB.keys()))
    with c2: inst = st.selectbox("Instrument:", list(DB[rynek].keys()))
    with c3: itv = st.selectbox("Interwał:", ["1", "5", "15", "60", "D"], index=2)
    with c4: audio = st.checkbox("Dźwięk", value=True)

    tv_symbol = DB[rynek][inst]["tv"]
    inv_id = DB[rynek][inst]["inv"]
    tv_interval = f"{itv}" if itv != "D" else "1D"

    st.subheader(f"🛡️ System Dual-Signal: {inst}")
    
    # --- PROPORCJE KOLUMN (Naprawiona szerokość) ---
    col_sig1, col_sig2 = st.columns([1.2, 2.8]) # Lewa kolumna węższa, prawa szersza pod zegary

    with col_sig1:
        st.markdown("<p style='font-size:12px; color:#83888D;'>ŹRÓDŁO 1: INVESTING (Sygnał Techniczny)</p>", unsafe_allow_html=True)
        # Widget Investing (Sygnały Kup/Sprzedaj)
        tech_inv = f"""
        <iframe src="https://ssltsw.investing.com?lang=51&forex={inv_id}&commodities={inv_id}&indices={inv_id}&stocks=&equities=&single_stock={inv_id}&indices_id={inv_id}&quotes_id={inv_id}&stocks_id=&time_frame=900" 
        width="100%" height="480" frameborder="0"></iframe>
        """
        components.html(tech_inv, height=490)

    with col_sig2:
        st.markdown("<p style='font-size:12px; color:#83888D;'>ŹRÓDŁO 2: TRADINGVIEW (Analiza Szczegółowa)</p>", unsafe_allow_html=True)
        # Widget TV (Zegary i Wskaźniki)
        tech_tv = f"""
        <div style="height: 480px;">
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
          {{
          "interval": "{tv_interval if tv_interval == '1D' else tv_interval+'m'}",
          "width": "100%", "height": 480,
          "isTransparent": true, 
          "symbol": "{tv_symbol}",
          "showIntervalTabs": true, "displayMode": "multiple",
          "locale": "pl", "colorTheme": "dark"
        }}
          </script>
        </div>
        """
        components.html(tech_tv, height=490)

    # --- WYKRES DOLNY ---
    st.markdown("---")
    chart_code = f"""
    <div id="tv_chart_main" style="height: 600px;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({{
      "width": "100%", "height": 600,
      "symbol": "{tv_symbol}", 
      "interval": "{itv}",
      "theme": "dark", "style": "1",
      "locale": "pl", "container_id": "tv_chart_main",
      "hide_side_toolbar": false, "allow_symbol_change": true
    }});
    </script>
    """
    components.html(chart_code, height=620)

if __name__ == "__main__":
    main()
