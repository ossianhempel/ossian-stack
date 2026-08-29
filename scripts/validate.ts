#!/usr/bin/env bun
/**
 * Repo-local consistency checks for the ossian-stack plugin.
 *
 * Run: bun run validate
 *
 * Checks (all deterministic, no network):
 *   1. The three manifests parse, agree on name, and agree on version.
 *   2. Every skills/<name>/ has a SKILL.md with name + description frontmatter,
 *      and the frontmatter name matches the directory name. Invocation policy
 *      agrees across runtimes: disable-model-invocation (Claude Code, Cursor)
 *      and agents/openai.yaml policy.allow_implicit_invocation (Codex).
 *   3. skills/sources.json covers every skill exactly once, with no orphans;
 *      vendored/adapted entries carry repo + upstreamRev.
 *   4. No shipped skill references a path outside its own directory.
 *   5. README lists every skill name exactly once and its counts are current.
 *   6. Internal skills under .agents/skills/ are well-formed, do not collide with
 *      shipped names, and .claude/skills still symlinks to them.
 *   7. CLAUDE.md is still a symlink to AGENTS.md.
 */
import { readFileSync, readdirSync, statSync, lstatSync, readlinkSync, existsSync } from "node:fs";
import { join } from "node:path";

const ROOT = new URL("..", import.meta.url).pathname.replace(/\/$/, "");
const errors: string[] = [];
const warnings: string[] = [];

const fail = (msg: string) => errors.push(msg);
const warn = (msg: string) => warnings.push(msg);
const read = (p: string) => readFileSync(join(ROOT, p), "utf8");
const readJson = (p: string) => {
  try {
    return JSON.parse(read(p));
  } catch (e) {
    fail(`${p}: ${(e as Error).message}`);
    return null;
  }
};

// ---------------------------------------------------------------- 1. manifests
const claudePlugin = readJson(".claude-plugin/plugin.json");
const marketplace = readJson(".claude-plugin/marketplace.json");
const codexPlugin = readJson(".codex-plugin/plugin.json");

const marketplaceEntry = marketplace?.plugins?.find((p: any) => p.name === "ossian-stack");
if (marketplace && !marketplaceEntry) fail(".claude-plugin/marketplace.json: no plugin entry named ossian-stack");

const versions: Record<string, string | undefined> = {
  ".claude-plugin/plugin.json": claudePlugin?.version,
  ".claude-plugin/marketplace.json": marketplaceEntry?.version,
  ".codex-plugin/plugin.json": codexPlugin?.version,
};
const distinct = new Set(Object.values(versions).filter(Boolean));
if (distinct.size > 1) {
  fail(
    `manifest versions disagree — bump all three together:\n` +
      Object.entries(versions)
        .map(([f, v]) => `        ${v ?? "(missing)"}  ${f}`)
        .join("\n"),
  );
}
const VERSION = claudePlugin?.version ?? "0.0.0";

for (const [file, name] of [
  [".claude-plugin/plugin.json", claudePlugin?.name],
  [".claude-plugin/marketplace.json", marketplaceEntry?.name],
  [".codex-plugin/plugin.json", codexPlugin?.name],
] as const) {
  if (name !== "ossian-stack") fail(`${file}: name is ${name ?? "(missing)"}, expected ossian-stack`);
}

// ------------------------------------------------------------------ 2. skills
// Backticked kebab tokens that are deliberately not skill names.
const KNOWN_NON_SKILL_REFS = new Set([
  "allow-implicit-invocation", "disable-model-invocation", "merge-queue",
  "read-only", "user-invoke-only", "red-capable", "well-known",
]);
const skillDirs = readdirSync(join(ROOT, "skills"))
  .filter((n) => !n.startsWith(".") && statSync(join(ROOT, "skills", n)).isDirectory())
  .sort();

if (skillDirs.length === 0) fail("skills/: no skill directories found");

