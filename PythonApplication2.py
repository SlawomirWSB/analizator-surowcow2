import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf

# --- KONFIGURACJA ---
st.set_page_config(page_title="Skaner PRO V5.1", layout="wide")

KRYPTO = [
    "BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "ADA-USD", "DOT-USD", 
    "LINK-USD", "LTC-USD", "AVAX-USD", "MATIC-USD", "TRX-USD", "DOGE-USD"
]

interval_map = {
    "5 min": "5m", "15 min": "15m", "30 min": "30m", "1 godz": "1h", 
    "4 godz": "4h", "1 dzień": "1d", "1 tydz": "1wk", "1 mies": "1mo"
}

@st.cache_data(ttl=600)
def pobierz_dane_v5(interwal_label):
    interwal = interval_map[interwal_label]
    if interwal in ["5m", "15m", "30m"]: okres = "7d"
    elif interwal in ["1h", "4h"]: okres = "60d"
    elif interwal == "1d": okres = "2y"
    else: okres = "max"
    try:
        data = yf.download(KRYPTO, period=okres, interval=interwal, group_by='ticker', progress=False)
        return data
    except Exception as e:
        st.error(f"Błąd pobierania danych: {e}")
        return None

def run_backtest(df):
    if len(df) < 51: return 0.0
    test_data = df.tail(50).copy()
    test_data['EMA'] = ta.ema(test_data['Close'], length=20)
    
    cap = 1000.0
    pos = 0.0
    
    for i in range(1, len(test_data)):
        price = test_data['Close'].iloc[i]
        ema = test_data['EMA'].iloc[i]
        if price > ema and pos == 0:
            pos = cap / price
        elif price < ema and pos > 0:
            cap = pos * price
            pos = 0.0
            
    final_val = cap if pos == 0 else pos * test_data['Close'].iloc[-1]
    return round(((final_val - 1000) / 1000) * 100, 2)

def przetworz_v5(data, tryb):
    if data is None: return []
    wyniki = []
    for symbol in KRYPTO:
        try:
            df = data[symbol].dropna()
            if len(df) < 35: continue
            
            # Wskaźniki
            df.ta.rsi(length=14, append=True)
            df.ta.ema(length=20, append=True)
            df.ta.adx(length=14, append=True)
            df.ta.atr(length=14, append=True)
            df['Vol_Avg'] = df['Volume'].rolling(20).mean()
            
            l = df.iloc[-1]
            cena = float(l['Close'])
            ema20 = float(l['EMA_20'])
            adx = float(l['ADX_14'])
            rsi = float(l['RSI_14'])
            atr = float(l['ATRr_14'])
            vol_ratio = float(l['Volume'] / l['Vol_Avg']) if l['Vol_Avg'] > 0 else 1.0
            
            # Logika Sygnału
            sig = "KUP" if cena > ema20 else "SPRZEDAJ"
            if adx < 20: sig = "KONSOLIDACJA"
            
            score = 45
            if adx > 25: score += 20
            if (sig == "KUP" and rsi < 55) or (sig == "SPRZEDAJ" and rsi > 45): score += 15
            if vol_ratio > 1.1: score += 15
            
            wej = cena if tryb == "rynkowy" else ema20
            hist_perf = run_backtest(df)
            
            wyniki.append({
                "Instrument": symbol.replace("-USD", ""),
                "Sygnał": sig,
                "Siła %": min(score, 98) if sig != "KONSOLIDACJA" else 0,
                "Cena Wejścia": round(wej, 4),
                "RSI": round(rsi, 1),
                "ADX": round(adx, 1),
                "Wolumen %": round(vol_ratio * 100),
                "Hist. 50 świec": f"{hist_perf}%",
                "TP (Cel)": round(wej + (atr*2.5) if sig=="KUP" else wej - (atr*2.5), 4),
                "SL (Stop)": round(wej - (atr*1.5) if sig=="KUP" else wej + (atr*1.5), 4)
            })
        except: continue
    return wyniki

# --- INTERFEJS ---
st.title("⚖️ Skaner PRO - System Ekspercki V5.1")
wybrany_int = st.select_slider("Wybierz interwał:", options=list(interval_map.keys()), value="4 godz")

c1, c2 = st.columns(2)
with c1: btn_m = st.button("🚀 ANALIZA - CENA RYNKOWA", use_container_width=True)
with c2: btn_s = st.button("💎 ANALIZA - SUGEROWANA (LIMIT)", use_container_width=True)

if btn_m or btn_s:
    mode = "rynkowy" if btn_m else "sugerowany"
    raw_data = pobierz_dane_v5(wybrany_int)
    if raw_data is not None:
        finalne = przetworz_v5(raw_data, mode)
        if finalne:
            df_res = pd.DataFrame(finalne).sort_values(by="Siła %", ascending=False)
            
            def stylizuj(row):
                s = [''] * len(row)
                sig = row['Sygnał']
                if sig == 'KUP': s[1] = 'background-color: #1e4620; color: white'
                elif sig == 'SPRZEDAJ': s[1] = 'background-color: #5f1a1d; color: white'
                s[2] = 'color: #00ff00; font-weight: bold' if row['Siła %'] > 70 else ''
                s[6] = 'color: #00ff00' if row['Wolumen %'] > 100 else 'color: #ff4b4b'
                return s

            st.dataframe(df_res.style.apply(stylizuj, axis=1), use_container_width=True)
            st.caption("Legenda: 'Cena Wejścia' zależy od wybranego trybu (Rynek vs Limit/EMA20).")
        else:
            st.warning("Za mało danych dla tego interwału.")
