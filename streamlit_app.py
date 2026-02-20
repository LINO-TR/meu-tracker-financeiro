import streamlit as st
import yfinance as yf
import pandas as pd
import streamlit.components.v1 as components

# Configuração da Página
st.set_page_config(page_title="Money Flow Tracker", layout="wide", page_icon="🦅")

# CSS para melhorar a visualização no celular
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 1.8rem; }
    </style>
    """, unsafe_allow_html=True)

st.title("🦅 Institutional Money Flow")

# --- DASHBOARD 1: MACRO & CRIPTO (Métricas Rápidas) ---
st.header("1️⃣ Monitor de Preços")
col1, col2, col3, col4 = st.columns(4)

def get_data():
    # Tickers: DXY, Juros 10Y, BTC, ETH
    tickers = {
        "DXY": "DX-Y.NYB", 
        "US10Y": "^TNX", 
        "BTC": "BTC-USD", 
        "ETH": "ETH-USD"
    }
    data = yf.download(list(tickers.values()), period="2d")['Close']
    return data

try:
    prices = get_data()
    
    with col1:
        val = prices["DX-Y.NYB"].iloc[-1]
        delta = val - prices["DX-Y.NYB"].iloc[-2]
        st.metric("DXY (Dólar)", f"{val:.2f}", f"{delta:.2f}")

    with col2:
        val = prices["^TNX"].iloc[-1]
        delta = val - prices["^TNX"].iloc[-2]
        st.metric("US10Y (Juros)", f"{val:.2f}%", f"{delta:.2f}")

    with col3:
        val = prices["BTC-USD"].iloc[-1]
        delta = val - prices["BTC-USD"].iloc[-2]
        st.metric("Bitcoin", f"${val:,.0f}", f"{delta:,.0f}")

    with col4:
        val = prices["ETH-USD"].iloc[-1]
        delta = val - prices["ETH-USD"].iloc[-2]
        st.metric("Ethereum", f"${val:,.2f}")
except:
    st.error("Erro ao carregar dados do Yahoo Finance. Tente atualizar.")

st.markdown("---")

# --- DASHBOARD 2: GRÁFICOS DO TRADINGVIEW ---
st.header("2️⃣ Gráficos em Tempo Real")

tab_btc, tab_dxy = st.tabs(["📊 Gráfico BTC", "🌎 Gráfico DXY"])

with tab_btc:
    # Widget do TradingView para BTC
    components.html("""
        <div class="tradingview-widget-container" style="height:400px;">
          <div id="tradingview_btc"></div>
          <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
          <script type="text/javascript">
          new TradingView.widget({
          "autosize": true, "symbol": "BINANCE:BTCUSDT", "interval": "60",
          "timezone": "Etc/UTC", "theme": "dark", "style": "1",
          "locale": "br", "toolbar_bg": "#f1f3f6", "enable_publishing": false,
          "hide_top_toolbar": true, "save_image": false, "container_id": "tradingview_btc"
          });
          </script>
        </div>
    """, height=400)

with tab_dxy:
    # Widget do TradingView para DXY
    components.html("""
        <div class="tradingview-widget-container" style="height:400px;">
          <div id="tradingview_dxy"></div>
          <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
          <script type="text/javascript">
          new TradingView.widget({
          "autosize": true, "symbol": "CAPITALCOM:DXY", "interval": "D",
          "timezone": "Etc/UTC", "theme": "dark", "style": "2",
          "locale": "br", "toolbar_bg": "#f1f3f6", "enable_publishing": false,
          "container_id": "tradingview_dxy"
          });
          </script>
        </div>
    """, height=400)

st.markdown("---")

# --- DASHBOARD 3: FLUXO & FERRAMENTAS ---
st.header("3️⃣ Fluxo Institucional")

c1, c2 = st.columns(2)
with c1:
    st.info("💡 **DICA:** DXY caindo e Juros caindo = Caminho livre para o BTC.")
    st.link_button("📊 Ver Fluxo de ETFs (Farside)", "https://farside.co.uk/btc/")
    st.link_button("🐋 Whale Alert (Grandes Movimentações)", "https://whale-alert.io/")

with c2:
    st.link_button("🔗 CryptoQuant (Netflow)", "https://cryptoquant.com/asset/btc/chart/exchange-flows/exchange-netflow-total?exchange=all_exchange&window=DAY&sma=0&ema=0&priceScale=log&metricScale=linear&chartStyle=column")
    st.link_button("🌡️ Mapa de Liquidação", "https://www.coinglass.com/pro/futures/LiquidationHeatMap")

# --- BARRA LATERAL (Checklist) ---
st.sidebar.header("📋 Rotina do Trader")
etf = st.sidebar.checkbox("ETF Flow (Entrou dinheiro?)")
macro = st.sidebar.checkbox("Macro (DXY e Juros em queda?)")
baleia = st.sidebar.checkbox("Baleias (Saindo de exchange?)")

if etf and macro and baleia:
    st.sidebar.success("✅ SINAL VERDE: Condições favoráveis.")
else:
    st.sidebar.warning("⚠️ AGUARDANDO: Nem todos os filtros batem.")
  
