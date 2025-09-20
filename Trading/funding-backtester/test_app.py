"""
测试版本 - 确保 events.json 能正确加载
"""

import streamlit as st
import json
import os

st.set_page_config(
    page_title="测试应用",
    page_icon="🧪",
    layout="wide"
)

def load_events():
    """加载事件配置"""
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    events_file = os.path.join(current_dir, 'events.json')
    
    st.write(f"当前目录: {current_dir}")
    st.write(f"events.json 路径: {events_file}")
    st.write(f"文件是否存在: {os.path.exists(events_file)}")
    
    try:
        with open(events_file, 'r', encoding='utf-8') as f:
            events = json.load(f)
        st.success(f"✅ 成功加载 {len(events)} 个事件")
        return events
    except FileNotFoundError:
        st.error(f"❌ 找不到 events.json 文件，路径: {events_file}")
        return []
    except json.JSONDecodeError as e:
        st.error(f"❌ events.json 文件格式错误: {e}")
        return []

def main():
    st.title("🧪 测试应用 - events.json 加载")
    
    st.subheader("文件路径测试")
    events = load_events()
    
    if events:
        st.subheader("事件列表")
        for i, event in enumerate(events[:5]):  # 只显示前5个
            st.write(f"{i+1}. {event['name']} - {event['coin']}")
        
        if len(events) > 5:
            st.write(f"... 还有 {len(events) - 5} 个事件")
    
    st.subheader("文件内容预览")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    events_file = os.path.join(current_dir, 'events.json')
    
    if os.path.exists(events_file):
        with open(events_file, 'r', encoding='utf-8') as f:
            content = f.read()
        st.code(content[:500] + "..." if len(content) > 500 else content)

if __name__ == "__main__":
    main()
