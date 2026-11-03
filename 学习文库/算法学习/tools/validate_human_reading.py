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
        r"堆",
    ]
]

STALE_APP_PATTERNS = [
    "HUMAN_ACCEPTANCE_STANDARD",
    "问题 3",
    "问题 4",
    "问题 3 -> 问题 4",
    "7 个阶段 · 3 条硬规则",
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


def candidate_hits(text: str) -> list[str]:
    hits: list[str] = []
    for pattern in CANDIDATE_PATTERNS:
        matches = pattern.findall(text)
        if matches:
            hits.extend(str(match) for match in matches)
    return sorted(set(hits))


def validate_data_range_zone(handoff: Handoff) -> None:
    if handoff.index != 6:
        return

    required_ideas = ("约束", "范围", "预算", "复杂度", "最坏")
    if not any(idea in handoff.block for idea in required_ideas):
        raise ValidationError(
            f"{handoff.location} 交接 6 没有留下范围或预算证据"
        )

    hits = candidate_hits(handoff.block)
    if hits:
        raise ValidationError(
            f"{handoff.location} 交接 6 提前出现具体方法或结构："
            + "、".join(hits)
        )


def validate_candidate_gate(chain: list[Handoff]) -> None:
    for handoff in chain[:7]:
        hits = candidate_hits(handoff.block)
        if hits:
            raise ValidationError(
                f"{handoff.location} 交接 {handoff.index} 在交接 8 前泄漏候选："
                + "、".join(hits)
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
        if index < 8:
            hits = candidate_hits(block)
            if hits:
                raise ValidationError(
                    f"site/assets/app.js 交接 {index} 在交接 8 前泄漏候选："
                    + "、".join(hits)
                )
        if index == 6 and not any(
            idea in block for idea in ("约束", "范围", "预算", "复杂度", "最坏")
        ):
            raise ValidationError("site/assets/app.js 交接 6 没有范围或预算证据")

    acceptance_start = script.find("function renderHumanAcceptanceStandard()")
    if acceptance_start < 0:
        raise ValidationError("site/assets/app.js 缺少九交接验收渲染函数")
    acceptance_tail = script[acceptance_start : acceptance_start + 1800]
    if "HANDOFFS.map" not in acceptance_tail:
        raise ValidationError("验收卡没有从唯一 HANDOFFS 数据生成")
    if "9 次交接 · 3 条硬规则" not in script:
        raise ValidationError("验收标题仍不是九次交接")


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

    concrete_range = fixture_chain(list(range(1, 10)))
    concrete_range[5] = Handoff(
        path=concrete_range[5].path,
        index=6,
        line=concrete_range[5].line,
        block=concrete_range[5].block + "\n这里应该使用 HashMap。",
    )
    expect_failure(
        "交接 6 出现具体结构",
        lambda: validate_data_range_zone(concrete_range[5]),
    )

    early_leak = fixture_chain(list(range(1, 10)))
    early_leak[2] = Handoff(
        path=early_leak[2].path,
        index=3,
        line=early_leak[2].line,
        block=early_leak[2].block + "\n下一步使用栈。",
    )
    expect_failure(
        "交接 8 前泄漏具体候选",
        lambda: validate_candidate_gate(early_leak),
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
    except ValidationError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    print(
        "OK: 九次交接、九字段、数据范围禁区、候选门槛和页面验收均已通过"
        f"（{total_chains} 条完整现场链）"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
