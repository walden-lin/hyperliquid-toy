"""
可视化模块 - Plotly 图表绘制
提供资金费率、价格、回测结果的可视化功能
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional

class FundingRateVisualizer:
    """资金费率可视化器"""
    
    def __init__(self):
        self.color_scheme = {
            'BTC': '#F7931A',
            'ETH': '#627EEA', 
            'SOL': '#9945FF',
            'BNB': '#F3BA2F',
            'LONG': '#00C851',
            'SHORT': '#FF4444',
            'HOLD': '#6C757D'
        }
    
    def plot_funding_rate_with_signals(self, df: pd.DataFrame, event_time: Optional[datetime] = None) -> go.Figure:
        """
        绘制资金费率曲线和交易信号
        
        Args:
            df: 包含资金费率和信号的 DataFrame
            event_time: 事件时间点（可选）
            
        Returns:
            Plotly Figure 对象
        """
        fig = go.Figure()
        
        # 主资金费率曲线
        fig.add_trace(go.Scatter(
            x=df["time"],
            y=df["fundingRate"],
            mode='lines',
            name='资金费率',
            line=dict(color='#1f77b4', width=2),
            hovertemplate='<b>时间:</b> %{x}<br><b>资金费率:</b> %{y:.4f}%<extra></extra>'
        ))
        
        # 添加滚动均值和标准差
        if "mean" in df.columns:
            fig.add_trace(go.Scatter(
                x=df["time"],
                y=df["mean"],
                mode='lines',
                name='滚动均值',
                line=dict(color='orange', width=1, dash='dash'),
                opacity=0.7
            ))
            
            # 添加置信区间
            if "std" in df.columns:
                upper_bound = df["mean"] + 2 * df["std"]
                lower_bound = df["mean"] - 2 * df["std"]
                
                fig.add_trace(go.Scatter(
                    x=df["time"],
                    y=upper_bound,
                    mode='lines',
                    line=dict(width=0),
                    showlegend=False,
                    hoverinfo='skip'
                ))
                
                fig.add_trace(go.Scatter(
                    x=df["time"],
                    y=lower_bound,
                    mode='lines',
                    line=dict(width=0),
                    fill='tonexty',
                    fillcolor='rgba(255, 165, 0, 0.2)',
                    name='±2σ 区间',
                    hoverinfo='skip'
                ))
        
        # 添加交易信号
        if "signal" in df.columns:
            # LONG 信号
            long_signals = df[df["signal"] == "LONG"]
            if not long_signals.empty:
                fig.add_trace(go.Scatter(
                    x=long_signals["time"],
                    y=long_signals["fundingRate"],
                    mode='markers',
                    name='LONG 信号',
                    marker=dict(
                        color=self.color_scheme['LONG'],
                        size=10,
                        symbol='triangle-up'
                    ),
                    hovertemplate='<b>LONG 信号</b><br>时间: %{x}<br>资金费率: %{y:.4f}%<br>Z-score: %{customdata:.2f}<extra></extra>',
                    customdata=long_signals["zscore"]
                ))
            
            # SHORT 信号
            short_signals = df[df["signal"] == "SHORT"]
            if not short_signals.empty:
                fig.add_trace(go.Scatter(
                    x=short_signals["time"],
                    y=short_signals["fundingRate"],
                    mode='markers',
                    name='SHORT 信号',
                    marker=dict(
                        color=self.color_scheme['SHORT'],
                        size=10,
                        symbol='triangle-down'
                    ),
                    hovertemplate='<b>SHORT 信号</b><br>时间: %{x}<br>资金费率: %{y:.4f}%<br>Z-score: %{customdata:.2f}<extra></extra>',
                    customdata=short_signals["zscore"]
                ))
        
        # 添加事件时间线
        if event_time:
            # 确保 event_time 是 datetime 对象
            if isinstance(event_time, str):
                event_time = pd.to_datetime(event_time)
            
            # 使用 add_shape 而不是 add_vline 来避免类型错误
            fig.add_shape(
                type="line",
                x0=event_time,
                x1=event_time,
                y0=0,
                y1=1,
                yref="paper",
                line=dict(color="red", width=2, dash="dash")
            )
            
            # 添加事件时间标注
            fig.add_annotation(
                x=event_time,
                y=1,
                yref="paper",
                text="事件时间",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor="red",
                ax=0,
                ay=-40,
                bgcolor="white",
                bordercolor="red",
                borderwidth=1
            )
        
        # 添加零线
        fig.add_hline(y=0, line_dash="dot", line_color="gray", opacity=0.5)
        
        # 更新布局
        fig.update_layout(
            title="资金费率走势与交易信号",
            xaxis_title="时间",
            yaxis_title="资金费率 (%)",
            hovermode='x unified',
            height=500,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig
    
    def plot_price_with_events(self, price_df: pd.DataFrame, event_time: Optional[datetime] = None) -> go.Figure:
        """
        绘制价格曲线和事件标记
        
        Args:
            price_df: 价格数据 DataFrame
            event_time: 事件时间点（可选）
            
        Returns:
            Plotly Figure 对象
        """
        fig = go.Figure()
        
        # 价格曲线
        fig.add_trace(go.Scatter(
            x=price_df["time"],
            y=price_df["price"],
            mode='lines',
            name='价格',
            line=dict(color='#2E8B57', width=2),
            hovertemplate='<b>时间:</b> %{x}<br><b>价格:</b> $%{y:,.2f}<extra></extra>'
        ))
        
        # 添加事件时间线
        if event_time:
            # 确保 event_time 是 datetime 对象
            if isinstance(event_time, str):
                event_time = pd.to_datetime(event_time)
            
            # 使用 add_shape 而不是 add_vline 来避免类型错误
            fig.add_shape(
                type="line",
                x0=event_time,
                x1=event_time,
                y0=0,
                y1=1,
                yref="paper",
                line=dict(color="red", width=2, dash="dash")
            )
            
            # 添加事件时间标注
            fig.add_annotation(
                x=event_time,
                y=1,
                yref="paper",
                text="事件时间",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor="red",
                ax=0,
                ay=-40,
                bgcolor="white",
                bordercolor="red",
                borderwidth=1
            )
        
        # 更新布局
        fig.update_layout(
            title="价格走势",
            xaxis_title="时间",
            yaxis_title="价格 (USD)",
            hovermode='x unified',
            height=400,
            showlegend=True
        )
        
        return fig
    
    def plot_portfolio_performance(self, portfolio_times: List[datetime], portfolio_values: List[float]) -> go.Figure:
        """
        绘制组合表现曲线
        
        Args:
            portfolio_times: 时间序列
            portfolio_values: 组合价值序列
            
        Returns:
            Plotly Figure 对象
        """
        fig = go.Figure()
        
        # 组合价值曲线
        fig.add_trace(go.Scatter(
            x=portfolio_times,
            y=portfolio_values,
            mode='lines',
            name='组合价值',
            line=dict(color='#17a2b8', width=2),
            hovertemplate='<b>时间:</b> %{x}<br><b>组合价值:</b> $%{y:,.2f}<extra></extra>'
        ))
        
        # 添加初始资金线
        if portfolio_values:
            initial_value = portfolio_values[0]
            fig.add_hline(
                y=initial_value,
                line_dash="dash",
                line_color="gray",
                annotation_text=f"初始资金: ${initial_value:,.2f}",
                annotation_position="bottom right"
            )
        
        # 更新布局
        fig.update_layout(
            title="组合表现",
            xaxis_title="时间",
            yaxis_title="组合价值 (USD)",
            hovermode='x unified',
            height=400,
            showlegend=True
        )
        
        return fig
    
    def plot_trades_timeline(self, trades_df: pd.DataFrame) -> go.Figure:
        """
        绘制交易时间线
        
        Args:
            trades_df: 交易记录 DataFrame
            
        Returns:
            Plotly Figure 对象
        """
        if trades_df.empty:
            fig = go.Figure()
            fig.add_annotation(
                text="暂无交易记录",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16)
            )
            fig.update_layout(
                title="交易时间线",
                height=300,
                showlegend=False
            )
            return fig
        
        fig = go.Figure()
        
        # 为每个交易添加时间线
        for i, trade in trades_df.iterrows():
            # 交易持续时间
            duration = trade["duration_hours"]
            
            # 根据盈亏选择颜色
            color = self.color_scheme['LONG'] if trade["total_pnl"] > 0 else self.color_scheme['SHORT']
            
            # 添加交易线段
            fig.add_trace(go.Scatter(
                x=[trade["entry_time"], trade["exit_time"]],
                y=[i, i],
                mode='lines+markers',
                name=f'{trade["side"]} {trade["coin"]}',
                line=dict(color=color, width=3),
                marker=dict(size=8),
                showlegend=False,
                hovertemplate=f'<b>{trade["side"]} {trade["coin"]}</b><br>' +
                            f'入场: {trade["entry_time"]}<br>' +
                            f'出场: {trade["exit_time"]}<br>' +
                            f'持续时间: {duration:.1f}小时<br>' +
                            f'盈亏: ${trade["total_pnl"]:.2f}<extra></extra>'
            ))
        
        # 更新布局
        fig.update_layout(
            title="交易时间线",
            xaxis_title="时间",
            yaxis_title="交易序号",
            height=max(300, len(trades_df) * 50),
            showlegend=False
        )
        
        return fig
    
    def plot_correlation_heatmap(self, trades_df: pd.DataFrame) -> go.Figure:
        """
        绘制交易指标相关性热力图
        
        Args:
            trades_df: 交易记录 DataFrame
            
        Returns:
            Plotly Figure 对象
        """
        if trades_df.empty or len(trades_df) < 2:
            fig = go.Figure()
            fig.add_annotation(
                text="数据不足，无法计算相关性",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16)
            )
            fig.update_layout(
                title="交易指标相关性",
                height=400,
                showlegend=False
            )
            return fig
        
        # 选择数值列进行相关性分析
        numeric_cols = ['entry_rate', 'exit_rate', 'position_size', 'funding_pnl', 'trade_pnl', 'total_pnl', 'duration_hours']
        available_cols = [col for col in numeric_cols if col in trades_df.columns]
        
        if len(available_cols) < 2:
            fig = go.Figure()
            fig.add_annotation(
                text="数值列不足，无法计算相关性",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16)
            )
            fig.update_layout(
                title="交易指标相关性",
                height=400,
                showlegend=False
            )
            return fig
        
        # 计算相关性矩阵
        corr_matrix = trades_df[available_cols].corr()
        
        # 创建热力图
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=np.round(corr_matrix.values, 2),
            texttemplate="%{text}",
            textfont={"size": 10},
            hoverongaps=False
        ))
        
        fig.update_layout(
            title="交易指标相关性矩阵",
            height=500,
            xaxis_title="指标",
            yaxis_title="指标"
        )
        
        return fig
    
    def create_dashboard(self, backtest_result: Dict) -> List[go.Figure]:
        """
        创建完整的回测仪表板
        
        Args:
            backtest_result: 回测结果字典
            
        Returns:
            图表列表
        """
        figures = []
        
        # 1. 资金费率走势图
        if "data" in backtest_result:
            funding_fig = self.plot_funding_rate_with_signals(
                backtest_result["data"],
                backtest_result.get("event_time")
            )
            figures.append(funding_fig)
        
        # 2. 组合表现图
        if "portfolio_times" in backtest_result and "portfolio_value" in backtest_result:
            portfolio_fig = self.plot_portfolio_performance(
                backtest_result["portfolio_times"],
                backtest_result["portfolio_value"]
            )
            figures.append(portfolio_fig)
        
        # 3. 交易时间线
        if "trades" in backtest_result and not backtest_result["trades"].empty:
            trades_fig = self.plot_trades_timeline(backtest_result["trades"])
            figures.append(trades_fig)
        
        # 4. 相关性热力图
        if "trades" in backtest_result and not backtest_result["trades"].empty:
            corr_fig = self.plot_correlation_heatmap(backtest_result["trades"])
            figures.append(corr_fig)
        
        return figures

# 便捷函数
def plot_funding(df: pd.DataFrame, event_time: Optional[datetime] = None) -> go.Figure:
    """绘制资金费率的便捷函数"""
    visualizer = FundingRateVisualizer()
    return visualizer.plot_funding_rate_with_signals(df, event_time)

def plot_portfolio(portfolio_times: List[datetime], portfolio_values: List[float]) -> go.Figure:
    """绘制组合表现的便捷函数"""
    visualizer = FundingRateVisualizer()
    return visualizer.plot_portfolio_performance(portfolio_times, portfolio_values)

# 测试函数
def test_visualization():
    """测试可视化功能"""
    print("测试可视化功能...")
    
    # 创建测试数据
    dates = pd.date_range(start='2024-01-01', end='2024-01-10', freq='8H')
    np.random.seed(42)
    
    funding_rates = np.random.normal(0, 0.02, len(dates))
    funding_rates[5] = 0.08  # 异常值
    
    test_df = pd.DataFrame({
        'time': dates,
        'fundingRate': funding_rates,
        'mean': np.mean(funding_rates),
        'std': np.std(funding_rates),
        'zscore': (funding_rates - np.mean(funding_rates)) / np.std(funding_rates),
        'signal': ['HOLD'] * len(dates)
    })
    test_df.loc[5, 'signal'] = 'SHORT'
    
    # 测试绘图
    visualizer = FundingRateVisualizer()
    fig = visualizer.plot_funding_rate_with_signals(test_df)
    
    print("可视化测试完成")
    return fig

if __name__ == "__main__":
    test_visualization()
