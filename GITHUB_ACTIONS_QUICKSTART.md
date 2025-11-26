# GitHub Actions 快速开始指南

## 🚀 5 分钟快速部署

### 步骤 1: Fork 项目 (30秒)

1. 访问：https://github.com/sansan0/TrendRadar
2. 点击右上角 **Fork** 按钮
3. 等待 Fork 完成

### 步骤 2: 配置通知渠道 (2分钟)

进入你 Fork 的仓库：
- `Settings` → `Secrets and variables` → `Actions` → `New repository secret`

**推荐：企业微信（最简单）**

1. 打开企业微信 App → 进入群聊 → 右上角"…" → "消息推送" → "添加"
2. 复制 Webhook 地址
3. 在 GitHub 添加 Secret：
   - **Name**: `WEWORK_WEBHOOK_URL`
   - **Secret**: 粘贴 Webhook 地址

### 步骤 3: 测试运行 (1分钟)

1. 进入你项目的 **Actions** 标签页
2. 找到 **"Hot News Crawler"**
3. 点击 **"Run workflow"** → **"Run workflow"**
4. 等待 1-2 分钟，检查是否收到推送

### 步骤 4: 配置关键词（可选，1分钟）

编辑 `config/frequency_words.txt`，添加你关心的关键词：

```txt
AI
ChatGPT
人工智能

比亚迪
特斯拉
```

### 步骤 5: 完成！🎉

系统会按照设定的时间自动运行（默认每小时一次）。

---

## 📋 常用配置

### 修改执行频率

编辑 `.github/workflows/crawler.yml`：

```yaml
schedule:
  - cron: "0 * * * *"  # 每小时（默认）
  # - cron: "*/30 * * * *"  # 每30分钟
```

### 修改推送模式

编辑 `config/config.yaml`：

```yaml
report:
  mode: "daily"  # daily | incremental | current
```

### 启用 GitHub Pages

1. `Settings` → `Pages`
2. Source: `main` 分支
3. 访问：`https://你的用户名.github.io/TrendRadar/`

---

## ❓ 遇到问题？

1. **没有收到推送**：检查是否配置了 Secret
2. **工作流失败**：查看 Actions 日志
3. **配置文件错误**：确保 `config/config.yaml` 和 `config/frequency_words.txt` 存在

详细帮助：查看 [GITHUB_ACTIONS_GUIDE.md](GITHUB_ACTIONS_GUIDE.md)

---

**就是这么简单！** 🎉

