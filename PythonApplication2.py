import streamlit as st

st.set_page_config(layout="wide", page_title="XTB REAL-TIME SIGNALS")

# Stylizacja
st.markdown("""
    <style>
    .signal-card { background-color: #1e222d; padding: 20px; border-radius: 10px; margin-bottom: 20px; color: white; border-left: 5px solid #ff4b4b; }
    .price-tag { font-size: 24px; font-weight: bold; color: #ffffff; }
    .status-sell { color: #ff4b4b; font-weight: bold; }
    .status-buy { color: #00ff88; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 Agregator Sygnałów: GOLD (Styczeń 2026)")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
        <div class="signal-card">
            <h3>🔴 Źródło: Investing.com (Twój Screen)</h3>
            <p class="price-tag">Cena: 4,500.90</p>
            <p>Werdykt: <span class="status-sell">STRONG SELL</span></p>
            <ul>
                <li>Średnie: Sell (6) / Buy (6) - Neutral</li>
                <li>Wskaźniki: Sell (5) / Buy (2) - Sell</li>
            </ul>
            <small>Data: 2026-01-10</small>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="signal-card" style="border-left: 5px solid #00ff88;">
            <h3>🟢 Źródło: TradingView Zegary (Twój Screen)</h3>
            <p class="price-tag">Cena rynkowa: ~4,501</p>
            <p>Werdykt: <span class="status-buy">KUPNO</span></p>
            <ul>
                <li>Podsumowanie: Kupno (14)</li>
                <li>Średnie kroczące: Silne Kupno (13)</li>
            </ul>
            <small>Data: 2026-01-10</small>
        </div>
    """, unsafe_allow_html=True)

st.warning("⚠️ Uwaga: Masz rozbieżność sygnałów (Investing SELL vs TradingView BUY). W takim przypadku profesjonalni traderzy czekają na ujednolicenie kierunku.")
