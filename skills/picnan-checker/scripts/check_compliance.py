#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Social Content Producer - 双重敏感词检测脚本
支持本地词库 + PicNan（图南坊）在线检测
无需额外依赖，使用标准库
"""

import sys
import re
import json
import argparse
import urllib.request
import urllib.error
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

# ============== 本地敏感词库 ==============

FORBIDDEN_WORDS = {
    "极限词": [
        "最好的", "最棒的", "最美的", "最牛的",
        "排名第一", "行业第一", "全网第一", "全港第一",
        "顶级享受", "顶级体验", "极品收藏", "极品体验",
        "极致体验", "极致享受", "极致美学",
        "完美体验", "完美享受", "完美攻略",
        "绝对值得", "绝对推荐", "绝对必看", "绝对要去",
        "保证有效", "保证成功", "保证满意", "保证不踩坑",
        "肯定有效", "肯定值得", "肯定要"
    ],
    "夸大宣传": [
        "闭眼跟", "闭眼入", "闭眼买",
        "必看展览", "必看攻略", "必看景点", "必去景点", "必去之地",
        "错过后悔", "错过等一年", "不看后悔", "不去会死",
        "一生必去", "一生必看", "此生必去", "此生必看",
        "震撼全场", "震撼人心", "震撼体验",
        "颠覆认知", "颠覆想象", "颠覆传统",
        "引领潮流", "引领时尚", "引领行业"
    ],
    "AI腔调": [
        "综上所述", "综上所述，", "综上所述：",
        "本文将", "本文将详细", "本文将介绍", "本文将为你",
        "首先其次最后", "首先，其次，最后", "首先。其次。最后",
        "以下是", "以下是详细", "以下是具体",
        "总而言之", "总而言之，", "总而言之：",
        "归纳如下", "归纳如下：", "归纳如下，",
        "通过本文", "通过这篇文章", "通过本攻略"
    ],
    "绝对化": [
        "所有人都会", "每个人都说", "无一例外", 
        "必然成功", "必然有效", "必然值得",
        "一定有效", "一定成功", "一定值得", "一定要去",
        "肯定有效", "肯定成功", "肯定值得", "肯定要去"
    ],
    "诱导性": [
        "立即购买", "立即行动", "立即下单",
        "马上行动", "马上购买", "马上下单",
        "限时优惠", "限时折扣", "限时活动", "限时",
        "倒计时", "倒计时开始",
        "最后机会", "最后名额", "最后一天",
        "错过等一年", "错过再等一年", "错过就没有了"
    ]
}

REPLACEMENTS = {
    "最": ["更", "比较", "相对", "挺", "蛮"],
    "第一": ["头回", "初次", "优先看", "可以先看"],
    "推荐": ["更适合", "可以先看", "值得看"],
    "完美": ["挺舒服的", "体验不错", "感觉很好"],
    "保证": ["一般来说", "通常", "大概率"],
    "绝对": ["比较", "相对", "大概率"],
    "综上所述": ["", "总之", "简单来说"],
    "本文将": ["", "这篇"],
    "首先其次最后": ["", "第一第二第三"],
    "闭眼跟": ["亲测好用", "值得参考", "可以先试试"],
    "必看": ["值得看", "可以先看", "推荐看"]
}

# ============== PicNan API 配置 ==============

PICNAN_API_URL = "https://www.picnan.com/sensitiveword/detect"
PICNAN_WORDBANKS = ["通用词库", "小红书", "抖音"]  # 默认词库


class LocalChecker:
    """本地敏感词检测器"""
    
    def check(self, text: str, filename: str = "") -> List[Dict]:
        """本地词库检测"""
        issues = []
        lines = text.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            for category, words in FORBIDDEN_WORDS.items():
                for word in words:
                    if word in line:
                        context_start = max(0, line.find(word) - 20)
                        context_end = min(len(line), line.find(word) + len(word) + 20)
                        context = line[context_start:context_end]
                        
                        suggestions = REPLACEMENTS.get(word, ["请使用更中性的表达"])
                        
                        issues.append({
                            "category": category,
                            "word": word,
                            "line": line_num,
                            "context": context,
                            "suggestions": suggestions,
                            "source": "local"
                        })
        
        return issues


class PicNanChecker:
    """PicNan（图南坊）在线检测器 - 使用 urllib"""
    
    def __init__(self, wordbanks: List[str] = None):
        self.wordbanks = wordbanks or PICNAN_WORDBANKS
    
    def check(self, text: str) -> Dict:
        """
        调用 PicNan API 检测敏感词 (使用 urllib)
        """
        try:
            payload = {
                "text": text,
                "wordbanks": self.wordbanks
            }
            
            data = json.dumps(payload).encode('utf-8')
            
            req = urllib.request.Request(
                PICNAN_API_URL,
                data=data,
                headers={
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                    'Origin': 'https://www.picnan.com',
                    'Referer': 'https://www.picnan.com/sensitiveword'
                },
                method='POST'
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                data = json.loads(response.read().decode('utf-8'))
            
            if not data.get("success"):
                return {
                    "success": False,
                    "error": data.get("message", "API返回失败"),
                    "issues": []
                }
            
            # 解析检测结果
            issues = []
            detected_words = data.get("data", {}).get("detectedWords", [])
            
            for word_info in detected_words:
                issues.append({
                    "category": word_info.get("category", "敏感词"),
                    "word": word_info.get("word", ""),
                    "risk_level": word_info.get("level", "未知"),
                    "wordbank": word_info.get("wordbank", ""),
                    "suggestions": REPLACEMENTS.get(word_info.get("word", ""), ["建议修改"]),
                    "source": "picnan"
                })
            
            return {
                "success": True,
                "total_words": data.get("data", {}).get("totalWords", 0),
                "prohibited_count": data.get("data", {}).get("prohibitedCount", 0),
                "sensitive_count": data.get("data", {}).get("sensitiveCount", 0),
                "highlighted_text": data.get("data", {}).get("highlightedText", ""),
                "issues": issues,
                "wordbanks": self.wordbanks
            }
            
        except urllib.error.URLError as e:
            return {
                "success": False,
                "error": f"网络请求失败: {str(e)}",
                "issues": [],
                "fallback": "请使用本地检测模式，或访问 https://www.picnan.com/sensitiveword 手动检测"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"处理失败: {str(e)}",
                "issues": [],
                "fallback": "请使用本地检测模式"
            }


class ComplianceChecker:
    """双重敏感词检测器（本地 + PicNan）"""
    
    def __init__(self, use_picnan: bool = True, wordbanks: List[str] = None):
        self.local_checker = LocalChecker()
        self.picnan_checker = PicNanChecker(wordbanks) if use_picnan else None
        self.use_picnan = use_picnan
    
    def check_file(self, filepath: Path) -> Dict:
        """检测单个文件"""
        text = filepath.read_text(encoding='utf-8')
        
        # 本地检测
        local_issues = self.local_checker.check(text, filepath.name)
        
        # PicNan 在线检测
        picnan_result = None
        picnan_issues = []
        if self.use_picnan and self.picnan_checker:
            picnan_result = self.picnan_checker.check(text)
            if picnan_result.get("success"):
                picnan_issues = picnan_result.get("issues", [])
        
        # 合并结果（去重）
        all_issues = local_issues + picnan_issues
        
        return {
            "file": str(filepath),
            "filename": filepath.name,
            "total_issues": len(all_issues),
            "local_issues": local_issues,
            "picnan_issues": picnan_issues,
            "picnan_result": picnan_result,
            "passed": len(all_issues) == 0
        }
    
    def check_directory(self, dir_path: Path, file_pattern: str = "*.md") -> Dict:
        """检测整个目录"""
        results = []
        
        for md_file in dir_path.glob(file_pattern):
            if md_file.name in ["deliverable.md", "validation_report.md", "validation_report_auto.md"]:
                continue
            result = self.check_file(md_file)
            results.append(result)
        
        total_local = sum(len(r["local_issues"]) for r in results)
        total_picnan = sum(len(r["picnan_issues"]) for r in results)
        total_issues = total_local + total_picnan
        
        return {
            "total_files": len(results),
            "total_issues": total_issues,
            "total_local_issues": total_local,
            "total_picnan_issues": total_picnan,
            "passed": total_issues == 0,
            "results": results,
            "use_picnan": self.use_picnan
        }
    
    def generate_report(self, result: Dict, output_file: Path = None) -> str:
        """生成检测报告"""
        report_lines = [
            "# 敏感词检测报告（双重检测）",
            "",
            f"**检测时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**检测文件数**: {result['total_files']}",
            f"**本地检测问题**: {result['total_local_issues']} 个",
        ]
        
        if result['use_picnan']:
            report_lines.append(f"**PicNan检测问题**: {result['total_picnan_issues']} 个")
        
        report_lines.extend([
            f"**发现问题总数**: {result['total_issues']}",
            f"**检测结果**: {'✅ 通过' if result['passed'] else '⚠️ 需修改'}",
            "",
            "---",
            ""
        ])
        
        if result['passed']:
            report_lines.append("🎉 恭喜！所有文件已通过双重敏感词检测。")
            report_lines.append("")
        else:
            report_lines.append("## 详细问题列表")
            report_lines.append("")
            
            for file_result in result['results']:
                if file_result['total_issues'] > 0:
                    report_lines.append(f"### {file_result['filename']}")
                    
                    # 本地检测问题
                    if file_result['local_issues']:
                        report_lines.append(f"\n**本地检测发现 {len(file_result['local_issues'])} 个问题：**")
                        for issue in file_result['local_issues']:
                            report_lines.append(f"- [{issue['category']}] `{issue['word']}`")
                            report_lines.append(f"  - 行号: {issue['line']}")
                            report_lines.append(f"  - 上下文: ...{issue['context']}...")
                            report_lines.append(f"  - 建议: {' / '.join(issue['suggestions'])}")
                    
                    # PicNan 检测问题
                    if file_result['picnan_issues']:
                        report_lines.append(f"\n**PicNan检测发现 {len(file_result['picnan_issues'])} 个问题：**")
                        for issue in file_result['picnan_issues']:
                            report_lines.append(f"- [{issue['category']}] `{issue['word']}`")
                            report_lines.append(f"  - 风险等级: {issue['risk_level']}")
                            report_lines.append(f"  - 命中词库: {issue['wordbank']}")
                            report_lines.append(f"  - 建议: {' / '.join(issue['suggestions'])}")
                    
                    report_lines.append("")
        
        report_lines.extend([
            "---",
            "",
            "## 检测说明",
            "",
            "本检测包含两部分：",
            "1. **本地词库检测**: 检测极限词、夸大宣传、AI腔调等常见敏感词",
        ])
        
        if result['use_picnan']:
            report_lines.extend([
                "2. **PicNan在线检测**: 调用图南坊敏感词检测API进行实时检测",
                f"   - API地址: {PICNAN_API_URL}",
                f"   - 检测词库: {' / '.join(PICNAN_WORDBANKS)}",
            ])
            
            # 如果有 PicNan 失败的情况
            for file_result in result['results']:
                if file_result.get('picnan_result') and not file_result['picnan_result'].get('success'):
                    report_lines.append(f"\n   ⚠️ **PicNan API 调用失败**: {file_result['picnan_result'].get('error', '未知错误')}")
                    if 'fallback' in file_result['picnan_result']:
                        report_lines.append(f"   - {file_result['picnan_result']['fallback']}")
        else:
            report_lines.append("2. **PicNan在线检测**: 未启用（使用 `--online` 参数启用）")
        
        report_lines.extend([
            "",
            "**注意**: 检测结果仅供参考，最终以平台审核为准。",
            ""
        ])
        
        report = '\n'.join(report_lines)
        
        if output_file:
            output_file.write_text(report, encoding='utf-8')
        
        return report


def main():
    parser = argparse.ArgumentParser(
        description='社交媒体内容敏感词检测（支持本地+PicNan双重检测）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 本地检测（无需网络）
  python3 check_compliance.py .
  
  # 本地+PicNan双重检测
  python3 check_compliance.py . --online
  
  # 生成详细报告
  python3 check_compliance.py . --online -v
  
  # 输出到文件
  python3 check_compliance.py . --online --output report.md
        """
    )
    parser.add_argument('path', help='要检测的文件或目录路径')
    parser.add_argument('-o', '--output', help='输出报告路径')
    parser.add_argument('-v', '--verbose', action='store_true', help='显示详细输出')
    parser.add_argument('--online', action='store_true', help='启用PicNan在线检测')
    parser.add_argument('--wordbanks', nargs='+', default=["通用词库", "小红书", "抖音"],
                       help='PicNan检测词库（默认：通用词库 小红书 抖音）')
    
    args = parser.parse_args()
    
    path = Path(args.path)
    checker = ComplianceChecker(use_picnan=args.online, wordbanks=args.wordbanks)
    
    print("=" * 60)
    print("🔍 敏感词检测（双重检测）")
    print("=" * 60)
    print(f"检测模式: {'本地+PicNan在线' if args.online else '仅本地'}")
    if args.online:
        print(f"PicNan词库: {' / '.join(args.wordbanks)}")
    print("-" * 60)
    
    if path.is_file():
        result = checker.check_file(path)
        results = {
            "total_files": 1,
            "total_issues": result["total_issues"],
            "total_local_issues": len(result["local_issues"]),
            "total_picnan_issues": len(result["picnan_issues"]),
            "passed": result["passed"],
            "results": [result],
            "use_picnan": args.online
        }
    else:
        results = checker.check_directory(path)
    
    # 生成报告
    output_path = Path(args.output) if args.output else None
    report = checker.generate_report(results, output_path)
    
    # 输出结果
    if args.verbose:
        print(report)
    else:
        print(f"\n检测文件: {results['total_files']} 个")
        print(f"本地问题: {results['total_local_issues']} 个")
        if args.online:
            print(f"PicNan问题: {results['total_picnan_issues']} 个")
            # 检查是否有 API 失败
            for r in results['results']:
                if r.get('picnan_result') and not r['picnan_result'].get('success'):
                    print(f"⚠️  PicNan API: {r['picnan_result'].get('error', '调用失败')}")
        print(f"发现问题: {results['total_issues']} 个")
        print(f"检测结果: {'✅ 通过' if results['passed'] else '⚠️ 需修改'}")
        
        if not results['passed']:
            print("\n发现的问题：")
            for file_result in results['results']:
                if file_result['total_issues'] > 0:
                    print(f"\n📄 {file_result['filename']}")
                    
                    if file_result['local_issues']:
                        print("  [本地检测]")
                        for issue in file_result['local_issues'][:3]:  # 最多显示3个
                            print(f"    - [{issue['category']}] {issue['word']}")
                    
                    if file_result['picnan_issues']:
                        print("  [PicNan检测]")
                        for issue in file_result['picnan_issues'][:3]:
                            print(f"    - [{issue['category']}] {issue['word']} (风险: {issue['risk_level']})")
    
    if output_path:
        print(f"\n✅ 报告已保存: {output_path}")
    
    # 返回退出码
    sys.exit(0 if results['passed'] else 1)


if __name__ == '__main__':
    main()
