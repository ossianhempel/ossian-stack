#!/usr/bin/env node
import { readFileSync, realpathSync } from "node:fs";
import { basename } from "node:path";
import { pathToFileURL } from "node:url";

export function parseContentMachinePost(markdown) {
  const title = parseTitle(markdown);
  const platformTitle = parsePlatformTitle(markdown);
  const caption = parseCaption(markdown);
  const onVideoText = parseOnVideoText(markdown);

  if (!title) {
    throw new Error("post.md is missing a top-level title");
  }
  if (!caption) {
    throw new Error("post.md is missing a caption fenced block");
  }

  return { title, platformTitle, caption, onVideoText };
}

function parseTitle(markdown) {
  const match = markdown.match(/^#\s+(.+?)\s*$/m);
  return match?.[1]?.trim() ?? "";
}

function parsePlatformTitle(markdown) {
  const match = markdown.match(/^##\s+Platform title\s*$[\s\S]*?^```\s*$\n?([\s\S]*?)\n?^```\s*$/m);
  return match?.[1]?.trim() ?? null;
}

function parseCaption(markdown) {
  const match = markdown.match(/^##\s+Caption\s*$[\s\S]*?^```\s*$\n?([\s\S]*?)\n?^```\s*$/m);
  return match?.[1]?.trim() ?? "";
}

function parseOnVideoText(markdown) {
  const items = [];
  const textSection = markdown.match(/^##\s+On-video text\s*$([\s\S]*)/m)?.[1] ?? "";
  const blockPattern = /^###\s+(.+?)\s*$[\s\S]*?^```\s*$\n?([\s\S]*?)\n?^```\s*$/gm;

  for (const match of textSection.matchAll(blockPattern)) {
    const label = match[1]?.trim();
    const text = match[2]?.trim();
    if (label && text) items.push({ label, text });
  }

  return items;
}

function main(argv) {
  const postPath = argv[2];
  if (!postPath) {
    throw new Error(`Usage: ${basename(argv[1] ?? "parse-content-factory-post.mjs")} <post.md>`);
  }

  const parsed = parseContentMachinePost(readFileSync(postPath, "utf8"));
  process.stdout.write(`${JSON.stringify(parsed, null, 2)}\n`);
}

// Compare realpaths: this script may be reached through a symlinked skills dir
// rather than its real location. Node resolves import.meta.url to the real path
// while argv[1] keeps the symlink path, so a naive string compare makes the CLI
// a silent no-op that still exits 0.
function isEntrypoint() {
  const entry = process.argv[1];
  if (!entry) return false;
  try {
    return import.meta.url === pathToFileURL(realpathSync(entry)).href;
  } catch {
    return false;
  }
}

if (isEntrypoint()) {
  try {
    main(process.argv);
  } catch (error) {
    process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`);
    process.exit(1);
  }
}
