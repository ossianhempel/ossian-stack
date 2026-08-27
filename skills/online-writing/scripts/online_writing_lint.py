#!/usr/bin/env python3
"""Mechanical shape checks for online articles.

Checks only what can be counted: word budget, headline shape, subhead style,
paragraph sentence counts, runs of long paragraphs, intro bookends.

It cannot see Form/Idea mismatch, a weak PROMISE, or Rate of Revelation.
Those are judgment gates in references/audit-rubric.md.

Usage:
    python3 online_writing_lint.py draft.md
    pbpaste | python3 online_writing_lint.py -
"""

import re
import sys

SWEET_SPOT = (800, 1200)
HEADLINE_MAX_WORDS = 12
PARA_SENTENCE_CEILING = 5
PARA_SENTENCE_HARD = 7
LONG_PARA_WORDS = 60
LONG_PARA_RUN = 3
GREASED_CHUTE_MAX = 8

PREAMBLE = re.compile(
    r"^\s*(a few thoughts|some thoughts|thoughts on|the reason why|some notes|"
    r"notes on|in this (article|post)|why i|on the subject|a look at|"
    r"an? (introduction|overview|update) to)\b",
    re.I,
)

# Words that carry no promise on their own when they end a headline.
WEAK_TAIL = {
    "thing", "things", "stuff", "idea", "ideas", "it", "them", "this",
    "that", "more", "better", "today", "now", "etc",
}

VAGUE_QUANTIFIER = re.compile(
    r"^\s*#*\s*\d+\s+(ways|things|tips|lessons|reasons|steps|habits|mistakes)\b",
    re.I,
)

SENTENCE_END = re.compile(r"(?<=[.!?])[\"')\]]*\s+")


def sentences(text):
    text = text.strip()
    if not text:
        return []
    parts = [p.strip() for p in SENTENCE_END.split(text) if p.strip()]
    return parts


def words(text):
    return re.findall(r"[A-Za-z0-9'’\-]+", text)


class Report:
    def __init__(self):
        self.rows = []

    def add(self, level, gate, msg, detail=None):
        self.rows.append((level, gate, msg, detail))

    def emit(self):
        order = {"FAIL": 0, "WARN": 1, "INFO": 2}
        self.rows.sort(key=lambda r: order[r[0]])
        fails = sum(1 for r in self.rows if r[0] == "FAIL")
        warns = sum(1 for r in self.rows if r[0] == "WARN")
        for level, gate, msg, detail in self.rows:
            print(f"{level:4}  {gate:5}  {msg}")
            if detail:
                for line in detail:
                    print(f"              {line}")
        print()
        print(f"{fails} fail, {warns} warn, "
              f"{len(self.rows) - fails - warns} info")
        print("Mechanical checks only. Run references/audit-rubric.md "
              "for Form, PROMISE, and Rate of Revelation.")
        return 1 if fails else 0


def parse_blocks(text):
    """Yield (kind, level, raw) for headings, code fences, and paragraphs."""
    blocks = []
    in_fence = False
    buf = []

    def flush():
        if buf:
            joined = "\n".join(buf).strip()
            if joined:
                blocks.append(("para", 0, joined))
            buf.clear()

    for line in text.splitlines():
        if line.strip().startswith("```"):
            flush()
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            flush()
            blocks.append(("heading", len(m.group(1)), m.group(2).strip()))
            continue
        if not line.strip():
            flush()
            continue
        buf.append(line)
    flush()
    return blocks


def check_headline(h, rep):
    w = words(h)
    if len(w) > HEADLINE_MAX_WORDS:
        rep.add("WARN", "G7", f"Headline is {len(w)} words (target <= "
                f"{HEADLINE_MAX_WORDS}).",
                ["Run the 4-step rewriting process; cut connecting words."])
    if PREAMBLE.match(h):
        rep.add("FAIL", "G6", "Headline opens with a preamble - the first "
                "words don't name the thing.",
                [f'"{h}"',
                 "Delete leading words until words 1-3 name the subject."])
    if w:
        tail = w[-1].lower().strip(".,!?:;")
        if tail in WEAK_TAIL:
            rep.add("WARN", "G6", f'Headline ends on "{w[-1]}" - the final '
                    "words should carry the PROMISE.")
    if VAGUE_QUANTIFIER.match(h):
        rep.add("WARN", "G5", "Headline uses a generic quantifier "
                '(e.g. "7 Ways").',
                ["Swap for a POWER phrase: 7 Little-Known Ways, "
                 "7 Small But Powerful Ways."])
    if not re.search(r"\d", h):
        rep.add("INFO", "G5", "Headline has no number. Numbers read as "
                "declarative and lower the barrier to entry.")


