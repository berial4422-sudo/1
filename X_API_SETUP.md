# X API Bearer Token 配置指南

## ⚠️ 重要安全提示

**请勿将 Bearer Token 提交到代码仓库！**

Bearer Token 是敏感信息，应该：
- ✅ 放在 GitHub Secrets 中
- ✅ 放在环境变量中
- ✅ 放在 `.env` 文件中（并添加到 `.gitignore`）
- ❌ **不要**放在代码文件中
- ❌ **不要**提交到 Git 仓库

---

## 🔧 配置方法

### 方法 1: GitHub Actions（推荐）

1. **进入 GitHub Secrets 设置**：
   - 访问：https://github.com/maverikhe-cpu/TrendRadar/settings/secrets/actions
   - 或：`Settings` → `Secrets and variables` → `Actions`

2. **添加 Secret**：
   - 点击 **"New repository secret"**
   - **Name（名称）**：`X_API_BEARER_TOKEN`
   - **Secret（值）**：粘贴你的 Bearer Token
   - 点击 **"Add secret"**

3. **验证配置**：
   - 在 Secrets 列表中应该能看到 `X_API_BEARER_TOKEN`
   - 保存后无法查看值的内容（这是正常的安全机制）

### 方法 2: 本地环境变量

**macOS/Linux**：
```bash
# 临时设置（当前终端会话）
export X_API_BEARER_TOKEN="AAAAAAAAAAAAAAAAAAAAAFpI5gEAAAAAsZ7IQ3BfS7kxaGaBrDiH2zsx%2B3c%3DJui9LO6StFReiTFR8pt5BTQKQfmW55uJeXg9sYari64UBDZPeA"

# 永久设置（添加到 ~/.zshrc 或 ~/.bashrc）
echo 'export X_API_BEARER_TOKEN="AAAAAAAAAAAAAAAAAAAAAFpI5gEAAAAAsZ7IQ3BfS7kxaGaBrDiH2zsx%2B3c%3DJui9LO6StFReiTFR8pt5BTQKQfmW55uJeXg9sYari64UBDZPeA"' >> ~/.zshrc
source ~/.zshrc
```

**Windows**：
```cmd
# 临时设置
set X_API_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAAFpI5gEAAAAAsZ7IQ3BfS7kxaGaBrDiH2zsx%2B3c%3DJui9LO6StFReiTFR8pt5BTQKQfmW55uJeXg9sYari64UBDZPeA

# 永久设置（系统环境变量）
# 控制面板 → 系统 → 高级系统设置 → 环境变量 → 新建
```

### 方法 3: Docker 环境变量

在 `docker-compose.yml` 或运行命令中添加：

```yaml
environment:
  - X_API_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAAFpI5gEAAAAAsZ7IQ3BfS7kxaGaBrDiH2zsx%2B3c%3DJui9LO6StFReiTFR8pt5BTQKQfmW55uJeXg9sYari64UBDZPeA
```

或使用 `.env` 文件（推荐）：

```bash
# .env 文件
X_API_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAAFpI5gEAAAAAsZ7IQ3BfS7kxaGaBrDiH2zsx%2B3c%3DJui9LO6StFReiTFR8pt5BTQKQfmW55uJeXg9sYari64UBDZPeA
```

**重要**：确保 `.env` 文件在 `.gitignore` 中！

---

## 🧪 测试配置

### 本地测试

```bash
# 设置环境变量
export X_API_BEARER_TOKEN="AAAAAAAAAAAAAAAAAAAAAFpI5gEAAAAAsZ7IQ3BfS7kxaGaBrDiH2zsx%2B3c%3DJui9LO6StFReiTFR8pt5BTQKQfmW55uJeXg9sYari64UBDZPeA"

# 测试 X 数据获取器
python custom_sources/x_fetcher.py

# 或测试完整流程
python main.py
```

### 验证环境变量

```bash
# 检查环境变量是否设置
echo $X_API_BEARER_TOKEN

# 在 Python 中验证
python3 -c "import os; print('✅ Token 已设置' if os.getenv('X_API_BEARER_TOKEN') else '❌ Token 未设置')"
```

---

## 📝 GitHub Actions 配置

### 更新工作流文件（可选）

如果你想在 GitHub Actions 中使用 X API，需要确保环境变量被传递：

编辑 `.github/workflows/crawler.yml`，在 `Run crawler` 步骤中添加：

```yaml
- name: 🕷️ Run crawler
  env:
    # ... 其他环境变量
    X_API_BEARER_TOKEN: ${{ secrets.X_API_BEARER_TOKEN }}
  run: |
    python main.py
```

---

## ✅ 配置检查清单

- [ ] Bearer Token 已添加到 GitHub Secrets（如果使用 GitHub Actions）
- [ ] 环境变量已设置（如果本地运行）
- [ ] 测试 X 数据获取器成功
- [ ] 测试完整流程成功
- [ ] **确认 Token 没有提交到代码仓库**

---

## 🔒 安全建议

1. **定期轮换 Token**：
   - 如果 Token 泄露，立即在 X Developer Portal 中撤销
   - 生成新的 Token

2. **权限最小化**：
   - 只授予必要的 API 权限
   - 定期检查 API 使用情况

3. **监控使用**：
   - 在 X Developer Portal 中监控 API 调用
   - 发现异常立即处理

---

## 🆘 故障排查

### 问题 1: Token 未生效

**检查**：
```bash
# 验证环境变量
echo $X_API_BEARER_TOKEN

# 在 Python 中检查
python3 -c "import os; print(os.getenv('X_API_BEARER_TOKEN'))"
```

### 问题 2: API 返回 401 错误

**可能原因**：
- Token 已过期
- Token 格式错误
- Token 权限不足

**解决**：
- 检查 Token 是否正确
- 在 X Developer Portal 中验证 Token 状态

### 问题 3: API 返回 429 错误（频率限制）

**解决**：
- 减少请求频率
- 等待限制重置
- 考虑升级 API 计划

---

## 📚 相关资源

- [X API 文档](https://developer.twitter.com/en/docs)
- [X Developer Portal](https://developer.twitter.com/en/portal)
- [API 使用限制](https://developer.twitter.com/en/docs/rate-limits)

---

**配置完成后，X 平台会自动使用 API 获取数据！** 🚀


