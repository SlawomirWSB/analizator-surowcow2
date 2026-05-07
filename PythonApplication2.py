//@version=5
indicator("Skaner PRO V9.6 - Decision Support", overlay=true)

// --- ⚙️ USTAWIENIA ---
ryzyko = input.string("Rygorystyczny", title="Tryb Ryzyka", options=["Poluzowany", "Rygorystyczny"])
kapital = input.float(10000, title="Kapitał (PLN)")

// --- 📊 WSKAŹNIKI (Obliczane na bieżąco) ---
ema20 = ta.ema(close, 20)
[diplus, diminus, adx_val] = ta.dmi(14, 14)
rsi14 = ta.rsi(close, 14)
stochK = ta.sma(ta.stoch(rsi14, rsi14, rsi14, 14), 3)
[macdLine, signalLine, histLine] = ta.macd(close, 12, 26, 9)
atr_val = ta.atr(14)

// --- 🧠 LOGIKA (Zamknięta Świeca = Indeks [1]) ---
adx_min = ryzyko == "Poluzowany" ? 18 : 25
st_b = ryzyko == "Poluzowany" ? 55 : 35
st_s = ryzyko == "Poluzowany" ? 45 : 65

// Bierzemy dane z poprzedniej (zamkniętej) świecy, aby uniknąć repaintingu!
c_zamkniete = close[1]
ema = ema20[1]
adx = adx_val[1]
stoch = stochK[1]
macd_h = histLine[1]
atr = atr_val[1]

longCondition = (c_zamkniete > ema) and (adx > adx_min) and (stoch < st_b) and (macd_h > 0)
shortCondition = (c_zamkniete < ema) and (adx > adx_min) and (stoch > st_s) and (macd_h < 0)

// Filtr: generujemy sygnał tylko raz na zmianę trendu (nie spamujemy co świecę)
var int pozycja = 0
if longCondition
    pozycja := 1
else if shortCondition
    pozycja := -1

nowyLong = longCondition and pozycja[1] <= 0
nowyShort = shortCondition and pozycja[1] >= 0

// --- 🎯 KALKULACJA POZYCJI ---
wejscie = open // Otwarcie obecnej świecy = nasze wejście po rynkowej
sl_buffer = atr * 0.1

sl_long = wejscie - (atr * 1.5) - sl_buffer
tp_long = wejscie + (atr * 2.5)

sl_short = wejscie + (atr * 1.5) + sl_buffer
tp_short = wejscie - (atr * 2.5)

// --- 🖌️ RYSOWANIE NA WYKRESIE ---
plot(ema20, color=color.new(color.blue, 0), title="EMA 20", linewidth=2)

plotshape(series=nowyLong, title="Sygnał KUP", location=location.belowbar, color=color.new(color.green, 0), style=shape.labelup, text="KUP", textcolor=color.white, size=size.small)
plotshape(series=nowyShort, title="Sygnał SPRZEDAJ", location=location.abovebar, color=color.new(color.red, 0), style=shape.labeldown, text="SELL", textcolor=color.white, size=size.small)

// --- 📡 GENEROWANIE ALERTÓW (JSON DLA TELEGRAMA) ---
// Formatyzujemy wiadomość jako JSON, aby łatwo przekazać ją do Make.com / Telegrama
if nowyLong
    msgLong = '{"Sygnal": "🟢 KUP", "Instrument": "' + syminfo.ticker + '", "Cena": ' + str.tostring(wejscie, "#.##") + ', "SL": ' + str.tostring(sl_long, "#.##") + ', "TP": ' + str.tostring(tp_long, "#.##") + '}'
    alert(msgLong, alert.freq_once_per_bar_close)

if nowyShort
    msgShort = '{"Sygnal": "🔴 SPRZEDAJ", "Instrument": "' + syminfo.ticker + '", "Cena": ' + str.tostring(wejscie, "#.##") + ', "SL": ' + str.tostring(sl_short, "#.##") + ', "TP": ' + str.tostring(tp_short, "#.##") + '}'
    alert(msgShort, alert.freq_once_per_bar_close)
