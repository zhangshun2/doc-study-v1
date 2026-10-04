#!/usr/bin/env python3
"""Migrate the algorithm library documents from schema v2 to schema v3.

The migration is intentionally mechanical:

* enrich problems.json with normalized source-fact hashes;
* add schema-v3 learning and navigation properties to standard solutions;
* add schema-v3 properties to the T0 modeling documents;
* keep all existing explanatory prose unchanged.
"""

from __future__ import annotations

import hashlib
import html
import json
import re
from pathlib import Path
from typing import Any


LIBRARY_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = LIBRARY_ROOT / "problems.json"
PROBLEMS_ROOT = LIBRARY_ROOT / "题目"
MODELING_ROOT = LIBRARY_ROOT / "建模专题" / "T0"
CORE_ROOT = LIBRARY_ROOT / "核心模型"

MASTERY = "已理解"
REVIEW_STATUS = "未安排"


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def decode_html_entities(value: str) -> str:
    named = {
        "nbsp": " ",
        "amp": "&",
        "lt": "<",
        "gt": ">",
        "quot": '"',
        "apos": "'",
        "#39": "'",
        "hellip": "...",
        "times": "x",
        "minus": "-",
        "le": "<=",
        "ge": ">=",
    }

    def decode_entity(match: re.Match[str]) -> str:
        token = match.group(1)
        if token.startswith("#x"):
            return chr(int(token[2:], 16))
        if token.startswith("#"):
            return chr(int(token[1:]))
        return named.get(token.lower(), match.group(0))

    return re.sub(r"&(#x[0-9a-fA-F]+|#\d+|[A-Za-z]+);", decode_entity, value)


def inline_text(value: str) -> str:
    text = re.sub(r"<br\s*/?>", "\n", value, flags=re.I)
    text = re.sub(
        r"<sup[^>]*>([\s\S]*?)</sup>",
        lambda match: "^" + inline_text(match.group(1)),
        text,
        flags=re.I,
    )
    text = re.sub(
        r"<sub[^>]*>([\s\S]*?)</sub>",
        lambda match: "_" + inline_text(match.group(1)),
        text,
        flags=re.I,
    )
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("\u00a0", " ")
    return text


def html_to_text(value: str) -> str:
    pre_blocks: list[str] = []

    def replace_pre(match: re.Match[str]) -> str:
        inner = decode_html_entities(
            inline_text(match.group(1)).strip().rstrip()
        )
        pre_blocks.append(f"```text\n{inner}\n```")
        return f"\n\n@@PRE_BLOCK_{len(pre_blocks) - 1}@@\n\n"

    text = re.sub(
        r"<pre\b[^>]*>([\s\S]*?)</pre>",
        replace_pre,
        value,
        flags=re.I,
    )
    text = re.sub(
        r"<img\b[^>]*src=[\"']([^\"']+)[\"'][^>]*>",
        lambda match: (
            f"\n\n![Official problem illustration]"
            f"({decode_html_entities(match.group(1))})\n\n"
        ),
        text,
        flags=re.I,
    )
    text = re.sub(
        r"<a\b[^>]*href=[\"']([^\"']+)[\"'][^>]*>([\s\S]*?)</a>",
        lambda match: (
            f"[{inline_text(match.group(2)).strip()}]"
            f"({decode_html_entities(match.group(1))})"
        ),
        text,
        flags=re.I,
    )
    text = re.sub(
        r"<code\b[^>]*>([\s\S]*?)</code>",
        lambda match: f"`{inline_text(match.group(1)).strip()}`",
        text,
        flags=re.I,
    )
    text = re.sub(
        r"<strong\b[^>]*>([\s\S]*?)</strong>",
        lambda match: f"**{inline_text(match.group(1)).strip()}**",
        text,
        flags=re.I,
    )
    text = re.sub(
        r"<em\b[^>]*>([\s\S]*?)</em>",
        lambda match: f"*{inline_text(match.group(1)).strip()}*",
        text,
        flags=re.I,
    )
    text = re.sub(
        r"<sup\b[^>]*>([\s\S]*?)</sup>",
        lambda match: "^" + inline_text(match.group(1)),
        text,
        flags=re.I,
    )
    text = re.sub(
        r"<sub\b[^>]*>([\s\S]*?)</sub>",
        lambda match: "_" + inline_text(match.group(1)),
        text,
        flags=re.I,
    )
    text = re.sub(
        r"<li\b[^>]*>([\s\S]*?)</li>",
        lambda match: f"\n- {inline_text(match.group(1)).strip()}\n",
        text,
        flags=re.I,
    )
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
    text = re.sub(
        r"</(?:p|div|ul|ol|blockquote|h[1-6])>",
        "\n\n",
        text,
        flags=re.I,
    )
    text = re.sub(
        r"<(?:p|div|ul|ol|blockquote|h[1-6])\b[^>]*>",
        "",
        text,
        flags=re.I,
    )
    text = re.sub(r"<[^>]+>", "", text)
    text = decode_html_entities(text).replace("\u00a0", " ")
    text = re.sub(
        r"@@PRE_BLOCK_(\d+)@@",
        lambda match: pre_blocks[int(match.group(1))],
        text,
    )
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def split_official_sections(problem: dict[str, Any]) -> dict[str, str]:
    markdown = html_to_text(problem.get("translatedContentHtml") or "")
    lines = markdown.splitlines()
    first_example = next(
        (
            index
            for index, line in enumerate(lines)
            if re.match(r"^(?:\*\*\s*)?示例(?:\s*\d+)?[：:](?:\s*\*\*)?$", line.strip())
        ),
        -1,
    )
    constraints = next(
        (
            index
            for index, line in enumerate(lines)
            if re.match(r"^(?:\*\*\s*)?(?:提示|约束)[：:](?:\s*\*\*)?$", line.strip())
        ),
        -1,
    )
    description_end = first_example if first_example >= 0 else constraints
    if description_end < 0:
        description_end = len(lines)
    examples_end = constraints if constraints >= 0 else len(lines)

    return {
        "description": "\n".join(lines[:description_end]).strip(),
        "examplesMarkdown": (
            "\n".join(lines[first_example:examples_end]).strip()
            if first_example >= 0
            else ""
        ),
        "constraints": (
            "\n".join(lines[constraints + 1 :]).strip()
            if constraints >= 0
            else ""
        ),
    }


