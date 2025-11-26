# 推送频率配置指南

## 📋 配置位置

推送频率有两个层面的配置：

1. **GitHub Actions 执行频率**：控制多久运行一次爬虫（`.github/workflows/crawler.yml`）
2. **推送模式**：控制每次运行时是否推送（`config/config.yaml`）

---

## ⏰ 配置 GitHub Actions 执行频率

### 位置

编辑文件：`.github/workflows/crawler.yml`

找到以下部分：

```yaml
on:
  schedule:
    - cron: "0 * * * *" # 每小时整点运行一次(实际有偏差)
```

### Cron 表达式说明

Cron 表达式格式：`分钟 小时 日 月 星期`

**重要提示**：
- GitHub Actions 使用 **UTC 时间**（不是北京时间）
- 北京时间 = UTC 时间 + 8 小时
- 定时任务可能有 ±20 分钟的偏差

### 常用配置示例

| Cron 表达式 | 说明 | 北京时间对应 |
|------------|------|------------|
| `0 * * * *` | 每小时整点运行 | 每小时的 08:00, 09:00, 10:00... |
| `*/30 * * * *` | 每 30 分钟运行一次 | 每小时的 08:00, 08:30, 09:00, 09:30... |
| `0 */2 * * *` | 每 2 小时运行一次 | 08:00, 10:00, 12:00, 14:00... |
| `0 8-22 * * *` | 每天 8-22 点，每小时运行 | 08:00-22:00 每小时 |
| `*/30 0-14 * * *` | UTC 0-14 点，每 30 分钟 | 08:00-22:00 每 30 分钟 |
| `0 9,12,18 * * *` | 每天 9 点、12 点、18 点运行 | 17:00, 20:00, 02:00（次日） |
| `0 9-18 * * 1-5` | 工作日 9-18 点，每小时运行 | 工作日 17:00-02:00（次日） |

### 时间换算示例

**示例 1**：想要每天 8:00-22:00（北京时间）每 30 分钟运行一次

- 北京时间 8:00 = UTC 0:00
- 北京时间 22:00 = UTC 14:00
- Cron 表达式：`*/30 0-14 * * *`

**示例 2**：想要每天 9:00-18:00（北京时间）每小时运行

- 北京时间 9:00 = UTC 1:00
- 北京时间 18:00 = UTC 10:00
- Cron 表达式：`0 1-10 * * *`

### 修改步骤

1. **编辑工作流文件**：
   ```bash
   # 在本地编辑
   vim .github/workflows/crawler.yml
   
   # 或使用你喜欢的编辑器
   ```

2. **修改 cron 表达式**：
   ```yaml
   on:
     schedule:
       - cron: "*/30 * * * *"  # 改为你想要的频率
   ```

3. **提交更改**：
   ```bash
   git add .github/workflows/crawler.yml
   git commit -m "调整推送频率为每30分钟"
   git push origin master
   ```

### ⚠️ 重要提醒

1. **不要过于频繁**：
   - GitHub Actions 有资源限制
   - 建议最低频率：每 30 分钟一次
   - 过于频繁可能被判定为滥用

2. **时间偏差**：
   - GitHub Actions 的定时任务可能有 ±20 分钟偏差
   - 如果需要精确时间，建议使用 Docker 部署

3. **UTC 时间**：
   - 记住使用 UTC 时间，不是北京时间
   - 可以使用在线工具转换：https://crontab.guru/

---

## 📊 配置推送模式

### 位置

编辑文件：`config/config.yaml`

找到以下部分：

```yaml
report:
  mode: "daily" # 可选: "daily"|"incremental"|"current"
```

### 三种推送模式

#### 1. daily（当日汇总模式）

**特点**：
- 按时推送当日所有匹配新闻
- 会包含之前推送过的新闻
- 适合：需要完整日报的用户

**配置**：
```yaml
report:
  mode: "daily"
```

**推送时机**：每次 GitHub Actions 执行时都推送

#### 2. incremental（增量监控模式）

**特点**：
- 只推送新增内容
- 零重复，避免信息干扰
- 适合：高频监控、避免打扰

**配置**：
```yaml
report:
  mode: "incremental"
```

**推送时机**：只有新出现匹配关键词的新闻时才推送

#### 3. current（当前榜单模式）

**特点**：
- 按时推送当前榜单匹配新闻
- 持续在榜的新闻每次都会出现
- 适合：实时热点追踪

**配置**：
```yaml
report:
  mode: "current"
```

**推送时机**：每次 GitHub Actions 执行时都推送

### 推送模式对比

| 模式 | 推送频率 | 内容特点 | 适用场景 |
|------|---------|---------|---------|
| `daily` | 每次执行都推送 | 当日所有新闻 | 日报总结 |
| `incremental` | 有新增才推送 | 只推送新内容 | 避免重复 |
| `current` | 每次执行都推送 | 当前榜单新闻 | 实时追踪 |

### 修改步骤

1. **编辑配置文件**：
   ```bash
   vim config/config.yaml
   ```

2. **修改模式**：
   ```yaml
   report:
     mode: "incremental"  # 改为你想要的模式
   ```

