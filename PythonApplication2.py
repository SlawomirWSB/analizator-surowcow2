import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf

# 1. KONFIGURACJA STRONY
st.set_page_config(page_title="Skaner Krypto PRO", layout="wide")

# Lista instrumentów XTB
KRYPTO_LISTA = [
    "BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "ADA-USD", "DOT-USD", 
    "LINK-USD", "LTC-USD", "MATIC-USD", "DOGE-USD", "AVAX-USD", "BCH-USD",
    "SHIB-USD", "ALGO-USD", "UNI-USD", "NEAR-USD", "ATOM-USD", "ICP-USD", 
    "XLM-USD", "ETC-USD", "FIL-USD", "SAND-USD", "MANA-USD", "AAVE-USD"
]

interval_map = {
    "1 min": "1m", "5 min": "5m", "15 min": "15m", "30 min": "30m",
    "1 godz": "1h", "4 godz": "1h", "1 dzień": "1d", "1 tydz": "1wk", "1 mies": "1mo"
}

def pobierz_dane(symbol, interwal, okres):
    try:
        df = yf.download(symbol, period=okres, interval=interwal, progress=False)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        return df
    except:
        return pd.DataFrame()

def wykonaj_analize(symbol, interwal_label):
    interwal = interval_map[interwal_label]
    okres_map = {"1m": "1d", "5m": "1d", "15m": "1d", "30m": "1d", "1h": "1mo", "1d": "2y", "1wk": "max", "1mo": "max"}
    
    df = pobierz_dane(symbol, interwal, okres_map.get(interwal, "2y"))
    
    if df.empty or len(df) < 50:
        return None

    # OBLICZENIA TECHNICZNE
    df.ta.rsi(length=14, append=True)
    df.ta.ema(length=20, append=True)
    df.ta.ema(length=50, append=True)
    df.ta.atr(length=14, append=True)
    df['Vol_Avg'] = df['Volume'].rolling(window=20).mean()

    last = df.iloc[-1]
    cena = float(last['Close'])
    rsi = float(last['RSI_14'])
    
    # FILTR TRENDU WYŻSZEGO (MTF)
    tf_wyzszy = "1d" if "m" in interwal or "h" in interwal else "1wk"
    df_big = pobierz_dane(symbol, tf_wyzszy, "2y")
    
    trend_wyzszy_ok = True
    if not df_big.empty and len(df_big) > 20:
        ema_big = ta.ema(df_big['Close'], length=20)
        trend_wyzszy_ok = float(df_big['Close'].iloc[-1]) > float(ema_big.iloc[-1])

    # SCORING (Rygorystyczny)
    score = 50
    if rsi < 30: score += 15
    if rsi > 70: score -= 20
    if cena > last['EMA_20'] > last['EMA_50']: score += 15
    if last['Volume'] > last['Vol_Avg']: score += 5
    if not trend_wyzszy_ok: score -= 30 

    # Werdykt
    signal = "KUP" if score >= 65 else "SPRZEDAJ" if score <= 35 else "CZEKAJ"
    atr = float(last['ATRr_14'])
    tp = cena + (atr * 3)
    sl = cena - (atr * 1.5)
    zysk_procent = ((tp - cena) / cena) * 100

    return {
        "Instrument": symbol.replace("-USD", ""),
        "Sygnał": signal,
        "Szansa %": int(min(max(score, 0), 100)),
        "Trend Wyższy": "WZROST" if trend_wyzszy_ok else "SPADEK",
        "Cena": round(cena, 4),
        "Zysk do TP": f"{round(zysk_procent, 2)}%",
        "RSI": round(rsi, 1),
        "Wejście": round(cena, 4),
        "TP": round(tp, 4),
        "SL": round(sl, 4)
    }

# --- UI ---
st.title("🛡️ Skaner Kryptowalut (Rygorystyczny MTF)")

wybrany_interwal = st.select_slider(
    "Zmień interwał analizy:", 
    options=list(interval_map.keys()), 
    value="1 godz"
)

if st.button("🚀 URUCHOM ANALIZĘ", use_container_width=True):
    wyniki = []
    progress = st.progress(0)
    for i, s in enumerate(KRYPTO_LISTA):
        res = wykonaj_analize(s, wybrany_interwal)
        if res: wyniki.append(res)
        progress.progress((i + 1) / len(KRYPTO_LISTA))
    
    if wyniki:
        df_final = pd.DataFrame(wyniki).sort_values(by="Szansa %", ascending=False)
        
        # Funkcja kolorowania wierszy
        def highlight_ready(row):
            if row['Sygnał'] == 'KUP' and row['Trend Wyższy'] == 'WZROST':
                return ['background-color: #004d00'] * len(row) # Ciemny zielony
            elif row['Sygnał'] == 'SPRZEDAJ':
                return ['color: #ff4d4d'] * len(row) # Czerwony tekst dla sprzedaży
            return [''] * len(row)

        st.dataframe(df_final.style.apply(highlight_ready, axis=1), use_container_width=True, height=800)
    else:
        st.error("Błąd pobierania danych.")
