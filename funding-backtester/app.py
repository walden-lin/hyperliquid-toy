"""
事件驱动资金费率回测工具 - Streamlit 主应用
基于 Hyperliquid 数据的事件驱动回测和可视化系统
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# 导入自定义模块
from data import get_funding_history, get_price_history
from strategy import FundingRateStrategy, EventDrivenBacktester
from visualization import FundingRateVisualizer
from advanced_strategies import AdvancedFundingRateStrategies

# 页面配置
st.set_page_config(
    page_title="📊 事件驱动资金费率回测工具",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 页面导航
def show_navigation():
    """显示页面导航"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style='text-align: center; margin: 1rem 0;'>
            <a href='?page=main' style='margin: 0 1rem; padding: 0.5rem 1rem; background-color: #1f77b4; color: white; text-decoration: none; border-radius: 0.5rem;'>🏠 主应用</a>
            <a href='?page=tutorial' style='margin: 0 1rem; padding: 0.5rem 1rem; background-color: #ff7f0e; color: white; text-decoration: none; border-radius: 0.5rem;'>📚 教程</a>
            <a href='?page=theory' style='margin: 0 1rem; padding: 0.5rem 1rem; background-color: #2ca02c; color: white; text-decoration: none; border-radius: 0.5rem;'>🧮 数学理论</a>
        </div>
        """, unsafe_allow_html=True)

# 获取当前页面
def get_current_page():
    """获取当前页面参数"""
    query_params = st.query_params
    return query_params.get("page", ["main"])[0] if "page" in query_params else "main"

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
        margin: 0.5rem 0;
    }
    .event-card {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .success-card {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .error-card {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def show_main_page():
    """显示主应用页面"""
    # 主标题
    st.markdown('<h1 class="main-header">📊 事件驱动资金费率回测工具</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666; font-size: 1.1rem;">基于 Hyperliquid 数据的事件驱动回测和可视化系统</p>', unsafe_allow_html=True)
    
    # 原来的主应用代码
    main_application()

def show_tutorial_page():
    """显示教程页面"""
    st.markdown('<h1 class="main-header">📚 使用教程</h1>', unsafe_allow_html=True)
    
    # 教程内容
    st.markdown("""
    ## 🎯 什么是资金费率？
    
    资金费率是加密货币期货市场中的一个重要机制，用于平衡多空双方的力量，确保期货价格与现货价格保持接近。
    
    ### 📊 资金费率的作用
    - **价格锚定**: 通过资金费率机制，期货价格会向现货价格收敛
    - **风险平衡**: 当市场偏向某一方向时，资金费率会调整以平衡风险
    - **套利机会**: 资金费率异常时，存在套利机会
    
    ### ⏰ 资金费率结算
    - **结算频率**: 每8小时结算一次（00:00, 08:00, 16:00 UTC）
    - **计算公式**: 资金费率 = 基础费率 + 溢价指数
    - **支付方向**: 当资金费率为正时，多头支付空头；为负时，空头支付多头
    
    ## 🔍 异常检测原理
    
    我们使用统计学中的 **Z-score** 方法来检测资金费率异常：
    
    ### 📈 Z-score 计算
    ```
    Z = (X - μ) / σ
    ```
    其中：
    - X: 当前资金费率
    - μ: 滚动均值
    - σ: 滚动标准差
    
    ### 🎯 交易信号
    - **Z > +2**: SHORT 信号（资金费率过高，做空收取资金费率）
    - **Z < -2**: LONG 信号（资金费率过低，做多收取资金费率）
    - **-2 ≤ Z ≤ +2**: HOLD 信号（正常范围）
    
    ## 🚀 如何使用这个工具
    
    ### 1️⃣ 选择事件
    从侧边栏下拉菜单选择要分析的重大事件。每个事件都有：
    - 事件名称和描述
    - 影响的币种
    - 事件发生时间
    - 影响程度评估
    
    ### 2️⃣ 调整策略参数
    - **滚动窗口**: 用于计算Z-score的时间窗口（8-168小时）
    - **Z-score阈值**: 触发交易信号的阈值（1.0-4.0）
    - **初始资金**: 回测的起始资金
    
    ### 3️⃣ 查看回测结果
    - **关键指标**: 总收益、胜率、夏普比率等
    - **可视化图表**: 资金费率走势、交易信号、组合表现
    - **交易记录**: 详细的交易历史记录
    
    ### 4️⃣ 分析事件影响
    - **事件前后对比**: 分析事件对资金费率的影响
    - **信号分布**: 查看异常信号的分布情况
    - **相关性分析**: 分析交易指标间的相关性
    
    ## 💡 使用技巧
    
    ### 🎯 参数调优
    - **滚动窗口**: 较小的窗口对短期变化更敏感，较大的窗口更稳定
    - **阈值设置**: 较低的阈值会产生更多信号，较高的阈值信号更可靠
    - **资金管理**: 建议使用总资金的10-20%进行单笔交易
    
    ### 📊 结果解读
    - **胜率**: 盈利交易占总交易的比例
    - **夏普比率**: 风险调整后的收益率
    - **最大回撤**: 从峰值到谷值的最大跌幅
    - **年化APY**: 资金费率的年化收益率
    
    ### ⚠️ 风险提示
    - 历史回测结果不代表未来表现
    - 实际交易存在滑点、手续费等成本
    - 资金费率策略存在价格风险
    - 请谨慎投资，风险自负
    """)

def show_theory_page():
    """显示数学理论页面"""
    st.markdown('<h1 class="main-header">🧮 数学理论与算法详解</h1>', unsafe_allow_html=True)
    
    # 数学理论内容
    st.markdown("""
    ## 📊 统计学基础
    
    ### 1. 正态分布与Z-score
    
    在统计学中，Z-score（标准分数）是衡量一个数据点距离均值有多少个标准差的方法。
    
    **数学定义：**
    ```
    Z = (X - μ) / σ
    ```
    
    其中：
    - X: 观测值
    - μ: 总体均值
    - σ: 总体标准差
    
    **Z-score的几何意义：**
    - Z = 0: 数据点等于均值
    - Z = ±1: 数据点距离均值1个标准差
    - Z = ±2: 数据点距离均值2个标准差（约95%的数据在此范围内）
    - Z = ±3: 数据点距离均值3个标准差（约99.7%的数据在此范围内）
    
    ### 2. 滚动统计量
    
    滚动统计量是时间序列分析中的重要概念，用于计算滑动窗口内的统计指标。
    
    **滚动均值：**
    ```
    μ_t = (1/n) × Σ(i=t-n+1 to t) X_i
    ```
    
    **滚动标准差：**
    ```
    σ_t = √[(1/n) × Σ(i=t-n+1 to t) (X_i - μ_t)²]
    ```
    
    其中n是窗口大小。
    
    ## 🎯 异常检测算法
    
    ### 1. 算法流程
    
    ```python
    def detect_anomalies(df, window_hours=24, threshold=2.0):
        # 1. 计算滚动统计量
        window_points = window_hours // 8  # 每8小时一次资金费率结算
        df["mean"] = df["fundingRate"].rolling(window=window_points).mean()
        df["std"] = df["fundingRate"].rolling(window=window_points).std()
        
        # 2. 计算Z-score
        df["zscore"] = (df["fundingRate"] - df["mean"]) / df["std"]
        
        # 3. 生成交易信号
        df["signal"] = df["zscore"].apply(
            lambda z: "SHORT" if z > threshold else ("LONG" if z < -threshold else "HOLD")
        )
        
        return df
    ```
    
    ### 2. 信号生成逻辑
    
    **数学条件：**
    - SHORT信号: Z > +threshold
    - LONG信号: Z < -threshold  
    - HOLD信号: -threshold ≤ Z ≤ +threshold
    
    **经济学解释：**
    - 当Z > +threshold时，资金费率异常高，说明市场情绪极度乐观，此时做空可以收取高额资金费率
    - 当Z < -threshold时，资金费率异常低，说明市场情绪极度悲观，此时做多可以收取资金费率
    
    ## 💰 回测算法
    
    ### 1. 持仓管理
    
    **开仓条件：**
    ```python
    if signal != "HOLD" and coin not in positions:
        position_size = capital * position_ratio  # 使用固定比例资金
        positions[coin] = {
            "side": signal,
            "entry_time": current_time,
            "entry_rate": funding_rate,
            "size": position_size
        }
    ```
    
    **平仓条件：**
    ```python
    if signal == "HOLD" and coin in positions:
        # 计算盈亏并平仓
        trade_pnl = calculate_trade_pnl(position, exit_rate, exit_time)
        capital += trade_pnl
        del positions[coin]
    ```
    
    ### 2. 盈亏计算
    
    **资金费率收益：**
    ```
    funding_pnl = position_size × funding_rate × (time_elapsed / 8_hours)
    ```
    
    **价格变动盈亏：**
    ```
    price_pnl = position_size × (exit_rate - entry_rate) / 100
    ```
    
    **总盈亏：**
    ```
    total_pnl = funding_pnl + price_pnl
    ```
    
    ### 3. 年化APY计算
    
    **数学公式：**
    ```
    年化APY = 资金费率 × 3 × 365
    ```
    
    **推导过程：**
    - 资金费率每8小时结算一次
    - 一天 = 24小时 ÷ 8小时 = 3次
    - 一年 = 3次 × 365天 = 1095次
    - 年化APY = 单次资金费率 × 1095
    
    ## 📈 风险指标计算
    
    ### 1. 夏普比率
    
    **定义：**
    ```
    Sharpe Ratio = (R_p - R_f) / σ_p
    ```
    
    其中：
    - R_p: 投资组合收益率
    - R_f: 无风险收益率（通常为0）
    - σ_p: 投资组合收益率标准差
    
    ### 2. 最大回撤
    
    **计算步骤：**
    1. 计算累计收益率序列
    2. 计算滚动最大值
    3. 计算回撤 = 累计收益率 - 滚动最大值
    4. 最大回撤 = 回撤序列的最小值
    
    **数学表达：**
    ```
    DD_t = max(0, max(CumRet_0 to CumRet_t) - CumRet_t)
    MaxDD = min(DD_0, DD_1, ..., DD_T)
    ```
    
    ### 3. 胜率
    
    **定义：**
    ```
    胜率 = 盈利交易数 / 总交易数 × 100%
    ```
    
    ## 🔬 算法优化
    
    ### 1. 参数敏感性分析
    
    **滚动窗口优化：**
    - 较小窗口：对短期变化敏感，信号频繁
    - 较大窗口：更稳定，信号较少但更可靠
    
    **阈值优化：**
    - 较低阈值：更多信号，但可能包含噪音
    - 较高阈值：信号更可靠，但可能错过机会
    
    ### 2. 动态调整策略
    
    **自适应阈值：**
    ```
    threshold_t = base_threshold × (1 + volatility_factor × σ_t)
    ```
    
    **动态仓位：**
    ```
    position_size_t = base_size × (1 - risk_factor × |zscore_t|)
    ```
    
    ## 🎓 进阶理论
    
    ### 1. 时间序列分析
    
    **自相关函数：**
    ```
    ACF(k) = Cov(X_t, X_{t-k}) / Var(X_t)
    ```
    
    **平稳性检验：**
    - 使用ADF检验（Augmented Dickey-Fuller test）
    - 确保时间序列的统计特性不随时间变化
    
    ### 2. 机器学习方法
    
    **特征工程：**
    - 技术指标：MA、EMA、RSI、MACD
    - 统计特征：偏度、峰度、分位数
    - 时间特征：小时、星期、月份
    
    **模型选择：**
    - 监督学习：随机森林、XGBoost、神经网络
    - 无监督学习：聚类、异常检测
    - 强化学习：Q-learning、策略梯度
    
    ### 3. 风险管理理论
    
    **VaR（风险价值）：**
    ```
    VaR_α = -F^{-1}(α) × σ × √T
    ```
    
    **CVaR（条件风险价值）：**
    ```
    CVaR_α = E[-R | R ≤ -VaR_α]
    ```
    
    **投资组合优化：**
    ```
    max E[R_p] - λ × Var[R_p]
    ```
    
    其中λ是风险厌恶系数。
    """)
    
    # 添加交互式数学公式演示
    st.markdown("## 🧮 交互式公式演示")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Z-score 计算器")
        current_rate = st.number_input("当前资金费率 (%)", value=0.01, step=0.001, format="%.4f")
        mean_rate = st.number_input("滚动均值 (%)", value=0.005, step=0.001, format="%.4f")
        std_rate = st.number_input("滚动标准差 (%)", value=0.002, step=0.001, format="%.4f")
        
        if std_rate > 0:
            z_score = (current_rate - mean_rate) / std_rate
            st.metric("Z-score", f"{z_score:.2f}")
            
            if z_score > 2:
                st.success("🟢 SHORT 信号：资金费率异常高")
            elif z_score < -2:
                st.success("🔴 LONG 信号：资金费率异常低")
            else:
                st.info("⚪ HOLD 信号：资金费率正常")
    
    with col2:
        st.markdown("### 年化APY 计算器")
        funding_rate = st.number_input("资金费率 (%)", value=0.01, step=0.001, format="%.4f")
        annual_apy = funding_rate * 3 * 365
        st.metric("年化APY", f"{annual_apy:.2f}%")
        
        st.markdown("**计算过程：**")
        st.write(f"• 单次资金费率: {funding_rate}%")
        st.write(f"• 每天结算次数: 3次")
        st.write(f"• 一年总次数: 3 × 365 = 1095次")
        st.write(f"• 年化APY: {funding_rate}% × 1095 = {annual_apy:.2f}%")

def main_application():
    """主应用逻辑"""
    # 加载事件配置
    def load_events():
        """加载事件配置"""
        import os
        
        # 获取当前脚本所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        events_file = os.path.join(current_dir, 'events.json')
        
        # 调试信息（仅在开发环境显示）
        if st.sidebar.checkbox("显示调试信息", value=False):
            st.write(f"当前工作目录: {os.getcwd()}")
            st.write(f"脚本目录: {current_dir}")
            st.write(f"events.json 路径: {events_file}")
            st.write(f"文件是否存在: {os.path.exists(events_file)}")
            if os.path.exists(current_dir):
                st.write(f"目录内容: {os.listdir(current_dir)}")
        
        try:
            with open(events_file, 'r', encoding='utf-8') as f:
                events = json.load(f)
            return events
        except FileNotFoundError:
            st.error(f"❌ 找不到 events.json 文件，路径: {events_file}")
            return []
        except json.JSONDecodeError:
            st.error("❌ events.json 文件格式错误")
            return []

    # 侧边栏配置
    st.sidebar.header("⚙️ 配置选项")

    # 加载事件数据
    events = load_events()
    if not events:
        st.error("无法加载事件配置，请检查 events.json 文件")
        st.stop()

    # 事件选择
    event_names = [event["name"] for event in events]
    selected_event_name = st.sidebar.selectbox(
        "选择事件:",
        event_names,
        help="选择要分析的重大事件"
    )

    # 获取选中事件
    selected_event = next(event for event in events if event["name"] == selected_event_name)

    # 策略选择
    st.sidebar.subheader("🎯 策略选择")
    
    analysis_mode = st.sidebar.radio(
        "分析模式:",
        ["单一策略", "策略对比"],
        help="选择单一策略分析或多种策略对比"
    )
    
    # 策略参数配置
    st.sidebar.subheader("📈 策略参数")

    window_hours = st.sidebar.slider(
        "滚动窗口 (小时):",
        min_value=8,
        max_value=168,
        value=24,
        step=8,
        help="用于计算 Z-score 的滚动窗口大小"
    )

    threshold = st.sidebar.slider(
        "Z-score 阈值:",
        min_value=1.0,
        max_value=4.0,
        value=2.0,
        step=0.1,
        help="触发交易信号的 Z-score 阈值"
    )

    initial_capital = st.sidebar.number_input(
        "初始资金 (USD):",
        min_value=1000,
        max_value=1000000,
        value=10000,
        step=1000,
        help="回测的初始资金"
    )

    # 数据获取选项
    st.sidebar.subheader("📊 数据选项")

    show_price_data = st.sidebar.checkbox("显示价格数据", value=True)
    show_portfolio_performance = st.sidebar.checkbox("显示组合表现", value=True)
    show_trades_timeline = st.sidebar.checkbox("显示交易时间线", value=True)

    # 主内容区域
    st.subheader("📅 事件信息")

    # 显示事件详情
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="event-card">
            <h4>📅 {selected_event['name']}</h4>
            <p><strong>币种:</strong> {selected_event['coin']}</p>
            <p><strong>时间:</strong> {selected_event['timestamp']}</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="event-card">
            <h4>📝 事件描述</h4>
            <p>{selected_event.get('description', '暂无描述')}</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        impact_colors = {
            'very_high': '#dc3545',
            'high': '#fd7e14', 
            'medium': '#ffc107',
            'low': '#28a745'
        }
        impact_color = impact_colors.get(selected_event.get('impact', 'medium'), '#6c757d')
        
        st.markdown(f"""
        <div class="event-card">
            <h4>📊 影响程度</h4>
            <p style="color: {impact_color}; font-weight: bold; font-size: 1.2rem;">
                {selected_event.get('impact', 'medium').upper()}
            </p>
            <p><strong>类别:</strong> {selected_event.get('category', 'unknown')}</p>
        </div>
        """, unsafe_allow_html=True)

    # 数据获取和处理
    st.subheader("📊 数据获取中...")

    # 计算时间窗口
    event_time = datetime.fromisoformat(selected_event["timestamp"])
    start_time = event_time - timedelta(hours=24)
    end_time = event_time + timedelta(hours=72)

    coin = selected_event["coin"]

    # 显示进度条
    progress_bar = st.progress(0)
    status_text = st.empty()

    # 获取资金费率数据
    status_text.text("正在获取资金费率数据...")
    progress_bar.progress(25)

    try:
        funding_data = get_funding_history(coin, start_time, end_time)
        if funding_data.empty:
            st.error(f"❌ 无法获取 {coin} 的资金费率数据")
            st.stop()
        
        status_text.text("资金费率数据获取成功")
        progress_bar.progress(50)
        
    except Exception as e:
        st.error(f"❌ 获取资金费率数据失败: {str(e)}")
        st.stop()

    # 获取价格数据（可选）
    price_data = None
    if show_price_data:
        status_text.text("正在获取价格数据...")
        progress_bar.progress(75)
        
        try:
            price_data = get_price_history(coin, start_time, end_time)
            status_text.text("价格数据获取成功")
        except Exception as e:
            st.warning(f"⚠️ 获取价格数据失败: {str(e)}")
            price_data = None

    progress_bar.progress(100)
    status_text.text("数据获取完成")
    progress_bar.empty()
    status_text.empty()

    # 策略执行
    st.subheader("🎯 策略执行")

    if analysis_mode == "单一策略":
        # 单一策略执行
        strategy = FundingRateStrategy(window_hours=window_hours, threshold=threshold)
        backtester = EventDrivenBacktester(strategy)

        # 执行回测
        with st.spinner("正在执行回测..."):
            try:
                backtest_result = backtester.run_event_backtest(selected_event, funding_data, price_data)
                
                if not backtest_result:
                    st.error("❌ 回测执行失败")
                    st.stop()
                
                st.success("✅ 回测执行成功")
                
            except Exception as e:
                st.error(f"❌ 回测执行失败: {str(e)}")
                st.stop()
                
    else:
        # 策略对比执行
        st.info("🔄 正在运行多种策略对比分析...")
        
        # 初始化高级策略
        advanced_strategies = AdvancedFundingRateStrategies()
        
        # 执行策略对比
        with st.spinner("正在执行策略对比..."):
            try:
                # 运行所有策略
                strategy_results = advanced_strategies.run_strategy_comparison(funding_data)
                
                if not strategy_results:
                    st.error("❌ 策略对比执行失败")
                    st.stop()
                
                st.success(f"✅ 成功执行 {len(strategy_results)} 种策略")
                
                # 显示策略对比结果
                st.subheader("📊 策略对比结果")
                
                # 计算策略性能指标
                metrics_df = advanced_strategies.calculate_strategy_metrics(strategy_results)
                
                # 显示性能指标表格
                st.dataframe(metrics_df, use_container_width=True)
                
                # 显示各策略的详细结果
                st.subheader("📈 各策略详细分析")
                
                # 创建标签页显示各策略
                strategy_tabs = st.tabs(list(strategy_results.keys()))
                
                for i, (strategy_name, result_df) in enumerate(strategy_results.items()):
                    with strategy_tabs[i]:
                        st.write(f"**{strategy_name}**")
                        
                        # 显示信号统计
                        signals = result_df[result_df["signal"] != "HOLD"]
                        if not signals.empty:
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("总信号数", len(signals))
                            with col2:
                                st.metric("做多信号", len(signals[signals["signal"] == "LONG"]))
                            with col3:
                                st.metric("做空信号", len(signals[signals["signal"] == "SHORT"]))
                            with col4:
                                st.metric("平均置信度", f"{signals['confidence'].mean():.3f}")
                            
                            # 显示信号详情
                            st.write("**信号详情:**")
                            st.dataframe(signals[["time", "fundingRate", "signal", "confidence"]], use_container_width=True)
                        else:
                            st.info("该策略在此时间段内未产生交易信号")
                
                # 设置回测结果为第一个策略的结果（用于后续显示）
                first_strategy = list(strategy_results.keys())[0]
                backtest_result = {
                    "strategy_name": first_strategy,
                    "trades": [],
                    "performance_metrics": {}
                }
                
            except Exception as e:
                st.error(f"❌ 策略对比执行失败: {str(e)}")
                st.stop()

    # 显示回测统计
    st.subheader("📈 回测统计")

    stats = backtest_result.get("stats", {})
    trades_df = backtest_result.get("trades", pd.DataFrame())

    if not trades_df.empty:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "总收益",
                f"${stats.get('total_return', 0):,.2f}",
                f"{stats.get('total_return_pct', 0):.2f}%"
            )
        
        with col2:
            st.metric(
                "总交易数",
                stats.get('total_trades', 0),
                f"胜率: {stats.get('win_rate', 0):.1f}%"
            )
        
        with col3:
            st.metric(
                "平均交易盈亏",
                f"${stats.get('avg_trade_pnl', 0):,.2f}",
                f"最大回撤: ${stats.get('max_drawdown', 0):,.2f}"
            )
        
        with col4:
            st.metric(
                "夏普比率",
                f"{stats.get('sharpe_ratio', 0):.2f}",
                f"最终资金: ${backtest_result.get('final_capital', initial_capital):,.2f}"
            )
    else:
        st.warning("⚠️ 在选定的事件窗口内没有产生交易信号")

    # 可视化
    st.subheader("📊 可视化分析")

    # 初始化可视化器
    visualizer = FundingRateVisualizer()

    # 资金费率走势图
    funding_fig = visualizer.plot_funding_rate_with_signals(
        backtest_result["data"],
        backtest_result.get("event_time")
    )
    st.plotly_chart(funding_fig, use_container_width=True)

    # 价格走势图（如果可用）
    if show_price_data and price_data is not None and not price_data.empty:
        price_fig = visualizer.plot_price_with_events(
            price_data,
            backtest_result.get("event_time")
        )
        st.plotly_chart(price_fig, use_container_width=True)

    # 组合表现图
    if show_portfolio_performance and "portfolio_times" in backtest_result:
        portfolio_fig = visualizer.plot_portfolio_performance(
            backtest_result["portfolio_times"],
            backtest_result["portfolio_value"]
        )
        st.plotly_chart(portfolio_fig, use_container_width=True)

    # 交易时间线
    if show_trades_timeline and not trades_df.empty:
        trades_fig = visualizer.plot_trades_timeline(trades_df)
        st.plotly_chart(trades_fig, use_container_width=True)

    # 交易记录表格
    if not trades_df.empty:
        st.subheader("📋 交易记录")
        
        # 格式化交易记录显示
        display_trades = trades_df.copy()
        display_trades["entry_time"] = display_trades["entry_time"].dt.strftime("%Y-%m-%d %H:%M")
        display_trades["exit_time"] = display_trades["exit_time"].dt.strftime("%Y-%m-%d %H:%M")
        display_trades["duration_hours"] = display_trades["duration_hours"].round(1)
        
        # 选择要显示的列
        display_columns = [
            "coin", "side", "entry_time", "exit_time", "duration_hours",
            "entry_rate", "exit_rate", "funding_pnl", "trade_pnl", "total_pnl"
        ]
        
        available_columns = [col for col in display_columns if col in display_trades.columns]
        st.dataframe(
            display_trades[available_columns],
            use_container_width=True,
            hide_index=True
        )
        
        # 下载交易记录
        csv = display_trades.to_csv(index=False)
        st.download_button(
            label="📥 下载交易记录 CSV",
            data=csv,
            file_name=f"trades_{selected_event['name'].replace(' ', '_')}.csv",
            mime="text/csv"
        )

    # 相关性分析
    if not trades_df.empty and len(trades_df) > 1:
        st.subheader("🔗 交易指标相关性分析")
        corr_fig = visualizer.plot_correlation_heatmap(trades_df)
        st.plotly_chart(corr_fig, use_container_width=True)

    # 策略分析
    st.subheader("🧠 策略分析")

    # 信号统计
    if "data" in backtest_result:
        signal_data = backtest_result["data"]
        signal_counts = signal_data["signal"].value_counts()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**信号分布:**")
            for signal, count in signal_counts.items():
                st.write(f"- {signal}: {count} 次")
        
        with col2:
            if "zscore" in signal_data.columns:
                st.markdown("**Z-score 统计:**")
                st.write(f"- 最大 Z-score: {signal_data['zscore'].max():.2f}")
                st.write(f"- 最小 Z-score: {signal_data['zscore'].min():.2f}")
                st.write(f"- 平均 Z-score: {signal_data['zscore'].mean():.2f}")

    # 事件影响分析
    st.subheader("📊 事件影响分析")

    # 计算事件前后的资金费率变化
    if "data" in backtest_result:
        data = backtest_result["data"]
        event_time = backtest_result.get("event_time")
        
        if event_time:
            # 事件前24小时
            pre_event = data[data["time"] < event_time]
            # 事件后24小时
            post_event = data[data["time"] > event_time]
            
            if not pre_event.empty and not post_event.empty:
                pre_avg = pre_event["fundingRate"].mean()
                post_avg = post_event["fundingRate"].mean()
                change = post_avg - pre_avg
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("事件前平均资金费率", f"{pre_avg:.4f}%")
                
                with col2:
                    st.metric("事件后平均资金费率", f"{post_avg:.4f}%")
                
                with col3:
                    st.metric("变化幅度", f"{change:.4f}%", f"{change/pre_avg*100:.1f}%" if pre_avg != 0 else "N/A")

    # 页脚
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            📊 事件驱动资金费率回测工具 | 
            数据来源: Hyperliquid API | 
            更新时间: {update_time}
        </div>
        """.format(update_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        unsafe_allow_html=True
    )

    # 侧边栏信息
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📚 使用说明")
    st.sidebar.markdown("""
    1. **选择事件**: 从下拉菜单选择要分析的重大事件
    2. **调整参数**: 设置策略参数（窗口大小、阈值等）
    3. **查看结果**: 分析回测结果和可视化图表
    4. **下载数据**: 可以下载交易记录进行进一步分析
    """)

    st.sidebar.markdown("### ⚠️ 风险提示")
    st.sidebar.markdown("""
    - 本工具仅用于教育和研究目的
    - 历史回测结果不代表未来表现
    - 实际交易存在滑点、手续费等成本
    - 请谨慎投资，风险自负
    """)

# 显示导航
show_navigation()

# 获取当前页面
current_page = get_current_page()

# 根据页面显示不同内容
if current_page == "tutorial":
    show_tutorial_page()
elif current_page == "theory":
    show_theory_page()
else:
    show_main_page()
