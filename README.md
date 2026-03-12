# Social Content Producer

自动化社交媒体内容生产系统 - 为微信、小红书、抖音生成完整的内容交付包。

## 快速开始

### 1. 环境要求

**必需环境变量**:
```bash
export GEMINI_API_KEY="your-google-ai-key"
# 或
export GOOGLE_API_KEY="your-google-ai-key"
```

**检查环境**:
```bash
echo $GEMINI_API_KEY
echo $GOOGLE_API_KEY
```

**必需工具**:
- `uv` - Python 包管理器
- `python3` >= 3.10
- `openclaw` CLI

### 2. 安装依赖 Skills

```bash
# 使用 OpenClaw 安装 nano-banana-pro（配图生成）
openclaw skills install @openclaw/nano-banana-pro

# 或手动复制（本项目已包含）
cp -r skills/nano-banana-pro ~/.openclaw/workspace/skills/
```

**注意**:
- `social-content-producer` skill 已在项目 `skills/` 目录中
- `picnan-checker` skill 已包含在项目中，支持本地+API双重检测

### 3. 准备需求文档

创建 `requirements.md` 文件，参考格式：

```markdown
# 项目需求文档

## 目标受众
- 旅游观众（第一次来、追求确定性）
- 学生观众（需要学习方法、作业模板）
- 艺术从业者（关注策展逻辑、方法论）

## 目标展览/主题
1. 展览A：名称 + 简介 + 链接
2. 展览B：名称 + 简介 + 链接
3. 展览C：名称 + 简介 + 链接

## 内容框架

### 微信公众号
- 类型：工具包型 / 短知识型
- 字数：800-1200字
- 结构：痛点共鸣 → 3个方法 → Checklist → CTA

### 小红书
- 风格：可截图保存的工具型内容
- 必含：时间表、路线图、清单、机位图
- 9图骨架：封面→时间表→地图→场景→CTA

### 抖音
- 时长：60-90秒
- 结构：2秒钩子 → 分人群讲解 → CTA
- 必须：开头给结论，每点用作品证明

## 交付标准

### 违禁词检查
- 禁用：最、第一、绝对、保证、完美
- 禁用：综上所述、本文将、首先其次最后
- 禁用：闭眼跟、必看、错过后悔

### "去AI化"要求
- 必须：第一人称经历分享
- 必须：具体坐标（200米、C1出口）
- 必须：感官描述（氛围感、吹吹风）
- 避免：过度总结式语气

### Double Check
- 符合各平台模板结构
- 每条内容2-5个标题备选
- 语言自然，像真人写的
```

### 4. 运行生产流程

```bash
# 告诉 AI：
按照 ~/workspace/my-project/requirements.md 生成社交媒体内容
```

AI 会自动执行以下流程：

#### Step 1: 读取需求
- 解析 requirements.md
- 提取目标受众、展览信息、内容框架

#### Step 2: 生成内容
- 微信公众号文章（3个标题备选）
- 小红书笔记（5个标题+9图骨架）
- 抖音脚本（分镜+口播+字幕）

#### Step 3: 违禁词检查（双重检测）

**本地检测**（无需网络）:
```bash
python3 scripts/check_compliance.py .
```
- 内置敏感词库，离线可用
- 检测极限词、夸大宣传、AI腔调
- 智能识别正常用词

**PicNan API 在线检测**:
```bash
python3 scripts/check_compliance.py . --online
```
- API地址: https://www.picnan.com/sensitiveword/detect
- 实时敏感词库
- 支持通用词库 / 小红书 / 抖音 / B站

**处理命中词**:
- `最` → `更` / `比较`
- `第一` → `头回` / `初次`
- `推荐` → `更适合` / `可以先看`
- `最佳` → `比较适合`

**注意**: PicNan 是第三方工具，不等同于平台官方审核

#### Step 4: 生成配图
使用 `nano-banana-pro` 生成12张2K高清图：
- 微信：1张信息图
- 小红书：8张（封面、时间表、地图、场景等）
- 抖音：2张（封面、资料包）

