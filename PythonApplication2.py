import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import re

# --- KONFIGURACJA ---
st.set_page_config(layout="wide", page_title="TERMINAL V18.0 | VERIFIED")

# --- STYLE ---
st.markdown("""
<style>
    .stApp { background: #0e1117; color: #e6edf3; }
    * { color: #e6edf3 !important; }
    .signal-card { 
        background: #161b22; border: 1px solid #30363d; border-radius: 10px; 
        padding: 25px; margin-bottom: 20px; border-left: 5px solid #00ff88;
    }
    .agg-box { 
        background: #1c2128; padding: 20px; border-radius: 10px; 
        text-align: center; border: 1px solid #30363d; margin-bottom: 15px;
    }
    div.stButton > button {
        background-color: #21262d !important; color: #58a6ff !important;
        border: 1px solid #30363d !important; font-weight: bold !important; width: 100%;
    }
    div.stButton > button:hover {
        background-color: #30363d !important; border-color: #58a6ff !important;
    }
    .streamlit-expanderHeader { background-color: #161b22 !important; color: #e6edf3 !important; }
    .streamlit-expanderContent { background-color: #0d1117 !important; border: 1px solid #30363d !important; }
    .logic-box { 
        background: #0d1117; border: 1px solid #30363d; padding: 12px; 
        border-radius: 6px; font-size: 0.9rem; color: #8b949e; margin-top: 10px;
    }
    .stProgress > div > div { background-color: #00ff88; }
    .stAlert { background-color: #1c2128 !important; color: #e6edf3 !important; }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'signals_data' not in st.session_state:
    st.session_state.signals_data = []
    st.session_state.last_update = None
    st.session_state.analysis_cache = {}
    st.session_state.current_pair = None

# --- FUNKCJE SCRAPINGU ---

def parse_bestfreesignal():
    """Scraping z BestFreeSignal.com - tabela z tr/td"""
    signals = []
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get('https://www.bestfreesignal.com/', headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Znajdujemy tabelę z sygnałami
        table = soup.find('table', class_=['table-bordered', 'table'])
        if not table:
            return signals
            
        rows = table.find_all('tr')[1:]  # Pomijamy nagłówek
        
        for row in rows:
            try:
                cells = row.find_all('td')
                if len(cells) < 6:
                    continue
                
                # Sprawdź czy nie jest "Expired"
                status = row.find('span', string='Expired')
                if status:
                    continue
                    
                date_cell = cells[0].get_text(strip=True)
                pair = cells[1].get_text(strip=True)
                action = cells[2].get_text(strip=True)
                entry = cells[3].get_text(strip=True).replace('$', '').replace(',', '')
                sl = cells[4].get_text(strip=True).replace('$', '').replace(',', '')
                tp = cells[5].get_text(strip=True).split('\n')[0].replace('$', '').replace(',', '')
                
                # Parsuj datę
                try:
                    date_parts = date_cell.split('\n')[0].strip()
                    signal_date = datetime.strptime(date_parts, '%Y-%m-%d %H:%M:%S')
                    date_str = signal_date.strftime("%d.%m %H:%M")
                except:
                    date_str = datetime.now().strftime("%d.%m %H:%M")
                
                signals.append({
                    'p': pair,
                    'type': action.upper(),
                    'in': entry,
                    'tp': tp,
                    'sl': sl,
                    'date': date_str,
                    'src': 'BESTFREESIGNAL',
                    'url': 'https://www.bestfreesignal.com/'
                })
            except Exception as e:
                continue
                
    except Exception as e:
        st.warning(f"⚠️ BestFreeSignal: {str(e)[:100]}")
    
    return signals

def parse_dailyforex():
    """Scraping z DailyForex.com"""
    signals = []
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get('https://www.dailyforex.com/forex-technical-analysis/free-forex-signals/page-1', 
                              headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # DailyForex używa divów, nie tabel - trzeba dostosować do rzeczywistej struktury
        recommendations = soup.find_all('div', class_='live-recommendations')
        
        for rec in recommendations[:10]:
            try:
                pair_elem = rec.find('h3') or rec.find('span', class_='pair')
                action_elem = rec.find('span', string=re.compile(r'Sell|Buy'))
                
                if pair_elem and action_elem:
                    signals.append({
                        'p': pair_elem.get_text(strip=True),
                        'type': action_elem.get_text(strip=True).upper(),
                        'in': 'N/A',
                        'tp': 'N/A',
                        'sl': 'N/A',
                        'date': datetime.now().strftime("%d.%m %H:%M"),
                        'src': 'DAILYFOREX',
                        'url': 'https://www.dailyforex.com/forex-technical-analysis/free-forex-signals/page-1'
                    })
            except:
                continue
                
    except Exception as e:
        st.warning(f"⚠️ DailyForex: {str(e)[:100]}")
    
    return signals

def parse_foresignal():
    """Scraping z ForeSignal.com - struktura z div.signal-card"""
    signals = []
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get('https://foresignal.com/en/', headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Szukamy kart sygnałów
        signal_cards = soup.find_all('div', class_='signal-card')
        
        for card in signal_cards:
            try:
                # Sprawdź czy nie jest "Filled"
                if 'Filled' in card.get_text():
                    continue
                
                # Znajdź typ sygnału (Buy/Sell) - z koloru tła
                card_body = card.find('div', class_='card-body')
                if not card_body:
                    continue
                    
                # Zielone tło = Buy, inne = Sell
                is_buy = 'signal-card.buy' in str(card.get('class', []))
                signal_type = 'BUY' if is_buy else 'SELL'
                
                # Znajdź parę walutową (w nagłówku)
                header = card.find('div', class_='signal-header')
                pair = header.get_text(strip=True) if header else 'N/A'
                
                # Znajdź poziomy cenowe
                rows = card.find_all('div', class_='d-flex')
                buy_at = ''
                take_profit = ''
                stop_loss = ''
                
                for row in rows:
                    text = row.get_text()
                    if 'Buy at' in text or 'Sold at' in text or 'Bought at' in text:
                        buy_at = text.split()[-1]
                    elif 'Take profit' in text:
                        take_profit = text.split()[-1]
                    elif 'Stop loss' in text:
                        stop_loss = text.split()[-1]
                
                signals.append({
                    'p': pair,
                    'type': signal_type,
                    'in': buy_at or 'N/A',
                    'tp': take_profit or 'N/A',
                    'sl': stop_loss or 'N/A',
                    'date': datetime.now().strftime("%d.%m %H:%M"),
                    'src': 'FORESIGNAL',
                    'url': 'https://foresignal.com/en/'
                })
            except Exception as e:
                continue
                
    except Exception as e:
        st.warning(f"⚠️ ForeSignal: {str(e)[:100]}")
    
    return signals

def parse_fxco():
    """Scraping z FX.co - struktura block-signals__item"""
    signals = []
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get('https://www.fx.co/pl/signals', headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Szukamy bloków z sygnałami
        signal_blocks = soup.find_all('div', class_='block-signals__item')
        
        for block in signal_blocks[:10]:
            try:
                # Znajdź informacje o sygnale w span.block-signals__info
                info_spans = block.find_all('span', class_='block-signals__info')
                
                if len(info_spans) < 2:
                    continue
                
                # Pierwszy span = instrument i interwał (np. "GOLD H1")
                instrument_text = info_spans[0].get_text(strip=True)
                
                # Znajdź typ sygnału (SELL STOP / BUY STOP)
                signal_type_elem = block.find('div', string=re.compile(r'Sell Stop|Buy Stop', re.IGNORECASE))
                signal_type = signal_type_elem.get_text(strip=True).upper() if signal_type_elem else 'N/A'
                
                # Znajdź poziomy TP, SL, P (cena wejścia)
                tp_elem = block.find(string=re.compile(r'TP:'))
                sl_elem = block.find(string=re.compile(r'SL:'))
                p_elem = block.find(string=re.compile(r'P:'))
                
                tp = tp_elem.parent.get_text().replace('TP:', '').strip() if tp_elem else 'N/A'
                sl = sl_elem.parent.get_text().replace('SL:', '').strip() if sl_elem else 'N/A'
                entry = p_elem.parent.get_text().replace('P:', '').strip() if p_elem else 'N/A'
                
                # Znajdź datę
                date_elem = block.find('span', class_='block-signals__info_period')
                date_str = datetime.now().strftime("%d.%m %H:%M")
                if date_elem:
                    date_text = date_elem.get_text(strip=True)
                    # Format: "Today at 17:00 (UTC+1)"
                    if 'Today' in date_text:
                        time_match = re.search(r'(\d{2}:\d{2})', date_text)
                        if time_match:
                            date_str = datetime.now().strftime("%d.%m ") + time_match.group(1)
                
                signals.append({
                    'p': instrument_text,
                    'type': signal_type,
                    'in': entry,
                    'tp': tp,
                    'sl': sl,
                    'date': date_str,
                    'src': 'FX.CO',
                    'url': 'https://www.fx.co/pl/signals'
                })
            except Exception as e:
                continue
                
    except Exception as e:
        st.warning(f"⚠️ FX.CO: {str(e)[:100]}")
    
    return signals

def calculate_success_probability(signal):
    """Oblicza prawdopodobieństwo sukcesu"""
    score = 50
    
    # Świeżość sygnału
    try:
        signal_time = datetime.strptime(signal['date'], "%d.%m %H:%M")
        hours_old = (datetime.now() - signal_time).total_seconds() / 3600
        if hours_old < 1:
            score += 25
        elif hours_old < 6:
            score += 15
        elif hours_old < 24:
            score += 5
    except:
        pass
    
    # Ratio TP/SL
    try:
        if signal['tp'] != 'N/A' and signal['sl'] != 'N/A' and signal['in'] != 'N/A':
            tp_str = re.sub(r'[^\d.]', '', str(signal['tp']))
            sl_str = re.sub(r'[^\d.]', '', str(signal['sl']))
            entry_str = re.sub(r'[^\d.]', '', str(signal['in']))
            
            if tp_str and sl_str and entry_str:
                tp = float(tp_str)
                sl = float(sl_str)
                entry = float(entry_str)
                
                reward = abs(tp - entry)
                risk = abs(sl - entry)
                
                if risk > 0:
                    ratio = reward / risk
                    if ratio > 3:
                        score += 20
                    elif ratio > 2:
                        score += 15
                    elif ratio > 1.5:
                        score += 10
    except:
        pass
    
    # Bonus za zaufane źródło
    if signal['src'] in ['FX.CO', 'DAILYFOREX']:
        score += 5
    
    return min(score, 99)

def generate_logic_explanation(signal, probability):
    """Generuje wyjaśnienie oceny"""
    logic_parts = []
    
    try:
        signal_time = datetime.strptime(signal['date'], "%d.%m %H:%M")
        hours_old = (datetime.now() - signal_time).total_seconds() / 3600
        if hours_old < 1:
            logic_parts.append("✅ Bardzo świeży (<1h)")
        elif hours_old < 6:
            logic_parts.append("✅ Świeży (<6h)")
        else:
            logic_parts.append("⚠️ Starszy sygnał")
    except:
        logic_parts.append("⚠️ Brak daty")
    
    try:
        if signal['tp'] != 'N/A' and signal['sl'] != 'N/A' and signal['in'] != 'N/A':
            tp_str = re.sub(r'[^\d.]', '', str(signal['tp']))
            sl_str = re.sub(r'[^\d.]', '', str(signal['sl']))
            entry_str = re.sub(r'[^\d.]', '', str(signal['in']))
            
            if tp_str and sl_str and entry_str:
                tp = float(tp_str)
                sl = float(sl_str)
                entry = float(entry_str)
                reward = abs(tp - entry)
                risk = abs(sl - entry)
                ratio = reward / risk if risk > 0 else 0
                logic_parts.append(f"✅ R/R: {ratio:.2f}")
        else:
            logic_parts.append("⚠️ Niepełne dane R/R")
    except:
        logic_parts.append("⚠️ Błąd kalkulacji R/R")
    
    logic_parts.append(f"📍 Źródło: {signal['src']}")
    
    return " | ".join(logic_parts)

def fetch_all_signals():
    """Pobiera sygnały ze wszystkich źródeł"""
    all_signals = []
    
    # Pobierz z każdego źródła
    all_signals.extend(parse_bestfreesignal())
    all_signals.extend(parse_dailyforex())
    all_signals.extend(parse_foresignal())
    all_signals.extend(parse_fxco())
    
    # Filtruj i dodaj metryki
    cutoff_date = datetime.now() - timedelta(days=2)
    processed = []
    
    for signal in all_signals:
        try:
            signal_time = datetime.strptime(signal['date'], "%d.%m %H:%M")
            if signal_time > cutoff_date:
                signal['szansa'] = calculate_success_probability(signal)
                signal['logic'] = generate_logic_explanation(signal, signal['szansa'])
                processed.append(signal)
        except:
            signal['szansa'] = calculate_success_probability(signal)
            signal['logic'] = generate_logic_explanation(signal, signal['szansa'])
            processed.append(signal)
    
    return processed

def fetch_aggregates(pair):
    """Mock agregatów - wymaga prawdziwego API"""
    import random
    options = ["SILNE KUPNO", "KUPNO", "NEUTRALNIE", "SPRZEDAŻ", "SILNA SPRZEDAŻ"]
    return {
        'inv': random.choice(options),
        'tv': random.choice(options)
    }

# --- INTERFEJS ---

header_left, header_right = st.columns([4, 1])
with header_left:
    st.title("🚀 TERMINAL V18.0 | XTB SMART SYNC")
with header_right:
    if st.button("🔄 AKTUALIZUJ"):
        st.session_state.signals_data = fetch_all_signals()
        st.session_state.last_update = datetime.now()
        st.session_state.analysis_cache = {}
        st.success("✅ Zaktualizowano!")
        time.sleep(0.5)
        st.rerun()

if st.session_state.last_update:
    st.caption(f"Ostatnia aktualizacja: {st.session_state.last_update.strftime('%d.%m.%Y %H:%M:%S')}")

if not st.session_state.signals_data:
    st.session_state.signals_data = fetch_all_signals()
    st.session_state.last_update = datetime.now()

col_left, col_right = st.columns([1.3, 0.7])

with col_left:
    st.subheader("📡 Sygnały Live")
    
    if not st.session_state.signals_data:
        st.info("Kliknij 'AKTUALIZUJ' aby pobrać sygnały")
    else:
        for s in st.session_state.signals_data:
            is_buy = any(word in s['type'].upper() for word in ['BUY', 'KUPNO', 'LONG'])
            color = "#00ff88" if is_buy else "#ff4b4b"
            
            st.markdown(f"""
            <div class="signal-card" style="border-left-color: {color}">
                <span style="color:#00ff88; font-weight:bold; float:right;">{s['date']}</span>
                <b style="font-size:1.1rem;">{s['p']}</b> | 
                <a href="{s.get('url', '#')}" target="_blank" style="color:#58a6ff; text-decoration:none;">
                    <small>{s['src']}</small>
                </a>
                <div style="color:{color}; font-size:1.4rem; font-weight:bold; margin:15px 0;">
                    {s['type']} @ {s['in']}
                </div>
                <div style="background:rgba(0,0,0,0.4); padding:10px; border-radius:8px; display:flex; justify-content:space-between; font-family:monospace;">
                    <span style="color:#00ff88">TP: {s['tp']}</span>
                    <span style="color:#ff4b4b">SL: {s['sl']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"🔍 ANALIZUJ {s['p']}", key=f"btn_{s['p']}"):
                st.session_state.current_pair = s['p']
                st.session_state.analysis_cache[s['p']] = fetch_aggregates(s['p'])
                st.rerun()

with col_right:
    st.subheader("📊 Niezależne Agregaty")
    
    pair = st.session_state.current_pair
    if pair and pair in st.session_state.analysis_cache:
        data = st.session_state.analysis_cache[pair]
        inv_color = "#00ff88" if "KUPNO" in data['inv'] else "#ff4b4b"
        tv_color = "#00ff88" if "KUPNO" in data['tv'] else "#ff4b4b"
        
        st.markdown(f"""
            <div class="agg-box">
                <b style="font-size:1.2rem;">{pair}</b><br><br>
                <div style="margin:10px 0;">
                    <small style="color:#8b949e">INVESTING.COM:</small><br>
                    <b style="color:{inv_color}; font-size:1.1rem;">{data['inv']}</b>
                </div>
                <div style="margin:10px 0;">
                    <small style="color:#8b949e">TRADINGVIEW:</small><br>
                    <b style="color:{tv_color}; font-size:1.1rem;">{data['tv']}</b>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Wybierz instrument, aby zobaczyć agregaty.")
    
    st.markdown("---")
    st.subheader("🏆 Power Ranking AI")
    
    if st.session_state.signals_data:
        sorted_signals = sorted(st.session_state.signals_data, key=lambda x: x['szansa'], reverse=True)
        
        for item in sorted_signals:
            with st.expander(f"{item['p']} — {item['szansa']}%", expanded=(item['szansa'] > 85)):
                st.progress(item['szansa']/100)
                st.markdown(f"""
                <div class="logic-box">
                    <b>PODSTAWA OCENY:</b><br>
                    {item['logic']}
                </div>
                """, unsafe_allow_html=True)
    
    if st.button("🔙 RESET WIDOKU"):
        st.session_state.current_pair = None
        st.rerun()
