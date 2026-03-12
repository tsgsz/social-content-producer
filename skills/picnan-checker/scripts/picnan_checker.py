#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PicNan (图南坊) 敏感词检测工具
支持本地词库 + PicNan API 在线检测
"""

import sys
import re
import json
import argparse
import requests
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

# PicNan API 配置
PICNAN_API_URL = "https://www.picnan.com/sensitiveword/detect"
DEFAULT_WORDBANKS = ["通用词库", "小红书", "抖音"]

# 本地敏感词库
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


class PicNanChecker:
    """PicNan（图南坊）敏感词检测器"""
    
    def __init__(self, wordbanks: List[str] = None):
        self.wordbanks = wordbanks or DEFAULT_WORDBANKS
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Origin': 'https://www.picnan.com',
            'Referer': 'https://www.picnan.com/sensitiveword'
        })
    
    def check_local(self, text: str) -> List[Dict]:
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
    
    def check_online(self, text: str) -> Dict:
        """调用 PicNan API 检测敏感词"""
        try:
            payload = {
                "text": text,
                "wordbanks": self.wordbanks
            }
            
            response = self.session.post(
                PICNAN_API_URL,
                json=payload,
                timeout=30
            )
            
            if response.status_code != 200:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}",
                    "issues": []
                }
            
            data = response.json()
            
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
            
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"网络请求失败: {str(e)}",
                "issues": []
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"处理失败: {str(e)}",
                "issues": []
            }
    
    def check_file(self, filepath: Path, use_online: bool = True) -> Dict:
        """检测单个文件"""
        text = filepath.read_text(encoding='utf-8')
        
        # 本地检测
        local_issues = self.check_local(text)
        
        # 在线检测
        online_result = None
        online_issues = []
        if use_online:
            online_result = self.check_online(text)
            if online_result.get("success"):
                online_issues = online_result.get("issues", [])
        
        all_issues = local_issues + online_issues
        
        return {
            "file": str(filepath),
            "filename": filepath.name,
            "total_issues": len(all_issues),
            "local_issues": local_issues,
            "online_issues": online_issues,
            "online_result": online_result,
            "passed": len(all_issues) == 0
        }
    
    def generate_report(self, result: Dict) -> str:
        """生成检测报告"""
        lines = [
            "# PicNan 敏感词检测报告",
            "",
            f"**检测文件**: {result['filename']}",
            f"**检测时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**本地问题**: {len(result['local_issues'])} 个",
            f"**在线问题**: {len(result['online_issues'])} 个",
            f"**检测结果**: {'✅ 通过' if result['passed'] else '⚠️ 需修改'}",
            "",
            "---",
            ""
        ]
        
        if result['local_issues']:
            lines.append("## 本地词库检测")
            for issue in result['local_issues']:
                lines.append(f"- [{issue['category']}] `{issue['word']}` (第{issue['line']}行)")
                lines.append(f"  - 建议: {' / '.join(issue['suggestions'])}")
            lines.append("")
        
        if result['online_issues']:
            lines.append("## PicNan在线检测")
            for issue in result['online_issues']:
                lines.append(f"- [{issue['category']}] `{issue['word']}` (风险: {issue['risk_level']})")
                lines.append(f"  - 命中词库: {issue['wordbank']}")
                lines.append(f"  - 建议: {' / '.join(issue['suggestions'])}")
            lines.append("")
        
        if result['online_result'] and result['online_result'].get('success'):
            lines.append("## 统计信息")
            lines.append(f"- 总字数: {result['online_result']['total_words']}")
            lines.append(f"- 违禁词: {result['online_result']['prohibited_count']} 个")
            lines.append(f"- 敏感词: {result['online_result']['sensitive_count']} 个")
            lines.append("")
        
        return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='PicNan敏感词检测工具')
    parser.add_argument('file', help='要检测的文件路径')
    parser.add_argument('--local-only', action='store_true', help='仅使用本地词库')
    parser.add_argument('--wordbanks', nargs='+', default=DEFAULT_WORDBANKS,
                       help=f'检测词库（默认: {" ".join(DEFAULT_WORDBANKS)}）')
    parser.add_argument('-o', '--output', help='输出报告文件')
    
    args = parser.parse_args()
    
    filepath = Path(args.file)
    if not filepath.exists():
        print(f"错误: 文件不存在 {filepath}")
        sys.exit(1)
    
    checker = PicNanChecker(wordbanks=args.wordbanks)
    result = checker.check_file(filepath, use_online=not args.local_only)
    
    report = checker.generate_report(result)
    print(report)
    
    if args.output:
        Path(args.output).write_text(report, encoding='utf-8')
        print(f"\n✅ 报告已保存: {args.output}")
    
    sys.exit(0 if result['passed'] else 1)


if __name__ == '__main__':
    main()
