# X API 故障排查指南

## 🔍 常见问题

### 问题 1: API 返回 400 Bad Request

**可能原因**：
- 查询参数格式错误
- API 端点不正确
- Bearer Token 格式问题

**解决方法**：
1. 检查 Bearer Token 是否正确（URL 编码问题）
2. 简化查询参数
3. 查看错误详情

### 问题 2: API 返回 401 Unauthorized

**可能原因**：
- Bearer Token 无效或已过期
- Token 权限不足

**解决方法**：
1. 在 X Developer Portal 中验证 Token
2. 重新生成 Bearer Token
3. 检查 API 权限设置

### 问题 3: API 返回 429 Too Many Requests

**可能原因**：
- 请求频率超过限制
- 免费层额度用完

**解决方法**：
1. 降低请求频率
2. 增加请求间隔
3. 考虑使用 Nitter 镜像作为备选

### 问题 4: 获取不到数据

**可能原因**：
- 搜索策略不合适
- 互动量阈值过高
- API 权限不足

**解决方法**：
1. 降低互动量阈值
2. 调整搜索关键词
3. 使用 Nitter 镜像作为备选

---

## 🔧 优化建议

### 1. 使用 Nitter 作为备选

如果 X API 有问题，系统会自动降级到 Nitter：

```python
# 在 main.py 中已实现自动降级
if id_value in ["x", "twitter"]:
    try:
        use_api = bool(os.getenv("X_API_BEARER_TOKEN"))
        x_fetcher = XDataFetcher(use_api=use_api)
        # 如果 API 失败，可以手动切换到 Nitter
        # x_fetcher = XDataFetcher(use_api=False)
    except:
        pass
```

### 2. 调整搜索策略

编辑 `custom_sources/x_fetcher.py`，修改搜索关键词：

```python
search_queries = [
    "你关心的关键词1",
    "你关心的关键词2",
    # ...
]
```

### 3. 调整互动量阈值

```python
# 降低阈值，获取更多内容
if engagement > 20:  # 原来是 50 或 100
    # ...
```

---

## 🧪 测试 API 连接

### 简单测试

```bash
export X_API_BEARER_TOKEN="your_token"
python3 -c "
import requests
import os
headers = {'Authorization': f'Bearer {os.getenv(\"X_API_BEARER_TOKEN\")}'}
r = requests.get('https://api.twitter.com/2/tweets/search/recent', 
                 headers=headers, 
                 params={'query': 'AI', 'max_results': 5}, 
                 timeout=10)
print('状态码:', r.status_code)
print('响应:', r.json() if r.status_code == 200 else r.text[:200])
"
```

### 完整测试

```bash
python custom_sources/x_fetcher.py
```

---

## 📚 X API 文档

- [X API v2 文档](https://developer.twitter.com/en/docs/twitter-api)
- [搜索 API 参考](https://developer.twitter.com/en/docs/twitter-api/tweets/search/introduction)
- [API 限制说明](https://developer.twitter.com/en/docs/rate-limits)

---

## 🔄 备选方案

如果 X API 不可用，系统会自动使用 Nitter 镜像（无需 API Key）。

**切换方法**：
- 不设置 `X_API_BEARER_TOKEN` 环境变量
- 或设置 `use_api=False`


