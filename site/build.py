#!/usr/bin/env python3
"""Build the static algorithm learning site from the Obsidian source tree."""

from __future__ import annotations

import datetime as dt
import hashlib
import html
import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
SITE_DIR = ROOT / "site"
SOURCE_DIR = ROOT / "学习文库" / "算法学习"
OUTPUT_DIR = ROOT / "_site"

SKIP_DIRS = {".obsidian", "__pycache__"}
SKIP_FILES = {".DS_Store"}
TEMPLATE_PREFIX = "99-模板/"

TOPIC_ORDER = [
    "数组与哈希",
    "哈希表",
    "双指针",
    "滑动窗口",
    "二分查找",
    "字符串",
    "数学",
    "链表",
    "栈",
    "单调结构",
    "单调栈",
    "二叉树",
    "图与搜索",
    "图与广度优先",
    "回溯",
    "动态规划",
    "贪心",
    "排序",
    "堆与选择",
    "矩阵与模拟",
    "设计",
    "位运算",
]

CATEGORY_LABELS = {
    "guide": "总览",
    "dashboard": "学习看板",
    "map": "知识地图",
    "problems": "标准题解",
    "core": "核心模型",
    "models": "完整建模",
    "concepts": "概念专题",
    "comparisons": "跨题对照",
    "java": "Java 速查",
    "resources": "方法与资料",
}

GROUP_ORDER = [
    "guide",
    "dashboard",
    "map",
    "problems",
    "core",
    "models",
    "concepts",
    "comparisons",
    "java",
    "resources",
]


def relative_files(base: Path) -> list[Path]:
    files: list[Path] = []
    for path in base.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(base)
        if any(part in SKIP_DIRS for part in relative.parts):
            continue
        if path.name in SKIP_FILES:
            continue
        files.append(relative)
    return sorted(files, key=lambda item: item.as_posix())


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return ""
    if value.startswith("[") and value.endswith("]"):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return [part.strip().strip("\"'") for part in value[1:-1].split(",") if part.strip()]
    if value in {"null", "~"}:
        return None
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    return value.strip("\"'")


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---"):
        return {}, text
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    end = None
    for index in range(1, min(len(lines), 80)):
        if lines[index].strip() == "---":
            end = index
            break
    if end is None:
        return {}, text
    frontmatter: dict[str, Any] = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        frontmatter[key.strip()] = parse_scalar(value)
    return frontmatter, "\n".join(lines[end + 1 :]).lstrip()


def plain_text(markdown: str) -> str:
    text = re.sub(r"```[^\n]*\n?(.*?)```", r"\1", markdown, flags=re.DOTALL)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", text)
    text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"^[>#*\-\d.\s|]+", "", text, flags=re.MULTILINE)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def first_heading(markdown: str) -> str:
    match = re.search(r"^#\s+(.+?)\s*$", markdown, flags=re.MULTILINE)
    if not match:
        return ""
    return re.sub(r"[*_`]", "", match.group(1)).strip()


def headings(markdown: str) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for match in re.finditer(r"^(#{2,4})\s+(.+?)\s*$", markdown, flags=re.MULTILINE):
        label = re.sub(r"[*_`]", "", match.group(2)).strip()
        result.append({"level": len(match.group(1)), "text": label})
    return result


def excerpt(markdown: str) -> str:
    without_heading = re.sub(r"^#{1,6}\s+.*$", "", markdown, flags=re.MULTILINE)
    for block in re.split(r"\n\s*\n", without_heading):
        text = plain_text(block).strip()
        if len(text) < 24:
            continue
        if text.startswith(("|", "```")):
            continue
        return re.sub(r"\s+", " ", text)[:180]
    return ""


def problem_number(path: str) -> int:
    match = re.match(r"(\d+)", Path(path).name)
    return int(match.group(1)) if match else 10**9


def classify(relative: str) -> tuple[str, str]:
    parts = Path(relative).parts
    first = parts[0] if parts else ""
    if first == "题目":
        topic = parts[1] if len(parts) > 1 else "未分类"
        return "problems", topic
    if first == "核心模型":
        topic = parts[1] if len(parts) > 1 else "未分类"
        return "core", topic
    if first == "建模专题":
        if len(parts) > 1 and parts[1] == "T0":
            return "models", "T0 完整建模"
        return "resources", "建模维护"
    if first == "02-概念专题":
        return "concepts", "搜索与回溯"
    if first == "04-跨题对照":
        return "comparisons", "跨题对照"
    if first == "Java速查":
        topic = parts[1] if len(parts) > 1 else "总览"
        return "java", topic
    if first == "学习看板":
        return "dashboard", "复习"
    if first == "01-地图":
        return "map", "知识地图"
    if first == "03-资料":
        return "resources", "方法与资料"
    return "guide", "总览"


