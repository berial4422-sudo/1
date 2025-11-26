# 添加 X (Twitter) 平台支持

## 🔍 第一步：检查 newsnow API 是否支持

### 方法 1: 访问 newsnow 网站查看

1. 访问：https://newsnow.busiyi.world/
2. 点击"更多"查看所有支持的平台
3. 查看是否有 X 或 Twitter

### 方法 2: 查看 newsnow 源代码

访问：https://github.com/ourongxing/newsnow/tree/main/server/sources

查看文件名列表，确认是否有：
- `twitter.ts` / `twitter.js`
- `x.ts` / `x.js`

### 方法 3: 测试 API（需要完整请求头）

```bash
# 测试 Twitter
curl -H "User-Agent: Mozilla/5.0" \
     -H "Accept: application/json" \
     "https://newsnow.busiyi.world/api/s?id=twitter&latest"

# 测试 X
curl -H "User-Agent: Mozilla/5.0" \
     -H "Accept: application/json" \
     "https://newsnow.busiyi.world/api/s?id=x&latest"
```

---

## ✅ 如果 newsnow 支持 X（最简单）

### 步骤 1: 添加平台配置

编辑 `config/config.yaml`：

```yaml
platforms:
  - id: "toutiao"
    name: "今日头条"
  - id: "baidu"
    name: "百度热搜"
  # ... 其他现有平台
  - id: "x"  # 或 "twitter"，根据 API 返回的实际 ID
    name: "X (Twitter)"
```

### 步骤 2: 测试配置

```bash
# 本地测试
python main.py

# 或使用 Python 测试单个平台
python3 -c "
import requests
url = 'https://newsnow.busiyi.world/api/s?id=x&latest'
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Accept': 'application/json'
}
response = requests.get(url, headers=headers)
print(response.json() if response.status_code == 200 else response.text)
"
```

### 步骤 3: 提交更改

```bash
git add config/config.yaml
git commit -m "添加 X (Twitter) 平台支持"
git push origin master
```

---

## 🛠️ 如果 newsnow 不支持 X（需要自己实现）

### 方案 A: 使用 X API（推荐但需要 API Key）

#### 1. 申请 X API 访问

- 访问：https://developer.twitter.com/
- 创建应用
- 获取 Bearer Token

#### 2. 创建自定义数据获取器

创建文件 `custom_x_fetcher.py`：

```python
"""
X (Twitter) 自定义数据获取器
需要 X API Bearer Token
"""
import os
import requests
from typing import Dict, Optional, List

class XDataFetcher:
    """X/Twitter 数据获取器"""
    
    def __init__(self):
        self.bearer_token = os.getenv("X_API_BEARER_TOKEN")
        if not self.bearer_token:
            raise ValueError("需要设置 X_API_BEARER_TOKEN 环境变量")
    
    def fetch_trending(self) -> Optional[Dict]:
        """
        获取 X 趋势话题
        
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
            # 使用 X API v2 获取趋势
            # 注意：X API 可能不直接提供趋势 API
            # 需要根据实际情况调整
            
            headers = {
                "Authorization": f"Bearer {self.bearer_token}",
            }
            
            # 方法1: 使用搜索 API 获取热门推文
            url = "https://api.twitter.com/2/tweets/search/recent"
            params = {
                "query": "lang:en -is:retweet",  # 英文非转推
                "max_results": 50,
                "tweet.fields": "public_metrics,created_at"
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            items = []
            
            for tweet in data.get("data", []):
                text = tweet.get("text", "")
                tweet_id = tweet.get("id")
                metrics = tweet.get("public_metrics", {})
                
                # 只选择高互动量的推文作为"热点"
                if metrics.get("like_count", 0) + metrics.get("retweet_count", 0) > 100:
                    items.append({
                        "title": text[:100],  # 限制长度
                        "url": f"https://twitter.com/i/web/status/{tweet_id}",
                        "mobileUrl": f"https://mobile.twitter.com/i/web/status/{tweet_id}"
                    })
            
            return {"items": items[:20]}  # 返回前20条
            
        except Exception as e:
            print(f"获取 X 趋势失败: {e}")
            return None
```

#### 3. 修改 main.py 集成

在 `DataFetcher` 类中修改 `fetch_data` 方法：

