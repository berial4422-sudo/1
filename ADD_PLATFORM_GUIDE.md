# 添加海外平台支持指南（X/Twitter 等）

## 📋 概述

TrendRadar 使用 [newsnow](https://github.com/ourongxing/newsnow) 项目提供的统一 API 获取热点数据。要添加新平台（如 X/Twitter），需要：

1. **确认 newsnow API 是否支持**（最简单）
2. **如果不支持，需要自己实现**（较复杂）

---

## 🔍 方法一：检查 newsnow API 是否支持

### 步骤 1: 查看 newsnow 支持的平台

1. **访问 newsnow 网站**：
   - https://newsnow.busiyi.world/
   - 点击"更多"查看所有支持的平台

2. **查看源代码**：
   - 访问：https://github.com/ourongxing/newsnow/tree/main/server/sources
   - 查看文件名，文件名就是平台 ID

3. **测试 API**：
   ```bash
   # 测试 X/Twitter（如果支持）
   curl "https://newsnow.busiyi.world/api/s?id=twitter&latest"
   # 或
   curl "https://newsnow.busiyi.world/api/s?id=x&latest"
   ```

### 步骤 2: 如果 API 支持，直接添加配置

编辑 `config/config.yaml`：

```yaml
platforms:
  - id: "toutiao"
    name: "今日头条"
  # ... 其他平台
  - id: "twitter"  # 或 "x"，根据 API 返回的 ID
    name: "X (Twitter)"
```

### 步骤 3: 测试新平台

```bash
# 在本地测试
python main.py

# 或使用 MCP 工具测试
# 在 AI 客户端中调用 trigger_crawl(platforms=['twitter'])
```

---

## 🛠️ 方法二：如果 newsnow 不支持，自己实现

### 方案 A: 向 newsnow 项目贡献支持

1. **Fork newsnow 项目**
2. **添加 X/Twitter 爬虫**
3. **提交 PR**
4. **等待合并后使用**

### 方案 B: 自己实现数据源（高级）

如果 newsnow 不支持，可以：

1. **创建自定义数据获取器**
2. **集成到 TrendRadar**

**实现步骤**：

#### 1. 创建自定义数据源类

创建新文件 `custom_sources.py`：

```python
import requests
from typing import Dict, List, Optional

class CustomDataFetcher:
    """自定义数据获取器（用于 newsnow 不支持的平台）"""
    
    def fetch_x_trending(self) -> Optional[Dict]:
        """
        获取 X/Twitter 趋势
        
        Returns:
            {
                "items": [
                    {
                        "title": "趋势话题",
                        "url": "链接",
                        "mobileUrl": "移动端链接"
                    }
                ]
            }
        """
        try:
            # 方法1: 使用 X API（需要 API Key）
            # 方法2: 爬取 X 趋势页面
            # 方法3: 使用第三方服务
            
            # 示例：使用 X API v2
            # 注意：需要申请 X API 访问权限
            headers = {
                "Authorization": f"Bearer {X_API_TOKEN}",
            }
            
            # 获取趋势
            response = requests.get(
                "https://api.twitter.com/2/tweets/search/recent",
                headers=headers,
                params={"query": "trending", "max_results": 50}
            )
            
            # 解析并转换为标准格式
            data = response.json()
            items = []
            for tweet in data.get("data", []):
                items.append({
                    "title": tweet.get("text", ""),
                    "url": f"https://twitter.com/i/web/status/{tweet.get('id')}",
                    "mobileUrl": f"https://mobile.twitter.com/i/web/status/{tweet.get('id')}"
                })
            
            return {"items": items}
            
        except Exception as e:
            print(f"获取 X 趋势失败: {e}")
            return None
```

#### 2. 修改 main.py 集成自定义数据源

在 `DataFetcher` 类中添加：

```python
def fetch_data(self, id_info, max_retries=2):
    """获取指定ID数据，支持重试"""
    if isinstance(id_info, tuple):
        id_value, alias = id_info
    else:
        id_value = id_info
        alias = id_value
    
    # 检查是否是自定义平台
    if id_value == "x" or id_value == "twitter":
        from custom_sources import CustomDataFetcher
        custom_fetcher = CustomDataFetcher()
        data = custom_fetcher.fetch_x_trending()
        if data:
            return json.dumps(data), id_value, alias
        return None, id_value, alias
    
    # 原有的 newsnow API 逻辑
    url = f"https://newsnow.busiyi.world/api/s?id={id_value}&latest"
    # ... 原有代码
```

#### 3. 添加配置

在 `config/config.yaml` 中添加：

```yaml
platforms:
  - id: "x"
    name: "X (Twitter)"
```

---

## 🔧 推荐的实现方案

### 方案 1: 使用 X API（推荐，但需要 API Key）

**优点**：
- 官方 API，稳定可靠
- 数据准确

**缺点**：
- 需要申请 X API 访问权限
- 可能有费用（取决于使用量）

**实现步骤**：

1. **申请 X API 访问**：
   - 访问：https://developer.twitter.com/
   - 创建应用，获取 API Key 和 Bearer Token

2. **配置 API Key**：
   ```bash
   # 添加到 GitHub Secrets 或环境变量
   X_API_BEARER_TOKEN=your_bearer_token
   ```

3. **实现数据获取**：
   ```python
   def fetch_x_trending(self):
       headers = {
           "Authorization": f"Bearer {os.getenv('X_API_BEARER_TOKEN')}"
       }
       # 使用 X API v2 获取趋势
       # ...
   ```

### 方案 2: 使用第三方服务

**优点**：
- 无需申请 API
- 实现简单

**缺点**：
- 可能不稳定
- 数据可能不完整

**可选服务**：
- Nitter（Twitter 镜像）
- 其他第三方 Twitter 趋势 API

### 方案 3: 等待 newsnow 支持

**优点**：
- 无需自己实现
- 维护成本低

**缺点**：
- 需要等待
- 可能不支持

**建议**：
- 在 newsnow 项目提 Issue 请求支持
- 或直接贡献代码

---

## 📝 添加 X 平台的完整示例

### 假设 newsnow 支持 X（最简单情况）

1. **编辑 `config/config.yaml`**：

```yaml
platforms:
  - id: "toutiao"
    name: "今日头条"
  - id: "baidu"
    name: "百度热搜"
  # ... 其他平台
  - id: "x"  # 或 "twitter"
    name: "X (Twitter)"
```

2. **测试配置**：

```bash
# 方法1: 直接运行
python main.py

# 方法2: 使用 curl 测试 API
curl "https://newsnow.busiyi.world/api/s?id=x&latest"
```

3. **提交更改**：

```bash
git add config/config.yaml
git commit -m "添加 X (Twitter) 平台支持"
git push origin master
```

---

## 🧪 测试新平台

### 方法 1: 本地测试

```bash
# 1. 修改 config.yaml 添加新平台
# 2. 运行测试
python main.py

# 3. 查看输出
# - 检查是否成功获取数据
# - 查看 output 目录下的文件
```

### 方法 2: 使用 MCP 工具测试

在 AI 客户端（如 Cursor）中：

```
触发一次只爬取 X 平台的测试
```

或使用 MCP 工具：

```python
# 在 Python 中
from mcp_server.tools.system import SystemManagementTools

tools = SystemManagementTools()
result = tools.trigger_crawl(platforms=['x'], save_to_local=True)
print(result)
```

### 方法 3: GitHub Actions 测试

1. 提交配置更改
2. 在 GitHub Actions 中手动触发
3. 查看执行日志

---

## ⚠️ 注意事项

### 1. API 限制

- **X API**：有请求频率限制，需要合理控制
- **newsnow API**：依赖第三方服务，可能有稳定性问题

### 2. 数据格式

确保返回的数据格式符合 TrendRadar 的要求：

```json
{
  "items": [
    {
      "title": "新闻标题",
      "url": "PC端链接",
      "mobileUrl": "移动端链接（可选）"
    }
  ]
}
```

### 3. 时区问题

- X 使用 UTC 时间
- 需要确保时间显示正确

### 4. 语言问题

- X 趋势可能是多语言的
- 关键词匹配需要考虑语言差异

---

## 🔍 检查 newsnow 是否支持 X

### 快速检查方法

```bash
# 测试常见的平台 ID
curl "https://newsnow.busiyi.world/api/s?id=twitter&latest"
curl "https://newsnow.busiyi.world/api/s?id=x&latest"
curl "https://newsnow.busiyi.world/api/s?id=twitter-trending&latest"

# 如果返回成功，说明支持
# 如果返回错误，说明不支持
```

### 查看 newsnow 源代码

访问：https://github.com/ourongxing/newsnow/tree/main/server/sources

查看是否有：
- `twitter.ts` 或 `twitter.js`
- `x.ts` 或 `x.js`
- 其他相关文件

---

## 📚 相关资源

- [newsnow 项目](https://github.com/ourongxing/newsnow)
- [newsnow API 文档](https://newsnow.busiyi.world/)
- [X API 文档](https://developer.twitter.com/en/docs)
- [TrendRadar 平台配置 Issue](https://github.com/sansan0/TrendRadar/issues/95)

---

## 🆘 需要帮助？

如果遇到问题：

1. **检查 newsnow 是否支持**：先确认 API 是否支持
2. **查看错误日志**：在本地运行查看具体错误
3. **提交 Issue**：在 TrendRadar 或 newsnow 项目提 Issue
4. **社区交流**：在项目 Discussions 中询问

---

**建议先检查 newsnow API 是否支持 X，这是最简单的方法！** 🚀

