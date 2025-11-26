# 集成 X (Twitter) 平台完整指南

## 📋 当前状态

✅ **测试结果**：newsnow API 目前**不支持** X/Twitter 平台
- 测试 `id=x`：返回 "Invalid source id"
- 测试 `id=twitter`：返回 "Invalid source id"

因此需要**自己实现**数据获取逻辑。

---

## 🚀 快速开始（推荐方案）

### 方案 1: 使用 Nitter 镜像（最简单，无需 API Key）

#### 步骤 1: 安装依赖

```bash
pip install beautifulsoup4
```

#### 步骤 2: 修改 main.py 集成自定义数据源

在 `DataFetcher` 类的 `fetch_data` 方法中添加：

```python
def fetch_data(self, id_info, max_retries=2, ...):
    """获取指定ID数据，支持重试"""
    if isinstance(id_info, tuple):
        id_value, alias = id_info
    else:
        id_value = id_info
        alias = id_value
    
    # 检查是否是 X 平台（自定义数据源）
    if id_value in ["x", "twitter"]:
        try:
            from custom_sources.x_fetcher import XDataFetcher
            x_fetcher = XDataFetcher(use_api=False)  # 使用 Nitter，无需 API
            data = x_fetcher.fetch_trending()
            if data:
                return json.dumps(data), id_value, alias
        except Exception as e:
            print(f"X 数据获取失败: {e}")
        return None, id_value, alias
    
    # 原有的 newsnow API 逻辑
    url = f"https://newsnow.busiyi.world/api/s?id={id_value}&latest"
    # ... 原有代码
```

#### 步骤 3: 添加平台配置

编辑 `config/config.yaml`：

```yaml
platforms:
  - id: "toutiao"
    name: "今日头条"
  # ... 其他平台
  - id: "x"
    name: "X (Twitter)"
```

#### 步骤 4: 更新 requirements.txt

```bash
echo "beautifulsoup4>=4.12.0" >> requirements.txt
```

#### 步骤 5: 测试

```bash
python main.py
```

---

### 方案 2: 使用 X API（更稳定，但需要 API Key）

#### 步骤 1: 申请 X API 访问

1. 访问：https://developer.twitter.com/
2. 创建应用
3. 获取 Bearer Token

#### 步骤 2: 配置环境变量

**GitHub Actions**：
- 在 GitHub Secrets 中添加：
  - Name: `X_API_BEARER_TOKEN`
  - Secret: 你的 Bearer Token

**本地/Docker**：
```bash
export X_API_BEARER_TOKEN="your_bearer_token_here"
```

#### 步骤 3: 修改 main.py

```python
# 在 fetch_data 方法中
if id_value in ["x", "twitter"]:
    try:
        from custom_sources.x_fetcher import XDataFetcher
        x_fetcher = XDataFetcher(use_api=True)  # 使用 X API
        data = x_fetcher.fetch_trending()
        if data:
            return json.dumps(data), id_value, alias
    except Exception as e:
        print(f"X 数据获取失败: {e}")
    return None, id_value, alias
```

---

## 📝 完整集成步骤

### 1. 创建自定义数据源目录

```bash
mkdir -p custom_sources
```

### 2. 创建 X 数据获取器

已创建文件：`custom_sources/x_fetcher.py`

### 3. 修改 main.py

在 `DataFetcher.fetch_data` 方法中添加 X 平台支持：

```python
# 在 fetch_data 方法开头添加
if isinstance(id_info, tuple):
    id_value, alias = id_info
else:
    id_value = id_info
    alias = id_value

# 添加 X 平台支持（在原有 newsnow API 逻辑之前）
if id_value in ["x", "twitter"]:
    try:
        from custom_sources.x_fetcher import XDataFetcher
        # 优先尝试 API，失败则使用 Nitter
        use_api = bool(os.getenv("X_API_BEARER_TOKEN"))
        x_fetcher = XDataFetcher(use_api=use_api)
        data = x_fetcher.fetch_trending()
        if data:
            return json.dumps(data), id_value, alias
    except Exception as e:
        print(f"X 数据获取失败: {e}")
    return None, id_value, alias

# 原有的 newsnow API 逻辑
url = f"https://newsnow.busiyi.world/api/s?id={id_value}&latest"
# ... 继续原有代码
```

### 4. 更新依赖

编辑 `requirements.txt`：

```txt
requests>=2.32.5,<3.0.0
pytz>=2025.2,<2026.0
PyYAML>=6.0.3,<7.0.0
fastmcp>=2.12.0,<2.14.0
websockets>=13.0,<14.0
beautifulsoup4>=4.12.0  # 新增：用于 Nitter 解析
```

