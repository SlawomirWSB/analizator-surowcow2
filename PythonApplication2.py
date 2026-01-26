import streamlit as st
import pandas as pd
import pandas_ta as ta
from tvdatafeed import TvDatafeed, Interval
import time

# --- KONFIGURACJA ---
st.set_page_config(page_title="Skaner PRO V5.4 - TV Engine", layout="wide")

KRYPTO_TV = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT", "DOTUSDT", 
             "LINKUSDT", "LTCUSDT", "AVAXUSDT", "MATICUSDT", "TRXUSDT", "DOGEUSDT"]

interval_map = {
    "5 min": Interval.in_5_minute, "15 min": Interval.in_15_minute, "30 min": Interval.in_30_minute,
    "1 godz": Interval.in_1_hour, "4 godz": Interval.in_4_hour, "1 dzień": Interval.in_daily,
    "1 tydz": Interval.in_weekly, "1 mies": Interval.in_monthly
}

@st.cache_resource
def init_tv():
    return TvDatafeed()

def pobierz_dane_tv(interwal_label):
    tv = init_tv()
    all_data = {}
    with st.spinner(f'Łączenie z TradingView...'):
        for sym in KRYPTO_TV:
            try:
                # Pobieramy 250 świec, aby backtest 50 świec miał solidną podstawę
                df = tv.get_hist(symbol=sym, exchange='BINANCE', 
                                 interval=interval_map[interwal_label], n_bars=250)
                if df is not None:
                    df = df.rename(columns={'open':'Open', 'high':'High', 'low':'Low', 
                                            'close':'Close', 'volume':'Volume'})
                    all_data[sym] = df
                time.sleep(0.1)
            except: continue
    return all_data

def run_backtest(df):
    if len(df) < 100: return 0.0
    # Testujemy na ostatnich 50 świecach, ale używamy reszty do stabilizacji wskaźników
    test_data = df.tail(100).copy()
    test_data['EMA'] = ta.ema(test_data['Close'], length=20)
    cap, pos = 1000.0, 0.0
    for i in range(50, len(test_data)):
        p, e = test_data['Close'].iloc[i], test_data['EMA'].iloc[i]
        if p > e and pos == 0: pos = cap / p
        elif p < e and pos > 0: cap, pos = pos * p, 0.0
    final = cap if pos == 0 else pos * test_data['Close'].iloc[-1]
    return round(((final - 1000) / 1000) * 100, 2)

def przetworz_v5_4(data, tryb):
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
                "Instrument": sym.replace("USDT", ""), 
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

# --- UI ---
st.title("⚖️ Skaner PRO V5.4 - TradingView Engine")
wybrany_int = st.select_slider("Wybierz interwał:", options=list(interval_map.keys()), value="4 godz")

c1, c2 = st.columns(2)
with c1: btn_m = st.button("🚀 ANALIZA - CENA RYNKOWA", use_container_width=True)
with c2: btn_s = st.button("💎 ANALIZA - SUGEROWANA (LIMIT)", use_container_width=True)

if btn_m or btn_s:
    mode = "rynkowy" if btn_m else "sugerowany"
    raw_data = pobierz_dane_tv(wybrany_int)
    if raw_data:
        res = przetworz_v5_4(raw_data, mode)
        df_res = pd.DataFrame(res).sort_values(by="Siła %", ascending=False)
        
        def stylizuj(row):
            s = [''] * len(row); sig = row['Sygnał']
            # Sygnał
            if sig == 'KUP': s[1] = 'background-color: #1e4620; color: white'
            elif sig == 'SPRZEDAJ': s[1] = 'background-color: #5f1a1d; color: white'
            # RSI
            if sig == 'KUP': s[4] = 'color: #00ff00' if row['RSI'] < 50 else 'color: #ff4b4b'
            elif sig == 'SPRZEDAJ': s[4] = 'color: #00ff00' if row['RSI'] > 50 else 'color: #ff4b4b'
            # ADX
            s[5] = 'color: #00ff00; font-weight: bold' if row['ADX'] > 25 else 'color: #ff4b4b'
            # Historia (Backtest)
            val_h = float(row['Hist. 50 świec'].replace('%',''))
            s[7] = 'color: #00ff00' if val_h > 0 else 'color: #ff4b4b' if val_h < 0 else ''
            return s
            
        st.dataframe(df_res.style.apply(stylizuj, axis=1), use_container_width=True)
    else:
        st.error("Błąd połączenia. Sprawdź requirements.txt lub spróbuj ponownie.")
