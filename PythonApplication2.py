import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf

# --- KONFIGURACJA ---
st.set_page_config(page_title="Skaner PRO V5 - Hybryda", layout="wide")

KRYPTO = [
    "BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "ADA-USD", "DOT-USD", 
    "LINK-USD", "LTC-USD", "AVAX-USD", "MATIC-USD"
]

interval_map = {
    "5 min": "5m", "15 min": "15m", "30 min": "30m", "1 godz": "1h", 
    "4 godz": "4h", "1 dzień": "1d"
}

@st.cache_data(ttl=600)
def pobierz_dane_v5(interwal_label):
    interwal = interval_map[interwal_label]
    okres = "60d" if interwal in ["1h", "4h", "5m", "15m", "30m"] else "2y"
    try:
        # Pobieramy dane grupowo dla szybkości
        data = yf.download(KRYPTO, period=okres, interval=interwal, group_by='ticker', progress=False)
        return data
    except Exception as e:
        st.error(f"Błąd yfinance: {e}")
        return None

def run_backtest(df):
    """Uproszczony backtest strategii opartej na EMA20 dla 50 ostatnich świec"""
    if len(df) < 50: return 0
    test_data = df.tail(50).copy()
    test_data['EMA'] = ta.ema(test_data['Close'], length=20)
    
    initial_cap = 1000
    cap = initial_cap
    pos = 0
    
    for i in range(1, len(test_data)):
        price = test_data['Close'].iloc[i]
        ema = test_data['EMA'].iloc[i]
        
        if price > ema and pos == 0:
            pos = cap / price
        elif price < ema and pos > 0:
            cap = pos * price
            pos = 0
            
    final_val = cap if pos == 0 else pos * test_data['Close'].iloc[-1]
    return round(((final_val - initial_cap) / initial_cap) * 100, 2)

def przetworz_v5(data, tryb):
    if data is None: return []
    wyniki = []
    for symbol in KRYPTO:
        try:
            df = data[symbol].dropna()
            if len(df) < 35: continue
            
            # Wskaźniki PRO
            df.ta.rsi(length=14, append=True)
            df.ta.ema(length=20, append=True)
            df.ta.adx(length=14, append=True)
            df.ta.atr(length=14, append=True)
            df['Vol_Avg'] = df['Volume'].rolling(20).mean()
            
            l = df.iloc[-1]
            cena = float(l['Close'])
            ema20 = float(l['EMA_20'])
            adx = float(l['ADX_14'])
            rsi = float(l['RSI_14'])
            atr = float(l['ATRr_14'])
            
            # Logika sygnału i scoringu
            sig = "KUP" if cena > ema20 else "SPRZEDAJ"
            if adx < 20: sig = "KONSOLIDACJA"
            
            score = 40
            if adx > 25: score += 20
            if (sig == "KUP" and rsi < 60) or (sig == "SPRZEDAJ" and rsi > 40): score += 20
            if l['Volume'] > l['Vol_Avg'] * 1.1: score += 20
            
            # Backtesting historyczny dla tego symbolu
            hist_perf = run_backtest(df)
            
            wej = cena if tryb == "rynkowy" else ema20
            
            wyniki.append({
                "Instrument": symbol.replace("-USD", ""),
                "Sygnał": sig,
                "Siła %": min(score, 98) if sig != "KONSOLIDACJA" else 0,
                "Cena": round(cena, 4),
                "RSI": round(rsi, 1),
                "ADX": round(adx, 1),
                "Hist. 50 świec": f"{hist_perf}%",
                "TP (Cel)": round(wej + (atr*2.5) if sig=="KUP" else wej - (atr*2.5), 4),
                "SL (Stop)": round(wej - (atr*1.5) if sig=="KUP" else wej + (atr*1.5), 4)
            })
        except: continue
    return wyniki

# --- UI ---
st.title("⚖️ Skaner PRO - System Ekspercki V5")
wybrany_int = st.select_slider("Wybierz interwał:", options=list(interval_map.keys()), value="4 godz")

c1, c2 = st.columns(2)
with c1: btn_m = st.button("🚀 ANALIZA - CENA RYNKOWA", use_container_width=True)
with c2: btn_s = st.button("💎 ANALIZA - SUGEROWANA (LIMIT)", use_container_width=True)

if btn_m or btn_s:
    mode = "rynkowy" if btn_m else "sugerowany"
    with st.spinner('Pobieranie i analiza danych...'):
        raw_data = pobierz_dane_v5(wybrany_int)
        if raw_data is not None:
            finalne = przetworz_v5(raw_data, mode)
            if finalne:
                df_res = pd.DataFrame(finalne).sort_values(by="Siła %", ascending=False)
                
                # Stylizacja tabeli
                def stylizuj(row):
                    s = [''] * len(row)
                    if row['Sygnał'] == 'KUP': s[1] = 'background-color: #1e4620'
                    elif row['Sygnał'] == 'SPRZEDAJ': s[1] = 'background-color: #5f1a1d'
                    return s

                st.dataframe(df_res.style.apply(stylizuj, axis=1), use_container_width=True)
                st.caption("Pamiętaj: 'Hist. 50 świec' to symulacja zysku/straty dla strategii EMA20 na ostatnim odcinku czasu.")
            else:
                st.warning("Brak wystarczającej ilości danych.")