def source_hashes(problem: dict[str, Any]) -> tuple[str, dict[str, str]]:
    split = split_official_sections(problem)
    sections = {
        "description": sha256_text(split["description"]),
        "examples": sha256_text(canonical_json(problem.get("officialExamples") or [])),
        "constraints": sha256_text(split["constraints"]),
        "hints": sha256_text(canonical_json(problem.get("officialHints") or [])),
        "tags": sha256_text(canonical_json(problem.get("officialTags") or [])),
        "signature": sha256_text(canonical_json(problem.get("signature") or {})),
        "javaTemplate": sha256_text(problem.get("javaTemplate") or ""),
    }
    facts = {
        "id": problem["id"],
        "slug": problem["slug"],
        "titleCn": problem["titleCn"],
        "titleEn": problem["titleEn"],
        "difficulty": problem["difficulty"],
        "sourceUrl": problem["sourceUrl"],
        **sections,
    }
    return sha256_text(canonical_json(facts)), sections


def parse_frontmatter(markdown: str) -> tuple[dict[str, Any], str]:
    match = re.match(r"\A---\r?\n([\s\S]*?)\r?\n---\r?\n", markdown)
    if not match:
        return {}, markdown

    result: dict[str, Any] = {}
    for line in match.group(1).splitlines():
        field = re.match(r"^([A-Za-z][A-Za-z0-9]*):\s*(.*)$", line)
        if not field:
            continue
        key, raw = field.groups()
        try:
            result[key] = json.loads(raw)
        except json.JSONDecodeError:
            result[key] = raw
    return result, markdown[match.end() :]


def yaml_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, (int, float)):
        return str(value)
    return json.dumps(str(value), ensure_ascii=False)


def frontmatter(
    values: dict[str, Any],
    source_sections: dict[str, str] | None = None,
) -> str:
    lines = ["---"]
    for key, value in values.items():
        if key == "sourceSectionHashes" and source_sections is not None:
            lines.append("sourceSectionHashes:")
            for section_name, section_hash in source_sections.items():
                lines.append(f"  {section_name}: {yaml_scalar(section_hash)}")
        elif isinstance(value, list):
            lines.append(f"{key}: {canonical_json(value)}")
        else:
            lines.append(f"{key}: {yaml_scalar(value)}")
    lines.append("---")
    return "\n".join(lines)


def normalized_priority(problem: dict[str, Any]) -> str:
    priorities = problem.get("checklistPriorities") or []
    return priorities[0] if priorities else "P2"


