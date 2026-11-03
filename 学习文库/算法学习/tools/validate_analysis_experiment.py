#!/usr/bin/env python3
"""Validate the human-first analysis-method experiment."""

from __future__ import annotations

import copy
import json
import re
import sys
from pathlib import Path
from typing import Callable


REPO_ROOT = Path(__file__).resolve().parents[3]
LIBRARY_ROOT = REPO_ROOT / "学习文库" / "算法学习"
EXPERIMENT_ROOT = REPO_ROOT / "LeetCode-系统复习" / "07-分析法实验"
DATA_PATH = EXPERIMENT_ROOT / "analysis-experiments.json"
PROBLEMS_PATH = LIBRARY_ROOT / "problems.json"

SCHEMA_VERSION = 2
REQUIRED_PROBLEM_IDS = {1, 11, 322, 739}
DIMENSIONS = {
    "absorb",
    "recall",
    "systems",
    "chain",
    "debug",
    "transfer",
}
GATES = {
    "factGate",
    "naturalReachability",
    "causalClosure",
    "codeTraceability",
    "closedBookRegeneration",
}
STATUSES = {"main", "alternative", "superseded", "rejected"}
MIGRATION_STATUSES = {
    "complete-human-chain",
    "post-hoc-pending-migration",
}
REFERENCE_KEYS = {
    "solutionPath",
    "reasoningAnchor",
    "answerAnchor",
    "codeAnchor",
    "coreModelPath",
    "coreModelAnchor",
}
HEADING_REFERENCE_KEYS = {
    "reasoningAnchor",
    "answerAnchor",
    "codeAnchor",
    "coreModelAnchor",
}
CODE_MAPPING_KEYS = {
    "object",
    "action",
    "operation",
    "state",
    "codeAnchor",
    "invariant",
    "counterexample",
}
REQUIRED_DOCS = {
    "README.md": [
        "人工过程法负责从题面走到第一次变化",
        "只选一个辅助分析法走完整因果链",
        "问题事实",
    ],
    "题库与题解生产协议-v2.md": [
        "唯一生产权威",
        "阶段 1｜交接 1：原题事实",
        "阶段 7｜交接 9：状态、更新顺序、不变量、代码、反例",
        "complete-human-chain",
        "post-hoc-pending-migration",
        "阶段 1 至 5 不读取比较字段、题解关联、代码和评分",
    ],
    "分析法实验协议.md": [
        "顺序、字段、门控和验收的唯一生产权威",
        "所有对照路径都必须使用",
        "同一套九次交接",
        "实验不重新定义阶段",
        "没有形成候选",
        "没有发生转折",
        "事后校验",
    ],
    "四题多路径实验.md": [
        "事后校验",
        "两数之和",
        "每日温度",
        "盛最多水的容器",
        "零钱兑换",
        "候选淘汰与不变量",
        "子问题复用",
    ],
    "评分与选择规则.md": [
        "先过五项门槛",
        "事实保真",
        "自然可达",
        "编码定位",
        "比较最低分",
        "具体候选留到交接 8",
    ],
    "量产与复习协议.md": [
        "同分异构",
        "标准题解仍是题意、签名、权威 Java 和复习日期的唯一来源",
        "不维护第二份日期",
        "单题顺序、九次交接、数据范围时机和页面门控的唯一生产权威",
        "本目录不复制第二份顺序表",
    ],
}

FORBIDDEN_DOC_PATTERNS = {
    "分析法实验协议.md": [
        "七阶段是共同基线",
        "-> 数据范围、操作预算、功能候选",
    ],
    "四题多路径实验.md": [
        "### 4. 数据范围、预算和候选池",
        "| 排除哪些功能候选 |",
        "| 保留哪些功能候选 |",
    ],
    "评分与选择规则.md": [
        "只写到事实、过程或候选池",
    ],
    "量产与复习协议.md": [
        "写七阶段主路径",
        "被排除的复杂度家族 -> 功能候选",
    ],
}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def load_json(path: Path, errors: list[str]) -> dict:
    if not path.is_file():
        fail(errors, f"{path.relative_to(REPO_ROOT)}: file is missing")
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(errors, f"{path.relative_to(REPO_ROOT)}: invalid JSON: {exc}")
        return {}
    if not isinstance(data, dict):
        fail(errors, f"{path.relative_to(REPO_ROOT)}: top level must be an object")
        return {}
    return data


