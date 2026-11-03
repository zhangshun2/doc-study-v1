#!/usr/bin/env python3
"""Validate the four-problem analysis-method experiment."""

from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
LIBRARY_ROOT = REPO_ROOT / "学习文库" / "算法学习"
EXPERIMENT_ROOT = REPO_ROOT / "LeetCode-系统复习" / "07-分析法实验"
DATA_PATH = EXPERIMENT_ROOT / "analysis-experiments.json"
PROBLEMS_PATH = LIBRARY_ROOT / "problems.json"

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
REQUIRED_DOCS = {
    "README.md": [
        "人工过程法负责从题面走到第一次变化",
        "只选一个辅助分析法走完整因果链",
        "问题事实",
    ],
    "分析法实验协议.md": [
        "七阶段、九次交接是共同基线",
        "交接 6 只排除复杂度家族",
        "交接 8 才允许具体候选上桌",
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
        "交接 6 不建立具体候选池",
        "交接 8 才比较具体方向",
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


def check_problem(problem: dict, errors: list[str]) -> None:
    problem_id = problem.get("id")
    prefix = f"problem {problem_id}"
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

        if path.get("status") not in STATUSES:
            fail(errors, f"{prefix}/{path_id}: invalid status")
        if not isinstance(path.get("label"), str) or not path.get("label"):
            fail(errors, f"{prefix}/{path_id}: label is missing")
        if "earliestFailure" not in path:
            fail(errors, f"{prefix}/{path_id}: earliestFailure is required")
        if not isinstance(path.get("evidence"), str) or not path.get("evidence"):
            fail(errors, f"{prefix}/{path_id}: evidence is missing")

        for gate in GATES:
            if not isinstance(path.get(gate), bool):
                fail(errors, f"{prefix}/{path_id}: gate {gate} must be boolean")

        scores = path.get("scores")
        if not isinstance(scores, dict) or set(scores) != DIMENSIONS:
            fail(errors, f"{prefix}/{path_id}: six score dimensions are required")
            continue
        for dimension, value in scores.items():
            if not isinstance(value, int) or isinstance(value, bool):
                fail(errors, f"{prefix}/{path_id}: score {dimension} must be integer")
            elif not 0 <= value <= 4:
                fail(errors, f"{prefix}/{path_id}: score {dimension} outside 0..4")

        if path.get("factGate") is False:
            fail(errors, f"{prefix}/{path_id}: factual failure invalidates the path")
        if path.get("status") == "main":
            if not all(path.get(gate) is True for gate in GATES):
                fail(errors, f"{prefix}/{path_id}: main path must pass every gate")
            if path.get("earliestFailure") is not None:
                fail(errors, f"{prefix}/{path_id}: main path cannot have earliestFailure")

    selected_id = problem.get("selectedPath")
    selected = by_id.get(selected_id)
    if selected is None:
        fail(errors, f"{prefix}: selectedPath does not refer to a path")
        return
    if selected.get("status") != "main":
        fail(errors, f"{prefix}: selected path status must be 'main'")
    for gate in GATES:
        if selected.get(gate) is not True:
            fail(errors, f"{prefix}: selected path must pass {gate}")

    if not isinstance(problem.get("selectedReason"), str) or not problem.get(
        "selectedReason"
    ):
        fail(errors, f"{prefix}: selectedReason is required")
    if not isinstance(problem.get("checkedAlternative"), str) or not problem.get(
        "checkedAlternative"
    ):
        fail(errors, f"{prefix}: checkedAlternative is required")

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


def main() -> int:
    errors: list[str] = []
    check_docs(errors)
    experiment = load_json(DATA_PATH, errors)
    official = load_json(PROBLEMS_PATH, errors)

    if experiment:
        if experiment.get("schemaVersion") != 1:
            fail(errors, "analysis experiment schemaVersion must be 1")
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
        "six dimensions, five admission gates."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
