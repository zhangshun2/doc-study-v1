#!/usr/bin/env python3
"""Compile the authoritative Java blocks and verify all official examples."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


LIBRARY_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = LIBRARY_ROOT / "problems.json"
JAVAC_TIMEOUT_SECONDS = 30
JAVA_TIMEOUT_SECONDS = 10

SUBMISSION_PATTERN = re.compile(
    r"^###\s+LeetCode 可直接提交代码\s*$.*?```java\s*\r?\n(.*?)\r?\n```",
    re.MULTILINE | re.DOTALL,
)
LOCAL_EXAMPLE_PATTERN = re.compile(
    r"^###\s+本地可运行示例\s*$.*?```java\s*\r?\n(.*?)\r?\n```",
    re.MULTILINE | re.DOTALL,
)
PUBLIC_CLASS_PATTERN = re.compile(
    r"\bpublic\s+(?:(?:abstract|final|strictfp)\s+)*class\s+([A-Za-z_$][\w$]*)"
)

OUTER_UNORDERED = {15, 46, 78, 301}
DEEP_UNORDERED = {49}
FLAT_UNORDERED = {1, 347}


class VerificationError(RuntimeError):
    """Raised when a document cannot be extracted or verified."""


def split_top_level(value: str, delimiter: str = ",") -> List[str]:
    parts: List[str] = []
    start = 0
    depth = 0
    quote: Optional[str] = None

    for index, char in enumerate(value):
        if quote is not None:
            if char == "\\":
                continue
            if char == quote:
                quote = None
            continue
        if char in "\"'":
            quote = char
        elif char in "[({":
            depth += 1
        elif char in "])}":
            depth -= 1
        elif char == delimiter and depth == 0:
            parts.append(value[start:index].strip())
            start = index + 1

    parts.append(value[start:].strip())
    return [part for part in parts if part]


def top_level_equals(value: str) -> int:
    depth = 0
    quote: Optional[str] = None

    for index, char in enumerate(value):
        if quote is not None:
            if char == "\\":
                continue
            if char == quote:
                quote = None
            continue
        if char in "\"'":
            quote = char
        elif char in "[({":
            depth += 1
        elif char in "])}":
            depth -= 1
        elif char == "=" and depth == 0:
            return index

    return -1


def parse_literal(raw: str) -> Any:
    normalized = raw.strip()

    def replace_character(match: re.Match[str]) -> str:
        value = match.group(1).replace("\\'", "'")
        return json.dumps(value, ensure_ascii=False)

    normalized = re.sub(
        r"'([^'\\]*(?:\\.[^'\\]*)*)'",
        replace_character,
        normalized,
    )
    return json.loads(normalized)


def parse_arguments(input_text: str, params: Sequence[Dict[str, Any]]) -> List[Any]:
    by_name: Dict[str, Any] = {}
    unnamed: List[Any] = []

    for part in split_top_level(input_text):
        equals = top_level_equals(part)
        if equals >= 0:
            by_name[part[:equals].strip()] = parse_literal(part[equals + 1 :])
        else:
            unnamed.append(parse_literal(part))

    missing = object()
    unnamed_index = 0
    aliases = {"list1": "l1", "list2": "l2"}
    values: List[Any] = []

    for param in params:
        name = param["name"]
        value = by_name.get(name, missing)
        if value is missing and name in aliases:
            value = by_name.get(aliases[name], missing)
        if value is missing and unnamed_index < len(unnamed):
            value = unnamed[unnamed_index]
            unnamed_index += 1
        values.append(None if value is missing else value)

    return values


def java_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False).replace("\u2028", "\\u2028").replace(
        "\u2029", "\\u2029"
    )


def java_character(value: str) -> str:
    if len(value) != 1:
        raise VerificationError(f"Expected one Java character, got {value!r}")
    if value == "\\":
        return "'\\\\'"
    if value == "'":
        return "'\\''"
    if value == "\n":
        return "'\\n'"
    if value == "\r":
        return "'\\r'"
    if value == "\t":
        return "'\\t'"
    return f"'{value}'"


def int_array(value: Sequence[Any]) -> str:
    return "new int[]{" + ", ".join(str(item) for item in value) + "}"


def integer_array(value: Sequence[Any]) -> str:
    items = ["null" if item is None else str(item) for item in value]
    return "new Integer[]{" + ", ".join(items) + "}"


def java_expression(value_type: str, value: Any) -> str:
    if value_type == "integer":
        return str(value)
    if value_type == "boolean":
        return "true" if value else "false"
    if value_type == "string":
        return java_string(str(value))
    if value_type == "integer[]":
        return int_array(value)
    if value_type == "integer[][]":
        return "new int[][]{" + ", ".join(int_array(row) for row in value) + "}"
    if value_type == "character[][]":
        rows = [
            "new char[]{" + ", ".join(java_character(str(item)) for item in row) + "}"
            for row in value
        ]
        return "new char[][]{" + ", ".join(rows) + "}"
    if value_type == "string[]":
        return "new String[]{" + ", ".join(java_string(str(item)) for item in value) + "}"
    if value_type == "list<string>":
        return "java.util.Arrays.asList(" + ", ".join(
            java_string(str(item)) for item in value
        ) + ")"
    if value_type == "ListNode":
        return f"buildList({int_array(value)})"
    if value_type == "ListNode[]":
        return "new ListNode[]{" + ", ".join(
            f"buildList({int_array(item)})" for item in value
        ) + "}"
    if value_type == "TreeNode":
        return f"buildTree({integer_array(value)})"
    raise VerificationError(f"Unsupported Java input type: {value_type}")


def java_type(value_type: str) -> str:
    types = {
        "integer": "int",
        "boolean": "boolean",
        "string": "String",
        "integer[]": "int[]",
        "integer[][]": "int[][]",
        "character[][]": "char[][]",
        "string[]": "String[]",
        "list<string>": "java.util.List<String>",
        "ListNode": "ListNode",
        "ListNode[]": "ListNode[]",
        "TreeNode": "TreeNode",
    }
    if value_type not in types:
        raise VerificationError(f"Unsupported Java declaration type: {value_type}")
    return types[value_type]


def canonical_value(value: Any, mode: str = "ordered") -> str:
    if isinstance(value, list):
        child_mode = "deep-unordered" if mode == "deep-unordered" else "ordered"
        children = [canonical_value(item, child_mode) for item in value]
        if mode in {"outer-unordered", "deep-unordered", "flat-unordered"}:
            children.sort()
        return "[" + ",".join(children) + "]"
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        return java_string(value)
    if isinstance(value, (int, float)):
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return str(value)
    raise VerificationError(f"Unsupported JSON value in expected output: {value!r}")


def comparison_mode(problem_id: int) -> str:
    if problem_id in DEEP_UNORDERED:
        return "deep-unordered"
    if problem_id in OUTER_UNORDERED:
        return "outer-unordered"
    if problem_id in FLAT_UNORDERED:
        return "flat-unordered"
    return "ordered"


def inject_support_types(source: str, force: bool = False) -> str:
    support_parts: List[str] = []
    if (force or re.search(r"\bListNode\b", source)) and not re.search(
        r"\bclass\s+ListNode\b", source
    ):
        support_parts.append(
            """class ListNode {
    int val;
    ListNode next;
    ListNode() {}
    ListNode(int val) { this.val = val; }
    ListNode(int val, ListNode next) { this.val = val; this.next = next; }
}
"""
        )
    if (force or re.search(r"\bTreeNode\b", source)) and not re.search(
        r"\bclass\s+TreeNode\b", source
    ):
        support_parts.append(
            """class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;
    TreeNode() {}
    TreeNode(int val) { this.val = val; }
    TreeNode(int val, TreeNode left, TreeNode right) {
        this.val = val;
        this.left = left;
        this.right = right;
    }
}
"""
        )

    if not support_parts:
        return source

    support = "\n".join(support_parts) + "\n"
    imports = list(re.finditer(r"^import\s+[^;]+;\s*$", source, re.MULTILINE))
    if not imports:
        return support + source
    last = imports[-1]
    return source[: last.end()] + "\n" + support + source[last.end() :]


def extract_block(markdown: str, pattern: re.Pattern[str], problem: Dict[str, Any], label: str) -> str:
    match = pattern.search(markdown)
    if not match:
        raise VerificationError(f"{problem['id']}: {label} Java block missing")
    return match.group(1)


def public_class_name(source: str) -> Optional[str]:
    match = PUBLIC_CLASS_PATTERN.search(source)
    return match.group(1) if match else None


def run_process(
    command: Sequence[str],
    cwd: Path,
    timeout_seconds: int,
    label: str,
) -> subprocess.CompletedProcess[str]:
    try:
        result = subprocess.run(
            list(command),
            cwd=str(cwd),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        raise VerificationError(
            f"{label}: timed out after {timeout_seconds} seconds"
        ) from error

    if result.returncode != 0:
        details = (result.stderr or result.stdout or "").strip()
        raise VerificationError(
            f"{label}: command exited with {result.returncode}"
            + (f"\n{details}" if details else "")
        )
    return result


def write_java_source(directory: Path, source: str, fallback_name: str) -> Tuple[Path, str]:
    directory.mkdir(parents=True, exist_ok=True)
    class_name = public_class_name(source) or fallback_name
    source_path = directory / f"{class_name}.java"
    with source_path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(source)
    return source_path, class_name


def compile_java(source: str, directory: Path, fallback_name: str, label: str) -> Tuple[Path, str]:
    source_path, class_name = write_java_source(directory, source, fallback_name)
    run_process(
        ["javac", "-encoding", "UTF-8", str(source_path)],
        directory,
        JAVAC_TIMEOUT_SECONDS,
        f"{label}: javac",
    )
    return source_path, class_name


def run_java(class_name: str, directory: Path, label: str) -> str:
    result = run_process(
        ["java", "-cp", str(directory), class_name],
        directory,
        JAVA_TIMEOUT_SECONDS,
        f"{label}: java",
    )
    return result.stdout


def regular_example_code(problem: Dict[str, Any], example: Dict[str, str], index: int) -> str:
    signature = problem["signature"]
    params = signature.get("params") or []
    values = parse_arguments(example["input"], params)
    if any(value is None for value in values):
        raise VerificationError(
            f"{problem['id']} example {index + 1}: input could not be mapped to all params"
        )

    declarations: List[str] = []
    arguments: List[str] = []
    root_variable: Optional[str] = None

    for param_index, param in enumerate(params):
        param_name = param["name"]
        variable = f"{param_name}_{index}"
        value = values[param_index]

        if problem["id"] == 236 and param_name in {"p", "q"}:
            if root_variable is None:
                raise VerificationError("236: p/q appeared before root")
            declarations.append(
                f"TreeNode {variable} = findNode({root_variable}, {value});"
            )
        else:
            effective_type = "TreeNode" if problem["id"] == 236 else param["type"]
            declarations.append(
                f"{java_type(effective_type)} {variable} = "
                f"{java_expression(effective_type, value)};"
            )
            if problem["id"] == 236 and param_name == "root":
                root_variable = variable
        arguments.append(variable)

    method = signature["name"]
    return_type = signature.get("return", {}).get("type")
    call = f"new Solution().{method}({', '.join(arguments)})"
    expected_value = parse_literal(example["output"])
    label = f"{problem['id']} example {index + 1}"

    if problem["id"] == 5:
        assertion = (
            f"assertPalindromeAnswer((String) actual_{index}, "
            f"{len(expected_value)}, {arguments[0]}, {java_string(label)});"
        )
    elif return_type == "double":
        assertion = (
            f"assertDouble((Double) actual_{index}, "
            f"{float(expected_value):g}, {java_string(label)});"
        )
    else:
        mode = comparison_mode(problem["id"])
        platform_empty = (
            return_type in {"ListNode", "TreeNode"}
            and isinstance(expected_value, list)
            and not expected_value
        )
        expected = canonical_value(None if platform_empty else expected_value, mode)
        assertion = (
            f"assertCanonical(actual_{index}, {java_string(expected)}, "
            f"{java_string(mode)}, {java_string(label)});"
        )

    if return_type == "void":
        output_index = int(signature.get("output", {}).get("paramindex", 0))
        invocation = f"{call};\nObject actual_{index} = {arguments[output_index]};"
    elif problem["id"] == 236:
        invocation = (
            f"TreeNode result_{index} = {call};\n"
            f"Object actual_{index} = result_{index} == null ? null : result_{index}.val;"
        )
    else:
        invocation = f"Object actual_{index} = {call};"

    return (
        f"// {label}\n"
        + "\n".join(declarations)
        + "\n"
        + invocation
        + "\n"
        + assertion
        + "\npassed++;"
    )


def design_example_code(problem: Dict[str, Any], example: Dict[str, str], index: int) -> str:
    lines = [line for line in re.split(r"\r?\n", example["input"]) if line.strip()]
    if len(lines) != 2:
        raise VerificationError(
            f"{problem['id']}: design example input is not two JSON arrays"
        )

    operations = json.loads(lines[0])
    arguments = json.loads(lines[1])
    expected = json.loads(example["output"])
    class_name = problem["signature"]["classname"]
    variable = f"instance_{index}"
    code = [f"// {problem['id']} design example {index + 1}"]

    constructor_arguments = arguments[0] if arguments else []
    code.append(
        f"{class_name} {variable} = new {class_name}("
        + ", ".join(java_inline_literal(value) for value in constructor_arguments)
        + ");"
    )

    for operation_index in range(1, len(operations)):
        method = operations[operation_index]
        operation_arguments = (
            arguments[operation_index] if operation_index < len(arguments) else []
        )
        call = (
            f"{variable}.{method}("
            + ", ".join(java_inline_literal(value) for value in operation_arguments)
            + ")"
        )
        if expected[operation_index] is None:
            code.append(f"{call};")
        else:
            canonical = canonical_value(expected[operation_index])
            label = f"{problem['id']} operation {operation_index}"
            code.append(
                f"assertCanonical({call}, {java_string(canonical)}, "
                f'"ordered", {java_string(label)});'
            )

    code.append("passed++;")
    return "\n".join(code)


def java_inline_literal(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        return java_string(value)
    if isinstance(value, (int, float)):
        return str(value)
    raise VerificationError(f"Unsupported design argument: {value!r}")


HARNESS_TEMPLATE = r"""
class OfficialExampleTest {
    private static int passed = 0;

