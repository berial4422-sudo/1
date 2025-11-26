# Vercel 部署指南

## ⚠️ 重要限制说明

Vercel Serverless Functions 有以下限制：

1. **执行时间限制**：
   - Hobby 计划：10 秒
   - Pro 计划：60 秒
   - 如果爬虫任务执行时间超过限制，会被强制终止

2. **定时任务**：
   - 免费计划不支持 Cron Jobs
   - 需要使用外部 cron 服务（如 cron-job.org）来触发

3. **文件系统**：
   - Serverless Functions 是临时环境
   - 需要将数据存储到外部服务（如 Vercel KV、Upstash、数据库等）

## 📋 部署步骤

### 1. 准备配置文件

确保以下文件存在：
- `config/config.yaml`
- `config/frequency_words.txt`

### 2. 配置 Vercel 环境变量

在 Vercel 项目设置中添加以下环境变量：

**通知渠道配置**（根据需要选择）：
```
FEISHU_WEBHOOK_URL=你的飞书webhook
DINGTALK_WEBHOOK_URL=你的钉钉webhook
WEWORK_WEBHOOK_URL=你的企业微信webhook
TELEGRAM_BOT_TOKEN=你的telegram_bot_token
TELEGRAM_CHAT_ID=你的telegram_chat_id
EMAIL_FROM=你的发件邮箱
EMAIL_PASSWORD=你的邮箱密码或授权码
EMAIL_TO=收件人邮箱
NTFY_TOPIC=你的ntfy主题
```

**运行配置**：
```
REPORT_MODE=daily
ENABLE_CRAWLER=true
ENABLE_NOTIFICATION=true
```

### 3. 部署到 Vercel

```bash
# 安装 Vercel CLI
npm i -g vercel

# 登录 Vercel
vercel login

# 部署
vercel

# 生产环境部署
vercel --prod
```

或者通过 GitHub 连接自动部署。

### 4. 配置外部 Cron 服务

由于 Vercel 免费计划不支持 Cron Jobs，需要使用外部服务：

#### 使用 cron-job.org（免费）

1. 注册账号：https://cron-job.org
2. 创建新任务：
   - **URL**: `https://你的项目.vercel.app/api/crawler`
   - **Schedule**: 选择执行频率（如每 30 分钟）
   - **Request Method**: GET 或 POST
3. 保存并启用

#### 使用 EasyCron（免费）

1. 注册账号：https://www.easycron.com
2. 创建 Cron Job：
   - **URL**: `https://你的项目.vercel.app/api/crawler`
   - **Cron Expression**: `*/30 * * * *`（每 30 分钟）
3. 保存

#### 使用 GitHub Actions（推荐）

如果你已经有 GitHub 仓库，可以继续使用 GitHub Actions，不需要部署到 Vercel。

### 5. 测试

访问你的 Vercel 函数 URL：
```
https://你的项目.vercel.app/api/crawler
```

如果返回 `{"success": true}`，说明部署成功。

## 🔧 优化建议

### 1. 处理超时问题

如果爬虫任务执行时间较长，可以考虑：

- **拆分任务**：将多个平台的爬取拆分为多个函数
- **异步处理**：使用队列服务（如 Vercel Queue、Upstash Queue）
- **升级到 Pro 计划**：获得 60 秒执行时间

### 2. 数据存储

由于 Serverless Functions 是临时环境，建议：

- 使用 Vercel KV 存储配置
- 使用 Upstash Redis 存储数据
- 使用数据库（如 Supabase、PlanetScale）存储历史数据

### 3. 监控和日志

- 使用 Vercel Analytics 监控函数执行
- 查看 Vercel Dashboard 的 Function Logs
- 集成 Sentry 进行错误追踪

## ❌ 不推荐使用 Vercel 的场景

1. **爬虫任务执行时间 > 60 秒**
2. **需要精确的定时执行**（外部 cron 服务可能有延迟）
3. **需要大量数据存储**（Serverless 存储成本高）
4. **需要长期运行的任务**

## ✅ 推荐替代方案

1. **GitHub Actions**（免费，适合定时任务）
2. **Railway**（免费额度，支持长时间运行）
3. **Render**（免费计划，支持 Cron Jobs）
4. **Fly.io**（免费额度，支持 Docker）
5. **自己的服务器 + Docker**（完全控制）

## 📝 示例：使用 Vercel KV 存储配置

如果需要动态配置，可以使用 Vercel KV：

```python
from vercel_kv import kv

# 存储配置
await kv.set("config", json.dumps(config_data))

# 读取配置
config = json.loads(await kv.get("config"))
```

## 🆘 故障排查

1. **函数超时**：
   - 检查执行时间是否超过限制
   - 优化爬虫代码，减少请求时间
   - 考虑升级到 Pro 计划

2. **配置文件找不到**：
   - 确保配置文件在项目根目录
   - 检查 `CONFIG_PATH` 环境变量

3. **依赖安装失败**：
   - 检查 `api/requirements.txt` 是否正确
   - 确保所有依赖都列在文件中

## 📚 相关资源

- [Vercel Serverless Functions 文档](https://vercel.com/docs/functions)
- [Vercel Cron Jobs（Pro 计划）](https://vercel.com/docs/cron-jobs)
- [cron-job.org](https://cron-job.org)
- [EasyCron](https://www.easycron.com)

