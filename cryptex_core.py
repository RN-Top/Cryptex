"""Core logic for Cryptex werd — no Streamlit imports, so it can be tested on its own.

The cylinder is a grid of 26 rows (wrapping around, like the real brass cylinder)
by 6 rings (columns, which do NOT wrap). Words are searched in every direction:

  GIFT   (forward,  read left -> right):  RIGHT, DOWN-RIGHT, UP-RIGHT   (+ DOWN if vertical is on)
  INTENT (backward, read right -> left):  LEFT,  UP-LEFT,    DOWN-LEFT  (+ UP   if vertical is on)
"""
import html
import os
import re
import time
import unicodedata

# Drew's 26-letter Pythagorean reduction alphabet (9 columns read down: A J S / B K T / ...)
DEVICE_ALPHA = "AJSBKTCLUDMVENWFOXGPYHQZIR"
RINGS = 6
ROWS = 26
CENTER = 12  # grid row index of the main row; displayed rows run -12 .. +13

PYTHAGOREAN_VALUES = {
    'A': 1, 'J': 1, 'S': 1, 'B': 2, 'K': 2, 'T': 2, 'C': 3, 'L': 3, 'U': 3,
    'D': 4, 'M': 4, 'V': 4, 'E': 5, 'N': 5, 'W': 5, 'F': 6, 'O': 6, 'X': 6,
    'G': 7, 'P': 7, 'Y': 7, 'H': 8, 'Q': 8, 'Z': 8, 'I': 9, 'R': 9
}

LETTER_MEANINGS = {
    'A': "Initiative & Origin", 'B': "Harmony & Cooperation", 'C': "Creative Spark",
    'D': "Foundation & Tenacity", 'E': "Freedom & Catalyst", 'F': "Nurturing Heart",
    'G': "Spiritual Intellect", 'H': "Power & Manifestation", 'I': "Universal Compassion",
    'J': "Bold Leadership", 'K': "Intuitive Insight", 'L': "Expressive Grace",
    'M': "Work & Stability", 'N': "Curiosity & Flow", 'O': "Protective Devotion",
    'P': "Philosophical Depth", 'Q': "Original Authority", 'R': "Mastery & Wisdom",
    'S': "Dynamic Will", 'T': "Peace & Patience", 'U': "Receptive Abundance",
    'V': "Architectural Vision", 'W': "Adaptive Transformation", 'X': "Mystery & Transition",
    'Y': "Intuitive Independence", 'Z': "Spiritual Endurance"
}

NUMEROLOGY_THEMES = {
    1: ("The Pioneer", "New beginnings, bold initiative, independence, and raw potential.", "Step forward fearlessly. A fresh cycle is initiating, urging you to trust your individual vision and lead without hesitation."),
    2: ("The Mirror", "Partnership, balance, intuition, and diplomatic harmony.", "Seek balance over force. Listen closely to subtle intuitions and cultivate harmony within partnerships and quiet spaces."),
    3: ("The Spark", "Creative expansion, joyous self-expression, and communication.", "Your voice and creativity hold power right now. Release self-doubt, express your truth authentically, and embrace lighthearted joy."),
    4: ("The Anchor", "Stability, discipline, grounded structure, and order.", "Build steadily upon solid foundations. Focus on patience, practical habits, and grounding your ideas into tangible reality."),
    5: ("The Catalyst", "Freedom, dynamic movement, curiosity, and transformation.", "Embrace unexpected shifts and welcome adventure. The winds of change are clearing away stagnant energy to expand your horizons."),
    6: ("The Guardian", "Nurturing love, protective balance, and community healing.", "Tend to the heart and home. Offer compassion to those you care for, while upholding healthy personal boundaries."),
    7: ("The Mystic", "Deep introspection, analytical truth, and spiritual search.", "Withdraw into quiet contemplation. The answers you seek cannot be found in outward noise - trust deep reflection and inner wisdom."),
    8: ("The Crown", "Manifestation, power, material mastery, and ambition.", "Step into your personal authority. Karma and material equilibrium support purposeful efforts to manifest lasting impact."),
    9: ("The Sage", "Universal wisdom, culmination, compassion, and completion.", "A cycle is completing. Release what no longer serves your growth, forgive past chapters, and step into higher perspective.")
}

