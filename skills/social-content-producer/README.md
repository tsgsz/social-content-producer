# Social Content Producer Skill

## 安装

Skill 已打包为 `.skill` 文件，可直接使用：

```bash
# 复制到技能目录
cp social-content-producer.skill ~/.openclaw/workspace/skills/

# 或使用 openclaw 安装
openclaw skills install ./social-content-producer.skill
```

## 使用方式

### 基本用法

当你有一个内容需求文档时，告诉 AI：

```
按照 ~/workspace/my-project/requirements.md 生成社交媒体内容
```

AI 会自动：
1. 读取需求文档
2. 生成微信公众号、小红书、抖音内容
3. 进行违禁词检查
4. 使用 nano-banana-pro 生成配图
5. 产出完整的交付包

### 输出结构

```
~/workspace/{project}/out/
├── wechat_article.md          # 微信公众号文章
├── wechat_article.html        # HTML 版本
├── xiaohongshu_note.md        # 小红书笔记
├── xiaohongshu_note.html      # HTML 版本
├── douyin_script.md           # 抖音脚本
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

## 文档规范要求

需求文档应包含：

1. **内容框架示例** - 各平台的内容结构和风格要求
2. **目标受众** - 旅游观众/学生观众/艺术从业者
3. **目标展览/主题** - 具体的展览名称、主题介绍
4. **交付标准** - 违禁词要求、语言风格、Double Check 标准
5. **平台要求** - 微信/小红书/抖音的具体格式要求

参考示例：social_content 项目中的 `AI Testing Case.extracted.txt` 和 `content framework sample.extracted.txt`

## 质量保证

Skill 会自动检查：

- ✅ 违禁词（最、第一、绝对、保证等）
- ✅ AI 腔调（综上所述、本文将、首先其次最后等）
- ✅ 平台调性（微信工具包型、小红书可截图、抖音快节奏）
- ✅ 具体细节（时间、坐标、价格、感官描述）
- ✅ 交付完整性（文案+图片+报告）

## 依赖

- nano-banana-pro skill（生成配图）
- publish skill（发布到公网）
- GEMINI_API_KEY 环境变量

## 示例项目

参考完整示例：
~/workspace/social_content/

生成结果：
- 微信公众号：https://benboerba.tingsongguan.com/file/mplus-deliverable-final/e2137edd7843/out/deliverable.html
- 图片素材：https://benboerba.tingsongguan.com/file/mplus-images/681883a335d8/images/

