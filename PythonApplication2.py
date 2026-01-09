with tab1:
        # Panel Wyboru
        c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
        with c1: rynek = st.selectbox("Wybierz rynek:", list(DB.keys()), index=0)
        with c2: inst = st.selectbox("Instrument:", list(DB[rynek].keys()), index=0)
        with c3: itv = st.selectbox("Interwał:", ["1", "5", "15", "60", "D"], index=1)
        with c4: audio = st.checkbox("Dźwięk", value=True)

        symbol = DB[rynek][inst]

        st.subheader("🤖 Analiza Wielu Wskaźników")
        col_sig1, col_sig2 = st.columns(2)

        with col_sig1:
            st.markdown("<p style='text-align:center; color:gray;'>Podsumowanie (Zegar)</p>", unsafe_allow_html=True)
            tech_code = f"""
            <div style="display: flex; justify-content: center; background: #131722; padding: 10px; border-radius: 10px;">
              <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
              {{
              "interval": "{itv}m" if "{itv}".isdigit() else "1D",
              "width": "100%", "height": 450,
              "isTransparent": true, "symbol": "{symbol}",
              "showIntervalTabs": false, "displayMode": "single",
              "locale": "pl", "colorTheme": "dark"
            }}
              </script>
            </div>
            """
            components.html(tech_code, height=480)

        with col_sig2:
            st.markdown("<p style='text-align:center; color:gray;'>Szczegóły (Wskaźniki)</p>", unsafe_allow_html=True)
            # Używamy stabilnego widgetu TradingView w wersji tabelarycznej zamiast Investing.com
            detailed_code = f"""
            <div style="border-radius: 10px; overflow: hidden; background: #131722; padding: 10px;">
              <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
              {{
              "interval": "{itv}m" if "{itv}".isdigit() else "1D",
              "width": "100%", "height": 450,
              "isTransparent": true, "symbol": "{symbol}",
              "showIntervalTabs": true, "displayMode": "multiple",
              "locale": "pl", "colorTheme": "dark"
            }}
              </script>
            </div>
            """
            components.html(detailed_code, height=480)

        # Wykres Główny
        st.markdown("---")
        # ... tutaj zostawiasz kod wykresu bez zmian ...
