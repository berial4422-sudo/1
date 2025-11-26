#!/bin/bash

# GitHub Actions 配置测试脚本
# 用于在本地验证配置是否正确

set -e

echo "🧪 开始测试 GitHub Actions 配置..."
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 测试结果
PASSED=0
FAILED=0

# 测试函数
test_check() {
    local name=$1
    local command=$2
    
    echo -n "测试: $name ... "
    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ 通过${NC}"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}❌ 失败${NC}"
        ((FAILED++))
        return 1
    fi
}

# 1. 检查工作流文件
echo "📋 检查工作流文件..."
test_check "工作流文件存在" "test -f .github/workflows/crawler.yml"
test_check "工作流文件语法" "python3 -c 'import yaml; yaml.safe_load(open(\".github/workflows/crawler.yml\"))'"

# 2. 检查配置文件
echo ""
echo "📋 检查配置文件..."
test_check "config.yaml 存在" "test -f config/config.yaml"
test_check "frequency_words.txt 存在" "test -f config/frequency_words.txt"
test_check "config.yaml 语法" "python3 -c 'import yaml; yaml.safe_load(open(\"config/config.yaml\"))'"

# 3. 检查 Python 依赖
echo ""
echo "📋 检查 Python 依赖..."
test_check "requirements.txt 存在" "test -f requirements.txt"

# Python 版本检查（警告而非失败）
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
echo -n "测试: Python 版本检查 ... "
if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 10 ]; then
    echo -e "${GREEN}✅ 通过 (Python $PYTHON_VERSION)${NC}"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠️  警告 (Python $PYTHON_VERSION，建议 >= 3.10，但 GitHub Actions 会使用 3.11)${NC}"
    ((PASSED++))
fi

# 4. 检查主程序文件
echo ""
echo "📋 检查主程序文件..."
test_check "main.py 存在" "test -f main.py"
test_check "main.py 语法" "python3 -m py_compile main.py"

# 5. 检查必要的目录结构
echo ""
echo "📋 检查目录结构..."
test_check "output 目录存在或可创建" "mkdir -p output && test -d output"

# 6. 检查工作流文件中的关键配置
echo ""
echo "📋 检查工作流配置..."
if grep -q "actions/checkout@v4" .github/workflows/crawler.yml; then
    echo -e "测试: 使用最新 checkout 版本 ... ${GREEN}✅ 通过${NC}"
    ((PASSED++))
else
    echo -e "测试: 使用最新 checkout 版本 ... ${YELLOW}⚠️  警告（使用旧版本）${NC}"
fi

if grep -q "setup-python@v5" .github/workflows/crawler.yml; then
    echo -e "测试: 使用最新 Python setup 版本 ... ${GREEN}✅ 通过${NC}"
    ((PASSED++))
else
    echo -e "测试: 使用最新 Python setup 版本 ... ${YELLOW}⚠️  警告（使用旧版本）${NC}"
fi

if grep -q "timeout-minutes" .github/workflows/crawler.yml; then
    echo -e "测试: 配置了超时保护 ... ${GREEN}✅ 通过${NC}"
    ((PASSED++))
else
    echo -e "测试: 配置了超时保护 ... ${YELLOW}⚠️  警告（未配置超时）${NC}"
fi

# 7. 检查配置文件中的关键设置
echo ""
echo "📋 检查配置文件设置..."
if python3 -c "import yaml; config = yaml.safe_load(open('config/config.yaml')); exit(0 if config.get('crawler', {}).get('enable_crawler', False) else 1)" 2>/dev/null; then
    echo -e "测试: 爬虫功能已启用 ... ${GREEN}✅ 通过${NC}"
    ((PASSED++))
else
    echo -e "测试: 爬虫功能已启用 ... ${YELLOW}⚠️  警告（爬虫未启用）${NC}"
fi

# 总结
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 测试结果汇总"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✅ 通过: $PASSED${NC}"
if [ $FAILED -gt 0 ]; then
    echo -e "${RED}❌ 失败: $FAILED${NC}"
    echo ""
    echo "⚠️  请修复上述错误后重试"
    exit 1
else
    echo -e "${GREEN}❌ 失败: $FAILED${NC}"
    echo ""
    echo "🎉 所有测试通过！配置看起来正确。"
    echo ""
    echo "📝 下一步："
    echo "   1. 提交更改到 GitHub"
    echo "   2. 配置 GitHub Secrets（通知渠道）"
    echo "   3. 在 GitHub Actions 中手动触发测试"
    exit 0
fi