### 5. 添加平台配置

编辑 `config/config.yaml`：

```yaml
platforms:
  - id: "toutiao"
    name: "今日头条"
  - id: "baidu"
    name: "百度热搜"
  # ... 其他平台
  - id: "x"
    name: "X (Twitter)"
```

### 6. 测试

```bash
# 测试 X 数据获取器
python custom_sources/x_fetcher.py

# 测试完整流程
python main.py
```

---

## 🔧 修改 main.py 的具体位置

找到 `main.py` 中的 `DataFetcher.fetch_data` 方法（约第 445 行），在方法开头添加：

```python
def fetch_data(
    self,
    id_info: Union[str, Tuple[str, str]],
    max_retries: int = 2,
    min_retry_wait: int = 3,
    max_retry_wait: int = 5,
) -> Tuple[Optional[str], str, str]:
    """获取指定ID数据，支持重试"""
    if isinstance(id_info, tuple):
        id_value, alias = id_info
    else:
        id_value = id_info
        alias = id_value

    # ========== 添加 X 平台支持 ==========
    if id_value in ["x", "twitter"]:
        try:
            from custom_sources.x_fetcher import XDataFetcher
            # 优先使用 API（如果配置了），否则使用 Nitter
            use_api = bool(os.getenv("X_API_BEARER_TOKEN"))
            x_fetcher = XDataFetcher(use_api=use_api)
            data = x_fetcher.fetch_trending()
            if data:
                print(f"获取 {id_value} 成功（自定义数据源）")
                return json.dumps(data), id_value, alias
        except ImportError as e:
            print(f"X 数据获取器导入失败: {e}")
            print("提示：使用 Nitter 需要安装 beautifulsoup4: pip install beautifulsoup4")
        except Exception as e:
            print(f"X 数据获取失败: {e}")
        return None, id_value, alias
    # ========== X 平台支持结束 ==========

    # 原有的 newsnow API 逻辑
    url = f"https://newsnow.busiyi.world/api/s?id={id_value}&latest"
    # ... 继续原有代码
```

---

## 🧪 测试步骤

### 1. 测试 X 数据获取器

```bash
# 测试 Nitter 方式
python custom_sources/x_fetcher.py
```

### 2. 测试完整流程

```bash
# 修改 config.yaml 添加 X 平台
# 运行主程序
python main.py
```

### 3. 检查输出

- 查看控制台日志，确认 X 平台数据获取成功
- 检查 `output` 目录，确认生成了 X 平台的数据文件

---

## ⚠️ 注意事项

### 1. Nitter 镜像可能不稳定

- Nitter 实例可能随时不可用
- 如果失败，可以：
  - 切换到其他 Nitter 实例
  - 或使用 X API

### 2. X API 限制

- 有请求频率限制
- 免费层每月有限额
- 需要合理控制请求频率

### 3. 数据格式

确保返回的数据格式符合要求：

```json
{
  "items": [
    {
      "title": "趋势话题（字符串）",
      "url": "PC端链接",
      "mobileUrl": "移动端链接（可选）"
    }
  ]
}
```

### 4. 语言问题

- X 趋势可能是多语言的
- 关键词匹配需要考虑语言
- 建议在 `frequency_words.txt` 中添加英文关键词

---

## 📚 相关文件

- `custom_sources/x_fetcher.py` - X 数据获取器实现
- `main.py` - 需要修改集成点
- `config/config.yaml` - 需要添加平台配置
- `requirements.txt` - 需要添加依赖

---

## 🆘 故障排查

### 问题 1: ImportError: No module named 'bs4'

**解决**：
```bash
pip install beautifulsoup4
```

### 问题 2: Nitter 实例不可用

**解决**：
- 编辑 `custom_sources/x_fetcher.py`
- 修改 `nitter_instances` 列表，添加其他可用的 Nitter 实例

### 问题 3: X API 返回 401 错误

**解决**：
- 检查 Bearer Token 是否正确
- 确认 API 权限是否足够

### 问题 4: 获取的数据为空

**解决**：
- 检查网络连接
- 查看错误日志
- 尝试切换数据源（API ↔ Nitter）

---

## 🎯 下一步

1. ✅ 创建 `custom_sources/x_fetcher.py`
2. ⏳ 修改 `main.py` 集成 X 数据获取器
3. ⏳ 更新 `requirements.txt`
4. ⏳ 添加平台配置
5. ⏳ 测试运行
6. ⏳ 提交更改

---

**需要我帮你修改 main.py 集成 X 平台吗？** 🚀


