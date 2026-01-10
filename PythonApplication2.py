import streamlit as st

# 1. Konfiguracja strony - Mobile Friendly
st.set_page_config(layout="wide", page_title="XTB HUB V64", page_icon="📱")

# 2. Zaawansowana stylizacja CSS (RWD - Responsive Web Design)
st.markdown("""
    <style>
    /* Reset paddingów dla małych ekranów */
    .block-container { padding: 1rem !important; }
    
    /* Karta sygnału po lewej */
    .signal-card {
        background-color: #1e222d;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        border-top: 5px solid #3d4451; /* Grubszy górny pasek dla czytelności na tel */
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    /* Oznaczenia kierunku */
    .badge {
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: bold;
        text-transform: uppercase;
        font-size: 0.9rem;
        display: inline-block;
        margin-bottom: 10px;
    }
    .badge-buy { background-color: #00ff88; color: #000; }
    .badge-sell { background-color: #ff4b4b; color: #fff; }
    
    .update-tag { 
        color: #f39c12; 
        font-size: 0.8rem; 
        display: block; 
        margin-bottom: 5px; 
    }
    
    .price-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
        gap: 10px;
        background: rgba(255,255,255,0.05);
        padding: 10px;
        border-radius: 8px;
        margin: 10px 0;
        font-family: monospace;
    }

    /* Agregator po prawej */
    .aggregator-container {
        background-color: #131722;
        border: 1px solid #2a2e39;
        border-radius: 12px;
        padding: 20px;
        margin-top: 20px;
    }
    
    .verdict-title { font-size: 1.8rem; font-weight: 900; margin: 10px 0; }
    
    /* Przycisk Telegram - Full Width na mobilki */
    .btn-telegram {
        display: block;
        padding: 12px;
        background-color: #0088cc;
        color: white !important;
        text-decoration: none !important;
        border-radius: 8px;
        font-weight: bold;
        text-align: center;
        margin-top: 15px;
    }

    /* Ukrywanie scrollbara dla czystego wyglądu */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-thumb { background: #2a2e39; }
    </style>
    """, unsafe_allow_html=True)

# 3. Aktualna baza danych (10.01.2026)
DATA = {
    "GBP/CHF": {
        "source": "SignalProvider",
        "type": "SPRZEDAŻ",
        "type_en": "SELL",
        "price": "1.073",
        "tp": "1.071",
        "sl": "1.075",
        "updated": "12:20",
        "note": "Testowanie oporu 1.073.",
        "link": "https://t.me/s/signalsproviderfx",
        "investing": {"verdict": "SELL", "color": "#ff4b4b", "summary": "Wskaźniki: Sell (5)"},
        "tradingview": {"verdict": "NEUTRAL", "color": "#8f94a1", "summary": "Zegary: Neutral (7)"}
    },
    "GBP/AUD": {
        "source": "SignalProvider",
        "type": "KUPNO",
        "type_en": "BUY",
        "price": "2.003",
        "tp": "2.007",
        "sl": "1.998",
        "updated": "12:30",
        "note": "Cena wokół struktury 2.003.",
        "link": "https://t.me/s/signalsproviderfx",
        "investing": {"verdict": "BUY", "color": "#00ff88", "summary": "Wskaźniki: Buy (6)"},
        "tradingview": {"verdict": "BUY", "color": "#00ff88", "summary": "Zegary: Kupno (11)"}
    },
    "CAD/JPY": {
        "source": "ProSignalsFx",
        "type": "KUPNO",
        "type_en": "BUY",
        "price": "113.85",
        "tp": "114.50",
        "sl": "113.30",
        "updated": "06:47",
        "note": "Wybicie z formacji trójkąta.",
        "link": "https://t.me/s/prosignalsfxx",
        "investing": {"verdict": "STRONG BUY", "color": "#00ff88", "summary": "Wskaźniki: Buy (8)"},
        "tradingview": {"verdict": "BUY", "color": "#00ff88", "summary": "Zegary: Kupno (12)"}
    }
}

def main():
    st.title("📱 Terminal V64 (10.01.2026)")

    if 'active_pair' not in st.session_state:
        st.session_state.active_pair = "GBP/CHF"

    # Na komputerze dwa panele, na telefonie jeden pod drugim
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader("📩 Sygnały Live")
        for pair, info in DATA.items():
            badge_class = "badge-buy" if info["type_en"] == "BUY" else "badge-sell"
            card_border = "#00ff88" if info["type_en"] == "BUY" else "#ff4b4b"
            
            st.markdown(f"""
                <div class="signal-card" style="border-top-color: {card_border}">
                    <span class="update-tag">🕒 Aktualizacja: {info['updated']}</span>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h3 style="margin:0;">{pair}</h3>
                        <span class="badge {badge_class}">{info['type']}</span>
                    </div>
                    <p style="margin: 5px 0; font-size: 0.9rem; color: #8f94a1;">Źródło: {info['source']}</p>
                    <div class="price-grid">
                        <div><b>IN:</b><br>{info['price']}</div>
                        <div><b>TP:</b><br>{info['tp']}</div>
                        <div><b>SL:</b><br>{info['sl']}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"🔎 Analiza {pair}", key=f"btn_{pair}", use_container_width=True):
                st.session_state.active_pair = pair
                st.rerun()

    with col_right:
        item = DATA[st.session_state.active_pair]
        st.subheader(f"📊 Analiza: {st.session_state.active_pair}")
        
        st.markdown(f"""<div class="aggregator-container">
            <h4 style="margin:0; color:#8f94a1;">Werdykt techniczny</h4>
            <div class="verdict-title" style="color:{item['tradingview']['color']}">{item['tradingview']['verdict']}</div>
            <hr style="border-color: #2a2e39;">
        """, unsafe_allow_html=True)
        
        # Wskaźniki w dwóch kolumnach (na tel. automatycznie się dopasują)
        m_col1, m_col2 = st.columns(2)
        with m_col1:
            st.markdown(f"<small>Investing</small><br><b style='color:{item['investing']['color']}'>{item['investing']['verdict']}</b>", unsafe_allow_html=True)
        with m_col2:
            st.markdown(f"<small>TradingView</small><br><b style='color:{item['tradingview']['color']}'>{item['tradingview']['verdict']}</b>", unsafe_allow_html=True)

        st.markdown(f"""
            <a href="{item['link']}" target="_blank" class="btn-telegram">
                ✈️ Otwórz źródło (Web View)
            </a>
            <div style="margin-top:15px; padding:10px; background:rgba(255,255,255,0.05); border-radius:5px;">
                <small><i>{item['note']}</i></small>
            </div>
        </div>""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
