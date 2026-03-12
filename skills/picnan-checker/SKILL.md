---
name: picnan-checker
description: 社交媒体内容敏感词检测工具，支持本地词库 + PicNan（图南坊）API 在线双重检测。用于检测微信、小红书、抖音等平台内容的违禁词、夸大宣传和AI腔调。无需额外依赖，使用 Python 标准库。
---

# PicNan Checker

社交媒体内容敏感词检测工具，支持**本地词库 + PicNan（图南坊）API 在线双重检测**。

## 功能特性

- ✅ **本地检测**: 内置敏感词库，**无需网络**即可检测
- ✅ **在线检测**: 调用 PicNan API，获取**实时敏感词库**
- ✅ **双重检测**: 本地+在线双重检测，结果互补
- ✅ **无需依赖**: 使用 Python 标准库 `urllib`，无需安装 `requests`
- ✅ **多平台**: 支持微信、小红书、抖音、B站等平台
- ✅ **智能识别**: 自动识别正常用词（如"第一次"），避免误报

## 安装

本项目已包含此 skill，无需额外安装。

如需在其他项目使用：
```bash
cp -r skills/picnan-checker ~/.openclaw/workspace/skills/
```

## 使用方法

### 1. 双重检测（推荐）

```bash
# 检测当前目录所有 Markdown 文件
python3 scripts/check_compliance.py . --online

# 生成详细报告
python3 scripts/check_compliance.py . --online -v

# 输出到文件
python3 scripts/check_compliance.py . --online --output report.md
```

### 2. 仅本地检测（无需网络）

```bash
python3 scripts/check_compliance.py .
```

### 3. 检测单个文件

```bash
python3 scripts/picnan_checker.py wechat_article.md --online
```

### 4. 自定义词库

```bash
python3 scripts/check_compliance.py . --online --wordbanks 通用词库 小红书 抖音 B站 广告
```

## API 检测说明

### PicNan API

- **API 地址**: `https://www.picnan.com/sensitiveword/detect`
- **请求方法**: POST
- **Content-Type**: application/json
- **请求体**:
```json
{
  "text": "待检测文本",
  "wordbanks": ["通用词库", "小红书", "抖音"]
}
```

### 响应格式

```json
{
  "success": true,
  "data": {
    "totalWords": 100,
    "prohibitedCount": 2,
    "sensitiveCount": 3,
    "detectedWords": [
      {
        "word": "最好",
        "category": "极限词",
        "level": "高",
        "wordbank": "通用词库"
      }
    ]
  }
}
```

## 检测词库

### 本地词库

| 类别 | 示例 |
|------|------|
| **极限词** | 最好的、排名第一、顶级享受、极致体验、完美攻略 |
| **夸大宣传** | 闭眼跟、必看攻略、错过后悔、一生必去、颠覆认知 |
| **AI腔调** | 综上所述、本文将、首先其次最后、归纳如下 |
| **绝对化** | 所有人都会、必然成功、一定有效、肯定值得 |
| **诱导性** | 立即购买、限时优惠、倒计时、最后机会 |

### PicNan 在线词库

- 通用词库
- 小红书
- 抖音
- B站
- 广告
- 医疗
- 政治

## 检测结果示例

### 本地检测结果

```
[极限词] `最好`
- 行号: 15
- 上下文: ...这是最好的展览...
- 建议: 更 / 比较 / 相对
```

### PicNan API 检测结果

```
[极限词] `最好` (风险: 高)
- 命中词库: 通用词库
- 建议: 更 / 比较 / 相对
```

## 替换建议

| 原词 | 替换建议 |
|------|----------|
| 最 | 更、比较、相对、挺、蛮 |
| 第一 | 头回、初次、优先看 |
| 完美 | 挺舒服的、体验不错 |
| 绝对 | 比较、相对、大概率 |
| 综上所述 | 总之、简单来说 |
| 闭眼跟 | 亲测好用、值得参考 |
| 必看 | 值得看、推荐看 |
| 推荐 | 更适合、可以先看 |
| 最佳 | 比较适合、位置不错 |

## 使用建议

1. **首次检测**: 使用 `check_compliance.py .` 进行本地快速检测
2. **二次验证**: 使用 `check_compliance.py . --online` 进行双重检测
3. **批量处理**: 使用 `check_compliance.py` 检测整个目录
4. **单文件检测**: 使用 `picnan_checker.py` 检测单个文件
5. **API 失败**: 如果 PicNan API 调用失败，脚本会自动提示使用本地检测或手动访问网站

## 故障排除

### API 调用失败

**症状**: `网络请求失败` 或 `HTTP Error`

**解决**:
- 检查网络连接
- 使用本地检测模式: `python3 scripts/check_compliance.py .`
- 或手动访问: https://www.picnan.com/sensitiveword

### 误报处理

PicNan 可能会将一些正常词汇标记为敏感词（如"微信"、"脚本"、"群"等），需要人工判断：
- 上下文正常的平台名称（如"微信小程序"）可保留
- 专业术语（如"视频脚本"）可保留
- 社交场景正常用词（如"评论区"）可保留

## 注意事项

1. **第三方工具**: PicNan 是第三方工具，不等同于平台官方审核
2. **仅供参考**: 检测结果仅供参考，最终以平台审核为准
3. **网络依赖**: 在线检测需要网络连接
4. **API 限制**: 频繁调用可能会被限制，请合理使用

## 更新日志

### v1.0 (2026-03-12)

- 初始版本
- 支持本地词库检测（无需依赖）
- 支持 PicNan API 在线检测（使用 urllib）
- 支持双重检测模式
- 无需安装 requests，使用 Python 标准库

## 参考链接

- PicNan 敏感词检测: https://www.picnan.com/sensitiveword
- API 地址: https://www.picnan.com/sensitiveword/detect
- 小红书社区规范: https://www.xiaohongshu.com/
- 抖音社区规范: https://www.douyin.com/

---

**作者**: AI Content Production Team  
**版本**: v1.0  
**日期**: 2026-03-12