# ---------------------------------------------------------------- lexicon
# (key, file, label, on by default, rank for readings: lower = more meaningful)
TIERS = [
    ("common", "common.txt", "Everyday English", True, 0),
    ("mystic", "mystic.txt", "Mystic, myth, titles & names", True, 0),
    ("slang", "slang.txt", "Slang & internet speak", True, 1),
    ("crude", "crude.txt", "Crude & adult slang", True, 1),
    ("dictionary", "dictionary.txt", "Full Scrabble dictionary", True, 2),
    ("deep", "deep.txt", "Deep lexicon (rare words, abbreviations, names)", False, 3),
]
TIER_LABEL = {t[0]: t[2] for t in TIERS}
TIER_RANK = {t[0]: t[4] for t in TIERS}
LEXICON_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lexicon")
_WORD = re.compile(r"[A-Z]{3,6}")


def read_wordfile(path):
    words = set()
    if not os.path.exists(path):
        return words
    with open(path, encoding="utf-8", errors="ignore") as f:
        for line in f:
            w = line.strip().upper()
            if w and not w.startswith("#") and _WORD.fullmatch(w):
                words.add(w)
    return words


def load_tiers(lexicon_dir=LEXICON_DIR):
    """Return {tier_key: set(words)} plus the Clean-mode filter set."""
    tiers = {key: read_wordfile(os.path.join(lexicon_dir, fname)) for key, fname, *_ in TIERS}
    clean_filter = read_wordfile(os.path.join(lexicon_dir, "clean_filter.txt")) | tiers["crude"]
    return tiers, clean_filter


def build_lookup(tiers, clean_filter, enabled, clean_mode=False):
    """Map WORD -> tier key, for the enabled tiers. Earlier tiers in TIERS win."""
    lookup = {}
    for key, *_ in reversed(TIERS):  # reversed so earlier tiers overwrite later ones
        if key in enabled:
            for w in tiers.get(key, ()):
                lookup[w] = key
    if clean_mode:
        for w in clean_filter:
            lookup.pop(w, None)
    return lookup


# ---------------------------------------------------------------- meanings
IRREGULAR = {
    "RAN": "RUN", "WENT": "GO", "GONE": "GO", "SAT": "SIT", "SANG": "SING", "SUNG": "SING", "SAW": "SEE",
    "SEEN": "SEE", "ATE": "EAT", "EATEN": "EAT", "BEGAN": "BEGIN", "BEGUN": "BEGIN", "BROKE": "BREAK",
    "CAME": "COME", "DID": "DO", "DONE": "DO", "DREW": "DRAW", "DRANK": "DRINK", "DROVE": "DRIVE",
    "FELL": "FALL", "FELT": "FEEL", "FLEW": "FLY", "FORGOT": "FORGET", "FROZE": "FREEZE", "GAVE": "GIVE",
    "GREW": "GROW", "HID": "HIDE", "HELD": "HOLD", "KEPT": "KEEP", "KNEW": "KNOW", "KNOWN": "KNOW",
    "LAID": "LAY", "LED": "LEAD", "LEFT": "LEAVE", "LENT": "LEND", "LOST": "LOSE", "MADE": "MAKE",
    "MET": "MEET", "PAID": "PAY", "RANG": "RING", "RODE": "RIDE", "ROSE": "RISE", "RISEN": "RISE",
    "SAID": "SAY", "SENT": "SEND", "SHOOK": "SHAKE", "SHONE": "SHINE", "SHOT": "SHOOT", "SLEPT": "SLEEP",
    "SPOKE": "SPEAK", "SPENT": "SPEND", "SPUN": "SPIN", "STOLE": "STEAL", "STOOD": "STAND", "STUCK": "STICK",
    "SWAM": "SWIM", "SWORE": "SWEAR", "TAUGHT": "TEACH", "TOLD": "TELL", "TOOK": "TAKE", "TORE": "TEAR",
    "THREW": "THROW", "WOKE": "WAKE", "WON": "WIN", "WORE": "WEAR", "WOVE": "WEAVE", "WROTE": "WRITE",
    "MEN": "MAN", "WOMEN": "WOMAN", "FEET": "FOOT", "TEETH": "TOOTH", "MICE": "MOUSE", "GEESE": "GOOSE",
    "BETTER": "GOOD", "BEST": "GOOD", "WORSE": "BAD", "WORST": "BAD",
}