def check_subhead(h, rep):
    w = words(h)
    if len(w) <= 3:
        plural = "word" if len(w) == 1 else "words"
        rep.add("FAIL", "G14", f'Label subhead: "{h}" ({len(w)} {plural}).',
                ["A skimmer reading only subheads must still get it.",
                 "Rewrite as the finding, not the topic."])
    elif len(w) <= 5 and not re.search(
            r"\b(is|are|was|were|has|have|will|should|can|do|does|make|makes|"
            r"means|beats|wins|fails|kills|needs|use|write|cut|start|stop)\b",
            h, re.I):
        rep.add("WARN", "G14", f'Subhead may be a label: "{h}".',
                ["State the point as a claim with a verb."])


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    src = sys.argv[1]
    text = sys.stdin.read() if src == "-" else open(src, encoding="utf-8").read()

    rep = Report()
    blocks = parse_blocks(text)
    paras = [b for b in blocks if b[0] == "para"]
    headings = [b for b in blocks if b[0] == "heading"]

    total_words = len(words("\n".join(b[2] for b in blocks)))
    lo, hi = SWEET_SPOT
    if total_words < lo:
        rep.add("WARN", "G15", f"{total_words} words - under the "
                f"{lo}-{hi} sweet spot.")
    elif total_words > hi:
        rep.add("WARN", "G15", f"{total_words} words - over the "
                f"{lo}-{hi} sweet spot.",
                ["More Main Points does not mean a longer piece. "
                 "Cut or split."])
    else:
        rep.add("INFO", "G15", f"{total_words} words - inside the "
                f"{lo}-{hi} sweet spot.")

    # Headline: first h1, else first heading, else first line.
    headline = next((raw for kind, level, raw in blocks
                     if kind == "heading" and level == 1), None)
    if headline is None:
        headline = next((raw for kind, _, raw in blocks
                         if kind == "heading"), None)
    if headline:
        check_headline(headline, rep)
    else:
        rep.add("WARN", "G5", "No heading found - cannot check the headline.")

    subheads = [h for h in headings if h[2] != headline]
    if not subheads:
        rep.add("WARN", "G14", "No subheads. Readers' eyes seek subheads "
                "before paragraphs.")
    for _, _, raw in subheads:
        check_subhead(raw, rep)

    if len(subheads) >= 2:
        firsts = [words(s[2])[0].lower() for s in subheads if words(s[2])]
        if len(set(firsts)) == len(firsts) and len(firsts) >= 3:
            rep.add("INFO", "G19", "Subheads share no parallel phrasing.",
                    ["Read them as a list in isolation - a deliberate set "
                     "signals the piece was organized."])

    # Paragraph shape.
    long_run = 0
    for idx, (_, _, raw) in enumerate(paras, start=1):
        if raw.lstrip().startswith(("-", "*", ">", "|")) or re.match(
                r"^\d+\.", raw.lstrip()):
            long_run = 0
            continue
        sents = sentences(raw)
        n = len(sents)
        wc = len(words(raw))
        if n > PARA_SENTENCE_HARD:
            rep.add("FAIL", "G17", f"Paragraph {idx}: {n} sentences "
                    f"(1/{n - 2}/1 territory).",
                    [f'"{sents[0][:70]}..."',
                     "Too many points -> split. Too much description -> cut "
                     "words. Unless it follows a 1/1/1+ run (decrescendo)."])
        elif n > PARA_SENTENCE_CEILING:
            rep.add("WARN", "G17", f"Paragraph {idx}: {n} sentences "
                    f"(ceiling {PARA_SENTENCE_CEILING}).",
                    ["Keep it as one block braced by single-sentence "
                     "bookends, or split it."])
        if wc >= LONG_PARA_WORDS:
            long_run += 1
            if long_run >= LONG_PARA_RUN:
                rep.add("FAIL", "G18", f"Paragraph {idx}: {long_run} long "
                        "paragraphs in a row.",
                        ["Never three or more. Resolve a long paragraph with "
                         "a single declarative sentence."])
                long_run = 0
        else:
            long_run = 0

    # Intro shape: first paragraph after the headline.
    intro = None
    seen_headline = headline is None
    for kind, level, raw in blocks:
        if kind == "heading" and raw == headline:
            seen_headline = True
            continue
        if kind == "para" and seen_headline:
            intro = raw
            break
    if intro:
        sents = sentences(intro)
        first_w = len(words(sents[0])) if sents else 0
        if first_w > GREASED_CHUTE_MAX:
            rep.add("WARN", "G11", f"Opening sentence is {first_w} words "
                    f"(greased chute: <= {GREASED_CHUTE_MAX}).",
                    [f'"{sents[0][:80]}"'])
        if len(sents) > 7:
            rep.add("FAIL", "G11", f"Intro paragraph is {len(sents)} "
                    "sentences.",
                    ["Every valid intro opens on one sentence and closes on "
                     "one. Default to 1/3/1."])
    else:
        rep.add("WARN", "G11", "No introduction paragraph found.")

    return rep.emit()


if __name__ == "__main__":
    sys.exit(main())