def check_docs(errors: list[str]) -> None:
    for name, phrases in REQUIRED_DOCS.items():
        path = EXPERIMENT_ROOT / name
        if not path.is_file():
            fail(errors, f"{path.relative_to(REPO_ROOT)}: file is missing")
            continue
        text = path.read_text(encoding="utf-8")
        compact_text = "".join(text.split())
        for phrase in phrases:
            if "".join(phrase.split()) not in compact_text:
                fail(
                    errors,
                    f"{path.relative_to(REPO_ROOT)}: missing required phrase {phrase!r}",
                )
        for forbidden in ("TODO", "TBD", "待填写"):
            if forbidden in text:
                fail(
                    errors,
                    f"{path.relative_to(REPO_ROOT)}: unfinished marker {forbidden!r}",
                )
        for forbidden in FORBIDDEN_DOC_PATTERNS.get(name, []):
            if forbidden in text:
                fail(
                    errors,
                    f"{path.relative_to(REPO_ROOT)}: stale sequential rule {forbidden!r}",
                )

    protocol_path = EXPERIMENT_ROOT / "题库与题解生产协议-v2.md"
    if protocol_path.is_file():
        text = protocol_path.read_text(encoding="utf-8")
        production_table = text.split("## 三、九次交接生产表", 1)
        if len(production_table) != 2:
            fail(errors, "题库与题解生产协议-v2.md: missing nine-handoff table")
            return
        table = production_table[1].split("## 四、", 1)[0]
        indexes = [
            int(match.group(1))
            for match in re.finditer(r"^\|\s*([1-9])\s+", table, re.MULTILINE)
        ]
        if indexes != list(range(1, 10)):
            fail(
                errors,
                "题库与题解生产协议-v2.md: nine-handoff table must cover 1-9 in order, "
                f"got {indexes}",
            )


def check_source_alignment(
    experiment: dict, official: dict, errors: list[str]
) -> None:
    official_problems = {
        item.get("id"): item
        for item in official.get("problems", [])
        if isinstance(item, dict)
    }
    for problem in experiment.get("problems", []):
        problem_id = problem.get("id")
        source = official_problems.get(problem_id)
        if source is None:
            fail(errors, f"problem {problem_id}: not found in problems.json")
            continue
        if problem.get("titleCn") != source.get("titleCn"):
            fail(errors, f"problem {problem_id}: titleCn differs from problems.json")
        if problem.get("sourceUrl") != source.get("sourceUrl"):
            fail(errors, f"problem {problem_id}: sourceUrl differs from problems.json")


def score_total(scores: dict[str, int]) -> int:
    return sum(scores.values())


def resolve_repo_reference(
    reference: object, prefix: str, key: str, errors: list[str]
) -> Path | None:
    if not isinstance(reference, str) or not reference:
        fail(errors, f"{prefix}: reference {key} is required")
        return None
    path = (REPO_ROOT / reference).resolve()
    try:
        path.relative_to(REPO_ROOT.resolve())
    except ValueError:
        fail(errors, f"{prefix}: reference {key} escapes the repository")
        return None
    if not path.is_file():
        fail(errors, f"{prefix}: referenced file for {key} does not exist: {reference}")
        return None
    return path


def markdown_headings(text: str) -> set[str]:
    headings: set[str] = set()
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith(("```", "~~~")):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if match:
            headings.add(match.group(1).strip())
    return headings


def check_references(problem: dict, errors: list[str]) -> str | None:
    problem_id = problem.get("id")
    prefix = f"problem {problem_id}"
    references = problem.get("references")
    if not isinstance(references, dict):
        fail(errors, f"{prefix}: references must be an object")
        return None
    missing = sorted(REFERENCE_KEYS - set(references))
    if missing:
        fail(errors, f"{prefix}: references missing {', '.join(missing)}")

    solution_path = resolve_repo_reference(
        references.get("solutionPath"), prefix, "solutionPath", errors
    )
    core_model_path = resolve_repo_reference(
        references.get("coreModelPath"), prefix, "coreModelPath", errors
    )
    solution_text = (
        solution_path.read_text(encoding="utf-8") if solution_path else None
    )

    for key in HEADING_REFERENCE_KEYS:
        anchor = references.get(key)
        source_path = solution_path if key != "coreModelAnchor" else core_model_path
        if not isinstance(anchor, str) or not anchor:
            fail(errors, f"{prefix}: reference {key} is required")
            continue
        if source_path is None:
            continue
        text = source_path.read_text(encoding="utf-8")
        headings = markdown_headings(text)
        if anchor not in headings and not (
            key == "codeAnchor" and anchor in text
        ):
            fail(
                errors,
                f"{prefix}: {key} target does not exist in "
                f"{source_path.relative_to(REPO_ROOT)}: {anchor!r}",
            )
    return solution_text


