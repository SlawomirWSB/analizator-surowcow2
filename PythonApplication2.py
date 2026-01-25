import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf

# --- KONFIGURACJA ---
st.set_page_config(page_title="Skaner PRO - Stabilny", layout="wide")

KRYPTO_XTB = ["BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "ADA-USD", "DOT-USD", "LINK-USD", "LTC-USD", "BCH-USD", "AVAX-USD"]

interval_map = {
    "5 min": "5m", "15 min": "15m", "1 godz": "1h", "4 godz": "4h", "1 dzień": "1d"
}

def wykonaj_skan(tryb, interwal_label):
    interwal = interval_map[interwal_label]
    okres = "7d" if "m" in interwal else "60d"
    
    # POBIERANIE WSZYSTKICH NARAZ (znacznie szybsze i bezpieczniejsze dla IP)
    try:
        data = yf.download(KRYPTO_XTB, period=okres, interval=interwal, group_by='ticker', progress=False, timeout=15)
    except:
        return None

    wyniki = []
    for symbol in KRYPTO_XTB:
        try:
            df = data[symbol].dropna()
            if len(df) < 25: continue

            # Wskaźniki
            df.ta.rsi(length=14, append=True)
            df.ta.ema(length=20, append=True)
            df['Vol_Avg'] = df['Volume'].rolling(window=20).mean()
            
            l = df.iloc[-1]
            cena = float(l['Close'])
            rsi = float(l['RSI_14'])
            ema20 = float(l['EMA_20'])
            vol_ratio = float(l['Volume'] / l['Vol_Avg']) if l['Vol_Avg'] > 0 else 1

            sig = "KUP" if cena > ema20 else "SPRZEDAJ"
            
            # Siła (uproszczona dla szybkości)
            score = 60
            if (sig == "KUP" and rsi < 50) or (sig == "SPRZEDAJ" and rsi > 50): score += 20
            if vol_ratio > 1.1: score += 15

            wejscie = cena if tryb == "rynkowy" else ema20
            # ATR do celów i stopów
            df.ta.atr(length=14, append=True)
            atr = df.iloc[-1]['ATRr_14']

            wyniki.append({
                "Instrument": symbol.replace("-USD", ""),
                "Sygnał": sig,
                "Siła %": min(score, 98),
                "Cena Wejścia": round(wejscie, 4),
                "Wolumen %": round(vol_ratio * 100),
                "RSI": round(rsi, 1),
                "TP": round(wejscie + (atr*2.5) if sig=="KUP" else wejscie - (atr*2.5), 4),
                "SL": round(wejscie - (atr*1.5) if sig=="KUP" else wejscie + (atr*1.5), 4)
            })
        except:
            continue
    return wyniki

def style_df(df):
    def row_style(row):
        s = [''] * len(row)
        sig = row['Sygnał']
        # Kolumny: 0:Inst, 1:Syg, 2:Siła, 3:Wejscie, 4:Vol, 5:RSI, 6:TP, 7:SL
        s[1] = 'background-color: #1e4620; color: white' if sig == 'KUP' else 'background-color: #5f1a1d; color: white'
        s[2] = 'color: #00ff00; font-weight: bold' if row['Siła %'] > 70 else 'color: #ff4b4b'
        s[4] = 'color: #00ff00' if row['Wolumen %'] > 100 else 'color: #ff4b4b'
        
        if sig == "KUP":
            s[5] = 'color: #00ff00' if row['RSI'] < 50 else 'color: #ff4b4b'
        else:
            s[5] = 'color: #00ff00' if row['RSI'] > 50 else 'color: #ff4b4b'
        return s
    return df.style.apply(row_style, axis=1)

# --- UI ---
st.title("⚖️ Skaner PRO - Analiza Stabilna")
wybrany_int = st.select_slider("Wybierz interwał:", options=list(interval_map.keys()), value="4 godz")

c1, c2 = st.columns(2)
with c1: btn_m = st.button("🚀 ANALIZA RYNKOWA", use_container_width=True)
with c2: btn_s = st.button("💎 ANALIZA SUGEROWANA (LIMIT)", use_container_width=True)

if btn_m or btn_s:
    t = "rynkowy" if btn_m else "sugerowany"
    with st.spinner("Pobieranie danych zbiorczych..."):
        dane = wykonaj_skan(t, wybrany_int)
    if dane:
        df = pd.DataFrame(dane).sort_values(by="Siła %", ascending=False)
        st.dataframe(style_df(df), use_container_width=True)
    else:
        st.error("Przekroczono limit zapytań Yahoo. Odczekaj 2 minuty i spróbuj ponownie.")
