# 快速开始指南

## 5分钟上手

### Step 1: 检查环境 (30秒)

```bash
# 检查 API Key
echo $GEMINI_API_KEY

# 如果没有，设置它
export GEMINI_API_KEY="your-key-here"
```

### Step 2: 创建需求文档 (2分钟)

复制模板并填写：

```bash
cp docs/requirements-template.md ~/workspace/my-project/requirements.md
# 用编辑器打开并填写
```

必填内容：
- 目标受众（3类）
- 展览/主题信息（名称+简介）
- 平台框架要求
- 关键词领取设置

### Step 3: 运行生产 (告诉 AI)

```
按照 ~/workspace/my-project/requirements.md 生成社交媒体内容
```

### Step 4: 等待完成 (2-3分钟)

AI 会自动：
1. ✅ 读取需求
2. ✅ 生成内容
3. ✅ 检查违禁词
4. ✅ 生成配图
5. ✅ 组装交付包
6. ✅ 发布到公网

### Step 5: 获取结果

输出路径：`~/workspace/my-project/out/`

公网链接：AI 会提供完整 URL

---

## 示例：M+ 博物馆项目

```bash
# 1. 进入示例项目
cd examples/social_content

# 2. 查看需求文档
cat AI\ Testing\ Case.extracted.txt

# 3. 告诉 AI 生成
cat << 'EOF'
按照 examples/social_content/AI Testing Case.extracted.txt 和 
examples/social_content/content framework sample.extracted.txt 
生成社交媒体内容
EOF

# 4. 查看结果
ls -la out/
# out/wechat_article.md
# out/xiaohongshu_note.md
# out/douyin_script.md
# out/images/ (12张配图)
```

---

## 常见问题

### Q: API Key 在哪里获取？
A: https://aistudio.google.com/app/apikey

### Q: 支持哪些平台？
A: 微信公众号、小红书、抖音

### Q: 生成多少张图片？
A: 12张2K高清图（微信1+小红书8+抖音2+通用1）

### Q: 如何修改已生成的内容？
A: 直接编辑 `out/*.md` 文件，然后重新发布

### Q: 可以批量生成多个项目吗？
A: 目前支持单项目，批量功能开发中

---

## 下一步

- 阅读完整指南: [README.md](README.md)
- 查看示例: [examples/social_content/](examples/social_content/)
- 了解检查清单: [skills/social-content-producer/references/quality-checklist.md](skills/social-content-producer/references/quality-checklist.md)

---

**有问题？** 提交 Issue 或查看故障排除章节
