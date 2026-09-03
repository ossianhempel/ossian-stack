#!/usr/bin/env node
/**
 * Build the data block for docs/plugin-map/index.html.
 *
 *   bun scripts/build-plugin-map.js          # rewrite the JSON block in index.html
 *   bun scripts/build-plugin-map.js --check  # exit 1 if anything is out of date
 *
 * Sources, merged in this order:
 *   skills/<name>/SKILL.md frontmatter   name, description, invocation flags
 *   skills/<name>/agents/openai.yaml     display_name
 *   skills/sources.json                  origin + upstream repo
 *   agents/<name>.md (optional)          subagents, if the plugin ever ships any
 *   docs/plugin-map/map.json             role, kind, calls graph, board sections
 *
 * Fails when a skill or agent on disk is missing from map.json, when map.json
 * names something that no longer exists, when an id is placed in zero or two
 * sections, or (with --check) when the HTML block is stale.
 *
 * Plain Node APIs only — runs under bun or node.
 */
const fs = require("node:fs");
const path = require("node:path");

const ROOT = path.resolve(__dirname, "..");
const MAP_PATH = path.join(ROOT, "docs/plugin-map/map.json");
const HTML_PATH = path.join(ROOT, "docs/plugin-map/index.html");
const BEGIN = "<!-- plugin-map:begin -->";
const END = "<!-- plugin-map:end -->";
const CHECK = process.argv.includes("--check");

const errors = [];
const warnings = [];
const fail = (m) => errors.push(m);
const warn = (m) => warnings.push(m);
const read = (p) => fs.readFileSync(p, "utf8");

// ------------------------------------------------------------ tiny YAML reader
// Enough of YAML for skill frontmatter: scalars, quoted strings, block scalars
// (> and |), and inline JSON on a key. Nested maps are skipped, not parsed.
function frontmatter(text) {
  const m = text.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!m) return null;
  const lines = m[1].split(/\r?\n/);
  const out = {};
  for (let i = 0; i < lines.length; i++) {
    const kv = lines[i].match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (!kv) continue;
    const key = kv[1];
    let val = kv[2];
    if (/^[>|][-+]?$/.test(val)) {
      const fold = val.startsWith(">");
      const buf = [];
      while (i + 1 < lines.length && (/^\s+\S/.test(lines[i + 1]) || lines[i + 1].trim() === "")) {
        buf.push(lines[++i].replace(/^\s+/, ""));
      }
      val = fold ? buf.join(" ").replace(/\s+/g, " ").trim() : buf.join("\n").trim();
    } else if ((val.startsWith('"') && !/"\s*$/.test(val.slice(1))) || (val.startsWith("'") && !/'\s*$/.test(val.slice(1)))) {
      const q = val[0];
      while (i + 1 < lines.length && !new RegExp(q + "\\s*$").test(val)) val += " " + lines[++i].trim();
      val = val.slice(1, -1);
    } else if (/^".*"$/.test(val) || /^'.*'$/.test(val)) {
      val = val.slice(1, -1);
    } else if (val === "") {
      continue; // nested map — ignore
    }
    if (val === "true") val = true;
    else if (val === "false") val = false;
    out[key] = val;
  }
  return out;
}

// ------------------------------------------------------------------- inputs
const map = JSON.parse(read(MAP_PATH));
const sources = JSON.parse(read(path.join(ROOT, "skills/sources.json")));
const sourceEntries = sources.skills ?? sources;

const skillsDir = path.join(ROOT, "skills");
const diskSkills = fs
  .readdirSync(skillsDir)
  .filter((n) => !n.startsWith(".") && fs.statSync(path.join(skillsDir, n)).isDirectory())
  .sort();

const agentsDir = path.join(ROOT, "agents");
const diskAgents = fs.existsSync(agentsDir)
  ? fs.readdirSync(agentsDir).filter((n) => n.endsWith(".md")).map((n) => n.replace(/\.md$/, "")).sort()
  : [];

const pluginIds = Object.keys(map.plugins);
const PLUGIN = pluginIds[0];
const ROLES = new Set(["human", "both", "auto", "knowledge"]);

// ------------------------------------------------------- disk <-> map.json
for (const id of diskSkills) if (!map.skills[id]) fail(`skills/${id}/ is on disk but not in map.json "skills"`);
for (const id of Object.keys(map.skills)) if (!diskSkills.includes(id)) fail(`map.json skills."${id}" no longer exists on disk`);
for (const id of diskAgents) if (!map.agents[id]) fail(`agents/${id}.md is on disk but not in map.json "agents"`);
for (const id of Object.keys(map.agents)) if (!diskAgents.includes(id)) fail(`map.json agents."${id}" no longer exists on disk`);

const known = new Set([...Object.keys(map.skills), ...Object.keys(map.agents)]);

for (const [id, s] of Object.entries(map.skills)) {
  if (!ROLES.has(s.role)) fail(`map.json skills."${id}".role "${s.role}" is not one of ${[...ROLES].join("/")}`);
}
for (const [from, tos] of Object.entries(map.calls)) {
  if (!known.has(from)) fail(`map.json calls."${from}" is not a known skill or agent`);
  for (const to of tos) if (!known.has(to)) fail(`map.json calls."${from}" names unknown "${to}"`);
}

