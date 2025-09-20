"""
策略模块 - 异常检测和回测逻辑
实现基于 Z-score 的资金费率异常检测和事件驱动回测
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import streamlit as st

class FundingRateStrategy:
    """资金费率策略类"""
    
    def __init__(self, window_hours: int = 24, threshold: float = 2.0):
        """
        初始化策略参数
        
        Args:
            window_hours: 滚动窗口小时数
            threshold: Z-score 阈值
        """
        self.window_hours = window_hours
        self.threshold = threshold
        self.window_points = window_hours // 8  # 每8小时一次资金费率结算
    
    def detect_anomalies(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        检测资金费率异常
        
        Args:
            df: 包含 fundingRate 列的 DataFrame
            
        Returns:
            添加了异常检测信号的 DataFrame
        """
        df = df.copy()
        
        # 计算滚动统计量
        df["mean"] = df["fundingRate"].rolling(window=self.window_points, min_periods=1).mean()
        df["std"] = df["fundingRate"].rolling(window=self.window_points, min_periods=1).std()
        
        # 避免除零错误
        df["std"] = df["std"].replace(0, np.nan)
        
        # 计算 Z-score
        df["zscore"] = (df["fundingRate"] - df["mean"]) / df["std"]
        
        # 生成交易信号
        df["signal"] = df["zscore"].apply(self._generate_signal)
        
        # 标记异常点
        df["is_anomaly"] = df["signal"] != "HOLD"
        
        # 计算信号强度
        df["signal_strength"] = np.abs(df["zscore"])
        
        return df
    
    def _generate_signal(self, zscore: float) -> str:
        """根据 Z-score 生成交易信号"""
        if pd.isna(zscore):
            return "HOLD"
        elif zscore > self.threshold:
            return "SHORT"  # 资金费率过高，做空收取资金费率
        elif zscore < -self.threshold:
            return "LONG"   # 资金费率过低，做多收取资金费率
        else:
            return "HOLD"
    
    def backtest(self, df: pd.DataFrame, initial_capital: float = 10000) -> Dict:
        """
        执行回测
        
        Args:
            df: 包含信号的 DataFrame
            initial_capital: 初始资金
            
        Returns:
            回测结果字典
        """
        trades = []
        positions = {}  # 当前持仓
        capital = initial_capital
        portfolio_value = [initial_capital]
        portfolio_times = [df.iloc[0]["time"]]
        
        for i, row in df.iterrows():
            current_time = row["time"]
            signal = row["signal"]
            funding_rate = row["fundingRate"]
            coin = row["coin"]
            
            # 处理现有持仓的资金费率结算
            for coin_pos, pos_info in positions.items():
                if coin_pos == coin:
                    # 计算资金费率收益
                    funding_pnl = pos_info["size"] * funding_rate / 100
                    capital += funding_pnl
                    
                    # 更新持仓信息
                    pos_info["total_funding_pnl"] += funding_pnl
                    pos_info["last_funding_time"] = current_time
            
            # 处理新信号
            if signal != "HOLD" and coin not in positions:
                # 开新仓
                position_size = capital * 0.1  # 使用10%的资金开仓
                
                positions[coin] = {
                    "side": signal,
                    "entry_time": current_time,
                    "entry_rate": funding_rate,
                    "size": position_size,
                    "total_funding_pnl": 0,
                    "last_funding_time": current_time
                }
                
            elif signal == "HOLD" and coin in positions:
                # 平仓
                pos_info = positions[coin]
                
                trade_pnl = self._calculate_trade_pnl(pos_info, funding_rate, current_time)
                capital += trade_pnl
                
                trades.append({
                    "coin": coin,
                    "side": pos_info["side"],
                    "entry_time": pos_info["entry_time"],
                    "exit_time": current_time,
                    "entry_rate": pos_info["entry_rate"],
                    "exit_rate": funding_rate,
                    "position_size": pos_info["size"],
                    "funding_pnl": pos_info["total_funding_pnl"],
                    "trade_pnl": trade_pnl,
                    "total_pnl": pos_info["total_funding_pnl"] + trade_pnl,
                    "duration_hours": (current_time - pos_info["entry_time"]).total_seconds() / 3600
                })
                
                del positions[coin]
            
            # 记录组合价值
            portfolio_value.append(capital)
            portfolio_times.append(current_time)
        
        # 计算回测统计
        trades_df = pd.DataFrame(trades) if trades else pd.DataFrame()
        
        stats = self._calculate_backtest_stats(trades_df, initial_capital, capital)
        
        return {
            "trades": trades_df,
            "portfolio_value": portfolio_value,
            "portfolio_times": portfolio_times,
            "final_capital": capital,
            "stats": stats,
            "positions": positions  # 未平仓的持仓
        }
    
    def _calculate_trade_pnl(self, position: Dict, exit_rate: float, exit_time: datetime) -> float:
        """计算交易盈亏"""
        entry_rate = position["entry_rate"]
        side = position["side"]
        
        if side == "LONG":
            # 做多：希望资金费率上涨
            rate_change = exit_rate - entry_rate
        else:  # SHORT
            # 做空：希望资金费率下跌
            rate_change = entry_rate - exit_rate
        
        # 简化的盈亏计算（实际应该考虑价格变动）
        return position["size"] * rate_change / 100
    
    def _calculate_backtest_stats(self, trades_df: pd.DataFrame, initial_capital: float, final_capital: float) -> Dict:
        """计算回测统计指标"""
        if trades_df.empty:
            return {
                "total_return": 0,
                "total_return_pct": 0,
                "total_trades": 0,
                "winning_trades": 0,
                "losing_trades": 0,
                "win_rate": 0,
                "avg_trade_pnl": 0,
                "max_drawdown": 0,
                "sharpe_ratio": 0
            }
        
        total_return = final_capital - initial_capital
        total_return_pct = (total_return / initial_capital) * 100
        
        total_trades = len(trades_df)
        winning_trades = len(trades_df[trades_df["total_pnl"] > 0])
        losing_trades = len(trades_df[trades_df["total_pnl"] < 0])
        win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
        
        avg_trade_pnl = trades_df["total_pnl"].mean()
        
        # 计算最大回撤
        cumulative_pnl = trades_df["total_pnl"].cumsum()
        running_max = cumulative_pnl.expanding().max()
        drawdown = cumulative_pnl - running_max
        max_drawdown = drawdown.min()
        
        # 计算夏普比率（简化版）
        if trades_df["total_pnl"].std() > 0:
            sharpe_ratio = trades_df["total_pnl"].mean() / trades_df["total_pnl"].std()
        else:
            sharpe_ratio = 0
        
        return {
            "total_return": total_return,
            "total_return_pct": total_return_pct,
            "total_trades": total_trades,
            "winning_trades": winning_trades,
            "losing_trades": losing_trades,
            "win_rate": win_rate,
            "avg_trade_pnl": avg_trade_pnl,
            "max_drawdown": max_drawdown,
            "sharpe_ratio": sharpe_ratio
        }

