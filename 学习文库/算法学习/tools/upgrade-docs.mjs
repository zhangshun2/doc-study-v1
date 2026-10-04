import { readdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDirectory = path.dirname(fileURLToPath(import.meta.url));
const libraryRoot = path.resolve(scriptDirectory, "..");
const manifestPath = path.join(libraryRoot, "problems.json");

function decodeEntities(value) {
  const named = new Map([
    ["nbsp", " "], ["amp", "&"], ["lt", "<"], ["gt", ">"],
    ["quot", "\""], ["apos", "'"], ["#39", "'"], ["hellip", "..."],
    ["times", "x"], ["minus", "-"], ["le", "<="], ["ge", ">="],
  ]);
  return value
    .replace(/&#x([0-9a-f]+);/gi, (_, hex) => String.fromCodePoint(Number.parseInt(hex, 16)))
    .replace(/&#(\d+);/g, (_, decimal) => String.fromCodePoint(Number(decimal)))
    .replace(/&([a-z]+|#39);/gi, (match, name) => named.get(name.toLowerCase()) ?? match);
}

function inlineText(html) {
  return decodeEntities(html
    .replace(/<br\s*\/?\s*>/gi, "\n")
    .replace(/<sup[^>]*>([\s\S]*?)<\/sup>/gi, "^$1")
    .replace(/<sub[^>]*>([\s\S]*?)<\/sub>/gi, "_$1")
    .replace(/<[^>]+>/g, ""))
    .replace(/\u00a0/g, " ");
}

function htmlToMarkdown(html) {
  if (!html) {
    return "";
  }
  const preBlocks = [];
  let markdown = html.replace(/<pre\b[^>]*>([\s\S]*?)<\/pre>/gi, (_, inner) => {
    const index = preBlocks.length;
    const text = inlineText(inner).replace(/^\s*\n|\n\s*$/g, "").trimEnd();
    preBlocks.push(`\`\`\`text\n${text}\n\`\`\``);
    return `\n\n@@PRE_BLOCK_${index}@@\n\n`;
  });

  markdown = markdown
    .replace(/<img\b[^>]*src=["']([^"']+)["'][^>]*>/gi, (_, source) =>
      `\n\n![Official problem illustration](${decodeEntities(source)})\n\n`)
    .replace(/<a\b[^>]*href=["']([^"']+)["'][^>]*>([\s\S]*?)<\/a>/gi,
      (_, href, label) => `[${inlineText(label).trim()}](${decodeEntities(href)})`)
    .replace(/<code\b[^>]*>([\s\S]*?)<\/code>/gi,
      (_, code) => `\`${inlineText(code).trim()}\``)
    .replace(/<strong\b[^>]*>([\s\S]*?)<\/strong>/gi,
      (_, strong) => `**${inlineText(strong).trim()}**`)
    .replace(/<em\b[^>]*>([\s\S]*?)<\/em>/gi,
      (_, emphasis) => `*${inlineText(emphasis).trim()}*`)
    .replace(/<sup\b[^>]*>([\s\S]*?)<\/sup>/gi, (_, value) => `^${inlineText(value)}`)
    .replace(/<sub\b[^>]*>([\s\S]*?)<\/sub>/gi, (_, value) => `_${inlineText(value)}`)
    .replace(/<li\b[^>]*>([\s\S]*?)<\/li>/gi, (_, item) => `\n- ${inlineText(item).trim()}\n`)
    .replace(/<br\s*\/?\s*>/gi, "\n")
    .replace(/<\/(?:p|div|ul|ol|blockquote|h[1-6])>/gi, "\n\n")
    .replace(/<(?:p|div|ul|ol|blockquote|h[1-6])\b[^>]*>/gi, "")
    .replace(/<[^>]+>/g, "");

  markdown = decodeEntities(markdown).replace(/\u00a0/g, " ");
  markdown = markdown.replace(/@@PRE_BLOCK_(\d+)@@/g,
    (_, index) => preBlocks[Number(index)]);
  return markdown
    .replace(/[ \t]+\n/g, "\n")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

function splitOfficialContent(html) {
  const markdown = htmlToMarkdown(html);
  const lines = markdown.split("\n");
  const firstExample = lines.findIndex((line) => /^\*\*\s*示例(?:\s*\d+)?[：:]\s*\*\*/.test(line.trim()));
  const constraints = lines.findIndex((line) => /^\*\*\s*(?:提示|约束)[：:]\s*\*\*/.test(line.trim()));

  const descriptionEnd = firstExample >= 0 ? firstExample : constraints >= 0 ? constraints : lines.length;
  const examplesEnd = constraints >= 0 ? constraints : lines.length;
  const description = lines.slice(0, descriptionEnd).join("\n").trim();
  const examples = firstExample >= 0
    ? lines.slice(firstExample, examplesEnd).join("\n").trim()
    : "官方题面未单独列出示例。";
  const constraintText = constraints >= 0
    ? lines.slice(constraints + 1).join("\n").trim()
    : "官方题面未单独列出约束。";
  return { description, examples, constraints: constraintText, full: markdown };
}

function section(markdown, headingPattern) {
  const lines = markdown.split(/\r?\n/);
  const start = lines.findIndex((line) => headingPattern.test(line));
  if (start < 0) {
    return null;
  }
  let end = lines.findIndex((line, index) => index > start && /^##\s+/.test(line));
  if (end < 0) {
    end = lines.length;
  }
  return { start, end, heading: lines[start], body: lines.slice(start + 1, end).join("\n").trim() };
}

function normalizeComparable(value) {
  return value.toLowerCase().replace(/[\s`'"，。：:；;\[\](){}_-]/g, "");
}

function supplementaryTests(oldProblemSection, officialMarkdown) {
  const official = normalizeComparable(officialMarkdown);
  const tests = [];
  for (const match of oldProblemSection.matchAll(/```text\s*\n([\s\S]*?)```/g)) {
    const block = match[1].trim();
    const input = block.match(/输入[：:]([\s\S]*?)(?=\n(?:输出|参数)[：:]|$)/)?.[1]?.trim();
    if (!input) {
      continue;
    }
    const signature = normalizeComparable(input);
    if (signature.length >= 2 && !official.includes(signature)) {
      tests.push(block);
    }
  }
  const unique = [...new Map(tests.map((test) => [normalizeComparable(test), test])).values()];
  if (!unique.length) {
    return [
      "- 复测全部官方示例。",
      "- 再根据下文“边界与易错点”构造最小规模、极端值、重复值或空结构输入。",
      "- 此处属于学习测试建议，不属于官方题面。",
    ].join("\n");
  }
  return [
    "> 以下用例来自原学习文档的补充示例，不属于官方题面。",
    "",
    ...unique.map((test, index) => `### 补充用例 ${index + 1}\n\n\`\`\`text\n${test}\n\`\`\``),
  ].join("\n\n");
}

function performanceNotes(oldConstraintBody) {
  const candidates = oldConstraintBody
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => line && !line.startsWith("```") &&
      /O\(|复杂度|目标|期望|超时|不应|要求|可接受|空间|时间/.test(line));
  const unique = [...new Set(candidates.map((line) => line.startsWith("-") ? line : `- ${line}`))];
  if (!unique.length) {
    unique.push("- 以本文推荐解法给出的时间复杂度和空间复杂度为实现目标。");
  }
  return [
    "> 本节是根据官方输入规模和推荐解法作出的学习推导，不属于官方题面原文。",
    "",
    ...unique,
  ].join("\n");
}

function matchingBrace(source, openBrace) {
  let depth = 0;
  let state = "code";
  for (let index = openBrace; index < source.length; index++) {
    const char = source[index];
    const next = source[index + 1];
    if (state === "lineComment") {
      if (char === "\n") state = "code";
      continue;
    }
    if (state === "blockComment") {
      if (char === "*" && next === "/") { state = "code"; index++; }
      continue;
    }
    if (state === "string") {
      if (char === "\\") index++;
      else if (char === "\"") state = "code";
      continue;
    }
    if (state === "character") {
      if (char === "\\") index++;
      else if (char === "'") state = "code";
      continue;
    }
    if (char === "/" && next === "/") { state = "lineComment"; index++; continue; }
    if (char === "/" && next === "*") { state = "blockComment"; index++; continue; }
    if (char === "\"") { state = "string"; continue; }
    if (char === "'") { state = "character"; continue; }
    if (char === "{") depth++;
    if (char === "}" && --depth === 0) return index;
  }
  throw new Error("Unbalanced Java braces");
}

function submissionCode(localCode) {
  let result = localCode.trim();
  const mainClassMatch = /\bpublic\s+class\s+Main\b/.exec(result);
  if (mainClassMatch) {
    const open = result.indexOf("{", mainClassMatch.index);
    const close = matchingBrace(result, open);
    result = `${result.slice(0, mainClassMatch.index)}${result.slice(close + 1)}`.trim();
  } else {
    const mainMethod = /\bpublic\s+static\s+void\s+main\s*\([^)]*\)\s*\{/.exec(result);
    if (!mainMethod) {
      throw new Error("Runnable Java block has no removable main entry");
    }
    const open = result.indexOf("{", mainMethod.index);
    const close = matchingBrace(result, open);
    result = `${result.slice(0, mainMethod.index)}${result.slice(close + 1)}`.trim();
  }
  for (const supportType of ["ListNode", "TreeNode"]) {
    const typeMatch = new RegExp(`^class\\s+${supportType}\\b`, "m").exec(result);
    if (typeMatch) {
      const open = result.indexOf("{", typeMatch.index);
      const close = matchingBrace(result, open);
      result = `${result.slice(0, typeMatch.index)}${result.slice(close + 1)}`.trim();
    }
  }
  result = result.replace(/\bpublic\s+class\s+Solution\b/, "class Solution");
  return result.replace(/\n{3,}/g, "\n\n");
}

function javaSection(markdown, problem) {
  const match = /## Java[^\n]*\n[\s\S]*?```java\s*\n([\s\S]*?)\n```/.exec(markdown);
  if (!match) {
    throw new Error(`${problem.id}: Java section not found`);
  }
  const localCode = match[1].trim();
  const submission = submissionCode(localCode);
  const expectedClass = problem.signature?.classname ?? "Solution";
  if (!new RegExp(`\\bclass\\s+${expectedClass}\\b`).test(submission)) {
    throw new Error(`${problem.id}: submission code is missing class ${expectedClass}`);
  }
  const replacement = [
    "## Java 实现",
    "",
    "### LeetCode 可直接提交代码",
    "",
    `> 入口类与方法已根据 ${problem.sourceCheckedAt} 的官方 Java 模板核验。本代码不包含本地 \`main\`。`,
    "",
    "```java",
    submission,
    "```",
    "",
    "### 本地可运行示例",
    "",
    "> 下面的代码包含完整数据构造和 `main`，用于本地编译、运行与观察输出。",
    "",
    "```java",
    localCode,
    "```",
  ].join("\n");
  return `${markdown.slice(0, match.index)}${replacement}${markdown.slice(match.index + match[0].length)}`;
}

function jsonValue(value) {
  return JSON.stringify(value);
}

function frontMatter(problem) {
  return [
    "---",
    "schemaVersion: 2",
    `leetcodeId: ${problem.id}`,
    `slug: ${jsonValue(problem.slug)}`,
    `titleCn: ${jsonValue(problem.titleCn)}`,
    `titleEn: ${jsonValue(problem.titleEn)}`,
    `difficulty: ${jsonValue(problem.difficulty)}`,
    `sourceUrl: ${jsonValue(problem.sourceUrl)}`,
    `sourceCheckedAt: ${jsonValue(problem.sourceCheckedAt)}`,
    `sourceContentSha256: ${jsonValue(problem.sourceContentSha256)}`,
    `primaryPattern: ${jsonValue(problem.primaryPattern)}`,
    `checklistPriorities: ${jsonValue(problem.checklistPriorities)}`,
    `checklistTags: ${jsonValue(problem.checklistTags)}`,
    "---",
  ].join("\n");
}

function officialTagText(problem) {
  return problem.officialTags
    .map((tag) => tag.translatedName ? `${tag.translatedName} (${tag.name})` : tag.name)
    .join("、");
}

function officialHints(problem) {
  if (!problem.officialHints.length) {
    return "- 当前官方接口未提供额外算法提示。";
  }
  return [
    "> 以下内容来自官方接口的额外提示字段；保留接口返回语言，不把学习提示冒充为官方提示。",
    "",
    ...problem.officialHints.map((hint, index) => `${index + 1}. ${htmlToMarkdown(hint)}`),
  ].join("\n");
}

function upgrade(markdown, problem) {
  if (/^---\s*\n[\s\S]*?schemaVersion:\s*2\b/m.test(markdown)) {
    throw new Error(`${problem.id}: document already uses schemaVersion 2`);
  }
  const problemSection = section(markdown, /^##\s+完整题目\s*$/);
  const constraintSection = section(markdown, /^##\s+约束/);
  const hintSection = section(markdown, /^##\s+题目提示\s*$/);
  if (!problemSection || !constraintSection || !hintSection) {
    throw new Error(`${problem.id}: required legacy sections are missing`);
  }

  const lines = markdown.split(/\r?\n/);
  const oldTitle = lines.find((line) => line.startsWith("# "));
  const mainModel = lines
    .slice(lines.indexOf(oldTitle) + 1, problemSection.start)
    .filter((line) => /主模型|主解法/.test(line.trim()));
  const official = splitOfficialContent(problem.translatedContentHtml);
  const oldProblemText = lines.slice(problemSection.start + 1, constraintSection.start).join("\n");
  const afterHints = lines.slice(hintSection.end).join("\n").trimStart();

  const overview = [
    `# ${problem.id}. ${problem.titleCn} / ${problem.titleEn}`,
    "",
    "## 题目信息",
    "",
    `- 官方难度：\`${problem.difficulty}\``,
    `- 主归档题型：\`${problem.primaryPattern}\``,
    `- 清单优先级：${problem.checklistPriorities.map((item) => `\`${item}\``).join("、")}`,
    `- 清单代表标签：${problem.checklistTags.map((item) => `\`${item}\``).join("、")}`,
    `- LeetCode 当前标签：${officialTagText(problem)}`,
    `- 官方来源：<${problem.sourceUrl}>`,
    `- 题面核验日期：\`${problem.sourceCheckedAt}\``,
    `- 官方内容 SHA-256：\`${problem.sourceContentSha256}\``,
    ...mainModel,
  ].join("\n");

  let upgraded = [
    frontMatter(problem),
    overview,
    "## 官方题意（LeetCode 中文题面）",
    "",
    "> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。",
    "",
    official.description,
    "",
    "## 官方示例",
    "",
    official.examples,
    "",
    "## 官方约束",
    "",
    official.constraints,
    "",
    "## 官方额外提示",
    "",
    officialHints(problem),
    "",
    "## 学习提示（非官方）",
    "",
    hintSection.body,
    "",
    "## 性能目标与约束推导",
    "",
    performanceNotes(constraintSection.body),
    "",
    "## 补充自测用例",
    "",
    supplementaryTests(oldProblemText, official.full),
    "",
    afterHints,
  ].join("\n").replace(/\n{3,}/g, "\n\n").trimEnd() + "\n";

  upgraded = javaSection(upgraded, problem);
  return upgraded.replace(/\n{3,}/g, "\n\n").trimEnd() + "\n";
}

export {
  frontMatter,
  htmlToMarkdown,
  officialHints,
  officialTagText,
  splitOfficialContent,
  submissionCode,
};

async function main() {
  const manifest = JSON.parse(await readFile(manifestPath, "utf8"));
  if (manifest.problems.length !== 60) {
    throw new Error(`Expected 60 manifest records, found ${manifest.problems.length}`);
  }

  const upgradedDocuments = [];
  for (const problem of manifest.problems) {
    const filePath = path.join(libraryRoot, ...problem.relativePath.split("/"));
    const markdown = await readFile(filePath, "utf8");
    const upgraded = upgrade(markdown, problem);
    upgradedDocuments.push({ filePath, upgraded });
  }

  for (const document of upgradedDocuments) {
    await writeFile(document.filePath, document.upgraded, "utf8");
  }

  console.log(`Upgraded ${manifest.problems.length} documents to schemaVersion 2.`);
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  await main();
}
