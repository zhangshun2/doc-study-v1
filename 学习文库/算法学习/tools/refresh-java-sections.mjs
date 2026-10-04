import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { submissionCode } from "./upgrade-docs.mjs";

const scriptDirectory = path.dirname(fileURLToPath(import.meta.url));
const libraryRoot = path.resolve(scriptDirectory, "..");
const manifest = JSON.parse(await readFile(path.join(libraryRoot, "problems.json"), "utf8"));
const updates = [];

for (const problem of manifest.problems) {
  const filePath = path.join(libraryRoot, ...problem.relativePath.split("/"));
  const markdown = await readFile(filePath, "utf8");
  const demoMatch = /### 本地可运行示例[\s\S]*?```java\s*\n([\s\S]*?)\n```/.exec(markdown);
  const submissionMatch = /(### LeetCode 可直接提交代码[\s\S]*?```java\s*\n)([\s\S]*?)(\n```)/.exec(markdown);
  if (!demoMatch || !submissionMatch) {
    throw new Error(`${problem.id}: Java sections are missing`);
  }
  const submission = submissionCode(demoMatch[1]);
  const expectedClass = problem.signature?.classname ?? "Solution";
  if (!new RegExp(`\\bclass\\s+${expectedClass}\\b`).test(submission)) {
    throw new Error(`${problem.id}: submission class ${expectedClass} is missing`);
  }
  const upgraded = `${markdown.slice(0, submissionMatch.index)}`
    + `${submissionMatch[1]}${submission}${submissionMatch[3]}`
    + `${markdown.slice(submissionMatch.index + submissionMatch[0].length)}`;
  updates.push({ filePath, upgraded });
}

for (const update of updates) {
  await writeFile(update.filePath, update.upgraded, "utf8");
}

console.log(`Refreshed ${updates.length} submission Java blocks.`);
