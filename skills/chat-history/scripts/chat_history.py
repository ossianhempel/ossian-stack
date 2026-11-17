#!/usr/bin/env python3
"""Search the user's own AI chat history across tools. Read-only, stdlib only.

Sources (auto-detected on this machine):
  claude-code  ~/.claude/projects/**/*.jsonl
  codex        ~/.codex/sessions/**/rollout-*.jsonl, ~/.codex/archived_sessions/
  pi           ~/.pi/agent/sessions/**/*.jsonl
  cursor       Cursor's state.vscdb (composer/agent chats)
Exports (pass with --export PATH; file, directory or .zip):
  claude-ai    claude.ai data export conversations.json
  chatgpt      ChatGPT data export conversations.json

Commands:
  sources                       list stores found and session counts
  search TERMS... [filters]     find messages containing every term
  show SESSION_REF [--full]     print one conversation (REF from search output)
"""

from __future__ import annotations

import argparse
import datetime as dt
import glob
import json
import os
import re
import sqlite3
import sys
import zipfile
from dataclasses import dataclass, field
from typing import Iterable, Iterator

HOME = os.path.expanduser("~")


@dataclass
class Msg:
    role: str  # "user" or "assistant"
    text: str
    ts: dt.datetime | None = None


@dataclass
class Session:
    source: str
    ref: str  # stable handle for `show`: "<source>:<locator>"
    title: str = ""
    cwd: str = ""
    started: dt.datetime | None = None
    messages: list[Msg] = field(default_factory=list)


# ---------------------------------------------------------------- helpers

def parse_ts(value) -> dt.datetime | None:
    if value in (None, ""):
        return None
    try:
        if isinstance(value, (int, float)):
            # seconds or milliseconds since epoch
            secs = value / 1000 if value > 1e11 else value
            return dt.datetime.fromtimestamp(secs, tz=dt.timezone.utc)
        s = str(value).replace("Z", "+00:00")
        t = dt.datetime.fromisoformat(s)
        return t if t.tzinfo else t.replace(tzinfo=dt.timezone.utc)
    except (ValueError, OverflowError, OSError):
        return None


