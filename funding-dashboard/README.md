# 📊 Crypto Funding Rate Dashboard

A simple dashboard for comparing funding rates across different exchanges and cryptocurrencies.

## 🚀 Features

- **Multi-Exchange Comparison**: Compare funding rates from different exchanges
- **Historical Data**: View funding rate trends over time
- **Interactive Charts**: Plotly-based visualization
- **Multi-Asset Support**: BTC, ETH, SOL, BNB

## 🛠️ Installation & Usage

### Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

### Using the launch script
```bash
chmod +x run.sh
./run.sh
```

## 📊 Supported Exchanges

- Binance
- Bybit
- Hyperliquid
- CoinGecko (fallback)

## 🏗️ Project Structure

```
funding-dashboard/
├── app.py              # Main Streamlit application
├── requirements.txt    # Dependencies
├── run.sh             # Launch script
└── README.md          # This file
```

## 🔧 Configuration

The dashboard automatically fetches data from multiple sources:
- Primary: Binance API
- Fallback: CoinGecko, CryptoCompare, CoinMarketCap
- Mock data: If all APIs fail

## 📈 Usage

1. **Select Coins**: Choose cryptocurrencies to compare
2. **Time Range**: Adjust the time period
3. **View Charts**: Interactive funding rate comparison
4. **Export Data**: Download results

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Visualization**: Plotly
- **Data Sources**: Multiple exchange APIs
- **Backend**: Python 3.12+

## 📄 License

MIT License

## 🔗 Links

- **GitHub**: [walden-lin/hyperliquid-toy](https://github.com/walden-lin/hyperliquid-toy)
- **Main Project**: [Event-Driven Funding Rate Backtester](../funding-backtester/)

---

⭐ **Star this repo if you find it useful!**