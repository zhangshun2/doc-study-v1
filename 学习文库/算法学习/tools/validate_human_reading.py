#!/usr/bin/env python3
"""Validate the beginner-first seven-stage, nine-handoff derivation contract."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]

STANDARD = REPO_ROOT / "LeetCode-系统复习" / "05-单题流程" / "单题推导标准卡.md"
TEMPLATE = REPO_ROOT / "LeetCode-系统复习" / "99-Skill" / "非压缩题解模板.md"
HUMAN_GUIDE = (
    REPO_ROOT / "LeetCode-系统复习" / "05-单题流程" / "人类推导样板与评分.md"
)
DEMO = REPO_ROOT / "LeetCode-系统复习" / "05-单题流程" / "小白读题现场示范.md"
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
REPO_SKILL = (
    REPO_ROOT
    / "LeetCode-系统复习"
    / "99-Skill"
    / "leetcode-steady-java-SKILL.md"
)
SITE_APP = REPO_ROOT / "site" / "assets" / "app.js"
AGENTS = REPO_ROOT / "学习文库" / "算法学习" / "AGENTS.md"
WORKBENCH = (
    REPO_ROOT
    / "学习文库"
    / "算法学习"
    / "学习看板"
    / "单题复习工作台.md"
)
ALGORITHM_README = REPO_ROOT / "学习文库" / "算法学习" / "README.md"

CHECKED_DOCUMENTS = [
    STANDARD,
    TEMPLATE,
    HUMAN_GUIDE,
    DEMO,
    REAL_PROBLEM_TEMPLATE,
    TWO_SUM,
    REPO_SKILL,
]

EXPECTED_MIN_CHAINS = {
    STANDARD: 1,
    TEMPLATE: 1,
    HUMAN_GUIDE: 4,
    DEMO: 1,
    REAL_PROBLEM_TEMPLATE: 1,
    TWO_SUM: 1,
}

HANDOFF_FIELDS = [
    "小白此刻真正的原话疑问",
    "为什么这个疑问现在才出现",
    "纸上实际做了什么",
    "做完后新增了什么证据",
    "这份证据只能说明什么",
    "它还不能说明什么",
    "因此下一问只能是什么",
    "回答它需要什么证据",
    "如果答不出，退回哪里",
]

HANDOFF_FIELD_KEYS = [
    "question",
    "whyNow",
    "paper",
    "evidence",
    "only",
    "cannot",
    "nextQuestion",
    "nextEvidence",
    "returnTo",
]

LIVE_GENERATION_FIELDS = [
    "我现在只能确认：",
    "它还不够回答：",
    "因此现在只做：",
    "做完必须多出的证据：",
    "证据不足就退回：",
]

OBJECT_TABLE_FIELDS = [
    "题目对象",
    "值和状态",
    "身份由什么决定",
    "位置或时间",
    "从何时有效到何时失效",
    "和谁发生关系",
    "最终要得到什么",
]

FIRST_CHANGE_FIELDS = [
    "谁发生变化：",
    "触发事件：",
    "变化前：",
    "变化后：",
    "答案确定时刻：",
    "为什么不是更早或更晚：",
]

SHARED_CONTRACT_DOCUMENTS = [
    STANDARD,
    TEMPLATE,
    REAL_PROBLEM_TEMPLATE,
    REPO_SKILL,
    AGENTS,
    WORKBENCH,
]

STRUCTURED_CONTRACT_DOCUMENTS = [
    STANDARD,
    TEMPLATE,
    REAL_PROBLEM_TEMPLATE,
    REPO_SKILL,
]

STALE_CONTRACT_PHRASES = [
    "每个结论只回答四件事",
    "只写四行",
    "我刚得到：",
    "答案产生时刻",
    "六列对象表",
    "三句话现场交接",
    "题目凭什么允许此刻停止",
    "它还不能说明：",
]

CANDIDATE_PATTERNS = [
    re.compile(pattern)
    for pattern in [
        r"哈希表",
        r"哈希",
        r"HashMap",
        r"\bMap\b",
        r"单调栈",
        r"\bStack\b",
        r"\bQueue\b",
        r"ArrayDeque",
        r"\bDeque\b",
        r"优先队列",
        r"双指针",
        r"动态规划",
        r"滑动窗口",
        r"回溯",
        r"二分查找",
        r"二分搜索",
        r"堆",
    ]
]

CANDIDATE_ZONE_FIELDS = [
    "范围后想到的方向：",
    "它可能消除的重复或失效工作：",
    "它依赖的题目条件：",
    "最坏预算是否允许：",
    "目前仍缺少什么过程证据：",
    "它还不能被选为主方向，因为：",
]

EARLY_SELECTION_PATTERNS = [
    re.compile(r"(?:所以|因此|于是).{0,10}(?:选择|采用|使用|就用)"),
    re.compile(r"(?:决定|确定).{0,6}(?:选择|采用|使用)"),
    re.compile(r"(?:最终方向|主方向)(?:就)?(?:是|选)"),
]

STALE_APP_PATTERNS = [
    "HUMAN_ACCEPTANCE_STANDARD",
    "问题 3",
    "问题 4",
    "问题 3 -> 问题 4",
    "7 个阶段 · 3 条硬规则",
    "八问",
    "8 个问题",
    "范围不能直接点名任何具体方法或结构",
    "不能出现具体方法或结构名称",
]

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
HANDOFF_RE = re.compile(r"交接\s*([1-9])")


class ValidationError(RuntimeError):
    """Raised when a contract check fails."""


@dataclass(frozen=True)
class Handoff:
    path: Path
    index: int
    line: int
    block: str

    @property
    def location(self) -> str:
        path = display_path(self.path)
        return f"{path}:{self.line}"


def display_path(path: Path) -> Path:
    try:
        return path.relative_to(REPO_ROOT)
    except ValueError:
        return path


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValidationError(f"无法读取 {path}: {exc}") from exc


def extract_handoffs(text: str, path: Path) -> list[Handoff]:
    """Find handoff headings while ignoring example headings inside code fences."""
    records: list[tuple[int, int, str, str]] = []
    in_fence = False
    offset = 0

    for line_number, line in enumerate(text.splitlines(keepends=True), start=1):
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            in_fence = not in_fence
            offset += len(line)
            continue

        if not in_fence:
            match = HEADING_RE.match(line.rstrip("\r\n"))
            if match:
                heading = match.group(2)
                handoff = HANDOFF_RE.search(heading)
                if handoff:
                    records.append(
                        (int(handoff.group(1)), line_number, offset, heading)
                    )
        offset += len(line)

    handoffs: list[Handoff] = []
    for position, (index, line_number, start, _heading) in enumerate(records):
        end = records[position + 1][2] if position + 1 < len(records) else len(text)
        handoffs.append(
            Handoff(
                path=path,
                index=index,
                line=line_number,
                block=text[start:end],
            )
        )
    return handoffs


def complete_chains(handoffs: list[Handoff]) -> list[list[Handoff]]:
    """Return runs containing all nine indexes, even if their order is wrong."""
    runs: list[list[Handoff]] = []
    current: list[Handoff] = []

    for handoff in handoffs:
        if handoff.index == 1:
            if current:
                runs.append(current)
            current = [handoff]
        elif current:
            current.append(handoff)

    if current:
        runs.append(current)

    expected = set(range(1, 10))
    return [
        run
        for run in runs
        if len(run) == 9 and {handoff.index for handoff in run} == expected
    ]


def validate_handoff_sequence(chain: list[Handoff]) -> None:
    indexes = [handoff.index for handoff in chain]
    expected = list(range(1, 10))
    if indexes != expected:
        path = display_path(chain[0].path)
        raise ValidationError(
            f"{path} 的交接顺序错误：期望 {expected}，实际 {indexes}"
        )


def validate_handoff_fields(handoff: Handoff) -> None:
    missing = [field for field in HANDOFF_FIELDS if field not in handoff.block]
    if missing:
        raise ValidationError(
            f"{handoff.location} 交接 {handoff.index} 缺少字段："
            + "、".join(missing)
        )


def missing_markers(text: str, markers: list[str]) -> list[str]:
    return [marker for marker in markers if marker not in text]


def validate_live_generation_contract(text: str, label: str) -> None:
    missing = missing_markers(text, LIVE_GENERATION_FIELDS)
    if missing:
        raise ValidationError(
            f"{label} 缺少现场五句：" + "、".join(missing)
        )
    if "它还不能说明：" in text:
        raise ValidationError(f"{label} 仍残留旧九字段笔误：它还不能说明：")


def validate_nine_field_contract(text: str, label: str) -> None:
    missing = missing_markers(text, [f"{field}：" for field in HANDOFF_FIELDS])
    if missing:
        raise ValidationError(
            f"{label} 缺少完整九字段：" + "、".join(missing)
        )
    if "它还不能说明：" in text:
        raise ValidationError(f"{label} 的九字段名称不完整：它还不能说明：")


def validate_object_table_contract(text: str, label: str) -> None:
    missing = missing_markers(text, OBJECT_TABLE_FIELDS)
    if missing:
        raise ValidationError(
            f"{label} 的对象表缺少列：" + "、".join(missing)
        )


def validate_first_change_contract(text: str, label: str) -> None:
    missing = missing_markers(text, FIRST_CHANGE_FIELDS)
    if missing:
        raise ValidationError(
            f"{label} 的第一次变化缺少字段：" + "、".join(missing)
        )


def validate_candidate_contract(text: str, label: str) -> None:
    missing = missing_markers(text, CANDIDATE_ZONE_FIELDS)
    if missing:
        raise ValidationError(
            f"{label} 的待验证方向缺少字段：" + "、".join(missing)
        )


def candidate_hits(text: str) -> list[str]:
    hits: list[str] = []
    for pattern in CANDIDATE_PATTERNS:
        matches = pattern.findall(text)
        if matches:
            hits.extend(str(match) for match in matches)
    return sorted(set(hits))


def extract_candidate_zone(block: str) -> tuple[int, int, str] | None:
    """Return the marked candidate-zone span and body inside handoff 6."""
    lines = block.splitlines(keepends=True)
    offset = 0
    for position, line in enumerate(lines):
        heading = HEADING_RE.match(line.rstrip("\r\n"))
        if not heading or "待验证方向" not in heading.group(2):
            offset += len(line)
            continue

        start = offset
        heading_level = len(heading.group(1))
        end = len(block)
        nested_offset = offset + len(line)
        for nested_line in lines[position + 1 :]:
            nested_heading = HEADING_RE.match(nested_line.rstrip("\r\n"))
            if nested_heading and len(nested_heading.group(1)) <= heading_level:
                end = nested_offset
                break
            nested_offset += len(nested_line)
        return start, end, block[start:end]
    return None


def validate_candidate_zone(handoff: Handoff) -> str | None:
    hits = candidate_hits(handoff.block)
    zone = extract_candidate_zone(handoff.block)

    if hits and zone is None:
        raise ValidationError(
            f"{handoff.location} 交接 6 的候选没有放进"
            "“范围后的待验证方向（未获证明资格）”："
            + "、".join(hits)
        )
    if zone is None:
        return None

    start, end, body = zone
    outside_hits = candidate_hits(handoff.block[:start] + handoff.block[end:])
    if outside_hits:
        raise ValidationError(
            f"{handoff.location} 交接 6 的待验证区之外泄漏候选："
            + "、".join(outside_hits)
        )

    missing = [field for field in CANDIDATE_ZONE_FIELDS if field not in body]
    if missing:
        raise ValidationError(
            f"{handoff.location} 待验证方向缺少证据字段："
            + "、".join(missing)
        )
    return body


def validate_data_range_zone(handoff: Handoff) -> None:
    if handoff.index != 6:
        return

    required_ideas = ("约束", "范围", "预算", "复杂度", "最坏")
    if not any(idea in handoff.block for idea in required_ideas):
        raise ValidationError(
            f"{handoff.location} 交接 6 没有留下范围或预算证据"
        )

    validate_candidate_zone(handoff)


def validate_candidate_gate(chain: list[Handoff]) -> None:
    for handoff in chain[:5]:
        hits = candidate_hits(handoff.block)
        if hits:
            raise ValidationError(
                f"{handoff.location} 交接 {handoff.index} 在交接 8 前泄漏候选："
                + "、".join(hits)
            )

    validate_data_range_zone(chain[5])

    handoff_seven = chain[6]
    hits = candidate_hits(handoff_seven.block)
    if hits:
        raise ValidationError(
            f"{handoff_seven.location} 交接 7 还没回到过程取证就泄漏候选："
            + "、".join(hits)
        )

    for handoff in chain[:6]:
        for pattern in EARLY_SELECTION_PATTERNS:
            match = pattern.search(handoff.block)
            if match:
                raise ValidationError(
                    f"{handoff.location} 交接 {handoff.index} 提前出现选择语气："
                    f"{match.group(0)}"
                )

    handoff_eight = chain[7]
    if "候选" not in handoff_eight.block:
        raise ValidationError(
            f"{handoff_eight.location} 交接 8 没有说明候选比较或“没有形成候选”"
        )


def validate_document(path: Path) -> int:
    text = read_text(path)
    handoffs = extract_handoffs(text, path)
    chains = complete_chains(handoffs)

    minimum = EXPECTED_MIN_CHAINS.get(path, 0)
    if len(chains) < minimum:
        raise ValidationError(
            f"{display_path(path)} 只找到 {len(chains)} 条完整 1-9 链，"
            f"至少需要 {minimum} 条"
        )

    for chain in chains:
        validate_handoff_sequence(chain)
        for handoff in chain:
            validate_handoff_fields(handoff)
            validate_data_range_zone(handoff)
        validate_candidate_gate(chain)

    if path == REPO_SKILL:
        for marker in ("七阶段、九次交接", "小白此刻真正的原话疑问", "交接 9"):
            if marker not in text:
                raise ValidationError(
                    f"{display_path(path)} 缺少九交接标记：{marker}"
                )

    return len(chains)


def extract_js_handoff_blocks(script: str) -> list[tuple[int, str]]:
    start = script.find("const HANDOFFS = [")
    end = script.find("const TWO_SUM_NINE_HANDOFF_DEMO")
    if start < 0 or end <= start:
        raise ValidationError("site/assets/app.js 找不到完整的 HANDOFFS 定义")

    source = script[start:end]
    matches = list(re.finditer(r"^\s{2}\{\s*$", source, flags=re.MULTILINE))
    blocks: list[tuple[int, str]] = []
    for position, match in enumerate(matches):
        block_end = matches[position + 1].start() if position + 1 < len(matches) else len(source)
        block = source[match.start():block_end]
        index_match = re.search(r'index:\s*"(0[1-9])"', block)
        if index_match:
            blocks.append((int(index_match.group(1)), block))
    return blocks


def extract_js_array(script: str, name: str) -> str:
    start = script.find(f"const {name} = [")
    if start < 0:
        raise ValidationError(f"site/assets/app.js 找不到 {name}")
    end = script.find("\n];", start)
    if end < 0:
        raise ValidationError(f"site/assets/app.js 的 {name} 没有结束")
    return script[start : end + len("\n];")]


def count_top_level_js_objects(array_source: str) -> int:
    return len(re.findall(r"^\s{2}\{\s*$", array_source, flags=re.MULTILINE))


def validate_beginner_question_structure(
    source: str,
    label: str,
    expected_terms: list[str] | None = None,
) -> None:
    count = count_top_level_js_objects(source)
    if count != 9:
        raise ValidationError(f"{label} 必须正好有 9 项，实际 {count} 项")

    required_order = ["对象", "最笨", "第一次变化", "数据范围", "重复"]
    positions = [source.find(word) for word in required_order]
    if any(position < 0 for position in positions) or positions != sorted(positions):
        raise ValidationError(
            f"{label} 必须按“读题 → 扩写 → 对象 → 笨过程 → "
            "第一次变化 → 数据范围 → 重复取证”展开"
        )

    if expected_terms:
        positions = [source.find(term) for term in expected_terms]
        if any(position < 0 for position in positions) or positions != sorted(positions):
            raise ValidationError(
                f"{label} 必须按九问顺序排列，实际缺少或错序："
                + "、".join(expected_terms)
            )


def extract_js_function_source(script: str, name: str) -> str:
    marker = f"function {name}("
    start = script.find(marker)
    if start < 0:
        raise ValidationError(f"site/assets/app.js 找不到函数 {name}")
    end = script.find("\nfunction ", start + len(marker))
    if end < 0:
        end = len(script)
    return script[start:end]


def validate_site_handoff_placement(script: str) -> None:
    live_call = "HANDOFFS.map((handoff) => renderLiveHandoffCard(handoff)).join(\"\")"
    complete_call = (
        "HANDOFFS.map((handoff) => renderCompleteHandoffCard(handoff, "
        "{ compact: true, idPrefix: \"handoff-complete\" })).join(\"\")"
    )
    diagnostics_start = script.find('<details class="review-diagnostics">')
    diagnostics_end = script.find("</details>", diagnostics_start)
    if script.count(live_call) != 1:
        raise ValidationError("主现场必须且只能从五句现场卡渲染九次交接")
    if script.count(complete_call) != 1:
        raise ValidationError("完整九字段必须且只能出现一次完成复盘卡")
    if diagnostics_start < 0 or diagnostics_end <= diagnostics_start:
        raise ValidationError("site/assets/app.js 找不到完成后诊断折叠区")
    complete_position = script.find(complete_call)
    if not diagnostics_start < complete_position < diagnostics_end:
        raise ValidationError("九字段完整卡被放在现场区，而不是完成后诊断区")
    live_position = script.find(live_call)
    if not 0 <= live_position < diagnostics_start:
        raise ValidationError("现场五句卡没有出现在完成后诊断区之前")


def validate_site_app(path: Path) -> None:
    script = read_text(path)

    for stale in STALE_APP_PATTERNS:
        if stale in script:
            raise ValidationError(f"site/assets/app.js 仍残留旧标准：{stale}")

    blocks = extract_js_handoff_blocks(script)
    indexes = [index for index, _block in blocks]
    if indexes != list(range(1, 10)):
        raise ValidationError(f"site/assets/app.js 的 HANDOFFS 顺序错误：{indexes}")

    for index, block in blocks:
        missing = [key for key in HANDOFF_FIELD_KEYS if f"{key}:" not in block]
        if missing:
            raise ValidationError(
                f"site/assets/app.js 交接 {index} 缺少字段："
                + "、".join(missing)
            )
        if index < 8 and index != 6:
            hits = candidate_hits(block)
            if hits:
                raise ValidationError(
                    f"site/assets/app.js 交接 {index} 在交接 8 前泄漏候选："
                    + "、".join(hits)
                )
        if index == 6:
            validate_data_range_zone(
                Handoff(path=path, index=6, line=0, block=block)
            )

    question_source = extract_js_array(script, "BEGINNER_QUESTION_CARD")
    action_source = extract_js_array(script, "BEGINNER_ACTION_STEPS")
    validate_beginner_question_structure(
        question_source,
        "九问卡",
        [
            "阶段 1",
            "阶段 2",
            "阶段 3 · 先分清对象",
            "阶段 3 · 再走最笨",
            "阶段 3 · 捕捉第一次变化",
            "阶段 4",
            "阶段 5",
            "阶段 6",
            "阶段 7",
        ],
    )
    validate_beginner_question_structure(
        action_source,
        "起步动作表",
        [
            "刚打开题",
            "题干扩写成动作",
            "对象混在一起",
            "最笨但正确",
            "第一次变化",
            "数据范围",
            "留下什么",
            "哪个候选",
            "状态和代码",
        ],
    )
    if "rangeBlocked" in script:
        raise ValidationError("site/assets/app.js 仍保留旧的范围段候选禁区字段")
    if "待验证方向" not in question_source or "六项" not in question_source:
        raise ValidationError("九问卡没有说明交接 6 的六项待验证方向")

    validate_live_generation_contract(script, "site/assets/app.js")
    for pattern in STALE_CONTRACT_PHRASES:
        if pattern in script:
            raise ValidationError(f"site/assets/app.js 仍残留旧标准：{pattern}")

    live_function = extract_js_function_source(script, "renderLiveHandoffCard")
    complete_function = extract_js_function_source(
        script, "renderCompleteHandoffCard"
    )
    leaked_fields = [field for field in HANDOFF_FIELDS if field in live_function]
    if leaked_fields:
        raise ValidationError(
            "现场交接卡又渲染了九字段："
            + "、".join(leaked_fields)
        )
    missing_complete_fields = missing_markers(
        complete_function, [f"{field}" for field in HANDOFF_FIELDS]
    )
    if missing_complete_fields:
        raise ValidationError(
            "完成后的九字段卡缺少："
            + "、".join(missing_complete_fields)
        )
    if "data-live-handoff=\"true\"" not in live_function:
        raise ValidationError("现场交接卡没有 data-live-handoff 标记")
    if "data-retrospective-handoff=\"true\"" not in complete_function:
        raise ValidationError("完成后九字段卡没有 data-retrospective-handoff 标记")

    validate_site_handoff_placement(script)

    acceptance_start = script.find("function renderHumanAcceptanceStandard()")
    if acceptance_start < 0:
        raise ValidationError("site/assets/app.js 缺少九交接验收渲染函数")
    acceptance_tail = script[acceptance_start : acceptance_start + 1800]
    if "HANDOFFS.map" not in acceptance_tail:
        raise ValidationError("验收卡没有从唯一 HANDOFFS 数据生成")
    if "9 次交接 · 3 条硬规则" not in script:
        raise ValidationError("验收标题仍不是九次交接")
    if "review-causal-path" not in script or "范围预算" not in script:
        raise ValidationError("复习页缺少从题面到算法方向的九次交接路径")


def validate_maintained_guides() -> None:
    standard = read_text(STANDARD)
    if "小白现场原话：每一步为什么自然产生" not in standard:
        raise ValidationError("标准卡缺少小白逐步产生下一问的现场因果表")
    if "数据范围必须放在第一次变化之后" not in standard:
        raise ValidationError("标准卡没有锁定数据范围与第一次变化的先后关系")

    for path in SHARED_CONTRACT_DOCUMENTS:
        text = read_text(path)
        label = str(display_path(path))
        validate_live_generation_contract(text, label)
        validate_nine_field_contract(text, label)
        for stale in STALE_CONTRACT_PHRASES:
            if stale in text:
                raise ValidationError(f"{label} 仍残留旧标准：{stale}")

    for path in STRUCTURED_CONTRACT_DOCUMENTS:
        text = read_text(path)
        label = str(display_path(path))
        validate_object_table_contract(text, label)
        validate_first_change_contract(text, label)
        validate_candidate_contract(text, label)

    agents = read_text(AGENTS)
    required_agents_questions = [
        "问题 4：照着最笨的办法走一遍，第一步先处理谁",
        "问题 5：走完以后，哪一刻什么变了",
        "问题 6：这个笨办法最坏会重复多少",
        "问题 7：带着这个代价重看",
        "问题 8：这些操作需要什么方向来承担",
        "问题 9：方向已经定了，状态、更新顺序、不变量、代码和反例",
        "知道可能太贵 -> 不知道留下什么、何时丢掉 -> 交接 7",
    ]
    for marker in required_agents_questions:
        if marker not in agents:
            raise ValidationError(f"AGENTS.md 的九问或现场因果已过期：{marker}")

    stale_agents_questions = [
        "问题 4：照着最笨的办法走一遍，哪一刻什么变了",
        "问题 5：这个笨办法最坏会重复多少",
        "问题 6：带着这个代价重看",
        "问题 7：这些操作需要什么方向来承担",
        "问题 8：方向已经定了",
    ]
    for stale in stale_agents_questions:
        if stale in agents:
            raise ValidationError(f"AGENTS.md 仍残留旧九问编号：{stale}")

    readme = read_text(ALGORITHM_README)
    stale_readme = ("第一层六个方向判断阶段", "方向确认后的 8 个推导确认点")
    for stale in stale_readme:
        if stale in readme:
            raise ValidationError(f"算法学习 README 仍残留旧复习页说明：{stale}")
    if "七阶段、九次交接" not in readme:
        raise ValidationError("算法学习 README 没有说明七阶段、九次交接")


def fixture_chain(order: list[int]) -> list[Handoff]:
    handoffs: list[Handoff] = []
    path = Path("fixture.md")
    for sequence, index in enumerate(order, start=1):
        lines = [f"## 交接 {index}", "```text"]
        for field in HANDOFF_FIELDS:
            lines.append(f"{field}：______")
        lines.append("```")
        if index == 6:
            lines.extend(["", "官方约束 n <= 10^5；最坏操作预算约为 n log n。"])
        handoffs.append(
            Handoff(path=path, index=index, line=sequence, block="\n".join(lines))
        )
    return handoffs


def expect_failure(label: str, action) -> None:
    try:
        action()
    except ValidationError:
        return
    raise ValidationError(f"负向夹具没有检出预期错误：{label}")


def run_fixture_checks() -> None:
    ordered = fixture_chain(list(range(1, 10)))

    validate_live_generation_contract(
        "\n".join(LIVE_GENERATION_FIELDS),
        "正向现场五句",
    )
    expect_failure(
        "现场五句缺少退回条件",
        lambda: validate_live_generation_contract(
            "\n".join(LIVE_GENERATION_FIELDS[:-1]),
            "缺句夹具",
        ),
    )

    validate_nine_field_contract(
        "\n".join(f"{field}：" for field in HANDOFF_FIELDS),
        "正向九字段",
    )
    expect_failure(
        "九字段名称被截短",
        lambda: validate_nine_field_contract(
            "\n".join(
                f"{field}：" for field in HANDOFF_FIELDS
            ).replace("它还不能说明什么：", "它还不能说明："),
            "错名夹具",
        ),
    )

    validate_object_table_contract(
        "| " + " | ".join(OBJECT_TABLE_FIELDS) + " |",
        "正向七列对象表",
    )
    expect_failure(
        "对象表退回六列",
        lambda: validate_object_table_contract(
            "| " + " | ".join(OBJECT_TABLE_FIELDS[:-1]) + " |",
            "六列夹具",
        ),
    )

    validate_first_change_contract(
        "\n".join(FIRST_CHANGE_FIELDS),
        "正向第一次变化六项",
    )
    expect_failure(
        "第一次变化缺少时间边界",
        lambda: validate_first_change_contract(
            "\n".join(FIRST_CHANGE_FIELDS[:-1]),
            "缺第六项夹具",
        ),
    )

    validate_candidate_contract(
        "\n".join(CANDIDATE_ZONE_FIELDS),
        "正向待验证方向六项",
    )
    expect_failure(
        "待验证方向缺少不能选择的理由",
        lambda: validate_candidate_contract(
            "\n".join(CANDIDATE_ZONE_FIELDS[:-1]),
            "缺候选证据夹具",
        ),
    )

    live_call = (
        "HANDOFFS.map((handoff) => renderLiveHandoffCard(handoff)).join(\"\")"
    )
    complete_call = (
        "HANDOFFS.map((handoff) => renderCompleteHandoffCard(handoff, "
        "{ compact: true, idPrefix: \"handoff-complete\" })).join(\"\")"
    )
    valid_site = (
        f"{live_call}\n<details class=\"review-diagnostics\">"
        f"{complete_call}</details>"
    )
    validate_site_handoff_placement(valid_site)

    retrospective_in_live = (
        f"<details class=\"review-diagnostics\">{complete_call}</details>"
        f"\n{complete_call}"
    )
    expect_failure(
        "九字段完整卡又被放回现场区",
        lambda: validate_site_handoff_placement(retrospective_in_live),
    )

    reversed_middle = fixture_chain([1, 2, 3, 4, 5, 7, 6, 8, 9])
    expect_failure(
        "交接 7 排在交接 6 前",
        lambda: validate_handoff_sequence(reversed_middle),
    )

    missing_field = fixture_chain(list(range(1, 10)))
    broken_block = missing_field[2].block.replace(
        "如果答不出，退回哪里：______\n", ""
    )
    missing_field[2] = Handoff(
        path=missing_field[2].path,
        index=3,
        line=missing_field[2].line,
        block=broken_block,
    )
    expect_failure(
        "交接缺九字段之一",
        lambda: validate_handoff_fields(missing_field[2]),
    )

    legal_candidate = fixture_chain(list(range(1, 10)))
    legal_candidate[5] = Handoff(
        path=legal_candidate[5].path,
        index=6,
        line=legal_candidate[5].line,
        block=legal_candidate[5].block
        + "\n### 范围后的待验证方向（未获证明资格）\n"
        + "\n".join(CANDIDATE_ZONE_FIELDS),
    )
    validate_data_range_zone(legal_candidate[5])

    concrete_outside_zone = fixture_chain(list(range(1, 10)))
    concrete_outside_zone[5] = Handoff(
        path=concrete_outside_zone[5].path,
        index=6,
        line=concrete_outside_zone[5].line,
        block=concrete_outside_zone[5].block + "\n这里应该使用 HashMap。",
    )
    expect_failure(
        "交接 6 的候选写在待验证区外",
        lambda: validate_data_range_zone(concrete_outside_zone[5]),
    )

    missing_candidate_field = fixture_chain(list(range(1, 10)))
    missing_candidate_field[5] = Handoff(
        path=missing_candidate_field[5].path,
        index=6,
        line=missing_candidate_field[5].line,
        block=missing_candidate_field[5].block
        + "\n### 范围后的待验证方向（未获证明资格）\n"
        + "\n".join(CANDIDATE_ZONE_FIELDS[:-1]),
    )
    expect_failure(
        "待验证方向缺少六字段之一",
        lambda: validate_data_range_zone(missing_candidate_field[5]),
    )

    early_leak = fixture_chain(list(range(1, 10)))
    early_leak[2] = Handoff(
        path=early_leak[2].path,
        index=3,
        line=early_leak[2].line,
        block=early_leak[2].block + "\n下一步使用栈。",
    )
    expect_failure(
        "交接 3 提前泄漏具体候选",
        lambda: validate_candidate_gate(early_leak),
    )

    handoff_seven_leak = fixture_chain(list(range(1, 10)))
    handoff_seven_leak[6] = Handoff(
        path=handoff_seven_leak[6].path,
        index=7,
        line=handoff_seven_leak[6].line,
        block=handoff_seven_leak[6].block + "\n这里使用单调栈。",
    )
    expect_failure(
        "交接 7 提前泄漏候选",
        lambda: validate_candidate_gate(handoff_seven_leak),
    )

    early_selection = fixture_chain(list(range(1, 10)))
    early_selection[4] = Handoff(
        path=early_selection[4].path,
        index=5,
        line=early_selection[4].line,
        block=early_selection[4].block + "\n所以选择这个方向。",
    )
    expect_failure(
        "交接 1 至 6 提前出现选择语气",
        lambda: validate_candidate_gate(early_selection),
    )

    duplicate_questions = (
        "const BEGINNER_QUESTION_CARD = [\n"
        + '  {\n    stage: "对象",\n  },\n'
        + '  {\n    stage: "最笨过程",\n  },\n'
        + '  {\n    stage: "第一次变化",\n  },\n'
        + '  {\n    stage: "数据范围",\n  },\n'
        + '  {\n    stage: "重复",\n  },\n'
        + '  {\n    stage: "多余",\n  },\n'
        + '  {\n    stage: "多余",\n  },\n'
        + '  {\n    stage: "多余",\n  },\n'
        + '  {\n    stage: "多余",\n  },\n'
        + '  {\n    stage: "多余",\n  },\n'
        + "];\n"
    )
    expect_failure(
        "九问卡重复成十项",
        lambda: validate_beginner_question_structure(
            duplicate_questions, "九问卡"
        ),
    )

    validate_beginner_question_structure(
        "const BEGINNER_ACTION_STEPS = [\n"
        + '  {\n    action: "对象",\n  },\n'
        + '  {\n    action: "最笨",\n  },\n'
        + '  {\n    action: "第一次变化",\n  },\n'
        + '  {\n    action: "数据范围",\n  },\n'
        + '  {\n    action: "重复",\n  },\n'
        + '  {\n    action: "候选",\n  },\n'
        + '  {\n    action: "方向",\n  },\n'
        + '  {\n    action: "状态",\n  },\n'
        + '  {\n    action: "反例",\n  },\n'
        + "];\n",
        "正向起步动作表",
    )

    if extract_handoffs("```md\n## 交接 1\n```\n", Path("fenced.md")):
        raise ValidationError("负向夹具没有忽略代码块里的示例标题")

    validate_handoff_sequence(ordered)


def main() -> int:
    try:
        run_fixture_checks()
        total_chains = 0
        for path in CHECKED_DOCUMENTS:
            total_chains += validate_document(path)
        validate_site_app(SITE_APP)
        validate_maintained_guides()
    except ValidationError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    print(
        "OK: 九次交接、九字段、待验证方向六字段、九问结构"
        "和页面验收均已通过"
        f"（{total_chains} 条完整现场链）"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
