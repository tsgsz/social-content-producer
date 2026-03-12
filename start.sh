#!/bin/bash
#
# Social Content Producer - 快速启动脚本
# 用法: ./start.sh ~/path/to/requirements.md

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查参数
if [ $# -eq 0 ]; then
    echo -e "${RED}错误: 请提供需求文档路径${NC}"
    echo "用法: ./start.sh ~/path/to/requirements.md"
    exit 1
fi

REQUIREMENTS_FILE=$1

# 检查文件是否存在
if [ ! -f "$REQUIREMENTS_FILE" ]; then
    echo -e "${RED}错误: 文件不存在: $REQUIREMENTS_FILE${NC}"
    exit 1
fi

echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}  Social Content Producer${NC}"
echo -e "${GREEN}================================${NC}"
echo ""

# 检查环境变量
if [ -z "$GEMINI_API_KEY" ] && [ -z "$GOOGLE_API_KEY" ]; then
    echo -e "${RED}错误: 未设置 GEMINI_API_KEY 或 GOOGLE_API_KEY${NC}"
    echo "请设置环境变量:"
    echo "  export GEMINI_API_KEY='your-key-here'"
    exit 1
fi

echo -e "${GREEN}✓${NC} 环境变量检查通过"

# 检查依赖
echo ""
echo -e "${YELLOW}检查依赖...${NC}"

if ! command -v uv &> /dev/null; then
    echo -e "${RED}✗ uv 未安装${NC}"
    echo "请安装: brew install uv"
    exit 1
fi
echo -e "${GREEN}✓${NC} uv 已安装"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ python3 未安装${NC}"
    exit 1
fi
echo -e "${GREEN}✓${NC} python3 已安装"

# 检查 Skills
SKILL_DIR="$HOME/.openclaw/workspace/skills"
if [ ! -d "$SKILL_DIR/social-content-producer" ]; then
    echo -e "${YELLOW}安装 social-content-producer skill...${NC}"
    cp -r "$(dirname "$0")/skills/social-content-producer" "$SKILL_DIR/"
fi
echo -e "${GREEN}✓${NC} social-content-producer skill 已就绪"

if [ ! -d "$SKILL_DIR/nano-banana-pro" ]; then
    echo -e "${YELLOW}安装 nano-banana-pro skill...${NC}"
    cp -r "$(dirname "$0")/skills/nano-banana-pro" "$SKILL_DIR/"
fi
echo -e "${GREEN}✓${NC} nano-banana-pro skill 已就绪"

if [ ! -d "$SKILL_DIR/publish" ]; then
    echo -e "${YELLOW}安装 publish skill...${NC}"
    cp -r "$(dirname "$0")/skills/publish" "$SKILL_DIR/"
fi
echo -e "${GREEN}✓${NC} publish skill 已就绪"

# 检查 picnan-checker (预装)
if [ ! -d "$SKILL_DIR/picnan-checker" ]; then
    echo -e "${YELLOW}⚠ picnan-checker skill 未找到，敏感词检测需要使用在线工具${NC}"
    echo "  网址: https://www.picnan.com/sensitiveword"
else
    echo -e "${GREEN}✓${NC} picnan-checker skill 已就绪 (图南坊敏感词检测)"
fi"

# 提取项目路径
PROJECT_DIR=$(dirname "$REQUIREMENTS_FILE")
OUT_DIR="$PROJECT_DIR/out"

echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${YELLOW}项目配置:${NC}"
echo -e "  需求文档: $REQUIREMENTS_FILE"
echo -e "  输出目录: $OUT_DIR"
echo -e "${GREEN}================================${NC}"
echo ""

# 创建输出目录
mkdir -p "$OUT_DIR"

echo -e "${YELLOW}准备就绪！请告诉 AI:${NC}"
echo ""
echo -e "  ${GREEN}按照 $REQUIREMENTS_FILE 生成社交媒体内容${NC}"
echo ""
echo "AI 将自动执行:"
echo "  1. 读取需求文档"
echo "  2. 生成微信/小红书/抖音内容"
echo "  3. 违禁词检查 (picnan-checker / 图南坊)"
echo "  4. 生成配图 (nano-banana-pro)"
echo "  5. 组装交付包"
echo "  6. 发布到公网"
echo ""
