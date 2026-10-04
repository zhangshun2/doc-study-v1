import { createHash } from "node:crypto";
import { readdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDirectory = path.dirname(fileURLToPath(import.meta.url));
const libraryRoot = path.resolve(scriptDirectory, "..");
const docsRoot = path.join(libraryRoot, "题目");
const checklistPath = "C:/d/a_project/tan_suo/leetcode-hot100-tags-checklist.md";
const outputPath = path.join(libraryRoot, "problems.json");
const endpoint = "https://leetcode.cn/graphql/";

const query = `
query questionData($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionFrontendId
    title
    titleSlug
    translatedTitle
    translatedContent
    difficulty
    topicTags { name translatedName slug }
    codeSnippets { lang langSlug code }
    hints
    exampleTestcases
    metaData
  }
}`;

async function walkMarkdown(directory) {
  const result = [];
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const fullPath = path.join(directory, entry.name);
    if (entry.isDirectory()) {
      result.push(...await walkMarkdown(fullPath));
    } else if (entry.isFile() && entry.name.endsWith(".md")) {
      result.push(fullPath);
    }
  }
  return result;
}

function parseChecklist(markdown) {
  const byId = new Map();
  let priority = null;
  for (const line of markdown.split(/\r?\n/)) {
    const priorityMatch = line.match(/^###\s+(P[012])\b/);
    if (priorityMatch) {
      priority = priorityMatch[1];
      continue;
    }
    const row = line.match(/^\|\s*(.+?)\s*\|\s*(\d+(?:、\d+)*)\s*\|\s*\[\s*\]\s*\|$/);
    if (!row || !priority) {
      continue;
    }
    const tag = row[1].trim();
    for (const idText of row[2].split("、")) {
      const id = Number(idText);
      if (!byId.has(id)) {
        byId.set(id, { priorities: new Set(), tags: new Set() });
      }
      byId.get(id).priorities.add(priority);
      byId.get(id).tags.add(tag);
    }
  }
  return byId;
}

function decodeEntities(value) {
  const named = new Map([
    ["nbsp", " "], ["amp", "&"], ["lt", "<"], ["gt", ">"],
    ["quot", "\""], ["apos", "'"], ["#39", "'"], ["hellip", "..."],
  ]);
  return value
    .replace(/&#x([0-9a-f]+);/gi, (_, hex) => String.fromCodePoint(Number.parseInt(hex, 16)))
    .replace(/&#(\d+);/g, (_, decimal) => String.fromCodePoint(Number(decimal)))
    .replace(/&([a-z]+|#39);/gi, (match, name) => named.get(name.toLowerCase()) ?? match);
}

function htmlToPlainText(html) {
  return decodeEntities(html
    .replace(/<br\s*\/?\s*>/gi, "\n")
    .replace(/<\/p>/gi, "\n")
    .replace(/<[^>]+>/g, ""))
    .replace(/\u00a0/g, " ")
    .replace(/[ \t]+\n/g, "\n")
    .trim();
}

function extractOfficialExamples(html) {
  const examples = [];
  const fragments = [
    ...[...html.matchAll(/<pre\b[^>]*>([\s\S]*?)<\/pre>/gi)].map((match) => match[1]),
    ...[...html.matchAll(/<div\b[^>]*class=["'][^"']*example-block[^"']*["'][^>]*>([\s\S]*?)<\/div>/gi)]
      .map((match) => match[1]),
  ];
  for (const fragment of fragments) {
    const text = htmlToPlainText(fragment);
    const parts = text.match(/输入[：:]?\s*([\s\S]*?)\n输出[：:]?\s*([\s\S]*?)(?:\n解释[：:]?\s*([\s\S]*))?$/);
    if (!parts) continue;
    examples.push({
      input: parts[1].trim(),
      output: parts[2].trim(),
      explanation: parts[3]?.trim() || null,
    });
  }
  return examples;
}

async function discoverDocuments() {
  const documents = [];
  for (const filePath of await walkMarkdown(docsRoot)) {
    const markdown = await readFile(filePath, "utf8");
    const idMatch = path.basename(filePath).match(/^(\d+)-/);
    const slugMatch = markdown.match(/https:\/\/leetcode\.cn\/problems\/([a-z0-9-]+)\/?/i);
    if (!idMatch || !slugMatch) {
      throw new Error(`Cannot discover id or slug from ${filePath}`);
    }
    documents.push({
      id: Number(idMatch[1]),
      slug: slugMatch[1].toLowerCase(),
      relativePath: path.relative(libraryRoot, filePath).replaceAll(path.sep, "/"),
      primaryPattern: path.basename(path.dirname(filePath)),
    });
  }
  documents.sort((a, b) => a.id - b.id);
  return documents;
}

async function fetchQuestion(document, attempt = 1) {
  try {
    const response = await fetch(endpoint, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "referer": `https://leetcode.cn/problems/${document.slug}/`,
        "user-agent": "Codex algorithm-library-sync/1.0",
      },
      body: JSON.stringify({
        operationName: "questionData",
        variables: { titleSlug: document.slug },
        query,
      }),
      signal: AbortSignal.timeout(30000),
    });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const payload = await response.json();
    if (payload.errors?.length || !payload.data?.question) {
      throw new Error(JSON.stringify(payload.errors ?? "question missing"));
    }
    const question = payload.data.question;
    if (Number(question.questionFrontendId) !== document.id) {
      throw new Error(`Expected id ${document.id}, received ${question.questionFrontendId}`);
    }
    return question;
  } catch (error) {
    if (attempt >= 4) {
      throw new Error(`${document.id}-${document.slug}: ${error.message}`);
    }
    await new Promise((resolve) => setTimeout(resolve, 500 * 2 ** (attempt - 1)));
    return fetchQuestion(document, attempt + 1);
  }
}

async function mapWithConcurrency(items, concurrency, mapper) {
  const output = new Array(items.length);
  let nextIndex = 0;
  async function worker() {
    while (true) {
      const index = nextIndex++;
      if (index >= items.length) {
        return;
      }
      output[index] = await mapper(items[index], index);
    }
  }
  await Promise.all(Array.from({ length: concurrency }, worker));
  return output;
}

function checkedDate() {
  return new Intl.DateTimeFormat("en-CA", {
    timeZone: "Asia/Shanghai",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).format(new Date());
}

const checklist = parseChecklist(await readFile(checklistPath, "utf8"));
const documents = await discoverDocuments();
if (documents.length !== 60) {
  throw new Error(`Expected 60 documents, found ${documents.length}`);
}

const duplicateIds = documents.filter((item, index) =>
  documents.findIndex((candidate) => candidate.id === item.id) !== index);
if (duplicateIds.length) {
  throw new Error(`Duplicate ids: ${duplicateIds.map((item) => item.id).join(", ")}`);
}

const questions = await mapWithConcurrency(documents, 4, async (document) => {
  const question = await fetchQuestion(document);
  const checklistEntry = checklist.get(document.id);
  if (!checklistEntry) {
    throw new Error(`Problem ${document.id} is missing from the checklist`);
  }
  let signature;
  try {
    signature = JSON.parse(question.metaData);
  } catch {
    signature = question.metaData;
  }
  return {
    id: document.id,
    slug: question.titleSlug,
    titleCn: question.translatedTitle,
    titleEn: question.title,
    difficulty: question.difficulty,
    sourceUrl: `https://leetcode.cn/problems/${question.titleSlug}/`,
    sourceCheckedAt: checkedDate(),
    sourceContentSha256: createHash("sha256")
      .update(question.translatedContent ?? "", "utf8")
      .digest("hex"),
    relativePath: document.relativePath,
    primaryPattern: document.primaryPattern,
    checklistPriorities: [...checklistEntry.priorities].sort(),
    checklistTags: [...checklistEntry.tags],
    officialTags: question.topicTags ?? [],
    signature,
    javaTemplate: (question.codeSnippets ?? [])
      .find((snippet) => snippet.langSlug === "java")?.code ?? null,
    officialHints: question.hints ?? [],
    exampleTestcases: question.exampleTestcases ?? "",
    officialExamples: extractOfficialExamples(question.translatedContent ?? ""),
    translatedContentHtml: question.translatedContent ?? "",
  };
});

const manifest = {
  schemaVersion: 1,
  generatedAt: new Date().toISOString(),
  source: {
    endpoint,
    checklistPath,
    sourceCheckedAt: checkedDate(),
    problemCount: questions.length,
  },
  problems: questions,
};

await writeFile(outputPath, `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
console.log(`Wrote ${questions.length} official records to ${outputPath}`);
