import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf

# --- KONFIGURACJA ---
st.set_page_config(page_title="Skaner PRO - Analiza Ekspercka", layout="wide")

# Pełna lista instrumentów z XTB
KRYPTO_XTB = [
    "BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "ADA-USD", "DOT-USD", 
    "LINK-USD", "LTC-USD", "BCH-USD", "AVAX-USD", "MATIC-USD", "TRX-USD", 
    "UNI-USD", "ATOM-USD", "ETC-USD", "XMR-USD", "ALGO-USD", "AAVE-USD", "VET-USD", "DOGE-USD"
]

interval_map = {
    "5 min": "5m", "15 min": "15m", "30 min": "30m", "1 godz": "1h", 
    "4 godz": "4h", "1 dzień": "1d", "1 tydz": "1wk", "1 mies": "1mo"
}

def pobierz_dane(tryb, interwal_label):
    interwal = interval_map[interwal_label]
    # Dynamiczny dobór okresu
    if interwal in ["5m", "15m", "30m"]: okres = "5d"
    elif interwal in ["1h", "4h"]: okres = "60d"
    elif interwal == "1d": okres = "1y"
    else: okres = "5y" # Dla 1wk i 1mo

    with st.spinner(f"Analizuję {len(KRYPTO_XTB)} instrumentów..."):
        try:
            # Pobieranie zbiorcze (optymalizacja połączenia)
            data = yf.download(KRYPTO_XTB, period=okres, interval=interwal, group_by='ticker', progress=False, timeout=20)
        except:
            return None

    wyniki = []
    for symbol in KRYPTO_XTB:
        try:
            df = data[symbol].dropna()
            if len(df) < 50: continue

            # Obliczenia techniczne
            df.ta.rsi(length=14, append=True)
            df.ta.ema(length=20, append=True)
            df.ta.ema(length=50, append=True)
            df.ta.adx(length=14, append=True)
            df.ta.bbands(length=20, append=True)
            df.ta.atr(length=14, append=True)
            df['Vol_Avg'] = df['Volume'].rolling(window=20).mean()
            
            l = df.iloc[-1]
            prev = df.iloc[-2]
            cena = float(l['Close'])
            rsi = float(l['RSI_14'])
            ema20 = float(l['EMA_20'])
            vol_ratio = float(l['Volume'] / l['Vol_Avg']) if l['Vol_Avg'] > 0 else 1

            # Sygnał
            sig = "KUP" if cena > ema20 else "SPRZEDAJ"
            
            # Punktacja Siły % (0-100)
            score = 30
            if (sig == "KUP" and cena > l['EMA_50']) or (sig == "SPRZEDAJ" and cena < l['EMA_50']): score += 20
            if (sig == "KUP" and rsi < 50) or (sig == "SPRZEDAJ" and rsi > 50): score += 20
            if vol_ratio > 1.1: score += 15
            if l['ADX_14'] > 25: score += 15

            # BB Status & Dywergencja
            bb_stat = "Wewnątrz"
            if cena > l['BBU_20_2.0']: bb_stat = "Wybicie Górą"
            elif cena < l['BBL_20_2.0']: bb_stat = "Wybicie Dołem"

            dyw = "BRAK"
            if sig == "KUP" and cena > prev['Close'] and rsi < prev['RSI_14']: dyw = "NIEDŹW."
            if sig == "SPRZEDAJ" and cena < prev['Close'] and rsi > prev['RSI_14']: dyw = "BYCZA"

            wejscie = cena if tryb == "rynkowy" else ema20
            atr = l['ATRr_14']

            wyniki.append({
                "Instrument": symbol.replace("-USD", ""),
                "Sygnał": sig,
                "Siła %": min(score, 98),
                "Cena Wejścia": round(wejscie, 4),
                "Wolumen %": round(vol_ratio * 100),
                "RSI": round(rsi, 1),
                "ADX": round(l['ADX_14'], 1),
                "BB Status": bb_stat,
                "Dyw.": dyw,
                "TP": round(wejscie + (atr*2.5) if sig=="KUP" else wejscie - (atr*2.5), 4),
                "SL": round(wejscie - (atr*1.5) if sig=="KUP" else wejscie + (atr*1.5), 4)
            })
        except: continue
    return wyniki

def stylizuj(df):
    def apply(row):
        s = [''] * len(row)
        sig = row['Sygnał']
        # 1: Sygnał tło
        s[1] = 'background-color: #1e4620; color: white' if sig == 'KUP' else 'background-color: #5f1a1d; color: white'
        # 2: Siła tekst
        s[2] = 'color: #00ff00; font-weight: bold' if row['Siła %'] > 70 else 'color: #ff4b4b'
        # 4: Wolumen tekst
        s[4] = 'color: #00ff00' if row['Wolumen %'] > 100 else 'color: #ff4b4b'
        # 5: RSI tekst
        if sig == "KUP":
            s[5] = 'color: #00ff00' if row['RSI'] < 50 else 'color: #ff4b4b'
        else:
            s[5] = 'color: #00ff00' if row['RSI'] > 50 else 'color: #ff4b4b'
        return s
    return df.style.apply(apply, axis=1)

# --- UI ---
st.title("⚖️ Skaner PRO - Analiza Precyzyjna")

int_label = st.select_slider("Wybierz interwał (od 5m do 1M):", options=list(interval_map.keys()), value="4 godz")

col1, col2 = st.columns(2)
with col1: btn_m = st.button("🚀 ANALIZA RYNKOWA", use_container_width=True)
with col2: btn_s = st.button("💎 ANALIZA SUGEROWANA (LIMIT)", use_container_width=True)

if btn_m or btn_s:
    mode = "rynkowy" if btn_m else "sugerowany"
    dane = pobierz_dane(mode, int_label)
    if dane:
        df_final = pd.DataFrame(dane).sort_values(by="Siła %", ascending=False)
        st.dataframe(stylizuj(df_final), use_container_width=True)
    else:
        st.error("Przekroczono limit zapytań Yahoo. Odczekaj 2 minuty.")
