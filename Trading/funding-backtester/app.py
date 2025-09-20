"""
事件驱动资金费率回测工具 - Streamlit Cloud 版本
简化版本，专门用于云端部署
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
import requests
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# 页面配置
st.set_page_config(
    page_title="📊 事件驱动资金费率回测工具",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS
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
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

def load_events():
    """加载事件配置"""
    try:
        with open('events.json', 'r', encoding='utf-8') as f:
            events = json.load(f)
        return events
    except FileNotFoundError:
        st.error("❌ 找不到 events.json 文件")
        return []
    except json.JSONDecodeError:
        st.error("❌ events.json 文件格式错误")
        return []

def get_mock_funding_data(coin, start_time, end_time):
    """生成模拟资金费率数据"""
    # 生成时间序列
    time_range = pd.date_range(start=start_time, end=end_time, freq='8h')
    
    # 生成模拟资金费率数据
    np.random.seed(42)  # 确保结果可重现
    base_rate = 0.0001  # 基础费率 0.01%
    
    # 添加一些随机波动
    rates = []
    for i, t in enumerate(time_range):
        # 基础费率 + 随机波动
        rate = base_rate + np.random.normal(0, 0.00005)
        # 确保费率在合理范围内
        rate = max(-0.001, min(0.001, rate))
        rates.append(rate * 100)  # 转换为百分比
    
    df = pd.DataFrame({
        'time': time_range,
        'fundingRate': rates
    })
    
    return df

def detect_anomalies(df, window=3, threshold=2):
    """检测资金费率异常"""
    df = df.copy()
    df['mean'] = df['fundingRate'].rolling(window=window, min_periods=1).mean()
    df['std'] = df['fundingRate'].rolling(window=window, min_periods=1).std()
    df['zscore'] = (df['fundingRate'] - df['mean']) / df['std']
    df['zscore'] = df['zscore'].fillna(0)
    
    # 生成信号
    df['signal'] = 'HOLD'
    df.loc[df['zscore'] > threshold, 'signal'] = 'SHORT'
    df.loc[df['zscore'] < -threshold, 'signal'] = 'LONG'
    
    return df

def plot_funding_rate(df, event_name, event_time):
    """绘制资金费率图表"""
    fig = go.Figure()
    
    # 添加资金费率线
    fig.add_trace(go.Scatter(
        x=df['time'],
        y=df['fundingRate'],
        mode='lines',
        name='资金费率',
        line=dict(color='#1f77b4', width=2)
    ))
    
    # 添加异常点
    anomalies = df[df['signal'] != 'HOLD']
    if not anomalies.empty:
        fig.add_trace(go.Scatter(
            x=anomalies['time'],
            y=anomalies['fundingRate'],
            mode='markers',
            name='异常信号',
            marker=dict(
                color=anomalies['signal'].map({'LONG': 'green', 'SHORT': 'red'}),
                size=10,
                symbol='diamond'
            )
        ))
    
    # 添加事件时间线
    if event_time:
        fig.add_vline(
            x=event_time,
            line_dash="dash",
            line_color="orange",
            annotation_text=f"事件: {event_name}",
            annotation_position="top"
        )
    
    fig.update_layout(
        title=f"资金费率分析 - {event_name}",
        xaxis_title="时间",
        yaxis_title="资金费率 (%)",
        hovermode='x unified',
        height=500
    )
    
    return fig

def main():
    """主应用函数"""
    st.markdown('<h1 class="main-header">📊 事件驱动资金费率回测工具</h1>', unsafe_allow_html=True)
    
    # 加载事件数据
    events = load_events()
    if not events:
        st.error("无法加载事件配置，请检查 events.json 文件")
        return
    
    # 侧边栏配置
    st.sidebar.header("⚙️ 配置选项")
    
    # 事件选择
    event_names = [event['name'] for event in events]
    selected_event_name = st.sidebar.selectbox("选择事件", event_names)
    
    # 获取选中事件
    selected_event = next(event for event in events if event['name'] == selected_event_name)
    
    # 策略参数
    st.sidebar.subheader("📊 策略参数")
    window_size = st.sidebar.slider("滚动窗口大小", 1, 10, 3)
    threshold = st.sidebar.slider("Z-score 阈值", 1.0, 5.0, 2.0)
    
    # 显示事件信息
    st.subheader("📅 事件信息")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("事件名称", selected_event['name'])
    with col2:
        st.metric("相关币种", selected_event['coin'])
    with col3:
        st.metric("事件时间", selected_event['timestamp'])
    
    st.info(f"📝 **事件描述**: {selected_event['description']}")
    
    # 数据获取和分析
    st.subheader("📈 数据分析")
    
    # 计算时间范围
    event_time = datetime.fromisoformat(selected_event['timestamp'])
    start_time = event_time - timedelta(hours=24)
    end_time = event_time + timedelta(hours=72)
    
    # 获取数据
    with st.spinner("正在获取数据..."):
        df = get_mock_funding_data(selected_event['coin'], start_time, end_time)
        df = detect_anomalies(df, window=window_size, threshold=threshold)
    
    # 显示图表
    fig = plot_funding_rate(df, selected_event['name'], event_time)
    st.plotly_chart(fig, use_container_width=True)
    
    # 显示统计信息
    st.subheader("📊 统计信息")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("数据点数", len(df))
    with col2:
        st.metric("平均费率", f"{df['fundingRate'].mean():.4f}%")
    with col3:
        st.metric("最大费率", f"{df['fundingRate'].max():.4f}%")
    with col4:
        st.metric("最小费率", f"{df['fundingRate'].min():.4f}%")
    
    # 显示异常信号
    anomalies = df[df['signal'] != 'HOLD']
    if not anomalies.empty:
        st.subheader("🚨 异常信号")
        st.dataframe(anomalies[['time', 'fundingRate', 'zscore', 'signal']], use_container_width=True)
    else:
        st.info("✅ 未检测到异常信号")
    
    # 显示原始数据
    if st.checkbox("显示原始数据"):
        st.subheader("📋 原始数据")
        st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()
