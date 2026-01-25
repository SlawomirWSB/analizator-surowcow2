import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf

# --- KONFIGURACJA ---
st.set_page_config(page_title="Skaner PRO - System Ekspercki V4", layout="wide")

KRYPTO_XTB = [
    "BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "ADA-USD", "DOT-USD", 
    "LINK-USD", "LTC-USD", "BCH-USD", "AVAX-USD", "MATIC-USD", "TRX-USD", 
    "UNI-USD", "ATOM-USD", "ETC-USD", "XMR-USD", "ALGO-USD", "AAVE-USD", "VET-USD", "DOGE-USD"
]

interval_map = {
    "5 min": "5m", "15 min": "15m", "30 min": "30m", "1 godz": "1h", 
    "4 godz": "4h", "1 dzień": "1d", "1 tydz": "1wk", "1 mies": "1mo"
}

# Cache zapobiega blokadom IP od Yahoo
@st.cache_data(ttl=600)
def pobierz_dane_v4(interwal_label):
    interwal = interval_map[interwal_label]
    if interwal in ["5m", "15m", "30m"]: okres = "7d"
    elif interwal in ["1h", "4h"]: okres = "60d"
    elif interwal == "1d": okres = "2y"
    else: okres = "max"

    try:
        data = yf.download(KRYPTO_XTB, period=okres, interval=interwal, group_by='ticker', progress=False, timeout=30)
        return data
    except:
        return None

def przetworz_v4(data, tryb):
    if data is None: return []
    wyniki = []
    
    for symbol in KRYPTO_XTB:
        try:
            df = data[symbol].dropna()
            if len(df) < 35: continue

            # Wskaźniki techniczne
            df.ta.rsi(length=14, append=True)
            df.ta.ema(length=20, append=True)
            df.ta.adx(length=14, append=True)
            df.ta.bbands(length=20, append=True)
            df.ta.atr(length=14, append=True)
            df['Vol_Avg'] = df['Volume'].rolling(window=20).mean()
            
            l = df.iloc[-1]
            cena = float(l['Close'])
            rsi = float(l['RSI_14'])
            ema20 = float(l['EMA_20'])
            vol_ratio = float(l['Volume'] / l['Vol_Avg']) if l['Vol_Avg'] > 0 else 1

            sig = "KUP" if cena > ema20 else "SPRZEDAJ"
            
            # Punktacja Siły
            score = 45
            if (sig == "KUP" and rsi < 50) or (sig == "SPRZEDAJ" and rsi > 50): score += 20
            if vol_ratio > 1.1: score += 15
            if l['ADX_14'] > 25: score += 15

            # BB i Dywergencja (Uproszczona)
            bb_stat = "Wewnątrz"
            if cena > l['BBU_20_2.0']: bb_stat = "Wybicie Górą"
            elif cena < l['BBL_20_2.0']: bb_stat = "Wybicie Dołem"

            wej = cena if tryb == "rynkowy" else ema20
            atr = l['ATRr_14']

            wyniki.append({
                "Instrument": symbol.replace("-USD", ""),
                "Sygnał": sig,
                "Siła %": min(score, 98),
                "Cena Wejścia": round(wej, 4),
                "Wolumen %": round(vol_ratio * 100),
                "RSI": round(rsi, 1),
                "ADX": round(l['ADX_14'], 1),
                "BB Status": bb_stat,
                "TP (Cel)": round(wej + (atr*2.5) if sig=="KUP" else wej - (atr*2.5), 4),
                "SL (Stop)": round(wej - (atr*1.5) if sig=="KUP" else wej + (atr*1.5), 4)
            })
        except: continue
    return wyniki

def stylizuj_v4(df):
    def apply_styles(row):
        s = [''] * len(row)
        sig = row['Sygnał']
        # Tło Sygnału
        s[1] = 'background-color: #1e4620; color: white' if sig == 'KUP' else 'background-color: #5f1a1d; color: white'
        # Siła %
        s[2] = 'color: #00ff00; font-weight: bold' if row['Siła %'] > 70 else 'color: #ff4b4b'
        # Wolumen i RSI
        s[4] = 'color: #00ff00' if row['Wolumen %'] > 100 else 'color: #ff4b4b'
        if sig == "KUP":
            s[5] = 'color: #00ff00' if row['RSI'] < 50 else 'color: #ff4b4b'
        else:
            s[5] = 'color: #00ff00' if row['RSI'] > 50 else 'color: #ff4b4b'
        return s
    return df.style.apply(apply_styles, axis=1)

# --- INTERFEJS ---
st.title("⚖️ Skaner PRO - System Ekspercki V4")

wybrany_int = st.select_slider("Wybierz interwał (5m - 1M):", options=list(interval_map.keys()), value="4 godz")

c1, c2 = st.columns(2)
with c1: btn_m = st.button("🚀 ANALIZA - CENA RYNKOWA", use_container_width=True)
with c2: btn_s = st.button("💎 ANALIZA - SUGEROWANA (LIMIT)", use_container_width=True)

if btn_m or btn_s:
    mode = "rynkowy" if btn_m else "sugerowany"
    raw_data = pobierz_dane_v4(wybrany_int)
    if raw_data is not None:
        wyniki_final = przetworz_v4(raw_data, mode)
        if wyniki_final:
            df = pd.DataFrame(wyniki_final).sort_values(by="Siła %", ascending=False)
            st.dataframe(stylizuj_v4(df), use_container_width=True)
            st.success("Dane zbuforowane. Kolejna analiza tego samego interwału będzie natychmiastowa.")
        else:
            st.warning("Pobrano dane, ale brak wystarczającej historii dla tego interwału. Spróbuj mniejszego.")
    else:
        st.error("Przekroczono limit zapytań Yahoo. Odczekaj 2-3 minuty i odśwież stronę (F5).")
