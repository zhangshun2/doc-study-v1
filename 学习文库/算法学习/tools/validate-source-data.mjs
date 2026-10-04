import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { splitOfficialContent } from "./upgrade-docs.mjs";

const scriptDirectory = path.dirname(fileURLToPath(import.meta.url));
const libraryRoot = path.resolve(scriptDirectory, "..");
const manifest = JSON.parse(await readFile(path.join(libraryRoot, "problems.json"), "utf8"));
const failures = [];

function fail(problem, message) {
  failures.push(`${problem.id}-${problem.slug}: ${message}`);
}

function parseFrontMatter(markdown) {
  const match = markdown.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n/);
  if (!match) {
    return null;
  }
  const result = {};
  for (const line of match[1].split(/\r?\n/)) {
    const keyValue = line.match(/^([A-Za-z][A-Za-z0-9]*):\s*(.*)$/);
    if (!keyValue) continue;
    const [, key, raw] = keyValue;
    try {
      result[key] = JSON.parse(raw);
    } catch {
      result[key] = raw;
    }
  }
  return result;
}

function bodyOf(markdown, heading) {
  const escaped = heading.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const match = new RegExp(`^## ${escaped}\\s*$([\\s\\S]*?)(?=^##\\s+|(?![\\s\\S]))`, "m").exec(markdown);
  return match?.[1]?.trim() ?? null;
}

