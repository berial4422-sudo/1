# GitHub Actions 部署完整指南

## 📋 目录

- [快速开始](#快速开始)
- [详细配置步骤](#详细配置步骤)
- [常见问题](#常见问题)
- [优化建议](#优化建议)

---

## 🚀 快速开始

### 1. Fork 项目

访问 [TrendRadar 项目](https://github.com/sansan0/TrendRadar)，点击右上角的 **Fork** 按钮。

### 2. 配置 GitHub Secrets

进入你 Fork 的仓库：
- `Settings` → `Secrets and variables` → `Actions` → `New repository secret`

添加你需要的通知渠道配置（至少配置一个）：

| Secret 名称 | 说明 | 必需 |
|------------|------|------|
| `FEISHU_WEBHOOK_URL` | 飞书机器人 Webhook | 否 |
| `WEWORK_WEBHOOK_URL` | 企业微信机器人 Webhook | 否 |
| `DINGTALK_WEBHOOK_URL` | 钉钉机器人 Webhook | 否 |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token | 否 |
| `TELEGRAM_CHAT_ID` | Telegram Chat ID | 否 |
| `EMAIL_FROM` | 发件人邮箱 | 否 |
| `EMAIL_PASSWORD` | 邮箱密码或授权码 | 否 |
| `EMAIL_TO` | 收件人邮箱 | 否 |
| `NTFY_TOPIC` | ntfy 主题名称 | 否 |

**⚠️ 重要提示**：
- 至少需要配置一个通知渠道，否则无法接收推送
- Secret 名称必须**严格一致**，不能自己修改
- 保存后无法查看值的内容，这是正常的安全机制

### 3. 测试运行

1. 进入你项目的 **Actions** 标签页
2. 找到 **"Hot News Crawler"** 工作流
3. 点击右侧的 **"Run workflow"** 按钮
4. 等待 1-2 分钟，检查是否收到推送

### 4. 配置完成！

如果测试成功，系统会按照设定的时间自动运行。

---

## ⚙️ 详细配置步骤

### 配置通知渠道

#### 企业微信（推荐，配置最简单）

1. **获取 Webhook URL**：
   - 打开企业微信 App → 进入目标群聊
   - 点击右上角"…" → "消息推送" → "添加"
   - 复制 Webhook 地址

2. **配置到 GitHub**：
   - Name: `WEWORK_WEBHOOK_URL`
   - Secret: 粘贴刚才复制的 Webhook 地址

#### 飞书

1. **创建机器人**：
   - 访问 https://botbuilder.feishu.cn/home/my-command
   - 创建 Webhook 触发器
   - 复制 Webhook 地址

2. **配置到 GitHub**：
   - Name: `FEISHU_WEBHOOK_URL`
   - Secret: 粘贴 Webhook 地址

#### Telegram

1. **创建 Bot**：
   - 在 Telegram 搜索 `@BotFather`
   - 发送 `/newbot` 创建机器人
   - 获取 Bot Token

2. **获取 Chat ID**：
   - 向你的机器人发送一条消息
   - 访问：`https://api.telegram.org/bot<你的Token>/getUpdates`
   - 找到 `"chat":{"id":数字}` 中的数字

3. **配置到 GitHub**：
   - Name: `TELEGRAM_BOT_TOKEN`，Secret: Bot Token
   - Name: `TELEGRAM_CHAT_ID`，Secret: Chat ID

#### 邮件

1. **获取邮箱授权码**：
   - QQ邮箱：设置 → 账户 → 开启 POP3/SMTP → 生成授权码
   - Gmail：开启两步验证 → 生成应用专用密码
   - 163邮箱：设置 → POP3/SMTP/IMAP → 开启服务 → 设置授权码

2. **配置到 GitHub**：
   - Name: `EMAIL_FROM`，Secret: 发件人邮箱
   - Name: `EMAIL_PASSWORD`，Secret: 授权码（不是密码）
   - Name: `EMAIL_TO`，Secret: 收件人邮箱

### 调整执行频率

编辑 `.github/workflows/crawler.yml` 文件，修改 `cron` 表达式：

```yaml
schedule:
  - cron: "0 * * * *"  # 每小时整点运行
```

**常用配置**：

| Cron 表达式 | 说明 |
|------------|------|
| `0 * * * *` | 每小时整点运行（默认） |
| `*/30 * * * *` | 每 30 分钟运行一次 |
| `0 */2 * * *` | 每 2 小时运行一次 |
| `0 8-22 * * *` | 每天 8 点到 22 点，每小时运行 |
| `*/30 0-14 * * *` | UTC 时间 0-14 点，每 30 分钟运行（北京时间 8-22 点） |

**⚠️ 注意事项**：
- GitHub Actions 的定时任务可能有 ±20 分钟的偏差
- 不建议设置过于频繁（如每分钟），可能被判定为滥用
- Cron 表达式使用 UTC 时间，需要换算为北京时间（UTC+8）

### 配置关键词

编辑 `config/frequency_words.txt` 文件，添加你关心的关键词：

```txt
AI
ChatGPT
人工智能

比亚迪
特斯拉
新能源汽车

A股
股市
上证指数
```

**语法说明**：
- **普通词**：直接写关键词
- **必须词**：使用 `+关键词`（必须同时包含）
- **过滤词**：使用 `!关键词`（排除包含该词的新闻）
- **词组**：用空行分隔不同的词组

---

## ❓ 常见问题

### Q1: 工作流没有自动运行？

**可能原因**：
1. Fork 的仓库默认不启用 Actions
2. 定时任务有延迟（±20 分钟）

**解决方法**：
1. 进入 `Settings` → `Actions` → `General`
2. 确保 "Allow all actions and reusable workflows" 已启用
3. 手动触发一次测试：`Actions` → `Hot News Crawler` → `Run workflow`

### Q2: 收到 "配置文件不存在" 错误？

**解决方法**：
1. 确保 `config/config.yaml` 和 `config/frequency_words.txt` 存在
2. 如果文件不存在，从原仓库复制：
   ```bash
   # 在本地克隆你的 fork
   git clone https://github.com/你的用户名/TrendRadar.git
   cd TrendRadar
   # 确保配置文件存在
   ls config/
   ```

### Q3: 没有收到推送通知？

**检查清单**：
1. ✅ 是否配置了至少一个通知渠道的 Secret？
2. ✅ Secret 名称是否正确（严格一致）？
3. ✅ Webhook URL 或 Token 是否正确？
4. ✅ 工作流是否成功执行（查看 Actions 日志）？
5. ✅ 是否有匹配关键词的新闻（检查 `frequency_words.txt`）？

### Q4: 工作流执行失败？

**查看日志**：
1. 进入 `Actions` 标签页
2. 点击失败的工作流运行
3. 查看具体的错误信息

**常见错误**：
- **依赖安装失败**：检查 `requirements.txt` 是否正确
- **网络请求超时**：可能是数据源问题，稍后重试
- **配置文件格式错误**：检查 YAML 格式是否正确

### Q5: 如何修改推送模式？

编辑 `config/config.yaml` 文件：

```yaml
report:
  mode: "daily"  # 可选: "daily" | "incremental" | "current"
```

- `daily`：当日汇总模式（按时推送所有匹配新闻）
- `incremental`：增量监控模式（只推送新增内容）
- `current`：当前榜单模式（推送当前榜单匹配新闻）

### Q6: 如何查看生成的报告？

1. **GitHub Pages**（推荐）：
   - `Settings` → `Pages`
   - 启用 GitHub Pages
   - 访问：`https://你的用户名.github.io/TrendRadar/`

2. **仓库文件**：
   - 查看 `output` 目录下的 HTML 和 TXT 文件

---

## 🎯 优化建议

### 1. 启用 GitHub Pages

自动生成网页报告，方便查看：

1. `Settings` → `Pages`
2. Source 选择 `main` 分支
3. 访问：`https://你的用户名.github.io/TrendRadar/`

### 2. 使用增量模式减少推送

如果不想看到重复新闻，使用增量模式：

```yaml
report:
  mode: "incremental"
```

### 3. 合理设置执行频率

- **普通用户**：每小时或每 2 小时运行一次
- **高频监控**：每 30 分钟运行一次（注意不要过于频繁）

### 4. 优化关键词配置

- 从宽泛到精确：先测试宽泛关键词，再逐步精确
- 使用词组功能：用空行分隔不同主题
- 使用过滤词：排除不相关的内容

### 5. 监控工作流状态

- 关注 GitHub 通知，及时了解工作流执行情况
- 定期检查 Actions 日志，确保正常运行

---

## 📚 相关资源

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [Cron 表达式生成器](https://crontab.guru/)
- [项目 README](README.md)
- [问题反馈](https://github.com/sansan0/TrendRadar/issues)

---

## 🆘 获取帮助

如果遇到问题：

1. **查看日志**：在 Actions 中查看详细的执行日志
2. **搜索 Issues**：在项目 Issues 中搜索类似问题
3. **提交 Issue**：如果问题仍未解决，提交新的 Issue
4. **关注公众号**：关注「硅基茶水间」获取最新更新和帮助

---

**祝使用愉快！** 🎉

