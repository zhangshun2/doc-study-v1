#!/usr/bin/env python3
"""Validate the human-first LeetCode derivation contract across all entry points."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
STANDARD = REPO_ROOT / "LeetCode-系统复习" / "05-单题流程" / "单题推导标准卡.md"
TEMPLATE = REPO_ROOT / "LeetCode-系统复习" / "99-Skill" / "非压缩题解模板.md"
REAL_PROBLEM_TEMPLATE = (
    REPO_ROOT / "学习文库" / "算法学习" / "99-模板" / "题解.md"
)
TWO_SUM = (
    REPO_ROOT
    / "学习文库"
    / "算法学习"
    / "题目"
    / "数组与哈希"
    / "1-Two-Sum.md"
)
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
RECORD_TEMPLATE = (
    REPO_ROOT
    / "LeetCode-系统复习"
    / "06-学习记录"
    / "单题复习记录模板.md"
)
SITE_APP = REPO_ROOT / "site" / "assets" / "app.js"
SCORE_GUIDE = (
    REPO_ROOT / "LeetCode-系统复习" / "05-单题流程" / "人类推导样板与评分.md"
)


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
    "## 3. 记录当前困惑和新增证据，再走对象、人工过程和第一次变化",
    "## 4. 读数据范围，只用来缩小候选",
    "## 5. 第二次观察变化",
    "## 6. 比较候选并确认算法方向",
    "## 7. 方向确认后的思维链",
]

REAL_PROBLEM_HEADINGS = [
    "## 阶段 1：",
    "## 阶段 2：",
    "## 阶段 3：",
    "## 阶段 4：",
    "## 阶段 5：",
    "## 阶段 6：",
    "## 阶段 7：",
]

REQUIRED_PHRASES = {
    STANDARD: [
        "八个自然问题",
        "现场交接表",
        "我刚得到",
        "但它还不能说明",
        "所以现在只问",
        "下一问必须由上一段留下的空缺产生",
        "身份由什么决定",
        "为什么还能继续",
        "答案产生时刻",
        "被排除的复杂度家族",
        "Java 代码位置",
        "对应反例",
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
        "新手的起步标准",
        "先做一个动作，不靠灵感",
        "新手的起步动作表",
        "推理转折必须可见",
        "当前最早空缺",
        "我实际做的纸面动作",
        "做完后多出的证据",
        "没有发生转折",
        "题目事实读错是一票否决",
        "卡住时只留五句",
        "此刻唯一该问的问题",
        "第一件实际纸面动作",
        "做完后只多出的证据",
        "禁止提前出现",
        "下一问如何自然产生",
    ],
    TEMPLATE: [
        "八个自然问题",
        "现场交接表",
        "我刚得到",
        "但它还不能说明",
        "所以现在只问",
        "下一问只能由当前最早缺口产生",
        "范围只缩小候选，不点名算法",
        "第二次变化出现之前不确认方向",
        "没有来源的结论不能进入下一步",
        "记忆候选，不是题目事实",
        "没有形成额外假设",
        "没有形成候选",
        "现场动作记录",
        "当前最早空缺",
        "第一件实际做的纸面动作",
        "做完后多出的证据",
        "推理转折记录",
        "我原来看到或以为",
        "没有发生转折",
        "完整方向确认句",
        "Java 代码位置",
        "对应反例",
    ],
    REAL_PROBLEM_TEMPLATE: [
        "现场推导",
        "事后校验",
        "前六个阶段",
        "此刻真实候选：没有形成候选",
        "没有形成额外假设",
        "变化前",
        "触发事件",
        "变化后",
        "答案产生时刻",
        "重复查询",
        "候选失效",
        "子问题复用",
        "顺序约束",
        "完整方向确认句",
        "Java 代码位置",
        "对应反例",
        "官方额外提示（答案侧）",
    ],
    TWO_SUM: [
        "事后校验",
        "此刻真实候选：没有形成候选",
        "没有形成额外假设",
        "变化前",
        "触发事件",
        "变化后",
        "答案产生时刻",
        "重复查询",
        "顺序要求",
        "完整方向确认句",
        "先查询历史",
        "后加入当前值",
        "Java 代码位置",
        "对应反例",
        "官方额外提示（答案侧）",
    ],
    RECORD_TEMPLATE: [
        "现场动作记录",
        "当前最早空缺",
        "第一件实际做的纸面动作",
        "做完后多出的证据",
        "推理转折记录",
        "没有形成候选",
        "没有发生真实转折",
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
        "现场交接表",
        "我刚得到",
        "但它还不能说明",
        "所以现在只问",
        "问题 3 和问题 4 不能压成一句“分析题意”",
        "题目事实写错是一票否决",
        "记忆候选，不是题目事实",
        "没有形成额外假设",
        "没有形成候选",
        "新手的起步标准",
        "先做一个动作",
        "当前最早空缺",
        "推理转折",
        "没有发生转折",
        "完整方向确认句",
        "Java 代码位置",
        "对应反例",
    ],
    INSTALLED_SKILL: [
        "八个自然问题",
        "现场交接表",
        "我刚得到",
        "但它还不能说明",
        "所以现在只问",
        "Questions 3 and 4 both belong to stage 3",
        "题目事实写错是一票否决",
        "记忆候选，不是题目事实",
        "没有形成额外假设",
        "没有形成候选",
        "Beginner start contract",
        "Concrete paper action",
        "Evidence gained",
        "没有形成候选",
        "没有发生转折",
        "direction-confirmation sentence",
        "Java 代码位置",
        "对应反例",
    ],
    AGENTS: [
        "八个自然问题",
        "阶段 3：问题 3 -> 问题 4",
        "不能压缩成一句“分析题意”",
        "我刚得到",
        "但它还不能说明",
        "所以现在只问",
        "新手的起步标准",
        "没有形成候选",
        "没有发生转折",
        "Java 代码位置",
        "对应反例",
    ],
    WORKBENCH: [
        "八个自然问题",
        "为什么现在轮到它",
        "先回答问题 3",
        "再回答问题 4",
        "没有形成额外假设",
        "完整因果句",
        "我刚得到",
        "但它还不能说明",
        "所以现在只问",
        "当前最早空缺",
        "第一件实际做的纸面动作",
        "做完后多出的证据",
        "没有形成候选",
        "没有发生转折",
    ],
    SITE_APP: [
        "const BEGINNER_QUESTION_CARD",
        "现场交接表 · 八个自然问题",
        "我刚得到",
        "但它还不能说明",
        "所以现在只问",
        "问题 3 和问题 4 同属第三阶段",
        "const BEGINNER_ACTION_STEPS",
        "新手的起步动作表",
        "renderBeginnerActionTable",
        "当前最早空缺",
        "第一件实际做的纸面动作",
        "没有发生转折",
        "对象、过程与第一次变化（问题 3 -> 问题 4）",
        "候选池不是结论",
        "完整方向确认句",
        "没有形成候选",
        "renderHumanStageContract",
        "Java 代码位置",
        "对应反例",
        "const BEGINNER_LIVE_STANDARD",
        "renderBeginnerLiveStandard",
        "小白现场统一标准",
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

FORBIDDEN_IN_STAGE_TWO = [
    "保存尚未结算",
    "先记下来",
    "等未来结算",
    "等待集合",
    "候选池",
    "重复劳动",
    "子问题复用",
    "优化暴力",
    "用栈",
    "用哈希",
    "用双指针",
    "用动态规划",
]

FORBIDDEN_BEFORE_DIRECTION = [
    "哈希",
    "双指针",
    "一次遍历",
    "HashMap",
    "索引映射",
]

NATURAL_QUESTION_FIELDS = [
    "这一步是小白的自然追问，因为",
    "我刚得到",
    "但这份证据只能说明",
    "它还不能说明",
    "因此现在只允许问",
    "回答它至少需要",
    "回答后只允许新增",
    "在回答之前禁止出现",
]

NATURAL_QUESTION_SOURCES = [
    STANDARD,
    TEMPLATE,
    HUMAN_GUIDE,
    REPO_SKILL,
    INSTALLED_SKILL,
    AGENTS,
    WORKBENCH,
    RECORD_TEMPLATE,
]

STAGE_GATE_MARKERS = [
    "| 1. 读题 |",
    "| 2. 扩写 |",
    "| 3. 当前困惑、证据、对象、过程与第一次变化 |",
    "| 4. 范围与候选 |",
    "| 5. 第二次变化 |",
    "| 6. 方向确认 |",
    "| 7. 推导链 |",
]

STAGE_GATE_FIELDS = ["进入条件", "允许产物", "禁止产物", "说不清时退回"]

STAGE_GATE_SOURCES = [
    STANDARD,
    TEMPLATE,
    REPO_SKILL,
    INSTALLED_SKILL,
    AGENTS,
    WORKBENCH,
]

HUMAN_ACCEPTANCE_SOURCES = [
    STANDARD,
    TEMPLATE,
    REPO_SKILL,
    INSTALLED_SKILL,
    AGENTS,
    SITE_APP,
]

HUMAN_ACCEPTANCE_RULES = [
    "题目事实错误一票否决",
    "流畅解释、知道方法名和代码跑通都不等于理解",
    "闭卷后必须重新生成判断",
]

ACCEPTANCE_STAGE_MARKERS = [
    "| 1. 读题 |",
    "| 2. 扩写 |",
    "| 3. 当前困惑、证据、对象、过程与第一次变化 |",
    "| 4. 范围与候选 |",
    "| 5. 第二次变化 |",
    "| 6. 方向确认 |",
    "| 7. 推导链 |",
]

STAGE_THREE_SOURCES = [
    STANDARD,
    TEMPLATE,
    DEMO,
    RECORD_TEMPLATE,
    REAL_PROBLEM_TEMPLATE,
    TWO_SUM,
    WORKBENCH,
    REPO_SKILL,
    INSTALLED_SKILL,
]

STAGE_THREE_MARKERS = [
    "当前困惑",
    "实际纸面动作",
    "新增证据",
    "对象表",
    "人工过程",
    "第一次变化",
]

OBJECT_TABLE_SOURCES = [
    STANDARD,
    TEMPLATE,
    RECORD_TEMPLATE,
    REAL_PROBLEM_TEMPLATE,
    TWO_SUM,
]

COUNTEREXAMPLE_SOURCES = [
    STANDARD,
    TEMPLATE,
    REAL_PROBLEM_TEMPLATE,
    TWO_SUM,
]

COUNTEREXAMPLE_FIELDS = [
    "最小输入：",
    "原本应保持的不变量或更新顺序：",
    "如果破坏它，具体哪一步先算错：",
    "错误输出：",
    "修复动作：",
]

ONE_VOTE_VETO_SOURCES = [
    STANDARD,
    REPO_SKILL,
    INSTALLED_SKILL,
    AGENTS,
    WORKBENCH,
    SCORE_GUIDE,
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


def markdown_blocks(text: str) -> list[str]:
    """Return heading sections and fenced blocks that can independently hold a standard."""
    blocks: list[str] = []
    headings = list(re.finditer(r"^#{1,6}\s+.+$", text, re.MULTILINE))
    for index, heading in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        blocks.append(text[heading.start() : end])
    for match in re.finditer(
        r"^```[^\n]*\n(.*?)^```\s*$", text, re.MULTILINE | re.DOTALL
    ):
        blocks.append(match.group(1))
    return blocks


def question_blocks(path: Path, text: str) -> list[str]:
    blocks = markdown_blocks(text)
    if path == SITE_APP:
        start = text.find("const BEGINNER_QUESTION_CARD = [")
        end = text.find("const READING_HARD_GATES", start)
        if start >= 0 and end > start:
            blocks.append(text[start:end])
    return blocks


def first_ordered_question_block(path: Path, text: str) -> str | None:
    for block in question_blocks(path, text):
        normalized = compact(block)
        cursor = 0
        for question in QUESTIONS:
            position = normalized.find(compact(question), cursor)
            if position < 0:
                break
            cursor = position + len(compact(question))
        else:
            return block
    return None


def markers_in_order(text: str, markers: list[str]) -> bool:
    cursor = 0
    for marker in markers:
        position = text.find(marker, cursor)
        if position < 0:
            return False
        cursor = position + len(marker)
    return True


def split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def has_six_column_object_table(text: str) -> bool:
    headers = [
        "题目对象",
        "值和状态",
        "身份由什么决定",
        "位置或时间",
        "和谁发生关系",
        "最终要得到什么",
    ]
    lines = text.splitlines()
    for index, line in enumerate(lines[:-1]):
        if split_table_row(line) != headers:
            continue
        separator = split_table_row(lines[index + 1])
        if len(separator) == 6 and all(
            re.fullmatch(r":?-{3,}:?", cell) for cell in separator
        ):
            return True
    return False


def check_question_sequence(errors: list[str]) -> None:
    for path in QUESTION_SOURCES:
        text = read_text(path, errors)
        if text is None:
            continue
        if first_ordered_question_block(path, text) is not None:
            continue

        missing: list[str] = []
        for index, question in enumerate(QUESTIONS, start=1):
            if compact(question) not in compact(text):
                missing.append(f"{index}: {question}")
        if missing:
            for message in missing:
                errors.append(
                    f"{display_path(path)}: question {message} is missing or differs "
                    "from the canonical wording"
                )
        else:
            errors.append(
                f"{display_path(path)}: the eight questions exist, but no single "
                "section or code block keeps them in canonical order"
            )


def check_stage_three_evidence_order(errors: list[str]) -> None:
    ranges = {
        STANDARD: ("## 第三阶段：", "## 第四阶段："),
        TEMPLATE: ("## 问题 3 -> 问题 4：", "## 问题 5："),
        DEMO: ("## 3. ", "## 4. "),
        RECORD_TEMPLATE: ("### 问题 3 -> 问题 4：", "### 问题 5："),
        REAL_PROBLEM_TEMPLATE: ("## 阶段 3：", "## 阶段 4："),
        TWO_SUM: ("## 阶段 3：", "## 阶段 4："),
        WORKBENCH: ("### 阶段 3 现场顺序", "### 阶段 4 现场顺序"),
        REPO_SKILL: ("### Stage 2: objects", "### Stage 3: constraints"),
        INSTALLED_SKILL: ("### Stage 2: objects", "### Stage 3: constraints"),
    }

    for path in STAGE_THREE_SOURCES:
        text = read_text(path, errors)
        if text is None:
            continue
        start_marker, end_marker = ranges[path]
        start = text.find(start_marker)
        end = text.find(end_marker, start + len(start_marker)) if start >= 0 else -1
        section = text[start:end] if start >= 0 and end > start else ""
        if not section:
            errors.append(
                f"{display_path(path)}: cannot isolate stage-3 evidence sequence"
            )
            continue
        if not markers_in_order(section, STAGE_THREE_MARKERS):
            errors.append(
                f"{display_path(path)}: stage 3 must keep evidence in one continuous "
                "order: 当前困惑 -> 实际纸面动作 -> 新增证据 -> 对象表 -> "
                "人工过程 -> 第一次变化"
            )


def check_object_tables(errors: list[str]) -> None:
    for path in OBJECT_TABLE_SOURCES:
        text = read_text(path, errors)
        if text is None:
            continue
        if not has_six_column_object_table(text):
            errors.append(
                f"{display_path(path)}: the task-object table must have six columns "
                "headed 题目对象、值和状态、身份由什么决定、位置或时间、"
                "和谁发生关系、最终要得到什么"
            )


def check_minimal_counterexamples(errors: list[str]) -> None:
    for path in COUNTEREXAMPLE_SOURCES:
        text = read_text(path, errors)
        if text is None:
            continue
        if not markers_in_order(text, COUNTEREXAMPLE_FIELDS):
            errors.append(
                f"{display_path(path)}: the minimal counterexample must keep all "
                "five causal fields in order"
            )


def check_retrospective_path_index(errors: list[str]) -> None:
    ranges = {
        STANDARD: ("## 第六阶段：", "## 第七阶段："),
        DEMO: ("## 6. ", "## 7. "),
    }
    for path, (start_marker, end_marker) in ranges.items():
        text = read_text(path, errors)
        if text is None:
            continue
        start = text.find(start_marker)
        end = text.find(end_marker, start + len(start_marker))
        section = text[start:end] if start >= 0 and end > start else ""
        if not markers_in_order(section, ["完整方向确认句", "事后路径索引"]):
            errors.append(
                f"{display_path(path)}: 事后路径索引 must follow the complete "
                "direction-confirmation sentence inside stage 6"
            )


def check_no_final_methods_before_direction(errors: list[str]) -> None:
    ranges = {
        STANDARD: ("## 第一阶段：", "## 第四阶段："),
        TEMPLATE: ("## 问题 1：", "## 问题 5："),
        DEMO: ("## 1. ", "## 4. "),
        REAL_PROBLEM_TEMPLATE: ("## 阶段 1：", "## 阶段 4："),
        TWO_SUM: ("## 阶段 1：", "## 阶段 4："),
    }
    final_methods = [
        "哈希",
        "双指针",
        "HashMap",
        "滑动窗口",
        "单调栈",
        "动态规划",
    ]
    allowed_context = ["禁止", "不能", "不要", "不允许", "记忆候选", "撤回"]

    for path, (start_marker, end_marker) in ranges.items():
        text = read_text(path, errors)
        if text is None:
            continue
        start = text.find(start_marker)
        end = text.find(end_marker, start + len(start_marker))
        section = text[start:end] if start >= 0 and end > start else ""
        if not section:
            errors.append(
                f"{display_path(path)}: cannot isolate stages 1-3 for method-name check"
            )
            continue
        line_offset = 0
        for line in section.splitlines(keepends=True):
            if any(term in line for term in final_methods) and not any(
                context in line for context in allowed_context
            ):
                line_number = text[: start + line_offset].count("\n") + 1
                errors.append(
                    f"{display_path(path)}:{line_number}: stages 1-3 name a final "
                    f"method instead of leaving it as a blocked memory: {line.strip()}"
                )
            line_offset += len(line)


def check_record_has_step(text: str, heading: str) -> bool:
    start = text.find(heading)
    if start < 0:
        return False
    next_heading = re.search(r"^### ", text[start + len(heading) :], re.MULTILINE)
    end = (
        start + len(heading) + next_heading.start()
        if next_heading is not None
        else len(text)
    )
    section = text[start:end]
    return all(
        marker in section
        for marker in [
            "当前困惑",
            "实际纸面动作",
            "新增证据",
            "对象表",
            "人工过程",
            "第一次变化",
        ]
    )


def run_validator_self_checks() -> list[str]:
    failures: list[str] = []
    q1, q2, q3 = QUESTIONS[:3]
    complete = "\n".join(QUESTIONS)
    if first_ordered_question_block(STANDARD, f"## 标准\n{complete}") is None:
        failures.append("ordered question block was not accepted")
    scattered = "\n".join(
        [
            f"## 标题\n{q1}\n## 下一段\n{q2}\n## 再下一段\n{q3}"
        ]
    )
    if first_ordered_question_block(STANDARD, scattered) is not None:
        failures.append("globally scattered questions were incorrectly accepted")
    if markers_in_order(
        "对象表 新增证据 实际纸面动作 当前困惑 人工过程 第一次变化",
        STAGE_THREE_MARKERS,
    ):
        failures.append("object-table-first stage 3 was incorrectly accepted")
    bad_table = (
        "| 题目对象 | 身份由什么决定 | 位置或时间 | 和谁发生关系 | "
        "最终要得到什么 |\n| --- | --- | --- | --- | --- |"
    )
    if has_six_column_object_table(bad_table):
        failures.append("five-column object table was incorrectly accepted")
    first_complete = (
        "### 问题 3 -> 问题 4：\n当前困惑 实际纸面动作 新增证据 对象表 人工过程 第一次变化\n"
    )
    second_missing = "### 问题 3 -> 问题 4：\n当前困惑 对象表 人工过程\n"
    if not check_record_has_step(first_complete, "### 问题 3 -> 问题 4："):
        failures.append("complete first record was incorrectly rejected")
    if check_record_has_step(second_missing, "### 问题 3 -> 问题 4："):
        failures.append("incomplete second record was incorrectly accepted")
    return failures


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


def check_stage_two_isolation(errors: list[str]) -> None:
    ranges = [
        (
            STANDARD,
            "## 第二阶段：问题 2",
            "## 第三阶段：问题 3 -> 问题 4",
        ),
        (
            TEMPLATE,
            "## 问题 2：",
            "## 问题 3 -> 问题 4：",
        ),
        (
            DEMO,
            "## 2. 把题干扩写成一个人能看见的过程",
            "## 3.",
        ),
        (
            HUMAN_GUIDE,
            "## 第二段：逐句扩写题干，再合成可执行过程",
            "## 第三段：",
        ),
    ]

    for path, start_marker, end_marker in ranges:
        text = read_text(path, errors)
        if text is None:
            continue
        start = text.find(start_marker)
        end = text.find(end_marker, start + len(start_marker))
        if start < 0 or end <= start:
            errors.append(
                f"{display_path(path)}: cannot isolate stage 2 expansion"
            )
            continue
        section = text[start:end]
        for term in FORBIDDEN_IN_STAGE_TWO:
            if term in section:
                errors.append(
                    f"{display_path(path)}: stage 2 expansion leaks later-stage "
                    f"model: {term}"
                )

    score = read_text(SCORE_GUIDE, errors)
    if score is None:
        return
    stage_two_heading = re.compile(r"^### 2\. 扩写题干\s*$", re.MULTILINE)
    next_heading = re.compile(r"^#{2,3} ", re.MULTILINE)
    matches = list(stage_two_heading.finditer(score))
    if not matches:
        errors.append(
            f"{display_path(SCORE_GUIDE)}: cannot isolate stage 2 expansion"
        )
        return
    for index, match in enumerate(matches, start=1):
        next_match = next_heading.search(score, match.end())
        end = next_match.start() if next_match is not None else len(score)
        section = score[match.end() : end]
        for term in FORBIDDEN_IN_STAGE_TWO:
            if term in section:
                errors.append(
                    f"{display_path(SCORE_GUIDE)}: stage 2 expansion {index} leaks "
                    f"later-stage model: {term}"
                )


def check_handoff_and_code_mapping(errors: list[str]) -> None:
    standard = read_text(STANDARD, errors)
    if standard is not None:
        questions_start = standard.find("## 八个自然问题")
        handoff = standard[:questions_start] if questions_start >= 0 else ""
        for phrase in ["现场交接表", "我刚得到", "但它还不能说明", "所以现在只问"]:
            if phrase not in handoff:
                errors.append(
                    f"{display_path(STANDARD)}: handoff section is missing {phrase}"
                )

        object_start = standard.find("把对象写成表")
        object_end = standard.find("身份决定后面能保存什么", object_start)
        object_section = (
            standard[object_start:object_end]
            if object_start >= 0 and object_end > object_start
            else ""
        )
        for phrase in [
            "身份由什么决定",
            "位置或时间",
            "和谁发生关系",
            "最终要得到什么",
        ]:
            if phrase not in object_section:
                errors.append(
                    f"{display_path(STANDARD)}: object table is missing {phrase}"
                )

        process_start = standard.find("现场过程不要写成一段没有时间顺序的概括")
        process_end = standard.find("如果某一格只能靠", process_start)
        process_section = (
            standard[process_start:process_end]
            if process_start >= 0 and process_end > process_start
            else ""
        )
        for phrase in ["看见什么", "处理谁", "具体做什么", "什么变了", "为什么还能继续"]:
            if phrase not in process_section:
                errors.append(
                    f"{display_path(STANDARD)}: process trace is missing {phrase}"
                )

        stage_7_start = standard.find("## 第七阶段：问题 8")
        stage_7_end = standard.find("## 每一步的结论必须有来源", stage_7_start)
        stage_7 = (
            standard[stage_7_start:stage_7_end]
            if stage_7_start >= 0 and stage_7_end > stage_7_start
            else ""
        )
        for phrase in [
            "Java 代码位置",
            "更新顺序或不变量",
            "对应反例",
        ]:
            if phrase not in stage_7:
                errors.append(
                    f"{display_path(STANDARD)}: stage 7 mapping is missing {phrase}"
                )

    workbench = read_text(WORKBENCH, errors)
    if workbench is not None:
        for phrase in ["为什么现在轮到它", "我刚得到", "但它还不能说明", "所以现在只问"]:
            if phrase not in workbench:
                errors.append(
                    f"{display_path(WORKBENCH)}: handoff table is missing {phrase}"
                )

    site = read_text(SITE_APP, errors)
    if site is not None:
        chain_start = site.find("const ALGORITHM_CHAIN_STEPS = [")
        step_start = site.find('index: "07"', chain_start)
        step_end = site.find('index: "08"', step_start)
        step = (
            site[step_start:step_end]
            if chain_start >= 0 and step_start >= 0 and step_end > step_start
            else ""
        )
        for phrase in [
            "Java 代码位置",
            "状态变量",
            "更新顺序或不变量",
            "对应反例",
        ]:
            if phrase not in step:
                errors.append(
                    f"{display_path(SITE_APP)}: code mapping step is missing {phrase}"
                )


def check_beginner_start_contract(errors: list[str]) -> None:
    standard = read_text(STANDARD, errors)
    if standard is not None:
        start = standard.find("## 新手的起步标准")
        end = standard.find("## 八个自然问题", start)
        section = standard[start:end] if start >= 0 and end > start else ""
        if not section:
            errors.append(
                f"{display_path(STANDARD)}: beginner start section is missing"
            )
        else:
            for phrase in [
                "最早卡点",
                "现在先做的纸面动作",
                "做完后多出的证据",
                "仍然不能做什么",
                "当前最早空缺",
                "我实际做的纸面动作",
                "推理转折必须可见",
            ]:
                if phrase not in section:
                    errors.append(
                        f"{display_path(STANDARD)}: beginner start section is missing "
                        f"{phrase}"
                    )

    template = read_text(TEMPLATE, errors)
    if template is not None:
        start = template.find("### 现场动作记录")
        end = template.find("## 问题 1：", start)
        section = template[start:end] if start >= 0 and end > start else ""
        if not section:
            errors.append(
                f"{display_path(TEMPLATE)}: live action record is missing"
            )
        else:
            for phrase in [
                "当前最早空缺",
                "第一件实际做的纸面动作",
                "做完后多出的证据",
                "此刻真实候选",
                "下一步只问",
                "推理转折记录",
                "没有形成候选",
            ]:
                if phrase not in section:
                    errors.append(
                        f"{display_path(TEMPLATE)}: live action record is missing "
                        f"{phrase}"
                    )

    record = read_text(RECORD_TEMPLATE, errors)
    if record is not None:
        start = record.find("### 现场动作记录")
        end = record.find("### 问题 1：", start)
        section = record[start:end] if start >= 0 and end > start else ""
        if not section:
            errors.append(
                f"{display_path(RECORD_TEMPLATE)}: live action record is missing"
            )
        else:
            for phrase in [
                "当前最早空缺",
                "第一件实际做的纸面动作",
                "做完后多出的证据",
                "此刻真实候选",
                "下一步只问",
                "推理转折记录",
                "没有形成候选",
            ]:
                if phrase not in section:
                    errors.append(
                        f"{display_path(RECORD_TEMPLATE)}: live action record is "
                        f"missing {phrase}"
                    )

    site = read_text(SITE_APP, errors)
    if site is not None:
        start = site.find("const BEGINNER_ACTION_STEPS = [")
        end = site.find("const BEGINNER_QUESTION_CARD = [", start)
        section = site[start:end] if start >= 0 and end > start else ""
        if not section:
            errors.append(
                f"{display_path(SITE_APP)}: beginner action table is missing"
            )
        else:
            for phrase in [
                "只知道题面文字",
                "知道要求但不会动",
                "对象混在一起",
                "操作预算",
                "方向已经确认",
            ]:
                if phrase not in section:
                    errors.append(
                        f"{display_path(SITE_APP)}: beginner action table is missing "
                        f"{phrase}"
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


def check_natural_question_contract(errors: list[str]) -> None:
    for path in NATURAL_QUESTION_SOURCES:
        text = read_text(path, errors)
        if text is None:
            continue
        normalized = normalize(text)
        for field in NATURAL_QUESTION_FIELDS:
            if normalize(field) not in normalized:
                errors.append(
                    f"{display_path(path)}: natural-question contract is missing "
                    f"{field}"
                )


def check_stage_gates(errors: list[str]) -> None:
    for path in STAGE_GATE_SOURCES:
        text = read_text(path, errors)
        if text is None:
            continue
        for field in STAGE_GATE_FIELDS:
            if field not in text:
                errors.append(
                    f"{display_path(path)}: stage gates are missing {field}"
                )
        check_ordered_markers(
            path,
            STAGE_GATE_MARKERS,
            "stage gate",
            errors,
        )

    standard = read_text(STANDARD, errors)
    if standard is None:
        return
    for index, heading in enumerate(STANDARD_HEADINGS):
        start = standard.find(heading)
        end = (
            standard.find(STANDARD_HEADINGS[index + 1], start)
            if index + 1 < len(STANDARD_HEADINGS)
            else standard.find("## 每一步的结论必须有来源", start)
        )
        section = standard[start:end] if start >= 0 and end > start else ""
        if not section:
            errors.append(
                f"{display_path(STANDARD)}: cannot isolate the gate section for "
                f"stage {index + 1}"
            )
            continue
        for field in STAGE_GATE_FIELDS:
            if field not in section:
                errors.append(
                    f"{display_path(STANDARD)}: stage {index + 1} gate is missing "
                    f"{field}"
                )


def check_human_acceptance_standard(errors: list[str]) -> None:
    for path in HUMAN_ACCEPTANCE_SOURCES:
        text = read_text(path, errors)
        if text is None:
            continue
        normalized = normalize(text)
        for rule in HUMAN_ACCEPTANCE_RULES:
            if normalize(rule) not in normalized:
                errors.append(
                    f"{display_path(path)}: human acceptance rule is missing {rule}"
                )

    standard = read_text(STANDARD, errors)
    if standard is not None:
        start = standard.find("## 人类解题验收标准")
        end = standard.find("## 自然追问合同", start)
        section = standard[start:end] if start >= 0 and end > start else ""
        if not section:
            errors.append(
                f"{display_path(STANDARD)}: human acceptance section is missing"
            )
        else:
            for field in [
                "先看什么",
                "下一件纸面动作",
                "允许继续的证据",
                "仍禁止出现",
                "说不通退回",
            ]:
                if field not in section:
                    errors.append(
                        f"{display_path(STANDARD)}: human acceptance table is "
                        f"missing {field}"
                    )
            cursor = 0
            for marker in ACCEPTANCE_STAGE_MARKERS:
                position = section.find(marker, cursor)
                if position < 0:
                    errors.append(
                        f"{display_path(STANDARD)}: human acceptance stage is "
                        f"missing or out of order: {marker}"
                    )
                    break
                cursor = position + len(marker)

    site = read_text(SITE_APP, errors)
    if site is not None:
        start = site.find("const HUMAN_ACCEPTANCE_STANDARD = [")
        end = site.find("const HUMAN_ACCEPTANCE_RULES = [", start)
        section = site[start:end] if start >= 0 and end > start else ""
        if not section:
            errors.append(
                f"{display_path(SITE_APP)}: HUMAN_ACCEPTANCE_STANDARD is missing"
            )
        else:
            for field in [
                "stage:",
                "firstLook:",
                "action:",
                "evidence:",
                "forbidden:",
                "returnTo:",
            ]:
                count = section.count(field)
                if count != 7:
                    errors.append(
                        f"{display_path(SITE_APP)}: human acceptance must define "
                        f"{field.rstrip(':')} exactly seven times (found {count})"
                    )
            stages = re.findall(r'stage: "([^"]+)"', section)
            expected_stages = [
                "1. 读题",
                "2. 扩写",
                "3. 对象、过程与第一次变化",
                "4. 范围与候选",
                "5. 第二次变化",
                "6. 方向确认",
                "7. 推导链",
            ]
            if stages != expected_stages:
                errors.append(
                    f"{display_path(SITE_APP)}: human acceptance stages are not in "
                    "the canonical seven-stage order"
                )
            stage_three = section.find('stage: "3. 对象、过程与第一次变化"')
            stage_four = section.find('stage: "4. 范围与候选"', stage_three)
            stage_three_section = (
                section[stage_three:stage_four]
                if stage_three >= 0 and stage_four > stage_three
                else ""
            )
            for problem in ["问题 3", "问题 4"]:
                if problem not in stage_three_section:
                    errors.append(
                        f"{display_path(SITE_APP)}: stage 3 acceptance must keep "
                        f"{problem}"
                    )

        render_start = site.find("function renderHumanAcceptanceStandard()")
        render_end = site.find("function renderReadingHardGates()", render_start)
        renderer = (
            site[render_start:render_end]
            if render_start >= 0 and render_end > render_start
            else ""
        )
        for phrase in [
            "先看什么",
            "下一件纸面动作",
            "允许继续的证据",
            "仍禁止出现",
            "说不通退回",
            "HUMAN_ACCEPTANCE_STANDARD.map",
        ]:
            if phrase not in renderer:
                errors.append(
                    f"{display_path(SITE_APP)}: human acceptance renderer is "
                    f"missing {phrase}"
                )


def check_human_causal_order(errors: list[str]) -> None:
    check_ordered_markers(
        STANDARD,
        [
            "## 第三阶段：问题 3 -> 问题 4",
            "### 3.4 第一次变化",
            "## 第四阶段：问题 5",
            "## 第五阶段：问题 6",
            "## 第六阶段：问题 7",
            "完整方向确认句",
            "## 第七阶段：问题 8",
        ],
        "causal stage",
        errors,
    )
    check_ordered_markers(
        TEMPLATE,
        [
            "## 问题 3 -> 问题 4：",
            "### 3.4 第一次变化",
            "## 问题 5：",
            "## 问题 6：",
            "## 问题 7：",
            "方向确认句：",
            "## 问题 8：",
        ],
        "causal stage",
        errors,
    )
    check_ordered_markers(
        DEMO,
        [
            "## 3. 记录当前困惑和新增证据，再走对象、人工过程和第一次变化",
            "### 3.4 第一次变化",
            "## 4. 读数据范围，只用来缩小候选",
            "## 5. 第二次观察变化：等待日期怎样产生和失效",
            "## 6. 比较候选并确认算法方向",
            "完整方向确认句",
            "## 7. 方向确认后的思维链",
        ],
        "causal stage",
        errors,
    )

    score = read_text(SCORE_GUIDE, errors)
    if score is not None:
        for dimension in [
            "自然可达性",
            "因果链完整度",
            "事实确定性",
            "闭卷重建",
        ]:
            if dimension not in score:
                errors.append(
                    f"{display_path(SCORE_GUIDE)}: admission dimension is missing "
                    f"{dimension}"
                )

    for path in ONE_VOTE_VETO_SOURCES:
        text = read_text(path, errors)
        if text is not None and "一票否决" not in text:
            errors.append(
                f"{display_path(path)}: wrong problem facts must be a one-vote veto"
            )


def check_site_stage_contract(errors: list[str]) -> None:
    site = read_text(SITE_APP, errors)
    if site is None:
        return

    start = site.find("const HUMAN_READING_STEPS = [")
    end = site.find("const BEGINNER_ACTION_STEPS = [", start)
    steps = site[start:end] if start >= 0 and end > start else ""
    if not steps:
        errors.append(
            f"{display_path(SITE_APP)}: cannot isolate HUMAN_READING_STEPS"
        )
        return

    for field in ["entry:", "allowed:", "blocked:", "returnTo:"]:
        count = steps.count(field)
        if count < 6:
            errors.append(
                f"{display_path(SITE_APP)}: the first six human stages must each "
                f"define {field.rstrip(':')} (found {count})"
            )

    gate_start = site.find("function renderHumanStageContract(step)")
    gate_end = site.find("function renderBankDetail(record)", gate_start)
    renderer = (
        site[gate_start:gate_end]
        if gate_start >= 0 and gate_end > gate_start
        else ""
    )
    for phrase in [
        "进入条件",
        "允许产物",
        "禁止产物",
        "说不清就退回",
        "step.entry",
        "step.allowed",
        "step.blocked",
        "step.returnTo",
    ]:
        if phrase not in renderer:
            errors.append(
                f"{display_path(SITE_APP)}: stage contract renderer is missing "
                f"{phrase}"
            )

    review_start = site.find("function renderReviewChainStep(step)")
    review_end = site.find("function renderReviewOption(", review_start)
    review_renderer = (
        site[review_start:review_end]
        if review_start >= 0 and review_end > review_start
        else ""
    )
    for phrase in [
        "进入条件",
        "允许产物",
        "禁止产物",
        "说不清就退回",
        "step.entry",
        "step.allowed",
        "step.blocked",
    ]:
        if phrase not in review_renderer:
            errors.append(
                f"{display_path(SITE_APP)}: review-chain renderer is missing "
                f"{phrase}"
            )

    stage_seven_start = site.find('entry: "完整方向确认句已经写成。"')
    stage_seven_end = site.find("</section>", stage_seven_start)
    stage_seven = (
        site[stage_seven_start:stage_seven_end]
        if stage_seven_start >= 0 and stage_seven_end > stage_seven_start
        else ""
    )
    for phrase in ["allowed:", "blocked:", "returnTo:"]:
        if phrase not in stage_seven:
            errors.append(
                f"{display_path(SITE_APP)}: stage 7 contract is missing {phrase}"
            )


def strip_markdown_links(text: str) -> str:
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", text)
    return re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)


def check_real_problem_sample(errors: list[str]) -> None:
    for path in [REAL_PROBLEM_TEMPLATE, TWO_SUM]:
        check_ordered_markers(path, REAL_PROBLEM_HEADINGS, "real-problem stage", errors)
        text = read_text(path, errors)
        if text is None:
            continue

        stage_one = text.find("## 阶段 1：")
        stage_six = text.find("## 阶段 6：", stage_one)
        stage_seven = text.find("## 阶段 7：", stage_six)
        official_hint = text.find("## 官方额外提示（答案侧）", stage_seven)
        if stage_one < 0 or stage_six <= stage_one or stage_seven <= stage_six:
            errors.append(
                f"{display_path(path)}: cannot isolate stages 1 through 7"
            )
            continue
        if official_hint < 0:
            errors.append(
                f"{display_path(path)}: official hints must follow the complete "
                "stage-7 derivation"
            )

        first_five = strip_markdown_links(text[stage_one:stage_six])
        for term in FORBIDDEN_BEFORE_DIRECTION:
            if term in first_five:
                errors.append(
                    f"{display_path(path)}: stages 1-5 leak a final method or "
                    f"structure name: {term}"
                )

        stage_three_end = text.find("## 阶段 4：", stage_one)
        stage_three = (
            text[text.find("## 阶段 3：", stage_one) : stage_three_end]
            if stage_three_end > stage_one
            else ""
        )
        for field in ["变化前", "触发事件", "变化后", "答案产生时刻"]:
            if field not in stage_three:
                errors.append(
                    f"{display_path(path)}: stage 3 first-change record is missing "
                    f"{field}"
                )

        stage_six_end = stage_seven
        stage_six_section = text[stage_six:stage_six_end]
        for phrase in ["候选", "完整方向确认句"]:
            if phrase not in stage_six_section:
                errors.append(
                    f"{display_path(path)}: stage 6 candidate confirmation is "
                    f"missing {phrase}"
                )

        stage_seven_section = text[stage_seven:official_hint]
        for phrase in [
            "状态",
            "不变量",
            "Java 代码位置",
            "更新顺序",
            "对应反例",
        ]:
            if phrase not in stage_seven_section:
                errors.append(
                    f"{display_path(path)}: stage 7 derivation is missing {phrase}"
                )

    sample = read_text(TWO_SUM, errors)
    if sample is not None:
        for phrase in [
            "此刻真实候选：没有形成候选",
            "题目没有保证数组有序或没有重复值，因此这里没有形成额外假设",
            "先查询历史\n后加入当前值",
        ]:
            if phrase not in sample:
                errors.append(
                    f"{display_path(TWO_SUM)}: human sample is missing the verified "
                    f"wording: {phrase}"
                )


def main() -> int:
    errors: list[str] = []
    errors.extend(f"validator self-check: {failure}" for failure in run_validator_self_checks())
    check_required_phrases(errors)
    check_question_sequence(errors)
    check_stage_three_evidence_order(errors)
    check_object_tables(errors)
    check_minimal_counterexamples(errors)
    check_retrospective_path_index(errors)
    check_no_final_methods_before_direction(errors)
    check_stage_structure(errors)
    check_range_before_second_change(errors)
    check_stage_two_isolation(errors)
    check_handoff_and_code_mapping(errors)
    check_beginner_start_contract(errors)
    check_legacy_language(errors)
    check_natural_question_contract(errors)
    check_stage_gates(errors)
    check_human_acceptance_standard(errors)
    check_human_causal_order(errors)
    check_site_stage_contract(errors)
    check_real_problem_sample(errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        "Human reading contract passed: 8 questions, 7 ordered stages, "
        "gated natural-question handoffs."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
