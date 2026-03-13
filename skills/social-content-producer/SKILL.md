---
name: social-content-producer
description: Automated social media content production for WeChat, Xiaohongshu (Little Red Book), and Douyin. Reads requirement documents, generates platform-specific content with forbidden word checking, creates visual assets using nano-banana-pro, and produces complete deliverable packages. Use when the user provides a content requirement document and asks to generate social media content for Chinese platforms (微信/小红书/抖音), or when needing end-to-end content production with compliance checking and visual assets.
---

# Social Content Producer

Automated social media content production system for Chinese platforms.

## Overview

This skill automates the complete workflow from requirement document to final deliverable:
1. Read and parse requirement documents
2. Generate platform-specific content (WeChat/Xiaohongshu/Douyin)
3. Check for forbidden words and AI-toned language
4. Generate visual assets using nano-banana-pro
5. Produce complete deliverable package with audit reports

## Workflow

### Step 1: Read Requirements

Read the provided requirement document(s) in the project directory. Look for:
- Content framework samples
- Platform-specific requirements
- Target audience definitions
- Delivery standards
- Forbidden word guidelines

### Step 2: Generate Platform Content

Generate content for each platform based on requirements:

**WeChat Article**:
- 3 title alternatives
- Cover copy and summary
- Structured body with hooks
- Practical checklists/tools
- CTA with keyword redemption

**Xiaohongshu Note**:
- 5 title alternatives
- Conclusion-first opening
- Detailed schedule/itinerary
- 9-image skeleton with descriptions
- Hashtags and engagement hooks

**Douyin Script**:
- Video title
- 60-90 second storyboard
- Shot-by-shot breakdown
- Complete voiceover script
- Subtitle design notes
- Posting caption with hashtags

### Step 3: Forbidden Word Check (via picnan-checker)

使用 `picnan-checker` skill 进行双重敏感词检测：

**1. 本地检测** (无需网络):
```bash
python3 ../../picnan-checker/scripts/check_compliance.py .
```
- 调用 picnan-checker 本地词库
- 检测极限词、夸大宣传、AI腔调
- 智能识别正常用词

**2. PicNan API 在线检测**:
```bash
python3 ../../picnan-checker/scripts/check_compliance.py . --online
```
- 调用 picnan-checker API 检测
- API地址: https://www.picnan.com/sensitiveword/detect
- 词库: 通用词库 / 小红书 / 抖音

**处理命中词**:
- `最` -> `更` / `比较`
- `第一` -> `头回` / `初次`
- `推荐` -> `更适合`
- `最佳` -> `比较适合`
- 高风险词 -> 改写为中性描述

**注意**: PicNan 是第三方工具，不等同于平台官方审核

**依赖**: 需要安装 `picnan-checker` skill:
```bash
cp -r ../../picnan-checker ~/.openclaw/workspace/skills/
```

### Step 4: Generate Visual Assets

Use nano-banana-pro to create platform-specific images:

**WeChat**:
- 1 infographic checklist (4:5 aspect ratio)

**Xiaohongshu** (9 images):
- Cover image (sunset/architectural, 9:16)
- Timeline infographic (9:16)
- Map/location guide (9:16)
- Audience comparison (9:16)
- Cafe/rest scene (9:16)
- Transportation guide (9:16)
- CTA end card (9:16)
- Night scene (9:16)
- Additional content image (9:16)

**Douyin**:
- Video thumbnail (16:9)
- Resource package preview (16:9)

### Step 5: Create Deliverables

Generate organized output:

```
out/
├── wechat_article.md          # WeChat content
├── wechat_article.html        # Styled HTML version
├── xiaohongshu_note.md        # Xiaohongshu content
├── xiaohongshu_note.html      # Styled HTML version
├── douyin_script.md           # Douyin content
├── douyin_script.html         # Styled HTML version
├── validation_report.md       # Audit report
├── validation_report.html     # Styled audit report
├── deliverable.md             # Complete package documentation
├── deliverable.html           # Complete package (HTML)
└── images/                    # 12 visual assets
```

### Step 6: Validation Report

Create comprehensive audit report including:
- Forbidden word check results
- "De-AI-fication" language check
- Platform tone compliance
- Specific detail verification
- Delivery completeness checklist

### Optional: Publish to Web

If the user needs public URLs, use the `publish` skill:

```bash
python3 ~/.openclaw/workspace/skills/publish/scripts/publish_gateway.py \
  ~/workspace/my-project/out --sub-dir my-project
```

This is optional. By default, all deliverables are saved to the local `out/` folder.

## Usage

### Basic Usage

```
User: 帮我按照 ~/workspace/my-project/requirements.md 生成社交媒体内容
```

The skill will:
1. Read requirements.md
2. Generate all platform content
3. Run compliance checks
4. Create visual assets
5. Produce complete deliverable

### With Custom Output Path

Content is generated in `~/workspace/{project}/out/` by default.

### Quality Standards

**Content must include**:
- Specific time details (e.g., "10:30-18:30")
- Spatial coordinates (e.g., "200米，看到长椅")
- Price information where applicable
- Sensory descriptions

**Content must avoid**:
- Superlatives without evidence
- AI-sounding summaries
- Empty marketing language
- Mechanical structures

## Reference Files

- `references/forbidden-words.md` - Complete forbidden word list
- `references/platform-guidelines.md` - Platform-specific requirements
- `references/quality-checklist.md` - Delivery quality standards

Read these references when generating content to ensure compliance.

## Scripts

- `scripts/generate_content.py` - Content generation helper (optional)
- `scripts/create_deliverable.py` - Package assembly (optional)

**Note**: Forbidden word checking is handled by `picnan-checker` skill, not local scripts.

Scripts are executed via `uv run` with appropriate dependencies.

## Integration

This skill integrates with:
- **`picnan-checker`** skill for forbidden word detection (required)
- **`nano-banana-pro`** skill for image generation (required)
- `publish` skill for web deployment (optional)
- Standard file operations for deliverable organization

### Dependencies

1. **picnan-checker** (required):
   ```bash
   cp -r ../../picnan-checker ~/.openclaw/workspace/skills/
   ```
   Used for forbidden word detection (local + API).

2. **nano-banana-pro** (required):
   ```bash
   cp -r ../../nano-banana-pro ~/.openclaw/workspace/skills/
   ```
   Used for image generation.

3. **publish** (optional):
   ```bash
   # Already installed in ~/.openclaw/workspace/skills/
   ```
   Used for web deployment.

## Example Output Structure

See `assets/example-deliverable/` for a complete example package.

