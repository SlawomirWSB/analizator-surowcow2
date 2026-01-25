import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf

st.set_page_config(page_title="Skaner PRO - Stabilny", layout="wide")

KRYPTO_XTB = ["BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "ADA-USD", "DOT-USD", "LINK-USD", "LTC-USD", "BCH-USD", "AVAX-USD"]

interval_map = {
    "5 min": "5m", "15 min": "15m", "1 godz": "1h", "4 godz": "4h", "1 dzień": "1d", "1 tydz": "1wk"
}

def wykonaj_skan(tryb, interwal_label):
    wyniki = []
    interwal = interval_map[interwal_label]
    
    # Używamy stałego, bezpiecznego okresu 1 rok dla wszystkich interwałów powyżej 1h
    okres = "60d" if "m" in interwal else "1y"
    if interwal == "1wk": okres = "5y"

    for symbol in KRYPTO_XTB:
        try:
            # Pobieranie z krótkim timeoutem, żeby nie wieszać apki
            df = yf.download(symbol, period=okres, interval=interwal, progress=False, timeout=5)
            if df.empty or len(df) < 30: continue
            if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)

            # Obliczenia - tylko niezbędne, by nie przeciążać procesu
            df.ta.rsi(length=14, append=True)
            df.ta.ema(length=20, append=True)
            df.ta.bbands(length=20, append=True)
            df['Vol_Avg'] = df['Volume'].rolling(window=20).mean()
            
            l = df.iloc[-1]
            prev = df.iloc[-2]
            cena = float(l['Close'])
            rsi = float(l['RSI_14'])
            ema20 = float(l['EMA_20'])
            vol_ratio = float(l['Volume'] / l['Vol_Avg']) if l['Vol_Avg'] > 0 else 1

            sig = "KUP" if cena > ema20 else "SPRZEDAJ"
            
            # Siła sygnału (Scoring)
            score = 50
            if (sig == "KUP" and rsi < 50) or (sig == "SPRZEDAJ" and rsi > 50): score += 20
            if vol_ratio > 1.1: score += 20
            
            # BB Status
            bb_s = "Wewnątrz"
            if cena > l['BBU_20_2.0']: bb_s = "Wybicie Górą"
            elif cena < l['BBL_20_2.0']: bb_s = "Wybicie Dołem"

            # Dywergencja (Uproszczona)
            dyw = "BRAK"
            if sig == "KUP" and cena > prev['Close'] and rsi < prev['RSI_14']: dyw = "NIEDŹW."
            if sig == "SPRZEDAJ" and cena < prev['Close'] and rsi > prev['RSI_14']: dyw = "BYCZA"

            wejscie = cena if tryb == "rynkowy" else ema20
            
            wyniki.append({
                "Instrument": symbol.replace("-USD", ""),
                "Sygnał": sig,
                "Siła %": min(score, 98),
                "Cena Wejścia": round(wejscie, 4),
                "Wolumen %": round(vol_ratio * 100),
                "RSI": round(rsi, 1),
                "BB Status": bb_s,
                "Dyw.": dyw
            })
        except:
            continue
    return wyniki

def style_df(df):
    def row_style(row):
        s = [''] * len(row)
        # Sygnał tło
        s[1] = 'background-color: #1e4620; color: white' if row['Sygnał'] == 'KUP' else 'background-color: #5f1a1d; color: white'
        # Siła kolor
        s[2] = 'color: #00ff00; font-weight: bold' if row['Siła %'] > 70 else 'color: #ff4b4b'
        # Wolumen kolor
        s[4] = 'color: #00ff00' if row['Wolumen %'] > 100 else 'color: #ff4b4b'
        # RSI kolor
        if row['Sygnał'] == "KUP":
            s[5] = 'color: #00ff00' if row['RSI'] < 50 else 'color: #ff4b4b'
        else:
            s[5] = 'color: #00ff00' if row['RSI'] > 50 else 'color: #ff4b4b'
        return s
    return df.style.apply(row_style, axis=1)

# --- UI ---
st.title("⚖️ Skaner PRO - Wersja Stabilna")
wybrany_int = st.select_slider("Interwał:", options=list(interval_map.keys()), value="4 godz")

c1, c2 = st.columns(2)
with c1: btn_m = st.button("🚀 ANALIZA RYNKOWA", use_container_width=True)
with c2: btn_s = st.button("💎 ANALIZA SUGEROWANA", use_container_width=True)

if btn_m or btn_s:
    t = "rynkowy" if btn_m else "sugerowany"
    with st.spinner("Łączenie z Yahoo Finance..."):
        dane = wykonaj_skan(t, wybrany_int)
    if dane:
        df = pd.DataFrame(dane).sort_values(by="Siła %", ascending=False)
        st.dataframe(style_df(df), use_container_width=True)
    else:
        st.error("Serwer Yahoo Finance nie odpowiedział. Spróbuj ponownie za chwilę.")
