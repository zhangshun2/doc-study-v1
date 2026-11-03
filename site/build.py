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
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
SITE_DIR = ROOT / "site"
SOURCE_DIR = ROOT / "学习文库" / "算法学习"
REVIEW_DIR = ROOT / "LeetCode-系统复习"
EXPERIMENT_PATH = (
    REVIEW_DIR / "07-分析法实验" / "analysis-experiments.json"
)
OUTPUT_DIR = ROOT / "_site"
SOURCE_ROOTS = [
    (SOURCE_DIR, ""),
    (REVIEW_DIR, "LeetCode-系统复习/"),
]

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
    "review": "系统复习",
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
    "review",
]

REVIEW_TOPIC_ORDER = [
    "总入口",
    "复习计划",
    "单题流程",
    "学习记录",
    "分析法实验",
    "基础公开课",
    "标签公开课",
    "Hot 100 题单",
    "学习基准",
]

REVIEW_TOPIC_LABELS = {
    "01-复习计划": "复习计划",
    "02-基础公开课": "基础公开课",
    "03-标签公开课": "标签公开课",
    "04-Hot100题单": "Hot 100 题单",
    "05-单题流程": "单题流程",
    "06-学习记录": "学习记录",
    "07-分析法实验": "分析法实验",
    "99-Skill": "学习基准",
}

DIFFICULTY_ORDER = ["Easy", "Medium", "Hard"]

SYSTEM_VIEWS = [
    {
        "id": "query-index",
        "label": "查询、历史与索引",
        "description": "反复回答“以前是否出现、前缀是什么、目标落在哪里”。",
        "patterns": {"数组与哈希", "哈希表"},
    },
    {
        "id": "sequence-window",
        "label": "顺序、窗口与区间",
        "description": "连续区间只从两端增删，或只需维护一段正在观察的范围。",
        "patterns": {"滑动窗口", "字符串", "排序", "矩阵与模拟"},
    },
    {
        "id": "execution-order",
        "label": "表达式、括号与执行顺序",
        "description": "后来的符号必须先于前面的对象结算，或需要显式保存执行现场。",
        "patterns": {"栈"},
    },
    {
        "id": "frontier",
        "label": "前沿、极值与候选淘汰",
        "description": "只关心当前最值得处理的一端，或一次比较就能排除一批候选。",
        "patterns": {"双指针", "单调结构", "单调栈", "贪心"},
    },
    {
        "id": "selection",
        "label": "选择、排序与第 K 个",
        "description": "答案由顺序、分界位置或候选集合中的前若干名决定。",
        "patterns": {"二分查找", "堆与选择"},
    },
    {
        "id": "state-reuse",
        "label": "状态、转移与子问题复用",
        "description": "同一更小问题从多条路径重复到达，保存结果后按依赖顺序复用。",
        "patterns": {"动态规划"},
    },
    {
        "id": "search-reachability",
        "label": "图、搜索与可达性",
        "description": "对象之间存在转移关系，需要寻找路径、连通块、排列或合法构造。",
        "patterns": {"图与搜索", "图与广度优先", "回溯"},
    },
    {
        "id": "recursive-hierarchy",
        "label": "递归、层次与树结构",
        "description": "问题由相同形状的更小部分组成，当前层依赖子结果或父子关系。",
        "patterns": {"链表", "二叉树"},
    },
    {
        "id": "design-transform",
        "label": "设计、变换与操作约束",
        "description": "重点不是单一答案，而是一组操作、状态边界或输入输出的重新表达。",
        "patterns": {"设计", "数学", "位运算"},
    },
]

SYSTEM_VIEW_BY_PATTERN = {
    pattern: view
    for view in SYSTEM_VIEWS
    for pattern in view["patterns"]
}