    public static void main(String[] args) {
        runExamples();
        System.out.println("OFFICIAL_EXAMPLES_PASSED=" + passed);
    }

    private static void assertDouble(double actual, double expected, String label) {
        if (Math.abs(actual - expected) > 1e-9) {
            throw new AssertionError(label + ": expected " + expected + ", actual " + actual);
        }
    }

    private static void assertPalindromeAnswer(String actual, int expectedLength, String input, String label) {
        boolean palindrome = true;
        for (int left = 0, right = actual.length() - 1; left < right; left++, right--) {
            if (actual.charAt(left) != actual.charAt(right)) palindrome = false;
        }
        if (actual.length() != expectedLength || !palindrome || !input.contains(actual)) {
            throw new AssertionError(label + ": invalid palindrome answer " + actual);
        }
    }

    private static void assertCanonical(Object actual, String expected, String mode, String label) {
        String actualText;
        if ("outer-unordered".equals(mode) || "flat-unordered".equals(mode)) {
            actualText = canonicalUnorderedOuter(actual, false);
        } else if ("deep-unordered".equals(mode)) {
            actualText = canonicalUnorderedOuter(actual, true);
        } else {
            actualText = canonical(actual);
        }
        if (!expected.equals(actualText)) {
            throw new AssertionError(label + ": expected " + expected + ", actual " + actualText);
        }
    }

