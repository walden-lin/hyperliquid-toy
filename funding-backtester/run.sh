#!/bin/bash

# 事件驱动资金费率回测工具启动脚本

echo "🚀 启动事件驱动资金费率回测工具..."
echo "📁 项目目录: $(pwd)"
echo "🌐 应用将在浏览器中自动打开: http://localhost:8501"
echo "⏹️  按 Ctrl+C 停止应用"
echo ""

# 检查依赖
echo "📦 检查依赖..."
if ! command -v python &> /dev/null; then
    echo "❌ Python 未安装，请先安装 Python 3.8+"
    exit 1
fi

# 检查 requirements.txt
if [ ! -f "requirements.txt" ]; then
    echo "❌ 找不到 requirements.txt 文件"
    exit 1
fi

# 安装依赖（如果需要）
echo "📦 安装依赖包..."
pip install -r requirements.txt

# 检查必要文件
echo "🔍 检查必要文件..."
required_files=("app.py" "data.py" "strategy.py" "visualization.py" "events.json")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ 找不到必要文件: $file"
        exit 1
    fi
done

echo "✅ 所有文件检查完成"
echo ""

# 启动 Streamlit 应用
echo "🚀 启动应用..."
streamlit run app.py --server.port 8501 --server.address localhost
