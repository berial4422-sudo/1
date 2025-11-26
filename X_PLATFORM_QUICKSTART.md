# X (Twitter) 平台快速开始

## ✅ 已完成

- ✅ 创建了 X 数据获取器（`custom_sources/x_fetcher.py`）
- ✅ 修改了 `main.py` 集成 X 平台支持
- ✅ 更新了 `requirements.txt` 添加依赖
- ✅ 更新了 `config/config.yaml` 添加 X 平台配置

## 🚀 快速使用

### 方式 1: 使用 Nitter 镜像（推荐，无需 API Key）

**优点**：
- ✅ 无需申请 API
- ✅ 免费使用
- ✅ 配置简单

**步骤**：

1. **安装依赖**：
   ```bash
   pip install beautifulsoup4
   ```

2. **测试运行**：
   ```bash
   python main.py
   ```

3. **完成！** X 平台会自动使用 Nitter 镜像获取数据

### 方式 2: 使用 X API（更稳定，需要 API Key）

**优点**：
- ✅ 官方 API，稳定可靠
- ✅ 数据准确

**步骤**：

1. **申请 X API 访问**：
   - 访问：https://developer.twitter.com/
   - 创建应用，获取 Bearer Token

2. **配置环境变量**：

   **GitHub Actions**：
   - 在 GitHub Secrets 中添加：
     - Name: `X_API_BEARER_TOKEN`
     - Secret: 你的 Bearer Token

   **本地/Docker**：
   ```bash
   export X_API_BEARER_TOKEN="your_bearer_token_here"
   ```

3. **运行**：
   ```bash
   python main.py
   ```

系统会自动检测到 `X_API_BEARER_TOKEN` 环境变量，优先使用 X API。

---

## 📋 配置说明

### 平台配置

已在 `config/config.yaml` 中添加：

```yaml
platforms:
  - id: "x"
    name: "X (Twitter)"
```

### 关键词配置

X 趋势可能是英文的，建议在 `config/frequency_words.txt` 中添加英文关键词：

```txt
AI
ChatGPT
OpenAI

Elon Musk
Tesla
SpaceX

Bitcoin
Crypto
```

---

## 🧪 测试

### 测试 X 数据获取器

```bash
# 直接运行测试
python custom_sources/x_fetcher.py
```

### 测试完整流程

```bash
# 运行主程序
python main.py

# 查看输出
# - 检查是否成功获取 X 平台数据
# - 查看 output 目录下的文件
```

---

## ⚠️ 注意事项

### 1. Nitter 镜像可能不稳定

- 如果某个 Nitter 实例不可用，会自动尝试其他实例
- 如果所有实例都不可用，可以：
  - 编辑 `custom_sources/x_fetcher.py`
  - 修改 `nitter_instances` 列表，添加其他可用的实例

### 2. X API 限制

- 有请求频率限制
- 免费层每月有限额
- 建议合理控制请求频率

### 3. 语言问题

- X 趋势可能是多语言的
- 关键词匹配需要考虑语言
- 建议添加英文关键词

---

## 🔧 故障排查

### 问题 1: ImportError: No module named 'bs4'

**解决**：
```bash
pip install beautifulsoup4
```

### 问题 2: Nitter 实例都不可用

**解决**：
1. 编辑 `custom_sources/x_fetcher.py`
2. 查找可用的 Nitter 实例：https://github.com/zedeus/nitter/wiki/Instances
3. 更新 `nitter_instances` 列表

### 问题 3: X API 返回 401 错误

**解决**：
- 检查 Bearer Token 是否正确
- 确认 API 权限是否足够

---

## 📚 相关文档

- [完整集成指南](INTEGRATE_X_PLATFORM.md)
- [添加平台指南](ADD_PLATFORM_GUIDE.md)
- [X 平台配置](ADD_X_PLATFORM.md)

---

## 🎯 下一步

1. ✅ 代码已集成
2. ⏳ 安装依赖：`pip install beautifulsoup4`
3. ⏳ 测试运行：`python main.py`
4. ⏳ 提交更改到 GitHub

---

**现在可以开始使用 X 平台了！** 🚀