def check_code_mappings(
    path: dict,
    prefix: str,
    solution_text: str | None,
    errors: list[str],
) -> None:
    mappings = path.get("codeMappings")
    is_main = path.get("status") == "main"
    if mappings is None:
        if is_main:
            fail(errors, f"{prefix}: main path requires non-empty codeMappings")
        return
    if not isinstance(mappings, list):
        fail(errors, f"{prefix}: codeMappings must be a list")
        return
    if is_main and not mappings:
        fail(errors, f"{prefix}: main path requires non-empty codeMappings")
    for index, mapping in enumerate(mappings, start=1):
        mapping_prefix = f"{prefix}/mapping {index}"
        if not isinstance(mapping, dict):
            fail(errors, f"{mapping_prefix}: must be an object")
            continue
        missing = sorted(CODE_MAPPING_KEYS - set(mapping))
        if missing:
            fail(errors, f"{mapping_prefix}: missing {', '.join(missing)}")
        for key in CODE_MAPPING_KEYS:
            if not isinstance(mapping.get(key), str) or not mapping.get(key):
                fail(errors, f"{mapping_prefix}: {key} must be non-empty text")
        anchor = mapping.get("codeAnchor")
        if (
            solution_text is not None
            and isinstance(anchor, str)
            and anchor
            and anchor not in solution_text
        ):
            fail(errors, f"{mapping_prefix}: Java codeAnchor not found: {anchor!r}")


def check_problem(problem: dict, errors: list[str]) -> None:
    problem_id = problem.get("id")
    prefix = f"problem {problem_id}"
    for key in ("selectedMethod", "selectedReason", "checkedAlternative"):
        if not isinstance(problem.get(key), str) or not problem.get(key):
            fail(errors, f"{prefix}: {key} is required")
    if problem.get("migrationStatus") not in MIGRATION_STATUSES:
        fail(errors, f"{prefix}: invalid migrationStatus")

    solution_text = check_references(problem, errors)
    paths = problem.get("paths")
    if not isinstance(paths, list) or len(paths) < 2:
        fail(errors, f"{prefix}: at least two analysis paths are required")
        return

    by_id: dict[str, dict] = {}
    for path in paths:
        if not isinstance(path, dict):
            fail(errors, f"{prefix}: every path must be an object")
            continue
        path_id = path.get("id")
        if not isinstance(path_id, str) or not path_id:
            fail(errors, f"{prefix}: path id is missing")
            continue
        if path_id in by_id:
            fail(errors, f"{prefix}: duplicate path id {path_id!r}")
            continue
        by_id[path_id] = path
        path_prefix = f"{prefix}/{path_id}"

        if path.get("status") not in STATUSES:
            fail(errors, f"{path_prefix}: invalid status")
        if not isinstance(path.get("label"), str) or not path.get("label"):
            fail(errors, f"{path_prefix}: label is missing")
        if not isinstance(path.get("evidence"), str) or not path.get("evidence"):
            fail(errors, f"{path_prefix}: evidence is missing")

        first_seen = path.get("firstSeenStage")
        if (
            not isinstance(first_seen, int)
            or isinstance(first_seen, bool)
            or not 1 <= first_seen <= 9
        ):
            fail(errors, f"{path_prefix}: firstSeenStage must be an integer in 1..9")
            first_seen = None

        earliest = path.get("earliestFailure")
        if earliest is not None and (
            not isinstance(earliest, int)
            or isinstance(earliest, bool)
            or not 1 <= earliest <= 9
        ):
            fail(errors, f"{path_prefix}: earliestFailure must be null or an integer in 1..9")
            earliest = None
        if first_seen is not None and earliest is not None and earliest < first_seen:
            fail(errors, f"{path_prefix}: earliestFailure cannot be earlier than firstSeenStage")

        for gate in GATES:
            if not isinstance(path.get(gate), bool):
                fail(errors, f"{path_prefix}: gate {gate} must be boolean")

        scores = path.get("scores")
        if not isinstance(scores, dict) or set(scores) != DIMENSIONS:
            fail(errors, f"{path_prefix}: six score dimensions are required")
        else:
            for dimension, value in scores.items():
                if not isinstance(value, int) or isinstance(value, bool):
                    fail(errors, f"{path_prefix}: score {dimension} must be integer")
                elif not 0 <= value <= 4:
                    fail(errors, f"{path_prefix}: score {dimension} outside 0..4")

        status = path.get("status")
        failed_gate = any(path.get(gate) is False for gate in GATES)
        if path.get("factGate") is False:
            fail(errors, f"{path_prefix}: factual failure invalidates the path")
        if status == "main":
            if earliest is not None:
                fail(errors, f"{path_prefix}: main path cannot have earliestFailure")
            if not all(path.get(gate) is True for gate in GATES):
                fail(errors, f"{path_prefix}: main path must pass every gate")
        elif status in {"rejected", "superseded"} and earliest is None:
            fail(errors, f"{path_prefix}: eliminated path must record earliestFailure")
        elif status == "alternative" and failed_gate and earliest is None:
            fail(errors, f"{path_prefix}: failed alternative must record earliestFailure")
        if failed_gate and earliest is None:
            fail(errors, f"{path_prefix}: failed gate must record earliestFailure")

        check_code_mappings(path, path_prefix, solution_text, errors)

    selected_id = problem.get("selectedPath")
    selected = by_id.get(selected_id)
    mains = [path for path in by_id.values() if path.get("status") == "main"]
    if len(mains) != 1:
        fail(errors, f"{prefix}: exactly one main path is required, got {len(mains)}")
    if selected is None:
        fail(errors, f"{prefix}: selectedPath does not refer to a path")
        return
    if selected.get("status") != "main":
        fail(errors, f"{prefix}: selected path status must be 'main'")
    for gate in GATES:
        if selected.get(gate) is not True:
            fail(errors, f"{prefix}: selected path must pass {gate}")

    selected_scores = selected.get("scores", {})
    if isinstance(selected_scores, dict) and set(selected_scores) == DIMENSIONS:
        selected_min = min(selected_scores.values())
        selected_total = score_total(selected_scores)
        for path_id, path in by_id.items():
            scores = path.get("scores", {})
            if not isinstance(scores, dict) or set(scores) != DIMENSIONS:
                continue
            if path.get("status") != "alternative":
                continue
            if min(scores.values()) > selected_min or (
                min(scores.values()) == selected_min
                and score_total(scores) > selected_total
            ):
                fail(
                    errors,
                    f"{prefix}: alternative {path_id!r} dominates the selected path",
                )


