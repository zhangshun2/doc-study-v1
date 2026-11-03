#!/usr/bin/env python3
"""Insert one nine-field live evidence card before each diagnostic card.

The default mode is a dry run. Pass ``--apply`` to write the migrated files.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS_DIR))

from validate_human_reading import (  # noqa: E402
    COIN_CHANGE,
    CONTAINER,
    DAILY_TEMPERATURES,
    DEMO,
    HANDOFF_FIELDS,
    HUMAN_GUIDE,
    LIVE_FIRST_PREVIOUS_EVIDENCE,
    REAL_PROBLEM_TEMPLATE,
    STANDARD,
    TEMPLATE,
    TEXT_FENCE_RE,
    TWO_SUM,
    complete_chains,
    display_path,
    extract_handoffs,
    validate_document,
    validate_handoff_fields,
    validate_handoff_live_generation_card,
    validate_handoff_sequence,
    validate_live_handoff_chain,
)

PATHS = [
    STANDARD,
    HUMAN_GUIDE,
    DEMO,
    TEMPLATE,
    REAL_PROBLEM_TEMPLATE,
    TWO_SUM,
    CONTAINER,
    COIN_CHANGE,
    DAILY_TEMPERATURES,
]

EXPECTED_CHAINS = {
    STANDARD: 1,
    HUMAN_GUIDE: 4,
    DEMO: 1,
    TEMPLATE: 1,
    REAL_PROBLEM_TEMPLATE: 1,
    TWO_SUM: 1,
    CONTAINER: 1,
    COIN_CHANGE: 1,
    DAILY_TEMPERATURES: 1,
}

HUMAN_GUIDE_KINDS = {
    "两数之和": "事后校验",
    "每日温度": "事后重建",
    "盛最多水的容器": "事后重建",
    "零钱兑换": "事后重建",
}

DIRECT_KINDS = {
    STANDARD: "事后重建",
    DEMO: "事后重建",
    TEMPLATE: "事后重建",
    REAL_PROBLEM_TEMPLATE: "事后重建",
    TWO_SUM: "事后校验",
    CONTAINER: "事后重建",
    COIN_CHANGE: "事后重建",
    DAILY_TEMPERATURES: "事后重建",
}

LIVE_LABELS = [
    "现场类型：",
    "上一份证据：",
    "它已经能回答：",
    "它仍然不能回答：",
    "本步由上一份证据逼出的疑问：",
    "纸上动作：",
    "新增证据：",
    "新增证据仍不能回答：",
    "证据不足退回：",
]

FIRST_EVIDENCE_ANSWERS = (
    "可以逐句确认题目给了什么、要交回什么以及示例怎样走",
    "还不能把静态题面变成一个人可以照着执行的动作",
)


def field_value(card: str, field: str) -> str:
    match = re.search(rf"(?m)^{re.escape(field)}：(?P<value>.*)$", card)
    return match.group("value").strip() if match else ""


def is_blank(value: str) -> bool:
    return not value.strip("_ \t")


def chain_heading(text: str, absolute_start: int) -> str:
    heading_start = text.rfind("\n## ", 0, absolute_start)
    if heading_start < 0:
        return ""
    heading_end = text.find("\n", heading_start + 1)
    return text[heading_start + 1 : heading_end if heading_end >= 0 else None]


def narrative_type(path: Path, heading: str) -> str:
    if path in DIRECT_KINDS:
        return DIRECT_KINDS[path]
    if path == HUMAN_GUIDE:
        for title, kind in HUMAN_GUIDE_KINDS.items():
            if title in heading:
                return kind
    raise RuntimeError(f"{display_path(path)} 无法确定叙事类型：{heading}")


def diagnostic_card(handoff_block: str, location: str) -> re.Match[str]:
    for match in TEXT_FENCE_RE.finditer(handoff_block):
        body = match.group("body")
        if all(f"{field}：" in body for field in HANDOFF_FIELDS):
            return match
    raise RuntimeError(f"{location} 找不到完整九字段诊断卡")


def values_from_card(card: str, *, allow_blank: bool, location: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for field in HANDOFF_FIELDS:
        value = field_value(card, field)
        if is_blank(value) and not allow_blank:
            raise RuntimeError(f"{location} 的诊断字段为空：{field}")
        values[field] = value
    return values


def live_value(value: str, *, allow_blank: bool) -> str:
    if is_blank(value):
        if not allow_blank:
            raise RuntimeError("真实交接不能使用空白现场字段")
        return "______"
    return value


def build_live_card(
    current: dict[str, str],
    previous: dict[str, str] | None,
    kind: str,
    *,
    allow_blank: bool,
) -> str:
    if previous is None:
        previous_evidence = LIVE_FIRST_PREVIOUS_EVIDENCE
        previous_only, previous_cannot = FIRST_EVIDENCE_ANSWERS
    else:
        previous_evidence = live_value(
            previous["做完后新增了什么证据"], allow_blank=allow_blank
        )
        previous_only = live_value(
            previous["这份证据只能说明什么"], allow_blank=allow_blank
        )
        previous_cannot = live_value(
            previous["它还不能说明什么"], allow_blank=allow_blank
        )

    values = [
        kind,
        previous_evidence,
        previous_only,
        previous_cannot,
        live_value(
            current["本步由上一份证据逼出的疑问"], allow_blank=allow_blank
        ),
        live_value(current["纸上实际做了什么"], allow_blank=allow_blank),
        live_value(current["做完后新增了什么证据"], allow_blank=allow_blank),
        live_value(current["它还不能说明什么"], allow_blank=allow_blank),
        live_value(current["如果答不出，退回哪里"], allow_blank=allow_blank),
    ]
    return "\n".join(
        f"{label}{value}" for label, value in zip(LIVE_LABELS, values)
    )


def validate_migrated_chains(path: Path, text: str) -> None:
    handoffs = extract_handoffs(text, path)
    chains = complete_chains(handoffs)
    expected = EXPECTED_CHAINS[path]
    if len(chains) != expected:
        raise RuntimeError(
            f"{display_path(path)} 期望 {expected} 条完整链，实际 {len(chains)} 条"
        )

    allow_blank = path == REAL_PROBLEM_TEMPLATE
    for chain in chains:
        validate_handoff_sequence(chain)
        for handoff in chain:
            validate_handoff_fields(handoff)
            validate_handoff_live_generation_card(handoff)
        validate_live_handoff_chain(
            chain, allow_instructional_template=allow_blank
        )


def migrate_text(path: Path) -> tuple[str, int]:
    original = path.read_text(encoding="utf-8")
    text = original
    handoffs = extract_handoffs(text, path)
    chains = complete_chains(handoffs)
    expected = EXPECTED_CHAINS[path]
    if len(chains) != expected:
        raise RuntimeError(
            f"{display_path(path)} 期望 {expected} 条完整链，实际 {len(chains)} 条"
        )

    replacements: list[tuple[int, str]] = []
    allow_blank = path == REAL_PROBLEM_TEMPLATE
    for chain in chains:
        chain_start = text.find(chain[0].block)
        kind = narrative_type(path, chain_heading(text, chain_start))
        existing = [
            handoff
            for handoff in chain
            if "现场类型：" in handoff.block
        ]
        if len(existing) == len(chain):
            continue
        if existing:
            raise RuntimeError(
                f"{display_path(path)} 的 {kind} 链只迁移了一部分，拒绝覆盖"
            )

        previous: dict[str, str] | None = None
        for handoff in chain:
            match = diagnostic_card(
                handoff.block, f"{display_path(path)} 交接 {handoff.index}"
            )
            handoff_start = text.find(handoff.block)
            if handoff_start < 0:
                raise RuntimeError(
                    f"{display_path(path)} 交接 {handoff.index} 找不到原块"
                )
            current = values_from_card(
                match.group("body"),
                allow_blank=allow_blank,
                location=f"{display_path(path)} 交接 {handoff.index}",
            )
            card = build_live_card(
                current, previous, kind, allow_blank=allow_blank
            )
            insertion = (
                f"现场九字段（{kind}，只记录现场能确认的证据）：\n\n"
                f"```text\n{card}\n```\n\n"
                "完成后九字段诊断卡：\n\n"
            )
            absolute = handoff_start + match.start()
            replacements.append((absolute, insertion))
            previous = current

    for absolute, insertion in sorted(replacements, reverse=True):
        text = text[:absolute] + insertion + text[absolute:]

    validate_migrated_chains(path, text)
    return text, len(text) - len(original)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--apply",
        action="store_true",
        help="write validated cards; without this flag only preview",
    )
    args = parser.parse_args()

    migrated: list[tuple[Path, str, int]] = []
    for path in PATHS:
        text, delta = migrate_text(path)
        migrated.append((path, text, delta))
        mode = "更新" if args.apply and delta else "预演"
        print(f"{mode}: {display_path(path)} ({delta:+d} 字符)")

    if not args.apply:
        print("未写入。确认后运行：python3 <本脚本> --apply")
        return 0

    for path, text, delta in migrated:
        if delta:
            path.write_text(text, encoding="utf-8")

    for path, _text, delta in migrated:
        if delta:
            validate_document(path)
    print("迁移完成，并已通过逐文件复核。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
