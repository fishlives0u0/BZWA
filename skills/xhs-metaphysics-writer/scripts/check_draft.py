#!/usr/bin/env python3
"""Mechanical pre-publish checks for xhs-metaphysics-writer drafts."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ABSOLUTE_PATTERNS = (
    "一定会",
    "百分百",
    "必然会",
    "注定会",
    "必复合",
    "必结婚",
    "必发财",
    "绝对不会",
)
JARGON = ("夫星", "妻星", "夫妻宫", "大运", "流年", "合盘", "暗合", "相冲", "相刑", "相害")
EXPLANATION_MARKERS = ("意味着", "现实", "表现为", "对应", "说明", "要看", "不能只看", "还需要", "并不等于")
NEGATION_MARKERS = ("不等于", "不代表", "不是", "并非", "不能说", "不意味着")


def chinese_count(text: str) -> int:
    return len(re.findall(r"[\u3400-\u9fff]", text))


def normalized_sentences(text: str) -> list[str]:
    parts = re.split(r"[。！？!?\n]+", text)
    return [re.sub(r"\s+", "", p) for p in parts if len(re.sub(r"\s+", "", p)) >= 8]


def unqualified_absolutes(text: str) -> list[str]:
    found = []
    for phrase in ABSOLUTE_PATTERNS:
        for match in re.finditer(re.escape(phrase), text):
            prefix = text[max(0, match.start() - 12) : match.start()]
            if not any(marker in prefix for marker in NEGATION_MARKERS):
                found.append(phrase)
                break
    return found


def main() -> int:
    parser = argparse.ArgumentParser()
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--body")
    source.add_argument("--body-file")
    parser.add_argument("--title", action="append", default=[])
    parser.add_argument("--min-chars", type=int, default=450)
    parser.add_argument("--max-chars", type=int, default=650)
    args = parser.parse_args()

    body = args.body if args.body is not None else Path(args.body_file).read_text(encoding="utf-8")
    count = chinese_count(body)
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]
    long_paragraphs = [i + 1 for i, p in enumerate(paragraphs) if chinese_count(p) > 160]

    sentences = normalized_sentences(body)
    duplicates = sorted({s for s in sentences if sentences.count(s) > 1})
    absolutes = unqualified_absolutes(body)

    jargon_risks = []
    for term in JARGON:
        for match in re.finditer(re.escape(term), body):
            window = body[match.start() : match.start() + 90]
            if not any(marker in window for marker in EXPLANATION_MARKERS):
                jargon_risks.append(term)
                break

    errors = []
    warnings = []
    if not args.min_chars <= count <= args.max_chars:
        errors.append(f"正文中文字数为{count}，目标范围为{args.min_chars}—{args.max_chars}")
    if args.title and not 3 <= len(args.title) <= 5:
        errors.append(f"标题数量为{len(args.title)}，目标为3—5个")
    if long_paragraphs:
        warnings.append(f"段落{long_paragraphs}超过160个中文字，建议拆分")
    if duplicates:
        errors.append(f"发现重复句：{duplicates}")
    if absolutes:
        errors.append(f"发现绝对化表达：{absolutes}")
    if jargon_risks:
        warnings.append(f"这些术语附近可能缺少现实解释或边界：{sorted(set(jargon_risks))}")
    if len(paragraphs) < 3:
        warnings.append("正文少于3个自然段，手机阅读节奏可能偏密")

    result = {
        "status": "PASS" if not errors else "FAIL",
        "chinese_characters": count,
        "title_count": len(args.title),
        "paragraph_count": len(paragraphs),
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
