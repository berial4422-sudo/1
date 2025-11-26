# GitHub Actions 测试检查清单

## ✅ 本地测试（在提交到 GitHub 之前）

### 1. 运行测试脚本

```bash
# 给脚本添加执行权限
chmod +x test_github_actions.sh

# 运行测试
./test_github_actions.sh
```

### 2. 手动检查清单

- [ ] 工作流文件语法正确（`.github/workflows/crawler.yml`）
- [ ] 配置文件存在且格式正确（`config/config.yaml`）
- [ ] 关键词文件存在（`config/frequency_words.txt`）
- [ ] Python 依赖文件存在（`requirements.txt`）
- [ ] 主程序文件存在（`main.py`）

### 3. 验证配置文件内容

检查 `config/config.yaml`：
- [ ] `crawler.enable_crawler` 设置为 `true`
- [ ] `notification.enable_notification` 设置为 `true`
- [ ] `report.mode` 设置为期望的模式（`daily`/`incremental`/`current`）
- [ ] 至少配置了一个监控平台

检查 `config/frequency_words.txt`：
- [ ] 文件不为空
- [ ] 关键词格式正确（每行一个关键词）

---

## 🚀 GitHub 测试（提交后）

### 1. 提交更改

```bash
git add .
git commit -m "优化 GitHub Actions 配置"
git push
```

### 2. 检查 GitHub Actions 是否启用

1. 进入你的 GitHub 仓库
2. 点击 `Settings` → `Actions` → `General`
3. 确保 "Allow all actions and reusable workflows" 已启用

### 3. 手动触发测试

1. 进入 `Actions` 标签页
2. 找到 **"Hot News Crawler"** 工作流
3. 点击 **"Run workflow"** → **"Run workflow"**
4. 等待执行完成（通常 1-3 分钟）

### 4. 检查执行结果

#### ✅ 成功标志

- [ ] 工作流显示绿色 ✅
- [ ] 所有步骤都成功完成
- [ ] 没有错误日志
- [ ] 如果配置了通知渠道，收到了推送消息

#### ❌ 失败排查

如果工作流失败，检查以下内容：

**依赖安装失败**：
- 检查 `requirements.txt` 是否正确
- 查看 "Install dependencies" 步骤的日志

**配置文件错误**：
- 检查 "Verify required files" 步骤
- 确保 `config/config.yaml` 和 `config/frequency_words.txt` 存在

**爬虫执行失败**：
- 查看 "Run crawler" 步骤的详细日志
- 检查是否有网络错误或数据源问题

**提交失败**：
- 检查是否有文件变更
- 确认仓库权限设置正确

---

## 🔍 详细测试步骤

### 测试 1: 工作流语法验证

```bash
# 使用 act（GitHub Actions 本地运行工具）测试
# 需要先安装: https://github.com/nektos/act

act -l  # 列出所有工作流
act workflow_dispatch  # 手动触发测试
```

### 测试 2: Python 环境测试

```bash
# 模拟 GitHub Actions 环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py --help  # 如果支持的话
```

### 测试 3: 配置文件验证

```bash
# 验证 YAML 语法
python3 -c "import yaml; yaml.safe_load(open('config/config.yaml'))"
```

---

## 📊 预期结果

### 成功的执行流程

1. ✅ Checkout repository - 成功拉取代码
2. ✅ Set up Python - 成功设置 Python 3.11
3. ✅ Install dependencies - 成功安装所有依赖
4. ✅ Verify required files - 配置文件检查通过
5. ✅ Run crawler - 成功执行爬虫任务
6. ✅ Commit and push - 如果有变更，成功提交
7. ✅ Workflow Summary - 显示执行摘要

### 预期输出

- 爬虫成功获取新闻数据
- 生成 HTML 和 TXT 报告文件
- 如果配置了通知渠道，发送推送消息
- 自动提交生成的报告文件到仓库

---

## 🐛 常见问题测试

### 问题 1: 工作流不运行

**测试**：
- [ ] 检查 Actions 是否启用
- [ ] 检查工作流文件是否在 `.github/workflows/` 目录
- [ ] 检查文件命名是否正确（`.yml` 或 `.yaml`）

### 问题 2: 依赖安装失败

**测试**：
- [ ] 本地运行 `pip install -r requirements.txt` 测试
- [ ] 检查 Python 版本是否 >= 3.10

### 问题 3: 配置文件找不到

**测试**：
- [ ] 确认文件路径正确：`config/config.yaml`
- [ ] 确认文件已提交到仓库
- [ ] 检查文件权限

### 问题 4: 没有收到推送

**测试**：
- [ ] 检查是否配置了 GitHub Secrets
- [ ] 检查 Secret 名称是否正确
- [ ] 检查 Webhook URL 或 Token 是否有效
- [ ] 查看工作流日志中的错误信息

---

## 📝 测试报告模板

完成测试后，记录结果：

```
测试日期: [日期]
测试人员: [你的名字]

✅ 通过的测试:
- [列出通过的测试项]

❌ 失败的测试:
- [列出失败的测试项]

⚠️  警告:
- [列出警告项]

📊 总体评估:
[总体评估和下一步计划]
```

---

## 🎯 快速测试命令

```bash
# 一键测试所有配置
./test_github_actions.sh

# 验证工作流语法
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/crawler.yml'))"

# 验证配置文件
python3 -c "import yaml; yaml.safe_load(open('config/config.yaml'))"

# 检查 Python 版本
python3 --version

# 测试依赖安装
pip install -r requirements.txt --dry-run
```

---

**完成所有测试后，你的 GitHub Actions 工作流应该可以正常运行了！** 🎉

