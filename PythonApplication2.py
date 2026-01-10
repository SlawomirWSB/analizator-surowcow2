import streamlit as st

# 1. Konfiguracja i optymalizacja UI
st.set_page_config(layout="wide", page_title="XTB HUB V66", page_icon="📈")

st.markdown("""
    <style>
    /* Globalne poprawki kolorów i kontrastu */
    .stApp { background-color: #0e1117; }
    
    /* Nagłówki */
    .main-title { 
        color: white; 
        font-size: 2rem; 
        font-weight: 800; 
        text-align: center; 
        margin-bottom: 0.5rem; 
    }
    
    /* Sekcja Sygnałów - Jasne napisy na ciemnym tle */
    .signal-card {
        background-color: #1e222d;
        border: 1px solid #2a2e39;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        color: #ffffff !important; /* Wymuszenie białego tekstu */
    }
    
    .pair-name {
        color: #ffffff !important;
        font-size: 1.4rem;
        font-weight: bold;
    }
    
    .badge {
        padding: 4px 12px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 0.9rem;
    }
    .badge-buy { background-color: #00ff88; color: #000000; }
    .badge-sell { background-color: #ff4b4b; color: #ffffff; }

    /* Podwójny Agregator - Wyraźny kontrast */
    .aggregator-box {
        background-color: #161a25;
        border: 1px solid #363c4e;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
    }
    
    .source-label { color: #b2b5be; font-size: 0.85rem; text-transform: uppercase; }
    .verdict-text { font-size: 1.8rem; font-weight: 900; margin: 10px 0; }
    
    .price-details {
        display: flex;
        justify-content: space-between;
        background: #2a2e39;
        padding: 12px;
        border-radius: 8px;
        margin-top: 15px;
        color: #d1d4dc;
        font-family: 'Courier New', monospace;
    }

    /* Responsywność dla telefonów */
    @media (max-width: 600px) {
        .main-title { font-size: 1.5rem; }
        .pair-name { font-size: 1.1rem; }
        .verdict-text { font-size: 1.4rem; }
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza danych (Zgodna ze screenami 10.01.2026)
DATA = {
    "GBP/CHF": {
        "source": "SignalProvider", "type": "SPRZEDAŻ", "type_en": "SELL",
        "price": "1.073", "tp": "1.071", "sl": "1.075", "updated": "12:20",
        "investing": {"verdict": "STRONG SELL", "color": "#ff4b4b", "summary": "Wskaźniki: Sell (5) / Buy (2)"},
        "tradingview": {"verdict": "NEUTRAL", "color": "#8f94a1", "summary": "Podsumowanie: Neutral (7)"},
        "link": "https://t.me/s/signalsproviderfx"
    },
    "GBP/AUD": {
        "source": "SignalProvider", "type": "KUPNO", "type_en": "BUY",
        "price": "2.003", "tp": "2.007", "sl": "1.998", "updated": "12:30",
        "investing": {"verdict": "BUY", "color": "#00ff88", "summary": "Wskaźniki: Buy (6) / Sell (1)"},
        "tradingview": {"verdict": "STRONG BUY", "color": "#00ff88", "summary": "Średnie: Silne Kupno (13)"},
        "link": "https://t.me/s/signalsproviderfx"
    },
    "CAD/JPY": {
        "source": "ProSignalsFx", "type": "KUPNO", "type_en": "BUY",
        "price": "113.85", "tp": "114.50", "sl": "113.30", "updated": "06:47",
        "investing": {"verdict": "STRONG BUY", "color": "#00ff88", "summary": "Wskaźniki: Buy (8)"},
        "tradingview": {"verdict": "BUY", "color": "#00ff88", "summary": "Podsumowanie: Kupno (14)"},
        "link": "https://t.me/s/prosignalsfxx"
    }
}

def main():
    st.markdown('<div class="main-title">Terminal V66</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#b2b5be;">Status: Połączono z Agregatorami (10.01.2026)</p>', unsafe_allow_html=True)

    if 'active' not in st.session_state:
        st.session_state.active = "GBP/CHF"

    col_signals, col_verify = st.columns([1, 1.2])

    # --- PANEL LEWY: LISTA SYGNAŁÓW ---
    with col_signals:
        st.subheader("📩 Sygnały Live")
        for pair, info in DATA.items():
            b_class = "badge-buy" if info["type_en"] == "BUY" else "badge-sell"
            border_color = "#00ff88" if info["type_en"] == "BUY" else "#ff4b4b"
            
            st.markdown(f"""
                <div class="signal-card" style="border-left: 5px solid {border_color};">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <span style="color:#f39c12; font-size:0.8rem; font-weight:bold;">🕒 {info['updated']}</span>
                            <div class="pair-name">{pair}</div>
                            <span style="color:#b2b5be; font-size:0.85rem;">{info['source']}</span>
                        </div>
                        <span class="badge {b_class}">{info['type']}</span>
                    </div>
                    <div class="price-details">
                        <span>IN: <b>{info['price']}</b></span>
                        <span>TP: <b>{info['tp']}</b></span>
                        <span>SL: <b>{info['sl']}</b></span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"🔎 Analiza Techniczna {pair}", key=f"btn_{pair}", use_container_width=True):
                st.session_state.active = pair
                st.rerun()

    # --- PANEL PRAWY: DUAL-VERIFY AGGREGATOR ---
    with col_verify:
        item = DATA[st.session_state.active]
        st.subheader(f"📊 Weryfikacja: {st.session_state.active}")
        
        # Agregat 1: Investing.com
        st.markdown(f"""
            <div class="aggregator-box">
                <div class="source-label">Investing.com (Wskaźniki)</div>
                <div class="verdict-text" style="color:{item['investing']['color']}">{item['investing']['verdict']}</div>
                <div style="color:#d1d4dc; font-size:0.9rem;">{item['investing']['summary']}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Agregat 2: TradingView
        st.markdown(f"""
            <div class="aggregator-box">
                <div class="source-label">TradingView (Analiza Zbiorcza)</div>
                <div class="verdict-text" style="color:{item['tradingview']['color']}">{item['tradingview']['verdict']}</div>
                <div style="color:#d1d4dc; font-size:0.9rem;">{item['tradingview']['summary']}</div>
            </div>
        """, unsafe_allow_html=True)

        st.link_button(f"✈️ Otwórz źródło na Telegramie", item["link"], use_container_width=True)
        
        # Dynamiczny alert o zgodności
        if (item['type_en'] in item['investing']['verdict']) and (item['type_en'] in item['tradingview']['verdict']):
            st.success(f"✅ Pełna zgodność systemów dla {st.session_state.active}")
        else:
            st.warning(f"⚠️ Uwaga: Rozbieżność wskaźników dla {st.session_state.active}")

if __name__ == "__main__":
    main()