def expect_problem_failure(
    label: str,
    problem: dict,
    mutate: Callable[[dict], None],
) -> None:
    fixture = copy.deepcopy(problem)
    mutate(fixture)
    errors: list[str] = []
    check_problem(fixture, errors)
    if not errors:
        raise AssertionError(f"negative fixture was not rejected: {label}")


def run_fixture_checks(problems: list[dict]) -> None:
    if not problems:
        return
    base = problems[0]

    def remove_selected_method(problem: dict) -> None:
        problem.pop("selectedMethod", None)

    def remove_references(problem: dict) -> None:
        problem.pop("references", None)

    def remove_first_seen(problem: dict) -> None:
        problem["paths"][0].pop("firstSeenStage", None)

    def remove_mapping(problem: dict) -> None:
        problem["paths"][1].pop("codeMappings", None)

    expect_problem_failure("missing selectedMethod", base, remove_selected_method)
    expect_problem_failure("missing references", base, remove_references)
    expect_problem_failure("missing firstSeenStage", base, remove_first_seen)
    expect_problem_failure("main path without codeMappings", base, remove_mapping)


def main() -> int:
    errors: list[str] = []
    check_docs(errors)
    experiment = load_json(DATA_PATH, errors)
    official = load_json(PROBLEMS_PATH, errors)

    if experiment:
        if experiment.get("schemaVersion") != SCHEMA_VERSION:
            fail(errors, f"analysis experiment schemaVersion must be {SCHEMA_VERSION}")
        if experiment.get("mode") != "post-hoc-verification":
            fail(errors, "analysis experiment mode must be post-hoc-verification")
        if set(experiment.get("dimensions", [])) != DIMENSIONS:
            fail(errors, "analysis experiment dimensions are incomplete")
        if set(experiment.get("gates", [])) != GATES:
            fail(errors, "analysis experiment gates are incomplete")

        problems = experiment.get("problems")
        if not isinstance(problems, list):
            fail(errors, "analysis experiment problems must be a list")
            problems = []
        ids = {problem.get("id") for problem in problems if isinstance(problem, dict)}
        if ids != REQUIRED_PROBLEM_IDS:
            fail(
                errors,
                f"analysis experiment problem ids must be {sorted(REQUIRED_PROBLEM_IDS)}, "
                f"got {sorted(ids)}",
            )
        for problem in problems:
            if isinstance(problem, dict):
                check_problem(problem, errors)
        try:
            run_fixture_checks([problem for problem in problems if isinstance(problem, dict)])
        except AssertionError as exc:
            fail(errors, str(exc))

    if experiment and official:
        check_source_alignment(experiment, official, errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    path_count = sum(len(problem["paths"]) for problem in experiment["problems"])
    print(
        "Analysis experiment contract passed: "
        f"{len(experiment['problems'])} problems, {path_count} paths, "
        "schema v2, human-chain migration, references, gates, and code mappings."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
