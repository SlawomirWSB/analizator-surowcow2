def analizuj(df_raw, name, kapital, tryb, ryzyko):
    try:
        df = df_raw.copy()
        # Optymalizacja wskaźników - liczymy raz
        df.ta.rsi(append=True); df.ta.ema(length=20, append=True)
        df.ta.adx(append=True); df.ta.atr(append=True); df.ta.macd(append=True)
        df.ta.stochrsi(append=True)
        df['V_Avg'] = df['Volume'].rolling(20).mean()
        
        # KRYTYCZNE: Bierzemy ostatnią ZAMKNIĘTĄ świecę (iloc[-2]), aby uniknąć repaintingu
        # Do aktualnej ceny rynkowej bierzemy iloc[-1]
        l = df.iloc[-2] 
        curr = df.iloc[-1] 
        c_zamkniete = float(l['Close'])
        c_akt = float(curr['Close']) 
        
        ema, atr = float(l['EMA_20']), float(l['ATRr_14'])
        adx, rsi, stoch = float(l['ADX_14']), float(l['RSI_14']), float(l['STOCHRSIk_14_14_3_3'])
        macd_h = float(l['MACDh_12_26_9'])
        
        # Zabezpieczenie przed brakiem wolumenu (szczególnie FX/Indeksy na YF)
        if pd.isna(l['Volume']) or l['Volume'] == 0 or l['V_Avg'] == 0:
            v_rat = 100.0
        else:
            v_rat = (float(l['Volume'] / l['V_Avg']) * 100)
        
        adx_min = 18 if ryzyko == "Poluzowany" else 25
        st_b, st_s = (55, 45) if ryzyko == "Poluzowany" else (35, 65)
        
        long = (c_zamkniete > ema) and (adx > adx_min) and (stoch < st_b) and (macd_h > 0)
        short = (c_zamkniete < ema) and (adx > adx_min) and (stoch > st_s) and (macd_h < 0)
        
        sig = "KUP" if long else "SPRZEDAJ" if short else "CZEKAJ"
        wej = ema if tryb == "Limit (EMA20)" else c_akt
        
        # Dodanie minimalnego bufora na spread (np. 0.1 * ATR) z dala od szumu
        sl_buffer = atr * 0.1
        sl = wej - (atr * 1.5) - sl_buffer if sig == "KUP" else wej + (atr * 1.5) + sl_buffer
        tp = wej + (atr * 2.5) if sig == "KUP" else wej - (atr * 2.5)
        
        # Usunąłem mylący backtest, który testował tylko EMA. Zamiast fałszywych 
        # danych, skupiamy się na jakości bieżącego sygnału.
        
        return {
            "Instrument": name, "Sygnał": sig, "Siła %": (90 if sig in ["KUP", "SPRZEDAJ"] else 50),
            "Cena Rynkowa": round(c_akt, 4), "Cena Wejścia": round(wej, 4), "RSI": round(rsi, 1),
            "StochRSI": round(stoch, 1), "Pęd": "Wzrost" if macd_h > 0 else "Spadek",
            "ADX": round(adx, 1), "Wolumen %": round(v_rat), 
            "Ile (1%)": round((kapital*0.01)/abs(wej-sl), 4) if abs(wej-sl) > 0 else 0,
            "TP": round(tp, 4), "SL": round(sl, 4)
        }
    except Exception as e:
        # Warto logować błędy w konsoli, by wiedzieć który ticker wyrzuca błąd
        # print(f"Błąd dla {name}: {e}") 
        return None
