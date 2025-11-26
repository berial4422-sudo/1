"""
X (Twitter) 自定义数据获取器

由于 newsnow API 目前不支持 X/Twitter，需要自己实现数据获取。

支持两种方式：
1. X API（需要 Bearer Token，推荐）
2. Nitter 镜像（无需 API，但可能不稳定）
"""
import os
import json
import requests
from typing import Dict, Optional, List
from datetime import datetime


class XDataFetcher:
    """X/Twitter 数据获取器"""
    
    def __init__(self, use_api: bool = True):
        """
        初始化 X 数据获取器
        
        Args:
            use_api: 是否使用 X API（需要 Bearer Token）
                     False 则使用 Nitter 镜像（无需 API）
        """
        self.use_api = use_api
        if use_api:
            self.bearer_token = os.getenv("X_API_BEARER_TOKEN")
            if not self.bearer_token:
                raise ValueError(
                    "使用 X API 需要设置 X_API_BEARER_TOKEN 环境变量\n"
                    "获取方式：https://developer.twitter.com/\n"
                    "或设置 use_api=False 使用 Nitter 镜像（无需 API）"
                )
        else:
            # Nitter 实例列表（如果某个不可用，可以切换）
            self.nitter_instances = [
                "https://nitter.net",
                "https://nitter.it",
                "https://nitter.pussthecat.org",
            ]
            self.current_nitter = self.nitter_instances[0]
    
    def fetch_trending_via_api(self) -> Optional[Dict]:
        """
        通过 X API 获取趋势话题
        
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
            headers = {
                "Authorization": f"Bearer {self.bearer_token}",
            }
            
            # X API v2 获取趋势的方法
            # 注意：X API v2 不直接提供趋势 API，需要使用搜索 API 获取热门内容
            
            items = []
            
            # X API v2 获取热门内容的方法
            # 注意：X API v2 不直接提供趋势 API，使用搜索 API 获取热门推文
            
            # 方法1: 搜索热门话题（使用通用关键词）
            search_queries = [
                "AI OR ChatGPT OR OpenAI",  # AI 相关
                "Bitcoin OR Crypto OR Blockchain",  # 加密货币
                "Tesla OR SpaceX OR Elon Musk",  # 科技/商业
                "breaking news",  # 突发新闻
                "trending",  # 趋势
            ]
            
            for query in search_queries[:3]:  # 限制搜索数量，避免超过 API 限制
                try:
                    url = "https://api.twitter.com/2/tweets/search/recent"
                    params = {
                        "query": f"{query} lang:en -is:retweet",  # 英文、非转推
                        "max_results": 10,  # 每个查询最多10条
                        "tweet.fields": "public_metrics,created_at,entities,text",
                    }
                    
                    response = requests.get(url, headers=headers, params=params, timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        tweets = data.get("data", [])
                        
                        if not tweets:
                            continue
                        
                        for tweet in tweets:
                            text = tweet.get("text", "")
                            tweet_id = tweet.get("id")
                            metrics = tweet.get("public_metrics", {})
                            
                            # 计算互动量
                            engagement = (
                                metrics.get("like_count", 0) +
                                metrics.get("retweet_count", 0) * 2 +
                                metrics.get("reply_count", 0) * 1.5
                            )
                            
                            # 只选择有一定互动量的推文（降低阈值）
                            if engagement > 20:
                                # 提取话题标签
                                entities = tweet.get("entities", {})
                                hashtags = entities.get("hashtags", [])
                                
                                if hashtags:
                                    # 使用话题标签作为标题
                                    title = "#" + " #".join([h.get("tag", "") for h in hashtags[:3]])
                                else:
                                    # 使用推文前80字符作为标题
                                    title = text[:80].replace("\n", " ").replace("\r", " ").strip()
                                    if len(text) > 80:
                                        title += "..."
                                
                                if title and len(title) > 3:  # 确保标题有效
                                    items.append({
                                        "title": title,
                                        "url": f"https://twitter.com/i/web/status/{tweet_id}",
                                        "mobileUrl": f"https://mobile.twitter.com/i/web/status/{tweet_id}",
                                        "engagement": engagement
                                    })
                    elif response.status_code == 429:
                        print("X API: 请求频率限制，建议稍后重试或使用 Nitter 镜像")
                        break
                    elif response.status_code == 401:
                        print("X API: 认证失败，请检查 Bearer Token 是否正确")
                        break
                    else:
                        # 其他错误，继续尝试下一个查询
                        error_data = response.json() if response.text else {}
                        print(f"X API 查询失败 ({response.status_code}): {error_data.get('detail', response.text[:100])}")
                        continue
                    
                    # 避免请求过快（API 限制）
                    import time
                    time.sleep(1)  # 增加延迟，避免触发频率限制
                    
                except requests.exceptions.RequestException as e:
                    # 单个请求失败不影响整体
                    print(f"X API 请求异常: {e}")
                    continue
                except Exception as e:
                    print(f"X API 处理异常: {e}")
                    continue
            
            # 去重（基于标题）
            seen_titles = set()
            unique_items = []
            for item in items:
                title_key = item["title"].lower()
                if title_key not in seen_titles:
                    seen_titles.add(title_key)
                    unique_items.append(item)
            
            # 按互动量排序
            unique_items.sort(key=lambda x: x.get("engagement", 0), reverse=True)
            
            # 移除 engagement 字段（不需要返回）
            for item in unique_items:
                item.pop("engagement", None)
            
            if unique_items:
                return {"items": unique_items[:20]}  # 返回前20条
            else:
                print("X API: 未获取到有效数据，可能 API 权限不足或需要调整搜索策略")
                return None
            
        except requests.exceptions.RequestException as e:
            print(f"X API 请求失败: {e}")
            if hasattr(e.response, 'text'):
                print(f"错误详情: {e.response.text[:200]}")
            return None
        except Exception as e:
            print(f"获取 X 趋势失败: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def fetch_trending_via_nitter(self) -> Optional[Dict]:
        """
        通过 Nitter 镜像获取 X 趋势（无需 API Key）
        
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
            from bs4 import BeautifulSoup
            
            # 尝试不同的 Nitter 实例
            for nitter_url in self.nitter_instances:
                try:
                    response = requests.get(
                        f"{nitter_url}/trending",
                        headers={
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                        },
                        timeout=10
                    )
                    response.raise_for_status()
                    
                    # 解析 HTML
                    soup = BeautifulSoup(response.text, 'html.parser')
                    items = []
                    
                    # Nitter 趋势页面的 HTML 结构（可能变化，需要根据实际情况调整）
                    # 查找趋势项
                    trend_items = soup.find_all(['div', 'span'], class_=lambda x: x and 'trend' in x.lower())
                    
                    if not trend_items:
                        # 尝试其他选择器
                        trend_items = soup.find_all('a', href=lambda x: x and '/hashtag/' in x)
                    
                    for item in trend_items[:20]:
                        text = item.get_text(strip=True)
                        if not text or len(text) < 2:
                            continue
                        
                        # 提取链接
                        link = item.find('a') if item.name != 'a' else item
                        href = link.get('href', '') if link else ''
                        
                        # 构建完整 URL
                        if href.startswith('/'):
                            url = f"{nitter_url}{href}"
                        elif href.startswith('http'):
                            url = href
                        else:
                            url = f"{nitter_url}/hashtag/{text.replace('#', '')}"
                        
                        items.append({
                            "title": text if text.startswith('#') else f"#{text}",
                            "url": url,
                            "mobileUrl": url
                        })
                    
                    if items:
                        self.current_nitter = nitter_url
                        return {"items": items}
                    
                except Exception as e:
                    print(f"Nitter 实例 {nitter_url} 失败: {e}")
                    continue
            
            print("所有 Nitter 实例都不可用")
            return None
            
        except ImportError:
            print("使用 Nitter 需要安装 beautifulsoup4: pip install beautifulsoup4")
            return None
        except Exception as e:
            print(f"通过 Nitter 获取 X 趋势失败: {e}")
            return None
    
    def fetch_trending(self) -> Optional[Dict]:
        """
        获取 X 趋势（自动选择方法）
        
        Returns:
            标准格式的数据字典
        """
        if self.use_api:
            return self.fetch_trending_via_api()
        else:
            return self.fetch_trending_via_nitter()


