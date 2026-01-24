import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf

st.set_page_config(page_title="Skaner Krypto PRO", layout="wide")

# Pełna lista krypto dostępnych na XTB (mapowanie na Yahoo Finance)
KRYPTO_LISTA = [
    "BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "ADA-USD", "DOT-USD", 
    "LINK-USD", "LTC-USD", "MATIC-USD", "DOGE-USD", "AVAX-USD", "BCH-USD",
    "SHIB-USD", "ALGO-USD", "UNI-USD", "NEAR-USD", "ATOM-USD", "ICP-USD", 
    "XLM-USD", "ETC-USD", "FIL-USD", "SAND-USD", "MANA-USD", "AAVE-USD", 
    "EOS-USD", "DYDX-USD", "CRV-USD", "GALA-USD", "GRT-USD", "MKR-USD"
]

interval_map = {
    "1 min": "1m", "5 min": "5m", "15 min": "15m", "30 min": "30m",
    "1 godz": "1h", "4 godz": "1h", "1 dzień": "1d", "1 tydz": "1wk"
}

def wykonaj_analize(symbol, interwal_label):
    try:
        interwal = interval_map[interwal_label]
        okres = "1d" if "min" in interwal_label else "1mo" if "godz" in interwal_label else "2y"
        
        df = yf.download(symbol, period=okres, interval=interwal, progress=False)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        if df.empty or len(df) < 50: return None

        # --- OBLICZENIA TECHNICZNE ---
        df.ta.rsi(length=14, append=True)
        df.ta.ema(length=20, append=True)
        df.ta.ema(length=50, append=True)
        df.ta.atr(length=14, append=True)
        df.ta.bbands(length=20, std=2, append=True) # Wstęgi Bollingera
        # Analiza wolumenu (Średnia z 20 okresów)
        df['Vol_Avg'] = df['Volume'].rolling(window=20).mean()

        last = df.iloc[-1]
        prev = df.iloc[-2]
        cena = float(last['Close'])
        rsi = float(last['RSI_14'])
        ema20 = float(last['EMA_20'])
        ema50 = float(last['EMA_50'])
        atr = float(last['ATRr_14'])
        upper_bb = float(last['BBU_20_2.0'])
        lower_bb = float(last['BBL_20_2.0'])
        vol_current = float(last['Volume'])
        vol_avg = float(last['Vol_Avg'])

        # --- RYGORYSTYCZNY SCORING (0-100) ---
        score = 50 
        
        # 1. RSI (Ekstrema)
        if rsi < 25: score += 20  # Silne wyprzedanie
        if rsi > 75: score -= 20  # Silne wykupienie
        
        # 2. Trend (Potwierdzenie EMA)
        if cena > ema20 > ema50: score += 15
        elif cena < ema20 < ema50: score -= 15
        
        # 3. Wolumen (Potwierdzenie siły ruchu)
        if vol_current > vol_avg * 1.5: # Wolumen o 50% większy od średniej
            score = score + 10 if cena > prev['Close'] else score - 10
            
        # 4. Bollinger Bands (Odbicia od band)
        if cena <= lower_bb: score += 10 # Cena na dolnej bandzie (okazja)
        if cena >= upper_bb: score -= 10 # Cena na górnej bandzie (ryzyko)

        # Decyzja
        signal = "KUP" if score >= 65 else "SPRZEDAJ" if score <= 35 else "CZEKAJ"
        
        return {
            "Instrument": symbol.replace("-USD", ""),
            "Sygnał": signal,
            "Cena": round(cena, 4),
            "Szansa %": int(min(max(score, 0), 100)),
            "RSI": round(rsi, 2),
            "Vol vs Średnia": f"{round((vol_current/vol_avg)*100)}%",
            "Wejście": round(cena, 4),
            "TP": round(cena + (atr * 3), 4),
            "SL": round(cena - (atr * 1.5), 4)
        }
    except:
        return None

# --- UI ---
st.title("🛡️ Rygorystyczny Skaner Kryptowalut")
st.markdown("Analiza uwzględnia: RSI, EMA, ATR, Wolumen oraz Wstęgi Bollingera.")

wybrany_interwal = st.select_slider("Zmień interwał analizy:", options=list(interval_map.keys()), value="1 godz")

if st.button("🚀 WYKONAJ PEŁNĄ ANALIZĘ", use_container_width=True):
    wyniki = []
    progress = st.progress(0)
    for i, s in enumerate(KRYPTO_LISTA):
        res = wykonaj_analize(s, wybrany_interwal)
        if res: wyniki.append(res)
        progress.progress((i + 1) / len(KRYPTO_LISTA))
    
    if wyniki:
        df_final = pd.DataFrame(wyniki).sort_values(by="Szansa %", ascending=False)
        
        # Kolorowanie sygnałów
        def style_signals(val):
            color = '#00ff00' if val == 'KUP' else '#ff0000' if val == 'SPRZEDAJ' else '#888888'
            return f'color: {color}; font-weight: bold'

        st.dataframe(df_final.style.applymap(style_signals, subset=['Sygnał']), use_container_width=True, height=1000)
    else:
        st.error("Błąd pobierania danych.")