class EventDrivenBacktester:
    """事件驱动回测器"""
    
    def __init__(self, strategy: FundingRateStrategy):
        self.strategy = strategy
    
    def run_event_backtest(self, event: Dict, funding_data: pd.DataFrame, price_data: pd.DataFrame = None) -> Dict:
        """
        运行单个事件的回测
        
        Args:
            event: 事件信息字典
            funding_data: 资金费率数据
            price_data: 价格数据（可选）
            
        Returns:
            回测结果
        """
        event_time = datetime.fromisoformat(event["timestamp"])
        coin = event["coin"]
        
        # 过滤事件窗口数据
        window_start = event_time - timedelta(hours=24)
        window_end = event_time + timedelta(hours=72)
        
        event_funding_data = funding_data[
            (funding_data["time"] >= window_start) & 
            (funding_data["time"] <= window_end)
        ].copy()
        
        if event_funding_data.empty:
            st.warning(f"事件 {event['name']} 窗口内无数据")
            return {}
        
        # 标记事件时间点
        event_funding_data["is_event_time"] = event_funding_data["time"] == event_time
        
        # 执行异常检测
        event_funding_data = self.strategy.detect_anomalies(event_funding_data)
        
        # 执行回测
        backtest_result = self.strategy.backtest(event_funding_data)
        
        # 添加事件信息
        backtest_result["event"] = event
        backtest_result["event_time"] = event_time
        backtest_result["data"] = event_funding_data
        
        return backtest_result
    
    def run_multiple_events(self, events: List[Dict], funding_data: Dict[str, pd.DataFrame]) -> Dict:
        """
        运行多个事件的回测
        
        Args:
            events: 事件列表
            funding_data: 按币种分组的资金费率数据
            
        Returns:
            所有事件的回测结果
        """
        results = {}
        
        for event in events:
            coin = event["coin"]
            if coin in funding_data:
                result = self.run_event_backtest(event, funding_data[coin])
                if result:
                    results[event["name"]] = result
            else:
                st.warning(f"币种 {coin} 的数据不可用")
        
        return results

# 便捷函数
def detect_anomalies(df: pd.DataFrame, window_hours: int = 24, threshold: float = 2.0) -> pd.DataFrame:
    """检测资金费率异常的便捷函数"""
    strategy = FundingRateStrategy(window_hours, threshold)
    return strategy.detect_anomalies(df)

def backtest(df: pd.DataFrame, initial_capital: float = 10000) -> Dict:
    """执行回测的便捷函数"""
    strategy = FundingRateStrategy()
    return strategy.backtest(df, initial_capital)

# 测试函数
def test_strategy():
    """测试策略功能"""
    print("测试策略功能...")
    
    # 创建测试数据
    dates = pd.date_range(start='2024-01-01', end='2024-01-10', freq='8H')
    np.random.seed(42)
    
    # 生成测试资金费率数据
    funding_rates = np.random.normal(0, 0.02, len(dates))
    # 添加一些异常值
    funding_rates[10] = 0.08  # 异常高
    funding_rates[15] = -0.06  # 异常低
    
    test_df = pd.DataFrame({
        'time': dates,
        'fundingRate': funding_rates,
        'coin': 'BTC'
    })
    
    # 测试异常检测
    strategy = FundingRateStrategy()
    result_df = strategy.detect_anomalies(test_df)
    
    print("异常检测结果:")
    print(result_df[result_df["is_anomaly"]][["time", "fundingRate", "zscore", "signal"]])
    
    # 测试回测
    backtest_result = strategy.backtest(result_df)
    print(f"\n回测结果:")
    print(f"总交易数: {backtest_result['stats']['total_trades']}")
    print(f"胜率: {backtest_result['stats']['win_rate']:.2f}%")
    print(f"总收益: {backtest_result['stats']['total_return_pct']:.2f}%")

if __name__ == "__main__":
    test_strategy()
