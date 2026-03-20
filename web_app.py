import streamlit as st
import streamlit.components.v1 as components

# 1. 頁面設定
st.set_page_config(page_title="全球 24H 實時監控牆", layout="wide")

# --- CSS 極致壓縮：消除間距，讓四格圖表貼齊 ---
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; }
    .block-container { padding: 0rem 0.5rem !important; }
    [data-testid="column"] { padding: 0px !important; margin: -10px !important; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    /* 下拉選單樣式 */
    .stMultiSelect label { color: #00ffcc !important; font-size: 16px !important; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 2. 數據清單 (全部採用 TradingView 官方數據，保證不封鎖)
market_options = {
    # 🏆 必看現貨 (固定標的)
    "黃金現貨 (GOLD)": "TVC:GOLD",
    "原油現貨 (WTI)": "TVC:USOIL",
    "布蘭特原油 (BRENT)": "TVC:UKOIL",
    
    # ₿ 虛擬貨幣 (主要)
    "比特幣 (BTC)": "BINANCE:BTCUSDT",
    "乙太幣 (ETH)": "BINANCE:ETHUSDT",
    "Solana (SOL)": "BINANCE:SOLUSDT",
    "BNB 幣 (BNB)": "BINANCE:BNBUSDT",
    "瑞波幣 (XRP)": "BINANCE:XRPUSDT",
    "比特幣現金 (BCH)": "BINANCE:BCHUSDT",
    
    # ₿ 虛擬貨幣 (熱門補充)
    "狗狗幣 (DOGE)": "BINANCE:DOGEUSDT",
    "艾達幣 (ADA)": "BINANCE:ADAUSDT",
    "雪崩幣 (AVAX)": "BINANCE:AVAXUSDT",
    "波卡幣 (DOT)": "BINANCE:DOTUSDT",
    "鏈結幣 (LINK)": "BINANCE:LINKUSDT",
    "萊特幣 (LTC)": "BINANCE:LTCUSDT"
}

# 3. 側邊欄：選擇要顯示的 4 個格子
with st.sidebar:
    st.header("📊 盤面監控設定")
    selected_names = st.multiselect(
        "請挑選 4 個標的顯示 (預設已選定):",
        options=list(market_options.keys()),
        default=["黃金現貨 (GOLD)", "原油現貨 (WTI)", "比特幣 (BTC)", "乙太幣 (ETH)"]
    )
    st.write("---")
    st.info("💡 這一版全部採用 TradingView 引擎，數據會自動跳動，無需手動刷新。")

# 4. TradingView Widget 產生器
def get_tv_widget(symbol):
    return f"""
    <div style="height:480px; width:100%; border: 1px solid #2a2e39;">
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <div id="tv_{symbol}" style="height:100%; width:100%;"></div>
      <script type="text/javascript">
      new TradingView.widget({{
        "autosize": true,
        "symbol": "{symbol}",
        "interval": "1",
        "timezone": "Asia/Taipei",
        "theme": "dark",
        "style": "1",
        "locale": "zh_TW",
        "toolbar_bg": "#f1f3f6",
        "enable_publishing": false,
        "hide_side_toolbar": false,
        "allow_symbol_change": true,
        "container_id": "tv_{symbol}"
      }});
      </script>
    </div>
    """

# 5. 2x2 佈局顯示
if selected_names:
    # 限制最多顯示 4 個，維持 2x2
    display_list = selected_names[:4]
    col1, col2 = st.columns(2, gap="small")
    
    for i, name in enumerate(display_list):
        target_col = col1 if i % 2 == 0 else col2
        with target_col:
            # 顯示標的名稱標籤
            st.markdown(f"<div style='color:#00ffcc; margin:5px 0 0 10px; font-weight:bold;'>📌 {name}</div>", unsafe_allow_html=True)
            components.html(get_tv_widget(market_options[name]), height=490)
else:
    st.warning("👈 請從左側選單選擇標的進行監控。")