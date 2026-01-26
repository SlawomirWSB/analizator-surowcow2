import streamlit as st
import pandas as pd
import pandas_ta as ta
import ccxt
import time

# --- KONFIGURACJA ---
st.set_page_config(page_title="Skaner PRO V5.5 - Stabilny", layout="wide")

KRYPTO = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "XRP/USDT", "ADA/USDT", "DOT/USDT", 
          "LINK/USDT", "LTC/USDT", "AVAX/USDT", "MATIC/USDT", "TRX/USDT", "DOGE/USDT"]

interval_map = {
    "5 min": "5m", "15 min": "15m", "30 min": "30m", "1 godz": "1h", 
    "4 godz": "4h", "1 dzień": "1d", "1 tydz": "1w", "1 mies": "1M"
}

def pobierz_dane_stabilne(interwal_label):
    # Używamy Binance US lub fallback, aby uniknąć blokad IP Streamlit (USA)
    ex = ccxt.binanceus() # Binance US jest lepiej tolerowany przez serwery w USA
    all_data = {}
    tf = interval_map[interwal_label]
    
    progress_text = st.empty()
    for idx, sym in enumerate(KRYPTO):
        try:
            progress_text.text(f"Pobieranie: {sym}...")
            # Pobieramy 200 świec dla stabilności wskaźników
            ohlcv = ex.fetch_ohlcv(sym, timeframe=tf, limit=200)
            df = pd.DataFrame(ohlcv, columns=['time', 'Open', 'High', 'Low', 'Close', 'Volume'])
            df['time'] = pd.to_datetime(df['time'], unit='ms')
            all_data[sym] = df.set_index('time')
            time.sleep(0.1) # Rate limit protection
        except:
            continue
    progress_text.empty()
    return all_data

def run_backtest(df):
    if len(df) < 60: return 0.0
    test_data = df.tail(60).copy()
    test_data['EMA'] = ta.ema(test_data['Close'], length=20)
    cap, pos = 1000.0, 0.0
    for i in range(20, len(test_data)):
        p, e = test_data['Close'].iloc[i], test_data['EMA'].iloc[i]
        if p > e and pos == 0: pos = cap / p
        elif p < e and pos > 0: cap, pos = pos * p, 0.0
    final = cap if pos == 0 else pos * test_data['Close'].iloc[-1]
    return round(((final - 1000) / 1000) * 100, 2)

def przetworz_v5_5(data, tryb):
    wyniki = []
    for sym, df in data.items():
        try:
            df.ta.rsi(length=14, append=True)
            df.ta.ema(length=20, append=True)
            df.ta.adx(length=14, append=True)
            df.ta.atr(length=14, append=True)
            df['Vol_Avg'] = df['Volume'].rolling(20).mean()
            
            l = df.iloc[-1]
            c, e, a, r, atr = float(l['Close']), float(l['EMA_20']), float(l['ADX_14']), float(l['RSI_14']), float(l['ATRr_14'])
            vol_ratio = float(l['Volume'] / l['Vol_Avg']) if l['Vol_Avg'] > 0 else 1.0
            
            sig = "KUP" if c > e else "SPRZEDAJ"
            if a < 20: sig = "KONSOLIDACJA"
            
            score = 45
            if a > 25: score += 20
            if (sig == "KUP" and r < 50) or (sig == "SPRZEDAJ" and r > 50): score += 20
            if vol_ratio > 1.1: score += 15
            
            wej = c if tryb == "rynkowy" else e
            wyniki.append({
                "Instrument": sym.replace("/USDT", ""), 
                "Sygnał": sig, 
                "Siła %": min(score, 98) if sig != "KONSOLIDACJA" else 0,
                "Cena Wejścia": round(wej, 4), 
                "RSI": round(r, 1), 
                "ADX": round(a, 1),
                "Wolumen %": round(vol_ratio * 100), 
                "Hist. 50 świec": f"{run_backtest(df)}%",
                "TP (Cel)": round(wej + (atr*2.5) if sig=="KUP" else wej - (atr*2.5), 4),
                "SL (Stop)": round(wej - (atr*1.5) if sig=="KUP" else wej + (atr*1.5), 4)
            })
        except: continue
    return wyniki

# --- INTERFEJS ---
st.title("⚖️ Skaner PRO V5.5 - System Ekspercki")
wybrany_int = st.select_slider("Wybierz interwał:", options=list(interval_map.keys()), value="4 godz")

c1, c2 = st.columns(2)
with c1: btn_m = st.button("🚀 ANALIZA - CENA RYNKOWA", use_container_width=True)
with c2: btn_s = st.button("💎 ANALIZA - SUGEROWANA (LIMIT)", use_container_width=True)

if btn_m or btn_s:
    mode = "rynkowy" if btn_m else "sugerowany"
    raw_data = pobierz_dane_stabilne(wybrany_int)
    if raw_data:
        res = przetworz_v5_5(raw_data, mode)
        df_res = pd.DataFrame(res).sort_values(by="Siła %", ascending=False)
        
        def stylizuj(row):
            s = [''] * len(row); sig = row['Sygnał']
            if sig == 'KUP': s[1] = 'background-color: #1e4620; color: white'
            elif sig == 'SPRZEDAJ': s[1] = 'background-color: #5f1a1d; color: white'
            if sig == 'KUP': s[4] = 'color: #00ff00' if row['RSI'] < 50 else 'color: #ff4b4b'
            elif sig == 'SPRZEDAJ': s[4] = 'color: #00ff00' if row['RSI'] > 50 else 'color: #ff4b4b'
            s[5] = 'color: #00ff00; font-weight: bold' if row['ADX'] > 25 else 'color: #ff4b4b'
            val_h = float(row['Hist. 50 świec'].replace('%',''))
            s[7] = 'color: #00ff00' if val_h > 0 else 'color: #ff4b4b' if val_h < 0 else ''
            return s
            
        st.dataframe(df_res.style.apply(stylizuj, axis=1), use_container_width=True)
    else:
        st.error("Błąd połączenia z giełdą. Upewnij się, że requirements.txt zawiera 'ccxt'.")
