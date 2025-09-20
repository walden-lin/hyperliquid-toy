# 📊 Crypto Trading Tools Collection

A collection of cryptocurrency trading analysis tools, focusing on funding rate analysis and event-driven backtesting.

## 🚀 Projects

### 1. 📈 Event-Driven Funding Rate Backtester
**Location**: `funding-backtester/`

A comprehensive tool for analyzing cryptocurrency funding rate anomalies around major market events using Hyperliquid data.

**Features**:
- Event-driven backtesting
- Z-score anomaly detection
- Multi-asset support (BTC, ETH, SOL, BNB)
- Interactive visualization with Plotly
- Strategy parameter optimization

**Quick Start**:
```bash
cd funding-backtester
pip install -r requirements.txt
streamlit run app.py
```

**Live Demo**: [Streamlit Cloud](https://hyperliquid-toy-hv6bmmdx4mjvgzcc3bcb9j.streamlit.app/)

### 2. 📊 Funding Rate Dashboard
**Location**: `funding-dashboard/`

A simple dashboard for comparing funding rates across different exchanges and cryptocurrencies.

**Features**:
- Multi-exchange funding rate comparison
- Historical data visualization
- Interactive charts

**Quick Start**:
```bash
cd funding-dashboard
pip install -r requirements.txt
streamlit run app.py
```

## 🏗️ Project Structure

```
Trading/
├── README.md                    # This file
├── funding-backtester/          # Main project - Event-driven backtester
│   ├── app.py                  # Main Streamlit application
│   ├── data.py                 # Data fetching module
│   ├── strategy.py             # Trading strategy and backtesting
│   ├── visualization.py        # Chart generation
│   ├── events.json             # Event configuration
│   ├── requirements.txt        # Dependencies
│   ├── README.md              # Detailed project documentation
│   └── run.sh                 # Launch script
└── funding-dashboard/          # Simple dashboard
    ├── app.py                 # Dashboard application
    ├── requirements.txt       # Dependencies
    ├── README.md             # Project documentation
    └── run.sh                # Launch script
```

## 🎯 Main Project: Event-Driven Funding Rate Backtester

The main project is the **Event-Driven Funding Rate Backtester** located in the `funding-backtester/` directory. This is the most comprehensive tool that includes:

### Core Features
- **Event Analysis**: Analyze funding rate patterns around major crypto events
- **Anomaly Detection**: Statistical analysis using Z-score methodology
- **Strategy Backtesting**: Test trading strategies based on funding rate signals
- **Interactive Visualization**: Rich charts with Plotly integration
- **Multi-page Interface**: Main app, tutorial, and theory pages

### Supported Events
- Technical upgrades (Ethereum Merge, Dencun Upgrade)
- Regulatory events (ETF approvals, policy changes)
- Market events (exchange collapses, stablecoin depegs)
- Network events (outages, forks)
- Halving events (Bitcoin halvings)

### Technology Stack
- **Frontend**: Streamlit
- **Visualization**: Plotly
- **Data Processing**: Pandas, NumPy
- **API Integration**: Hyperliquid API
- **Backend**: Python 3.12+

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- pip package manager

### Installation
1. Clone the repository:
```bash
git clone https://github.com/walden-lin/hyperliquid-toy.git
cd hyperliquid-toy/Trading
```

2. Choose your project:
```bash
# For the main backtester
cd funding-backtester
pip install -r requirements.txt
streamlit run app.py

# For the simple dashboard
cd funding-dashboard
pip install -r requirements.txt
streamlit run app.py
```

## 📊 Usage Examples

### Event-Driven Analysis
1. Select an event from the sidebar
2. Adjust strategy parameters (rolling window, Z-score threshold)
3. View funding rate charts and anomaly detection
4. Analyze backtest results and trade records
5. Export data for further analysis

### Strategy Development
- Customize detection parameters
- Test different time windows
- Compare multiple events
- Analyze performance metrics

## 🔧 Configuration

### Events Configuration
Edit `funding-backtester/events.json` to add new events:
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

## 📈 Data Sources

- **Hyperliquid API**: Real-time funding rate data
- **Historical Events**: Manually configured major event timestamps
- **Price Data**: For P&L calculation

## 🌐 Online Demo

**Main Project**: [Event-Driven Funding Rate Backtester](https://hyperliquid-toy-hv6bmmdx4mjvgzcc3bcb9j.streamlit.app/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](funding-backtester/LICENSE) file for details.

## 📞 Contact

- GitHub: [@walden-lin](https://github.com/walden-lin)
- Project Repository: [hyperliquid-toy](https://github.com/walden-lin/hyperliquid-toy)

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) - For building interactive web applications
- [Plotly](https://plotly.com/) - For data visualization
- [Hyperliquid](https://hyperliquid.xyz/) - For providing funding rate data
- [Pandas](https://pandas.pydata.org/) - For data processing and analysis

---

⭐ **Star this repository if you find it useful!**
