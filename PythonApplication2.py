import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf

# Konfiguracja strony
st.set_page_config(page_title="Skaner Krypto", layout="wide")

# Lista kryptowalut (odpowiedniki tych z XTB)
KRYPTO_LISTA = [
    "BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "ADA-USD", "DOT-USD", 
    "LINK-USD", "LTC-USD", "MATIC-USD", "DOGE-USD", "AVAX-USD", "BCH-USD"
]

# Mapowanie interwałów
interval_map = {
    "1 min": "1m", "5 min": "5m", "15 min": "15m", "30 min": "30m",
    "1 godz": "1h", "4 godz": "1h", "1 dzień": "1d", "1 tydz": "1wk"
}

def wykonaj_analize(symbol, interwal_label):
    try:
        # Pobieranie danych (yfinance)
        interwal = interval_map[interwal_label]
        okres = "1d" if "min" in interwal_label else "1mo" if "godz" in interwal_label else "1y"
        
        df = yf.download(symbol, period=okres, interval=interwal, progress=False)
        
        if df.empty or len(df) < 30:
            return None

        # Obliczanie wskaźników przez pandas_ta
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

        # Punktacja szansy (0-100)
        wynik = 50
        if rsi < 35: wynik += 25  # Wyprzedanie
        if rsi > 65: wynik -= 25  # Wykupienie
        if cena > ema20 > ema50: wynik += 15 # Trend wzrostowy

        return {
            "Kryptowaluta": symbol.replace("-USD", ""),
            "Cena": round(cena, 4),
            "Szansa %": int(min(max(wynik, 5), 95)),
            "RSI": round(rsi, 2),
            "Wejście": round(cena, 4),
            "TP (Zysk)": round(cena + (atr * 2), 4),
            "SL (Stop)": round(cena - (atr * 1.5), 4)
        }
    except:
        return None

# --- INTERFEJS ---
st.title("📈 Skaner Kryptowalut")

col_suwak, col_przycisk = st.columns([3, 1])

with col_suwak:
    wybrany_interwal = st.select_slider("Wybierz czasookres:", options=list(interval_map.keys()), value="1 godz")

with col_przycisk:
    st.write("##")
    klik = st.button("🚀 ANALIZUJ", use_container_width=True)

if klik:
    wyniki = []
    postep = st.progress(0)
    
    for i, s in enumerate(KRYPTO_LISTA):
        res = wykonaj_analize(s, wybrany_interwal)
        if res:
            wyniki.append(res)
        postep.progress((i + 1) / len(KRYPTO_LISTA))
    
    if wyniki:
        df_final = pd.DataFrame(wyniki).sort_values(by="Szansa %", ascending=False)
        st.dataframe(df_final, use_container_width=True, height=500)
    else:
        st.error("Brak danych. Spróbuj zmienić interwał.")