def topic_names(problem: dict[str, Any]) -> list[str]:
    names = [problem["primaryPattern"]]
    for tag in problem.get("officialTags") or []:
        name = tag.get("translatedName") or tag.get("name")
        if name and name not in names:
            names.append(name)
    return names


def standard_values(
    problem: dict[str, Any],
    old: dict[str, Any],
    source_hash: str,
    source_sections: dict[str, str],
) -> dict[str, Any]:
    return {
        "schemaVersion": 3,
        "type": "problem",
        "leetcodeId": problem["id"],
        "slug": problem["slug"],
        "titleCn": problem["titleCn"],
        "titleEn": problem["titleEn"],
        "difficulty": problem["difficulty"],
        "sourceUrl": problem["sourceUrl"],
        "sourceCheckedAt": problem["sourceCheckedAt"],
        "sourceContentSha256": problem["sourceContentSha256"],
        "sourceFactsSha256": source_hash,
        "sourceSectionHashes": source_sections,
        "primaryPattern": problem["primaryPattern"],
        "topics": topic_names(problem),
        "priority": normalized_priority(problem),
        "checklistPriorities": problem.get("checklistPriorities") or [],
        "checklistTags": problem.get("checklistTags") or [],
        "mastery": old.get("mastery", MASTERY),
        "reviewStatus": old.get("reviewStatus", REVIEW_STATUS),
        "nextReview": old.get("nextReview"),
        "lastReviewed": old.get("lastReviewed"),
        "errorTags": old.get("errorTags", []),
        "independentAttempts": old.get("independentAttempts", 0),
    }


def modeling_values(
    problem: dict[str, Any],
    source_hash: str,
    source_sections: dict[str, str],
) -> dict[str, Any]:
    return {
        "schemaVersion": 3,
        "type": "modeling-topic",
        "leetcodeId": problem["id"],
        "slug": problem["slug"],
        "titleCn": problem["titleCn"],
        "titleEn": problem["titleEn"],
        "difficulty": problem["difficulty"],
        "sourceUrl": problem["sourceUrl"],
        "sourceCheckedAt": problem["sourceCheckedAt"],
        "sourceFactsSha256": source_hash,
        "sourceSectionHashes": source_sections,
        "primaryPattern": problem["primaryPattern"],
        "topics": topic_names(problem),
        "priority": normalized_priority(problem),
        "sourceProblem": problem["relativePath"],
        "mastery": MASTERY,
        "reviewStatus": REVIEW_STATUS,
        "nextReview": None,
        "lastReviewed": None,
        "errorTags": [],
        "independentAttempts": 0,
    }


def replace_or_insert_after_title(markdown: str, block: str) -> str:
    title = re.search(r"^# .+$", markdown, re.M)
    if not title:
        raise ValueError("document title is missing")
    cleaned = re.sub(
        r"\n> \*\*双轨入口：\*\*[\s\S]*?(?=\n## )",
        "\n",
        markdown,
    )
    title = re.search(r"^# .+$", cleaned, re.M)
    assert title is not None
    return (
        cleaned[: title.end()]
        + "\n\n"
        + block
        + cleaned[title.end() :]
    )


def replace_section(markdown: str, heading: str, body: str) -> str:
    pattern = re.compile(
        rf"(^##\s+{re.escape(heading)}\s*$)"
        r"([\s\S]*?)(?=^##\s+|\Z)",
        re.M,
    )
    if not pattern.search(markdown):
        raise ValueError(f"section is missing: {heading}")
    return pattern.sub(
        lambda match: f"{match.group(1)}\n\n{body.strip()}\n\n",
        markdown,
        count=1,
    )


def official_hints_markdown(problem: dict[str, Any]) -> str:
    hints = problem.get("officialHints") or []
    if not hints:
        return "- 当前官方接口未提供额外算法提示。"
    rendered = [
        f"{index}. {html_to_text(hint)}"
        for index, hint in enumerate(hints, start=1)
    ]
    return "\n".join(
        [
            "> 以下内容来自官方接口的额外提示字段；保留接口返回语言，"
            "不把学习提示冒充为官方提示。",
            "",
            *rendered,
        ]
    )


def refresh_official_sections(markdown: str, problem: dict[str, Any]) -> str:
    official = split_official_sections(problem)
    markdown = replace_section(
        markdown,
        "官方题意（LeetCode 中文题面）",
        "\n".join(
            [
                "> 以下题意由官方中文题面快照转换为 Markdown；"
                "来源、核验日期和内容哈希见上方元信息。",
                "",
                official["description"],
            ]
        ),
    )
    markdown = replace_section(
        markdown,
        "官方示例",
        official["examplesMarkdown"] or "官方题面未单独列出示例。",
    )
    markdown = replace_section(
        markdown,
        "官方约束",
        official["constraints"] or "官方题面未单独列出约束。",
    )
    markdown = replace_section(
        markdown,
        "官方额外提示",
        official_hints_markdown(problem),
    )
    return markdown


