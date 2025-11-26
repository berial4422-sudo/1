# X API Bearer Token 配置完成指南

## ✅ 当前状态

- ✅ X 数据获取器已创建
- ✅ main.py 已集成 X 平台支持
- ✅ GitHub Actions 工作流已更新
- ✅ 配置文档已创建

## 🔒 重要：配置 Bearer Token

### ⚠️ 安全警告

**你的 Bearer Token**：
```
AAAAAAAAAAAAAAAAAAAAAFpI5gEAAAAAsZ7IQ3BfS7kxaGaBrDiH2zsx%2B3c%3DJui9LO6StFReiTFR8pt5BTQKQfmW55uJeXg9sYari64UBDZPeA
```

**请勿将此 Token 提交到代码仓库！**

---

## 📋 配置步骤

### 步骤 1: 添加到 GitHub Secrets（必需）

1. **访问 GitHub Secrets 设置**：
   - https://github.com/maverikhe-cpu/TrendRadar/settings/secrets/actions
   - 或：`Settings` → `Secrets and variables` → `Actions`

2. **添加 Secret**：
   - 点击 **"New repository secret"**
   - **Name（名称）**：`X_API_BEARER_TOKEN`
   - **Secret（值）**：粘贴你的 Bearer Token
     ```
     AAAAAAAAAAAAAAAAAAAAAFpI5gEAAAAAsZ7IQ3BfS7kxaGaBrDiH2zsx%2B3c%3DJui9LO6StFReiTFR8pt5BTQKQfmW55uJeXg9sYari64UBDZPeA
     ```
   - 点击 **"Add secret"**

3. **验证**：
   - 在 Secrets 列表中应该能看到 `X_API_BEARER_TOKEN`
   - 保存后无法查看值的内容（这是正常的安全机制）

### 步骤 2: 本地测试（可选）

如果你想在本地测试：

```bash
# 临时设置（当前终端会话）
export X_API_BEARER_TOKEN="AAAAAAAAAAAAAAAAAAAAAFpI5gEAAAAAsZ7IQ3BfS7kxaGaBrDiH2zsx%2B3c%3DJui9LO6StFReiTFR8pt5BTQKQfmW55uJeXg9sYari64UBDZPeA"

# 测试运行
python main.py
```

**注意**：本地测试后，记得取消设置环境变量，避免泄露。

---

## 🔄 自动降级机制

系统已实现智能降级：

1. **优先使用 X API**（如果配置了 Bearer Token）
2. **自动降级到 Nitter**（如果 API 失败或未配置）

**工作流程**：
```python
if os.getenv("X_API_BEARER_TOKEN"):
    # 尝试使用 X API
    try:
        data = fetch_via_api()
    except:
        # API 失败，自动降级到 Nitter
        data = fetch_via_nitter()
else:
    # 直接使用 Nitter（无需 API）
    data = fetch_via_nitter()
```

---

## ⚠️ 关于 API 频率限制

测试时遇到 429 错误（Too Many Requests）是正常的：

1. **原因**：X API 有严格的请求频率限制
2. **影响**：短时间内多次请求会触发限制
3. **解决**：
   - 等待限制重置（通常 15 分钟）
   - 系统会自动降级到 Nitter
   - 或减少请求频率

**建议**：
- 在 GitHub Actions 中运行时，频率较低，通常不会触发限制
- 如果频繁触发限制，考虑使用 Nitter 作为主要数据源

---

## 🧪 测试配置

### 方法 1: 测试 X 数据获取器

```bash
# 设置环境变量
export X_API_BEARER_TOKEN="your_token"

# 测试
python custom_sources/x_fetcher.py
```

### 方法 2: 测试完整流程

```bash
# 设置环境变量
export X_API_BEARER_TOKEN="your_token"

# 运行主程序
python main.py
```

### 方法 3: GitHub Actions 测试

1. 确保已添加 `X_API_BEARER_TOKEN` 到 GitHub Secrets
2. 在 GitHub Actions 中手动触发工作流
3. 查看执行日志，确认 X 平台数据获取成功

---

## 📝 配置检查清单

- [ ] Bearer Token 已添加到 GitHub Secrets
- [ ] Secret 名称正确：`X_API_BEARER_TOKEN`
- [ ] 已更新 GitHub Actions 工作流（已自动完成）
- [ ] 已测试本地运行（可选）
- [ ] **确认 Token 没有提交到代码仓库**

---

## 🔍 验证配置

### 检查 GitHub Secrets

访问：https://github.com/maverikhe-cpu/TrendRadar/settings/secrets/actions

确认能看到：
- ✅ `X_API_BEARER_TOKEN`（如果已添加）

### 检查工作流配置

查看 `.github/workflows/crawler.yml`，确认包含：

```yaml
X_API_BEARER_TOKEN: ${{ secrets.X_API_BEARER_TOKEN }}
```

---

## 🎯 下一步

1. ✅ **立即添加 Bearer Token 到 GitHub Secrets**（重要！）
2. ⏳ 提交代码更改到 GitHub
3. ⏳ 在 GitHub Actions 中测试运行
4. ⏳ 验证 X 平台数据获取成功

---

## 📚 相关文档

- [X API 配置指南](X_API_SETUP.md)
- [故障排查指南](X_API_TROUBLESHOOTING.md)
- [快速开始指南](X_PLATFORM_QUICKSTART.md)

---

## 🆘 需要帮助？

如果遇到问题：

1. **API 频率限制**：等待 15 分钟后重试，或使用 Nitter
2. **401 错误**：检查 Bearer Token 是否正确
3. **获取不到数据**：查看 [故障排查指南](X_API_TROUBLESHOOTING.md)

---

**配置完成后，X 平台会自动使用 API 获取数据！** 🚀

