import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf

# Ustawienia strony
st.set_page_config(page_title="Skaner Krypto XTB", layout="wide")

# Lista kryptowalut dostępnych w XTB (mapowanie na symbole Yahoo Finance)
KRYPTO_XTB = [
    "BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "ADA-USD", "DOT-USD", 
    "LINK-USD", "LTC-USD", "MATIC-USD", "SHIB-USD", "AVAX-USD", "BCH-USD",
    "ALGO-USD", "UNI-USD", "NEAR-USD", "ATOM-USD", "ICP-USD", "XLM-USD",
    "ETC-USD", "FIL-USD", "SAND-USD", "MANA-USD", "AAVE-USD", "EOS-USD"
]

# Mapowanie interwałów dla yfinance
interval_map = {
    "1 min": "1m", "5 min": "5m", "15 min": "15m", "30 min": "30m",
    "1 godz": "1h", "4 godz": "1h", "1 dzień": "1d", "1 tydz": "1wk", "1 mies": "1mo"
}

def fetch_and_analyze(symbol, timeframe):
    try:
        # Dobór okresu pobierania danych
        period = "1d" if "min" in timeframe else "1y"
        if timeframe == "1 godz" or timeframe == "4 godz": period = "1mo"
        
        # Pobieranie danych
        df = yf.download(symbol, period=period, interval=interval_map[timeframe], progress=False)
        
        if df.empty or len(df) < 20:
            return None

        # Obliczanie wskaźników technicznych
        df.ta.rsi(length=14, append=True)
        df.ta.ema(length=20, append=True)
        df.ta.ema(length=50, append=True)
        df.ta.macd(append=True)
        df.ta.atr(length=14, append=True)

        last_row = df.iloc[-1]
        close_price = float(last_row['Close'])
        rsi = float(last_row['RSI_14'])
        ema20 = float(last_row['EMA_20'])
        ema50 = float(last_row['EMA_50'])
        atr = float(last_row['ATRr_14'])

        # Logika oceny szansy (Score 0-100%)
        score = 50
        if rsi < 35: score += 20  # Wyprzedanie - szansa na wzrost
        if rsi > 65: score -= 20  # Wykupienie - ryzyko spadku
        if close_price > ema20 > ema50: score += 15  # Trend wzrostowy
        if last_row['MACDh_12_26_9'] > 0: score += 15 # Momentum dodatnie

        # Obliczanie poziomów wejścia
        tp = close_price + (atr * 2.5)
        sl = close_price - (atr * 1.5)

        return {
            "Kryptowaluta": symbol.replace("-USD", ""),
            "Aktualna Cena": round(close_price, 4),
            "Szansa %": int(min(max(score, 0), 100)),
            "RSI": round(rsi, 2),
            "Wejście (Entry)": round(close_price, 4),
            "Take Profit": round(tp, 4),
            "Stop Loss": round(sl, 4)
        }
    except:
        return None

# --- UI INTERFEJS ---
st.title("🔍 Krypto Analizator (Model XTB)")
st.subheader("Automatyczna analiza techniczna dla dostępnych aktywów")

# Kontrolki w jednej linii
col_btn, col_slider = st.columns([1, 2])

with col_slider:
    timeframe = st.select_slider(
        "Wybierz interwał czasowy (Timeframe):",
        options=list(interval_map.keys()),
        value="4 godz"
    )

with col_btn:
    st.write("##") # Margines
    run_analysis = st.button("🚀 ANALIZUJ WSZYSTKIE KRYPTO", use_container_width=True)

if run_analysis:
    results = []
    progress_bar = st.progress(0)
    status_text = st.empty()

    for i, symbol in enumerate(KRYPTO_XTB):
        status_text.text(f"Analizowanie: {symbol}...")
        res = fetch_and_analyze(symbol, timeframe)
        if res:
            results.append(res)
        progress_bar.progress((i + 1) / len(KRYPTO_XTB))

    status_text.success("Analiza zakończona!")
    
    if results:
        df_final = pd.DataFrame(results).sort_values(by="Szansa %", ascending=False)
        
        # Stylizacja tabeli
        def color_score(val):
            color = 'red' if val < 40 else 'orange' if val < 60 else 'green'
            return f'color: {color}; font-weight: bold'

        st.dataframe(
            df_final.style.applymap(color_score, subset=['Szansa %']),
            use_container_width=True,
            height=800
        )
    else:
        st.error("Nie udało się pobrać danych. Spróbuj ponownie za chwilę.")
