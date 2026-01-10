import streamlit as st

# 1. Konfiguracja strony i CSS
st.set_page_config(layout="wide", page_title="XTB HUB V69 - Pro Analyzer", page_icon="⚖️")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Naprawa widoczności napisów na przyciskach - zawsze białe */
    div.stButton > button {
        color: #ffffff !important;
        background-color: #2a2e39 !important;
        border: 1px solid #3d4451 !important;
        font-weight: bold !important;
        width: 100%;
        height: 45px;
    }
    div.stButton > button:hover {
        border-color: #00ff88 !important;
        background-color: #3d4451 !important;
    }

    /* Karty i Agregatory */
    .signal-card {
        background-color: #1e222d;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        border-left: 5px solid #3d4451;
    }
    .aggregator-card {
        background-color: #161a25;
        border: 1px solid #2a2e39;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
    }
    
    .pair-title { font-size: 1.3rem; font-weight: bold; color: #ffffff !important; }
    .label-gray { color: #b2b5be; font-size: 0.85rem; text-transform: uppercase; }
    
    /* Stylizacja Slidera */
    .stSlider { padding-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza Danych Multi-Timeframe (Zsynchronizowana z 10.01.2026)
DB = {
    "GBP/CHF": {
        "updated": "12:20", "type": "SPRZEDAŻ", "color": "#ff4b4b", "source": "SignalProvider",
        "1D": {"inv": "STRONG SELL", "tv": "STRONG SELL", "osc": "14/9/3"},
        "4H": {"inv": "SELL", "tv": "SELL", "osc": "10/5/5"},
        "1H": {"inv": "NEUTRAL", "tv": "SELL", "osc": "6/8/8"}
    },
    "GBP/AUD": {
        "updated": "12:30", "type": "KUPNO", "color": "#00ff88", "source": "SignalProvider",
        "1D": {"inv": "BUY", "tv": "STRONG BUY", "osc": "12/1/1"},
        "4H": {"inv": "STRONG BUY", "tv": "STRONG BUY", "osc": "15/0/0"},
        "1H": {"inv": "BUY", "tv": "BUY", "osc": "8/2/2"}
    },
    "CAD/JPY": {
        "updated": "06:47", "type": "KUPNO", "color": "#00ff88", "source": "ProSignalsFx",
        "1D": {"inv": "STRONG BUY", "tv": "BUY", "osc": "2/3/14"},
        "4H": {"inv": "BUY", "tv": "BUY", "osc": "5/5/10"},
        "1H": {"inv": "NEUTRAL", "tv": "NEUTRAL", "osc": "8/8/4"}
    }
}

def main():
    st.markdown('<h2 style="text-align:center; color:white;">Terminal V69 - Multi-Verify</h2>', unsafe_allow_html=True)

    # GLOBALNY WYBÓR INTERWAŁU - Domyślnie 1 Dzień
    st.markdown('<div style="background:#1e222d; padding:10px 30px; border-radius:15px; border:1px solid #3d4451; margin-bottom:25px;">', unsafe_allow_html=True)
    global_tf = st.select_slider(
        "Zmień interwał dla wszystkich analiz (Investing & TradingView):",
        options=["1H", "4H", "1D"],
        value="1D"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if 'active' not in st.session_state:
        st.session_state.active = "GBP/CHF"

    col_left, col_right = st.columns([1, 1.2])

    # --- PANEL LEWY: LISTA ---
    with col_left:
        st.subheader("📩 Sygnały Live")
        for pair, info in DB.items():
            st.markdown(f"""
                <div class="signal-card" style="border-left-color: {info['color']}">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span class="pair-title">{pair}</span>
                        <span style="background:{info['color']}; color:white; padding:2px 10px; border-radius:5px; font-weight:bold;">{info['type']}</span>
                    </div>
                    <div style="margin-top:5px; color:#b2b5be; font-size:0.85rem;">
                        🕒 {info['updated']} | Źródło: {info['source']}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Analiza techniczna {pair}", key=f"btn_{pair}"):
                st.session_state.active = pair
                st.rerun()

    # --- PANEL PRAWY: SZCZEGÓŁY ---
    with col_right:
        item = DB[st.session_state.active]
        data = item[global_tf]
        
        st.subheader(f"📊 Detale ({global_tf}): {st.session_state.active}")
        
        # Dwa główne agregaty (Średnie/Trend)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""<div class="aggregator-card">
                <div class="label-gray">Investing.com</div>
                <div style="font-size:1.6rem; font-weight:900; color:{item['color']}; margin:5px 0;">{data['inv']}</div>
                <small>Interwał: {global_tf}</small>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class="aggregator-card">
                <div class="label-gray">TradingView (Trend)</div>
                <div style="font-size:1.6rem; font-weight:900; color:{item['color']}; margin:5px 0;">{data['tv']}</div>
                <small>Interwał: {global_tf}</small>
            </div>""", unsafe_allow_html=True)

        # Sekcja Oscylatorów (Wyjaśnienie rozbieżności)
        osc_vals = data['osc'].split('/')
        st.markdown(f"""
            <div class="aggregator-card">
                <div class="label-gray" style="text-align:center; margin-bottom:15px;">Licznik Oscylatorów (Pęd Rynku)</div>
                <div style="display:flex; justify-content:space-around; text-align:center;">
                    <div><small>Sprzedaż</small><br><b style="color:#ff4b4b; font-size:1.5rem;">{osc_vals[0]}</b></div>
                    <div><small>Neutralnie</small><br><b style="color:#f39c12; font-size:1.5rem;">{osc_vals[1]}</b></div>
                    <div><small>Kupno</small><br><b style="color:#00ff88; font-size:1.5rem;">{osc_vals[2]}</b></div>
                </div>
                <div style="margin-top:15px; padding:10px; background:rgba(255,255,255,0.05); border-radius:8px; font-size:0.85rem; color:#d1d4dc;">
                    ℹ️ <b>Dlaczego liczby się różnią?</b> Trend główny (powyżej) może być wzrostowy, ale oscylatory (tutaj) pokazują, 
                    czy rynek nie jest już zbyt drogi. Duża liczba 'Sprzedaż' przy trendzie 'Kupno' to sygnał ostrzegawczy!
                </div>
            </div>
        """, unsafe_allow_html=True)

        if int(osc_vals[0]) > 10 and "BUY" in data['tv']:
            st.warning("⚠️ WYKRYTO DYWERGENCJĘ: Silny trend wzrostowy, ale oscylatory sugerują wyprzedanie rynku!")

if __name__ == "__main__":
    main()
