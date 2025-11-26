"""
TrendRadar Vercel Serverless Function
将爬虫任务包装为 Vercel Serverless Function
通过外部 cron 服务（如 cron-job.org）定时触发

⚠️ 重要限制：
1. Vercel Serverless Functions 执行时间限制：
   - Hobby 计划：10 秒
   - Pro 计划：60 秒
   如果爬虫任务执行时间超过限制，会被强制终止

2. 数据存储：
   - Serverless Functions 是临时环境
   - output 目录无法持久化
   - 建议使用外部存储（Vercel KV、Upstash、数据库等）

3. 定时任务：
   - 免费计划不支持 Cron Jobs
   - 需要使用外部 cron 服务触发

推荐：如果爬虫任务执行时间较长，建议使用 GitHub Actions 或 Docker 部署
"""
import os
import sys
import json
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 设置环境变量
os.environ.setdefault("CONFIG_PATH", "config/config.yaml")


def handler(request):
    """
    Vercel Serverless Function 入口
    
    Vercel 会自动调用这个函数，传入 request 对象
    request 对象包含：
    - method: HTTP 方法
    - path: 请求路径
    - headers: 请求头
    - body: 请求体（如果有）
    """
    try:
        # 导入主程序（延迟导入，避免启动时错误）
        from main import main
        
        # 执行爬虫任务
        main()
        
        # 返回成功响应
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps({
                "success": True,
                "message": "爬虫任务执行成功"
            })
        }
        
    except FileNotFoundError as e:
        # 配置文件错误
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps({
                "success": False,
                "error": f"配置文件错误: {str(e)}",
                "message": "请确保 config/config.yaml 和 config/frequency_words.txt 存在"
            })
        }
        
    except Exception as e:
        # 其他错误
        import traceback
        error_trace = traceback.format_exc()
        
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps({
                "success": False,
                "error": str(e),
                "traceback": error_trace
            })
        }

