# 🚀 Streamlit Cloud 部署指南

## 问题诊断

你的应用 `https://hyperliquid-toy-hv6bmmdx4mjvgzcc3bcb9j.streamlit.app/` 无法访问，可能的原因：

### 1. **文件路径问题**
- 确保 `events.json` 文件在根目录
- 检查所有导入路径是否正确

### 2. **依赖问题**
- 确保 `requirements.txt` 包含所有必要的包
- 检查版本兼容性

### 3. **代码错误**
- 检查是否有语法错误
- 确保所有模块都能正确导入

## 解决方案

### 方案 1: 使用简化版本 (推荐)

1. **重命名文件**：
   ```bash
   mv app.py app_original.py
   mv app_cloud.py app.py
   ```

2. **更新 requirements.txt**：
   ```bash
   cp requirements_cloud.txt requirements.txt
   ```

3. **提交到 GitHub**：
   ```bash
   git add .
   git commit -m "Fix Streamlit Cloud deployment"
   git push
   ```

### 方案 2: 修复原始版本

1. **检查导入问题**：
   - 确保 `data.py`, `strategy.py`, `visualization.py` 文件存在
   - 检查所有函数是否正确导入

2. **添加错误处理**：
   - 在 `app.py` 中添加 try-catch 块
   - 处理文件不存在的情况

3. **简化依赖**：
   - 移除不必要的导入
   - 使用内置模块替代第三方包

## 部署步骤

### 1. 准备文件
确保以下文件在根目录：
- `app.py` (主应用文件)
- `events.json` (事件配置)
- `requirements.txt` (依赖列表)
- `.streamlit/config.toml` (可选配置)

### 2. 推送到 GitHub
```bash
git add .
git commit -m "Deploy to Streamlit Cloud"
git push origin main
```

### 3. 在 Streamlit Cloud 部署
1. 访问 [share.streamlit.io](https://share.streamlit.io)
2. 连接 GitHub 仓库
3. 选择分支 (通常是 `main`)
4. 设置主文件路径为 `app.py`
5. 点击 "Deploy"

### 4. 监控部署
- 查看部署日志
- 检查错误信息
- 测试应用功能

## 常见问题

### Q: 应用显示 "Something went wrong"
**A**: 检查部署日志，通常是导入错误或文件路径问题

### Q: 无法加载 events.json
**A**: 确保文件在根目录，并且格式正确

### Q: 依赖安装失败
**A**: 检查 requirements.txt 中的包名和版本

### Q: 应用加载缓慢
**A**: 优化代码，减少不必要的计算

## 测试本地运行

在部署前，先测试本地运行：

```bash
streamlit run app.py
```

确保应用能正常启动和运行。

## 联系支持

如果问题仍然存在：
1. 检查 Streamlit Cloud 状态页面
2. 查看 GitHub Issues
3. 在 Streamlit 社区论坛寻求帮助
