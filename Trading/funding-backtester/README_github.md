# 📊 Event-Driven Funding Rate Backtester

A comprehensive tool for analyzing cryptocurrency funding rate anomalies around major market events using Hyperliquid data.

## 🎯 What It Does

This tool helps you:
- **Analyze funding rate patterns** around major crypto events
- **Detect anomalies** using statistical methods (Z-score)
- **Backtest trading strategies** based on funding rate signals
- **Visualize results** with interactive charts

## 🚀 Quick Start

### Local Development
```bash
# Clone the repository
git clone https://github.com/walden-lin/hyperliquid-toy.git
cd hyperliquid-toy/Trading/funding-backtester

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Online Demo
🌐 **[Try it live on Streamlit Cloud](https://hyperliquid-toy-hv6bmmdx4mjvgzcc3bcb9j.streamlit.app/)**

## 📊 Features

- **Event-Driven Analysis**: Analyze funding rates around major events
- **Anomaly Detection**: Z-score based statistical analysis
- **Multi-Asset Support**: BTC, ETH, SOL, BNB
- **Interactive Visualization**: Plotly charts with zoom/pan
- **Strategy Backtesting**: Test funding rate trading strategies
- **Export Results**: Download data and charts

## 🏗️ Project Structure

```
funding-backtester/
├── app.py              # Main Streamlit application
├── data.py             # Data fetching from Hyperliquid API
├── strategy.py         # Trading strategy and backtesting
├── visualization.py    # Chart generation
├── events.json         # Event configuration
└── requirements.txt    # Dependencies
```

## 📈 How It Works

1. **Event Selection**: Choose from pre-configured major events
2. **Data Fetching**: Get funding rate data from Hyperliquid API
3. **Anomaly Detection**: Calculate Z-scores and identify signals
4. **Strategy Backtesting**: Simulate trades based on signals
5. **Visualization**: Display results with interactive charts

## 🔧 Configuration

### Events Configuration
Edit `events.json` to add new events:
```json
{
  "name": "Event Name",
  "coin": "BTC",
  "timestamp": "2024-01-01 12:00:00",
  "description": "Event description",
  "category": "upgrade",
  "impact": "high"
}
```

### Strategy Parameters
- **Rolling Window**: Time window for mean/std calculation
- **Z-score Threshold**: Sensitivity for anomaly detection
- **Position Management**: Entry/exit rules

## 📊 Supported Events

- **Technical Upgrades**: Ethereum Merge, Dencun Upgrade
- **Regulatory Events**: ETF Approvals, Policy Changes
- **Market Events**: Exchange Collapses, Stablecoin Depegs
- **Network Events**: Outages, Forks
- **Halving Events**: Bitcoin Halvings

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Visualization**: Plotly
- **Data Processing**: Pandas, NumPy
- **API Integration**: Requests
- **Data Source**: Hyperliquid API

## 📝 Usage Examples

### Basic Analysis
1. Select an event from the sidebar
2. Adjust strategy parameters
3. View funding rate charts and anomalies
4. Analyze backtest results

### Advanced Features
- Export trade records
- Customize visualization
- Adjust detection sensitivity
- Compare multiple events

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

## 🔗 Links

- **GitHub**: [walden-lin/hyperliquid-toy](https://github.com/walden-lin/hyperliquid-toy)
- **Live Demo**: [Streamlit Cloud](https://hyperliquid-toy-hv6bmmdx4mjvgzcc3bcb9j.streamlit.app/)
- **Documentation**: See README.md for detailed usage

---

⭐ **Star this repo if you find it useful!**
