#!/usr/bin/env python3
"""Validate that the human-first reading standard stays executable and aligned."""

from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
STANDARD = REPO_ROOT / "LeetCode-系统复习" / "05-单题流程" / "单题推导标准卡.md"
TEMPLATE = REPO_ROOT / "LeetCode-系统复习" / "99-Skill" / "非压缩题解模板.md"
DEMO = REPO_ROOT / "LeetCode-系统复习" / "05-单题流程" / "小白读题现场示范.md"
REPO_SKILL = (
    REPO_ROOT
    / "LeetCode-系统复习"
    / "99-Skill"
    / "leetcode-steady-java-SKILL.md"
)
SITE_APP = REPO_ROOT / "site" / "assets" / "app.js"


CHECKS = [
    (
        STANDARD,
        [
            "我一开始以为",
            "哪条事实让它成立、失效或暂时保留",
            "什么证据会改变判断",
            "逐句扩写不能从结论倒写",
            "第一次变化",
            "第二次变化",
            "候选池不是结论；范围只负责排除和保留方向",
            "方向确认的完整句",
            "最早缺口",
        ],
    ),
    (
        TEMPLATE,
        [
            "我一开始最容易想到的方向",
            "原句",
            "事实 / 推导 / 推测",
            "对象、直接过程和第一次变化",
            "数据范围、操作预算与功能候选",
            "第二次变化：重复劳动和所需操作",
            "候选方向与选择理由",
            "没有这句话，不进入完整实现",
            "状态、初始条件、转移和更新顺序",
        ],
    ),
    (
        DEMO,
        [
            "我一开始以为",
            "哪条事实让我保留疑问",
            "下一个最小问题",
            "什么证据会改变判断",
            "原句",
            "来源",
            "第一次变化",
            "第二次观察变化",
            "方向确认句",
        ],
    ),
    (
        REPO_SKILL,
        [
            "小白现场必须留下的五件事",
            "事实 / 推导 / 推测",
            "题目事实写错是一票否决",
            "第一次变化只说明",
            "第二次变化必须归入",
            "方向确认",
            "最早缺口",
        ],
    ),
    (
        SITE_APP,
        [
            "只读原题事实",
            "把题干扩写成完整生活过程",
            "第一次捕捉变化",
            "读范围，缩小候选方向",
            "第二次捕捉变化",
            "确认算法方向，再进入推导链",
            "定义状态的真实含义",
        ],
    ),
]

ORDERED_CHECKS = [
    (
        STANDARD,
        [
            "| 1. 读题 |",
            "| 2. 扩写 |",
            "| 3. 对象、过程与第一次变化 |",
            "| 4. 范围与候选 |",
            "| 5. 第二次变化 |",
            "| 6. 方向确认 |",
            "| 7. 推导链 |",
        ],
    ),
    (
        TEMPLATE,
        [
            "## 只读原题事实",
            "## 扩写成完整人话过程",
            "## 对象、直接过程和第一次变化",
            "## 数据范围、操作预算与功能候选",
            "## 第二次变化：重复劳动和所需操作",
            "## 候选方向与选择理由",
            "## 状态、初始条件、转移和更新顺序",
        ],
    ),
    (
        DEMO,
        [
            "## 1. 先只读题",
            "## 2. 把题干扩写成一个人能看见的过程",
            "## 3. 清点对象、走人工过程、第一次观察变化",
            "## 4. 读数据范围，只用来缩小候选",
            "## 5. 第二次观察变化",
            "## 6. 比较候选并确认算法方向",
            "## 7. 方向确认后的思维链",
        ],
    ),
    (
        SITE_APP,
        [
            'title: "只读原题事实"',
            'title: "把题干扩写成完整生活过程"',
            'title: "对象、过程与第一次捕捉变化"',
            'title: "读范围，缩小候选方向"',
            'title: "第二次捕捉变化，寻找重复劳动"',
            'title: "确认算法方向，再进入推导链"',
            'title: "定义状态的真实含义"',
        ],
    ),
]


def main() -> int:
    errors: list[str] = []
    for path, required_phrases in CHECKS:
        if not path.is_file():
            errors.append(f"{path.relative_to(REPO_ROOT)}: file is missing")
            continue
        text = path.read_text(encoding="utf-8")
        missing = [phrase for phrase in required_phrases if phrase not in text]
        if missing:
            joined = "、".join(missing)
            errors.append(f"{path.relative_to(REPO_ROOT)}: missing {joined}")

    for path, ordered_phrases in ORDERED_CHECKS:
        if not path.is_file():
            errors.append(f"{path.relative_to(REPO_ROOT)}: file is missing")
            continue
        text = path.read_text(encoding="utf-8")
        cursor = 0
        for phrase in ordered_phrases:
            position = text.find(phrase, cursor)
            if position < 0:
                errors.append(
                    f"{path.relative_to(REPO_ROOT)}: out of order or missing {phrase}"
                )
                break
            cursor = position + len(phrase)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Human reading contract passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
