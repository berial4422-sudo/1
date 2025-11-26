# Fork 仓库并推送更改

## 📋 当前状态

✅ Git remote 已更新为你的 Fork 地址  
❌ 仓库尚未 Fork（需要先 Fork）

## 🚀 操作步骤

### 步骤 1: Fork 仓库

1. **访问原仓库**：
   - 打开浏览器，访问：https://github.com/sansan0/TrendRadar

2. **点击 Fork 按钮**：
   - 在页面右上角找到 **"Fork"** 按钮
   - 点击它

3. **等待 Fork 完成**：
   - GitHub 会自动创建 `maverikhe-cpu/TrendRadar` 仓库
   - 通常需要几秒钟

### 步骤 2: 验证 Fork 成功

访问你的 Fork 地址，确认仓库已创建：
- https://github.com/maverikhe-cpu/TrendRadar

### 步骤 3: 推送更改

Fork 完成后，运行以下命令：

```bash
git push origin master
```

或者如果默认分支是 `main`：

```bash
git push origin master:main
```

---

## 🔍 如果 Fork 后仍然无法推送

### 检查 1: 确认仓库已 Fork

访问 https://github.com/maverikhe-cpu/TrendRadar，确认能看到仓库。

### 检查 2: 检查分支名称

GitHub 新仓库默认分支可能是 `main` 而不是 `master`：

```bash
# 查看本地分支
git branch

# 如果本地是 master，推送到 main
git push origin master:main

# 或者重命名本地分支
git branch -m master main
git push origin main
```

### 检查 3: 使用 SSH（如果配置了 SSH key）

如果配置了 SSH key，可以使用 SSH 方式：

```bash
git remote set-url origin git@github.com:maverikhe-cpu/TrendRadar.git
git push origin master
```

---

## ✅ 推送成功后的下一步

1. **配置 GitHub Secrets**：
   - 进入 https://github.com/maverikhe-cpu/TrendRadar/settings/secrets/actions
   - 添加通知渠道的 Secret（如 `WEWORK_WEBHOOK_URL`）

2. **启用 GitHub Actions**：
   - Settings → Actions → General
   - 确保 "Allow all actions and reusable workflows" 已启用

3. **手动触发测试**：
   - 进入 Actions 标签页
   - 找到 "Hot News Crawler"
   - 点击 "Run workflow"

---

## 🆘 需要帮助？

如果遇到问题：
- 确认已登录 GitHub
- 确认有权限访问仓库
- 检查网络连接
- 查看 GitHub 的错误提示