    private static String canonicalUnorderedOuter(Object value, boolean deep) {
        java.util.List<String> children = childCanonicalValues(value, deep);
        java.util.Collections.sort(children);
        return "[" + join(children) + "]";
    }

    private static java.util.List<String> childCanonicalValues(Object value, boolean deep) {
        java.util.List<String> children = new java.util.ArrayList<>();
        if (value instanceof Iterable<?>) {
            for (Object child : (Iterable<?>) value) {
                children.add(deep && isContainer(child) ? canonicalUnorderedOuter(child, true) : canonical(child));
            }
        } else if (value != null && value.getClass().isArray()) {
            int length = java.lang.reflect.Array.getLength(value);
            for (int i = 0; i < length; i++) {
                Object child = java.lang.reflect.Array.get(value, i);
                children.add(deep && isContainer(child) ? canonicalUnorderedOuter(child, true) : canonical(child));
            }
        }
        return children;
    }

    private static boolean isContainer(Object value) {
        return value instanceof Iterable<?> || (value != null && value.getClass().isArray());
    }

    private static String canonical(Object value) {
        if (value == null) return "null";
        if (value instanceof String || value instanceof Character) return quote(String.valueOf(value));
        if (value instanceof Number || value instanceof Boolean) return String.valueOf(value);
        if (value instanceof ListNode) {
            java.util.List<String> values = new java.util.ArrayList<>();
            for (ListNode node = (ListNode) value; node != null; node = node.next) values.add(String.valueOf(node.val));
            return "[" + join(values) + "]";
        }
        if (value instanceof TreeNode) return canonicalTree((TreeNode) value);
        if (value instanceof Iterable<?>) {
            java.util.List<String> values = new java.util.ArrayList<>();
            for (Object child : (Iterable<?>) value) values.add(canonical(child));
            return "[" + join(values) + "]";
        }
        if (value.getClass().isArray()) {
            java.util.List<String> values = new java.util.ArrayList<>();
            int length = java.lang.reflect.Array.getLength(value);
            for (int i = 0; i < length; i++) values.add(canonical(java.lang.reflect.Array.get(value, i)));
            return "[" + join(values) + "]";
        }
        return quote(String.valueOf(value));
    }