#### Step 5: 组装交付包
生成完整项目结构到 `out/` 文件夹：
```
out/
├── wechat_article.md          # 微信公众号
├── wechat_article.html        # HTML 版本
├── xiaohongshu_note.md        # 小红书
├── xiaohongshu_note.html      # HTML 版本
├── douyin_script.md           # 抖音
├── douyin_script.html         # HTML 版本
├── validation_report.md       # 审核报告
├── validation_report.html     # HTML 审核报告
├── deliverable.md             # 完整交付文档
├── deliverable.html           # HTML 交付文档
└── images/                    # 12张配图
    ├── wechat_checklist.png
    ├── xiaohongshu_cover.png
    ├── xiaohongshu_timeline.png
    ├── xiaohongshu_map.png
    ├── xiaohongshu_audience.png
    ├── xiaohongshu_cafe.png
    ├── xiaohongshu_transport.png
    ├── xiaohongshu_cta.png
    ├── douyin_thumbnail.png
    ├── mplus_night.png
    ├── zao_wouki_art.png
    └── resource_package.png
```

#### Step 6: 完成
所有交付物已保存到本地 `out/` 文件夹！

**可选**: 如需公网访问链接，使用 `publish` skill（需单独安装）：
```bash
python3 ~/.openclaw/workspace/skills/publish/scripts/publish_gateway.py \
  ./out --sub-dir my-project
```

---

## 项目结构

```
social-content-producer/
├── README.md                    # 本文件
├── QUICKSTART.md               # 5分钟快速上手
├── start.sh                    # 启动脚本
│
├── docs/
│   └── requirements-template.md # 需求文档模板
│
├── skills/                     # 依赖 Skills
│   ├── social-content-producer/  # 主 Skill（必需）
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   ├── forbidden-words.md
│   │   │   ├── platform-guidelines.md
│   │   │   └── quality-checklist.md
│   │   └── scripts/
│   │       └── check_compliance.py
│   │
│   └── nano-banana-pro/         # 配图生成（必需）
│       ├── SKILL.md
│       └── scripts/
│           └── generate_image.py
│
└── examples/
    └── social_content/          # M+博物馆案例
        ├── AI Testing Case.extracted.txt
        ├── content framework sample.extracted.txt
        └── out/                 # 完整交付物示例
```

---

## 核心组件说明

### 1. Social Content Producer Skill

**路径**: `skills/social-content-producer/`

**功能**:
- 读取需求文档并解析
- 生成三平台内容（微信/小红书/抖音）
- 调用 `picnan-checker` 进行敏感词检测
- 协调配图生成
- 组装交付包到 `out/` 文件夹

**参考文档**:
- `references/forbidden-words.md` - 违禁词列表
- `references/platform-guidelines.md` - 平台规范
- `references/quality-checklist.md` - 质量检查清单

**敏感词检测**:
使用 `picnan-checker` skill（图南坊敏感词检测）：
- 网址: https://www.picnan.com/sensitiveword
- 支持词库: 通用词库、小红书、抖音、B站、广告、医疗、政治

### 2. PicNan Checker Skill (敏感词检测)

**路径**: `skills/picnan-checker/`

**功能**: 双重敏感词检测（本地词库 + PicNan API）

**检测方式**:
- **本地检测**: 内置词库，无需网络
  ```bash
  python3 scripts/check_compliance.py .
  ```
- **API检测**: 调用 PicNan 实时词库
  ```bash
  python3 scripts/check_compliance.py . --online
  ```

**本地词库覆盖**:
- 极限词、夸大宣传、AI腔调、绝对化、诱导性

**PicNan API**:
- 地址: https://www.picnan.com/sensitiveword/detect
- 词库: 通用词库、小红书、抖音、B站、广告、医疗、政治

**无需依赖**: 使用 Python 标准库 `urllib`，无需安装 `requests`

