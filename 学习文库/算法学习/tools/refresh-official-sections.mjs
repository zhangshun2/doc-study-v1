import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  frontMatter,
  officialHints,
  officialTagText,
  splitOfficialContent,
} from "./upgrade-docs.mjs";

const scriptDirectory = path.dirname(fileURLToPath(import.meta.url));
const libraryRoot = path.resolve(scriptDirectory, "..");
const manifest = JSON.parse(await readFile(path.join(libraryRoot, "problems.json"), "utf8"));

function replaceSection(markdown, heading, body) {
  const escaped = heading.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const expression = new RegExp(`(^## ${escaped}\\s*$)[\\s\\S]*?(?=^##\\s+|(?![\\s\\S]))`, "m");
  if (!expression.test(markdown)) {
    throw new Error(`Section missing: ${heading}`);
  }
  return markdown.replace(expression, `## ${heading}\n\n${body.trim()}\n\n`);
}

function infoSection(markdown, problem) {
  const current = /^## 题目信息\s*$([\s\S]*?)(?=^##\s+)/m.exec(markdown)?.[1] ?? "";
  const mainModel = current
    .split(/\r?\n/)
    .filter((line) => /主模型|主解法/.test(line.trim()));
  return [
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
}

const updates = [];
for (const problem of manifest.problems) {
  const filePath = path.join(libraryRoot, ...problem.relativePath.split("/"));
  let markdown = await readFile(filePath, "utf8");
  if (!/^---\s*\n[\s\S]*?schemaVersion:\s*2\b/m.test(markdown)) {
    throw new Error(`${problem.id}: schemaVersion 2 front matter missing`);
  }
  const official = splitOfficialContent(problem.translatedContentHtml);
  markdown = markdown.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, `${frontMatter(problem)}\n`);
  markdown = markdown.replace(/^# .*$/m, `# ${problem.id}. ${problem.titleCn} / ${problem.titleEn}`);
  markdown = replaceSection(markdown, "题目信息", infoSection(markdown, problem));
  markdown = replaceSection(markdown, "官方题意（LeetCode 中文题面）", [
    "> 以下题意由官方中文题面快照转换为 Markdown；来源、核验日期和内容哈希见上方元信息。",
    "",
    official.description,
  ].join("\n"));
  markdown = replaceSection(markdown, "官方示例", official.examples);
  markdown = replaceSection(markdown, "官方约束", official.constraints);
  markdown = replaceSection(markdown, "官方额外提示", officialHints(problem));
  markdown = markdown.replace(
    /入口类与方法已根据 \d{4}-\d{2}-\d{2} 的官方 Java 模板核验/g,
    `入口类与方法已根据 ${problem.sourceCheckedAt} 的官方 Java 模板核验`,
  );
  updates.push({ filePath, markdown: markdown.replace(/\n{3,}/g, "\n\n").trimEnd() + "\n" });
}

for (const update of updates) {
  await writeFile(update.filePath, update.markdown, "utf8");
}
console.log(`Refreshed official sections in ${updates.length} documents.`);