def nav_item(path: str, docs: dict[str, dict[str, Any]]) -> dict[str, Any]:
    doc = docs[path]
    return {
        "path": path,
        "title": doc["title"],
        "category": doc["category"],
        "categoryLabel": doc["categoryLabel"],
        "topic": doc["topic"],
    }


def build_nav(docs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    def items(paths: list[str]) -> list[dict[str, Any]]:
        return [nav_item(path, docs) for path in paths if path in docs]

    problem_topics: list[dict[str, Any]] = []
    problem_paths = [path for path, doc in docs.items() if doc["category"] == "problems"]
    for topic in sorted(
        {docs[path]["topic"] for path in problem_paths},
        key=lambda value: (
            TOPIC_ORDER.index(value) if value in TOPIC_ORDER else len(TOPIC_ORDER),
            value,
        ),
    ):
        topic_paths = sorted(
            [path for path in problem_paths if docs[path]["topic"] == topic],
            key=lambda path: (problem_number(path), docs[path]["title"]),
        )
        problem_topics.append({"label": topic, "items": items(topic_paths)})

    core_paths = sorted(
        [path for path, doc in docs.items() if doc["category"] == "core"],
        key=lambda path: path,
    )
    model_paths = sorted(
        [path for path, doc in docs.items() if doc["category"] == "models"],
        key=lambda path: (problem_number(path), path),
    )
    concept_paths = sorted(
        [path for path, doc in docs.items() if doc["category"] == "concepts"],
        key=lambda path: path,
    )
    comparison_paths = sorted(
        [path for path, doc in docs.items() if doc["category"] == "comparisons"],
        key=lambda path: path,
    )
    java_paths = sorted(
        [path for path, doc in docs.items() if doc["category"] == "java"],
        key=lambda path: path,
    )
    resource_paths = sorted(
        [path for path, doc in docs.items() if doc["category"] == "resources"],
        key=lambda path: path,
    )

    return [
        {
            "id": "start",
            "label": "开始",
            "items": items(
                [
                    "README.md",
                    "00-首页.md",
                    "学习看板/README.md",
                    "01-地图/算法知识地图.md",
                    "03-资料/高效理解与回忆方法.md",
                ]
            ),
        },
        {
            "id": "problems",
            "label": "题库",
            "topics": problem_topics,
        },
        {
            "id": "core",
            "label": "核心模型",
            "items": items(core_paths),
        },
        {
            "id": "models",
            "label": "完整建模",
            "items": items(model_paths),
        },
        {
            "id": "concepts",
            "label": "概念专题",
            "items": items(concept_paths),
        },
        {
            "id": "comparisons",
            "label": "跨题对照",
            "items": items(comparison_paths),
        },
        {
            "id": "java",
            "label": "Java 速查",
            "items": items(java_paths),
        },
        {
            "id": "resources",
            "label": "方法与资料",
            "items": items(resource_paths),
        },
    ]


def build_manifest(docs: dict[str, dict[str, Any]]) -> dict[str, Any]:
    problems = [doc for doc in docs.values() if doc["category"] == "problems"]
    public_docs = {
        path: {key: value for key, value in doc.items() if key != "searchText"}
        for path, doc in docs.items()
    }
    problem_count = len(problems)
    core_count = sum(doc["category"] == "core" for doc in docs.values())
    model_count = sum(doc["category"] == "models" for doc in docs.values())
    concept_count = sum(
        doc["category"] == "concepts" and Path(doc["path"]).name != "README.md"
        for doc in docs.values()
    )
    comparison_count = sum(
        doc["category"] == "comparisons" and Path(doc["path"]).name != "README.md"
        for doc in docs.values()
    )
    java_count = sum(
        doc["category"] == "java" and Path(doc["path"]).name != "00-索引.md"
        for doc in docs.values()
    )
    review_due = [
        doc["path"]
        for doc in problems
        if doc.get("reviewStatus") == "待复习"
    ]
    independent = [
        doc["path"]
        for doc in problems
        if doc.get("mastery") == "可独立实现"
    ]
    transferable = [
        doc["path"]
        for doc in problems
        if doc.get("mastery") == "可迁移"
    ]

    try:
        revision = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        revision = "local"

    return {
        "title": "算法学习库",
        "subtitle": "从理解、复述到独立实现与迁移",
        "generatedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
        "revision": revision,
        "sourceLabel": "学习文库/算法学习",
        "homepage": "README.md",
        "stats": {
            "problems": problem_count,
            "core": core_count,
            "models": model_count,
            "concepts": concept_count,
            "comparisons": comparison_count,
            "java": java_count,
            "documents": len(public_docs),
            "reviewDue": len(review_due),
            "independent": len(independent),
            "transferable": len(transferable),
        },
        "review": {
            "due": review_due,
            "independent": independent,
            "transferable": transferable,
        },
        "nav": build_nav(docs),
        "docs": public_docs,
    }


def build_search_index(docs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    index: list[dict[str, Any]] = []
    for doc in sorted(docs.values(), key=lambda item: item["path"]):
        if doc.get("isTemplate"):
            continue
        index.append(
            {
                "path": doc["path"],
                "title": doc["title"],
                "category": CATEGORY_LABELS.get(doc["category"], doc["category"]),
                "topic": doc["topic"],
                "headings": [heading["text"] for heading in doc["headings"]],
                "text": doc["searchText"],
            }
        )
    return index


def write_json(path: Path, value: Any, pretty: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if pretty:
        payload = json.dumps(value, ensure_ascii=False, indent=2)
    else:
        payload = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    path.write_text(payload + "\n", encoding="utf-8")


def asset_version() -> str:
    digest = hashlib.sha256()
    for path in sorted((SITE_DIR / "assets").rglob("*")):
        if not path.is_file():
            continue
        digest.update(path.relative_to(SITE_DIR).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()[:10]


def copy_site_files() -> None:
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    shutil.copytree(SITE_DIR / "assets", OUTPUT_DIR / "assets")
    index = (SITE_DIR / "index.html").read_text(encoding="utf-8")
    (OUTPUT_DIR / "index.html").write_text(
        index.replace("__ASSET_VERSION__", asset_version()),
        encoding="utf-8",
    )
    for relative in relative_files(SOURCE_DIR):
        source = SOURCE_DIR / relative
        target = OUTPUT_DIR / "content" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def collect_docs() -> dict[str, dict[str, Any]]:
    docs: dict[str, dict[str, Any]] = {}
    for relative_path in relative_files(SOURCE_DIR):
        if relative_path.suffix.lower() != ".md":
            continue
        relative = relative_path.as_posix()
        if relative.startswith(TEMPLATE_PREFIX):
            continue
        markdown = (SOURCE_DIR / relative_path).read_text(encoding="utf-8")
        frontmatter, body = parse_frontmatter(markdown)
        category, topic = classify(relative)
        title = first_heading(body) or frontmatter.get("titleCn") or relative_path.stem
        text = plain_text(body)
        docs[relative] = {
            "path": relative,
            "title": str(title),
            "category": category,
            "categoryLabel": CATEGORY_LABELS.get(category, category),
            "topic": topic,
            "headings": headings(body),
            "excerpt": excerpt(body),
            "searchText": text[:12000],
            "type": frontmatter.get("type"),
            "mastery": frontmatter.get("mastery"),
            "reviewStatus": frontmatter.get("reviewStatus"),
            "nextReview": frontmatter.get("nextReview"),
            "lastReviewed": frontmatter.get("lastReviewed"),
            "topics": frontmatter.get("topics") or [],
            "sourceUrl": frontmatter.get("sourceUrl"),
            "isTemplate": relative.startswith(TEMPLATE_PREFIX),
        }
    return docs


def main() -> None:
    docs = collect_docs()
    manifest = build_manifest(docs)
    search_index = build_search_index(docs)
    copy_site_files()
    write_json(OUTPUT_DIR / "assets" / "manifest.json", manifest)
    write_json(OUTPUT_DIR / "assets" / "search.json", search_index)
    print(
        f"Built {len(docs)} documents into {OUTPUT_DIR} "
        f"({manifest['stats']['problems']} problems, {output_size(OUTPUT_DIR)})."
    )


def output_size(path: Path) -> str:
    total = sum(item.stat().st_size for item in path.rglob("*") if item.is_file())
    if total >= 1024 * 1024:
        return f"{total / 1024 / 1024:.1f} MB"
    return f"{total / 1024:.0f} KB"


if __name__ == "__main__":
    main()