def block_text(content, text_types=("text", "input_text", "output_text")) -> str:
    """Join the human-readable text in a message content field, skipping tool blocks."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for b in content:
            if isinstance(b, str):
                parts.append(b)
            elif isinstance(b, dict) and b.get("type") in text_types:
                parts.append(str(b.get("text", "")))
        return "\n".join(p for p in parts if p)
    return ""


# Harness-injected text that arrives as a "user" message but was not typed by the user.
INJECTED_PREFIXES = (
    "<environment_context>", "<user_instructions>", "# AGENTS.md", "<system-reminder>",
    "<command-name>", "<local-command-stdout>", "<command-message>", "Caveat: The messages below",
    "<user-prompt-submit-hook>", "This session is being continued from a previous conversation",
    "[Request interrupted",
)


def is_injected(text: str) -> bool:
    return text.lstrip().startswith(INJECTED_PREFIXES)


def read_jsonl(path: str) -> Iterator[dict]:
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(obj, dict):
                    yield obj
    except OSError:
        return


def file_contains_all(path: str, needles: list[str]) -> bool:
    """Cheap prefilter: skip files that cannot match before parsing JSON."""
    if not needles:
        return True
    try:
        with open(path, "rb") as fh:
            data = fh.read().decode("utf-8", errors="replace").lower()
    except OSError:
        return False
    return all(n in data for n in needles)


# ---------------------------------------------------------------- sources

def claude_code_files() -> list[str]:
    base = os.environ.get("CLAUDE_CONFIG_DIR") or os.path.join(HOME, ".claude")
    return sorted(glob.glob(os.path.join(base, "projects", "**", "*.jsonl"), recursive=True))


def load_claude_code(path: str) -> Session:
    s = Session("claude-code", f"claude-code:{path}")
    for o in read_jsonl(path):
        if o.get("type") == "summary" and o.get("summary") and not s.title:
            s.title = o["summary"]
        if o.get("type") not in ("user", "assistant") or o.get("isMeta"):
            continue
        s.cwd = s.cwd or o.get("cwd", "")
        ts = parse_ts(o.get("timestamp"))
        s.started = s.started or ts
        m = o.get("message") or {}
        role = m.get("role") or o["type"]
        text = block_text(m.get("content")).strip()
        if not text or (role == "user" and is_injected(text)):
            continue
        s.messages.append(Msg(role, text, ts))
    return s


def codex_files() -> list[str]:
    base = os.environ.get("CODEX_HOME") or os.path.join(HOME, ".codex")
    files = glob.glob(os.path.join(base, "sessions", "**", "*.jsonl"), recursive=True)
    files += glob.glob(os.path.join(base, "archived_sessions", "**", "*.jsonl"), recursive=True)
    return sorted(files)


def load_codex(path: str) -> Session:
    s = Session("codex", f"codex:{path}")
    for o in read_jsonl(path):
        typ = o.get("type")
        p = o.get("payload") if isinstance(o.get("payload"), dict) else o
        if typ == "session_meta" or (typ is None and "instructions" in o and "id" in o):
            s.cwd = s.cwd or p.get("cwd", "")
            s.started = s.started or parse_ts(p.get("timestamp") or o.get("timestamp"))
            continue
        # Current format wraps items in response_item; older rollouts store them bare.
        if typ not in ("response_item", "message", None) or p.get("type") != "message":
            continue
        role = p.get("role")
        if role not in ("user", "assistant"):
            continue
        text = block_text(p.get("content")).strip()
        if not text or (role == "user" and is_injected(text)):
            continue
        ts = parse_ts(o.get("timestamp"))
        s.started = s.started or ts
        s.messages.append(Msg(role, text, ts))
    return s


def pi_files() -> list[str]:
    base = os.environ.get("PI_CODING_AGENT_DIR") or os.path.join(HOME, ".pi", "agent")
    return sorted(glob.glob(os.path.join(base, "sessions", "**", "*.jsonl"), recursive=True))


def load_pi(path: str) -> Session:
    s = Session("pi", f"pi:{path}")
    for o in read_jsonl(path):
        if o.get("type") == "session":
            s.cwd = o.get("cwd", "")
            s.started = parse_ts(o.get("timestamp"))
            continue
        if o.get("type") != "message":
            continue
        m = o.get("message") or {}
        role = m.get("role")
        if role not in ("user", "assistant"):
            continue
        text = block_text(m.get("content")).strip()
        if not text:
            continue
        s.messages.append(Msg(role, text, parse_ts(o.get("timestamp") or m.get("timestamp"))))
    return s


def cursor_dbs() -> list[str]:
    candidates = [
        os.path.join(HOME, "Library", "Application Support", "Cursor", "User", "globalStorage", "state.vscdb"),
        os.path.join(HOME, ".config", "Cursor", "User", "globalStorage", "state.vscdb"),
        os.path.join(os.environ.get("APPDATA", ""), "Cursor", "User", "globalStorage", "state.vscdb"),
    ]
    return [c for c in candidates if c and os.path.isfile(c)]


def load_cursor(db: str) -> Iterator[Session]:
    """Composer/agent chats. Messages live inline (older) or as bubbleId:<chat>:<bubble> rows."""
    try:
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        rows = con.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'composerData:%'").fetchall()
    except sqlite3.Error as e:
        print(f"cursor: cannot read {db}: {e}", file=sys.stderr)
        return
    for key, value in rows:
        try:
            c = json.loads(value)
        except (TypeError, json.JSONDecodeError):
            continue
        cid = key.split(":", 1)[1]
        s = Session("cursor", f"cursor:{db}#{cid}", title=c.get("name") or "",
                    started=parse_ts(c.get("createdAt")))
        bubbles = c.get("conversation") or []
        if not bubbles:
            for h in c.get("fullConversationHeadersOnly") or []:
                row = con.execute("SELECT value FROM cursorDiskKV WHERE key = ?",
                                  (f"bubbleId:{cid}:{h.get('bubbleId')}",)).fetchone()
                if row:
                    try:
                        bubbles.append(json.loads(row[0]))
                    except (TypeError, json.JSONDecodeError):
                        pass
        for b in bubbles:
            role = {1: "user", 2: "assistant"}.get(b.get("type"))
            text = (b.get("text") or "").strip()
            if role and text:
                s.messages.append(Msg(role, text, parse_ts(b.get("createdAt"))))
        if s.messages:
            yield s
    con.close()


def export_payloads(path: str) -> Iterator[tuple[str, object]]:
    """Yield (label, parsed conversations.json) from a file, directory or zip."""
    path = os.path.abspath(os.path.expanduser(path))
    if os.path.isdir(path):
        for f in glob.glob(os.path.join(path, "**", "conversations.json"), recursive=True):
            yield from export_payloads(f)
    elif zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as z:
            for name in z.namelist():
                if name.endswith("conversations.json"):
                    yield f"{path}!{name}", json.loads(z.read(name))
    elif os.path.isfile(path):
        with open(path, encoding="utf-8") as fh:
            yield path, json.load(fh)
    else:
        print(f"export not found: {path}", file=sys.stderr)


def load_export(label: str, data) -> Iterator[Session]:
    if not isinstance(data, list):
        return
    for conv in data:
        if not isinstance(conv, dict):
            continue
        if "chat_messages" in conv:  # claude.ai
            s = Session("claude-ai", f"claude-ai:{label}#{conv.get('uuid')}",
                        title=conv.get("name") or "", started=parse_ts(conv.get("created_at")))
            for m in conv.get("chat_messages") or []:
                role = {"human": "user", "assistant": "assistant"}.get(m.get("sender"))
                text = (m.get("text") or block_text(m.get("content"))).strip()
                if role and text:
                    s.messages.append(Msg(role, text, parse_ts(m.get("created_at"))))
            yield s
        elif "mapping" in conv:  # ChatGPT
            cid = conv.get("conversation_id") or conv.get("id")
            s = Session("chatgpt", f"chatgpt:{label}#{cid}", title=conv.get("title") or "",
                        started=parse_ts(conv.get("create_time")))
            nodes = conv.get("mapping") or {}
            # Walk the active branch from current_node back to the root.
            chain, node = [], conv.get("current_node")
            while node and node in nodes:
                chain.append(nodes[node])
                node = nodes[node].get("parent")
            if not chain:
                chain = list(nodes.values())
            for n in reversed(chain):
                m = n.get("message") or {}
                role = (m.get("author") or {}).get("role")
                content = m.get("content") or {}
                if role not in ("user", "assistant") or content.get("content_type") not in ("text", "multimodal_text"):
                    continue
                text = "\n".join(p for p in content.get("parts") or [] if isinstance(p, str)).strip()
                if text:
                    s.messages.append(Msg(role, text, parse_ts(m.get("create_time"))))
            yield s


FILE_SOURCES = {
    "claude-code": (claude_code_files, load_claude_code),
    "codex": (codex_files, load_codex),
    "pi": (pi_files, load_pi),
}
ALL_SOURCES = ["claude-code", "codex", "pi", "cursor", "claude-ai", "chatgpt"]


def iter_sessions(sources: set[str], exports: list[str], needles: list[str]) -> Iterator[Session]:
    for name, (lister, loader) in FILE_SOURCES.items():
        if name in sources:
            for f in lister():
                if file_contains_all(f, needles):
                    yield loader(f)
    if "cursor" in sources:
        for db in cursor_dbs():
            yield from load_cursor(db)
    for e in exports:
        for label, data in export_payloads(e):
            for s in load_export(label, data):
                if s.source in sources:
                    yield s


# ---------------------------------------------------------------- commands

def parse_since(value: str | None) -> dt.datetime | None:
    if not value:
        return None
    m = re.fullmatch(r"(\d+)([dwmy])", value)
    if m:
        days = int(m.group(1)) * {"d": 1, "w": 7, "m": 30, "y": 365}[m.group(2)]
        return dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)
    t = parse_ts(value)
    if t is None:
        sys.exit(f"--since: expected 30d, 2w, 6m, 1y or a date, got {value!r}")
    return t


def snippet(text: str, pos: int, width: int) -> str:
    start = max(0, pos - width // 3)
    out = text[start:start + width].replace("\n", " ")
    return ("…" if start else "") + out + ("…" if start + width < len(text) else "")


def fmt_date(t: dt.datetime | None) -> str:
    return t.astimezone().strftime("%Y-%m-%d %H:%M") if t else "????-??-?? ??:??"


def session_label(s: Session) -> str:
    if s.title:
        return s.title
    first = next((m.text for m in s.messages if m.role == "user"), "")
    return first.replace("\n", " ")[:80]


def cmd_search(a) -> None:
    sources = set(a.source or ALL_SOURCES)
    since = parse_since(a.since)
    if a.regex:
        pats = [re.compile(t, re.I) for t in a.terms]
        needles: list[str] = []
    else:
        pats = [re.compile(re.escape(t), re.I) for t in a.terms]
        needles = [t.lower() for t in a.terms]
    hits = []
    for s in iter_sessions(sources, a.export or [], needles):
        if a.project and a.project.lower() not in (s.cwd or s.ref).lower():
            continue
        found = []
        for m in s.messages:
            if a.role != "any" and m.role != a.role:
                continue
            when = m.ts or s.started
            if since and when and when < since:
                continue
            if a.mode == "message":
                ok = all(p.search(m.text) for p in pats)
            else:
                ok = any(p.search(m.text) for p in pats)
            if ok:
                found.append(m)
        if a.mode == "session" and found:
            joined = "\n".join(m.text for m in found)
            if not all(p.search(joined) for p in pats):
                found = []
        if found:
            last = max((m.ts or s.started for m in found if (m.ts or s.started)), default=None)
            hits.append((last, s, found))
    hits.sort(key=lambda h: h[0] or dt.datetime.min.replace(tzinfo=dt.timezone.utc), reverse=True)
    hits = hits[: a.limit]

    if a.json:
        print(json.dumps([{
            "source": s.source, "ref": s.ref, "title": session_label(s), "cwd": s.cwd,
            "last_match": last.isoformat() if last else None,
            "matches": [{"role": m.role, "ts": m.ts.isoformat() if m.ts else None,
                         "text": m.text[: a.width * 4]} for m in found[: a.per_session]],
        } for last, s, found in hits], ensure_ascii=False, indent=1))
        return
    if not hits:
        print("no matches", file=sys.stderr)
        return
    for last, s, found in hits:
        print(f"== {fmt_date(last)}  [{s.source}]  {session_label(s)}")
        if s.cwd:
            print(f"   cwd: {s.cwd}")
        print(f"   ref: {s.ref}")
        for m in found[: a.per_session]:
            pos = min((p.search(m.text).start() for p in pats if p.search(m.text)), default=0)
            print(f"   {m.role:>9}: {snippet(m.text, pos, a.width)}")
        if len(found) > a.per_session:
            print(f"   (+{len(found) - a.per_session} more matching messages)")
        print()


def find_session(ref: str, exports: list[str]) -> Session | None:
    source, _, loc = ref.partition(":")
    if source in FILE_SOURCES:
        return FILE_SOURCES[source][1](loc) if os.path.isfile(loc) else None
    if source == "cursor":
        db, _, _cid = loc.partition("#")
        return next((s for s in load_cursor(db) if s.ref == ref), None)
    if source in ("claude-ai", "chatgpt"):
        label = loc.rsplit("#", 1)[0]
        path = label.split("!", 1)[0]
        for lab, data in export_payloads(path):
            for s in load_export(lab, data):
                if s.ref == ref:
                    return s
    return None


def cmd_show(a) -> None:
    s = find_session(a.ref, a.export or [])
    if not s:
        sys.exit(f"session not found: {a.ref}")
    print(f"# {session_label(s)}\nsource: {s.source}  started: {fmt_date(s.started)}  cwd: {s.cwd or '-'}\n")
    msgs = [m for m in s.messages if a.role == "any" or m.role == a.role]
    for m in msgs:
        body = m.text if a.full or len(m.text) <= a.max_chars else m.text[: a.max_chars] + " …[truncated]"
        print(f"--- {m.role} {fmt_date(m.ts) if m.ts else ''}".rstrip() + f"\n{body}\n")


def cmd_sources(a) -> None:
    for name, (lister, _) in FILE_SOURCES.items():
        files = lister()
        print(f"{name:12} {len(files):6} session files")
    dbs = cursor_dbs()
    print(f"{'cursor':12} {len(dbs):6} database(s) {' '.join(dbs)}")
    for e in a.export or []:
        for label, data in export_payloads(e):
            sess = list(load_export(label, data))
            kinds = sorted({s.source for s in sess}) or ["unrecognized"]
            print(f"{'/'.join(kinds):12} {len(sess):6} conversations in {label}")


def main(argv: Iterable[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p):
        p.add_argument("--export", action="append", metavar="PATH",
                       help="claude.ai or ChatGPT export (zip, dir, or conversations.json); repeatable")

    p = sub.add_parser("sources", help="list stores found on this machine")
    common(p)
    p.set_defaults(fn=cmd_sources)

    p = sub.add_parser("search", help="search messages")
    p.add_argument("terms", nargs="+")
    p.add_argument("--source", action="append", choices=ALL_SOURCES, help="repeatable; default all")
    p.add_argument("--role", choices=["user", "assistant", "any"], default="any")
    p.add_argument("--since", help="30d, 2w, 6m, 1y, or a date")
    p.add_argument("--project", help="substring of the session's working directory")
    p.add_argument("--regex", action="store_true", help="treat terms as regular expressions")
    p.add_argument("--mode", choices=["message", "session"], default="message",
                   help="all terms in one message (default) or anywhere in the session")
    p.add_argument("--limit", type=int, default=20, help="max sessions")
    p.add_argument("--per-session", type=int, default=3)
    p.add_argument("--width", type=int, default=220, help="snippet characters")
    p.add_argument("--json", action="store_true")
    common(p)
    p.set_defaults(fn=cmd_search)

    p = sub.add_parser("show", help="print one conversation")
    p.add_argument("ref", help="the ref: line from search output")
    p.add_argument("--role", choices=["user", "assistant", "any"], default="any")
    p.add_argument("--full", action="store_true", help="do not truncate long messages")
    p.add_argument("--max-chars", type=int, default=1500)
    common(p)
    p.set_defaults(fn=cmd_show)

    a = ap.parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        pass
