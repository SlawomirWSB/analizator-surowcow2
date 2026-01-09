with tab1:
        # Panel Wyboru
        c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
        with c1: rynek = st.selectbox("Rynek:", list(DB.keys()), index=0)
        with c2: inst = st.selectbox("Instrument:", list(DB[rynek].keys()), index=0)
        with c3: itv = st.selectbox("Interwał:", ["1", "5", "15", "60", "D"], index=1)
        with c4: audio = st.checkbox("Dźwięk", value=True)

        # Pobieramy wybrany symbol z bazy
        selected_symbol = DB[rynek][inst]

        st.subheader("🤖 Analiza Wielu Źródeł")
        col_sig1, col_sig2 = st.columns(2)

        with col_sig1:
            st.markdown("<p style='text-align:center; color:#83888D;'>Źródło 1: TradingView (Analiza Live)</p>", unsafe_allow_html=True)
            # Poprawiony widżet z dynamicznym symbolem
            tech_tv = f"""
            <div style="height: 450px;">
              <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-technical-analysis.js" async>
              {{
              "interval": "{itv}m" if "{itv}".isdigit() else "1D",
              "width": "100%", "height": 450,
              "isTransparent": true, 
              "symbol": "{selected_symbol}",
              "showIntervalTabs": false, "displayMode": "single",
              "locale": "pl", "colorTheme": "dark"
            }}
              </script>
            </div>
            """
            components.html(tech_tv, height=470)

        with col_sig2:
            st.markdown("<p style='text-align:center; color:#83888D;'>Źródło 2: Investing.com (Sentyment Globalny)</p>", unsafe_allow_html=True)
            # Zmieniamy na widżet sentymentu/podsumowania, który jest stabilniejszy
            tech_inv = """
            <iframe src="https://www.widgets.investing.com/live-currency-cross-rates?theme=darkTheme&roundedCorners=true&pairs=1,3,2,5,7,9,10" 
            width="100%" height="450" frameborder="0" allowtransparency="true" marginwidth="0" marginheight="0"></iframe>
            """
            components.html(tech_inv, height=470)

        # Wykres Główny - upewniamy się, że też reaguje na zmianę
        st.markdown("---")
        chart_code = f"""
        <div id="tv_chart_main" style="height: 600px;"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget({{
          "autosize": true, 
          "symbol": "{selected_symbol}", 
          "interval": "{itv}",
          "timezone": "Europe/Warsaw", "theme": "dark", "style": "1",
          "locale": "pl", "container_id": "tv_chart_main"
        }});
        </script>
        """
        components.html(chart_code, height=620)
