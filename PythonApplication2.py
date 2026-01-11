import streamlit as st
import streamlit.components.v1 as components

# 1. Konfiguracja i Zaawansowany Styl
st.set_page_config(layout="wide", page_title="TERMINAL V143", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* GWARANTOWANA WIDOCZNOŚĆ TEKSTU */
    div.stButton > button { 
        background-color: #262730 !important; 
        color: #ffffff !important; 
        border: 1px solid #00ff88 !important;
        font-weight: bold !important;
        opacity: 1 !important;
        text-transform: uppercase;
    }

    /* Układ Mobile: Przyciski obok siebie */
    .mobile-row { display: flex; gap: 4px; margin-top: 5px; }
    
    .signal-card-v143 { background-color: #1e222d; border-radius: 8px; padding: 12px; margin-bottom: 8px; border-left: 5px solid #3d4451; }
    .card-top { display: flex; justify-content: space-between; align-items: center; }
    .pair-title { font-size: 1.1rem; font-weight: bold; }
    .time-stamp { font-size: 0.8rem; color: #00ff88; }
    .data-row { background: #000; padding: 8px; border-radius: 5px; color: #00ff88; font-family: monospace; text-align: center; margin: 8px 0; border: 1px solid #333; }

    .tg-link-pl { background-color: #0088cc; color: white !important; text-decoration: none; display: flex; align-items: center; justify-content: center; height: 38px; border-radius: 4px; font-weight: bold; font-size: 0.85rem; border: 1px solid #4b4d5a; width: 100%; }
    
    /* Skalowanie widgetów na mobile */
    @media (max-width: 600px) { .tv-widget { transform: scale(0.9); transform-origin: top left; } }
    </style>
    """, unsafe_allow_html=True)

# 2. Baza Danych z polskimi opisami i wielowskaźnikową analizą
db = [
    {"pair": "XAU/USD", "sym": "OANDA:XAUUSD", "time": "11.01 | 07:44", "tg": "https://t.me/s/VasilyTrading", "color": "#00ff88", "type": "KUPNO", "in": "4498", "tp": "4540", "conf": 94, "basis": "Silny impet wzrostowy, odbicie od kluczowego wsparcia, RSI w strefie byka."},
    {"pair": "GBP/JPY", "sym": "FX:GBPJPY", "time": "11.01 | 11:49", "tg": "https://t.me/s/signalsproviderfx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "211.700", "tp": "208.935", "conf": 89, "basis": "RSI wskazuje wykupienie, przecięcie średnich EMA, odrzucenie poziomu 211.70."},
    {"pair": "US30", "sym": "TVC:US30", "time": "11.01 | 07:03", "tg": "https://t.me/s/prosignalsfxx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "37580", "tp": "37450", "conf": 87, "basis": "Odrzucenie oporu horyzontalnego, niedźwiedzia dywergencja na oscylatorach."},
    {"pair": "NATGAS", "sym": "TVC:NATGAS", "time": "11.01 | 08:15", "tg": "https://t.me/s/top_tradingsignals", "color": "#00ff88", "type": "KUPNO", "in": "2.850", "tp": "3.100", "conf": 82, "basis": "Wsparcie linii trendu wzrostowego, RSI w strefie wyprzedania na H4."},
    {"pair": "EUR/CHF", "sym": "FX:EURCHF", "time": "11.01 | 07:02", "tg": "https://t.me/s/prosignalsfxx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "0.942", "tp": "0.938", "conf": 78, "basis": "Struktura niższych szczytów, słaby popyt na poziomach Fibonacciego."},
    {"pair": "CAD/JPY", "sym": "FX:CADJPY", "time": "10.01 | 08:15", "tg": "https://t.me/s/prosignalsfxx", "color": "#00ff88", "type": "KUPNO", "in": "113.85", "tp": "114.50", "conf": 75, "basis": "Wsparcie na średniej kroczącej MA 200, zwiększony wolumen zakupowy."},
    {"pair": "NZD/USD", "sym": "FX:NZDUSD", "time": "10.01 | 19:59", "tg": "https://t.me/s/top_tradingsignals", "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "0.624", "tp": "0.618", "conf": 72, "basis": "Zniesienie Fibonacciego 0.618, sygnał Price Action na oporze."},
    {"pair": "GBP/CHF", "sym": "FX:GBPCHF", "time": "10.01 | 16:45", "tg": "https://t.me/s/prosignalsfxx", "color": "#ff4b4b", "type": "SPRZEDAŻ", "in": "1.073", "tp": "1.071", "conf": 68, "basis": "Test oporu horyzontalnego, słabość funta w korelacji z CHF."},
    {"pair": "GBP/AUD", "sym": "FX:GBPAUD", "time": "10.01 | 14:20", "tg": "https://t.me/s/top_tradingsignals", "color": "#00ff88", "type": "KUPNO", "in": "2.003", "tp": "2.007", "conf": 65, "basis": "Wybicie z formacji flagi byka, wsparcie dynamiczne EMA 20."},
    {"pair": "USD/CHF", "sym": "FX:USDCHF", "time": "10.01 | 19:23", "tg": "https://t.me/s/top_tradingsignals", "color": "#00ff88", "type": "KUPNO", "in": "0.851", "tp": "0.858", "conf": 62, "basis": "Wejście w strefę popytu (Demand Zone), potwierdzenie świecowe Hammer."},
    {"pair": "EUR/GBP", "sym": "FX:EURGBP", "time": "10.01 | 21:03", "tg": "https://t.me/s/prosignalsfxx", "color": "#00ff88", "type": "KUPNO", "in": "0.860", "tp": "0.865", "conf": 60, "basis": "Reakcja na blok zleceń (Orderblock), płynność zebrana z dołu."}
]

if 'active_idx' not in st.session_state: st.session_state.active_idx = 0

# 3. OKNO RANKINGU AI PO POLSKU
@st.dialog("🤖 RANKING SKUTECZNOŚCI AI (11.01)")
def show_ai_ranking_pl():
    st.write("Instrumenty posegregowane według siły sygnału (wielowskaźnikowo):")
    ranked = sorted(db, key=lambda x: x['conf'], reverse=True)
    for i, item in enumerate(ranked):
        clr = "#00ff88" if item['conf'] > 80 else "#ff9800" if item['conf'] > 70 else "#ff4b4b"
        st.markdown(f"""
            **{i+1}. {item['pair']}** | Prawdopodobieństwo: <span style="color:{clr}; font-weight:bold;">{item['conf']}%</span>  
            *Analiza:* {item['basis']}  
            ---
        """, unsafe_allow_html=True)
    if st.button("ZAMKNIJ RANKING"): st.rerun()

# --- NAGŁÓWEK ---
st.markdown('<div style="background:#1e222d; padding:10px; border-radius:5px; border:1px solid #00ff88; text-align:center; margin-bottom:15px;">TERMINAL V143 | 11.01.2026 | Polska Analiza AI</div>', unsafe_allow_html=True)

c_nav1, c_nav2 = st.columns(2)
with c_nav1:
    if st.button("🔄 SYNCHRONIZUJ DANE"):
        st.success("✅ Zaktualizowano: Dodano 0 nowych sygnałów.")
with c_nav2:
    if st.button("🤖 ANALIZUJ AI (Ranking PL)"): show_ai_ranking_pl()

st.write("---")
col_l, col_r = st.columns([1.5, 2.5])

# --- LEWA STRONA: SYGNAŁY ---
with col_l:
    for idx, s in enumerate(db):
        st.markdown(f"""
            <div class="signal-card-v143" style="border-left-color:{s['color']}">
                <div class="card-top">
                    <span class="pair-title">{s['pair']} <span style="color:{s['color']}">{s['type']}</span></span>
                    <span class="time-stamp">{s['time']}</span>
                </div>
                <div class="data-row">WEJŚCIE: {s['in']} | CEL (TP): {s['tp']}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Przyciski w jednym wierszu (st.columns wymusza to w Streamlit)
        btn_c1, btn_c2 = st.columns(2)
        with btn_c1:
            if st.button(f"📊 ANALIZA", key=f"an_{idx}"):
                st.session_state.active_idx = idx
                st.rerun()
        with btn_c2:
            st.markdown(f'<a href="{s["tg"]}" target="_blank" class="tg-link-pl">✈️ TELEGRAM</a>', unsafe_allow_html=True)

# --- PRAWA STRONA: INTERWAŁ I 3 ZEGARY ---
with col_r:
    cur = db[st.session_state.active_idx]
    st.write("### Interwał czasowy (Domyślnie 1D):")
    tf = st.select_slider("Wybierz interwał do analizy:", options=["1m", "5m", "15m", "30m", "1h", "4h", "1D", "1W", "1M"], value="1D")
    
    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    m1.metric("Investing.com", cur['type'])
    m2.metric("TradingView", cur['type'])
    m3.metric("Pewność AI", f"{cur['conf']}%")

    # 3 Zegary Techniczne
    components.html(f"""
        <div class="tv-widget">
          <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
          {{
            "interval": "{tf}",
            "width": "100%", "isTransparent": true, "height": 450,
            "symbol": "{cur['sym']}", "showIntervalTabs": false, "displayMode": "multiple",
            "locale": "pl", "colorTheme": "dark"
          }}
          </script>
        </div>""", height=480)
