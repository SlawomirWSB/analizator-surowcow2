import streamlit as st

# 1. Konfiguracja i Stylizacja
st.set_page_config(layout="wide", page_title="XTB HUB V72 - Pro", page_icon="📈")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Przyciski główne - Zawsze białe napisy */
    div.stButton > button {
        color: #ffffff !important;
        background-color: #2a2e39 !important;
        border: 1px solid #3d4451 !important;
        font-weight: bold !important;
        width: 100%;
        margin-bottom: 5px;
    }
    div.stButton > button:hover { border-color: #00ff88 !important; background-color: #3d4451 !important; }

    /* Przyciski Linków po lewej - Stylizacja */
    .stLinkButton > a {
        background-color: #1e222d !important;
        color: #3498db !important;
        border: 1px solid #3498db !important;
        font-size: 0.8rem !important;
        font-weight: normal !important;
        padding: 5px !important;
        text-align: center;
    }

    /* Karty i Agregatory */
    .signal-card {
        background-color: #1e222d;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 5px;
        border-left: 5px solid #3d4451;
    }
    .aggregator-card {
        background-color: #161a25;
        border: 1px solid #2a2e39;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
    }
    
    /* Pasek Podsumowania */
    .gauge-wrapper {
        background: #2a2e39;
        height: 14px;
        border-radius: 7px;
        margin: 15px 0;
        overflow: hidden;
        display: flex;
    }
    .gauge-sell { background: #ff4b4b; height: 100%; }
    .gauge-neutral { background: #f39c12; height: 100%; }
    .gauge-buy { background: #00ff88; height: 100%; }
    
    .mini-gauge {
        text-align: center;
        padding: 10px;
        background: rgba(255,255,255,0.03);
        border-radius: 8px;
        border: 1px solid #2a2e39;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza Danych Multi-Timeframe (10.01.2026)
DB = {
    "GBP/CHF": {
        "updated": "12:20", "type": "SPRZEDAŻ", "color": "#ff4b4b", "link": "https://t.me/s/signalsproviderfx",
        "1D": {"inv": "STRONG SELL", "tv": "SELL", "s": 14, "n": 9, "k": 3},
        "4H": {"inv": "SELL", "tv": "NEUTRAL", "s": 10, "n": 5, "k": 5},
        "1H": {"inv": "NEUTRAL", "tv": "BUY", "s": 6, "n": 8, "k": 8}
    },
    "GBP/AUD": {
        "updated": "12:30", "type": "KUPNO", "color": "#00ff88", "link": "https://t.me/s/signalsproviderfx",
        "1D": {"inv": "BUY", "tv": "STRONG BUY", "s": 1, "n": 1, "k": 12},
        "4H": {"inv": "STRONG BUY", "tv": "STRONG BUY", "s": 0, "n": 0, "k": 15},
        "1H": {"inv": "BUY", "tv": "BUY", "s": 2, "n": 2, "k": 8}
    },
    "CAD/JPY": {
        "updated": "06:47", "type": "KUPNO", "color": "#00ff88", "link": "https://t.me/s/prosignalsfxx",
        "1D": {"inv": "STRONG BUY", "tv": "BUY", "s": 2, "n": 3, "k": 14},
        "4H": {"inv": "BUY", "tv": "BUY", "s": 5, "n": 5, "k": 10},
        "1H": {"inv": "NEUTRAL", "tv": "NEUTRAL", "s": 8, "n": 8, "k": 4}
    }
}

def render_mini_gauge(title, verdict, color):
    st.markdown(f"""
        <div class="mini-gauge">
            <small style="color:#b2b5be;">{title}</small>
            <div style="color:{color}; font-weight:bold; font-size:1.1rem; margin-top:5px;">{verdict}</div>
            <div style="height:3px; background:#2a2e39; margin-top:8px; border-radius:2px;">
                <div style="width:70%; height:100%; background:{color}; border-radius:2px;"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def main():
    st.markdown('<h2 style="text-align:center;">Terminal V72 - Pełna Kontrola</h2>', unsafe_allow_html=True)

    # Globalny wybór interwału
    global_tf = st.select_slider("Interwał systemowy (Investing/TV):", options=["1H", "4H", "1D"], value="1D")

    if 'active' not in st.session_state: st.session_state.active = "GBP/CHF"
    col_l, col_r = st.columns([1, 1.4])

    # --- PANEL LEWY: LISTA + LINKI ---
    with col_l:
        st.subheader("📩 Aktywne Sygnały")
        for pair, info in DB.items():
            st.markdown(f"""
                <div class="signal-card" style="border-left-color: {info['color']}">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-size:1.3rem; font-weight:bold;">{pair}</span>
                        <span style="background:{info['color']}; color:white; padding:2px 10px; border-radius:5px; font-weight:bold;">{info['type']}</span>
                    </div>
                    <small style="color:#b2b5be;">🕒 {info['updated']} | {global_tf}</small>
                </div>
            """, unsafe_allow_html=True)
            
            # Przycisk weryfikacji
            if st.button(f"Weryfikuj {pair}", key=f"v_{pair}"):
                st.session_state.active = pair
                st.rerun()
            
            # NOWOŚĆ: Link pod każdą pozycją
            st.link_button(f"✈️ Otwórz oryginał {pair}", info["link"], use_container_width=True)
            st.markdown("<div style='margin-bottom:20px;'></div>", unsafe_allow_html=True)

    # --- PANEL PRAWY: ANALIZA + ZEGAREK ---
    with col_r:
        item = DB[st.session_state.active]
        data = item[global_tf]
        
        st.subheader(f"📊 Analiza {global_tf}: {st.session_state.active}")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="aggregator-card"><small>Investing.com</small><br><b style="font-size:1.5rem; color:{item["color"]}">{data["inv"]}</b></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="aggregator-card"><small>TradingView Trend</small><br><b style="font-size:1.5rem; color:{item["color"]}">{data["tv"]}</b></div>', unsafe_allow_html=True)

        # PASEK PODSUMOWANIA I ZEGARY
        total = data['s'] + data['n'] + data['k']
        st.markdown(f"""
            <div class="aggregator-card">
                <div style="text-align:center; font-weight:bold; color:#b2b5be;">PODSUMOWANIE ANALITYCZNE ({global_tf})</div>
                <div class="gauge-wrapper">
                    <div class="gauge-sell" style="width: {(data['s']/total)*100}%"></div>
                    <div class="gauge-neutral" style="width: {(data['n']/total)*100}%"></div>
                    <div class="gauge-buy" style="width: {(data['k']/total)*100}%"></div>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:15px; font-size:0.85rem;">
                    <span>Sprzedaż: {data['s']}</span>
                    <span>Neutralnie: {data['n']}</span>
                    <span>Kupno: {data['k']}</span>
                </div>
        """, unsafe_allow_html=True)
        
        # Naprawiona siatka zegarów
        g1, g2, g3 = st.columns(3)
        with g1: render_mini_gauge("Oscylatory", "Sprzedaż" if data['s'] > 10 else "Neutralnie", "#ff4b4b" if data['s'] > 10 else "#f39c12")
        with g2: render_mini_gauge("Podsumowanie", data['tv'], item['color'])
        with g3: render_mini_gauge("Średnie", data['inv'], item['color'])
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Link zbiorczy na dole po prawej również zostawiłem dla wygody
        st.link_button(f"🔗 Pełny raport na Telegramie", item["link"], use_container_width=True)

if __name__ == "__main__": main()