class FragmentTextExtractor(HTMLParser):
    """Extract readable text and list items without adding a parser dependency."""

    BLOCK_TAGS = {"br", "p", "li", "pre", "ul", "ol", "div"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.items: list[str] = []
        self._item_parts: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in self.BLOCK_TAGS:
            self.parts.append("\n")
        if tag == "sup":
            self.parts.append("^")
            if self._item_parts is not None:
                self._item_parts.append("^")
        if tag == "li":
            self._item_parts = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "li" and self._item_parts is not None:
            item = re.sub(r"\s+", " ", "".join(self._item_parts)).strip()
            if item:
                self.items.append(item)
            self._item_parts = None
        if tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        self.parts.append(data)
        if self._item_parts is not None:
            self._item_parts.append(data)

    @property
    def text(self) -> str:
        value = "".join(self.parts).replace("\xa0", " ")
        lines = [re.sub(r"[ \t]+", " ", line).strip() for line in value.splitlines()]
        return "\n".join(line for line in lines if line)


def html_fragment_text(fragment: str) -> str:
    parser = FragmentTextExtractor()
    parser.feed(fragment)
    parser.close()
    return parser.text


def html_fragment_items(fragment: str) -> list[str]:
    parser = FragmentTextExtractor()
    parser.feed(fragment)
    parser.close()
    return parser.items


def unique_strings(values: list[Any]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = str(value).strip() if value is not None else ""
        if not text or text in seen:
            continue
        seen.add(text)
        result.append(text)
    return result


def split_official_html(content: str) -> dict[str, str]:
    example = re.search(
        r"<p[^>]*>\s*<strong[^>]*>\s*示例",
        content,
        flags=re.IGNORECASE,
    )
    constraints = re.search(
        r"(?:<p[^>]*>\s*)?<strong[^>]*>\s*提示\s*[：:]\s*</strong>",
        content,
        flags=re.IGNORECASE,
    )
    advanced = re.search(
        r"(?:<p[^>]*>\s*)?<strong[^>]*>\s*进阶\s*[：:]\s*</strong>",
        content,
        flags=re.IGNORECASE,
    )

    description_end = min(
        [
            match.start()
            for match in (example, constraints)
            if match is not None
        ]
        or [len(content)]
    )
    constraints_start = constraints.end() if constraints else description_end
    constraints_end = advanced.start() if advanced else len(content)
    advanced_start = advanced.end() if advanced else len(content)

    return {
        "descriptionHtml": content[:description_end].strip(),
        "constraintsHtml": content[constraints_start:constraints_end].strip(),
        "advancedHtml": content[advanced_start:].strip() if advanced else "",
    }


def complexity_sentences(text: str) -> list[str]:
    result: list[str] = []
    for sentence in re.split(r"[。；\n]+", text):
        normalized = re.sub(r"\s+", " ", sentence).strip()
        if not normalized:
            continue
        if "复杂度" not in normalized and not re.search(r"\bO\s*\(", normalized):
            continue
        if normalized not in result:
            result.append(normalized)
    return result


def first_matching_anchor(doc: dict[str, Any], candidates: list[str]) -> str:
    headings_list = [item["text"] for item in doc.get("headings") or []]
    for candidate in candidates:
        for heading in headings_list:
            if candidate in heading:
                return heading
    return ""


def build_fact_bank(
    problems_payload: dict[str, Any],
    docs: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    for problem in problems_payload.get("problems") or []:
        sections = split_official_html(problem.get("translatedContentHtml") or "")
        description_text = html_fragment_text(sections["descriptionHtml"])
        advanced_text = html_fragment_text(sections["advancedHtml"])
        required_complexity = complexity_sentences(description_text)
        advanced_complexity = complexity_sentences(advanced_text)
        solution_path = str(problem.get("relativePath") or "")
        solution_doc = docs.get(solution_path)
        official_tags = []
        seen_tags: set[str] = set()
        for tag in problem.get("officialTags") or []:
            translated = str(tag.get("translatedName") or tag.get("name") or "").strip()
            if not translated or translated in seen_tags:
                continue
            seen_tags.add(translated)
            official_tags.append(
                {
                    "name": str(tag.get("name") or translated),
                    "translatedName": translated,
                    "slug": str(tag.get("slug") or ""),
                }
            )

        pattern = str(problem.get("primaryPattern") or "未分类")
        system_view = SYSTEM_VIEW_BY_PATTERN.get(
            pattern,
            {
                "id": "design-transform",
                "label": "设计、变换与操作约束",
            },
        )
        solution_links = None
        if solution_doc:
            solution_links = {
                "path": solution_path,
                "title": solution_doc["title"],
                "reasoningAnchor": first_matching_anchor(
                    solution_doc,
                    ["核心观察", "最优方案推导", "最优方案"],
                ),
                "answerAnchor": first_matching_anchor(
                    solution_doc,
                    ["正确性与不变量", "复杂度", "最优方案推导"],
                ),
                "codeAnchor": first_matching_anchor(
                    solution_doc,
                    ["Java 实现", "LeetCode 可直接提交代码"],
                ),
            }

        records.append(
            {
                "id": problem.get("id"),
                "slug": problem.get("slug"),
                "titleCn": problem.get("titleCn"),
                "titleEn": problem.get("titleEn"),
                "difficulty": problem.get("difficulty"),
                "sourceUrl": problem.get("sourceUrl"),
                "sourceCheckedAt": problem.get("sourceCheckedAt"),
                "primaryPattern": pattern,
                "priorities": unique_strings(problem.get("checklistPriorities") or []),
                "checklistTags": unique_strings(problem.get("checklistTags") or []),
                "officialTags": official_tags,
                "descriptionHtml": sections["descriptionHtml"],
                "constraints": html_fragment_items(sections["constraintsHtml"]),
                "complexity": {
                    "required": required_complexity,
                    "advanced": advanced_complexity,
                },
                "officialExamples": problem.get("officialExamples") or [],
                "officialHints": [
                    hint for hint in (problem.get("officialHints") or []) if hint
                ],
                "signature": problem.get("signature") or {},
                "javaTemplate": problem.get("javaTemplate") or "",
                "exampleTestcases": problem.get("exampleTestcases") or "",
                "sourceFactsSha256": problem.get("sourceFactsSha256"),
                "solution": solution_links,
                "system": {
                    "id": system_view["id"],
                    "label": system_view["label"],
                },
            }
        )

    by_id = {record["id"]: record for record in records}

    def record_ids(predicate: Any) -> list[int]:
        return [
            record["id"]
            for record in sorted(
                records,
                key=lambda item: (
                    DIFFICULTY_ORDER.index(item["difficulty"])
                    if item["difficulty"] in DIFFICULTY_ORDER
                    else len(DIFFICULTY_ORDER),
                    item["id"],
                ),
            )
            if predicate(record)
        ]

    official_groups = [
        {
            "id": difficulty,
            "label": {
                "Easy": "简单",
                "Medium": "中等",
                "Hard": "困难",
            }[difficulty],
            "description": "",
            "problemIds": record_ids(
                lambda record, level=difficulty: record["difficulty"] == level
            ),
        }
        for difficulty in DIFFICULTY_ORDER
    ]

    interview_groups = [
        {
            "id": f"interview-{difficulty}",
            "label": {
                "Easy": "简单",
                "Medium": "中等",
                "Hard": "困难",
            }[difficulty],
            "description": "",
            "problemIds": [
                problem_id
                for problem_id in record_ids(
                    lambda record, level=difficulty: (
                        record["difficulty"] == level
                        and "P0" in record["priorities"]
                    )
                )
            ],
        }
        for difficulty in DIFFICULTY_ORDER
    ]

    tag_labels = sorted(
        {
            tag["translatedName"]
            for record in records
            for tag in record["officialTags"]
        }
    )
    tag_groups = [
        {
            "id": f"tag-{index}",
            "label": label,
            "description": "",
            "problemIds": record_ids(
                lambda record, tag_label=label: any(
                    tag["translatedName"] == tag_label
                    for tag in record["officialTags"]
                )
            ),
        }
        for index, label in enumerate(tag_labels, start=1)
    ]

    system_groups = []
    for system_view in SYSTEM_VIEWS:
        system_groups.append(
            {
                "id": system_view["id"],
                "label": system_view["label"],
                "description": system_view["description"],
                "problemIds": record_ids(
                    lambda record, view_id=system_view["id"]: (
                        record["system"]["id"] == view_id
                    )
                ),
            }
        )

    return {
        "schemaVersion": 1,
        "generatedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
        "source": {
            "path": "学习文库/算法学习/problems.json",
            "schemaVersion": problems_payload.get("schemaVersion"),
            "generatedAt": problems_payload.get("generatedAt"),
        },
        "stats": {
            "records": len(records),
            "easy": sum(record["difficulty"] == "Easy" for record in records),
            "medium": sum(record["difficulty"] == "Medium" for record in records),
            "hard": sum(record["difficulty"] == "Hard" for record in records),
            "interview": len(
                record_ids(lambda record: "P0" in record["priorities"])
            ),
            "tags": len(tag_labels),
            "systemForms": len(SYSTEM_VIEWS),
        },
        "views": {
            "official": {
                "label": "官方事实",
                "description": "直接投影 LeetCode 快照；不混入本地推导、难度之外的招考判断或推荐解法。",
                "groups": official_groups,
            },
            "interview": {
                "label": "面试高频",
                "description": "本地策展视图，只取清单中标记为 P0 的题。它帮助临时扫读，不代表平台的官方面试评级。",
                "groups": interview_groups,
            },
            "system": {
                "label": "体系形态",
                "description": "按计算机里经常重复出现的问题形态重排；与官方标签正交，一道题只归入一个主要形态。",
                "groups": system_groups,
            },
            "tags": {
                "label": "官方标签",
                "description": "保留 LeetCode 官方标签，用于原样检索；标签只描述题目，不自动证明某个算法方向。",
                "groups": tag_groups,
            },
        },
        "records": records,
        "recordById": {str(key): value for key, value in by_id.items()},
    }


def build_experiment_payload() -> dict[str, Any]:
    if not EXPERIMENT_PATH.exists():
        raise FileNotFoundError(
            f"缺少分析实验数据源：{EXPERIMENT_PATH}"
        )
    payload = json.loads(EXPERIMENT_PATH.read_text(encoding="utf-8"))
    problems = payload.get("problems")
    if not isinstance(problems, list):
        raise ValueError("analysis-experiments.json 的 problems 必须是数组")
    payload["problemById"] = {
        str(problem["id"]): problem
        for problem in problems
        if isinstance(problem, dict) and "id" in problem
    }
    return payload


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
    if first == "LeetCode-系统复习":
        if len(parts) <= 2:
            return "review", "总入口"
        return "review", REVIEW_TOPIC_LABELS.get(parts[1], "其他")
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
    review_paths = [path for path, doc in docs.items() if doc["category"] == "review"]
    review_topics: list[dict[str, Any]] = []
    for topic in sorted(
        {docs[path]["topic"] for path in review_paths},
        key=lambda value: (
            REVIEW_TOPIC_ORDER.index(value) if value in REVIEW_TOPIC_ORDER else len(REVIEW_TOPIC_ORDER),
            value,
        ),
    ):
        topic_paths = sorted(
            [path for path in review_paths if docs[path]["topic"] == topic],
            key=lambda path: (problem_number(path), path),
        )
        review_topics.append(
            {
                "label": topic,
                "category": "review",
                "items": items(topic_paths),
            }
        )

    return [
        {
            "id": "start",
            "label": "开始",
            "items": items(
                [
                    "README.md",
                    "00-首页.md",
                    "LeetCode-系统复习/00-总入口.md",
                    "学习看板/README.md",
                    "学习看板/单题复习工作台.md",
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
        {
            "id": "review",
            "label": "复习系统",
            "topics": review_topics,
        },
    ]


def build_manifest(
    docs: dict[str, dict[str, Any]],
    fact_bank: dict[str, Any] | None = None,
) -> dict[str, Any]:
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
    review_count = sum(doc["category"] == "review" for doc in docs.values())
    review_count += int("学习看板/单题复习工作台.md" in docs)
    today = dt.date.today().isoformat()
    priority_order = {"P0": 0, "P1": 1, "P2": 2}

    def review_order(doc: dict[str, Any]) -> tuple[Any, ...]:
        next_review = doc.get("nextReview")
        return (
            priority_order.get(str(doc.get("priority")), 9),
            next_review if isinstance(next_review, str) else "9999-12-31",
            problem_number(doc["path"]),
            doc["title"],
        )

    scheduled = sorted(
        [
            doc["path"]
            for doc in problems
            if doc.get("reviewStatus") == "待复习"
        ],
        key=lambda path: review_order(docs[path]),
    )
    review_due = [
        path
        for path in scheduled
        if isinstance(docs[path].get("nextReview"), str)
        and docs[path]["nextReview"] <= today
    ]
    review_upcoming = [
        path
        for path in scheduled
        if isinstance(docs[path].get("nextReview"), str)
        and docs[path]["nextReview"] > today
    ]
    review_unarranged = sorted(
        [
            doc["path"]
            for doc in problems
            if doc.get("reviewStatus") == "未安排"
        ],
        key=lambda path: review_order(docs[path]),
    )
    review_reviewed = sorted(
        [
            doc["path"]
            for doc in problems
            if doc.get("reviewStatus") == "已复习"
        ],
        key=lambda path: review_order(docs[path]),
    )
    review_all = sorted(
        [doc["path"] for doc in problems],
        key=lambda path: review_order(docs[path]),
    )
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
    error_counts: dict[str, list[str]] = {}
    for doc in problems:
        for tag in doc.get("errorTags") or []:
            label = str(tag).strip()
            if label:
                error_counts.setdefault(label, []).append(doc["path"])
    review_errors = [
        {"tag": tag, "count": len(paths), "paths": sorted(paths)}
        for tag, paths in sorted(
            error_counts.items(),
            key=lambda item: (-len(item[1]), item[0]),
        )
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

    manifest = {
        "title": "算法学习与复习库",
        "subtitle": "从理解、复述到独立实现、间隔复现与迁移",
        "generatedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
        "revision": revision,
        "sourceLabel": "学习文库 · 算法学习与系统复习",
        "homepage": "README.md",
        "stats": {
            "problems": problem_count,
            "core": core_count,
            "models": model_count,
            "concepts": concept_count,
            "comparisons": comparison_count,
            "java": java_count,
            "reviews": review_count,
            "documents": len(public_docs),
            "reviewDue": len(review_due),
            "reviewScheduled": len(scheduled),
            "reviewUnarranged": len(review_unarranged),
            "reviewReviewed": len(review_reviewed),
            "independent": len(independent),
            "transferable": len(transferable),
        },
        "review": {
            "all": review_all,
            "due": review_due,
            "scheduled": scheduled,
            "upcoming": review_upcoming,
            "unarranged": review_unarranged,
            "reviewed": review_reviewed,
            "independent": independent,
            "transferable": transferable,
            "errors": review_errors,
        },
        "nav": build_nav(docs),
        "docs": public_docs,
    }
    if fact_bank:
        manifest["factBank"] = {
            "sourcePath": fact_bank["source"]["path"],
            "sourceGeneratedAt": fact_bank["source"].get("generatedAt"),
            "stats": fact_bank["stats"],
            "views": {
                key: {
                    "label": view["label"],
                    "description": view["description"],
                }
                for key, view in fact_bank["views"].items()
            },
        }
    return manifest


def build_search_index(
    docs: dict[str, dict[str, Any]],
    fact_bank: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
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
    if fact_bank:
        for record in fact_bank["records"]:
            official_text = " ".join(
                [
                    html_fragment_text(record.get("descriptionHtml") or ""),
                    " ".join(record.get("constraints") or []),
                    " ".join(record.get("officialHints") or []),
                    " ".join(
                        tag.get("translatedName", "")
                        for tag in record.get("officialTags") or []
                    ),
                ]
            )
            index.append(
                {
                    "path": f"fact-bank/{record['id']}",
                    "href": f"#/bank?id={record['id']}",
                    "title": f"{record['id']}. {record['titleCn']}",
                    "category": "官方题面事实",
                    "topic": record.get("primaryPattern") or "未分类",
                    "headings": [],
                    "text": re.sub(r"\s+", " ", official_text).strip()[:12000],
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
    (OUTPUT_DIR / ".nojekyll").write_text("", encoding="utf-8")
    index = (SITE_DIR / "index.html").read_text(encoding="utf-8")
    (OUTPUT_DIR / "index.html").write_text(
        index.replace("__ASSET_VERSION__", asset_version()),
        encoding="utf-8",
    )
    for source_root, prefix in SOURCE_ROOTS:
        for relative in relative_files(source_root):
            source = source_root / relative
            target = OUTPUT_DIR / "content" / prefix / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)


def collect_docs() -> dict[str, dict[str, Any]]:
    docs: dict[str, dict[str, Any]] = {}
    for source_root, prefix in SOURCE_ROOTS:
        for relative_path in relative_files(source_root):
            if relative_path.suffix.lower() != ".md":
                continue
            relative = (Path(prefix) / relative_path).as_posix()
            if relative.startswith(TEMPLATE_PREFIX):
                continue
            markdown = (source_root / relative_path).read_text(encoding="utf-8")
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
                "leetcodeId": frontmatter.get("leetcodeId"),
                "difficulty": frontmatter.get("difficulty"),
                "primaryPattern": frontmatter.get("primaryPattern"),
                "priority": frontmatter.get("priority"),
                "errorTags": frontmatter.get("errorTags") or [],
                "independentAttempts": frontmatter.get("independentAttempts"),
                "isTemplate": relative.startswith(TEMPLATE_PREFIX),
            }
    return docs


def main() -> None:
    docs = collect_docs()
    problems_path = SOURCE_DIR / "problems.json"
    if not problems_path.exists():
        raise FileNotFoundError(f"缺少官方题面事实源：{problems_path}")
    problems_payload = json.loads(problems_path.read_text(encoding="utf-8"))
    fact_bank = build_fact_bank(problems_payload, docs)
    analysis_experiments = build_experiment_payload()
    manifest = build_manifest(docs, fact_bank)
    search_index = build_search_index(docs, fact_bank)
    copy_site_files()
    write_json(OUTPUT_DIR / "assets" / "manifest.json", manifest)
    write_json(OUTPUT_DIR / "assets" / "search.json", search_index)
    write_json(OUTPUT_DIR / "assets" / "fact-bank.json", fact_bank)
    write_json(
        OUTPUT_DIR / "assets" / "analysis-experiments.json",
        analysis_experiments,
    )
    print(
        f"Built {len(docs)} documents into {OUTPUT_DIR} "
        f"({manifest['stats']['problems']} problems, "
        f"{fact_bank['stats']['records']} fact records, {output_size(OUTPUT_DIR)})."
    )


def output_size(path: Path) -> str:
    total = sum(item.stat().st_size for item in path.rglob("*") if item.is_file())
    if total >= 1024 * 1024:
        return f"{total / 1024 / 1024:.1f} MB"
    return f"{total / 1024:.0f} KB"


if __name__ == "__main__":
    main()
