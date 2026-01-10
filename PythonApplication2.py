import streamlit as st

# 1. Konfiguracja strony i CSS
st.set_page_config(layout="wide", page_title="XTB HUB V70 - Gauge Pro", page_icon="⚖️")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* Przyciski - Naprawa widoczności */
    div.stButton > button {
        color: #ffffff !important;
        background-color: #2a2e39 !important;
        border: 1px solid #3d4451 !important;
        font-weight: bold !important;
    }
    div.stButton > button:hover { border-color: #00ff88 !important; }

    /* Karty */
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
    
    /* Custom Progress Bar (Zamiast licznika) */
    .gauge-wrapper {
        background: #2a2e39;
        height: 12px;
        border-radius: 6px;
        margin: 15px 0;
        overflow: hidden;
        display: flex;
    }
    .gauge-sell { background: #ff4b4b; height: 100%; }
    .gauge-neutral { background: #f39c12; height: 100%; }
    .gauge-buy { background: #00ff88; height: 100%; }
    
    .pair-title { font-size: 1.3rem; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza Danych (Synchronizacja 10.01.2026)
DB = {
    "GBP/CHF": {
        "updated": "12:20", "type": "SPRZEDAŻ", "color": "#ff4b4b",
        "1D": {"inv": "STRONG SELL", "tv": "STRONG SELL", "s": 14, "n": 9, "k": 3},
        "4H": {"inv": "SELL", "tv": "SELL", "s": 10, "n": 5, "k": 5},
        "1H": {"inv": "NEUTRAL", "tv": "SELL", "s": 6, "n": 8, "k": 8}
    },
    "GBP/AUD": {
        "updated": "12:30", "type": "KUPNO", "color": "#00ff88",
        "1D": {"inv": "BUY", "tv": "STRONG BUY", "s": 1, "n": 1, "k": 12},
        "4H": {"inv": "STRONG BUY", "tv": "STRONG BUY", "s": 0, "n": 0, "k": 15},
        "1H": {"inv": "BUY", "tv": "BUY", "s": 2, "n": 2, "k": 8}
    },
    "CAD/JPY": {
        "updated": "06:47", "type": "KUPNO", "color": "#00ff88",
        "1D": {"inv": "STRONG BUY", "tv": "BUY", "s": 2, "n": 3, "k": 14},
        "4H": {"inv": "BUY", "tv": "BUY", "s": 5, "n": 5, "k": 10},
        "1H": {"inv": "NEUTRAL", "tv": "NEUTRAL", "s": 8, "n": 8, "k": 4}
    }
}

def main():
    st.markdown('<h2 style="text-align:center;">Terminal V70 - Gauge View</h2>', unsafe_allow_html=True)

    # Globalny wybór interwału
    global_tf = st.select_slider(
        "Interwał analizy (Domyślnie 1D):",
        options=["1H", "4H", "1D"],
        value="1D"
    )

    if 'active' not in st.session_state: st.session_state.active = "GBP/CHF"
    col_l, col_r = st.columns([1, 1.2])

    with col_l:
        for pair, info in DB.items():
            st.markdown(f"""
                <div class="signal-card" style="border-left-color: {info['color']}">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span class="pair-title">{pair}</span>
                        <span style="background:{info['color']}; color:white; padding:2px 10px; border-radius:5px; font-weight:bold;">{info['type']}</span>
                    </div>
                    <small style="color:#b2b5be;">🕒 {info['updated']} | {global_tf}</small>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Analiza {pair}", key=f"btn_{pair}"):
                st.session_state.active = pair
                st.rerun()

    with col_r:
        item = DB[st.session_state.active]
        data = item[global_tf]
        
        # Agregaty Trendu
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="aggregator-card"><small>Investing.com</small><br><b style="font-size:1.5rem; color:{item["color"]}">{data["inv"]}</b></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="aggregator-card"><small>TradingView Trend</small><br><b style="font-size:1.5rem; color:{item["color"]}">{data["tv"]}</b></div>', unsafe_allow_html=True)

        # WIZUALNY WIDGET (Zamiast licznika)
        total = data['s'] + data['n'] + data['k']
        s_pct = (data['s'] / total) * 100
        n_pct = (data['n'] / total) * 100
        k_pct = (data['k'] / total) * 100

        st.markdown(f"""
            <div class="aggregator-card">
                <div style="text-align:center; font-weight:bold; color:#b2b5be; margin-bottom:10px;">PODSUMOWANIE TECHNICZNE ({global_tf})</div>
                <div class="gauge-wrapper">
                    <div class="gauge-sell" style="width: {s_pct}%"></div>
                    <div class="gauge-neutral" style="width: {n_pct}%"></div>
                    <div class="gauge-buy" style="width: {k_pct}%"></div>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:0.85rem;">
                    <span style="color:#ff4b4b;">Sprzedaż: {data['s']}</span>
                    <span style="color:#f39c12;">Neutralnie: {data['n']}</span>
                    <span style="color:#00ff88;">Kupno: {data['k']}</span>
                </div>
                <div style="margin-top:15px; font-size:0.8rem; color:#8f94a1; border-top:1px solid #2a2e39; padding-top:10px; text-align:center;">
                    Wizualizacja oparta na 26 wskaźnikach technicznych (Oscylatory + Średnie).
                </div>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__": main()
