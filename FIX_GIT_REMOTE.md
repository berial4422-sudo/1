# 修复 Git Remote 配置

## 🔍 问题诊断

当前 remote 指向原仓库，导致没有推送权限：
```
origin  https://github.com/sansan0/TrendRadar
```

## ✅ 解决方案

### 方案 1: 如果你已经 Fork 了仓库

1. **获取你的 Fork 地址**：
   - 访问 https://github.com/你的用户名/TrendRadar
   - 复制仓库地址

2. **更新 remote URL**：
   ```bash
   # 替换为你的 GitHub 用户名
   git remote set-url origin https://github.com/你的用户名/TrendRadar.git
   
   # 或者使用 SSH（如果配置了 SSH key）
   git remote set-url origin git@github.com:你的用户名/TrendRadar.git
   ```

3. **验证配置**：
   ```bash
   git remote -v
   ```

4. **重新推送**：
   ```bash
   git push origin master
   # 或者
   git push origin main
   ```

### 方案 2: 如果还没有 Fork

1. **Fork 仓库**：
   - 访问 https://github.com/sansan0/TrendRadar
   - 点击右上角的 "Fork" 按钮
   - 等待 Fork 完成

2. **然后按照方案 1 的步骤操作**

### 方案 3: 添加新的 remote（保留原仓库）

如果你想同时保留原仓库和你的 Fork：

```bash
# 添加你的 Fork 作为新的 remote
git remote add myfork https://github.com/你的用户名/TrendRadar.git

# 推送到你的 Fork
git push myfork master

# 查看所有 remote
git remote -v
```

---

## 🔧 快速修复命令

**替换 `YOUR_USERNAME` 为你的 GitHub 用户名**：

```bash
# 更新 remote URL
git remote set-url origin https://github.com/YOUR_USERNAME/TrendRadar.git

# 验证
git remote -v

# 推送
git push origin master
```

---

## 📝 设置 Git 用户信息（可选）

如果看到用户信息警告，可以设置：

```bash
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"
```

---

## ✅ 验证

推送成功后，你应该能看到：
- 你的 Fork 仓库中有新的提交
- GitHub Actions 可以正常触发



