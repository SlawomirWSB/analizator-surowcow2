import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf

# --- KONFIGURACJA ---
st.set_page_config(page_title="Skaner PRO - Ekspert V2", layout="wide")

KRYPTO_XTB = [
    "BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "ADA-USD", "DOT-USD", 
    "LINK-USD", "LTC-USD", "BCH-USD", "AVAX-USD", "MATIC-USD", "TRX-USD", 
    "UNI-USD", "ATOM-USD", "AAVE-USD"
]

interval_map = {
    "5 min": "5m", "15 min": "15m", "30 min": "30m", "1 godz": "1h", 
    "4 godz": "4h", "1 dzień": "1d", "1 tydz": "1wk", "1 mies": "1mo"
}

def wykonaj_skan(tryb, interwal_label):
    wyniki = []
    interwal = interval_map[interwal_label]
    # Określenie okresu pobierania danych
    if interwal in ["5m", "15m", "30m"]: period = "7d"
    elif interwal in ["1h", "4h"]: period = "60d"
    else: period = "max"
    
    for symbol in KRYPTO_XTB:
        try:
            df = yf.download(symbol, period=period, interval=interwal, progress=False)
            if df.empty or len(df) < 50: continue
            if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)

            # Wskaźniki
            df.ta.rsi(length=14, append=True)
            df.ta.ema(length=20, append=True)
            df.ta.ema(length=50, append=True)
            df.ta.atr(length=14, append=True)
            df.ta.macd(append=True)
            df.ta.adx(length=14, append=True)
            df.ta.bbands(length=20, append=True)
            df['Vol_Avg'] = df['Volume'].rolling(window=20).mean()
            
            l = df.iloc[-1]
            prev = df.iloc[-2]
            cena = float(l['Close'])
            rsi = float(l['RSI_14'])
            ema20 = float(l['EMA_20'])
            vol_ratio = float(l['Volume'] / l['Vol_Avg']) if l['Vol_Avg'] != 0 else 1

            # Logika Sygnału i Siły
            sig = "KUP" if cena > ema20 else "SPRZEDAJ"
            score = 40
            if (sig == "KUP" and l['MACD_12_26_9'] > l['MACDs_12_26_9']) or (sig == "SPRZEDAJ" and l['MACD_12_26_9'] < l['MACDs_12_26_9']): score += 20
            if vol_ratio > 1.1: score += 15
            if (sig == "KUP" and rsi < 50) or (sig == "SPRZEDAJ" and rsi > 50): score += 15
            if l['ADX_14'] > 25: score += 10

            # Dywergencja i BB
            dyw = "BRAK"
            if sig == "KUP" and cena > prev['Close'] and rsi < prev['RSI_14']: dyw = "NIEDŹWIEDZIA"
            if sig == "SPRZEDAJ" and cena < prev['Close'] and rsi > prev['RSI_14']: dyw = "BYCZA"

            bb_stat = "Wewnątrz"
            if cena > l['BBU_20_2.0']: bb_stat = "Wybicie Górą"
            elif cena < l['BBL_20_2.0']: bb_stat = "Wybicie Dołem"

            wejscie = cena if tryb == "rynkowy" else ema20
            atr = l['ATRr_14']

            wyniki.append({
                "Instrument": symbol.replace("-USD", ""),
                "Sygnał": sig,
                "Siła %": min(score, 98),
                "Cena Wejścia": round(wejscie, 4),
                "TP (Cel)": round(wejscie + (atr*2.5) if sig=="KUP" else wejscie - (atr*2.5), 4),
                "SL (Stop)": round(wejscie - (atr*1.5) if sig=="KUP" else wejscie + (atr*1.5), 4),
                "Wolumen %": round(vol_ratio * 100),
                "RSI": round(rsi, 1),
                "BB Status": bb_stat,
                "Dywergencja": dyw
            })
        except: continue
    return wyniki

# --- STYLIZACJA ---
def color_table(df):
    def apply_styles(row):
        # Neutralny start
        formats = [''] * len(row)
        sig = row['Sygnał']
        
        # 1. Sygnał (Tło)
        formats[1] = 'background-color: #1e4620; color: white' if sig == 'KUP' else 'background-color: #5f1a1d; color: white'
        
        # 2. Siła %
        formats[2] = 'color: #00ff00; font-weight: bold' if row['Siła %'] > 70 else 'color: #ff4b4b'
        
        # 3. Wolumen
        formats[6] = 'color: #00ff00' if row['Wolumen %'] > 100 else 'color: #ff4b4b'
        
        # 4. RSI
        if sig == "KUP":
            formats[7] = 'color: #00ff00' if row['RSI'] < 50 else 'color: #ff4b4b'
        else:
            formats[7] = 'color: #00ff00' if row['RSI'] > 50 else 'color: #ff4b4b'
            
        return formats

    return df.style.apply(apply_styles, axis=1)

# --- UI ---
st.title("⚖️ Skaner PRO - System Ekspercki V2")

# Suwak interwału
wybrany_interwal = st.select_slider("Wybierz interwał:", options=list(interval_map.keys()), value="4 godz")

col1, col2 = st.columns(2)
with col1:
    btn_m = st.button("🚀 ANALIZA - CENA RYNKOWA", use_container_width=True)
with col2:
    btn_s = st.button("💎 ANALIZA - SUGEROWANA (LIMIT)", use_container_width=True)

# Obsługa przycisków
if btn_m or btn_s:
    tryb = "rynkowy" if btn_m else "sugerowany"
    with st.spinner("Pobieranie i analiza danych..."):
        dane = wykonaj_skan(tryb, wybrany_interwal)
        
    if dane:
        df_final = pd.DataFrame(dane).sort_values(by="Siła %", ascending=False)
        st.dataframe(color_table(df_final), use_container_width=True)
        st.success(f"Zakończono skanowanie dla interwału: {wybrany_interwal}")
    else:
        st.warning("Brak danych dla wybranego interwału. Spróbuj zwiększyć interwał (np. na 1 godz).")
