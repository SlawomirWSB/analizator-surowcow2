import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf

st.set_page_config(page_title="Skaner Krypto XTB", layout="wide")

# Lista symboli (używamy par z USDT i USD dla większej stabilności danych)
KRYPTO_LISTA = [
    "BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "ADA-USD", "DOT-USD", 
    "LINK-USD", "LTC-USD", "MATIC-USD", "DOGE-USD", "AVAX-USD", "BCH-USD"
]

interval_map = {
    "1 min": "1m", "5 min": "5m", "15 min": "15m", "30 min": "30m",
    "1 godz": "1h", "4 godz": "1h", "1 dzień": "1d", "1 tydz": "1wk"
}

def wykonaj_analize(symbol, interwal_label):
    try:
        interwal = interval_map[interwal_label]
        
        # dynamiczny dobór okresu, żeby nie było pustych danych
        if "min" in interwal_label:
            okres = "1d"
        elif "godz" in interwal_label:
            okres = "7d"
        else:
            okres = "1y"
        
        # Pobieranie danych
        df = yf.download(symbol, period=okres, interval=interwal, progress=False)
        
        # Sprawdzenie czy MultiIndex (poprawka dla nowej wersji yfinance)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        if df.empty or len(df) < 15:
            return None

        # Analiza Techniczna
        df.ta.rsi(length=14, append=True)
        df.ta.ema(length=20, append=True)
        df.ta.ema(length=50, append=True)
        df.ta.atr(length=14, append=True)

        ostatni = df.iloc[-1]
        cena = float(ostatni['Close'])
        rsi = float(ostatni['RSI_14'])
        ema20 = float(ostatni['EMA_20'])
        ema50 = float(ostatni['EMA_50'])
        atr = float(ostatni['ATRr_14'])

        # Logika szansy
        wynik = 50
        if rsi < 30: wynik += 25
        elif rsi > 70: wynik -= 25
        if cena > ema20: wynik += 10
        if ema20 > ema50: wynik += 15

        return {
            "Kryptowaluta": symbol.replace("-USD", ""),
            "Cena": round(cena, 4),
            "Szansa %": int(min(max(wynik, 5), 98)),
            "RSI": round(rsi, 2),
            "Wejście": round(cena, 4),
            "TP": round(cena + (atr * 2.5), 4),
            "SL": round(cena - (atr * 1.5), 4)
        }
    except Exception as e:
        return None

# UI
st.title("📈 Skaner Kryptowalut")

wybrany_interwal = st.select_slider("Wybierz czasookres:", options=list(interval_map.keys()), value="1 godz")

if st.button("🚀 URUCHOM ANALIZĘ", use_container_width=True):
    wyniki = []
    with st.spinner('Pobieranie danych rynkowych...'):
        for s in KRYPTO_LISTA:
            res = wykonaj_analize(s, wybrany_interwal)
            if res:
                wyniki.append(res)
    
    if wyniki:
        df_final = pd.DataFrame(wyniki).sort_values(by="Szansa %", ascending=False)
        
        # Wyświetlanie wyników w ładnej tabeli
        st.table(df_final) 
    else:
        st.error("Nie udało się pobrać danych dla wybranego interwału. Spróbuj wybrać '1 godz' lub '1 dzień'.")
