import { execFileSync } from "node:child_process";
import { mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDirectory = path.dirname(fileURLToPath(import.meta.url));
const libraryRoot = path.resolve(scriptDirectory, "..");
const manifest = JSON.parse(await readFile(path.join(libraryRoot, "problems.json"), "utf8"));
const tempRoot = await mkdtemp(path.join(os.tmpdir(), "official-examples-"));
const failures = [];
let verifiedExamples = 0;

function splitTopLevel(value, delimiter = ",") {
  const parts = [];
  let start = 0;
  let depth = 0;
  let quote = null;
  for (let index = 0; index < value.length; index++) {
    const char = value[index];
    if (quote) {
      if (char === "\\") index++;
      else if (char === quote) quote = null;
      continue;
    }
    if (char === "\"" || char === "'") { quote = char; continue; }
    if ("[({".includes(char)) depth++;
    else if ("])}".includes(char)) depth--;
    else if (char === delimiter && depth === 0) {
      parts.push(value.slice(start, index).trim());
      start = index + 1;
    }
  }
  parts.push(value.slice(start).trim());
  return parts.filter(Boolean);
}

function topLevelEquals(value) {
  let depth = 0;
  let quote = null;
  for (let index = 0; index < value.length; index++) {
    const char = value[index];
    if (quote) {
      if (char === "\\") index++;
      else if (char === quote) quote = null;
      continue;
    }
    if (char === "\"" || char === "'") { quote = char; continue; }
    if ("[({".includes(char)) depth++;
    else if ("])}".includes(char)) depth--;
    else if (char === "=" && depth === 0) return index;
  }
  return -1;
}

function parseLiteral(raw) {
  const normalized = raw.trim().replace(/'([^'\\]*(?:\\.[^'\\]*)*)'/g,
    (_, value) => JSON.stringify(value.replace(/\\'/g, "'")));
  return JSON.parse(normalized);
}

function parseArguments(input, params) {
  const byName = new Map();
  const unnamed = [];
  for (const part of splitTopLevel(input)) {
    const equals = topLevelEquals(part);
    if (equals >= 0) {
      byName.set(part.slice(0, equals).trim(), parseLiteral(part.slice(equals + 1)));
    } else {
      unnamed.push(parseLiteral(part));
    }
  }
  let unnamedIndex = 0;
  const aliases = { list1: "l1", list2: "l2" };
  return params.map((param) => byName.has(param.name)
    ? byName.get(param.name)
    : byName.has(aliases[param.name])
      ? byName.get(aliases[param.name])
      : unnamed[unnamedIndex++]);
}

function javaString(value) {
  return JSON.stringify(value)
    .replace(/\\u2028/g, "\\u2028")
    .replace(/\\u2029/g, "\\u2029");
}

function intArray(value) {
  return `new int[]{${value.join(", ")}}`;
}

function integerArray(value) {
  return `new Integer[]{${value.map((item) => item === null ? "null" : item).join(", ")}}`;
}

function javaExpression(type, value) {
  switch (type) {
    case "integer": return String(value);
    case "boolean": return String(value);
    case "string": return javaString(value);
    case "integer[]": return intArray(value);
    case "integer[][]": return `new int[][]{${value.map(intArray).join(", ")}}`;
    case "character[][]":
      return `new char[][]{${value.map((row) =>
        `new char[]{${row.map((item) => `'${item.replace(/'/g, "\\'")}'`).join(", ")}}`).join(", ")}}`;
    case "string[]": return `new String[]{${value.map(javaString).join(", ")}}`;
    case "list<string>": return `java.util.Arrays.asList(${value.map(javaString).join(", ")})`;
    case "ListNode": return `buildList(${intArray(value)})`;
    case "ListNode[]": return `new ListNode[]{${value.map((item) => `buildList(${intArray(item)})`).join(", ")}}`;
    case "TreeNode": return `buildTree(${integerArray(value)})`;
    default: throw new Error(`Unsupported Java input type: ${type}`);
  }
}

function canonicalJs(value, mode = "ordered") {
  if (Array.isArray(value)) {
    let children = value.map((item) => canonicalJs(item, mode === "deep-unordered" ? mode : "ordered"));
    if (mode === "outer-unordered" || mode === "deep-unordered" || mode === "flat-unordered") {
      children = children.sort();
    }
    return `[${children.join(",")}]`;
  }
  return JSON.stringify(value);
}

function javaLiteral(value) {
  return javaString(value);
}

const outerUnordered = new Set([15, 46, 78]);
const deepUnordered = new Set([49]);
const flatUnordered = new Set([1, 347]);

function comparisonMode(id) {
  if (deepUnordered.has(id)) return "deep-unordered";
  if (outerUnordered.has(id)) return "outer-unordered";
  if (flatUnordered.has(id)) return "flat-unordered";
  return "ordered";
}

function injectSupportTypes(source) {
  const support = `
class ListNode {
    int val;
    ListNode next;
    ListNode() {}
    ListNode(int val) { this.val = val; }
    ListNode(int val, ListNode next) { this.val = val; this.next = next; }
}

class TreeNode {
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

`;
  const imports = [...source.matchAll(/^import\s+[^;]+;\s*$/gm)];
  if (!imports.length) return support + source;
  const last = imports.at(-1);
  const index = last.index + last[0].length;
  return `${source.slice(0, index)}\n${support}${source.slice(index)}`;
}

function extractSubmission(markdown, problem) {
  const match = /### LeetCode 可直接提交代码[\s\S]*?```java\s*\n([\s\S]*?)\n```/.exec(markdown);
  if (!match) throw new Error(`${problem.id}: submission Java block missing`);
  return match[1];
}

function regularExampleCode(problem, example, index) {
  const params = problem.signature.params ?? [];
  const values = parseArguments(example.input, params);
  if (values.some((value) => value === undefined)) {
    throw new Error(`${problem.id} example ${index + 1}: input could not be mapped to all params`);
  }
  const declarations = [];
  const argumentsList = [];
  let rootVariable = null;
  for (let paramIndex = 0; paramIndex < params.length; paramIndex++) {
    const param = params[paramIndex];
    const variable = `${param.name}_${index}`;
    if (problem.id === 236 && (param.name === "p" || param.name === "q")) {
      declarations.push(`TreeNode ${variable} = findNode(${rootVariable}, ${values[paramIndex]});`);
    } else {
      const effectiveType = problem.id === 236 && param.name === "root" ? "TreeNode" : param.type;
      declarations.push(`${javaType(effectiveType)} ${variable} = ${javaExpression(effectiveType, values[paramIndex])};`);
      if (problem.id === 236 && param.name === "root") rootVariable = variable;
    }
    argumentsList.push(variable);
  }

  const method = problem.signature.name;
  const returnType = problem.signature.return?.type;
  const call = `new Solution().${method}(${argumentsList.join(", ")})`;
  const expectedValue = parseLiteral(example.output);
  const label = `${problem.id} example ${index + 1}`;
  let assertion;
  if (problem.id === 5) {
    assertion = `assertPalindromeAnswer((String) actual_${index}, ${javaLiteral(expectedValue.length)}, ${argumentsList[0]}, ${javaLiteral(label)});`;
  } else if (returnType === "double") {
    assertion = `assertDouble((Double) actual_${index}, ${Number(expectedValue)}, ${javaLiteral(label)});`;
  } else {
    const mode = comparisonMode(problem.id);
    const platformEmpty = (returnType === "ListNode" || returnType === "TreeNode")
      && Array.isArray(expectedValue) && expectedValue.length === 0;
    const expected = canonicalJs(platformEmpty ? null : expectedValue, mode);
    assertion = `assertCanonical(actual_${index}, ${javaLiteral(expected)}, ${javaLiteral(mode)}, ${javaLiteral(label)});`;
  }

  let invocation;
  if (returnType === "void") {
    const outputIndex = Number(problem.signature.output?.paramindex ?? 0);
    invocation = `${call};\nObject actual_${index} = ${argumentsList[outputIndex]};`;
  } else if (problem.id === 236) {
    invocation = `TreeNode result_${index} = ${call};\nObject actual_${index} = result_${index} == null ? null : result_${index}.val;`;
  } else {
    invocation = `Object actual_${index} = ${call};`;
  }
  return `// ${label}\n${declarations.join("\n")}\n${invocation}\n${assertion}\npassed++;`;
}

function javaType(type) {
  const types = {
    integer: "int", boolean: "boolean", string: "String", "integer[]": "int[]",
    "integer[][]": "int[][]", "character[][]": "char[][]", "string[]": "String[]",
    "list<string>": "java.util.List<String>", ListNode: "ListNode", "ListNode[]": "ListNode[]",
    TreeNode: "TreeNode",
  };
  if (!types[type]) throw new Error(`Unsupported Java declaration type: ${type}`);
  return types[type];
}

function designExampleCode(problem, example, index) {
  const lines = example.input.split(/\r?\n/).filter((line) => line.trim());
  if (lines.length !== 2) throw new Error(`${problem.id}: design example input is not two JSON arrays`);
  const operations = JSON.parse(lines[0]);
  const args = JSON.parse(lines[1]);
  const expected = JSON.parse(example.output);
  const className = problem.signature.classname;
  const variable = `instance_${index}`;
  const code = [`// ${problem.id} design example ${index + 1}`];
  code.push(`${className} ${variable} = new ${className}(${(args[0] ?? []).join(", ")});`);
  for (let operationIndex = 1; operationIndex < operations.length; operationIndex++) {
    const method = operations[operationIndex];
    const call = `${variable}.${method}(${(args[operationIndex] ?? []).join(", ")})`;
    if (expected[operationIndex] === null) code.push(`${call};`);
    else code.push(`assertCanonical(${call}, ${javaLiteral(canonicalJs(expected[operationIndex]))}, "ordered", ${javaLiteral(`${problem.id} operation ${operationIndex}`)});`);
  }
  code.push("passed++;");
  return code.join("\n");
}

const harnessHelpers = String.raw`
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
`;

try {
  for (const problem of manifest.problems) {
    try {
      const filePath = path.join(libraryRoot, ...problem.relativePath.split("/"));
      const markdown = await readFile(filePath, "utf8");
      const submission = injectSupportTypes(extractSubmission(markdown, problem));
      const examples = problem.officialExamples.map((example, index) =>
        problem.signature?.systemdesign
          ? designExampleCode(problem, example, index)
          : regularExampleCode(problem, example, index));
      const harness = harnessHelpers.replace("/*__EXAMPLES__*/", examples.join("\n\n"));
      const source = `${submission}\n\n${harness}\n`;
      const caseDirectory = path.join(tempRoot, `${problem.id}-${problem.slug}`);
      await import("node:fs/promises").then(({ mkdir }) => mkdir(caseDirectory, { recursive: true }));
      const sourcePath = path.join(caseDirectory, "OfficialExampleTest.java");
      await writeFile(sourcePath, source, "utf8");
      execFileSync("javac", ["-encoding", "UTF-8", sourcePath], { cwd: caseDirectory, stdio: "pipe", timeout: 30000 });
      const output = execFileSync("java", ["-cp", caseDirectory, "OfficialExampleTest"], {
        cwd: caseDirectory, encoding: "utf8", stdio: ["ignore", "pipe", "pipe"], timeout: 10000,
      });
      const passed = Number(/OFFICIAL_EXAMPLES_PASSED=(\d+)/.exec(output)?.[1]);
      if (passed !== problem.officialExamples.length) {
        throw new Error(`expected ${problem.officialExamples.length} passing examples, runner reported ${passed}`);
      }
      verifiedExamples += passed;
    } catch (error) {
      const stderr = error.stderr?.toString?.("utf8")?.trim();
      failures.push(`${problem.id}-${problem.slug}: ${error.message}${stderr ? `\n${stderr}` : ""}`);
    }
  }
} finally {
  await rm(tempRoot, { recursive: true, force: true });
}

console.log(`Problems tested: ${manifest.problems.length - failures.length}/${manifest.problems.length}`);
console.log(`Official examples verified: ${verifiedExamples}/${manifest.problems.reduce((sum, problem) => sum + problem.officialExamples.length, 0)}`);
console.log(`Official example failures: ${failures.length}`);
if (failures.length) {
  for (const failure of failures) console.error(`\n- ${failure}`);
  process.exitCode = 1;
} else {
  console.log("All structured official examples passed against the submission code.");
}
