import streamlit as st
import pandas as pd
import pandas_ta as ta
import ccxt
import time

# --- KONFIGURACJA STRONY ---
st.set_page_config(page_title="Skaner PRO V5.7 - System Ekspercki", layout="wide")

# Lista instrumentów (Binance US dla stabilności na serwerach Streamlit)
KRYPTO = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "XRP/USDT", "ADA/USDT", "DOT/USDT", 
          "LINK/USDT", "LTC/USDT", "AVAX/USDT", "MATIC/USDT", "TRX/USDT", "DOGE/USDT"]

interval_map = {
    "5 min": "5m", "15 min": "15m", "30 min": "30m", "1 godz": "1h", 
    "4 godz": "4h", "1 dzień": "1d", "1 tydz": "1w", "1 mies": "1M"
}

@st.cache_data(ttl=300)
def pobierz_dane_stabilne(interwal_label):
    # Binance US omija błąd 451 (geolokalizacja) na serwerach Streamlit Cloud
    ex = ccxt.binanceus() 
    all_data = {}
    tf = interval_map[interwal_label]
    
    with st.spinner(f'Pobieranie danych dla interwału {interwal_label}...'):
        for sym in KRYPTO:
            try:
                # Pobieramy 200 świec, aby wskaźniki (szczególnie MACD) miały czas się wyliczyć
                ohlcv = ex.fetch_ohlcv(sym, timeframe=tf, limit=200)
                df = pd.DataFrame(ohlcv, columns=['time', 'Open', 'High', 'Low', 'Close', 'Volume'])
                df['time'] = pd.to_datetime(df['time'], unit='ms')
                all_data[sym] = df.set_index('time')
                time.sleep(0.05) 
            except:
                continue
    return all_data

def run_backtest(df):
    if len(df) < 70: return 0.0
    # Symulacja na ostatnich 50 świecach z marginesem na wskaźniki
    test_data = df.tail(100).copy()
    test_data['EMA'] = ta.ema(test_data['Close'], length=20)
    cap, pos = 1000.0, 0.0
    for i in range(50, len(test_data)):
        p, e = test_data['Close'].iloc[i], test_data['EMA'].iloc[i]
        if p > e and pos == 0: pos = cap / p
        elif p < e and pos > 0: cap, pos = pos * p, 0.0
    final = cap if pos == 0 else pos * test_data['Close'].iloc[-1]
    return round(((final - 1000) / 1000) * 100, 2)

def przetworz_v5_7(data, tryb):
    wyniki = []
    for sym, df in data.items():
        try:
            # Obliczenia wskaźników
            df.ta.rsi(length=14, append=True)
            df.ta.ema(length=20, append=True)
            df.ta.adx(length=14, append=True)
            df.ta.atr(length=14, append=True)
            df.ta.macd(fast=12, slow=26, signal=9, append=True)
            df.ta.stochrsi(length=14, append=True)
            
            df['Vol_Avg'] = df['Volume'].rolling(20).mean()
            
            # Pobranie ostatnich wartości
            l = df.iloc[-1]
            c, e, a, r, atr = float(l['Close']), float(l['EMA_20']), float(l['ADX_14']), float(l['RSI_14']), float(l['ATRr_14'])
            macd_h = float(l['MACDh_12_26_9'])
            stoch_k = float(l['STOCHRSIk_14_14_3_3'])
            vol_ratio = float(l['Volume'] / l['Vol_Avg']) if l['Vol_Avg'] > 0 else 1.0
            
            # Logika Sygnału
            sig = "KUP" if c > e else "SPRZEDAJ"
            if a < 20: sig = "KONSOLIDACJA"
            
            pęd = "Wzrostowy" if macd_h > 0 else "Słabnący"
            
            # Zaawansowana punktacja Siły %
            score = 40
            if a > 25: score += 20
            if (sig == "KUP" and r < 50) or (sig == "SPRZEDAJ" and r > 50): score += 10
            if (sig == "KUP" and macd_h > 0) or (sig == "SPRZEDAJ" and macd_h < 0): score += 15
            if (sig == "KUP" and stoch_k < 20) or (sig == "SPRZEDAJ" and stoch_k > 80): score += 10 # Kupuj dołki, sprzedaj górki
            if vol_ratio > 1.1: score += 5
            
            wej = c if tryb == "rynkowy" else e
            wyniki.append({
                "Instrument": sym.replace("/USDT", ""), 
                "Sygnał": sig, 
                "Siła %": min(score, 98) if sig != "KONSOLIDACJA" else 0,
                "Cena Wejścia": round(wej, 4), 
                "RSI": round(r, 1), 
                "StochRSI": round(stoch_k, 1),
                "Pęd (MACD)": pęd,
                "Trend (ADX)": round(a, 1),
                "Wolumen %": round(vol_ratio * 100), 
                "Hist. 50 świec": f"{run_backtest(df)}%",
                "TP (Cel)": round(wej + (atr*2.5) if sig=="KUP" else wej - (atr*2.5), 4),
                "SL (Stop)": round(wej - (atr*1.5) if sig=="KUP" else wej + (atr*1.5), 4)
            })
        except: continue
    return wyniki