    private static String canonicalTree(TreeNode root) {
        if (root == null) return "[]";
        java.util.List<String> values = new java.util.ArrayList<>();
        java.util.Queue<TreeNode> queue = new java.util.LinkedList<>();
        queue.offer(root);
        while (!queue.isEmpty()) {
            TreeNode node = queue.poll();
            if (node == null) {
                values.add("null");
            } else {
                values.add(String.valueOf(node.val));
                queue.offer(node.left);
                queue.offer(node.right);
            }
        }
        while (!values.isEmpty() && "null".equals(values.get(values.size() - 1))) values.remove(values.size() - 1);
        return "[" + join(values) + "]";
    }

    private static String join(java.util.List<String> values) {
        StringBuilder builder = new StringBuilder();
        for (int i = 0; i < values.size(); i++) {
            if (i > 0) builder.append(',');
            builder.append(values.get(i));
        }
        return builder.toString();
    }

    private static String quote(String value) {
        return "\"" + value.replace("\\", "\\\\").replace("\"", "\\\"") + "\"";
    }

    private static ListNode buildList(int[] values) {
        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;
        for (int value : values) {
            tail.next = new ListNode(value);
            tail = tail.next;
        }
        return dummy.next;
    }

    private static TreeNode buildTree(Integer[] values) {
        if (values.length == 0 || values[0] == null) return null;
        TreeNode root = new TreeNode(values[0]);
        java.util.Queue<TreeNode> queue = new java.util.ArrayDeque<>();
        queue.offer(root);
        int index = 1;
        while (!queue.isEmpty() && index < values.length) {
            TreeNode node = queue.poll();
            if (index < values.length && values[index] != null) {
                node.left = new TreeNode(values[index]);
                queue.offer(node.left);
            }
            index++;
            if (index < values.length && values[index] != null) {
                node.right = new TreeNode(values[index]);
                queue.offer(node.right);
            }
            index++;
        }
        return root;
    }

