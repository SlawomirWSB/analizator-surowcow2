import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf

# Konfiguracja i lista krypto (XTB)
st.set_page_config(page_title="Skaner PRO - Color Analytics", layout="wide")
KRYPTO_XTB = ["BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "ADA-USD", "DOT-USD", "LINK-USD", "LTC-USD", "AVAX-USD", "MATIC-USD"]
interval_map = {"5 min": "5m", "15 min": "15m", "1 godz": "1h", "4 godz": "4h", "1 dzień": "1d", "1 tydz": "1wk"}

def wykonaj_skan(tryb, interwal_label):
    wyniki = []
    interwal = interval_map[interwal_label]
    period = "60d" if "h" in interwal or "m" in interwal else "max"
    
    for symbol in KRYPTO_XTB:
        try:
            df = yf.download(symbol, period=period, interval=interwal, progress=False)
            if df.empty or len(df) < 50: continue
            if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)

            df.ta.rsi(length=14, append=True)
            df.ta.ema(length=20, append=True)
            df.ta.atr(length=14, append=True)
            df.ta.adx(length=14, append=True)
            df['Vol_Avg'] = df['Volume'].rolling(window=20).mean()
            
            l = df.iloc[-1]
            cena = float(l['Close'])
            rsi = float(l['RSI_14'])
            vol_ratio = float(l['Volume'] / l['Vol_Avg'])
            ema20 = float(l['EMA_20'])
            
            # Prosty model decyzyjny dla kierunku
            sig = "KUP" if cena > ema20 else "SPRZEDAJ"
            
            # Obliczanie siły (uproszczone dla prezentacji kolorów)
            power = 50
            if sig == "KUP":
                if rsi < 50: power += 20
                if vol_ratio > 1.1: power += 20
            else:
                if rsi > 50: power += 20
                if vol_ratio > 1.1: power += 20

            wejscie = cena if tryb == "rynkowy" else ema20
            atr = l['ATRr_14']
            
            wyniki.append({
                "Instrument": symbol.replace("-USD", ""),
                "Sygnał": sig,
                "Siła %": min(power, 98),
                "Cena Wejścia": round(wejscie, 4),
                "Wolumen %": round(vol_ratio * 100),
                "TP (Cel)": round(wejscie + (atr*2.5) if sig=="KUP" else wejscie - (atr*2.5), 4),
                "SL (Stop)": round(wejscie - (atr*1.5) if sig=="KUP" else wejscie + (atr*1.5), 4),
                "RSI": round(rsi, 1)
            })
        except: continue
    return wyniki

# --- LOGIKA KOLOROWANIA ---
def style_dataframe(df):
    def apply_colors(row):
        styles = [''] * len(row)
        sig = row['Sygnał']
        
        # Kolor dla Sygnału (Pełne tło)
        styles[1] = 'background-color: #1e4620; color: white' if sig == 'KUP' else 'background-color: #5f1a1d; color: white'
        
        # Kolor dla Siły %
        styles[2] = 'color: #00ff00' if row['Siła %'] > 70 else 'color: #ff4b4b'
        
        # Kolor dla Wolumenu (Zielony jeśli > 100% - potwierdza ruch)
        styles[4] = 'color: #00ff00' if row['Wolumen %'] > 100 else 'color: #ff4b4b'
        
        # Kolor dla RSI (Warunkowy względem Sygnału)
        if sig == "KUP":
            styles[7] = 'color: #00ff00' if row['RSI'] < 50 else 'color: #ff4b4b'
        else:
            styles[7] = 'color: #00ff00' if row['RSI'] > 50 else 'color: #ff4b4b'
            
        return styles

    return df.style.apply(apply_colors, axis=1)

# --- UI ---
st.title("⚖️ Skaner PRO - Inteligentne Kolorowanie")
int_sel = st.select_slider("Interwał:", options=list(interval_map.keys()), value="4 godz")
c1, c2 = st.columns(2)
with c1: btn_m = st.button("🚀 CENA RYNKOWA", use_container_width=True)
with c2: btn_s = st.button("💎 CENA SUGEROWANA", use_container_width=True)

if btn_m or btn_s:
    res = wykonaj_skan("rynkowy" if btn_m else "sugerowany", int_sel)
    if res:
        df = pd.DataFrame(res).sort_values(by="Siła %", ascending=False)
        st.dataframe(style_dataframe(df), use_container_width=True)
        st.caption("Legenda: Zielone wartości w RSI/Wolumen oznaczają potwierdzenie sygnału. Czerwone - ostrzeżenie.")