# --- INTERFEJS UŻYTKOWNIKA ---
st.title("⚖️ Skaner PRO V5.7 - System Ekspercki")
st.caption("Dane: Binance Real-Time | Wskaźniki: RSI, StochRSI, MACD, ADX | Backtest: Strategia EMA20")

wybrany_int = st.select_slider("Wybierz interwał czasowy:", 
                               options=list(interval_map.keys()), value="4 godz")

c1, c2 = st.columns(2)
with c1: btn_m = st.button("🚀 ANALIZA - CENA RYNKOWA", use_container_width=True)
with c2: btn_s = st.button("💎 ANALIZA - SUGEROWANA (LIMIT/EMA)", use_container_width=True)

if btn_m or btn_s:
    mode = "rynkowy" if btn_m else "sugerowany"
    raw_data = pobierz_dane_stabilne(wybrany_int)
    
    if raw_data:
        res = przetworz_v5_7(raw_data, mode)
        df_res = pd.DataFrame(res).sort_values(by="Siła %", ascending=False)
        
        def stylizuj(row):
            s = [''] * len(row); sig = row['Sygnał']
            # Kolorowanie sygnału
            if sig == 'KUP': s[1] = 'background-color: #1e4620; color: white'
            elif sig == 'SPRZEDAJ': s[1] = 'background-color: #5f1a1d; color: white'
            # RSI
            if sig == 'KUP': s[4] = 'color: #00ff00' if row['RSI'] < 50 else 'color: #ff4b4b'
            elif sig == 'SPRZEDAJ': s[4] = 'color: #00ff00' if row['RSI'] > 50 else 'color: #ff4b4b'
            # StochRSI
            if row['StochRSI'] < 20: s[5] = 'background-color: #004d00; color: white'
            elif row['StochRSI'] > 80: s[5] = 'background-color: #4d0000; color: white'
            # MACD
            s[6] = 'color: #00ff00' if row['Pęd (MACD)'] == 'Wzrostowy' else 'color: #ff4b4b'
            # ADX
            s[7] = 'color: #00ff00; font-weight: bold' if row['Trend (ADX)'] > 25 else 'color: #ff4b4b'
            # Historia
            val_h = float(row['Hist. 50 świec'].replace('%',''))
            s[9] = 'color: #00ff00' if val_h > 0 else 'color: #ff4b4b' if val_h < 0 else ''
            return s
            
        st.dataframe(df_res.style.apply(stylizuj, axis=1), use_container_width=True)
        st.info("Legenda: StochRSI < 20 (Zielone tło) = Wyprzedanie (Okazja). StochRSI > 80 (Czerwone tło) = Wykupienie (Ryzyko).")
    else:
        st.error("Błąd połączenia. Odśwież stronę lub sprawdź requirements.txt.")
