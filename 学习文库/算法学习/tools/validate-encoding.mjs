import { readdir, readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDirectory = path.dirname(fileURLToPath(import.meta.url));
const libraryRoot = path.resolve(scriptDirectory, "..");
const textExtensions = new Set([".md", ".json", ".mjs", ".ps1"]);
const decoder = new TextDecoder("utf-8", { fatal: true });
const failures = [];
let checked = 0;

async function walk(directory) {
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const fullPath = path.join(directory, entry.name);
    if (entry.isSymbolicLink()) continue;
    if (entry.isDirectory()) {
      await walk(fullPath);
      continue;
    }
    if (!entry.isFile() || !textExtensions.has(path.extname(entry.name).toLowerCase())) continue;
    const bytes = await readFile(fullPath);
    checked++;
    if (bytes.length >= 3 && bytes[0] === 0xef && bytes[1] === 0xbb && bytes[2] === 0xbf) {
      failures.push(`${fullPath}: UTF-8 BOM detected`);
      continue;
    }
    try {
      decoder.decode(bytes);
    } catch (error) {
      failures.push(`${fullPath}: invalid UTF-8 (${error.message})`);
    }
  }
}

await walk(libraryRoot);
console.log(`UTF-8 text files checked: ${checked}`);
console.log(`Encoding failures: ${failures.length}`);
if (failures.length) {
  for (const failure of failures) console.error(`- ${failure}`);
  process.exitCode = 1;
} else {
  console.log("All checked files are valid UTF-8 without BOM.");
}