    private static TreeNode findNode(TreeNode root, int value) {
        if (root == null) return null;
        if (root.val == value) return root;
        TreeNode left = findNode(root.left, value);
        return left != null ? left : findNode(root.right, value);
    }

    private static void runExamples() {
/*__EXAMPLES__*/
    }
}
"""


def verify_problem(problem: Dict[str, Any], temp_root: Path) -> int:
    problem_id = int(problem["id"])
    slug = problem["slug"]
    document_path = LIBRARY_ROOT / Path(*problem["relativePath"].split("/"))
    markdown = document_path.read_text(encoding="utf-8")
    case_root = temp_root / f"{problem_id}-{slug}"

    submission = extract_block(
        markdown, SUBMISSION_PATTERN, problem, "submission"
    )
    local_example = extract_block(
        markdown, LOCAL_EXAMPLE_PATTERN, problem, "local example"
    )

    submission_source = inject_support_types(submission)
    compile_java(
        submission_source,
        case_root / "submission",
        "Submission",
        f"{problem_id}-{slug} [submission]",
    )

    local_source = inject_support_types(local_example)
    _, local_class = compile_java(
        local_source,
        case_root / "local",
        "Main",
        f"{problem_id}-{slug} [local]",
    )
    if "static void main" not in local_source:
        raise VerificationError(f"{problem_id}-{slug} [local]: main method missing")
    run_java(local_class, case_root / "local", f"{problem_id}-{slug} [local]")

    examples = problem.get("officialExamples") or []
    if not examples:
        raise VerificationError(f"{problem_id}-{slug}: structured official examples missing")

    generated = [
        design_example_code(problem, example, index)
        if problem.get("signature", {}).get("systemdesign")
        else regular_example_code(problem, example, index)
        for index, example in enumerate(examples)
    ]
    harness = HARNESS_TEMPLATE.replace("/*__EXAMPLES__*/", "\n\n".join(generated))
    runner_source = inject_support_types(submission, force=True).rstrip() + "\n\n" + harness
    _, runner_class = compile_java(
        runner_source,
        case_root / "official",
        "OfficialExampleTest",
        f"{problem_id}-{slug} [official]",
    )
    if runner_class != "OfficialExampleTest":
        runner_class = "OfficialExampleTest"
    output = run_java(
        runner_class,
        case_root / "official",
        f"{problem_id}-{slug} [official]",
    )
    match = re.search(r"OFFICIAL_EXAMPLES_PASSED=(\d+)", output)
    if not match:
        raise VerificationError(
            f"{problem_id}-{slug} [official]: runner did not report passed count"
        )

    passed = int(match.group(1))
    if passed != len(examples):
        raise VerificationError(
            f"{problem_id}-{slug}: expected {len(examples)} passing examples, "
            f"runner reported {passed}"
        )
    return passed


def main() -> int:
    if shutil.which("javac") is None or shutil.which("java") is None:
        print("javac and java must both be available on PATH.", file=sys.stderr)
        return 1
    if not MANIFEST_PATH.exists():
        print(f"Official manifest not found: {MANIFEST_PATH}", file=sys.stderr)
        return 1

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    problems = manifest["problems"]
    failures: List[str] = []
    verified_examples = 0

    with tempfile.TemporaryDirectory(prefix="official-examples-") as temp_name:
        temp_root = Path(temp_name)
        for problem in problems:
            try:
                verified_examples += verify_problem(problem, temp_root)
            except (OSError, ValueError, VerificationError) as error:
                failures.append(f"{problem['id']}-{problem['slug']}: {error}")

    total_examples = sum(len(problem.get("officialExamples") or []) for problem in problems)
    print(f"Problems tested: {len(problems) - len(failures)}/{len(problems)}")
    print(f"Submission blocks compiled: {len(problems) - len(failures)}/{len(problems)}")
    print(f"Local examples compiled and run: {len(problems) - len(failures)}/{len(problems)}")
    print(f"Official examples verified: {verified_examples}/{total_examples}")
    print(f"Official example failures: {len(failures)}")

    if failures:
        for failure in failures:
            print(f"\n- {failure}", file=sys.stderr)
        return 1

    print("All structured official examples passed against the submission code.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