def load_meanings(lexicon_dir=LEXICON_DIR):
    """Return (glosses, definitions).
    glosses:     WORD -> [(kind, text)]   hand-written slang/mystic/title/name/crude meanings
    definitions: WORD -> [(pos, text)] or the string '=BASE' for word forms (DOGS -> =DOG)
    """
    glosses, definitions = {}, {}
    gpath = os.path.join(lexicon_dir, "glosses.txt")
    if os.path.exists(gpath):
        with open(gpath, encoding="utf-8") as f:
            for line in f:
                if line.startswith("#") or "|" not in line:
                    continue
                parts = [x.strip() for x in line.split("|", 2)]
                if len(parts) == 3 and parts[0]:
                    glosses.setdefault(parts[0].upper(), []).append((parts[1], parts[2]))
    dpath = os.path.join(lexicon_dir, "definitions.tsv")
    if os.path.exists(dpath):
        with open(dpath, encoding="utf-8") as f:
            for line in f:
                if line.startswith("#"):
                    continue
                parts = line.rstrip("\n").split("\t")
                if len(parts) == 2 and parts[1].startswith("="):
                    definitions[parts[0]] = parts[1]
                elif len(parts) >= 3:
                    definitions[parts[0]] = [(parts[i], parts[i + 1]) for i in range(1, len(parts) - 1, 2)]
    return glosses, definitions


def explain(word, meanings):
    """Plain-language explanation of one word.
    Returns dict(lines=[(label, text)], base=WORD or None, vibration=(n, title, desc))."""
    glosses, definitions = meanings
    lines, base = [], None
    for kind, text in glosses.get(word, []):
        lines.append((kind, text))
    d = definitions.get(word)
    if d is None and word in IRREGULAR:
        d = "=" + IRREGULAR[word]
    if isinstance(d, str):
        base = d[1:]
        d = definitions.get(base)
        if isinstance(d, str):
            d = None
        if not lines:
            for kind, text in glosses.get(base, []):
                lines.append((kind, text))
    if d:
        lines.extend(d if not lines else d[:1])  # slang/mystic meaning first, then the dictionary sense
    n, title, desc, _ = numerology(word)
    return {"lines": lines, "base": base, "vibration": (n, title, desc)}


def short_meaning(info, n=80):
    if not info["lines"]:
        return ""
    t = info["lines"][0][1]
    return t if len(t) <= n else t[: n - 1].rsplit(" ", 1)[0] + "…"


# ---------------------------------------------------------------- cylinder
def build_grid(offsets):
    """26 x 6 list of letters. Row CENTER is the main row."""
    return [[DEVICE_ALPHA[(offsets[c] + r - CENTER) % 26] for c in range(RINGS)] for r in range(ROWS)]


def row_label(r):
    s = r - CENTER
    return "MAIN" if s == 0 else f"{s:+d}"


# (name, arrow, d_row, d_col, kind)
DIRECTIONS = [
    ("RIGHT", "→", 0, 1, "gift"),
    ("DOWN-RIGHT", "↘", 1, 1, "gift"),
    ("UP-RIGHT", "↗", -1, 1, "gift"),
    ("LEFT", "←", 0, -1, "intent"),
    ("UP-LEFT", "↖", -1, -1, "intent"),
    ("DOWN-LEFT", "↙", 1, -1, "intent"),
]
VERTICAL = [
    ("DOWN", "↓", 1, 0, "gift"),
    ("UP", "↑", -1, 0, "intent"),
]


def find_words(grid, lookup, min_len=3, horizontal=True, diagonal=True, vertical=False, hide_nested=True, rings=RINGS):
    """Only rings 1..`rings` are read - the rings the main word occupies. The others are switched off."""
    """Return a list of occurrences: dict(word, tier, kind, dir, arrow, cells=[(r,c),...])."""
    dirs = []
    for d in DIRECTIONS:
        if (d[2] == 0 and horizontal) or (d[2] != 0 and diagonal):
            dirs.append(d)
    if vertical:
        dirs.extend(VERTICAL)

    found, seen = [], set()
    for r in range(ROWS):
        for c in range(rings):
            for name, arrow, dr, dc, kind in dirs:
                for length in range(max(3, min_len), RINGS + 1):
                    end_c = c + dc * (length - 1)
                    if not 0 <= end_c < rings:
                        break
                    cells = tuple(((r + dr * k) % ROWS, c + dc * k) for k in range(length))
                    word = "".join(grid[rr][cc] for rr, cc in cells)
                    tier = lookup.get(word)
                    if not tier:
                        continue
                    key = (word, frozenset(cells))  # palindromes: keep only one reading
                    if key in seen:
                        continue
                    seen.add(key)
                    found.append({"word": word, "tier": tier, "kind": kind, "dir": name,
                                  "arrow": arrow, "cells": list(cells)})

    if hide_nested:
        sets = [set(o["cells"]) for o in found]
        keep = []
        for i, o in enumerate(found):
            if not any(len(sets[j]) > len(sets[i]) and sets[i] < sets[j] for j in range(len(found))):
                keep.append(o)
        found = keep
    return found


