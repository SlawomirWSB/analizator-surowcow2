import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf

st.set_page_config(page_title="Skaner Krypto PRO", layout="wide")

# Rozszerzona lista instrumentów (zgodna z XTB)
KRYPTO_LISTA = [
    "BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "ADA-USD", "DOT-USD", 
    "LINK-USD", "LTC-USD", "MATIC-USD", "DOGE-USD", "AVAX-USD", "BCH-USD",
    "SHIB-USD", "ALGO-USD", "UNI-USD", "NEAR-USD", "ATOM-USD", "ICP-USD", 
    "XLM-USD", "ETC-USD", "FIL-USD", "SAND-USD", "MANA-USD", "AAVE-USD"
]

# Mapowanie interwałów z dodanym miesiącem
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
    # 1. Pobieranie danych dla wybranego interwału
    interwal = interval_map[interwal_label]
    okres_map = {"1m": "1d", "5m": "1d", "15m": "1d", "30m": "1d", "1h": "1mo", "1d": "2y", "1wk": "max", "1mo": "max"}
    
    df = pobierz_dane(symbol, interwal, okres_map.get(interwal, "1y"))
    
    if df.empty or len(df) < 50:
        return None

    # --- OBLICZENIA TECHNICZNE (GŁÓWNY TF) ---
    df.ta.rsi(length=14, append=True)
    df.ta.ema(length=20, append=True)
    df.ta.ema(length=50, append=True)
    df.ta.atr(length=14, append=True)
    df.ta.bbands(length=20, append=True)
    df['Vol_Avg'] = df['Volume'].rolling(window=20).mean()

    last = df.iloc[-1]
    cena = float(last['Close'])
    
    # 2. FILTR TRENDU WYŻSZEGO RZĘDU (MTF)
    # Jeśli analizujemy < 1d, sprawdź trend na 1d. Jeśli analizujemy 1d, sprawdź 1wk.
    tf_wyzszy = "1d" if "m" in interwal or "h" in interwal else "1wk"
    df_big = pobierz_dane(symbol, tf_wyzszy, "2y")
    
    trend_wyzszy_ok = True
    if not df_big.empty and len(df_big) > 20:
        ema_big = ta.ema(df_big['Close'], length=20)
        trend_wyzszy_ok = float(df_big['Close'].iloc[-1]) > float(ema_big.iloc[-1])

    # --- RYGORYSTYCZNY SCORING ---
    score = 50
    rsi = float(last['RSI_14'])
    
    if rsi < 30: score += 15
    if rsi > 70: score -= 20
    if cena > last['EMA_20'] > last['EMA_50']: score += 15
    if last['Volume'] > last['Vol_Avg']: score += 5
    if not trend_wyzszy_ok: score -= 30 # Kara za granie przeciw trendowi wyższemu

    # Werdykt
    signal = "KUP" if score >= 65 else "SPRZEDAJ" if score <= 35 else "CZEKAJ"
    atr = float(last['ATRr_14'])

    return {
        "Instrument": symbol.replace("-USD", ""),
        "Sygnał": signal,
        "Cena": round(cena, 4),
        "Szansa %": int(min(max(score, 0), 100)),
        "Trend Wyższy": "WZROST" if trend_wyzszy_ok else "SPADEK",
        "RSI": round(rsi, 2),
        "Wejście": round(cena, 4),
        "TP": round(cena + (atr * 3), 4),
        "SL": round(cena - (atr * 1.5), 4)
    }

# --- UI ---
st.title("🛡️ Rygorystyczny Analizator Multitimeframe")
st.info("System analizuje wybrany interwał oraz sprawdza trend na wyższym TF (np. 1H -> 1D).")

# Rozszerzony suwak
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
        
        def color_signal(val):
            color = 'green' if val == 'KUP' else 'red' if val == 'SPRZEDAJ' else 'gray'
            return f'color: {color}; font-weight: bold'

        st.dataframe(df_final.style.applymap(color_signal, subset=['Sygnał']), use_container_width=True, height=800)
    else:
        st.error("Brak danych dla tego interwału. Yahoo Finance może mieć przerwy w danych minutowych.")