def insert_modeling_code_note(markdown: str, standard_link: str) -> str:
    heading_match = re.search(r"^##\s+16\..*$", markdown, re.M)
    if not heading_match:
        return markdown
    next_heading = re.search(r"^##\s+", markdown[heading_match.end() :], re.M)
    insertion_end = (
        heading_match.end() + next_heading.start()
        if next_heading
        else len(markdown)
    )
    section = markdown[heading_match.end() : insertion_end]
    if "权威实现见" in section:
        return markdown
    note = (
        "\n\n> 本节代码用于串联模型与实现；可提交、可运行的权威版本见 "
        f"{standard_link}。"
    )
    return markdown[: heading_match.end()] + note + markdown[heading_match.end() :]


def main() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    problems = manifest["problems"]
    problem_by_id = {int(problem["id"]): problem for problem in problems}
    source_hash_by_id: dict[int, str] = {}
    source_sections_by_id: dict[int, dict[str, str]] = {}

    for problem in problems:
        source_hash, source_sections = source_hashes(problem)
        problem["sourceFactsSha256"] = source_hash
        problem["sourceSectionHashes"] = source_sections
        source_hash_by_id[int(problem["id"])] = source_hash
        source_sections_by_id[int(problem["id"])] = source_sections

    MANIFEST_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    modeling_by_id = {
        int(match.group(1)): path
        for path in MODELING_ROOT.glob("*.md")
        if (match := re.match(r"^(\d+)-", path.name))
    }

    for problem in problems:
        problem_id = int(problem["id"])
        standard_path = LIBRARY_ROOT / problem["relativePath"]
        standard_markdown = standard_path.read_text(encoding="utf-8")
        old_frontmatter, standard_body = parse_frontmatter(standard_markdown)
        core_relative = (
            Path("核心模型")
            / problem["primaryPattern"]
            / f"{standard_path.stem}-核心模型.md"
        )
        links = [f"[[{core_relative.as_posix()}|核心模型]]"]
        if problem_id in modeling_by_id:
            deep_relative = modeling_by_id[problem_id].relative_to(LIBRARY_ROOT)
            links.append(f"[[{deep_relative.as_posix()}|完整建模]]")
        entry_line = "> **双轨入口：** " + " · ".join(links)
        standard_body = replace_or_insert_after_title(standard_body, entry_line)
        standard_body = refresh_official_sections(standard_body, problem)
        standard_path.write_text(
            frontmatter(
                standard_values(
                    problem,
                    old_frontmatter,
                    source_hash_by_id[problem_id],
                    source_sections_by_id[problem_id],
                ),
                source_sections_by_id[problem_id],
            )
            + "\n"
            + standard_body.lstrip("\n"),
            encoding="utf-8",
        )

    for problem_id, modeling_path in sorted(modeling_by_id.items()):
        problem = problem_by_id[problem_id]
        markdown = modeling_path.read_text(encoding="utf-8")
        _, body = parse_frontmatter(markdown)
        standard_relative = problem["relativePath"]
        core_relative = (
            Path("核心模型")
            / problem["primaryPattern"]
            / f"{Path(standard_relative).stem}-核心模型.md"
        )
        entry_line = (
            f"> **双轨入口：** [[{standard_relative}|标准题解]]"
            f" · [[{core_relative.as_posix()}|核心模型]]"
        )
        body = replace_or_insert_after_title(body, entry_line)
        body = insert_modeling_code_note(
            body,
            f"[[{standard_relative}|标准题解 Java 实现]]",
        )
        modeling_path.write_text(
            frontmatter(
                modeling_values(
                    problem,
                    source_hash_by_id[problem_id],
                    source_sections_by_id[problem_id],
                ),
                source_sections_by_id[problem_id],
            )
            + "\n"
            + body.lstrip("\n"),
            encoding="utf-8",
        )

    CORE_ROOT.mkdir(parents=True, exist_ok=True)
    print(f"Migrated {len(problems)} standard solutions.")
    print(f"Migrated {len(modeling_by_id)} modeling documents.")
    print(f"Enriched {MANIFEST_PATH}.")


if __name__ == "__main__":
    main()
