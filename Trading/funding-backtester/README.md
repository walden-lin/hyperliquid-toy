# 📊 事件驱动资金费率回测工具

一个基于 Hyperliquid 数据的事件驱动资金费率回测和可视化系统，用于分析重大事件对加密货币资金费率的影响。

## 🚀 功能特性

- **事件驱动回测**: 基于历史重大事件进行资金费率策略回测
- **异常检测**: 使用 Z-score 算法检测资金费率异常
- **多币种支持**: 支持 BTC、ETH、SOL、BNB 等主流币种
- **交互式可视化**: 使用 Plotly 提供丰富的图表展示
- **策略参数调优**: 可调整滚动窗口、阈值等策略参数
- **交易记录导出**: 支持 CSV 格式导出交易记录

## 🏗️ 项目结构

```
funding-backtester/
├── app.py                # Streamlit 主应用
├── data.py               # 数据获取模块
├── strategy.py           # 策略和回测逻辑
├── visualization.py      # 可视化模块
├── events.json           # 事件配置文件
├── requirements.txt      # Python 依赖
├── run.sh               # 启动脚本
└── README.md            # 项目说明
```

## 🛠️ 安装和运行

### 1. 克隆项目
```bash
git clone https://github.com/walden-lin/hyperliquid-toy.git
cd hyperliquid-toy/Trading/funding-backtester
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 运行应用
```bash
streamlit run app.py
```

或者使用启动脚本：
```bash
chmod +x run.sh
./run.sh
```

## 📈 使用说明

### 主应用页面
1. **选择事件**: 在侧边栏选择要分析的历史事件
2. **调整参数**: 设置滚动窗口大小和 Z-score 阈值
3. **查看结果**: 分析资金费率走势和异常信号
4. **导出数据**: 下载交易记录和统计结果

### 教程页面
- 详细的使用教程和操作指南
- 策略原理和参数说明
- 常见问题解答

### 数学理论页面
- Z-score 异常检测算法详解
- 资金费率计算原理
- 回测策略数学基础
- 风险指标计算方法

## 📊 核心算法

### 异常检测算法
```python
# Z-score 计算
z_score = (funding_rate - rolling_mean) / rolling_std

# 信号生成
if z_score > threshold:
    signal = "SHORT"
elif z_score < -threshold:
    signal = "LONG"
else:
    signal = "HOLD"
```

### 回测策略
1. **开仓条件**: 检测到异常信号时开仓
2. **持仓管理**: 持有至信号反转或资金费率结算
3. **盈亏计算**: 资金费率收入 ± 价格变动
4. **风险控制**: 设置止损和最大持仓时间

## 📅 支持的事件类型

- **技术升级**: 以太坊合并、Dencun 升级等
- **监管事件**: ETF 批准、监管政策变化
- **市场事件**: 交易所破产、稳定币脱锚
- **网络事件**: 网络中断、分叉等
- **减半事件**: 比特币减半等周期性事件

## 🔧 配置说明

### events.json 格式
```json
[
  {
    "name": "事件名称",
    "coin": "BTC",
    "timestamp": "2024-01-01 12:00:00",
    "description": "事件描述",
    "category": "upgrade",
    "impact": "high"
  }
]
```

### 策略参数
- **滚动窗口**: 计算均值和标准差的时间窗口
- **Z-score 阈值**: 异常检测的敏感度
- **持仓时间**: 最大持仓时间限制
- **止损比例**: 风险控制参数

## 📊 数据来源

- **Hyperliquid API**: 实时资金费率数据
- **历史事件**: 手动配置的重大事件时间点
- **价格数据**: 用于计算盈亏的价格信息

## 🚀 在线演示

访问 [Streamlit Cloud 部署版本](https://hyperliquid-toy-hv6bmmdx4mjvgzcc3bcb9j.streamlit.app/)

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📝 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

- GitHub: [@walden-lin](https://github.com/walden-lin)
- 项目链接: [https://github.com/walden-lin/hyperliquid-toy](https://github.com/walden-lin/hyperliquid-toy)

## 🙏 致谢

- [Streamlit](https://streamlit.io/) - 用于构建交互式 Web 应用
- [Plotly](https://plotly.com/) - 用于数据可视化
- [Hyperliquid](https://hyperliquid.xyz/) - 提供资金费率数据
- [Pandas](https://pandas.pydata.org/) - 数据处理和分析

## 📈 未来计划

- [ ] 支持更多交易所数据源
- [ ] 添加机器学习异常检测
- [ ] 实现实时数据更新
- [ ] 增加更多技术指标
- [ ] 支持自定义策略开发
- [ ] 添加回测性能优化
- [ ] 实现多币种组合策略
- [ ] 添加风险管理模块

---

⭐ 如果这个项目对你有帮助，请给它一个星标！