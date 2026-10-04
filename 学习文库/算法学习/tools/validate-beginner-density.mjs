import { readdir, readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDirectory = path.dirname(fileURLToPath(import.meta.url));
const libraryRoot = path.resolve(scriptDirectory, "..");
const defaultDocsDirectory = path.join(libraryRoot, "建模专题", "T0");
const defaultLedgerPath = path.join(libraryRoot, "建模专题", "小白逐句审稿台账.md");
const allExpectedIds = [
  1, 3, 11, 15, 20, 33, 46, 53, 55, 56, 70, 102, 200, 206, 207, 215, 236, 239, 322, 560, 739,
];
const qaLabels = ["小白追问", "先给短答", "最小例子", "回到模型/代码"];
const coreReasoningSections = [8, 9, 10, 14, 15, 16];
const riskPattern = /只需|可以删除|安全删除|不会遗漏|一定|必然|最优|均摊|不变量|剪枝|支配|因此|所以|显然|当然|不难看出/;
const decoder = new TextDecoder("utf-8", { fatal: true });

function readOption(name, fallback) {
  const index = process.argv.indexOf(name);
  return index >= 0 && process.argv[index + 1] ? process.argv[index + 1] : fallback;
}

function parseRequestedIds() {
  const value = readOption("--ids", "");
  if (!value) return allExpectedIds;
  const ids = value.split(",").map((part) => Number(part.trim())).filter(Number.isInteger);
  if (!ids.length) throw new Error("--ids must contain at least one numeric problem id");
  return ids;
}

function countCjk(value) {
  return (value.match(/[\p{Script=Han}]/gu) ?? []).length;
}

function extractId(filename) {
  const match = /^(\d+)-/.exec(filename);
  return match ? Number(match[1]) : null;
}

function sectionNumber(heading) {
  const match = /^(\d+)\./.exec(heading);
  return match ? Number(match[1]) : null;
}

function inspectQaBlocks(lines, filename, failures) {
  const blocks = [];
  let currentSection = null;

  for (let index = 0; index < lines.length; index++) {
    const headingMatch = /^##\s+(.+)$/.exec(lines[index]);
    if (headingMatch) currentSection = sectionNumber(headingMatch[1]);
    if (!lines[index].startsWith("> **小白追问：**")) continue;

    let end = index + 1;
    while (end < lines.length
      && !lines[end].startsWith("> **小白追问：**")
      && !/^##\s+/.test(lines[end])) {
      end++;
    }
    const blockLines = lines.slice(index, end);
    const positions = qaLabels.map((label) => blockLines.findIndex((line) => {
      const prefix = `> **${label}：**`;
      return line.startsWith(prefix) && line.slice(prefix.length).trim().length > 0;
    }));

    if (positions.some((position) => position < 0)
      || positions.some((position, labelIndex) => labelIndex > 0 && position <= positions[labelIndex - 1])) {
      failures.push(`${filename}:${index + 1}: malformed beginner Q&A block`);
    }
    blocks.push({ line: index + 1, section: currentSection });
  }
  return blocks;
}

function proseParagraphs(lines) {
  const paragraphs = [];
  let paragraph = [];
  let inFence = false;

  function flush() {
    if (paragraph.length) paragraphs.push(paragraph.join(" "));
    paragraph = [];
  }

  for (const line of lines) {
    if (/^```/.test(line.trim())) {
      inFence = !inFence;
      flush();
      continue;
    }
    if (inFence || /^\s*$/.test(line)) {
      flush();
      continue;
    }
    if (/^(#{1,6}\s|\||>\s|[-*]\s|\d+\.\s)/.test(line.trim())) {
      flush();
      continue;
    }
    paragraph.push(line.trim());
  }
  flush();
  return paragraphs;
}

function inspectDensity(lines, headings, qaBlocks) {
  const warnings = [];
  const paragraphs = proseParagraphs(lines);
  let longSentences = 0;
  let longParagraphs = 0;

  for (const paragraph of paragraphs) {
    const normalized = paragraph
      .replace(/`[^`]*`/g, "X")
      .replace(/\[[^\]]+\]\([^)]+\)/g, "LINK")
      .replace(/https?:\/\/\S+/g, "URL");
    if (countCjk(normalized) > 260) longParagraphs++;
    for (const sentence of normalized.split(/[。！？；]/)) {
      if (countCjk(sentence) > 80) longSentences++;
    }
  }

  const sectionRanges = headings.map((heading, index) => ({
    number: sectionNumber(heading.title),
    start: heading.line,
    end: index + 1 < headings.length ? headings[index + 1].line : lines.length,
  }));
  const missingCoreQa = [];
  for (const section of sectionRanges) {
    if (!coreReasoningSections.includes(section.number)) continue;
    const sectionText = lines.slice(section.start, section.end).join("\n");
    const hasRiskClaim = riskPattern.test(sectionText);
    const hasQa = qaBlocks.some((block) => block.section === section.number);
    if (hasRiskClaim && !hasQa) missingCoreQa.push(section.number);
  }

  if (longSentences) warnings.push(`${longSentences} sentence(s) exceed 80 Chinese characters`);
  if (longParagraphs) warnings.push(`${longParagraphs} paragraph(s) exceed 260 Chinese characters`);
  if (missingCoreQa.length) warnings.push(`core section(s) with risk claims but no Q&A: ${missingCoreQa.join(",")}`);
  return { warnings, longSentences, longParagraphs, missingCoreQa };
}