def test_x_fetcher():
    """测试 X 数据获取器"""
    print("测试 X 数据获取器...")
    
    # 测试 Nitter 方式（无需 API）
    print("\n1. 测试 Nitter 方式（无需 API）...")
    try:
        fetcher = XDataFetcher(use_api=False)
        data = fetcher.fetch_trending()
        if data:
            print(f"✅ 成功获取 {len(data.get('items', []))} 条趋势")
            for i, item in enumerate(data['items'][:5], 1):
                print(f"  {i}. {item['title']}")
        else:
            print("❌ 获取失败")
    except Exception as e:
        print(f"❌ 错误: {e}")
    
    # 测试 API 方式（需要 Bearer Token）
    print("\n2. 测试 X API 方式（需要 Bearer Token）...")
    if os.getenv("X_API_BEARER_TOKEN"):
        try:
            fetcher = XDataFetcher(use_api=True)
            data = fetcher.fetch_trending()
            if data:
                print(f"✅ 成功获取 {len(data.get('items', []))} 条趋势")
                for i, item in enumerate(data['items'][:5], 1):
                    print(f"  {i}. {item['title']}")
            else:
                print("❌ 获取失败")
        except Exception as e:
            print(f"❌ 错误: {e}")
    else:
        print("⚠️  未设置 X_API_BEARER_TOKEN，跳过 API 测试")


if __name__ == "__main__":
    test_x_fetcher()