def rank_key(word, tier):
    return (TIER_RANK.get(tier, 9), -len(word), word)


def group_words(found, kind, meanings=None):
    """Unique words of one kind, best first: list of (word, tier, [occurrences]).
    With meanings given, words that have a definition rank above words that don't."""
    groups = {}
    for o in found:
        if o["kind"] == kind:
            groups.setdefault(o["word"], []).append(o)
    out = [(w, occ[0]["tier"], occ) for w, occ in groups.items()]

    def key(g):
        k = rank_key(g[0], g[1])
        if meanings is not None:
            lines = explain(g[0], meanings)["lines"]
            if not lines:
                k = (k[0] + 3,) + k[1:]
            elif lines[0][0] == "1913":  # only an old Webster meaning
                k = (k[0] + 1,) + k[1:]
        return k
    out.sort(key=key)
    return out


# ---------------------------------------------------------------- reading
def numerology(word):
    total = sum(PYTHAGOREAN_VALUES.get(c, 0) for c in word)
    while total > 9:
        total = sum(int(d) for d in str(total))
    title, desc, guide = NUMEROLOGY_THEMES.get(
        total, ("The Seeker", "Mysterious potential.", "Follow your intuition and listen to the wisdom of the cylinder."))
    return total, title, desc, guide


def synthesis(main_word, gifts, intents, num_desc, meanings=None):
    g = [w for w, _, _ in gifts if w != main_word][:6]   # the aligned word itself isn't a gift
    i = [w for w, _, _ in intents if w != main_word][:6]

    def gloss(w):
        if not meanings:
            return ""
        m = short_meaning(explain(w, meanings))
        return f" ({m})" if m else ""

    parts = []
    if g:
        parts.append(f"The cylinder offers its GIFTS around {main_word}: {', '.join(g)}. "
                     f"{g[0]}{gloss(g[0])} is the strongest gift being handed to you.")
    if i:
        parts.append(f"Read backward, it reveals the INTENT moving beneath: {', '.join(i)}. "
                     f"{i[0]}{gloss(i[0])} is the will behind this turn of the rings.")
    if g and i:
        parts.append(f"Hold {g[0]} (what is given) together with {i[0]} (what is meant), "
                     f"and let {main_word} guide you toward {num_desc[0].lower() + num_desc[1:]}")
    if not parts:
        parts.append(f"{main_word} stands in solitary focus - no other words echo around it. "
                     f"Its core archetype speaks alone: {num_desc[0].lower() + num_desc[1:]}")
    return " ".join(parts)


# ---------------------------------------------------------------- printable text file
def _ascii(s):
    s = s.replace("—", "-").replace("–", "-").replace("’", "'").replace("•", "*").replace("…", "...")
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")