```python
def fetch_data(self, id_info, max_retries=2, ...):
    """获取指定ID数据，支持重试"""
    if isinstance(id_info, tuple):
        id_value, alias = id_info
    else:
        id_value = id_info
        alias = id_value
    
    # 检查是否是 X 平台
    if id_value in ["x", "twitter"]:
        try:
            from custom_x_fetcher import XDataFetcher
            x_fetcher = XDataFetcher()
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

#### 4. 配置环境变量

在 GitHub Secrets 中添加：
- Name: `X_API_BEARER_TOKEN`
- Secret: 你的 X API Bearer Token

或在本地 `.env` 文件：
```
X_API_BEARER_TOKEN=your_bearer_token_here
```

### 方案 B: 使用第三方服务（无需 API Key）

#### 使用 Nitter（Twitter 镜像）

```python
import requests
from bs4 import BeautifulSoup

def fetch_x_via_nitter() -> Optional[Dict]:
    """通过 Nitter 获取 X 趋势（无需 API Key）"""
    try:
        # 使用 Nitter 实例（需要找到可用的实例）
        nitter_url = "https://nitter.net"  # 或使用其他实例
        
        # 获取趋势页面
        response = requests.get(f"{nitter_url}/trending", timeout=10)
        response.raise_for_status()
        
        # 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        items = []
        
        # 根据 Nitter 的 HTML 结构提取趋势
        # 注意：Nitter 的 HTML 结构可能变化，需要根据实际情况调整
        trend_items = soup.find_all('div', class_='trend-item')  # 示例选择器
        
        for item in trend_items[:20]:
            title = item.get_text(strip=True)
            link = item.find('a')
            url = link['href'] if link else ""
            
            items.append({
                "title": title,
                "url": f"{nitter_url}{url}" if url else "",
                "mobileUrl": f"{nitter_url}{url}" if url else ""
            })
        
        return {"items": items}
        
    except Exception as e:
        print(f"通过 Nitter 获取 X 趋势失败: {e}")
        return None
```

**注意**：
- Nitter 实例可能不稳定
- HTML 结构可能变化
- 需要定期维护

---

## 📋 添加步骤总结

### 最简单的方法（如果 newsnow 支持）

1. ✅ 编辑 `config/config.yaml`，添加 X 平台
2. ✅ 测试运行
3. ✅ 提交更改

### 需要自己实现的方法

1. ✅ 选择实现方案（X API 或第三方服务）
2. ✅ 创建自定义数据获取器
3. ✅ 修改 `main.py` 集成
4. ✅ 配置环境变量（如需要）
5. ✅ 测试运行
6. ✅ 提交更改

---

## 🧪 测试新平台

### 本地测试

```bash
# 1. 修改配置添加 X 平台
# 2. 运行测试
python main.py

# 3. 检查输出
# - 查看是否成功获取数据
# - 检查 output 目录下的文件
# - 查看控制台日志
```

### 使用 MCP 工具测试

在 AI 客户端中：

```
触发一次只爬取 X 平台的测试，保存到本地
```

---

## ⚠️ 重要提示

### 1. API 限制

- **X API**：有严格的请求频率限制
- **免费层**：每月有限额
- **建议**：合理控制请求频率

### 2. 数据格式

确保返回的数据格式符合要求：

```json
{
  "items": [
    {
      "title": "新闻标题（字符串）",
      "url": "PC端链接",
      "mobileUrl": "移动端链接（可选）"
    }
  ]
}
```

### 3. 语言处理

- X 趋势可能是多语言的
- 关键词匹配需要考虑语言
- 建议在 `frequency_words.txt` 中添加英文关键词

### 4. 时区问题

- X 使用 UTC 时间
- 确保时间显示正确

---

## 📚 相关资源

- [newsnow 项目](https://github.com/ourongxing/newsnow)
- [newsnow 支持的平台列表](https://newsnow.busiyi.world/)
- [X API 文档](https://developer.twitter.com/en/docs)
- [Nitter 项目](https://github.com/zedeus/nitter)
- [TrendRadar 平台配置讨论](https://github.com/sansan0/TrendRadar/issues/95)

---

## 🎯 推荐方案

**优先级排序**：

1. **首选**：检查 newsnow 是否支持，如果支持直接添加配置
2. **次选**：如果 newsnow 不支持，向 newsnow 项目提 Issue 或贡献代码
3. **备选**：自己实现，使用 X API（需要 API Key）
4. **最后**：使用第三方服务（如 Nitter，可能不稳定）

---

**建议先检查 newsnow API 是否支持 X，这是最简单的方法！** 🚀

