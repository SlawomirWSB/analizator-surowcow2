import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf

# Rozszerzona lista o najważniejsze projekty z XTB
KRYPTO_XTB = [
    "BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "ADA-USD", "DOT-USD", 
    "LINK-USD", "LTC-USD", "BCH-USD", "AVAX-USD", "MATIC-USD", "TRX-USD", 
    "UNI-USD", "ATOM-USD", "ETC-USD", "ALGO-USD", "AAVE-USD"
]

# Mapowanie suwaka na interwały techniczne
interval_map = {
    "5 min": "5m", "15 min": "15m", "30 min": "30m", "1 godz": "1h", 
    "4 godz": "4h", "1 dzień": "1d", "1 tydz": "1wk", "1 mies": "1mo"
}

def wykonaj_skan(tryb="rynkowy", interwal_label="4 godz"):
    wyniki = []
    interwal = interval_map[interwal_label]
    
    # Wybór okresu pobierania danych w zależności od interwału
    period = "60d" if "h" in interwal or "m" in interwal else "max"
    
    for symbol in KRYPTO_XTB:
        try:
            df = yf.download(symbol, period=period, interval=interwal, progress=False)
            if df.empty or len(df) < 50: continue
            if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)

            # --- ANALIZA TECHNICZNA ---
            df.ta.rsi(length=14, append=True)
            df.ta.ema(length=20, append=True)
            df.ta.ema(length=50, append=True)
            df.ta.atr(length=14, append=True)
            df.ta.macd(append=True)
            df.ta.adx(append=True)
            
            # Obliczanie średniego wolumenu z 20 ostatnich świec
            df['Vol_Avg'] = df['Volume'].rolling(window=20).mean()
            
            l = df.iloc[-1]
            prev = df.iloc[-2]
            
            cena_r = float(l['Close'])
            rsi = float(l['RSI_14'])
            adx = float(l['ADX_14'])
            vol_ratio = float(l['Volume'] / l['Vol_Avg']) # Stosunek obecnego wolumenu do średniej

            # --- WYRAFINOWANY SCORING ---
            score = 30
            if cena_r > l['EMA_20']: score += 10
            if l['EMA_20'] > l['EMA_50']: score += 10
            if l['MACD_12_26_9'] > l['MACDs_12_26_9']: score += 15
            if rsi < 40: score += 15
            if adx > 25: score += 10
            if vol_ratio > 1.2: score += 10 # Bonus za wysoki wolumen (popyt)

            # Określenie kierunku
            sig = "KUP" if l['MACD_12_26_9'] > l['MACDs_12_26_9'] else "SPRZEDAJ"
            
            # Logika wejścia
            if tryb == "rynkowy":
                wejscie = cena_r
            else:
                # Sugerowane: wejście przy EMA20 (zdrowsze RR)
                wejscie = l['EMA_20']

            atr = l['ATRr_14']
            wyniki.append({
                "Instrument": symbol.replace("-USD", ""),
                "Sygnał": sig,
                "Siła %": min(power := score, 98),
                "Cena Wejścia": round(wejscie, 4),
                "Wolumen (vs Śr)": f"{round(vol_ratio * 100)}%",
                "TP (Cel)": round(wejscie + (atr*2.5) if sig=="KUP" else wejscie - (atr*2.5), 4),
                "SL (Stop)": round(wejscie - (atr*1.5) if sig=="KUP" else wejscie + (atr*1.5), 4),
                "RSI": round(rsi, 1)
            })
        except: continue
    return wyniki

# --- UI ---
st.set_page_config(layout="wide")
st.title("⚖️ Skaner PRO - Multi-Interwał & Wolumen")

int_sel = st.select_slider("Wybierz interwał (od 5m do 1M):", options=list(interval_map.keys()), value="4 godz")

col1, col2 = st.columns(2)
with col1:
    btn_market = st.button("🚀 ANALIZA - CENA RYNKOWA", use_container_width=True)
with col2:
    btn_sug = st.button("💎 ANALIZA - SUGEROWANA (LIMIT)", use_container_width=True)

if btn_market or btn_sug:
    tryb = "rynkowy" if btn_market else "sugerowany"
    wyniki = wykonaj_skan(tryb, int_sel)
    
    if wyniki:
        df = pd.DataFrame(wyniki).sort_values(by="Siła %", ascending=False)
        
        # Stylizacja
        def style_rows(row):
            bg = '#1e4620' if row['Sygnał'] == 'KUP' else '#5f1a1d'
            return [f'background-color: {bg}; color: white'] * len(row)

        st.dataframe(df.style.apply(style_rows, axis=1), use_container_width=True)
        st.info("💡 Wskazówka: Szukaj Wolumenu > 100%. Oznacza to, że obecna świeca ma większe zainteresowanie niż średnia z ostatnich 20 okresów.")
