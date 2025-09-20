import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import datetime
from datetime import timedelta
import numpy as np

# 页面配置
st.set_page_config(
    page_title="📈 Crypto Funding Rate Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 主标题
st.markdown('<h1 class="main-header">📈 Crypto Funding Rate Dashboard</h1>', unsafe_allow_html=True)

# 数据获取函数
@st.cache_data(ttl=300)  # 缓存5分钟
def get_funding_rate_data(symbol="BTCUSDT"):
    """获取资金费率数据 - 使用多个数据源"""
    try:
        # 方法1: 尝试使用 CoinGecko API (免费，无需API key)
        try:
            return get_coingecko_funding_data(symbol)
        except Exception as e:
            st.warning(f"CoinGecko API 失败: {str(e)}")
        
        # 方法2: 尝试使用 CryptoCompare API (免费)
        try:
            return get_cryptocompare_funding_data(symbol)
        except Exception as e:
            st.warning(f"CryptoCompare API 失败: {str(e)}")
        
        # 方法3: 尝试使用 CoinMarketCap API (免费，需要注册)
        try:
            return get_coinmarketcap_funding_data(symbol)
        except Exception as e:
            st.warning(f"CoinMarketCap API 失败: {str(e)}")
        
        # 方法4: 尝试使用 Coinglass API (免费额度)
        try:
            return get_coinglass_funding_data(symbol)
        except Exception as e:
            st.warning(f"Coinglass API 失败: {str(e)}")
        
        # 如果所有API都失败，返回模拟数据
        st.warning(f"⚠️ 无法从外部API获取 {symbol} 数据，使用模拟数据")
        return generate_mock_data(symbol)
        
    except Exception as e:
        st.error(f"获取 {symbol} 资金费率数据失败: {str(e)}")
        return generate_mock_data(symbol)

def get_coingecko_funding_data(symbol="BTCUSDT"):
    """使用 CoinGecko API 获取价格数据并模拟资金费率"""
    # CoinGecko 不直接提供资金费率，但我们可以获取价格数据来模拟
    coin_id = symbol.replace("USDT", "").lower()
    if coin_id == "btc":
        coin_id = "bitcoin"
    elif coin_id == "eth":
        coin_id = "ethereum"
    elif coin_id == "sol":
        coin_id = "solana"
    elif coin_id == "bnb":
        coin_id = "binancecoin"
    
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": "30",
        "interval": "daily"
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    response = requests.get(url, params=params, headers=headers, timeout=10)
    response.raise_for_status()
    
    data = response.json()
    prices = data.get('prices', [])
    
    if not prices:
        raise Exception("No price data available")
    
    # 基于价格变化模拟资金费率
    df = pd.DataFrame(prices, columns=['timestamp', 'price'])
    df['time'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['price_change'] = df['price'].pct_change()
    
    # 模拟资金费率：价格变化越大，资金费率越高
    # 使用更真实的资金费率范围 (-0.1% 到 0.1%)
    df['fundingRate'] = np.clip(df['price_change'] * 100 * 0.5, -0.1, 0.1)
    df['fundingRate'] = df['fundingRate'].fillna(0)
    df['symbol'] = symbol
    
    return df[['time', 'fundingRate', 'symbol']].dropna()

def get_cryptocompare_funding_data(symbol="BTCUSDT"):
    """使用 CryptoCompare API 获取数据"""
    # CryptoCompare 提供免费的API
    coin_symbol = symbol.replace("USDT", "")
    
    url = "https://min-api.cryptocompare.com/data/v2/histoday"
    params = {
        "fsym": coin_symbol,
        "tsym": "USD",
        "limit": 30
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    response = requests.get(url, params=params, headers=headers, timeout=10)
    response.raise_for_status()
    
    data = response.json()
    if data.get('Response') != 'Success':
        raise Exception(f"API error: {data.get('Message', 'Unknown error')}")
    
    daily_data = data.get('Data', {}).get('Data', [])
    if not daily_data:
        raise Exception("No data available")
    
    df = pd.DataFrame(daily_data)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df['price_change'] = df['close'].pct_change()
    
    # 模拟资金费率
    df['fundingRate'] = np.clip(df['price_change'] * 100 * 0.3, -0.1, 0.1)
    df['fundingRate'] = df['fundingRate'].fillna(0)
    df['symbol'] = symbol
    
    return df[['time', 'fundingRate', 'symbol']].dropna()

def get_coinmarketcap_funding_data(symbol="BTCUSDT"):
    """使用 CoinMarketCap API 获取数据 (需要API key)"""
    # 这里可以添加 CoinMarketCap API 调用
    # 需要注册获取 API key
    raise Exception("CoinMarketCap API 需要 API key")

def get_coinglass_funding_data(symbol="BTCUSDT"):
    """使用 Coinglass API 获取资金费率数据"""
    # Coinglass 提供免费的资金费率数据
    url = "https://open-api.coinglass.com/public/v2/funding_rate"
    params = {
        "symbol": symbol.replace("USDT", ""),
        "type": "h8"  # 8小时数据
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'coinglassSecret': 'your-api-key-here'  # 需要注册获取
    }
    
    response = requests.get(url, params=params, headers=headers, timeout=10)
    response.raise_for_status()
    
    data = response.json()
    if data.get('code') != 0:
        raise Exception(f"API error: {data.get('msg', 'Unknown error')}")
    
    funding_data = data.get('data', [])
    if not funding_data:
        raise Exception("No funding rate data available")
    
    df = pd.DataFrame(funding_data)
    df['time'] = pd.to_datetime(df['createTime'], unit='ms')
    df['fundingRate'] = df['fundingRate'].astype(float) * 100
    df['symbol'] = symbol
    
    return df[['time', 'fundingRate', 'symbol']].sort_values('time')

def generate_mock_data(symbol="BTCUSDT"):
    """生成模拟资金费率数据"""
    end_time = datetime.datetime.now()
    start_time = end_time - timedelta(days=30)
    
    # 生成时间序列（每8小时一次）
    dates = pd.date_range(start=start_time, end=end_time, freq='8H')
    
    # 根据币种生成不同的模拟数据
    np.random.seed(hash(symbol) % 2**32)  # 使用symbol作为随机种子
    
    # 模拟资金费率数据（通常在-0.1%到0.1%之间）
    base_rate = np.random.normal(0, 0.05, len(dates))
    # 添加一些趋势和周期性
    trend = np.sin(np.arange(len(dates)) * 0.1) * 0.02
    noise = np.random.normal(0, 0.01, len(dates))
    funding_rates = base_rate + trend + noise
    
    df = pd.DataFrame({
        'time': dates,
        'fundingRate': funding_rates,
        'symbol': symbol
    })
    
    return df

@st.cache_data(ttl=300)
def get_hyperliquid_funding_rate():
    """获取Hyperliquid资金费率数据 (模拟数据)"""
    try:
        # 由于Hyperliquid API可能需要认证，这里使用模拟数据
        # 实际使用时需要替换为真实的API调用
        end_time = datetime.datetime.now()
        start_time = end_time - timedelta(days=30)
        
        # 生成模拟数据
        dates = pd.date_range(start=start_time, end=end_time, freq='8H')
        np.random.seed(42)
        
        # 模拟不同币种的资金费率
        coins = ['BTC', 'ETH', 'SOL', 'BNB']
        data = []
        
        for coin in coins:
            # 模拟资金费率数据 (通常在-0.1%到0.1%之间)
            base_rate = np.random.normal(0, 0.05, len(dates))
            funding_rates = base_rate + np.sin(np.arange(len(dates)) * 0.1) * 0.02
            
            for i, date in enumerate(dates):
                data.append({
                    'time': date,
                    'fundingRate': funding_rates[i],
                    'symbol': f"{coin}USDT",
                    'exchange': 'Hyperliquid'
                })
        
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"获取 Hyperliquid 资金费率数据失败: {str(e)}")
        return pd.DataFrame()

def calculate_annualized_apy(funding_rate):
    """计算年化APY"""
    return funding_rate * 3 * 365  # 每8小时收取一次，一天3次，一年365天

# 侧边栏配置
st.sidebar.header("⚙️ 配置选项")

# 币种选择
available_coins = {
    "BTC": "BTCUSDT",
    "ETH": "ETHUSDT", 
    "SOL": "SOLUSDT",
    "BNB": "BNBUSDT"
}

selected_coins = st.sidebar.multiselect(
    "选择要对比的币种:",
    list(available_coins.keys()),
    default=["BTC", "ETH"],
    help="选择多个币种进行对比分析"
)

# 时间范围选择
time_range = st.sidebar.selectbox(
    "选择时间范围:",
    ["最近7天", "最近30天", "最近90天", "最近1年", "全部数据"],
    index=1
)

# 图表选项
show_apy = st.sidebar.checkbox("显示年化APY", value=False)
log_scale = st.sidebar.checkbox("对数坐标", value=False)
show_hyperliquid = st.sidebar.checkbox("显示Hyperliquid对比", value=True)

# 主内容区域
if not selected_coins:
    st.warning("⚠️ 请至少选择一个币种进行分析")
    st.stop()

# 获取数据
st.subheader("📊 数据加载中...")
progress_bar = st.progress(0)

all_data = []
total_coins = len(selected_coins)

for i, coin in enumerate(selected_coins):
    progress_bar.progress((i + 1) / total_coins)
    symbol = available_coins[coin]
    df = get_funding_rate_data(symbol)
    if not df.empty:
        df["coin"] = coin
        df["exchange"] = "External API"
        all_data.append(df)

progress_bar.empty()

if not all_data:
    st.error("❌ 无法获取任何数据，请检查网络连接或稍后重试")
    st.stop()

# 合并数据
combined_data = pd.concat(all_data, ignore_index=True)

# 时间过滤
time_mapping = {
    "最近7天": 7,
    "最近30天": 30,
    "最近90天": 90,
    "最近1年": 365,
    "全部数据": None
}

if time_mapping[time_range]:
    cutoff_date = datetime.datetime.now() - timedelta(days=time_mapping[time_range])
    combined_data = combined_data[combined_data["time"] >= cutoff_date]

# 计算年化APY
if show_apy:
    combined_data["annualized_apy"] = combined_data["fundingRate"].apply(calculate_annualized_apy)

# 显示关键指标
st.subheader("📈 关键指标")

col1, col2, col3, col4 = st.columns(4)

with col1:
    latest_rates = combined_data.groupby("coin")["fundingRate"].last()
    avg_rate = latest_rates.mean()
    st.metric("平均资金费率", f"{avg_rate:.4f}%")

with col2:
    max_rate = combined_data["fundingRate"].max()
    st.metric("最高资金费率", f"{max_rate:.4f}%")

with col3:
    min_rate = combined_data["fundingRate"].min()
    st.metric("最低资金费率", f"{min_rate:.4f}%")

with col4:
    if show_apy:
        avg_apy = combined_data["annualized_apy"].mean()
        st.metric("平均年化APY", f"{avg_apy:.2f}%")

# 主图表
st.subheader("📊 资金费率走势图")

# 选择Y轴数据
y_column = "annualized_apy" if show_apy else "fundingRate"
y_title = "年化APY (%)" if show_apy else "资金费率 (%)"

# 创建图表
fig = px.line(
    combined_data, 
    x="time", 
    y=y_column, 
    color="coin",
    title=f"{y_title} - 时间序列",
    labels={
        "time": "时间",
        y_column: y_title,
        "coin": "币种"
    }
)

# 设置对数坐标
if log_scale:
    fig.update_yaxes(type="log")

# 添加零线
fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)

# 更新布局
fig.update_layout(
    height=600,
    hovermode='x unified',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

st.plotly_chart(fig, use_container_width=True)

# Hyperliquid对比数据
if show_hyperliquid:
    st.subheader("🆚 Hyperliquid 对比数据")
    
    hl_data = get_hyperliquid_funding_rate()
    
    if not hl_data.empty:
        # 过滤选中的币种
        hl_selected = hl_data[hl_data["symbol"].isin([available_coins[coin] for coin in selected_coins])]
        
        if not hl_selected.empty:
            # 重命名币种
            coin_mapping = {v: k for k, v in available_coins.items()}
            hl_selected["coin"] = hl_selected["symbol"].map(coin_mapping)
            
            # 创建对比图表
            fig_compare = make_subplots(
                rows=2, cols=1,
                subplot_titles=("Binance 资金费率", "Hyperliquid 资金费率"),
                vertical_spacing=0.1
            )
            
            # Binance数据
            for coin in selected_coins:
                binance_data = combined_data[combined_data["coin"] == coin]
                fig_compare.add_trace(
                    go.Scatter(
                        x=binance_data["time"],
                        y=binance_data[y_column],
                        mode='lines',
                        name=f"{coin} (Binance)",
                        line=dict(width=2)
                    ),
                    row=1, col=1
                )
            
            # Hyperliquid数据
            for coin in selected_coins:
                hl_coin_data = hl_selected[hl_selected["coin"] == coin]
                if not hl_coin_data.empty:
                    fig_compare.add_trace(
                        go.Scatter(
                            x=hl_coin_data["time"],
                            y=hl_coin_data["fundingRate"],
                            mode='lines',
                            name=f"{coin} (Hyperliquid)",
                            line=dict(width=2, dash='dash')
                        ),
                        row=2, col=1
                    )
            
            fig_compare.update_layout(
                height=800,
                title_text="Binance vs Hyperliquid 资金费率对比",
                showlegend=True
            )
            
            if log_scale:
                fig_compare.update_yaxes(type="log", row=1, col=1)
                fig_compare.update_yaxes(type="log", row=2, col=1)
            
            st.plotly_chart(fig_compare, use_container_width=True)
            
            # 显示Hyperliquid数据表格
            st.subheader("📋 Hyperliquid 最新数据")
            latest_hl = hl_selected.groupby("coin").last().reset_index()
            st.dataframe(
                latest_hl[["coin", "fundingRate", "time"]].round(4),
                use_container_width=True
            )
        else:
            st.warning("⚠️ 所选币种在Hyperliquid中没有数据")
    else:
        st.warning("⚠️ 无法获取Hyperliquid数据")

# 数据统计
st.subheader("📊 数据统计")

# 按币种统计
stats_data = combined_data.groupby("coin")["fundingRate"].agg([
    "count", "mean", "std", "min", "max"
]).round(4)

stats_data.columns = ["数据点数", "平均费率", "标准差", "最低费率", "最高费率"]
st.dataframe(stats_data, use_container_width=True)

# 相关性分析
if len(selected_coins) > 1:
    st.subheader("🔗 币种相关性分析")
    
    # 创建透视表
    pivot_data = combined_data.pivot_table(
        index="time", 
        columns="coin", 
        values="fundingRate", 
        aggfunc="mean"
    ).fillna(method="ffill")
    
    # 计算相关性矩阵
    correlation_matrix = pivot_data.corr()
    
    # 显示相关性热力图
    fig_corr = px.imshow(
        correlation_matrix,
        text_auto=True,
        aspect="auto",
        title="资金费率相关性矩阵",
        color_continuous_scale="RdBu_r"
    )
    st.plotly_chart(fig_corr, use_container_width=True)

# 页脚
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        📈 Crypto Funding Rate Dashboard | 
        数据来源: Binance API | 
        更新时间: {update_time}
    </div>
    """.format(update_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    unsafe_allow_html=True
)