// Every id is drawn exactly once.
const placed = new Map();
const place = (id, where) => {
  if (!known.has(id)) fail(`map.json sections: "${id}" (${where}) is not a known skill or agent`);
  if (placed.has(id)) fail(`map.json sections: "${id}" is drawn twice (${placed.get(id)} and ${where})`);
  placed.set(id, where);
};
for (const lane of map.sections.lanes) {
  for (const st of lane.steps) place(st.id, `lane ${lane.id}`);
  for (const st of lane.extras ?? []) place(st.id, `lane ${lane.id} extras`);
}
for (const p of map.sections.platforms) for (const s of p.skills) place(s.id, `platform ${p.id}`);
for (const id of map.sections.sideDoors) place(id, "sideDoors");
for (const id of map.sections.knowledge.ids) place(id, "knowledge");
for (const id of known) if (!placed.has(id)) fail(`map.json sections: "${id}" is not drawn anywhere`);

// ------------------------------------------- merge frontmatter into nodes
const nodes = {};
for (const id of diskSkills) {
  const fm = frontmatter(read(path.join(skillsDir, id, "SKILL.md"))) ?? {};
  let display = id;
  const yamlPath = path.join(skillsDir, id, "agents/openai.yaml");
  if (fs.existsSync(yamlPath)) {
    const dm = read(yamlPath).match(/display_name:\s*["']?([^"'\n]+)["']?/);
    if (dm) display = dm[1].trim();
  }
  const src = sourceEntries[id] ?? {};
  const curated = map.skills[id] ?? {};
  nodes[id] = {
    id,
    type: "skill",
    plugin: PLUGIN,
    display,
    description: String(fm.description ?? "").trim(),
    role: curated.role,
    humanOnly: fm["disable-model-invocation"] === true,
    argumentHint: fm["argument-hint"] ?? null,
    origin: src.origin ?? null,
    repo: src.repo ?? null,
    calls: map.calls[id] ?? [],
  };
  if (!nodes[id].description) fail(`skills/${id}/SKILL.md: frontmatter has no description`);
  if (nodes[id].humanOnly && !["human", "knowledge"].includes(curated.role)) {
    warn(`${id}: disable-model-invocation is set but map.json role is "${curated.role}"`);
  }
  if (!nodes[id].humanOnly && curated.role === "human") {
    warn(`${id}: map.json role is "human" but SKILL.md does not set disable-model-invocation`);
  }
  // Sibling references in the SKILL.md that map.json does not record as calls.
  const body = read(path.join(skillsDir, id, "SKILL.md"));
  const refs = new Set([...body.matchAll(/`([a-z0-9-]+)`/g)].map((m) => m[1]).filter((t) => t !== id && diskSkills.includes(t)));
  for (const r of refs) if (!(map.calls[id] ?? []).includes(r)) warn(`${id}: SKILL.md mentions \`${r}\` but map.json calls does not`);
}
for (const id of diskAgents) {
  const fm = frontmatter(read(path.join(agentsDir, id + ".md"))) ?? {};
  nodes[id] = {
    id,
    type: "agent",
    plugin: PLUGIN,
    display: fm.name ?? id,
    description: String(fm.description ?? "").trim(),
    role: "auto",
    kind: map.agents[id].kind,
    humanOnly: false,
    argumentHint: null,
    origin: null,
    repo: null,
    calls: map.calls[id] ?? [],
  };
}
// Reverse edges.
for (const n of Object.values(nodes)) n.calledBy = [];
for (const n of Object.values(nodes)) for (const to of n.calls) nodes[to]?.calledBy.push(n.id);

const data = {
  generated: "scripts/build-plugin-map.js",
  plugins: map.plugins,
  runtimes: map.runtimes,
  entry: map.entry,
  sections: map.sections,
  nodes,
  counts: { skills: diskSkills.length, agents: diskAgents.length, plugins: pluginIds.length },
};

// ------------------------------------------------------------------ output
for (const w of warnings) console.log(`warn  ${w}`);
for (const e of errors) console.log(`fail  ${e}`);
if (errors.length) {
  console.log(`\nplugin-map: ${errors.length} error(s)`);
  process.exit(1);
}

const html = read(HTML_PATH);
const a = html.indexOf(BEGIN);
const b = html.indexOf(END);
if (a < 0 || b < 0 || b < a) {
  console.log(`fail  ${path.relative(ROOT, HTML_PATH)}: marker comments not found`);
  process.exit(1);
}
const block = `${BEGIN}\n<script type="application/json" id="plugin-map-data">\n${JSON.stringify(data, null, 1)}\n</script>\n`;
const next = html.slice(0, a) + block + html.slice(b);

if (CHECK) {
  if (next !== html) {
    console.log(`fail  docs/plugin-map/index.html data block is stale — run: bun run map`);
    process.exit(1);
  }
  console.log(`plugin-map: ok · ${data.counts.skills} skills · ${data.counts.agents} agents · ${data.counts.plugins} plugin(s)`);
} else {
  fs.writeFileSync(HTML_PATH, next);
  console.log(`plugin-map: wrote data block · ${data.counts.skills} skills · ${data.counts.agents} agents · ${data.counts.plugins} plugin(s)`);
}