### 3. Nano Banana Pro Skill

**路径**: `skills/nano-banana-pro/`

**功能**: 使用 Gemini 3 Pro Image 生成高质量配图

**依赖**: `GEMINI_API_KEY` 或 `GOOGLE_API_KEY` 环境变量

**使用示例**:
```bash
uv run skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "A beautiful sunset at West Kowloon" \
  --filename "sunset.png" \
  --resolution 2K \
  --aspect-ratio 9:16
```

**支持的分辨率**: 1K, 2K, 4K
**支持的宽高比**: 1:1, 2:3, 3:2, 3:4, 4:3, 9:16, 16:9, 21:9

### 4. Publish Skill (可选)

**路径**: `~/.openclaw/workspace/skills/publish/` (系统预装，可选)

**功能**: 将文件发布到公网，生成可访问链接

**注意**: 此 skill 为可选。默认只输出到本地 `out/` 文件夹。

如需发布功能：
```bash
python3 ~/.openclaw/workspace/skills/publish/scripts/publish_gateway.py \
  ./out --sub-dir my-project
```

---

## 质量检查清单

### 内容完整性

#### 微信公众号
- [ ] 3个标题备选
- [ ] 封面文案
- [ ] 痛点共鸣开头
- [ ] 3个方法+示例
- [ ] Checklist（可截图）
- [ ] CTA+关键词领取
- [ ] 1张配图

#### 小红书
- [ ] 5个标题备选
- [ ] 结论前置
- [ ] 完整时间表
- [ ] 8张配图
- [ ] 10个标签
- [ ] 9图骨架说明

#### 抖音
- [ ] 视频标题
- [ ] 0-2秒钩子
- [ ] 3段人群讲解
- [ ] 口播完整稿
- [ ] 2张配图
- [ ] 发布文案

### 合规检查

使用 `picnan-checker` skill（图南坊敏感词检测）：

1. 打开 https://www.picnan.com/sensitiveword
2. 选择词库：通用词库 + 小红书 + 抖音
3. 粘贴文本检测
4. 处理命中词后重新检测

**检查清单**:
- [ ] 无"最"字系列
- [ ] 无"第一"系列
- [ ] 无"绝对/保证"
- [ ] 无"综上所述/本文将"
- [ ] 有第一人称经历
- [ ] 有具体坐标细节
- [ ] 有感官描述

**注意**: PicNan 是第三方工具，检测结果仅供参考

---

## 示例项目

### M+ 博物馆社交媒体内容

**位置**: `examples/social_content/`

**需求文档**:
- `AI Testing Case.extracted.txt` - 内容生产规范
- `content framework sample.extracted.txt` - 平台框架示例

**交付物**:
- 微信公众号文章
- 小红书笔记（9图）
- 抖音脚本
- 12张配图
- 审核报告

---

## 故障排除

### 1. GEMINI_API_KEY 未设置

**错误**: `Error: GEMINI_API_KEY not found`

**解决**:
```bash
export GEMINI_API_KEY="your-key-here"
# 添加到 ~/.env 或 ~/.zshrc 永久生效
```

### 2. uv 未安装

**错误**: `uv: command not found`

**解决**:
```bash
brew install uv
# 或
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. 图片生成失败

**检查**:
- API Key 是否有效
- 网络连接是否正常
- 提示词是否合规

### 4. picnan-checker skill 未找到

**解决**: 敏感词检测直接使用在线工具 https://www.picnan.com/sensitiveword

---

## 开发计划

- [x] 核心内容生成
- [x] 违禁词检查 (picnan-checker)
- [x] 配图生成集成
- [x] 交付包组装 (输出到 out/)
- [ ] 批量项目支持
- [ ] 数据追踪集成
- [ ] 用户反馈收集

---

## 贡献

欢迎提交 Issue 和 PR！

---

## 许可证

MIT License

---

**版本**: v1.0
**创建日期**: 2026-03-12
**作者**: AI Content Production Team
