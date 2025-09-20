"""
Streamlit Cloud 部署入口文件
重定向到主应用文件
"""

import sys
import os

# 添加当前目录到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入主应用
from app import *

# 如果直接运行此文件，启动 Streamlit
if __name__ == "__main__":
    import streamlit as st
    st.set_page_config(
        page_title="📊 事件驱动资金费率回测工具",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
