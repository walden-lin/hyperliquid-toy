#!/usr/bin/env python3
"""
Hyperliquid API 调试脚本
用于测试和验证 Hyperliquid fundingHistory 接口的正确用法
"""

import requests
import pandas as pd
import json
from datetime import datetime, timedelta
import time

class HyperliquidAPIDebugger:
    """Hyperliquid API 调试器"""
    
    def __init__(self):
        self.base_url = "https://api.hyperliquid.xyz/info"
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        })
    
    def test_funding_history_api(self, coin="BTC", hours_back=48):
        """
        测试 fundingHistory API
        
        Args:
            coin: 币种符号
            hours_back: 获取多少小时前的数据
        """
        print(f"🔍 测试 Hyperliquid fundingHistory API")
        print(f"币种: {coin}")
        print(f"时间范围: 过去 {hours_back} 小时")
        print("-" * 50)
        
        # 计算时间范围
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours_back)
        
        print(f"开始时间: {start_time} (UTC)")
        print(f"结束时间: {end_time} (UTC)")
        print(f"开始时间戳: {int(start_time.timestamp() * 1000)} (毫秒)")
        print(f"结束时间戳: {int(end_time.timestamp() * 1000)} (毫秒)")
        print("-" * 50)
        
        # 构建正确的请求
        payload = {
            "type": "fundingHistory",  # 关键：使用 "type" 而不是 "method"
            "coin": coin,
            "startTime": int(start_time.timestamp() * 1000),
            "endTime": int(end_time.timestamp() * 1000)
        }
        
        print("📤 发送请求:")
        print(f"URL: {self.base_url}")
        print(f"方法: POST")
        print(f"Headers: {dict(self.session.headers)}")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        print("-" * 50)
        
        try:
            # 发送请求
            response = self.session.post(self.base_url, json=payload, timeout=30)
            
            print(f"📥 响应状态码: {response.status_code}")
            print(f"响应头: {dict(response.headers)}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 请求成功!")
                print(f"返回数据类型: {type(data)}")
                
                if isinstance(data, list):
                    print(f"数据条数: {len(data)}")
                    if data:
                        print(f"第一条数据: {data[0]}")
                        print(f"最后一条数据: {data[-1]}")
                        
                        # 转换为 DataFrame 进行分析
                        df = pd.DataFrame(data)
                        print(f"\n📊 数据分析:")
                        print(f"列名: {list(df.columns)}")
                        print(f"数据形状: {df.shape}")
                        print(f"前5行数据:")
                        print(df.head())
                        
                        # 检查时间字段
                        if "time" in df.columns:
                            df["datetime"] = pd.to_datetime(df["time"], unit="ms")
                            print(f"\n⏰ 时间范围分析:")
                            print(f"最早时间: {df['datetime'].min()}")
                            print(f"最晚时间: {df['datetime'].max()}")
                            print(f"时间间隔: {df['datetime'].max() - df['datetime'].min()}")
                        
                        # 检查资金费率字段
                        if "fundingRate" in df.columns:
                            print(f"\n💰 资金费率分析:")
                            print(f"最小费率: {df['fundingRate'].min()}")
                            print(f"最大费率: {df['fundingRate'].max()}")
                            print(f"平均费率: {df['fundingRate'].mean()}")
                            print(f"费率标准差: {df['fundingRate'].std()}")
                        
                        return df
                    else:
                        print("⚠️ 返回空数据列表")
                        return pd.DataFrame()
                else:
                    print(f"⚠️ 返回数据格式不是列表: {data}")
                    return pd.DataFrame()
            else:
                print(f"❌ 请求失败!")
                print(f"错误响应: {response.text}")
                return pd.DataFrame()
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 网络请求异常: {str(e)}")
            return pd.DataFrame()
        except Exception as e:
            print(f"❌ 其他异常: {str(e)}")
            return pd.DataFrame()
    
    def test_different_coins(self, coins=["BTC", "ETH", "SOL", "BNB"], hours_back=24):
        """测试不同币种的 API 调用"""
        print(f"🪙 测试多个币种的 fundingHistory API")
        print("=" * 60)
        
        results = {}
        for coin in coins:
            print(f"\n测试币种: {coin}")
            print("-" * 30)
            df = self.test_funding_history_api(coin, hours_back)
            results[coin] = df
            
            if not df.empty:
                print(f"✅ {coin} 数据获取成功: {len(df)} 条记录")
            else:
                print(f"❌ {coin} 数据获取失败")
            
            # 避免请求过于频繁
            time.sleep(1)
        
        return results
    
    def test_pagination(self, coin="BTC", total_hours=168):
        """测试分页功能（当数据量超过500条时）"""
        print(f"📄 测试分页功能")
        print(f"币种: {coin}")
        print(f"总时间范围: {total_hours} 小时")
        print("=" * 60)
        
        all_data = []
        current_time = datetime.utcnow()
        chunk_hours = 48  # 每次请求48小时的数据
        
        for i in range(0, total_hours, chunk_hours):
            start_time = current_time - timedelta(hours=i + chunk_hours)
            end_time = current_time - timedelta(hours=i)
            
            print(f"\n📦 分页 {i//chunk_hours + 1}: {start_time} 到 {end_time}")
            
            payload = {
                "type": "fundingHistory",
                "coin": coin,
                "startTime": int(start_time.timestamp() * 1000),
                "endTime": int(end_time.timestamp() * 1000)
            }
            
            try:
                response = self.session.post(self.base_url, json=payload, timeout=30)
                if response.status_code == 200:
                    data = response.json()
                    if data:
                        all_data.extend(data)
                        print(f"✅ 获取 {len(data)} 条记录")
                    else:
                        print("⚠️ 无数据")
                else:
                    print(f"❌ 请求失败: {response.status_code}")
            except Exception as e:
                print(f"❌ 异常: {str(e)}")
            
            # 避免请求过于频繁
            time.sleep(1)
        
        if all_data:
            df = pd.DataFrame(all_data)
            df["datetime"] = pd.to_datetime(df["time"], unit="ms")
            df = df.sort_values("datetime").reset_index(drop=True)
            
            print(f"\n📊 分页结果汇总:")
            print(f"总数据条数: {len(df)}")
            print(f"时间范围: {df['datetime'].min()} 到 {df['datetime'].max()}")
            
            return df
        else:
            print("❌ 分页测试失败，无数据")
            return pd.DataFrame()

def main():
    """主函数"""
    debugger = HyperliquidAPIDebugger()
    
    print("🚀 Hyperliquid API 调试工具")
    print("=" * 60)
    
    # 测试单个币种
    print("\n1️⃣ 测试单个币种 (BTC, 48小时)")
    btc_data = debugger.test_funding_history_api("BTC", 48)
    
    # 测试多个币种
    print("\n2️⃣ 测试多个币种")
    multi_results = debugger.test_different_coins(["BTC", "ETH"], 24)
    
    # 测试分页
    print("\n3️⃣ 测试分页功能")
    paginated_data = debugger.test_pagination("BTC", 168)
    
    print("\n🎉 调试完成!")
    
    # 保存结果
    if not btc_data.empty:
        btc_data.to_csv("btc_funding_debug.csv", index=False)
        print("💾 BTC 数据已保存到 btc_funding_debug.csv")
    
    if not paginated_data.empty:
        paginated_data.to_csv("btc_paginated_debug.csv", index=False)
        print("💾 分页数据已保存到 btc_paginated_debug.csv")

if __name__ == "__main__":
    main()
