API 请求失败: 422 Client Error: Unprocessable Entity for url: https://api.hyperliquid.xyz/info

无法获取 ETH 资金费率数据，使用模拟数据


#!/bin/bash

# Crypto Funding Rate Dashboard 启动脚本

echo "🚀 启动 Crypto Funding Rate Dashboard..."
echo "📁 项目目录: $(pwd)"
echo "🌐 应用将在浏览器中自动打开: http://localhost:8501"
echo "⏹️  按 Ctrl+C 停止应用"
echo ""

# 启动 Streamlit 应用
streamlit run app.py --server.port 8501 --server.address localhost
