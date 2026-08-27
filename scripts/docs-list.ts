#!/usr/bin/env tsx

import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import { basename, dirname, isAbsolute, join, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const docsListFile = fileURLToPath(import.meta.url);
const docsListDir = dirname(docsListFile);

// Resolve the docs dir so a copy shipped inside a plugin still lists the docs of
// the repo you are actually working in, not the plugin's own.
//   1. an explicit path argument (a docs/ dir, or a repo root containing one)
//   2. ./docs under the current working directory
//   3. ../docs next to this script (in-repo fallback)
function isDir(candidate: string): boolean {
  return existsSync(candidate) && statSync(candidate).isDirectory();
}

function resolveDocsDir(): string | null {
  const arg = process.argv[2];
  if (arg) {
    const target = isAbsolute(arg) ? arg : resolve(process.cwd(), arg);
    if (basename(target) === 'docs' && isDir(target)) {
      return target;
    }
    if (isDir(join(target, 'docs'))) {
      return join(target, 'docs');
    }
    if (isDir(target)) {
      return target;
    }
    return null;
  }
  const cwdDocs = join(process.cwd(), 'docs');
  if (isDir(cwdDocs)) {
    return cwdDocs;
  }
  const localDocs = join(docsListDir, '..', 'docs');
  return isDir(localDocs) ? localDocs : null;
}

const DOCS_DIR = resolveDocsDir();

const EXCLUDED_DIRS = new Set(['archive', 'research']);

function compactStrings(values: unknown[]): string[] {
  const result: string[] = [];
  for (const value of values) {
    if (value === null || value === undefined) {
      continue;
    }
    const normalized = String(value).trim();
    if (normalized.length > 0) {
      result.push(normalized);
    }
  }
  return result;
}

function walkMarkdownFiles(dir: string, base: string = dir): string[] {
  const entries = readdirSync(dir, { withFileTypes: true });
  const files: string[] = [];
  for (const entry of entries) {
    if (entry.name.startsWith('.')) {
      continue;
    }
    const fullPath = join(dir, entry.name);
    if (entry.isDirectory()) {
      if (EXCLUDED_DIRS.has(entry.name)) {
        continue;
      }
      files.push(...walkMarkdownFiles(fullPath, base));
    } else if (entry.isFile() && entry.name.endsWith('.md')) {
      files.push(relative(base, fullPath));
    }
  }
  return files.sort((a, b) => a.localeCompare(b));
}

function extractMetadata(fullPath: string): {
  summary: string | null;
  readWhen: string[];
  error?: string;
} {
  const content = readFileSync(fullPath, 'utf8');

  if (!content.startsWith('---')) {
    return { summary: null, readWhen: [], error: 'missing front matter' };
  }

  const endIndex = content.indexOf('\n---', 3);
  if (endIndex === -1) {
    return { summary: null, readWhen: [], error: 'unterminated front matter' };
  }

  const frontMatter = content.slice(3, endIndex).trim();
  const lines = frontMatter.split('\n');

  let summaryLine: string | null = null;
  const readWhen: string[] = [];
  let collectingField: 'read_when' | null = null;

  for (const rawLine of lines) {
    const line = rawLine.trim();

    if (line.startsWith('summary:')) {
      summaryLine = line;
      collectingField = null;
      continue;
    }

    if (line.startsWith('read_when:')) {
      collectingField = 'read_when';
      const inline = line.slice('read_when:'.length).trim();
      if (inline.startsWith('[') && inline.endsWith(']')) {
        try {
          const parsed = JSON.parse(inline.replace(/'/g, '"')) as unknown;
          if (Array.isArray(parsed)) {
            readWhen.push(...compactStrings(parsed));
          }
        } catch {
          // ignore malformed inline arrays
        }
      }
      continue;
    }

    if (collectingField === 'read_when') {
      if (line.startsWith('- ')) {
        const hint = line.slice(2).trim();
        if (hint) {
          readWhen.push(hint);
        }
      } else if (line === '') {
      } else {
        collectingField = null;
      }
    }
  }

  if (!summaryLine) {
    return { summary: null, readWhen, error: 'summary key missing' };
  }

  const summaryValue = summaryLine.slice('summary:'.length).trim();
  const normalized = summaryValue
    .replace(/^['"]|['"]$/g, '')
    .replace(/\s+/g, ' ')
    .trim();

  if (!normalized) {
    return { summary: null, readWhen, error: 'summary is empty' };
  }

  return { summary: normalized, readWhen };
}

if (!DOCS_DIR) {
  const arg = process.argv[2];
  console.log(
    arg
      ? `docs-list: no docs directory found at ${arg}`
      : `docs-list: no docs/ directory found in ${process.cwd()} (pass a path to point elsewhere)`
  );
  process.exit(0);
}

const displayPath = relative(process.cwd(), DOCS_DIR);
console.log(
  `Listing all markdown files in ${
    !displayPath || displayPath.startsWith('..') ? DOCS_DIR : displayPath
  }:`
);

const markdownFiles = walkMarkdownFiles(DOCS_DIR);

for (const relativePath of markdownFiles) {
  const fullPath = join(DOCS_DIR, relativePath);
  const { summary, readWhen, error } = extractMetadata(fullPath);
  if (summary) {
    console.log(`${relativePath} - ${summary}`);
    if (readWhen.length > 0) {
      console.log(`  Read when: ${readWhen.join('; ')}`);
    }
  } else {
    const reason = error ? ` - [${error}]` : '';
    console.log(`${relativePath}${reason}`);
  }
}

console.log(
  '\nReminder: keep docs up to date as behavior changes. When your task matches any "Read when" hint above (React hooks, cache directives, database work, tests, etc.), read that doc before coding, and suggest new coverage when it is missing.'
);