def _wrap(text, width=76, indent="  "):
    words, lines, cur = _ascii(text).split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width:
            lines.append(indent + cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur:
        lines.append(indent + cur)
    return lines


def _grid_lines(grid, active_len, show=None):
    """Fixed-width grid. Every letter sits in its own 3-character column."""
    lines = ["   ROW    |  1  2  3  4  5  6  |",
             "  --------+--------------------+"]
    for r in range(ROWS):
        lab = row_label(r)
        lab = ">> MAIN" if lab == "MAIN" else lab
        cells = ""
        for c in range(RINGS):
            ch = grid[r][c]
            if show is not None and (r, c) not in show:
                ch = "."
            elif c >= active_len and show is None:
                ch = ch.lower()
            cells += f"  {ch}"
        lines.append(f"  {lab:>7} |{cells}  |")
    return lines


def build_text_report(main_word, active_len, grid, found, gifts, intents, num, settings, meanings=None, reading=None):
    total, title, desc, guide = num
    W = 78
    bar, thin = "=" * W, "-" * W
    gift_cells = {cell for o in found if o["kind"] == "gift" for cell in o["cells"]}
    intent_cells = {cell for o in found if o["kind"] == "intent" for cell in o["cells"]}

    L = [bar, "  CRYPTEX WERD  -  CYLINDER ORACLE READING", bar,
         f"  Timestamp      : {time.strftime('%Y-%m-%d %H:%M:%S')}",
         f"  Main word      : {main_word}  ({active_len} letters)",
         f"  Vibration      : {total} - {title}",
         ]
    sw = _wrap(settings, width=57, indent="")
    L += [f"  Search         : {sw[0] if sw else ''}"] + [" " * 19 + x for x in sw[1:]]
    L += ["", "  Letter values:"]
    for c in main_word:
        L.append(f"    {c} = {PYTHAGOREAN_VALUES.get(c, 0)}   {LETTER_MEANINGS.get(c, '')}")
    L += ["", "  Essence:"] + _wrap(desc, indent="    ") + ["", "  Guidance:"] + _wrap(guide, indent="    ")

    L += ["", bar, "  1. THE FULL CYLINDER  (26 rows x 6 rings, unrolled)", bar,
          "  The main row is marked >> MAIN. Lowercase letters are rings outside",
          "  the aligned word - they are switched off and not read.", ""]
    L += _grid_lines(grid, active_len)

    L += ["", bar, "  2. GIFT MAP  (forward words: read left to right)", bar,
          "  Only letters that belong to a GIFT word are shown.", ""]
    L += _grid_lines(grid, active_len, show=gift_cells)

    L += ["", bar, "  3. INTENT MAP  (backward words: read right to left)", bar,
          "  Only letters that belong to an INTENT word are shown.", ""]
    L += _grid_lines(grid, active_len, show=intent_cells)

    def word_table(groups, heading, kind):
        out = ["", bar, heading, bar]
        if not groups:
            return out + ["  (none found)"]
        for w, tier, occ in groups:
            n, t, _ = numerology(w)[:3]
            out.append("")
            out.append(f"  {w:<8} vibration {n} - {t}   |   source: {_ascii(TIER_LABEL.get(tier, tier))}")
            for o in occ:
                r0, c0 = o["cells"][0]
                where = f"starts row {row_label(r0)}, ring {c0 + 1}, reads {o['dir']}"
                if kind == "intent":
                    letters = "".join(grid[r][c] for r, c in sorted(o["cells"], key=lambda rc: rc[1]))
                    where += f"  (on the rings: {letters})"
                out.append(f"    - {where}")
            if meanings:
                info = explain(w, meanings)
                if info["base"]:
                    out.append(f"    form of: {info['base']}")
                if info["lines"]:
                    for label, text in info["lines"]:
                        out += _wrap(f"{label}: {text}", width=72, indent="    ")
                else:
                    out.append("    meaning: (valid word - no definition on file)")
        return out

    L += word_table(gifts, f"  4. GIFTS - {len(gifts)} forward word(s) - what is given", "gift")
    L += word_table(intents, f"  5. INTENTS - {len(intents)} backward word(s) - the will beneath", "intent")

    L += ["", bar, "  6. THE ORACLE READING", bar]
    if reading:
        for head, paras in reading:
            if head == "The reading in brief":
                L += ["", "  THE READING IN BRIEF", "  " + "-" * 20] + _wrap(paras[0], width=74) + [""]
                continue
            L += ["", f"  {_ascii(head).upper()}", "  " + "-" * min(len(_ascii(head)), 74)]
            for para in paras:
                L += _wrap(para, width=74) + [""]
    else:
        L += _wrap(synthesis(main_word, gifts, intents, desc, meanings))
    L += [bar, ""]
    return "\n".join(_ascii(x) for x in L)


# ---------------------------------------------------------------- printable HTML page
def build_print_html(main_word, active_len, grid, found, gifts, intents, num, meanings=None, reading=None):
    total, title, desc, guide = num
    gift_cells = {cell for o in found if o["kind"] == "gift" for cell in o["cells"]}
    intent_cells = {cell for o in found if o["kind"] == "intent" for cell in o["cells"]}
    rows = []
    for r in range(ROWS):
        tds = ""
        for c in range(RINGS):
            cls = []
            if (r, c) in gift_cells:
                cls.append("g")
            if (r, c) in intent_cells:
                cls.append("i")
            if r == CENTER:
                cls.append("m" if c < active_len else "mo")
            elif c >= active_len:
                cls.append("mo")
            tds += f'<td class="{" ".join(cls)}">{grid[r][c]}</td>'
        lab = row_label(r)
        rows.append(f'<tr><th>{"&#9658; MAIN" if lab == "MAIN" else lab}</th>{tds}</tr>')

    def tbl(groups):
        if not groups:
            return "<p><i>None found.</i></p>"
        trs = ""
        for w, t, occ in groups:
            n, title_w, _ = numerology(w)[:3]
            where = "<br>".join(f"{o['arrow']} {o['dir'].lower()} from row {row_label(o['cells'][0][0])}, ring {o['cells'][0][1] + 1}"
                                for o in occ)
            mean = ""
            if meanings:
                info = explain(w, meanings)
                mean = "<br>".join(f"<i>{html.escape(l)}</i> {html.escape(x)}" for l, x in info["lines"]) or "<i>no definition on file</i>"
                if info["base"]:
                    mean = f"<small>form of {info['base']}</small><br>" + mean
            trs += (f"<tr><td><b>{w}</b><br><small>{n} &middot; {html.escape(title_w)}</small></td>"
                    f"<td>{mean}</td><td><small>{where}<br>{html.escape(TIER_LABEL.get(t, t))}</small></td></tr>")
        return f"<table class='list'><tr><th>Word</th><th>Meaning</th><th>Where</th></tr>{trs}</table>"

    if reading:
        reading_html = "".join((f"<div style='border:2px solid #00a37a;border-radius:10px;padding:8px 14px;margin:8px 0'>"
                                f"<b>The reading in brief</b><p style='font-size:17px'>{html.escape(ps[0])}</p></div>")
                               if h == "The reading in brief" else
                               f"<h3>{html.escape(h)}</h3>" + "".join(f"<p>{html.escape(x)}</p>" for x in ps)
                               for h, ps in reading)
    else:
        reading_html = (f"<p><b>{title}:</b> {html.escape(desc)}</p><p>{html.escape(guide)}</p>"
                        f"<p>{html.escape(synthesis(main_word, gifts, intents, desc, meanings))}</p>")
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><title>Cryptex werd - {main_word}</title>
<style>
body{{font-family:Helvetica,Arial,sans-serif;color:#111;max-width:760px;margin:24px auto;padding:0 16px}}
h1{{letter-spacing:4px;margin:0}} h3{{margin:18px 0 4px 0;color:#00775a}} p{{line-height:1.5}} h1 .x{{font-size:1.6em;color:#00a37a}}
.grid{{border-collapse:collapse;margin:12px 0}}
.grid td{{width:34px;height:34px;text-align:center;font:700 20px "Courier New",monospace;border:1px solid #bbb}}
.grid th{{font:600 12px monospace;padding-right:8px;text-align:right;color:#555}}
.grid td.g{{background:#c8f7e6}} .grid td.i{{background:#f7c8ee}} .grid td.g.i{{background:linear-gradient(135deg,#c8f7e6 50%,#f7c8ee 50%)}}
.grid td.m{{outline:3px solid #000;outline-offset:-3px}} .grid td.mo{{color:#999}}
.list{{border-collapse:collapse;width:100%;font-size:13px}} .list td,.list th{{border-bottom:1px solid #ddd;padding:5px 6px;text-align:left;vertical-align:top}} .list tr{{page-break-inside:avoid}}
.key span{{display:inline-block;padding:2px 8px;margin-right:6px;border:1px solid #999}}
@media print{{ .grid td{{-webkit-print-color-adjust:exact;print-color-adjust:exact}} }}
</style></head><body>
<h1>CRYPTE<span class="x">X</span> WERD</h1>
<p><b>Main word:</b> {main_word} &nbsp; <b>Vibration:</b> {total} - {title}<br><small>{time.strftime('%Y-%m-%d %H:%M:%S')}</small></p>
<p class="key"><span style="background:#c8f7e6">GIFT &mdash; forward</span><span style="background:#f7c8ee">INTENT &mdash; backward</span><span style="outline:3px solid #000">Main row</span></p>
<table class="grid">{''.join(rows)}</table>
<h2>The Oracle Reading</h2>{reading_html}
<h2>Gifts ({len(gifts)})</h2>{tbl(gifts)}
<h2>Intents ({len(intents)})</h2>{tbl(intents)}

</body></html>"""
