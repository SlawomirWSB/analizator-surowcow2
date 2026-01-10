import streamlit as st

# 1. Konfiguracja interfejsu i Stylizacja
st.set_page_config(layout="wide", page_title="XTB HUB V68 - Global Control", page_icon="⚙️")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Poprawa widoczności napisów na przyciskach */
    .stButton > button {
        color: #ffffff !important;
        background-color: #2a2e39 !important;
        border: 1px solid #3d4451 !important;
        font-weight: bold !important;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #3d4451 !important;
        border-color: #00ff88 !important;
    }

    /* Karty sygnałów i agregatorów */
    .signal-card {
        background-color: #1e222d;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        border-left: 5px solid #3d4451;
    }
    .pair-name { font-size: 1.2rem; font-weight: bold; color: #ffffff; }
    
    .aggregator-card {
        background-color: #161a25;
        border: 1px solid #2a2e39;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
    }
    
    .time-selector-box {
        background: #1e222d;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        border: 1px solid #00ff88;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza Danych z danymi dla różnych interwałów
# Symulacja danych: Zmiana global_tf wpłynie na 'verdict' i 'details'
DB = {
    "GBP/CHF": {
        "updated": "12:20", "type": "SPRZEDAŻ", "color": "#ff4b4b",
        "1D": {"inv": "STRONG SELL", "tv": "SELL", "counts": "14 / 9 / 3"},
        "4H": {"inv": "SELL", "tv": "NEUTRAL", "counts": "10 / 5 / 5"},
        "1H": {"inv": "NEUTRAL", "tv": "BUY", "counts": "5 / 10 / 8"}
    },
    "GBP/AUD": {
        "updated": "12:30", "type": "KUPNO", "color": "#00ff88",
        "1D": {"inv": "BUY", "tv": "STRONG BUY", "counts": "12 / 1 / 1"},
        "4H": {"inv": "STRONG BUY", "tv": "STRONG BUY", "counts": "15 / 0 / 0"},
        "1H": {"inv": "BUY", "tv": "BUY", "counts": "8 / 2 / 2"}
    },
    "CAD/JPY": {
        "updated": "06:47", "type": "KUPNO", "color": "#00ff88",
        "1D": {"inv": "STRONG BUY", "tv": "BUY", "counts": "14 / 2 / 0"},
        "4H": {"inv": "BUY", "tv": "BUY", "counts": "11 / 4 / 1"},
        "1H": {"inv": "NEUTRAL", "tv": "SELL", "counts": "3 / 9 / 12"}
    }
}

def main():
    st.markdown('<h2 style="text-align:center;">Terminal V68 - Kontrola Globalna</h2>', unsafe_allow_html=True)

    # GLOBALNY WYBÓR INTERWAŁU (Domyślnie 1 dzień)
    st.markdown('<div class="time-selector-box">', unsafe_allow_html=True)
    global_tf = st.select_slider(
        "Wybierz interwał dla wszystkich analiz:",
        options=["1H", "4H", "1D"],
        value="1D"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if 'active' not in st.session_state: st.session_state.active = "GBP/CHF"

    col_l, col_r = st.columns([1, 1.3])

    with col_l:
        st.subheader("📩 Aktywne Sygnały")
        for pair, info in DB.items():
            st.markdown(f"""
                <div class="signal-card" style="border-left-color: {info['color']}">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span class="pair-name">{pair}</span>
                        <span style="background:{info['color']}; color:white; padding:2px 8px; border-radius:4px; font-size:0.8rem;">{info['type']}</span>
                    </div>
                    <small style="color:#b2b5be;">Aktualizacja: {info['updated']} | Globalny TF: {global_tf}</small>
                </div>
            """, unsafe_allow_html=True)
            # Przycisk z poprawionym kontrastem
            if st.button(f"Weryfikuj {pair}", key=f"btn_{pair}", use_container_width=True):
                st.session_state.active = pair
                st.rerun()

    with col_r:
        item = DB[st.session_state.active]
        data_tf = item[global_tf]
        
        st.subheader(f"📊 Analiza ({global_tf}): {st.session_state.active}")
        
        # PRZYWRÓCONE DWA AGREGATY Z JEDNOLITYM CZASEM
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""<div class="aggregator-card">
                <small style="color:#b2b5be;">Investing.com</small>
                <div style="font-size:1.5rem; font-weight:900; color:{info['color'] if 'BUY' in data_tf['inv'] else '#ff4b4b'}; margin:10px 0;">{data_tf['inv']}</div>
                <small>Interwał: {global_tf}</small>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class="aggregator-card">
                <small style="color:#b2b5be;">TradingView</small>
                <div style="font-size:1.5rem; font-weight:900; color:{info['color'] if 'BUY' in data_tf['tv'] else '#ff4b4b'}; margin:10px 0;">{data_tf['tv']}</div>
                <small>Interwał: {global_tf}</small>
            </div>""", unsafe_allow_html=True)

        # WIDGET ZEGAROWY (Zintegrowany z interwałem)
        st.markdown(f"""
            <div class="aggregator-card" style="text-align:center;">
                <small style="color:#b2b5be;">PODSUMOWANIE ANALITYCZNE ({global_tf})</small>
                <div style="display:flex; justify-content:space-around; margin-top:15px;">
                    <div><small>Sprzedaż</small><br><b>{data_tf['counts'].split('/')[0]}</b></div>
                    <div style="color:#f39c12;"><small>Neutralnie</small><br><b>{data_tf['counts'].split('/')[1]}</b></div>
                    <div style="color:#00ff88;"><small>Kupno</small><br><b>{data_tf['counts'].split('/')[2]}</b></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.info(f"System zsynchronizowany: Wszystkie dane wyświetlane dla interwału {global_tf}")

if __name__ == "__main__": main()
