import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf
import time

# --- USTALENIA STAŁE ---
KRYPTO_XTB = [
    "BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "ADA-USD", "DOT-USD", 
    "LINK-USD", "LTC-USD", "BCH-USD", "AVAX-USD", "MATIC-USD", "TRX-USD", 
    "UNI-USD", "ATOM-USD", "ETC-USD", "XMR-USD", "ALGO-USD", "AAVE-USD", "VET-USD", "DOGE-USD"
]

intervals = {
    "5 min": "5m", "15 min": "15m", "30 min": "30m", "1 godz": "1h", 
    "4 godz": "4h", "1 dzień": "1d", "1 tydz": "1wk", "1 mies": "1mo"
}

st.set_page_config(page_title="Skaner PRO - Total", layout="wide")

# --- LOGIKA POBIERANIA (ZABEZPIECZONA) ---
@st.cache_data(ttl=900)  # Zapamiętaj dane na 15 minut!
def pobierz_paczke_danych(interwal_klucz):
    interwal = intervals[interwal_klucz]
    # Dobór okresu tak, by EMA i RSI zawsze miały dość danych
    okres = "7d" if "m" in interwal else "60d"
    if interwal == "1d": okres = "2y"
    if interwal in ["1wk", "1mo"]: okres = "max"

    try:
        # Pobieramy wszystko jednym strzałem (najbezpieczniej dla IP)
        dane = yf.download(KRYPTO_XTB, period=okres, interval=interwal, group_by='ticker', progress=False, timeout=20)
        if dane.empty: return None
        return dane
    except:
        return None

def generuj_wyniki(raw_data, tryb):
    if raw_data is None: return []
    final_list = []
    
    for ticker in KRYPTO_XTB:
        try:
            df = raw_data[ticker].dropna()
            if len(df) < 30: continue

            # Obliczenia techniczne
            df.ta.rsi(length=14, append=True)
            df.ta.ema(length=20, append=True)
            df.ta.adx(length=14, append=True)
            df.ta.bbands(length=20, append=True)
            df.ta.atr(length=14, append=True)
            df['Vol_Avg'] = df['Volume'].rolling(window=20).mean()
            
            last = df.iloc[-1]
            prev = df.iloc[-2]
            cena = float(last['Close'])
            rsi = float(last['RSI_14'])
            ema = float(last['EMA_20'])
            vol_ratio = float(last['Volume'] / last['Vol_Avg']) if last['Vol_Avg'] > 0 else 0

            # Sygnał i Siła
            sygnal = "KUP" if cena > ema else "SPRZEDAJ"
            score = 50
            if (sygnal == "KUP" and rsi < 50) or (sygnal == "SPRZEDAJ" and rsi > 50): score += 20
            if vol_ratio > 1.1: score += 15
            if last['ADX_14'] > 25: score += 10

            wejscie = cena if tryb == "rynkowy" else ema
            atr = last['ATRr_14']

            final_list.append({
                "Instrument": ticker.replace("-USD", ""),
                "Sygnał": sygnal,
                "Siła %": min(score, 98),
                "Cena Wejścia": round(wejscie, 4),
                "Wolumen %": round(vol_ratio * 100),
                "RSI": round(rsi, 1),
                "ADX": round(last['ADX_14'], 1),
                "TP (Cel)": round(wejscie + (atr*2.5) if sygnal=="KUP" else wejscie - (atr*2.5), 4),
                "SL (Stop)": round(wejscie - (atr*1.5) if sygnal=="KUP" else wejscie + (atr*1.5), 4)
            })
        except: continue
    return final_list

# --- STYLIZACJA ---
def stylizuj(df):
    def r_style(row):
        styles = [''] * len(row)
        # Sygnał
        styles[1] = 'background-color: #1e4620; color: white' if row['Sygnał'] == 'KUP' else 'background-color: #5f1a1d; color: white'
        # Siła
        styles[2] = 'color: #00ff00; font-weight: bold' if row['Siła %'] > 70 else 'color: #ff4b4b'
        # Wolumen
        styles[4] = 'color: #00ff00' if row['Wolumen %'] > 100 else 'color: #ff4b4b'
        # RSI
        if row['Sygnał'] == "KUP":
            styles[5] = 'color: #00ff00' if row['RSI'] < 50 else 'color: #ff4b4b'
        else:
            styles[5] = 'color: #00ff00' if row['RSI'] > 50 else 'color: #ff4b4b'
        return styles
    return df.style.apply(r_style, axis=1)

# --- UI ---
st.title("⚖️ Skaner PRO - Wersja Totalna")
st.markdown("---")

wybrany_int = st.select_slider("Wybierz interwał (5m - 1M):", options=list(intervals.keys()), value="4 godz")

col1, col2 = st.columns(2)
with col1: btn_m = st.button("🚀 ANALIZA - CENA RYNKOWA", use_container_width=True)
with col2: btn_s = st.button("💎 ANALIZA - CENA LIMIT (EMA20)", use_container_width=True)

if btn_m or btn_s:
    mode = "rynkowy" if btn_m else "sugerowany"
    
    # 1. Pobierz dane (z cache)
    with st.spinner("Łączenie z serwerem..."):
        paczka = pobierz_paczke_danych(wybrany_int)
    
    if paczka is not None:
        # 2. Przetwórz
        wyniki = generuj_wyniki(paczka, mode)
        if wyniki:
            df_final = pd.DataFrame(wyniki).sort_values(by="Siła %", ascending=False)
            st.dataframe(stylizuj(df_final), use_container_width=True, height=700)
            st.success(f"Analiza zakończona. Dane zbuforowane dla interwału {wybrany_int}.")
        else:
            st.error("Błąd obliczeń. Spróbuj odświeżyć stronę (F5).")
    else:
        st.error("Yahoo Finance odmawia dostępu. Twoje IP ma blokadę czasową. ODCZEKAJ 5 MINUT i spróbuj ponownie.")