3. **提交更改**：
   ```bash
   git add config/config.yaml
   git commit -m "切换为增量监控模式"
   git push origin master
   ```

---

## 🕐 推送时间窗口控制（可选）

### 功能说明

可以限制推送的时间范围，避免非工作时间打扰。

### 配置位置

编辑文件：`config/config.yaml`

找到以下部分：

```yaml
notification:
  push_window:
    enabled: false  # 是否启用推送时间窗口控制
    time_range:
      start: "20:00"  # 推送时间窗口开始（北京时间）
      end: "22:00"    # 推送时间窗口结束（北京时间）
    once_per_day: true  # 每天在时间窗口内只推送一次
```

### 配置示例

**示例 1**：只在工作日 9:00-18:00 推送

```yaml
notification:
  push_window:
    enabled: true
    time_range:
      start: "09:00"
      end: "18:00"
    once_per_day: false  # 窗口内每次执行都推送
```

**示例 2**：每天晚上 20:00-22:00 只推送一次

```yaml
notification:
  push_window:
    enabled: true
    time_range:
      start: "20:00"
      end: "22:00"
    once_per_day: true  # 每天只推送一次
```

### ⚠️ 注意事项

1. **GitHub Actions 时间不稳定**：
   - 执行时间可能有 ±20 分钟偏差
   - 时间窗口建议至少留足 2 小时

2. **精确时间控制**：
   - 如果需要精确的定时推送，建议使用 Docker 部署

---

## 🎯 推荐配置方案

### 方案 1: 普通用户（推荐）

**执行频率**：每小时一次
```yaml
cron: "0 * * * *"
```

**推送模式**：增量监控
```yaml
mode: "incremental"
```

**效果**：每小时检查一次，有新内容才推送，避免打扰

### 方案 2: 高频监控

**执行频率**：每 30 分钟一次
```yaml
cron: "*/30 * * * *"
```

**推送模式**：增量监控
```yaml
mode: "incremental"
```

**效果**：更频繁检查，但只推送新内容

### 方案 3: 日报模式

**执行频率**：每天固定时间（如 18:00）
```yaml
cron: "0 10 * * *"  # UTC 10:00 = 北京时间 18:00
```

**推送模式**：当日汇总
```yaml
mode: "daily"
```

**效果**：每天一次完整日报

### 方案 4: 工作时间推送

**执行频率**：每 30 分钟一次
```yaml
cron: "*/30 0-14 * * *"  # UTC 0-14 点 = 北京时间 8-22 点
```

**推送模式**：当前榜单
```yaml
mode: "current"
```

**推送时间窗口**：
```yaml
push_window:
  enabled: true
  time_range:
    start: "09:00"
    end: "18:00"
  once_per_day: false
```

**效果**：工作时间每 30 分钟检查，推送当前热点

---

## 🔧 快速修改命令

### 修改执行频率

```bash
# 编辑工作流文件
vim .github/workflows/crawler.yml

# 修改 cron 表达式后提交
git add .github/workflows/crawler.yml
git commit -m "调整执行频率"
git push origin master
```

### 修改推送模式

```bash
# 编辑配置文件
vim config/config.yaml

# 修改 mode 后提交
git add config/config.yaml
git commit -m "切换推送模式"
git push origin master
```

---

## 📝 配置检查清单

修改后，确认：

- [ ] Cron 表达式语法正确
- [ ] 考虑了 UTC 时间转换
- [ ] 推送模式符合需求
- [ ] 已提交并推送到 GitHub
- [ ] 手动触发测试，验证配置生效

---

## 🛠️ 实用工具

### Cron 表达式生成器

- **在线工具**：https://crontab.guru/
- **说明**：输入 cron 表达式，查看执行时间

### UTC 时间转换

- **在线工具**：https://www.timeanddate.com/worldclock/converter.html
- **说明**：将北京时间转换为 UTC 时间

---

## ❓ 常见问题

### Q1: 为什么设置了每 30 分钟，但实际不是？

**原因**：GitHub Actions 的定时任务有 ±20 分钟偏差

**解决**：这是正常现象，无法避免。如需精确时间，使用 Docker 部署。

### Q2: 如何知道当前配置的执行时间？

**方法**：
1. 查看 Cron 表达式
2. 使用 https://crontab.guru/ 查看执行时间
3. 记住转换为北京时间（UTC + 8）

### Q3: 增量模式为什么没有推送？

**原因**：
- 没有新出现匹配关键词的新闻
- 这是正常行为，说明没有新热点

**验证**：
- 查看 Actions 日志
- 确认是否有匹配的新闻

### Q4: 可以设置每分钟执行吗？

**不推荐**：
- GitHub Actions 有资源限制
- 过于频繁可能被判定为滥用
- 建议最低频率：每 30 分钟

---

## 📚 相关文档

- [GitHub Actions 配置指南](GITHUB_ACTIONS_GUIDE.md)
- [配置文件说明](README.md#配置详解)
- [推送模式详解](README.md#3-推送模式详解)

---

**配置完成后，记得提交更改并测试！** 🚀

