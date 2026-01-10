import streamlit as st
import streamlit.components.v1 as components

# 1. Konfiguracja interfejsu
st.set_page_config(layout="wide", page_title="XTB HUB V82", page_icon="📈")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Przyciski - wysoka widoczność */
    div.stButton > button {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #00ff88 !important;
        font-weight: 900 !important;
        width: 100%;
    }

    .signal-card {
        background-color: #1e222d;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 5px;
        border-left: 5px solid #3d4451;
    }

    .data-row {
        background: #000000;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        font-family: 'Courier New', monospace;
        color: #00ff88;
        font-weight: bold;
        border: 1px solid #333;
    }

    .agg-box {
        background-color: #161a25;
        border: 1px solid #2a2e39;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza danych (Pełne dane z V63/V64)
DB = {
    "GBP/CHF": {"in": "1.073", "tp": "1.071", "sl": "1.075", "upd": "12:20", "type": "SPRZEDAŻ", "color": "#ff4b4b", "sym": "FX_IDC:GBPCHF", "inv": "STRONG SELL", "tv": "SELL"},
    "GBP/AUD": {"in": "2.003", "tp": "2.007", "sl": "1.998", "upd": "12:30", "type": "KUPNO", "color": "#00ff88", "sym": "FX:GBPAUD", "inv": "BUY", "tv": "STRONG BUY"},
    "CAD/JPY": {"in": "113.85", "tp": "114.50", "sl": "113.30", "upd": "06:47", "type": "KUPNO", "color": "#00ff88", "sym": "FX:CADJPY", "inv": "STRONG BUY", "tv": "BUY"}
}

def main():
    st.markdown("<h2 style='text-align:center;'>Terminal V82 - Final Widget Fix</h2>", unsafe_allow_html=True)
    
    if 'active' not in st.session_state: st.session_state.active = "GBP/CHF"
    col_l, col_r = st.columns([1, 1.6])
    
    with col_l:
        st.subheader("📩 Sygnały Live")
        for pair, d in DB.items():
            st.markdown(f"""
                <div class="signal-card" style="border-left-color: {d['color']}">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-size:1.2rem; font-weight:bold;">{pair}</span>
                        <span style="background:{d['color']}; color:white; padding:2px 10px; border-radius:4px; font-weight:bold;">{d['type']}</span>
                    </div>
                    <div class="data-row">IN: {d['in']} | TP: {d['tp']} | SL: {d['sl']}</div>
                    <small style="color:#63676a;">🕒 Aktualizacja: {d['upd']} | 1D</small>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f" ANALIZA {pair} ", key=f"btn_{pair}"):
                st.session_state.active = pair
            st.link_button(f"✈️ Telegram: {pair}", "https://t.me/s/signalsproviderfx")
            st.write("")

    with col_r:
        sel = st.session_state.active
        st.subheader(f"📊 Pełna Weryfikacja: {sel}")
        
        # Przywrócone dwa agregaty
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="agg-box"><small>Investing.com</small><br><b style="color:{DB[sel]["color"]}; font-size:1.4rem;">{DB[sel]["inv"]}</b></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="agg-box"><small>TradingView Text</small><br><b style="color:{DB[sel]["color"]}; font-size:1.4rem;">{DB[sel]["tv"]}</b></div>', unsafe_allow_html=True)
            
        st.write("")
        
        # OSTATECZNA METODA: Iframe SRC (Najbardziej odporna na blokady)
        # Zmieniłem symbol na format z '_' dla lepszej kompatybilności
        tv_url = f"https://s.tradingview.com/embed-widget/technical-analysis/?locale=pl#%7B%22interval%22%3A%221d%22%2C%22width%22%3A%22100%25%22%2C%22isTransparent%22%3Atrue%2C%22height%22%3A450%2C%22symbol%22%3A%22{DB[sel]['sym']}%22%2C%22showIntervalTabs%22%3Afalse%2C%22displayMode%22%3A%22multiple%22%2C%22colorTheme%22%3A%22dark%22%7D"
        
        st.markdown(f"""
            <iframe src="{tv_url}" width="100%" height="480" frameborder="0" allowtransparency="true" scrolling="no" style="border-radius: 8px;"></iframe>
        """, unsafe_allow_html=True)
        
        st.caption("Oryginalne zegary TV ładowane natywną ramką.")

if __name__ == "__main__": main()