const docsDirectory = path.resolve(readOption("--docs", defaultDocsDirectory));
const ledgerPath = path.resolve(readOption("--ledger", defaultLedgerPath));
const requestedIds = parseRequestedIds();
const requireComplete = process.argv.includes("--require-complete");
const failures = [];
const warningLines = [];
const metrics = [];

const entries = await readdir(docsDirectory, { withFileTypes: true });
const markdownFiles = entries
  .filter((entry) => entry.isFile() && entry.name.endsWith(".md"))
  .map((entry) => entry.name)
  .filter((name) => requestedIds.includes(extractId(name)))
  .sort((left, right) => extractId(left) - extractId(right));

for (const id of requestedIds) {
  const matches = markdownFiles.filter((name) => extractId(name) === id);
  if (matches.length !== 1) failures.push(`problem ${id}: expected one document, found ${matches.length}`);
}

for (const filename of markdownFiles) {
  const fullPath = path.join(docsDirectory, filename);
  const bytes = await readFile(fullPath);
  if (bytes.length >= 3 && bytes[0] === 0xef && bytes[1] === 0xbb && bytes[2] === 0xbf) {
    failures.push(`${filename}: UTF-8 BOM detected`);
    continue;
  }

  let content;
  try {
    content = decoder.decode(bytes);
  } catch (error) {
    failures.push(`${filename}: invalid UTF-8 (${error.message})`);
    continue;
  }

  const lines = content.split(/\r?\n/);
  const headings = [];
  for (let index = 0; index < lines.length; index++) {
    const match = /^##\s+(.+)$/.exec(lines[index]);
    if (match) headings.push({ title: match[1], line: index });
  }
  const headingNumbers = headings.map((heading) => sectionNumber(heading.title));
  if (headings.length !== 19 || headingNumbers.join(",") !== Array.from({ length: 19 }, (_, index) => index + 1).join(",")) {
    failures.push(`${filename}: expected ordered sections 1..19, found ${headingNumbers.join(",")}`);
  }
  if ((content.match(/^### LeetCode 可直接提交代码\s*$/gm) ?? []).length !== 1) {
    failures.push(`${filename}: expected exactly one LeetCode submission heading`);
  }
  if ((content.match(/^### 本地可运行示例\s*$/gm) ?? []).length !== 1) {
    failures.push(`${filename}: expected exactly one runnable example heading`);
  }
  if (/(?:TODO|TBD|待填写|待补充|省略实现)/i.test(content)) {
    failures.push(`${filename}: placeholder text detected`);
  }

  const qaBlocks = inspectQaBlocks(lines, filename, failures);
  if (!qaBlocks.length) failures.push(`${filename}: no structured beginner Q&A block found`);
  const density = inspectDensity(lines, headings, qaBlocks);
  for (const warning of density.warnings) warningLines.push(`${filename}: ${warning}`);

  const chineseCharacters = countCjk(content);
  if (chineseCharacters < 12000 || chineseCharacters > 18000) {
    warningLines.push(`${filename}: ${chineseCharacters} Chinese characters, target is 12000..18000`);
  }
  metrics.push({
    id: extractId(filename),
    filename,
    chineseCharacters,
    qaBlocks: qaBlocks.length,
    longSentences: density.longSentences,
    longParagraphs: density.longParagraphs,
    missingCoreQa: density.missingCoreQa.join(",") || "-",
  });
}

const ledger = await readFile(ledgerPath, "utf8");
for (const id of requestedIds) {
  const row = ledger.split(/\r?\n/).find((line) => new RegExp(`^\\|\\s*${id}\\s*\\|`).test(line));
  if (!row) {
    failures.push(`ledger: problem ${id} row missing`);
  } else if (requireComplete && !/\|\s*已完成\s*\|\s*$/.test(row)) {
    failures.push(`ledger: problem ${id} is not marked complete`);
  }
}

console.table(metrics);
console.log(`Documents checked: ${metrics.length}`);
console.log(`Structured Q&A blocks: ${metrics.reduce((sum, item) => sum + item.qaBlocks, 0)}`);
console.log(`Density warnings: ${warningLines.length}`);
for (const warning of warningLines) console.warn(`- ${warning}`);
console.log(`Failures: ${failures.length}`);
for (const failure of failures) console.error(`- ${failure}`);
if (failures.length) process.exitCode = 1;
