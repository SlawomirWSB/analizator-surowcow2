import streamlit as st
import streamlit.components.v1 as components

# 1. Konfiguracja i Stylizacja V83
st.set_page_config(layout="wide", page_title="XTB HUB V83 - Investing Gauges", page_icon="📊")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Przyciski w rzędzie */
    .row-btn {
        display: flex;
        gap: 10px;
        margin-top: 10px;
    }
    
    div.stButton > button {
        background-color: #262730 !important;
        color: #ffffff !important;
        border: 1px solid #4b4d5a !important;
        font-weight: bold !important;
        height: 45px;
    }
    
    .stLinkButton > a {
        background-color: #1e222d !important;
        color: #3498db !important;
        border: 1px solid #3498db !important;
        height: 45px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-decoration: none;
        border-radius: 5px;
        font-weight: bold;
    }

    .signal-card {
        background-color: #1e222d;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        border-left: 5px solid #3d4451;
    }

    .data-row {
        background: #000000;
        padding: 12px;
        border-radius: 6px;
        margin: 10px 0;
        font-family: monospace;
        color: #00ff88;
        font-size: 1.1rem;
        border: 1px solid #333;
        text-align: center;
    }

    .agg-box {
        background-color: #161a25;
        border: 1px solid #2a2e39;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza danych (Pełne dane z V63/V64)
DB = {
    "GBP/CHF": {"in": "1.073", "tp": "1.071", "sl": "1.075", "upd": "12:20", "type": "SPRZEDAŻ", "color": "#ff4b4b", "inv_id": "1", "inv": "STRONG SELL", "tv": "SELL"},
    "GBP/AUD": {"in": "2.003", "tp": "2.007", "sl": "1.998", "upd": "12:30", "type": "KUPNO", "color": "#00ff88", "inv_id": "27", "inv": "BUY", "tv": "STRONG BUY"},
    "CAD/JPY": {"in": "113.85", "tp": "114.50", "sl": "113.30", "upd": "06:47", "type": "KUPNO", "color": "#00ff88", "inv_id": "95", "inv": "STRONG BUY", "tv": "BUY"}
}

def main():
    st.markdown("<h2 style='text-align:center;'>Terminal V83 - Investing.com Integration</h2>", unsafe_allow_html=True)
    
    if 'active' not in st.session_state: st.session_state.active = "GBP/CHF"
    col_l, col_r = st.columns([1.1, 1.4])
    
    with col_l:
        st.subheader("📩 Sygnały")
        for pair, d in DB.items():
            st.markdown(f"""
                <div class="signal-card" style="border-left-color: {d['color']}">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <b style="font-size:1.3rem;">{pair}</b>
                        <span style="background:{d['color']}; color:white; padding:3px 12px; border-radius:5px; font-weight:bold;">{d['type']}</span>
                    </div>
                    <div class="data-row">IN: {d['in']} | TP: {d['tp']} | SL: {d['sl']}</div>
                    <small style="color:#63676a;">🕒 {d['upd']} | Interwał: 1D</small>
                </div>
            """, unsafe_allow_html=True)
            
            # Przyciski obok siebie
            c_btn1, c_btn2 = st.columns(2)
            with c_btn1:
                if st.button(f"📊 ANALIZA", key=f"an_{pair}", use_container_width=True):
                    st.session_state.active = pair
            with c_btn2:
                st.link_button(f"✈️ TELEGRAM", "https://t.me/s/signalsproviderfx", use_container_width=True)
            st.write("---")

    with col_r:
        sel = st.session_state.active
        st.subheader(f"🔍 Analiza Techniczna: {sel}")
        
        # Agregaty tekstowe
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="agg-box"><small>Investing.com</small><br><b style="color:{DB[sel]["color"]}; font-size:1.4rem;">{DB[sel]["inv"]}</b></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="agg-box"><small>TradingView Text</small><br><b style="color:{DB[sel]["color"]}; font-size:1.4rem;">{DB[sel]["tv"]}</b></div>', unsafe_allow_html=True)
            
        st.write("")
        
        # NOWY WIDGET: Zegary Investing.com (Alternatywa dla TradingView)
        # Wykorzystujemy format iframe dla stabilności
        inv_url = f"https://pl.investing.com/currencies/{sel.lower().replace('/', '-')}-technical"
        
        st.info(f"Poniżej powinny załadować się zegary Investing dla {sel}.")
        
        # Próba osadzenia technicznego podsumowania Investing
        components.iframe(f"https://www.widgets.investing.com/live-currency-cross-rates?theme=darkTheme&pairs={DB[sel]['inv_id']}", height=400)
        
        st.markdown(f"""
            <div style="background:#1e222d; padding:10px; border-radius:5px; text-align:center; border:1px dashed #3498db;">
                <a href="{inv_url}" target="_blank" style="color:#3498db; text-decoration:none; font-weight:bold;">
                    🔗 Kliknij tutaj, aby otworzyć pełne zegary Investing.com dla {sel}
                </a>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__": main()
