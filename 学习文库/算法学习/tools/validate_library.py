#!/usr/bin/env python3
"""Validate the layered algorithm library and its schema-v3 contract."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "problems.json"
PROBLEMS_ROOT = ROOT / "题目"
CORE_ROOT = ROOT / "核心模型"
MODELING_ROOT = ROOT / "建模专题" / "T0"
JAVA_ROOT = ROOT / "Java速查"
CONCEPT_ROOT = ROOT / "02-概念专题"
COMPARISON_ROOT = ROOT / "04-跨题对照"
TEMPLATE_ROOT = ROOT / "99-模板"

TEXT_SUFFIXES = {".md", ".json", ".py", ".sh", ".mjs", ".ps1", ".base"}
MASTERY_VALUES = {"未学", "已理解", "可独立实现", "可迁移"}
REVIEW_VALUES = {"未安排", "待复习", "已复习"}
DOCUMENT_TYPES = {
    "problem",
    "core-model",
    "modeling-topic",
    "java-api",
    "concept",
    "comparison-topic",
}
PRIORITIES = {"P0", "P1", "P2"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")

COMMON_REQUIRED = {
    "schemaVersion",
    "type",
    "titleCn",
    "topics",
    "priority",
    "mastery",
    "reviewStatus",
    "nextReview",
    "lastReviewed",
    "errorTags",
    "independentAttempts",
}

CORE_HEADINGS = [
    "一句话本质",
    "直观画面与扩题",
    "关系重写",
    "模型要素",
    "最小演算",
    "为什么成立",
    "代码映射",
    "复杂度",
    "30 秒识别信号",
    "最小反例与易错点",
    "分层入口",
]

MODELING_SEMANTICS = {
    "题意": ("题意", "题目", "输入", "输出"),
    "暴力基线": ("暴力", "直接模型", "人工模型", "朴素"),
    "浪费点": ("浪费", "重复工作", "重复扫描", "无效状态"),
    "视角转换": ("视角转换", "关键视角", "转换视角", "新的视角"),
    "状态": ("状态",),
    "不变量": ("不变量",),
    "结构选择": ("数据结构", "结构选择", "队列", "栈", "哈希", "堆"),
    "演算": ("演算", "数据变化", "状态快照", "逐步"),
    "正确性": ("正确性", "不会漏", "为什么成立", "证明"),
    "复杂度": ("复杂度",),
    "迁移": ("可迁移", "迁移", "模型卡", "模板"),
}

JAVA_CARD_SECTIONS = {
    "典型场景": ("典型场景",),
    "构造方式": ("构造方式", "构造"),
    "常用操作": ("常用操作", "常用运算"),
    "复杂度": ("复杂度",),
    "返回值语义": ("返回值语义", "返回值"),
    "空值与装箱": ("空值", "装箱"),
    "比较器或迭代修改": ("比较器", "迭代修改", "常见边界", "常见误区"),
    "关联题目": ("关联题目", "关联题"),
}

CONCEPT_HEADINGS = [
    "一句话本质",
    "直观过程",
    "对象与状态",
    "不变量",
    "最小演算",
    "适用信号",
    "最小反例",
    "代码映射",
    "代表题与相邻概念",
]

COMPARISON_HEADINGS = [
    "共同搜索骨架",
    "五题变化总览",
]

COMPARISON_PROBLEM_HEADINGS = [
    "200 岛屿数量：基础搜索模型",
    "127 单词接龙：从可达变成最少步数",
    "79 单词搜索：从全局访问变成路径访问",
    "46 全排列：从访问对象变成构造答案",
    "78 子集：从路径终点变成路径本身",
]

COMPARISON_PROBLEM_SECTIONS = [
    "完整题目",
    "相对基础模型的变化",
    "Java 入口",
    "完整 Java 实现",
    "代码与搜索模型逐段对照",
]


class Validator:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.texts: dict[Path, str] = {}
        self.frontmatter: dict[Path, dict[str, Any]] = {}
        self.bodies: dict[Path, str] = {}
        self.heading_anchors: dict[Path, set[str]] = {}
        self.markdown_files: list[Path] = []
        self.problems: list[dict[str, Any]] = []
        self.problem_by_id: dict[int, dict[str, Any]] = {}
        self.docs_by_type: dict[str, list[Path]] = {
            name: [] for name in DOCUMENT_TYPES
        }

    def error(self, path: Path | None, message: str) -> None:
        prefix = str(path.relative_to(ROOT)) if path else "library"
        self.errors.append(f"{prefix}: {message}")

    def read_all(self) -> None:
        for path in sorted(ROOT.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            if ".obsidian" in path.parts or "__pycache__" in path.parts:
                continue
            raw = path.read_bytes()
            if raw.startswith(b"\xef\xbb\xbf"):
                self.error(path, "UTF-8 BOM is not allowed")
            try:
                text = raw.decode("utf-8")
            except UnicodeDecodeError as exc:
                self.error(path, f"invalid UTF-8: {exc}")
                continue
            self.texts[path] = text
            if path.suffix.lower() == ".md":
                self.markdown_files.append(path)
                self.frontmatter[path], self.bodies[path] = self.parse_frontmatter(
                    text
                )
                self.heading_anchors[path] = self.collect_anchors(self.bodies[path])

    @staticmethod
    def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
        match = re.match(r"\A---\r?\n([\s\S]*?)\r?\n---\r?\n", text)
        if not match:
            return {}, text
        values: dict[str, Any] = {}
        current_mapping: str | None = None
        for line in match.group(1).splitlines():
            if not line.strip():
                continue
            nested = re.match(r"^\s{2}([A-Za-z][A-Za-z0-9]*):\s*(.*)$", line)
            if nested and current_mapping:
                key, raw = nested.groups()
                current = values.get(current_mapping)
                if not isinstance(current, dict):
                    current = {}
                    values[current_mapping] = current
                current[key] = Validator.decode_scalar(raw)
                continue
            field = re.match(r"^([A-Za-z][A-Za-z0-9]*):\s*(.*)$", line)
            if not field:
                current_mapping = None
                continue
            key, raw = field.groups()
            current_mapping = key
            values[key] = Validator.decode_scalar(raw)
        return values, text[match.end() :]

    @staticmethod
    def decode_scalar(raw: str) -> Any:
        raw = raw.strip()
        if raw == "":
            return None
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return raw

    def validate_manifest(self) -> None:
        manifest = json.loads(self.texts[MANIFEST_PATH])
        if manifest.get("schemaVersion") != 3:
            self.error(MANIFEST_PATH, "root schemaVersion must be 3")
        problems = manifest.get("problems")
        if not isinstance(problems, list):
            self.error(MANIFEST_PATH, "problems must be an array")
            return
        self.problems = problems
        required = {
            "id",
            "slug",
            "titleCn",
            "titleEn",
            "difficulty",
            "sourceUrl",
            "sourceCheckedAt",
            "relativePath",
            "primaryPattern",
            "signature",
            "officialExamples",
            "sourceFactsSha256",
            "sourceSectionHashes",
        }
        for position, problem in enumerate(problems, start=1):
            label = f"problem #{position}"
            missing = sorted(required - set(problem))
            if missing:
                self.error(MANIFEST_PATH, f"{label} missing {', '.join(missing)}")
                continue
            problem_id = int(problem["id"])
            if problem_id in self.problem_by_id:
                self.error(MANIFEST_PATH, f"duplicate problem id {problem_id}")
            self.problem_by_id[problem_id] = problem
            standard_path = ROOT / problem["relativePath"]
            if not standard_path.is_file():
                self.error(
                    MANIFEST_PATH,
                    f"problem {problem_id} relativePath does not exist: "
                    f"{problem['relativePath']}",
                )
            if not DATE_RE.match(problem["sourceCheckedAt"]):
                self.error(
                    MANIFEST_PATH,
                    f"problem {problem_id} sourceCheckedAt is not YYYY-MM-DD",
                )
            if not problem["officialExamples"]:
                self.error(
                    MANIFEST_PATH,
                    f"problem {problem_id} has no official examples",
                )

        migration = self.load_migration_module()
        for problem in problems:
            if "id" not in problem or "sourceFactsSha256" not in problem:
                continue
            expected, sections = migration.source_hashes(problem)
            problem_id = int(problem["id"])
            if problem["sourceFactsSha256"] != expected:
                self.error(
                    MANIFEST_PATH,
                    f"problem {problem_id} sourceFactsSha256 mismatch; "
                    f"expected {expected}",
                )
            actual_sections = problem.get("sourceSectionHashes")
            if actual_sections != sections:
                self.error(
                    MANIFEST_PATH,
                    f"problem {problem_id} sourceSectionHashes mismatch",
                )

    @staticmethod
    def load_migration_module() -> Any:
        module_path = ROOT / "tools" / "migrate_library_v3.py"
        spec = importlib.util.spec_from_file_location(
            "migrate_library_v3", module_path
        )
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def validate_frontmatter(self) -> None:
        for path in self.markdown_files:
            if TEMPLATE_ROOT in path.parents:
                continue
            in_content_layer = (
                path.parent == PROBLEMS_ROOT
                or PROBLEMS_ROOT in path.parents
                or path.parent == CORE_ROOT
                or CORE_ROOT in path.parents
                or path.parent == MODELING_ROOT
                or path.parent == JAVA_ROOT
                or JAVA_ROOT in path.parents
                or path.parent == CONCEPT_ROOT
                or CONCEPT_ROOT in path.parents
                or path.parent == COMPARISON_ROOT
                or COMPARISON_ROOT in path.parents
            )
            if not in_content_layer:
                continue
            if path.name == "README.md" and path.parent in {
                CONCEPT_ROOT,
                COMPARISON_ROOT,
            }:
                continue
            data = self.frontmatter.get(path, {})
            if not data:
                self.error(path, "frontmatter is missing")
                continue
            if path.parent == PROBLEMS_ROOT or PROBLEMS_ROOT in path.parents:
                expected_type = "problem"
            elif path.parent == CORE_ROOT or CORE_ROOT in path.parents:
                expected_type = "core-model"
            elif path.parent == MODELING_ROOT:
                expected_type = "modeling-topic"
            elif path.parent == JAVA_ROOT or JAVA_ROOT in path.parents:
                expected_type = "java-api"
            elif path.parent == CONCEPT_ROOT or CONCEPT_ROOT in path.parents:
                expected_type = "concept"
            elif path.parent == COMPARISON_ROOT or COMPARISON_ROOT in path.parents:
                expected_type = "comparison-topic"
            else:
                continue
            self.docs_by_type[expected_type].append(path)
            if data.get("schemaVersion") != 3:
                self.error(path, "schemaVersion must be 3")
            if data.get("type") != expected_type:
                self.error(
                    path,
                    f"type must be {expected_type!r}, got {data.get('type')!r}",
                )
            missing = sorted(COMMON_REQUIRED - set(data))
            if missing:
                self.error(path, f"missing frontmatter fields: {', '.join(missing)}")
            if data.get("mastery") not in MASTERY_VALUES:
                self.error(path, f"invalid mastery {data.get('mastery')!r}")
            if data.get("reviewStatus") not in REVIEW_VALUES:
                self.error(
                    path, f"invalid reviewStatus {data.get('reviewStatus')!r}"
                )
            if data.get("priority") not in PRIORITIES:
                self.error(path, f"invalid priority {data.get('priority')!r}")
            for field in ("nextReview", "lastReviewed"):
                value = data.get(field)
                if value is not None and not (
                    isinstance(value, str) and DATE_RE.match(value)
                ):
                    self.error(path, f"{field} must be YYYY-MM-DD or null")
            if not isinstance(data.get("errorTags"), list):
                self.error(path, "errorTags must be a JSON array")
            attempts = data.get("independentAttempts")
            if isinstance(attempts, bool) or not isinstance(attempts, int) or attempts < 0:
                self.error(path, "independentAttempts must be a non-negative integer")
            if not isinstance(data.get("topics"), list):
                self.error(path, "topics must be a JSON array")

            if expected_type in {"concept", "comparison-topic"}:
                related = data.get("relatedProblems")
                if not isinstance(related, list) or not related:
                    self.error(
                        path,
                        "relatedProblems must be a non-empty JSON array",
                    )
                else:
                    for problem_id in related:
                        if (
                            isinstance(problem_id, bool)
                            or not isinstance(problem_id, int)
                            or problem_id not in self.problem_by_id
                        ):
                            self.error(
                                path,
                                f"invalid relatedProblems entry {problem_id!r}",
                            )

            if expected_type in {"problem", "core-model", "modeling-topic"}:
                self.validate_fact_hash(path, data)

    def validate_fact_hash(self, path: Path, data: dict[str, Any]) -> None:
        problem = self.problem_by_id.get(int(data.get("leetcodeId", -1)))
        if not problem:
            self.error(path, "leetcodeId does not exist in problems.json")
            return
        if data.get("sourceFactsSha256") != problem["sourceFactsSha256"]:
            self.error(path, "sourceFactsSha256 does not match problems.json")
        if data.get("type") in {"problem", "modeling-topic"}:
            if data.get("sourceSectionHashes") != problem["sourceSectionHashes"]:
                self.error(path, "sourceSectionHashes does not match problems.json")
        for field in ("titleCn", "titleEn", "difficulty", "sourceUrl"):
            if data.get(field) != problem.get(field):
                self.error(path, f"{field} does not match problems.json")

    def validate_relationships(self) -> None:
        core_by_id: dict[int, Path] = {}
        modeling_by_id: dict[int, Path] = {}
        for path in self.docs_by_type["core-model"]:
            data = self.frontmatter[path]
            problem_id = int(data.get("leetcodeId", -1))
            if problem_id in core_by_id:
                self.error(path, f"duplicate core card for problem {problem_id}")
            core_by_id[problem_id] = path
        for path in self.docs_by_type["modeling-topic"]:
            data = self.frontmatter[path]
            problem_id = int(data.get("leetcodeId", -1))
            if problem_id in modeling_by_id:
                self.error(path, f"duplicate modeling topic for problem {problem_id}")
            modeling_by_id[problem_id] = path

        for problem_id, problem in self.problem_by_id.items():
            standard = ROOT / problem["relativePath"]
            core = core_by_id.get(problem_id)
            if not core:
                self.error(MANIFEST_PATH, f"problem {problem_id} has no core card")
            elif self.frontmatter[core].get("problemPath") != problem["relativePath"]:
                self.error(core, "problemPath does not match standard solution")
            deep = modeling_by_id.get(problem_id)
            deep_value = self.frontmatter.get(core, {}).get("deepDivePath")
            if deep:
                expected = str(deep.relative_to(ROOT))
                if deep_value != expected:
                    self.error(core, f"deepDivePath must be {expected!r}")
            elif deep_value is not None:
                self.error(core, "deepDivePath is set but no matching topic exists")
            if standard.is_file():
                body = self.bodies[standard]
                if core and str(core.relative_to(ROOT)) not in body:
                    self.error(standard, "standard solution does not link to core card")
                if deep and str(deep.relative_to(ROOT)) not in body:
                    self.error(standard, "standard solution does not link to modeling topic")
            if deep:
                body = self.bodies[deep]
                if problem["relativePath"] not in body:
                    self.error(deep, "modeling topic does not link to standard solution")
                if core and str(core.relative_to(ROOT)) not in body:
                    self.error(deep, "modeling topic does not link to core card")

    @staticmethod
    def collect_anchors(markdown: str) -> set[str]:
        anchors: set[str] = set()
        for match in re.finditer(r"^#{1,6}\s+(.+?)\s*$", markdown, re.M):
            heading = match.group(1)
            heading = re.sub(r"`([^`]*)`", r"\1", heading)
            heading = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", heading)
            heading = re.sub(r"[*_~]", "", heading)
            anchors.update(Validator.anchor_variants(heading))
        return anchors

    @staticmethod
    def anchor_variants(value: str) -> set[str]:
        normalized = unicodedata.normalize("NFKC", value).strip().lower()
        collapsed = re.sub(r"\s+", " ", normalized)
        no_punctuation = re.sub(
            r"[\s`~!@#$%^&*()+=\[\]{}\\|;:'\",.<>/?，。！？；：“”‘’（）【】、《》]+",
            "",
            collapsed,
        )
        return {
            normalized,
            collapsed,
            collapsed.replace(" ", "-"),
            no_punctuation,
        }

    def validate_links(self) -> None:
        for path in self.markdown_files:
            if TEMPLATE_ROOT in path.parents:
                continue
            body = self.strip_fenced_blocks(self.bodies[path])
            for target, label in self.extract_links(body):
                if self.is_external(target):
                    continue
                self.validate_link_target(path, target, label)

    @staticmethod
    def strip_fenced_blocks(markdown: str) -> str:
        return re.sub(r"```[\s\S]*?```", "", markdown)

    @staticmethod
    def extract_links(markdown: str) -> list[tuple[str, str]]:
        markdown = re.sub(r"`[^`\n]*`", "", markdown)
        links: list[tuple[str, str]] = []
        for match in re.finditer(r"(?<!!)\[[^\]]*\]\(([^)\n]+)\)", markdown):
            raw = match.group(1).strip()
            if raw.startswith("<") and ">" in raw:
                raw = raw[1 : raw.index(">")]
            else:
                raw = re.split(r'\s+["\']', raw, maxsplit=1)[0]
            links.append((raw, "markdown"))
        for match in re.finditer(r"\[\[([^\]\n]+)\]\]", markdown):
            raw = match.group(1).split("|", 1)[0].strip()
            # JSON-like example arrays can look like [[...]] but never form
            # valid vault links. Reject quoted or array-shaped candidates.
            if (
                raw
                and not raw.startswith(("\"", "'", "["))
                and not raw.endswith(("\"", "'", "]"))
            ):
                links.append((raw, "wiki"))
        return links

    @staticmethod
    def is_external(target: str) -> bool:
        return bool(
            re.match(
                r"^(?:https?|mailto|obsidian|codex|file|tel|data):",
                target,
                re.I,
            )
        )

    def validate_link_target(
        self, source: Path, raw_target: str, kind: str
    ) -> None:
        decoded = unquote(raw_target)
        target_part, separator, anchor = decoded.partition("#")
        anchor = anchor.strip()
        if not target_part:
            target = source
        else:
            target_path = Path(target_part)
            candidates = []
            if target_path.is_absolute():
                candidates.append(ROOT / target_path.relative_to(target_path.anchor))
            else:
                candidates.append((source.parent / target_path).resolve())
            if not target_path.suffix:
                candidates.insert(
                    0, ((source.parent / target_path).resolve()).with_suffix(".md")
                )
            target = next((item for item in candidates if item.exists()), None)
            if target is None:
                # Wiki links may omit a leading vault-relative directory.
                target = self.resolve_root_relative(target_path)
        if target is None or not target.exists():
            self.error(source, f"broken {kind} link: {raw_target}")
            return
        if target.is_dir():
            if separator:
                self.error(source, f"directory link cannot have anchor: {raw_target}")
            return
        if target.suffix.lower() != ".md" or not separator:
            return
        anchors = self.heading_anchors.get(target)
        if anchors is None:
            self.error(source, f"link target is outside Markdown inventory: {raw_target}")
            return
        if not (self.anchor_variants(anchor) & anchors):
            self.error(source, f"broken heading anchor: {raw_target}")

    def resolve_root_relative(self, path: Path) -> Path | None:
        candidates = [ROOT / path, (ROOT / path).with_suffix(".md")]
        for candidate in candidates:
            if candidate.exists():
                return candidate
        return None

    def validate_placeholders_and_fences(self) -> None:
        placeholder_re = re.compile(r"\b(?:TODO|TBD)\b|待填写")
        for path in self.markdown_files:
            if TEMPLATE_ROOT in path.parents:
                continue
            in_content_layer = (
                PROBLEMS_ROOT in path.parents
                or CORE_ROOT in path.parents
                or path.parent == MODELING_ROOT
                or JAVA_ROOT in path.parents
                or path.parent == CONCEPT_ROOT
                or CONCEPT_ROOT in path.parents
                or path.parent == COMPARISON_ROOT
                or COMPARISON_ROOT in path.parents
            )
            if not in_content_layer:
                continue
            text = self.texts[path]
            for line_number, line in enumerate(text.splitlines(), start=1):
                if placeholder_re.search(line):
                    self.error(path, f"placeholder text on line {line_number}")
            if len(re.findall(r"^```", text, re.M)) % 2:
                self.error(path, "unbalanced Markdown code fence")

    def validate_core_cards(self) -> None:
        for path in self.docs_by_type["core-model"]:
            text = self.bodies[path]
            count = len(CJK_RE.findall(text))
            if not 600 <= count <= 1200:
                self.error(path, f"CJK length {count} is outside 600..1200")
            headings = {value.strip() for value in re.findall(r"^##\s+(.+)$", text, re.M)}
            for heading in CORE_HEADINGS:
                if heading not in headings:
                    self.error(path, f"missing core-card section: {heading}")
            mapping = self.section_text(text, "代码映射")
            pseudo = re.findall(r"```text\s*\n([\s\S]*?)```", mapping)
            if not pseudo:
                self.error(path, "code mapping must contain a text pseudocode block")
            elif len([line for line in pseudo[0].splitlines() if line.strip()]) > 15:
                self.error(path, "pseudocode exceeds 15 lines")
            self.validate_core_table(path, text)

    @staticmethod
    def section_text(markdown: str, heading: str) -> str:
        match = re.search(
            rf"^##\s+{re.escape(heading)}[^\n]*\n([\s\S]*?)(?=^##\s+|\Z)",
            markdown,
            re.M,
        )
        return match.group(1) if match else ""

    def validate_core_table(self, path: Path, text: str) -> None:
        model_section = self.section_text(text, "模型要素")
        rows = [
            line
            for line in model_section.splitlines()
            if line.startswith("|") and not re.match(r"^\|\s*-", line)
        ]
        if len(rows) < 2:
            self.error(path, "model table must have a header and one data row")
        for row in rows[2:]:
            for cell in [item.strip() for item in row.strip("|").split("|")]:
                if cell.endswith(("，", "；", "：", "、", "（")):
                    self.error(path, f"truncated model-table cell: {cell!r}")
        calculation = self.section_text(text, "最小演算")
        for line in calculation.splitlines():
            if re.match(r"^\d+\.\s+\*\*(?:初始状态|触发事件|结束条件)", line):
                if line.rstrip().endswith(("，", "；", "：", "、")):
                    self.error(path, f"truncated calculation step: {line!r}")

    def validate_modeling_topics(self) -> None:
        for path in self.docs_by_type["modeling-topic"]:
            headings = self.bodies[path]
            for semantic, keywords in MODELING_SEMANTICS.items():
                if not any(keyword in headings for keyword in keywords):
                    self.error(path, f"missing modeling semantic: {semantic}")

    def validate_concept_cards(self) -> None:
        for path in self.docs_by_type["concept"]:
            text = self.bodies[path]
            count = len(CJK_RE.findall(text))
            if not 600 <= count <= 1800:
                self.error(path, f"CJK length {count} is outside 600..1800")
            headings = {
                value.strip() for value in re.findall(r"^##\s+(.+)$", text, re.M)
            }
            for heading in CONCEPT_HEADINGS:
                if heading not in headings:
                    self.error(path, f"missing concept-card section: {heading}")
            mapping = self.section_text(text, "代码映射")
            pseudo = re.findall(r"```text\s*\n([\s\S]*?)```", mapping)
            if not pseudo:
                self.error(path, "code mapping must contain a text pseudocode block")
            elif len([line for line in pseudo[0].splitlines() if line.strip()]) > 20:
                self.error(path, "concept pseudocode exceeds 20 lines")

    @staticmethod
    def heading_section(markdown: str, heading: str, level: int = 2) -> str:
        marker = "#" * level
        match = re.search(
            rf"^{marker}\s+{re.escape(heading)}[^\n]*\n"
            rf"([\s\S]*?)(?=^{marker}\s+|\Z)",
            markdown,
            re.M,
        )
        return match.group(1) if match else ""

    @staticmethod
    def extract_java_code(markdown: str) -> str | None:
        match = re.search(r"```java\s*\n([\s\S]*?)\n```", markdown)
        return match.group(1) if match else None

    @staticmethod
    def normalize_java(code: str) -> str:
        return "\n".join(line.rstrip() for line in code.strip().splitlines()).strip()

    def validate_comparison_topics(self) -> None:
        for path in self.docs_by_type["comparison-topic"]:
            text = self.bodies[path]
            related = self.frontmatter[path].get("relatedProblems")
            if related != [200, 127, 79, 46, 78]:
                self.error(
                    path,
                    "relatedProblems must be [200, 127, 79, 46, 78]",
                )

            headings = {
                value.strip() for value in re.findall(r"^##\s+(.+)$", text, re.M)
            }
            for heading in COMPARISON_HEADINGS + COMPARISON_PROBLEM_HEADINGS:
                if heading not in headings:
                    self.error(path, f"missing comparison section: {heading}")

            for problem_heading in COMPARISON_PROBLEM_HEADINGS:
                problem_id = int(problem_heading.split()[0])
                problem = self.problem_by_id.get(problem_id)
                if not problem:
                    continue
                section = self.heading_section(text, problem_heading)
                for required in COMPARISON_PROBLEM_SECTIONS:
                    if not self.heading_section(section, required, level=3):
                        self.error(
                            path,
                            f"{problem_heading} missing subsection: {required}",
                        )

                authority_path = ROOT / problem["relativePath"]
                authority_section = self.heading_section(
                    self.bodies[authority_path],
                    "LeetCode 可直接提交代码",
                    level=3,
                )
                authority_code = self.extract_java_code(authority_section)
                comparison_code = self.extract_java_code(
                    self.heading_section(section, "完整 Java 实现", level=3)
                )
                if authority_code is None:
                    self.error(authority_path, "authoritative Java code is missing")
                elif comparison_code is None:
                    self.error(path, f"{problem_heading} has no Java code")
                elif self.normalize_java(authority_code) != self.normalize_java(
                    comparison_code
                ):
                    self.error(
                        path,
                        f"{problem_heading} Java differs from the authoritative "
                        "standard solution",
                    )

    def validate_standard_solutions(self) -> None:
        required_code_headings = [
            "### LeetCode 可直接提交代码",
            "### 本地可运行示例",
        ]
        for path in self.docs_by_type["problem"]:
            text = self.bodies[path]
            for heading in required_code_headings:
                if heading not in text:
                    self.error(path, f"missing Java section: {heading}")
                    continue
                section = text[text.index(heading) :]
                if not re.search(r"```java\s*\n[\s\S]*?\n```", section):
                    self.error(path, f"{heading} has no Java code block")
            if "复杂度" not in text:
                self.error(path, "complexity section is missing")

    def validate_java_cards(self) -> None:
        cards = [
            path
            for path in self.docs_by_type["java-api"]
            if not path.name.startswith("00-")
        ]
        if len(cards) != 5:
            self.error(JAVA_ROOT, f"expected 5 Java cards, found {len(cards)}")
        for path in cards:
            text = self.bodies[path]
            for section_name, keywords in JAVA_CARD_SECTIONS.items():
                if not any(keyword in text for keyword in keywords):
                    self.error(path, f"missing Java-card coverage: {section_name}")

    def validate_templates(self) -> None:
        standard_semantics = {
            "官方事实": ("官方事实", "题意", "示例", "约束"),
            "标准方案": ("标准方案", "推导", "不变量"),
            "权威 Java 实现": ("权威 Java 实现",),
            "本地验证": ("本地验证",),
            "易错点与边界": ("易错点", "边界"),
            "三层入口": ("三层入口",),
        }
        expected = {
            "题解.md": standard_semantics,
            "建模专题.md": {
                semantic: keywords
                for semantic, keywords in MODELING_SEMANTICS.items()
            },
            "核心模型.md": {
                heading: (heading,) for heading in CORE_HEADINGS
            },
            "Java API.md": {
                section: keywords
                for section, keywords in JAVA_CARD_SECTIONS.items()
            },
            "概念卡.md": {
                heading: (heading,) for heading in CONCEPT_HEADINGS
            },
            "跨题对照.md": {
                **{heading: (heading,) for heading in COMPARISON_HEADINGS},
                **{
                    heading: (heading,)
                    for heading in COMPARISON_PROBLEM_SECTIONS
                },
            },
        }
        for name, semantics in expected.items():
            path = TEMPLATE_ROOT / name
            if not path.is_file():
                self.error(path, "template is missing")
                continue
            text = self.texts[path]
            if "schemaVersion: 3" not in text:
                self.error(path, "template must declare schemaVersion 3")
            for semantic, keywords in semantics.items():
                if not any(keyword in text for keyword in keywords):
                    self.error(path, f"template missing semantic: {semantic}")

    def validate_unique_paths(self) -> None:
        seen: dict[str, Path] = {}
        for path in self.markdown_files:
            relative = str(path.relative_to(ROOT))
            key = relative.casefold()
            if key in seen:
                self.error(path, f"duplicate path conflicts with {seen[key]}")
            seen[key] = path

    def run(self) -> int:
        self.read_all()
        self.validate_unique_paths()
        self.validate_manifest()
        self.validate_frontmatter()
        self.validate_relationships()
        self.validate_links()
        self.validate_placeholders_and_fences()
        self.validate_core_cards()
        self.validate_modeling_topics()
        self.validate_concept_cards()
        self.validate_comparison_topics()
        self.validate_standard_solutions()
        self.validate_java_cards()
        self.validate_templates()
        if self.errors:
            print(f"Library validation failed: {len(self.errors)} error(s)")
            for message in self.errors:
                print(f"- {message}")
            return 1
        print(
            "Library validation passed: "
            f"{len(self.problems)} problems, "
            f"{len(self.docs_by_type['core-model'])} core cards, "
            f"{len(self.docs_by_type['modeling-topic'])} modeling topics, "
            f"{len(self.docs_by_type['java-api'])} Java cards, "
            f"{len(self.docs_by_type['concept'])} concept cards, "
            f"{len(self.docs_by_type['comparison-topic'])} comparison topics."
        )
        for warning in self.warnings:
            print(f"warning: {warning}")
        return 0


if __name__ == "__main__":
    sys.exit(Validator().run())