const frontmatter = (body: string): Record<string, string> | null => {
  const m = body.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!m) return null;
  const out: Record<string, string> = {};
  let key = "";
  for (const line of m[1].split(/\r?\n/)) {
    const kv = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (kv) {
      key = kv[1];
      out[key] = kv[2].trim().replace(/^["']|["']$/g, "");
    } else if (key && /^\s+\S/.test(line)) {
      out[key] = `${out[key]} ${line.trim()}`.trim();
    }
  }
  return out;
};

for (const dir of skillDirs) {
  const skillMd = join("skills", dir, "SKILL.md");
  if (!existsSync(join(ROOT, skillMd))) {
    fail(`${skillMd}: missing`);
    continue;
  }
  const fm = frontmatter(read(skillMd));
  if (!fm) {
    fail(`${skillMd}: no YAML frontmatter`);
    continue;
  }
  if (!fm.name) fail(`${skillMd}: frontmatter has no name`);
  else if (fm.name !== dir) fail(`${skillMd}: frontmatter name "${fm.name}" != directory "${dir}"`);
  if (!fm.description) fail(`${skillMd}: frontmatter has no description`);
  else if (fm.description.length > 1024) fail(`${skillMd}: description is ${fm.description.length} chars (max 1024)`);
  if (!/^[a-z0-9]+(-[a-z0-9]+)*$/.test(dir)) fail(`skills/${dir}: not kebab-case`);

  // Invocation policy must agree across runtimes. Claude Code and Cursor read
  // `disable-model-invocation` in SKILL.md; Codex ignores that field entirely and
  // reads `policy.allow_implicit_invocation` from agents/openai.yaml. Declaring
  // one without the other means the skill silently auto-invokes on the runtime
  // that was never told.
  const yamlPath = join("skills", dir, "agents", "openai.yaml");
  const noAuto = fm["disable-model-invocation"] === "true";
  // undefined = no declaration, which is Codex's default of "implicit allowed"
  let implicit: unknown;

  if (existsSync(join(ROOT, yamlPath))) {
    let doc: any;
    let parsed = true;
    try {
      doc = Bun.YAML.parse(read(yamlPath));
    } catch (err) {
      fail(`${yamlPath}: not valid YAML — ${(err as Error).message}`);
      parsed = false;
    }
    if (parsed) {
      if (doc === null || typeof doc !== "object" || Array.isArray(doc)) {
        fail(`${yamlPath}: top level must be a mapping`);
      } else {
        const iface = doc.interface;
        if (iface === undefined) fail(`${yamlPath}: no interface block`);
        else if (typeof iface !== "object" || iface === null || Array.isArray(iface))
          fail(`${yamlPath}: interface must be a mapping`);
        else {
          if (!iface.display_name) fail(`${yamlPath}: interface.display_name is missing`);
          if (!iface.short_description) fail(`${yamlPath}: interface.short_description is missing`);
        }
        implicit = doc.policy?.allow_implicit_invocation;
        if (implicit !== undefined && typeof implicit !== "boolean") {
          fail(`${yamlPath}: policy.allow_implicit_invocation must be true or false, got ${JSON.stringify(implicit)}`);
          implicit = undefined; // don't let a bad value drive the parity verdict below
        }
      }
    }
  }

  if (noAuto && implicit === true)
    fail(`${yamlPath}: policy.allow_implicit_invocation is true but ${skillMd} sets disable-model-invocation: true — the two runtimes are told opposite things`);
  else if (noAuto && implicit === undefined)
    fail(`${skillMd}: disable-model-invocation is set but ${yamlPath} does not set policy.allow_implicit_invocation: false — Codex will auto-invoke it`);
  if (implicit === false && !noAuto)
    fail(`${yamlPath}: policy.allow_implicit_invocation is false but ${skillMd} has no disable-model-invocation: true — Claude Code will auto-invoke it`);
}

// -------------------------------------------------------------- 3. sources.json
const sources = readJson("skills/sources.json");
const entries: Record<string, any> = sources?.skills ?? {};
for (const dir of skillDirs) {
  if (!entries[dir]) fail(`skills/sources.json: no entry for skills/${dir}/ (every skill needs one)`);
}
for (const name of Object.keys(entries)) {
  if (!skillDirs.includes(name)) fail(`skills/sources.json: entry "${name}" has no skills/${name}/ directory`);
}
const ORIGINS = new Set(["local", "vendored", "adapted", "companion", "derived"]);
for (const [name, entry] of Object.entries(entries)) {
  if (!ORIGINS.has(entry.origin)) fail(`skills/sources.json: ${name} has unknown origin "${entry.origin}"`);
  if (entry.origin === "vendored" || entry.origin === "adapted") {
    if (!entry.repo) fail(`skills/sources.json: ${name} is ${entry.origin} but has no repo`);
    if (!entry.upstreamRev) {
      warn(`skills/sources.json: ${name} has no upstreamRev — run scripts/check-upstream.sh --record ${name}`);
    }
  }
}

// ------------------------------------------------- 4. self-contained skill refs
const OUTSIDE = [
  { re: /\.\.\/\.\.\/skills\//g, why: "traversal into a sibling skill" },
  { re: /\$\{CLAUDE_PLUGIN_ROOT\}\/skills\//g, why: "absolute reference to another skill" },
  // Prose may name the cache path (skill-cleaner audits it); loading a *file* from it is the bug.
  { re: /~\/\.claude\/plugins\/cache\/\S+\.[a-z]{2,4}\b/g, why: "loads a file from the install cache" },
  { re: /\/Users\/[a-z]+\/(Developer|repos)\/ossian-stack\/\S+\.[a-z]{2,4}\b/g, why: "absolute path into this checkout" },
];
const walk = (dir: string): string[] =>
  readdirSync(join(ROOT, dir), { withFileTypes: true }).flatMap((d) =>
    d.isDirectory() ? walk(join(dir, d.name)) : [join(dir, d.name)],
  );

for (const dir of skillDirs) {
  for (const file of walk(join("skills", dir))) {
    if (!/\.(md|ts|js|sh|py|json|ya?ml)$/.test(file)) continue;
    const body = read(file);
    for (const { re, why } of OUTSIDE) {
      if (re.test(body)) fail(`${file}: ${why} — skills must be self-contained`);
      re.lastIndex = 0;
    }
  }
}

// ------------------------------------------------- 4b. project-convention names
// This plugin's term for a project's shared-vocabulary document is GLOSSARY.md.
// Vendored skills arrive using other conventions (mattpocock reads CONTEXT.md,
// Every's compound reads CONCEPTS.md); a skill that tells a user to write the
// wrong filename splits the convention across their repos. Checked in what an
// agent actually reads -- SKILL.md and references -- not in per-skill READMEs.
const BANNED_DOC_NAMES = ["CONTEXT.md", "CONCEPTS.md", "VOCABULARY.md"];
for (const dir of skillDirs) {
  for (const file of walk(join("skills", dir))) {
    if (!/\.(md|ya?ml|txt)$/i.test(file)) continue;
    // A skill's own README is maintainer documentation, not something an agent
    // loads. Vendoring notes must be able to name the convention they converted.
    if (file.endsWith("/README.md")) continue;
    const body = read(file);
    for (const banned of BANNED_DOC_NAMES) {
      if (new RegExp(`\\b${banned.replace(".", "\\.")}\\b`).test(body))
        fail(`${file}: references ${banned} — this plugin uses GLOSSARY.md for a project's shared vocabulary`);
    }
  }
}

// ------------------------------------------------- 4c. cross-skill references
// A skill that names a sibling we do not ship routes the reader to a dead end.
// Only four shapes are unambiguous; anything looser matches CSS properties, model
// ids, API routes, and filesystem paths, and a check that cries wolf gets ignored.
// A bare `/name` is NOT enough — that matches /tmp, /docs, and other tools' slash
// commands. Recognised: "`name` skill", "the skill `name`", "`/name` skill",
// "`principle-*`". Warn, not fail: pruning a skill leaves inbound references
// behind in siblings, and that debt should surface without blocking a commit.
const SKILL_REF_PATTERNS = [
  /`([a-z][a-z0-9-]*)` skill\b/g,
  /\bskill `([a-z][a-z0-9-]*)`/g,
  /`\/([a-z][a-z0-9-]*)` skill\b/g,
  /`(principle-[a-z0-9-]+)`/g,
];
for (const dir of skillDirs) {
  const body = read(join("skills", dir, "SKILL.md"));
  const seen = new Set<string>();
  for (const re of SKILL_REF_PATTERNS) {
    for (const m of body.matchAll(re)) {
      const ref = m[1];
      if (ref === dir || seen.has(ref)) continue;
      seen.add(ref);
      if (!skillDirs.includes(ref))
        warn(`skills/${dir}/SKILL.md: refers to the \`${ref}\` skill, but no skills/${ref}/ exists`);
    }
  }
}

// ------------------------------------------------------------------ 5. README
const readme = read("README.md");
for (const dir of skillDirs) {
  const hits = readme.split(new RegExp(`\`${dir}\``, "g")).length - 1;
  if (hits === 0) fail(`README.md: skill "${dir}" is not listed`);
  else if (hits > 1) fail(`README.md: skill "${dir}" is listed ${hits} times`);
}
const claimed = readme.match(/(\d+)\s+skills/g) ?? [];
for (const claim of claimed) {
  const n = Number(claim.match(/\d+/)![0]);
  if (n !== skillDirs.length) fail(`README.md: says "${claim}" but skills/ has ${skillDirs.length}`);
}
if (!readme.includes(`skills-${skillDirs.length}-`)) {
  warn(`README.md: skills badge does not show ${skillDirs.length}`);
}

// ------------------------------------------------------- 6. internal skill tier
const INTERNAL_ROOT = ".agents/skills";
const internalDirs = existsSync(join(ROOT, INTERNAL_ROOT))
  ? readdirSync(join(ROOT, INTERNAL_ROOT))
      .filter((n) => !n.startsWith(".") && statSync(join(ROOT, INTERNAL_ROOT, n)).isDirectory())
      .sort()
  : [];

for (const dir of internalDirs) {
  const skillMd = join(INTERNAL_ROOT, dir, "SKILL.md");
  if (!existsSync(join(ROOT, skillMd))) {
    // A leftover `npx skills add` download, not a skill of ours.
    warn(`${INTERNAL_ROOT}/${dir}/: no SKILL.md — vendoring scratch? trash it`);
    continue;
  }
  const fm = frontmatter(read(skillMd));
  if (!fm?.name) fail(`${skillMd}: frontmatter has no name`);
  else if (fm.name !== dir) fail(`${skillMd}: frontmatter name "${fm.name}" != directory "${dir}"`);
  if (!fm?.description) fail(`${skillMd}: frontmatter has no description`);
  if (skillDirs.includes(dir)) {
    fail(`"${dir}" exists in both skills/ and ${INTERNAL_ROOT}/ — a name lives in one tier only`);
  }
  if (entries[dir]) {
    fail(`skills/sources.json: "${dir}" is an internal skill — internal skills get no entry`);
  }
}

// `.claude/skills` must symlink to the internal tier so Claude Code sees it too.
const claudeSkills = join(ROOT, ".claude/skills");
if (!existsSync(claudeSkills)) {
  fail(".claude/skills: missing — must be a symlink to ../.agents/skills");
} else if (!lstatSync(claudeSkills).isSymbolicLink()) {
  fail(".claude/skills: is a real directory — must be a symlink to ../.agents/skills");
} else if (readlinkSync(claudeSkills) !== "../.agents/skills") {
  fail(`.claude/skills: points at ${readlinkSync(claudeSkills)}, expected ../.agents/skills`);
}

// ------------------------------------------------------------- 7. CLAUDE.md link
const claudeMd = join(ROOT, "CLAUDE.md");
if (!existsSync(claudeMd)) {
  fail("CLAUDE.md: missing (must be a symlink to AGENTS.md)");
} else if (!lstatSync(claudeMd).isSymbolicLink()) {
  fail("CLAUDE.md: is a regular file — must stay a symlink to AGENTS.md, see AGENTS.md");
} else if (readlinkSync(claudeMd) !== "AGENTS.md") {
  fail(`CLAUDE.md: symlink points at ${readlinkSync(claudeMd)}, expected AGENTS.md`);
}

// ------------------------------------------------------------------- report
for (const w of warnings) console.log(`\x1b[33mwarn\x1b[0m  ${w}`);
for (const e of errors) console.log(`\x1b[31mfail\x1b[0m  ${e}`);
console.log(
  `\n${skillDirs.length} skills · ${internalDirs.length} internal · v${VERSION} · ` +
    `${errors.length} error(s) · ${warnings.length} warning(s)`,
);
process.exit(errors.length ? 1 : 0);
