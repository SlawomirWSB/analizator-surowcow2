import streamlit as st
import pandas as pd
import pandas_ta as ta
import ccxt
from datetime import datetime, timedelta

# --- KONFIGURACJA ---
st.set_page_config(page_title="Skaner PRO V5 - System Ekspercki", layout="wide")

KRYPTO = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "XRP/USDT", "ADA/USDT", "DOT/USDT", "LINK/USDT", "LTC/USDT"]
exchange = ccxt.binance()

def fetch_data(symbol, timeframe):
    try:
        # Pobieramy 200 świec, aby mieć zapas dla wskaźników
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=200)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except Exception as e:
        st.error(f"Błąd pobierania {symbol}: {e}")
        return None

def run_backtest(df, score_threshold=70):
    """Prosty backtest ostatnich 50 świec"""
    capital = 1000.0
    position = 0
    trades = 0
    
    # Symulacja uproszczona na danych historycznych
    for i in range(35, len(df)):
        # Tu kopiujemy logikę sygnału (uproszczoną do Close > EMA)
        ema = df.ta.ema(length=20)[i]
        price = df['Close'][i]
        
        if price > ema and position == 0:
            position = capital / price
            trades += 1
        elif price < ema and position > 0:
            capital = position * price
            position = 0
            
    final_val = capital if position == 0 else position * df['Close'].iloc[-1]
    return round(((final_val - 1000) / 1000) * 100, 2), trades

def przetworz_v5(symbol, timeframe):
    df = fetch_data(symbol, timeframe)
    if df is None or len(df) < 50: return None
    
    # Obliczenia Techniczne
    df.ta.rsi(length=14, append=True)
    df.ta.ema(length=20, append=True)
    df.ta.adx(length=14, append=True)
    df.ta.atr(length=14, append=True)
    df['Vol_Avg'] = df['Volume'].rolling(20).mean()
    
    l = df.iloc[-1]
    prev = df.iloc[-2]
    
    # Logika Sygnału
    cena = l['Close']
    ema20 = l['EMA_20']
    adx = l['ADX_14']
    rsi = l['RSI_14']
    
    # 1. Główny trend
    trend_up = cena > ema20 and ema20 > prev['EMA_20']
    trend_down = cena < ema20 and ema20 < prev['EMA_20']
    
    # 2. Scoring
    score = 30
    if adx > 25: score += 20 # Silny trend
    if (trend_up and rsi < 60) or (trend_down and rsi > 40): score += 20 # Miejsce na ruch
    if l['Volume'] > l['Vol_Avg']: score += 20 # Potwierdzenie wolumenem
    
    sig = "KUP" if trend_up else "SPRZEDAJ" if trend_down else "NEUTRAL"
    if adx < 20: sig = "KONSOLIDACJA" # Filtr trendu bocznego
    
    # Backtest
    profit, num_trades = run_backtest(df)
    
    atr = l['ATRr_14']
    return {
        "Instrument": symbol,
        "Sygnał": sig,
        "Siła %": min(score, 99) if sig != "KONSOLIDACJA" else 0,
        "Cena": round(cena, 4),
        "ADX (Siła)": round(adx, 1),
        "RSI": round(rsi, 1),
        "Est. Profit (hist)": f"{profit}%",
        "TP": round(cena + (atr * 2.5) if trend_up else cena - (atr * 2.5), 4),
        "SL": round(cena - (atr * 1.5) if trend_up else cena + (atr * 1.5), 4)
    }

# --- INTERFEJS ---
st.title("⚖️ Skaner Ekspercki V5")
st.caption("Dane z Binance Real-Time | Filtry trendu ADX | Backtesting Historyczny")

t_frame = st.selectbox("Interwał", ["15m", "1h", "4h", "1d"], index=1)

if st.button("URUCHOM ANALIZĘ MOCY", use_container_width=True):
    results = []
    progress_bar = st.progress(0)
    
    for idx, s in enumerate(KRYPTO):
        res = przetworz_v5(s, t_frame)
        if res: results.append(res)
        progress_bar.progress((idx + 1) / len(KRYPTO))
        
    if results:
        df_res = pd.DataFrame(results).sort_values(by="Siła %", ascending=False)
        
        # Stylizacja
        def color_signal(val):
            if val == "KUP": return 'background-color: #004d00; color: white'
            if val == "SPRZEDAJ": return 'background-color: #4d0000; color: white'
            return ''

        st.dataframe(df_res.style.applymap(color_signal, subset=['Sygnał']), use_container_width=True)
        
        st.info("💡 **Legenda:** 'Est. Profit' pokazuje wynik strategii opartej na EMA20 dla ostatnich 200 świec na tym interwale.")
    else:
        st.warning("Brak danych do wyświetlenia.")
