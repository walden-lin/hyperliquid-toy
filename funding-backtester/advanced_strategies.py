"""
高级策略模块 - 多种资金费率异常检测策略
包含常见的资金费率套利和异常检测策略
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import streamlit as st

class AdvancedFundingRateStrategies:
    """高级资金费率策略集合"""
    
    def __init__(self):
        self.strategies = {
            "Z-Score 异常检测": self.zscore_strategy,
            "百分位数策略": self.percentile_strategy,
            "移动平均偏离": self.ma_deviation_strategy,
            "波动率突破": self.volatility_breakout_strategy,
            "资金费率反转": self.funding_reversal_strategy,
            "多时间框架": self.multi_timeframe_strategy,
            "均值回归": self.mean_reversion_strategy,
            "动量策略": self.momentum_strategy
        }
    
    def zscore_strategy(self, df: pd.DataFrame, window: int = 24, threshold: float = 2.0) -> pd.DataFrame:
        """
        策略1: Z-Score 异常检测
        基于统计学的异常检测方法
        """
        df = df.copy()
        window_points = window // 8
        
        # 计算滚动统计量
        df["mean"] = df["fundingRate"].rolling(window=window_points, min_periods=1).mean()
        df["std"] = df["fundingRate"].rolling(window=window_points, min_periods=1).std()
        df["std"] = df["std"].replace(0, np.nan)
        
        # 计算 Z-score
        df["zscore"] = (df["fundingRate"] - df["mean"]) / df["std"]
        
        # 生成信号
        df["signal"] = "HOLD"
        df.loc[df["zscore"] > threshold, "signal"] = "SHORT"
        df.loc[df["zscore"] < -threshold, "signal"] = "LONG"
        
        df["strategy_name"] = "Z-Score 异常检测"
        df["confidence"] = np.abs(df["zscore"]) / threshold
        
        return df
    
    def percentile_strategy(self, df: pd.DataFrame, window: int = 24, upper_pct: float = 95, lower_pct: float = 5) -> pd.DataFrame:
        """
        策略2: 百分位数策略
        基于历史百分位数的异常检测
        """
        df = df.copy()
        window_points = window // 8
        
        # 计算滚动百分位数
        df["upper_bound"] = df["fundingRate"].rolling(window=window_points, min_periods=1).quantile(upper_pct/100)
        df["lower_bound"] = df["fundingRate"].rolling(window=window_points, min_periods=1).quantile(lower_pct/100)
        df["median"] = df["fundingRate"].rolling(window=window_points, min_periods=1).quantile(0.5)
        
        # 生成信号
        df["signal"] = "HOLD"
        df.loc[df["fundingRate"] > df["upper_bound"], "signal"] = "SHORT"
        df.loc[df["fundingRate"] < df["lower_bound"], "signal"] = "LONG"
        
        # 计算偏离程度
        df["deviation"] = np.where(
            df["fundingRate"] > df["upper_bound"],
            (df["fundingRate"] - df["upper_bound"]) / (df["upper_bound"] - df["median"]),
            np.where(
                df["fundingRate"] < df["lower_bound"],
                (df["lower_bound"] - df["fundingRate"]) / (df["median"] - df["lower_bound"]),
                0
            )
        )
        
        df["strategy_name"] = "百分位数策略"
        df["confidence"] = np.abs(df["deviation"])
        
        return df
    
    def ma_deviation_strategy(self, df: pd.DataFrame, short_window: int = 8, long_window: int = 24, threshold: float = 0.5) -> pd.DataFrame:
        """
        策略3: 移动平均偏离策略
        基于短期和长期移动平均的偏离
        """
        df = df.copy()
        short_points = short_window // 8
        long_points = long_window // 8
        
        # 计算移动平均
        df["ma_short"] = df["fundingRate"].rolling(window=short_points, min_periods=1).mean()
        df["ma_long"] = df["fundingRate"].rolling(window=long_points, min_periods=1).mean()
        
        # 计算偏离百分比
        df["deviation_pct"] = (df["ma_short"] - df["ma_long"]) / df["ma_long"] * 100
        
        # 生成信号
        df["signal"] = "HOLD"
        df.loc[df["deviation_pct"] > threshold, "signal"] = "SHORT"
        df.loc[df["deviation_pct"] < -threshold, "signal"] = "LONG"
        
        df["strategy_name"] = "移动平均偏离"
        df["confidence"] = np.abs(df["deviation_pct"]) / threshold
        
        return df
    
    def volatility_breakout_strategy(self, df: pd.DataFrame, window: int = 24, volatility_threshold: float = 2.0) -> pd.DataFrame:
        """
        策略4: 波动率突破策略
        基于波动率异常的检测
        """
        df = df.copy()
        window_points = window // 8
        
        # 计算滚动波动率
        df["volatility"] = df["fundingRate"].rolling(window=window_points, min_periods=1).std()
        df["vol_mean"] = df["volatility"].rolling(window=window_points, min_periods=1).mean()
        
        # 计算波动率 Z-score
        df["vol_zscore"] = (df["volatility"] - df["vol_mean"]) / df["vol_mean"]
        
        # 计算价格变化
        df["price_change"] = df["fundingRate"].diff()
        
        # 生成信号
        df["signal"] = "HOLD"
        df.loc[(df["vol_zscore"] > volatility_threshold) & (df["price_change"] > 0), "signal"] = "SHORT"
        df.loc[(df["vol_zscore"] > volatility_threshold) & (df["price_change"] < 0), "signal"] = "LONG"
        
        df["strategy_name"] = "波动率突破"
        df["confidence"] = df["vol_zscore"] / volatility_threshold
        
        return df
    
    def funding_reversal_strategy(self, df: pd.DataFrame, window: int = 16, reversal_threshold: float = 0.3) -> pd.DataFrame:
        """
        策略5: 资金费率反转策略
        基于资金费率极值后的反转
        """
        df = df.copy()
        window_points = window // 8
        
        # 计算滚动极值
        df["rolling_max"] = df["fundingRate"].rolling(window=window_points, min_periods=1).max()
        df["rolling_min"] = df["fundingRate"].rolling(window=window_points, min_periods=1).min()
        
        # 检测极值点
        df["is_max"] = df["fundingRate"] == df["rolling_max"]
        df["is_min"] = df["fundingRate"] == df["rolling_min"]
        
        # 计算反转信号
        df["reversal_signal"] = 0
        df.loc[df["is_max"], "reversal_signal"] = -1  # 高点反转做空
        df.loc[df["is_min"], "reversal_signal"] = 1   # 低点反转做多
        
        # 计算反转强度
        df["reversal_strength"] = np.where(
            df["reversal_signal"] == -1,
            (df["fundingRate"] - df["rolling_min"]) / (df["rolling_max"] - df["rolling_min"]),
            np.where(
                df["reversal_signal"] == 1,
                (df["rolling_max"] - df["fundingRate"]) / (df["rolling_max"] - df["rolling_min"]),
                0
            )
        )
        
        # 生成信号
        df["signal"] = "HOLD"
        df.loc[(df["reversal_signal"] == -1) & (df["reversal_strength"] > reversal_threshold), "signal"] = "SHORT"
        df.loc[(df["reversal_signal"] == 1) & (df["reversal_strength"] > reversal_threshold), "signal"] = "LONG"
        
        df["strategy_name"] = "资金费率反转"
        df["confidence"] = df["reversal_strength"]
        
        return df
    
    def multi_timeframe_strategy(self, df: pd.DataFrame, short_window: int = 8, long_window: int = 48) -> pd.DataFrame:
        """
        策略6: 多时间框架策略
        结合短期和长期趋势
        """
        df = df.copy()
        short_points = short_window // 8
        long_points = long_window // 8
        
        # 短期趋势
        df["short_trend"] = df["fundingRate"].rolling(window=short_points, min_periods=1).mean()
        df["short_slope"] = df["short_trend"].diff()
        
        # 长期趋势
        df["long_trend"] = df["fundingRate"].rolling(window=long_points, min_periods=1).mean()
        df["long_slope"] = df["long_trend"].diff()
        
        # 趋势一致性
        df["trend_consistency"] = np.sign(df["short_slope"]) * np.sign(df["long_slope"])
        
        # 趋势强度
        df["trend_strength"] = np.abs(df["short_slope"]) + np.abs(df["long_slope"])
        
        # 生成信号
        df["signal"] = "HOLD"
        df.loc[(df["trend_consistency"] > 0) & (df["short_slope"] < -0.1), "signal"] = "LONG"
        df.loc[(df["trend_consistency"] > 0) & (df["short_slope"] > 0.1), "signal"] = "SHORT"
        
        df["strategy_name"] = "多时间框架"
        df["confidence"] = df["trend_strength"] * df["trend_consistency"]
        
        return df
    
    def mean_reversion_strategy(self, df: pd.DataFrame, window: int = 24, reversion_threshold: float = 1.5) -> pd.DataFrame:
        """
        策略7: 均值回归策略
        基于均值回归理论
        """
        df = df.copy()
        window_points = window // 8
        
        # 计算移动平均和标准差
        df["ma"] = df["fundingRate"].rolling(window=window_points, min_periods=1).mean()
        df["std"] = df["fundingRate"].rolling(window=window_points, min_periods=1).std()
        
        # 计算偏离程度
        df["deviation"] = (df["fundingRate"] - df["ma"]) / df["std"]
        
        # 计算回归速度
        df["reversion_speed"] = -df["deviation"].diff()
        
        # 生成信号
        df["signal"] = "HOLD"
        df.loc[(df["deviation"] > reversion_threshold) & (df["reversion_speed"] > 0), "signal"] = "SHORT"
        df.loc[(df["deviation"] < -reversion_threshold) & (df["reversion_speed"] < 0), "signal"] = "LONG"
        
        df["strategy_name"] = "均值回归"
        df["confidence"] = np.abs(df["deviation"]) / reversion_threshold
        
        return df
    
    def momentum_strategy(self, df: pd.DataFrame, window: int = 16, momentum_threshold: float = 0.2) -> pd.DataFrame:
        """
        策略8: 动量策略
        基于价格动量
        """
        df = df.copy()
        window_points = window // 8
        
        # 计算动量
        df["momentum"] = df["fundingRate"].diff(window_points)
        df["momentum_ma"] = df["momentum"].rolling(window=window_points, min_periods=1).mean()
        
        # 计算动量变化率
        df["momentum_change"] = df["momentum"].diff()
        
        # 生成信号
        df["signal"] = "HOLD"
        df.loc[(df["momentum"] > momentum_threshold) & (df["momentum_change"] > 0), "signal"] = "SHORT"
        df.loc[(df["momentum"] < -momentum_threshold) & (df["momentum_change"] < 0), "signal"] = "LONG"
        
        df["strategy_name"] = "动量策略"
        df["confidence"] = np.abs(df["momentum"]) / momentum_threshold
        
        return df
    
    def run_strategy_comparison(self, df: pd.DataFrame, strategy_params: Dict = None) -> Dict[str, pd.DataFrame]:
        """
        运行所有策略并返回结果对比
        
        Args:
            df: 资金费率数据
            strategy_params: 策略参数字典
            
        Returns:
            包含所有策略结果的字典
        """
        if strategy_params is None:
            strategy_params = {
                "Z-Score 异常检测": {"window": 24, "threshold": 2.0},
                "百分位数策略": {"window": 24, "upper_pct": 95, "lower_pct": 5},
                "移动平均偏离": {"short_window": 8, "long_window": 24, "threshold": 0.5},
                "波动率突破": {"window": 24, "volatility_threshold": 2.0},
                "资金费率反转": {"window": 16, "reversal_threshold": 0.3},
                "多时间框架": {"short_window": 8, "long_window": 48},
                "均值回归": {"window": 24, "reversion_threshold": 1.5},
                "动量策略": {"window": 16, "momentum_threshold": 0.2}
            }
        
        results = {}
        for strategy_name, strategy_func in self.strategies.items():
            try:
                params = strategy_params.get(strategy_name, {})
                result = strategy_func(df, **params)
                results[strategy_name] = result
            except Exception as e:
                st.error(f"策略 {strategy_name} 执行失败: {e}")
                continue
        
        return results
    
    def calculate_strategy_metrics(self, results: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        计算策略性能指标
        
        Args:
            results: 策略结果字典
            
        Returns:
            包含性能指标的 DataFrame
        """
        metrics = []
        
        for strategy_name, df in results.items():
            # 计算信号统计
            total_signals = len(df[df["signal"] != "HOLD"])
            long_signals = len(df[df["signal"] == "LONG"])
            short_signals = len(df[df["signal"] == "SHORT"])
            
            # 计算平均置信度
            avg_confidence = df[df["signal"] != "HOLD"]["confidence"].mean() if total_signals > 0 else 0
            
            # 计算信号分布
            signal_distribution = df["signal"].value_counts()
            
            metrics.append({
                "策略名称": strategy_name,
                "总信号数": total_signals,
                "做多信号": long_signals,
                "做空信号": short_signals,
                "平均置信度": round(avg_confidence, 3),
                "信号频率": round(total_signals / len(df) * 100, 2),
                "做多比例": round(long_signals / total_signals * 100, 2) if total_signals > 0 else 0,
                "做空比例": round(short_signals / total_signals * 100, 2) if total_signals > 0 else 0
            })
        
        return pd.DataFrame(metrics)
