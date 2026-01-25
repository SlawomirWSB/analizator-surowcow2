import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf

# --- KONFIGURACJA ---
st.set_page_config(page_title="Skaner PRO - Ekspert V3", layout="wide")

KRYPTO_XTB = [
    "BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "ADA-USD", "DOT-USD", 
    "LINK-USD", "LTC-USD", "BCH-USD", "AVAX-USD", "MATIC-USD", "TRX-USD", 
    "UNI-USD", "ATOM-USD", "AAVE-USD"
]

interval_map = {
    "5 min": "5m", "15 min": "15m", "30 min": "30m", "1 godz": "1h", 
    "4 godz": "4h", "1 dzień": "1d", "1 tydz": "1wk", "1 mies": "1mo"
}

def pobierz_bezpieczny_okres(interwal):
    """Dobiera optymalny period, aby nie przeciążyć API i mieć dane do wskaźników."""
    mapa_okresow = {
        "5m": "1d", "15m": "5d", "30m": "5d", "1h": "30d", 
        "4h": "60d", "1d": "365d", "1wk": "730d", "1mo": "1825d"
    }
    return mapa_okresow.get(interwal, "60d")

def wykonaj_skan(tryb, interwal_label):
    wyniki = []
    interwal = interval_map[interwal_label]
    okres = pobierz_bezpieczny_okres(interwal)
    
    # Pasek postępu
    progress_bar = st.progress(0)
    total = len(KRYPTO_XTB)
    
    for i, symbol in enumerate(KRYPTO_XTB):
        try:
            # Pobieranie danych
            df = yf.download(symbol, period=okres, interval=interwal, progress=False, timeout=10)
            
            if df.empty or len(df) < 55: # Potrzebujemy min. 50 świec dla EMA50
                continue
            
            # Naprawa MultiIndex w kolumnach
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            # Obliczanie wskaźników
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
            vol_ratio = float(l['Volume'] / l['Vol_Avg']) if l['Vol_Avg'] > 0 else 1

            # Logika Sygnału
            sig = "KUP" if cena > ema20 else "SPRZEDAJ"
            
            # Scoring
            score = 40
            if (sig == "KUP" and l['MACD_12_26_9'] > l['MACDs_12_26_9']) or (sig == "SPRZEDAJ" and l['MACD_12_26_9'] < l['MACDs_12_26_9']): score += 20
            if vol_ratio > 1.1: score += 15
            if (sig == "KUP" and rsi < 50) or (sig == "SPRZEDAJ" and rsi > 50): score += 15
            if l['ADX_14'] > 25: score += 10

            # Dywergencja i Bollinger
            dyw = "BRAK"
            if sig == "KUP" and cena > prev['Close'] and rsi < prev['RSI_14']: dyw = "NIEDŹW."
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
                "Dyw.": dyw
            })
        except Exception as e:
            continue
        finally:
            progress_bar.progress((i + 1) / total)
            
    progress_bar.empty()
    return wyniki

# --- STYLIZACJA ---
def color_table(df):
    def apply_styles(row):
        formats = [''] * len(row)
        sig = row['Sygnał']
        
        # Kolumny: 0:Inst, 1:Syg, 2:Siła, 3:Wejscie, 4:TP, 5:SL, 6:Vol, 7:RSI, 8:BB, 9:Dyw
        formats[1] = 'background-color: #1e4620; color: white' if sig == 'KUP' else 'background-color: #5f1a1d; color: white'
        formats[2] = 'color: #00ff00; font-weight: bold' if row['Siła %'] > 70 else 'color: #ff4b4b'
        formats[6] = 'color: #00ff00' if row['Wolumen %'] > 100 else 'color: #ff4b4b'
        
        if sig == "KUP":
            formats[7] = 'color: #00ff00' if row['RSI'] < 50 else 'color: #ff4b4b'
        else:
            formats[7] = 'color: #00ff00' if row['RSI'] > 50 else 'color: #ff4b4b'
            
        return formats
    return df.style.apply(apply_styles, axis=1)

# --- UI ---
st.title("⚖️ Skaner PRO - System Ekspercki V3")

wybrany_interwal = st.select_slider("Wybierz interwał:", options=list(interval_map.keys()), value="4 godz")

col1, col2 = st.columns(2)
with col1:
    btn_m = st.button("🚀 ANALIZA - CENA RYNKOWA", use_container_width=True)
with col2:
    btn_s = st.button("💎 ANALIZA - SUGEROWANA (LIMIT)", use_container_width=True)

if btn_m or btn_s:
    tryb = "rynkowy" if btn_m else "sugerowany"
    dane = wykonaj_skan(tryb, wybrany_interwal)
    
    if dane:
        df_final = pd.DataFrame(dane).sort_values(by="Siła %", ascending=False)
        st.dataframe(color_table(df_final), use_container_width=True)
    else:
        st.error("Błąd pobierania danych. Spróbuj zmienić interwał lub odśwież stronę (F5).")
