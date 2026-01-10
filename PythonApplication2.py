import streamlit as st

# 1. Konfiguracja i RWD (Responsive Web Design)
st.set_page_config(layout="wide", page_title="XTB HUB V65", page_icon="📱")

st.markdown("""
    <style>
    /* Elastyczne fonty - mniejsze na telefonach */
    html { font-size: 16px; }
    @media (max-width: 600px) {
        html { font-size: 14px; }
        .main-title { font-size: 1.6rem !important; }
        .section-header { font-size: 1.2rem !important; }
    }

    .main-title { font-size: 2.5rem; font-weight: 800; margin-bottom: 0.5rem; text-align: center; }
    
    /* Karta sygnału */
    .signal-card {
        background-color: #1e222d;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        border-top: 4px solid #3d4451;
    }
    
    .badge {
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: bold;
        font-size: 0.8rem;
    }
    .badge-buy { background-color: #00ff88; color: #000; }
    .badge-sell { background-color: #ff4b4b; color: #fff; }

    /* Podwójny Agregator */
    .aggregator-box {
        background-color: #131722;
        border: 1px solid #2a2e39;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 10px;
    }
    .verdict-large { font-size: 1.5rem; font-weight: 900; margin: 5px 0; }
    
    .price-row {
        display: flex;
        justify-content: space-around;
        background: rgba(255,255,255,0.05);
        padding: 8px;
        border-radius: 6px;
        font-family: monospace;
        font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza danych (Stan na 10.01.2026)
DATA = {
    "GBP/CHF": {
        "source": "SignalProvider", "type": "SPRZEDAŻ", "type_en": "SELL",
        "price": "1.073", "tp": "1.071", "sl": "1.075", "updated": "12:20",
        "investing": {"verdict": "STRONG SELL", "color": "#ff4b4b", "details": "Wskaźniki: Sell (5) / Buy (2)"},
        "tradingview": {"verdict": "NEUTRAL", "color": "#8f94a1", "details": "Średnie: Neutral (7)"},
        "link": "https://t.me/s/signalsproviderfx"
    },
    "GBP/AUD": {
        "source": "SignalProvider", "type": "KUPNO", "type_en": "BUY",
        "price": "2.003", "tp": "2.007", "sl": "1.998", "updated": "12:30",
        "investing": {"verdict": "BUY", "color": "#00ff88", "details": "Wskaźniki: Buy (6)"},
        "tradingview": {"verdict": "STRONG BUY", "color": "#00ff88", "details": "Zegary: Silne Kupno (13)"},
        "link": "https://t.me/s/signalsproviderfx"
    },
    "CAD/JPY": {
        "source": "ProSignalsFx", "type": "KUPNO", "type_en": "BUY",
        "price": "113.85", "tp": "114.50", "sl": "113.30", "updated": "06:47",
        "investing": {"verdict": "STRONG BUY", "color": "#00ff88", "details": "Wskaźniki: Buy (8)"},
        "tradingview": {"verdict": "BUY", "color": "#00ff88", "details": "Podsumowanie: Kupno (14)"},
        "link": "https://t.me/s/prosignalsfxx"
    }
}

def main():
    st.markdown('<div class="main-title">Terminal V65</div>', unsafe_allow_html=True)
    st.caption("Aktualizacja: 10.01.2026 | System Dual-Verify")

    if 'active' not in st.session_state: st.session_state.active = "GBP/CHF"

    col_l, col_r = st.columns([1, 1])

    with col_l:
        st.markdown('<div class="section-header">📩 Sygnały Live</div>', unsafe_allow_html=True)
        for pair, info in DATA.items():
            b_class = "badge-buy" if info["type_en"] == "BUY" else "badge-sell"
            st.markdown(f"""
                <div class="signal-card" style="border-top-color:{'#00ff88' if info['type_en']=='BUY' else '#ff4b4b'}">
                    <small style="color:#f39c12">🕒 {info['updated']}</small>
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <b style="font-size:1.1rem">{pair}</b>
                        <span class="badge {b_class}">{info['type']}</span>
                    </div>
                    <div class="price-row" style="margin-top:8px;">
                        <span>IN: {info['price']}</span><span>TP: {info['tp']}</span><span>SL: {info['sl']}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"Sprawdź {pair}", key=f"btn_{pair}", use_container_width=True):
                st.session_state.active = pair
                st.rerun()

    with col_r:
        item = DATA[st.session_state.active]
        st.markdown(f'<div class="section-header">📊 Agregator: {st.session_state.active}</div>', unsafe_allow_html=True)
        
        # PRZYWRÓCONY PODWÓJNY AGREGAT (Investing + TradingView)
        st.markdown(f"""
            <div class="aggregator-box" style="border-left: 5px solid #ff4b4b;">
                <small style="color:#8f94a1;">Źródło: Investing.com</small>
                <div class="verdict-large" style="color:{item['investing']['color']}">{item['investing']['verdict']}</div>
                <small>{item['investing']['details']}</small>
            </div>
            <div class="aggregator-box" style="border-left: 5px solid #00ff88;">
                <small style="color:#8f94a1;">Źródło: TradingView Zegary</small>
                <div class="verdict-large" style="color:{item['tradingview']['color']}">{item['tradingview']['verdict']}</div>
                <small>{item['tradingview']['details']}</small>
            </div>
        """, unsafe_allow_html=True)

        st.link_button(f"✈️ Otwórz źródło {item['source']}", item["link"], use_container_width=True)

if __name__ == "__main__": main()
