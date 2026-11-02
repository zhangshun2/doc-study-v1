#!/usr/bin/env python3
"""Validate the human-first LeetCode derivation contract across all entry points."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
STANDARD = REPO_ROOT / "LeetCode-系统复习" / "05-单题流程" / "单题推导标准卡.md"
TEMPLATE = REPO_ROOT / "LeetCode-系统复习" / "99-Skill" / "非压缩题解模板.md"
DEMO = REPO_ROOT / "LeetCode-系统复习" / "05-单题流程" / "小白读题现场示范.md"
HUMAN_GUIDE = (
    REPO_ROOT / "LeetCode-系统复习" / "05-单题流程" / "人类读题与算法确认.md"
)
REPO_SKILL = (
    REPO_ROOT
    / "LeetCode-系统复习"
    / "99-Skill"
    / "leetcode-steady-java-SKILL.md"
)
INSTALLED_SKILL = Path("/Users/a123456/.codex/skills/leetcode-steady-java/SKILL.md")
AGENTS = REPO_ROOT / "学习文库" / "算法学习" / "AGENTS.md"
WORKBENCH = (
    REPO_ROOT
    / "学习文库"
    / "算法学习"
    / "学习看板"
    / "单题复习工作台.md"
)
SITE_APP = REPO_ROOT / "site" / "assets" / "app.js"


# These are the canonical user-facing questions. Whitespace is normalized before
# comparison so a table cell or wrapped code block may break a line without
# creating a second version of the standard.
QUESTIONS = [
    "我刚读完题，题目到底给了我什么，要我交回什么？",
    "每个字都懂，可一个普通人在纸上第一步做什么？",
    "这个任务里有哪些对象，谁和谁有关系？",
    "照着最笨的办法走一遍，哪一刻什么变了，答案什么时候定下来？",
    "这个笨办法最坏会重复多少，数据范围先排除哪些方向？",
    "带着这个代价重看，哪份信息还会被再次问起，哪批候选会过期，"
    "哪个子问题会复用，哪条顺序不能乱？",
    "这些操作需要什么方向来承担，另一个方向为什么不够？",
    "方向已经定了，状态、更新顺序、不变量和代码怎样逐段对应？",
]

QUESTION_SOURCES = [
    STANDARD,
    TEMPLATE,
    DEMO,
    HUMAN_GUIDE,
    REPO_SKILL,
    INSTALLED_SKILL,
    AGENTS,
    WORKBENCH,
    SITE_APP,
]

STAGE_MAP = [
    "阶段 1：问题 1",
    "阶段 2：问题 2",
    "阶段 3：问题 3 -> 问题 4",
    "阶段 4：问题 5",
    "阶段 5：问题 6",
    "阶段 6：问题 7",
    "阶段 7：问题 8",
]

STAGE_MAP_SOURCES = [STANDARD, TEMPLATE, AGENTS]

STANDARD_HEADINGS = [
    "## 第一阶段：问题 1",
    "## 第二阶段：问题 2",
    "## 第三阶段：问题 3 -> 问题 4",
    "## 第四阶段：问题 5",
    "## 第五阶段：问题 6",
    "## 第六阶段：问题 7",
    "## 第七阶段：问题 8",
]

TEMPLATE_HEADINGS = [
    "## 问题 1：",
    "## 问题 2：",
    "## 问题 3 -> 问题 4：",
    "## 问题 5：",
    "## 问题 6：",
    "## 问题 7：",
    "## 问题 8：",
]

DEMO_HEADINGS = [
    "## 1. 先只读题",
    "## 2. 把题干扩写成一个人能看见的过程",
    "## 3. 清点对象、走人工过程、第一次观察变化",
    "## 4. 读数据范围，只用来缩小候选",
    "## 5. 第二次观察变化",
    "## 6. 比较候选并确认算法方向",
    "## 7. 方向确认后的思维链",
]

REQUIRED_PHRASES = {
    STANDARD: [
        "八个自然问题",
        "下一问必须由上一段留下的空缺产生",
        "照着最笨的办法走一遍",
        "带着这个代价重看",
        "数据范围能做的事情只有两件",
        "候选池不是结论，范围也不是算法暗号",
        "最近端加入、读取和连续删除",
        "完整方向确认句",
        "没有来源的结论不能进入下一步",
        "记忆候选，不是题目事实",
        "没有形成额外假设",
        "没有形成候选",
        "题目事实读错是一票否决",
        "卡住时只留五句",
    ],
    TEMPLATE: [
        "八个自然问题",
        "下一问只能由当前最早缺口产生",
        "范围只缩小候选，不点名算法",
        "第二次变化出现之前不确认方向",
        "没有来源的结论不能进入下一步",
        "记忆候选，不是题目事实",
        "没有形成额外假设",
        "没有形成候选",
        "完整方向确认句",
    ],
    DEMO: [
        "八个自然问题嵌在七个阶段里",
        "没有形成候选",
        "事后校验",
        "第一次变化",
        "第二次变化",
    ],
    HUMAN_GUIDE: [
        "八个自然问题与七个阶段的对应",
        "问题 3 和问题 4 都属于第三阶段",
        "没有形成额外假设",
        "完整方向确认句",
        "卡住时",
    ],
    REPO_SKILL: [
        "八个自然问题",
        "问题 3 和问题 4 不能压成一句“分析题意”",
        "题目事实写错是一票否决",
        "记忆候选，不是题目事实",
        "没有形成额外假设",
        "没有形成候选",
        "完整方向确认句",
    ],
    INSTALLED_SKILL: [
        "八个自然问题",
        "Questions 3 and 4 both belong to stage 3",
        "题目事实写错是一票否决",
        "记忆候选，不是题目事实",
        "没有形成额外假设",
        "没有形成候选",
        "direction-confirmation sentence",
    ],
    AGENTS: [
        "八个自然问题",
        "阶段 3：问题 3 -> 问题 4",
        "不能压缩成一句“分析题意”",
    ],
    WORKBENCH: [
        "八个自然问题",
        "先回答问题 3",
        "再回答问题 4",
        "没有形成额外假设",
        "完整因果句",
    ],
    SITE_APP: [
        "const BEGINNER_QUESTION_CARD",
        "八个自然问题 · 小白现场提问卡",
        "问题 3 和问题 4 同属第三阶段",
        "对象、过程与第一次变化（问题 3 -> 问题 4）",
        "候选池不是结论",
        "完整方向确认句",
        "没有形成候选",
        "renderHumanStageContract",
    ],
}

LEGACY_TERMS = [
    "单屏现场卡",
    "十二句",
    "七个自然问题",
    "七问清单",
    "七项待办",
    "标准确认：十二句连续现场链",
]

FORBIDDEN_IN_RANGE_STAGE = [
    "哈希",
    "双指针",
    "动态规划",
    "单调栈",
    "滑动窗口",
    "二分查找",
    "优先队列",
]


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


def read_text(path: Path, errors: list[str]) -> str | None:
    if not path.is_file():
        errors.append(f"{display_path(path)}: file is missing")
        return None
    return path.read_text(encoding="utf-8")


def check_required_phrases(errors: list[str]) -> None:
    for path, phrases in REQUIRED_PHRASES.items():
        text = read_text(path, errors)
        if text is None:
            continue
        normalized = normalize(text)
        for phrase in phrases:
            if normalize(phrase) not in normalized:
                errors.append(f"{display_path(path)}: missing {phrase}")


def check_question_sequence(errors: list[str]) -> None:
    for path in QUESTION_SOURCES:
        text = read_text(path, errors)
        if text is None:
            continue
        normalized = compact(text)
        positions: list[int] = []
        for index, question in enumerate(QUESTIONS, start=1):
            position = normalized.find(compact(question))
            if position < 0:
                errors.append(
                    f"{display_path(path)}: question {index} is missing or differs "
                    f"from the canonical wording: {question}"
                )
                continue
            positions.append(position)
        if len(positions) == len(QUESTIONS) and positions != sorted(positions):
            errors.append(
                f"{display_path(path)}: the eight questions are not in canonical order"
            )


def check_ordered_markers(
    path: Path, markers: list[str], label: str, errors: list[str]
) -> None:
    text = read_text(path, errors)
    if text is None:
        return
    cursor = 0
    for marker in markers:
        position = text.find(marker, cursor)
        if position < 0:
            errors.append(
                f"{display_path(path)}: {label} marker is out of order or missing: "
                f"{marker}"
            )
            return
        cursor = position + len(marker)


def check_stage_structure(errors: list[str]) -> None:
    check_ordered_markers(STANDARD, STANDARD_HEADINGS, "stage", errors)
    check_ordered_markers(TEMPLATE, TEMPLATE_HEADINGS, "stage", errors)
    check_ordered_markers(DEMO, DEMO_HEADINGS, "stage", errors)

    for path in STAGE_MAP_SOURCES:
        check_ordered_markers(path, STAGE_MAP, "stage map", errors)

    for path in [REPO_SKILL, HUMAN_GUIDE, WORKBENCH]:
        text = read_text(path, errors)
        if text is None:
            continue
        if text.count("| 阶段 3 |") < 2:
            errors.append(
                f"{display_path(path)}: question 3 and question 4 must both be in stage 3"
            )

    site = read_text(SITE_APP, errors)
    if site is not None:
        card_start = site.find("const BEGINNER_QUESTION_CARD = [")
        card_end = site.find("const READING_HARD_GATES", card_start)
        if card_start < 0 or card_end < 0:
            errors.append(
                f"{display_path(SITE_APP)}: cannot isolate BEGINNER_QUESTION_CARD"
            )
        else:
            card = site[card_start:card_end]
            if card.count('index: "') != 8:
                errors.append(
                    f"{display_path(SITE_APP)}: beginner question card must contain "
                    "exactly eight entries"
                )
            if card.count('stage: "阶段 3') != 2:
                errors.append(
                    f"{display_path(SITE_APP)}: question 3 and question 4 must both "
                    "carry stage 3"
                )
            for stage in [4, 5, 6, 7]:
                if f'stage: "阶段 {stage}' not in card:
                    errors.append(
                        f"{display_path(SITE_APP)}: missing stage {stage} question card"
                    )


def check_range_before_second_change(errors: list[str]) -> None:
    standard = read_text(STANDARD, errors)
    if standard is None:
        return

    stage_4_start = standard.find("## 第四阶段：问题 5")
    stage_5_start = standard.find("## 第五阶段：问题 6")
    if stage_4_start < 0 or stage_5_start <= stage_4_start:
        errors.append(
            f"{display_path(STANDARD)}: range stage must precede the second-change stage"
        )
        return

    range_stage = standard[stage_4_start:stage_5_start]
    for term in FORBIDDEN_IN_RANGE_STAGE:
        if term in range_stage:
            errors.append(
                f"{display_path(STANDARD)}: range stage names {term}; it may only "
                "exclude complexity families and leave functional candidates"
            )

    range_evidence = [
        "最坏可以取单调不升的温度",
        "n(n - 1) / 2",
        "不能稳定依赖",
        "候选池不是结论",
    ]
    for phrase in range_evidence:
        if phrase not in range_stage:
            errors.append(
                f"{display_path(STANDARD)}: range stage is missing evidence: {phrase}"
            )

    stage_5_start = standard.find("## 第五阶段：问题 6")
    stage_6_start = standard.find("## 第六阶段：问题 7")
    if stage_6_start <= stage_5_start:
        errors.append(
            f"{display_path(STANDARD)}: second-change stage must precede direction"
        )
        return
    second_change = standard[stage_5_start:stage_6_start]
    for phrase in [
        "重复查询",
        "候选失效",
        "子问题复用",
        "顺序约束",
        "最近端加入、读取、连续删除",
    ]:
        if phrase not in second_change:
            errors.append(
                f"{display_path(STANDARD)}: second-change stage is missing {phrase}"
            )


def check_legacy_language(errors: list[str]) -> None:
    for path in QUESTION_SOURCES:
        text = read_text(path, errors)
        if text is None:
            continue
        for term in LEGACY_TERMS:
            if term in text:
                errors.append(
                    f"{display_path(path)}: legacy competing framework remains: {term}"
                )


def main() -> int:
    errors: list[str] = []
    check_required_phrases(errors)
    check_question_sequence(errors)
    check_stage_structure(errors)
    check_range_before_second_change(errors)
    check_legacy_language(errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Human reading contract passed: 8 questions, 7 ordered stages.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
