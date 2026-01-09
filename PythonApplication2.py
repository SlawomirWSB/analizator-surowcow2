with tab1:
        # Panel Wyboru
        c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
        with c1: rynek = st.selectbox("Wybierz rynek:", list(DB.keys()), index=0)
        with c2: inst = st.selectbox("Instrument:", list(DB[rynek].keys()), index=0)
        with c3: itv = st.selectbox("Interwał:", ["1", "5", "15", "60", "D"], index=1)
        with c4: audio = st.checkbox("Dźwięk", value=True)

        symbol = DB[rynek][inst]

        # --- DWA ŹRÓDŁA SYGNAŁÓW OBOK SIEBIE ---
        col_signal1, col_signal2 = st.columns(2)

        with col_signal1:
            st.markdown("<p style='text-align:center; color:gray;'>Źródło 1: TradingView</p>", unsafe_allow_html=True)
            tech_code = f"""
            <div style="height: 450px; background: #131722; border-radius: 10px; padding: 5px;">
              <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
              {{
              "interval": "{itv}m" if "{itv}".isdigit() else "1D",
              "width": "100%", "height": 420,
              "isTransparent": true, "symbol": "{symbol}",
              "showIntervalTabs": false, "displayMode": "single",
              "locale": "pl", "colorTheme": "dark"
            }}
              </script>
            </div>
            """
            components.html(tech_code, height=460)

        with col_signal2:
            st.markdown("<p style='text-align:center; color:gray;'>Źródło 2: Investing.com</p>", unsafe_allow_html=True)
            # Przykład widgetu Investing.com (wymaga dopasowania ID instrumentu)
            # Uwaga: Investing używa innych ID niż TradingView, poniżej widget uniwersalny
            investing_code = """
            <div style="height: 450px; border-radius: 10px; overflow: hidden;">
              <iframe src="https://it.widgets.investing.com/technical-summary?theme=darkTheme&pairs=1,2,3,5,7,8,9" 
              width="100%" height="420" frameborder="0" allowtransparency="true" marginwidth="0" marginheight="0"></iframe>
            </div>
            """
            components.html(investing_code, height=460)

        # Wykres Główny (pod sygnałami)
        # ... tutaj reszta Twojego kodu z wykresem ...
