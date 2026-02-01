def stylizuj(row, stopien_ryzyka): # Dodaliśmy stopien_ryzyka jako argument
    s = [''] * len(row)
    sig = row['Sygnał']
    
    # Próg kolorowania zależny od wybranego trybu
    stoch_threshold_buy = 50 if stopien_ryzyka == "Poluzowany" else 30
    stoch_threshold_sell = 50 if stopien_ryzyka == "Poluzowany" else 70

    # Sygnał - tło tylko dla akcji
    if sig == 'KUP': s[1] = 'background-color: #00ff00; color: black; font-weight: bold'
    elif sig == 'SPRZEDAJ': s[1] = 'background-color: #ff0000; color: white; font-weight: bold'
    
    # RSI - czcionka
    rsi = row['RSI']
    if rsi > 70: s[5] = 'color: #ff4b4b'
    elif rsi < 30: s[5] = 'color: #00ff00'
    
    # StochRSI - TERAZ DYNAMICZNY KOLOR
    stoch = row['StochRSI']
    if stoch < stoch_threshold_buy: s[6] = 'color: #00ff00'
    elif stoch > stoch_threshold_sell: s[6] = 'color: #ff4b4b'
    
    # Pęd, ADX, Wolumen - czcionka (ujednolicone)
    s[7] = 'color: #00ff00' if row['Pęd'] == 'Wzrost' else 'color: #ff4b4b'
    adx = row['ADX']
    if adx > 25: s[8] = 'color: #00ff00'
    elif adx < 20: s[8] = 'color: #ff9900'
    
    vol = row['Wolumen %']
    if vol > 110: s[9] = 'color: #00ff00'
    elif vol < 80: s[9] = 'color: #ff4b4b'

    v_h = float(row['Hist. 50ś'].replace('%',''))
    s[13] = 'color: #00ff00' if v_h > 0 else 'color: #ff4b4b' if v_h < 0 else ''
    
    return s
