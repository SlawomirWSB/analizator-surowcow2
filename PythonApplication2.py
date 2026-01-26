import streamlit as st
import pandas as pd
import pandas_ta as ta
import ccxt
import time

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Skaner PRO V5.9 - System Ekspercki", layout="wide")

KRYPTO = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "XRP/USDT", "ADA/USDT", "DOT/USDT", 
          "LINK/USDT", "LTC/USDT", "AVAX/USDT", "MATIC/USDT", "TRX/USDT", "DOGE/USDT"]

interval_map = {
    "5 min": "5m", "15 min": "15m", "30 min": "30m", "1 godz": "1h", 
    "4 godz": "4h", "1 dzień": "1d", "1 tydz": "1w"
}

@st.cache_data(ttl=300)
def pobierz_dane_stabilne(interwal_label):
    ex = ccxt.binanceus() 
    all_data = {}
    tf = interval_map[interwal_label]
    for sym in KRYPTO:
        try:
            ohlcv = ex.fetch_ohlcv(sym, timeframe=tf, limit=200)
            df = pd.DataFrame(ohlcv, columns=['time', 'Open', 'High', 'Low', 'Close', 'Volume'])
            df['time'] = pd.to_datetime(df['time'], unit='ms')
            all_data[sym] = df.set_index('time')
            time.sleep(0.05) 
        except: continue
    return all_data

def run_backtest(df):
    if len(df) < 70: return 0.0
    test_data = df.tail(100).copy()
    test_data['EMA'] = ta.ema(test_data['Close'], length=20)
    cap, pos = 1000.0, 0.0
    for i in range(50, len(test_data)):
        p, e = test_data['Close'].iloc[i], test_data['EMA'].iloc[i]
        if p > e and pos == 0: pos = cap / p
        elif p < e and pos > 0: cap, pos = pos * p, 0.0
    final = cap if pos == 0 else pos * test_data['Close'].iloc[-1]
    return round(((final - 1000) / 1000) * 100, 2)

def przetworz_v5_9(data, tryb, kapital):
    wyniki = []
    for sym, df in data.items():
        try:
            df.ta.rsi(length=14, append=True)
            df.ta.ema(length=20, append=True)
            df.ta.adx(length=14, append=True)
            df.ta.atr(length=14, append=True)
            df.ta.macd(append=True)
            df.ta.stochrsi(length=14, append=True)
            df['Vol_Avg'] = df['Volume'].rolling(20).mean()
            
            l = df.iloc[-1]
            c, e, a, r, atr = float(l['Close']), float(l['EMA_20']), float(l['ADX_14']), float(l['RSI_14']), float(l['ATRr_14'])
            macd_h = float(l['MACDh_12_26_9'])
            stoch_k = float(l['STOCHRSIk_14_14_3_3'])
            vol_ratio = float(l['Volume'] / l['Vol_Avg']) if l['Vol_Avg'] > 0 else 1.0
            
            sig = "KUP" if c > e else "SPRZEDAJ"
            if a < 20: sig = "KONSOLIDACJA"
            
            sl_dist = atr * 1.5
            sl_price = round(c - sl_dist if sig == "KUP" else c + sl_dist, 4)
            ilosc = (kapital * 0.01) / sl_dist if sl_dist > 0 else 0
            
            wyniki.append({
                "Instrument": sym.replace("/USDT", ""), 
                "Sygnał": sig, 
                "Siła %": min(98, 40 + (20 if a > 25 else 0) + (15 if macd_h > 0 else 0)) if sig != "KONSOLIDACJA" else 0,
                "Cena": round(c, 4), 
                "RSI": round(r, 1), 
                "StochRSI": round(stoch_k, 1),
                "Pęd (MACD)": "Wzrost" if macd_h > 0 else "Spadek",
                "Trend (ADX)": round(a, 1),
                "Ile kupić (1%)": round(ilosc, 4),
                "SL (Stop)": sl_price,
                "Hist. 50ś": f"{run_backtest(df)}%"
            })
        except: continue
    return wyniki

# --- INTERFEJS ---
st.title("⚖️ Skaner PRO V5.9 - Inteligentne Kolory")

with st.sidebar:
    st.header("Zarządzanie Ryzykiem")
    user_kapital = st.number_input("Kapitał (USD):", value=5000, step=100)

wybrany_int = st.select_slider("Interwał:", options=list(interval_map.keys()), value="4 godz")
btn = st.button("🚀 URUCHOM ANALIZĘ", use_container_width=True)

if btn:
    raw_data = pobierz_dane_stabilne(wybrany_int)
    if raw_data:
        res = przetworz_v5_9(raw_data, "rynkowy", user_kapital)
        df_res = pd.DataFrame(res).sort_values(by="Siła %", ascending=False)
        
        def stylizuj(row):
            s = [''] * len(row)
            sig = row['Sygnał']
            stoch = row['StochRSI']
            
            # Kolor Sygnału
            if sig == 'KUP': s[1] = 'background-color: #1e4620; color: white'
            elif sig == 'SPRZEDAJ': s[1] = 'background-color: #5f1a1d; color: white'
            
            # INTELIGENTNY STOCH RSI (Logika Potwierdzenia)
            if sig == 'KUP':
                if stoch < 20: s[5] = 'background-color: #007d00; color: white' # POTWIERDZENIE (Kupuj dołek)
                elif stoch > 80: s[5] = 'background-color: #7d0000; color: white' # OSTRZEŻENIE (Kupujesz górkę)
            elif sig == 'SPRZEDAJ':
                if stoch > 80: s[5] = 'background-color: #007d00; color: white' # POTWIERDZENIE (Shortuj górkę)
                elif stoch < 20: s[5] = 'background-color: #7d0000; color: white' # OSTRZEŻENIE (Shortujesz dołek)
            
            # Pęd i Trend
            s[6] = 'color: #00ff00' if row['Pęd (MACD)'] == 'Wzrost' else 'color: #ff4b4b'
            s[7] = 'color: #00ff00; font-weight: bold' if row['Trend (ADX)'] > 25 else 'color: #ff4b4b'
            
            # Historia
            v_h = float(row['Hist. 50ś'].replace('%',''))
            s[10] = 'color: #00ff00' if v_h > 0 else 'color: #ff4b4b' if v_h < 0 else ''
            return s
            
        st.dataframe(df_res.style.apply(stylizuj, axis=1), use_container_width=True)
        st.info("Legenda StochRSI: ZIELONY = Sygnał potwierdzony przez oscylator. CZERWONY = Ryzykowne wejście (przegrzanie/wyprzedanie).")
