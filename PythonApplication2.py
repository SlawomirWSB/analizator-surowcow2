import streamlit as st
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

# 1. Konfiguracja strony
st.set_page_config(layout="wide", page_title="XTB TERMINAL V37", page_icon="📈")
st_autorefresh(interval=60 * 1000, key="data_refresh")

# Stylizacja dla idealnego dopasowania ramek
st.markdown("""
    <style>
    .block-container { padding: 1rem !important; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    iframe { border-radius: 8px; background: #131722; border: 1px solid #2a2e39; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# 2. Rozszerzona Baza Instrumentów XTB
DB = {
    "SUROWCE": {
        "GOLD (Złoto)": {"tv": "OANDA:XAUUSD", "inv": "8830"},
        "SILVER (Srebro)": {"tv": "OANDA:XAGUSD", "inv": "8836"},
        "OIL.WTI (Ropa)": {"tv": "TVC:USOIL", "inv": "8849"},
        "NATGAS (Gaz)": {"tv": "TVC:NATGAS", "inv": "8862"},
        "COCOA (Kakao)": {"tv": "PEPPERSTONE:COCOA", "inv": "8894"},
        "COFFEE (Kawa)": {"tv": "ICEUS:KC1!", "inv": "8832"},
        "SUGAR (Cukier)": {"tv": "ICEUS:SB1!", "inv": "8869"},
        "COPPER (Miedź)": {"tv": "COMEX:HG1!", "inv": "8831"},
        "WHEAT (Pszenica)": {"tv": "CBOT:ZW1!", "inv": "8917"}
    },
    "INDEKSY": {
        "US100 (Nasdaq)": {"tv": "NASDAQ:IXIC", "inv": "14958"},
        "US500 (S&P500)": {"tv": "TVC:SPX", "inv": "166"},
        "US30 (Dow Jones)": {"tv": "TVC:DJI", "inv": "169"},
        "DE30 (DAX)": {"tv": "GLOBALPRIME:GER30", "inv": "172"},
        "WIG20 (Polska)": {"tv": "GPW:WIG20", "inv": "10668"},
        "UK100 (FTSE)": {"tv": "INDEX:UKX", "inv": "27"}
    },
    "FOREX": {
        "EURUSD": {"tv": "FX:EURUSD", "inv": "1"},
        "USDPLN": {"tv": "OANDA:USDPLN", "inv": "40"},
        "EURPLN": {"tv": "OANDA:EURPLN", "inv": "45"},
        "GBPUSD": {"tv": "FX:GBPUSD", "inv": "2"},
        "USDJPY": {"tv": "FX:USDJPY", "inv": "3"}
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
        st.info("### 🚀 REKOMENDACJA\nXTB - Najlepszy broker 2026")
        st.markdown("[👉 Otwórz Konto XTB](https://www.xtb.com/pl)") 
        st.markdown("---")
        st.warning("📊 **STATUS**: LIVE")
        st.caption("Wersja: V37 PRO | Full Assets")

    # --- PANEL WYBORU ---
    c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
    with c1: rynek = st.selectbox("Rynek:", list(DB.keys()))
    with c2: inst = st.selectbox("Instrument:", list(DB[rynek].keys()))
    with c3: itv = st.selectbox("Interwał:", ["1", "5", "15", "60", "D"], index=1)
    with c4: audio = st.checkbox("Dźwięk", value=True)

    tv_symbol = DB[rynek][inst]["tv"]
    inv_id = DB[rynek][inst]["inv"]
    tv_interval = f"{itv}" if itv != "D" else "1D"

    st.subheader(f"🛡️ Dual-Analysis System: {inst}")
    
    # --- PROPORCJE KOLUMN (Poprawka szerokości) ---
    col_sig1, col_sig2 = st.columns([1, 2]) # Lewa węższa, prawa szersza

    with col_sig1:
        st.markdown("<p style='font-size:12px; color:#83888D;'>ŹRÓDŁO 1: INVESTING (Sygnał)</p>", unsafe_allow_html=True)
        # Technical Summary Widget - dopasowany do mniejszej kolumny
        tech_inv = f"""
        <iframe src="https://ssltsw.investing.com?lang=51&forex={inv_id}&commodities={inv_id}&indices={inv_id}&stocks=&equities=&single_stock={inv_id}&indices_id={inv_id}&quotes_id={inv_id}&stocks_id=&time_frame=300" 
        width="100%" height="450" frameborder="0"></iframe>
        """
        components.html(tech_inv, height=460)

    with col_sig2:
        st.markdown("<p style='font-size:12px; color:#83888D;'>ŹRÓDŁO 2: TRADINGVIEW (Analiza Techniczna)</p>", unsafe_allow_html=True)
        # Zegar w trybie Multiple - teraz ma więcej miejsca
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
        components.html(tech_tv, height=460)

    # --- WYKRES DOLNY (ŚWIECZKI) ---
    st.markdown("---")
    chart_code = f"""
    <div id="tv_chart_container" style="height: 600px;"></div>
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
    <script type="text/javascript">
    new TradingView.widget({{
      "width": "100%", "height": 600,
      "symbol": "{tv_symbol}", 
      "interval": "{itv}",
      "theme": "dark", "style": "1",
      "locale": "pl", "container_id": "tv_chart_container",
      "withdateranges": true, "hide_side_toolbar": false, "allow_symbol_change": true
    }});
    </script>
    """
    components.html(chart_code, height=620)

    # Powiadomienia dźwiękowe
    if audio:
        audio_js = """<script>setInterval(() => {if (document.body.innerText.includes('Mocne Kupno') || document.body.innerText.includes('STRONG BUY')) {const ctx = new AudioContext(); const o = ctx.createOscillator(); o.connect(ctx.destination); o.start(); o.stop(ctx.currentTime + 0.1);}}, 30000);</script>"""
        components.html(audio_js, height=0)

if __name__ == "__main__":
    main()