function normalized(value) {
  return value
    .replace(/\r/g, "")
    .replace(/[ \t]+$/gm, "")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

function sameArray(left, right) {
  return JSON.stringify(left) === JSON.stringify(right);
}

function mismatchSummary(actual, expected) {
  const left = normalized(actual ?? "");
  const right = normalized(expected ?? "");
  let index = 0;
  while (index < left.length && index < right.length && left[index] === right[index]) index++;
  return `at ${index}; actual=${JSON.stringify(left.slice(index, index + 60))}; expected=${JSON.stringify(right.slice(index, index + 60))}`;
}

function expectedJavaType(type) {
  const types = {
    integer: "int",
    "integer[]": "int[]",
    "integer[][]": "int[][]",
    character: "char",
    "character[][]": "char[][]",
    string: "String",
    "string[]": "String[]",
    boolean: "boolean",
    double: "double",
    void: "void",
    ListNode: "ListNode",
    "ListNode[]": "ListNode[]",
    TreeNode: "TreeNode",
    "list<integer>": "List<Integer>",
    "list<string>": "List<String>",
    "list<list<integer>>": "List<List<Integer>>",
    "list<list<string>>": "List<List<String>>",
  };
  return types[type] ?? type;
}

function normalizeJavaType(type) {
  return type
    .replace(/\b(?:java\.util\.)/g, "")
    .replace(/\s+/g, "")
    .replace(/\?extends/g, "?");
}

function validateMethodSignature(problem, source, method) {
  const expression = new RegExp(`\\bpublic\\s+([A-Za-z0-9_.$<>?, \\[\\]]+)\\s+${method.name}\\s*\\(([^)]*)\\)`);
  const match = expression.exec(source);
  if (!match) {
    fail(problem, `public Java method signature missing: ${method.name}`);
    return;
  }
  const actualReturn = normalizeJavaType(match[1]);
  const officialMatch = expression.exec(problem.javaTemplate ?? "");
  const expectedReturn = officialMatch
    ? normalizeJavaType(officialMatch[1])
    : normalizeJavaType(expectedJavaType(method.return?.type ?? "void"));
  if (actualReturn !== expectedReturn) {
    fail(problem, `${method.name} return type mismatch: expected ${expectedReturn}, found ${actualReturn}`);
  }
  const actualParams = match[2].trim()
    ? match[2].split(",").map((param) => normalizeJavaType(param.trim().replace(/\s+[A-Za-z_$][\w$]*$/, "")))
    : [];
  const expectedParams = officialMatch
    ? (officialMatch[2].trim()
      ? officialMatch[2].split(",").map((param) => normalizeJavaType(param.trim().replace(/\s+[A-Za-z_$][\w$]*$/, "")))
      : [])
    : (method.params ?? []).map((param) => normalizeJavaType(expectedJavaType(param.type)));
  if (!sameArray(actualParams, expectedParams)) {
    fail(problem, `${method.name} parameter types mismatch: expected ${expectedParams.join(",")}, found ${actualParams.join(",")}`);
  }
}

if (manifest.schemaVersion !== 1) {
  failures.push(`manifest: expected schemaVersion 1, found ${manifest.schemaVersion}`);
}
if (manifest.problems.length !== 60) {
  failures.push(`manifest: expected 60 problems, found ${manifest.problems.length}`);
}

const ids = manifest.problems.map((problem) => problem.id);
if (new Set(ids).size !== ids.length) {
  failures.push("manifest: duplicate problem ids");
}

for (const problem of manifest.problems) {
  if (!Array.isArray(problem.officialExamples) || problem.officialExamples.length === 0) {
    fail(problem, "structured official examples are missing");
  } else {
    for (const [index, example] of problem.officialExamples.entries()) {
      if (typeof example.input !== "string" || typeof example.output !== "string") {
        fail(problem, `official example ${index + 1} is missing input or output`);
      }
    }
  }
  const contentHash = createHash("sha256")
    .update(problem.translatedContentHtml ?? "", "utf8")
    .digest("hex");
  if (contentHash !== problem.sourceContentSha256) {
    fail(problem, "manifest HTML does not match sourceContentSha256");
  }

  const filePath = path.join(libraryRoot, ...problem.relativePath.split("/"));
  const bytes = await readFile(filePath);
  if (bytes.length >= 3 && bytes[0] === 0xef && bytes[1] === 0xbb && bytes[2] === 0xbf) {
    fail(problem, "UTF-8 BOM detected");
  }
  const markdown = bytes.toString("utf8");
  const frontMatter = parseFrontMatter(markdown);
  if (!frontMatter) {
    fail(problem, "front matter missing");
    continue;
  }

  const scalarFields = [
    ["schemaVersion", 2],
    ["leetcodeId", problem.id],
    ["slug", problem.slug],
    ["titleCn", problem.titleCn],
    ["titleEn", problem.titleEn],
    ["difficulty", problem.difficulty],
    ["sourceUrl", problem.sourceUrl],
    ["sourceCheckedAt", problem.sourceCheckedAt],
    ["sourceContentSha256", problem.sourceContentSha256],
    ["primaryPattern", problem.primaryPattern],
  ];
  for (const [field, expected] of scalarFields) {
    if (frontMatter[field] !== expected) {
      fail(problem, `front matter ${field} mismatch`);
    }
  }
  if (!sameArray(frontMatter.checklistPriorities, problem.checklistPriorities)) {
    fail(problem, "front matter checklistPriorities mismatch");
  }
  if (!sameArray(frontMatter.checklistTags, problem.checklistTags)) {
    fail(problem, "front matter checklistTags mismatch");
  }

  const expectedTitle = `# ${problem.id}. ${problem.titleCn} / ${problem.titleEn}`;
  if (!markdown.includes(expectedTitle)) {
    fail(problem, "canonical title missing");
  }

  const official = splitOfficialContent(problem.translatedContentHtml);
  const actualDescription = bodyOf(markdown, "官方题意（LeetCode 中文题面）");
  const actualExamples = bodyOf(markdown, "官方示例");
  const actualConstraints = bodyOf(markdown, "官方约束");
  if (!actualDescription || !normalized(actualDescription).includes(normalized(official.description))) {
    fail(problem, "official description differs from the stored snapshot");
  }
  if (!actualExamples || !normalized(actualExamples).includes(normalized(official.examples))) {
    fail(problem, `official examples differ from the stored snapshot (${mismatchSummary(actualExamples, official.examples)})`);
  }
  if (!actualConstraints || !normalized(actualConstraints).includes(normalized(official.constraints))) {
    fail(problem, "official constraints differ from the stored snapshot");
  }

  const requiredHeadings = [
    "## 官方题意（LeetCode 中文题面）",
    "## 官方示例",
    "## 官方约束",
    "## 官方额外提示",
    "## 学习提示（非官方）",
    "## 性能目标与约束推导",
    "## 补充自测用例",
    "### LeetCode 可直接提交代码",
    "### 本地可运行示例",
  ];
  let previousIndex = -1;
  for (const heading of requiredHeadings) {
    const index = markdown.indexOf(heading);
    if (index < 0) {
      fail(problem, `required heading missing: ${heading}`);
    } else if (index <= previousIndex) {
      fail(problem, `heading order is invalid at: ${heading}`);
    }
    previousIndex = index;
  }

  const submissionMatch = /### LeetCode 可直接提交代码[\s\S]*?```java\s*\n([\s\S]*?)\n```/.exec(markdown);
  const demoMatch = /### 本地可运行示例[\s\S]*?```java\s*\n([\s\S]*?)\n```/.exec(markdown);
  if (!submissionMatch) {
    fail(problem, "submission Java block missing");
  } else {
    const submission = submissionMatch[1];
    const expectedClass = problem.signature?.classname ?? "Solution";
    if (!new RegExp(`\\bclass\\s+${expectedClass}\\b`).test(submission)) {
      fail(problem, `submission class ${expectedClass} missing`);
    }
    if (/\bstatic\s+void\s+main\s*\(/.test(submission)) {
      fail(problem, "submission block contains main");
    }
    if (/\bclass\s+(?:ListNode|TreeNode)\b/.test(submission)) {
      fail(problem, "submission block redefines a platform-managed node type");
    }
    const methods = problem.signature?.methods
      ?? (problem.signature?.name ? [{
        name: problem.signature.name,
        params: problem.signature.params,
        return: problem.signature.return,
      }] : []);
    for (const method of methods) {
      validateMethodSignature(problem, submission, method);
    }
    if (problem.signature?.classname) {
      const constructorExpression = new RegExp(`\\bpublic\\s+${problem.signature.classname}\\s*\\(([^)]*)\\)`);
      const constructor = constructorExpression.exec(submission);
      if (!constructor) {
        fail(problem, `public constructor missing: ${problem.signature.classname}`);
      } else {
        const actualParams = constructor[1].trim()
          ? constructor[1].split(",").map((param) => normalizeJavaType(param.trim().replace(/\s+[A-Za-z_$][\w$]*$/, "")))
          : [];
        const officialConstructor = constructorExpression.exec(problem.javaTemplate ?? "");
        const expectedParams = officialConstructor
          ? (officialConstructor[1].trim()
            ? officialConstructor[1].split(",").map((param) => normalizeJavaType(param.trim().replace(/\s+[A-Za-z_$][\w$]*$/, "")))
            : [])
          : (problem.signature.constructor?.params ?? [])
            .map((param) => normalizeJavaType(expectedJavaType(param.type)));
        if (!sameArray(actualParams, expectedParams)) {
          fail(problem, `${problem.signature.classname} constructor parameter types mismatch`);
        }
      }
    }
  }
  if (!demoMatch || !/\bstatic\s+void\s+main\s*\(/.test(demoMatch[1])) {
    fail(problem, "runnable demo main missing");
  }
}

console.log(`Manifest problems: ${manifest.problems.length}`);
console.log(`Source validation failures: ${failures.length}`);
if (failures.length) {
  for (const failure of failures) console.error(`- ${failure}`);
  process.exitCode = 1;
} else {
  console.log("Official source metadata and document sections are consistent.");
}
