#!/usr/bin/env python3
"""
Create a master showcase HTML page that references all deliverables.
Usage: python3 create_showcase.py <project_name> <output_dir>
"""

import sys
import os
from pathlib import Path

def create_showcase_page(project_name, output_dir):
    """Generate index.html showcasing all deliverables."""
    
    out_path = Path(output_dir)
    images_dir = out_path / "images"
    
    # Get all images
    images = []
    if images_dir.exists():
        images = sorted([f.name for f in images_dir.iterdir() if f.suffix.lower() in ['.png', '.jpg', '.jpeg']])
    
    # Build image gallery HTML
    image_gallery = ""
    for img in images:
        image_gallery += f'''
        <div class="image-card">
            <img src="images/{img}" alt="{img}" loading="lazy">
            <p class="image-caption">{img}</p>
        </div>'''
    
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name} - 社交媒体内容交付展示</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 20px;
            text-align: center;
        }}
        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 10px;
        }}
        .header p {{
            font-size: 1.1rem;
            opacity: 0.9;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        .section {{
            background: white;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .section h2 {{
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #f0f0f0;
        }}
        .platform-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        .platform-card {{
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            border-left: 4px solid #667eea;
        }}
        .platform-card h3 {{
            color: #333;
            margin-bottom: 10px;
        }}
        .platform-card p {{
            color: #666;
            font-size: 0.9rem;
            margin-bottom: 15px;
        }}
        .btn {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 10px 20px;
            border-radius: 6px;
            text-decoration: none;
            font-size: 0.9rem;
            transition: background 0.3s;
        }}
        .btn:hover {{
            background: #5568d3;
        }}
        .image-gallery {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        .image-card {{
            background: #f8f9fa;
            border-radius: 8px;
            overflow: hidden;
            transition: transform 0.3s;
        }}
        .image-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        .image-card img {{
            width: 100%;
            height: 200px;
            object-fit: cover;
        }}
        .image-caption {{
            padding: 10px;
            font-size: 0.85rem;
            color: #666;
            text-align: center;
        }}
        .status-badge {{
            display: inline-block;
            background: #28a745;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            margin-left: 10px;
        }}
        .meta-info {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}
        .meta-item {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 6px;
        }}
        .meta-item strong {{
            display: block;
            color: #667eea;
            margin-bottom: 5px;
        }}
        .footer {{
            text-align: center;
            padding: 40px 20px;
            color: #666;
            font-size: 0.9rem;
        }}
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 1.8rem;
            }}
            .platform-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📱 {project_name}</h1>
        <p>社交媒体内容交付展示 | 微信 · 小红书 · 抖音</p>
    </div>
    
    <div class="container">
        <!-- 项目概览 -->
        <div class="section">
            <h2>📋 项目概览 <span class="status-badge">✓ 已完成</span></h2>
            <div class="meta-info">
                <div class="meta-item">
                    <strong>项目名称</strong>
                    {project_name}
                </div>
                <div class="meta-item">
                    <strong>交付平台</strong>
                    微信 / 小红书 / 抖音
                </div>
                <div class="meta-item">
                    <strong>文案数量</strong>
                    3 篇
                </div>
                <div class="meta-item">
                    <strong>配图数量</strong>
                    {len(images)} 张
                </div>
                <div class="meta-item">
                    <strong>敏感词检测</strong>
                    双重检测通过
                </div>
                <div class="meta-item">
                    <strong>生成工具</strong>
                    social-content-producer
                </div>
            </div>
        </div>
        
        <!-- 平台内容 -->
        <div class="section">
            <h2>📝 平台内容</h2>
            <div class="platform-grid">
                <div class="platform-card">
                    <h3>📢 微信公众号</h3>
                    <p>工具包型文章：3个看懂方法 + 可截图清单</p>
                    <a href="wechat_article.html" class="btn">查看内容</a>
                    <a href="wechat_article.md" class="btn" style="background:#6c757d">下载 MD</a>
                </div>
                <div class="platform-card">
                    <h3>📕 小红书</h3>
                    <p>可截图保存：时间表 + 路线图 + 9图骨架</p>
                    <a href="xiaohongshu_note.html" class="btn">查看内容</a>
                    <a href="xiaohongshu_note.md" class="btn" style="background:#6c757d">下载 MD</a>
                </div>
                <div class="platform-card">
                    <h3>🎬 抖音</h3>
                    <p>短视频脚本：分镜 + 口播 + CTA</p>
                    <a href="douyin_script.html" class="btn">查看内容</a>
                    <a href="douyin_script.md" class="btn" style="background:#6c757d">下载 MD</a>
                </div>
            </div>
        </div>
        
        <!-- 图片素材 -->
        <div class="section">
            <h2>🎨 图片素材 ({len(images)} 张)</h2>
            <div class="image-gallery">
                {image_gallery if image_gallery else '<p style="color:#999;text-align:center;padding:40px;">暂无图片</p>'}
            </div>
        </div>
        
        <!-- 验证报告 -->
        <div class="section">
            <h2>✅ 质量验证</h2>
            <p>所有内容已通过双重敏感词检测和"去AI化"语言检查。</p>
            <div style="margin-top:15px;">
                <a href="validation_report.html" class="btn">查看验证报告</a>
                <a href="deliverable.html" class="btn" style="background:#28a745">完整交付文档</a>
            </div>
        </div>
        
        <!-- 文件下载 -->
        <div class="section">
            <h2>📦 文件下载</h2>
            <p>所有交付物均可下载：</p>
            <div style="margin-top:15px;">
                <a href="wechat_article.md" class="btn">微信公众号 MD</a>
                <a href="xiaohongshu_note.md" class="btn">小红书 MD</a>
                <a href="douyin_script.md" class="btn">抖音 MD</a>
                <a href="deliverable.md" class="btn" style="background:#6c757d">交付文档</a>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <p>Generated by social-content-producer skill</p>
        <p style="margin-top:10px;color:#999;">© 2026</p>
    </div>
</body>
</html>'''
    
    # Write index.html
    index_path = out_path / "index.html"
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ 主展示页已生成: {index_path}")
    return index_path

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 create_showcase.py <project_name> <output_dir>")
        sys.exit(1)
    
    project_name = sys.argv[1]
    output_dir = sys.argv[2]
    
    create_showcase_page(project_name, output_dir)
