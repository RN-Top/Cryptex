"""Build lexicon/definitions.tsv from the Open English WordNet (CC BY 4.0, based on Princeton WordNet).

Usage:  python tools/build_definitions.py PATH/TO/english-wordnet/src/yaml [PATH/TO/webster/dictionary.json]

Get the data:
  git clone --depth 1 https://github.com/globalwordnet/english-wordnet          (CC BY 4.0)
  git clone --depth 1 https://github.com/matthewreagan/WebstersEnglishDictionary (Webster's 1913, public domain)
Webster's is used only for words WordNet doesn't have; those meanings are tagged "1913".

Output lines:
    WORD <tab> pos <tab> definition [<tab> pos <tab> definition]   (most common meaning first)
    WORD <tab> =BASE      (WORD is a form of BASE, e.g. DOGS -> =DOG)
"""
import glob
import json
import os
import re
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "..", "lexicon")
WORD = re.compile(r"[a-z]{3,6}")
POS = {"n": "noun", "v": "verb", "a": "adj", "s": "adj", "r": "adv"}

try:
    Loader = yaml.CSafeLoader
except AttributeError:
    Loader = yaml.SafeLoader


def lex_words():
    words = set()
    for name in ("common", "dictionary", "deep", "slang", "mystic", "crude"):
        with open(os.path.join(LEX, f"{name}.txt"), encoding="utf-8") as f:
            words |= {l.strip() for l in f if l.strip() and not l.startswith("#")}
    return words


def candidates(w):
    out = []
    for suf, rep in [("IES", "Y"), ("IED", "Y"), ("IER", "Y"), ("IEST", "Y"), ("ES", ""), ("S", ""),
                     ("ED", ""), ("ED", "E"), ("ING", ""), ("ING", "E"), ("ER", ""), ("ER", "E"),
                     ("EST", ""), ("EST", "E"), ("LY", ""), ("D", "")]:
        if w.endswith(suf) and len(w) - len(suf) >= 2:
            out.append(w[: -len(suf)] + rep)
    m = re.match(r"^(.*?)(.)\2(ED|ING|ER|EST)$", w)
    if m:
        out.append(m.group(1) + m.group(2))
    return out


def clean(s, n=150):
    s = re.sub(r"\s+", " ", str(s).replace("\t", " ")).strip()
    return s if len(s) <= n else s[: n - 1].rsplit(" ", 1)[0] + "…"


def main():
    src = sys.argv[1]
    synsets = {}
    for path in glob.glob(os.path.join(src, "*.yaml")):
        base = os.path.basename(path)
        if base.startswith(("noun.", "verb.", "adj.", "adv.")):
            with open(path, encoding="utf-8") as f:
                for sid, s in (yaml.load(f, Loader=Loader) or {}).items():
                    if s.get("definition"):
                        synsets[sid] = s["definition"][0]

    defs = {}  # WORD -> list of (pos, definition), most common first
    for path in sorted(glob.glob(os.path.join(src, "entries-*.yaml"))):
        with open(path, encoding="utf-8") as f:
            for lemma, by_pos in (yaml.load(f, Loader=Loader) or {}).items():
                lemma = str(lemma)
                if not WORD.fullmatch(lemma):  # lowercase only: skips proper nouns like "Love"
                    continue
                groups = []
                for p, entry in by_pos.items():
                    senses = [s for s in entry.get("sense", []) if s.get("synset") in synsets]
                    if senses:
                        groups.append((len(senses), POS.get(p, p), synsets[senses[0]["synset"]]))
                groups.sort(key=lambda g: -g[0])  # the part of speech with the most senses first
                picked, seen = [], set()
                for _, p, d in groups:
                    if p not in seen:
                        picked.append((p, clean(d)))
                        seen.add(p)
                if picked:
                    defs[lemma.upper()] = picked[:2]

    webster = {}
    if len(sys.argv) > 2:
        with open(sys.argv[2], encoding="utf-8") as f:
            for k, v in json.load(f).items():
                if WORD.fullmatch(k) and v:
                    first = re.split(r"(?<=[.;])\s+(?=[A-Z0-9])|\s+\d+\.\s+", re.sub(r"^\s*1\.\s*", "", v.strip()))[0]
                    webster[k.upper()] = clean(first.rstrip(".;"), 140)

    lines, direct, linked, old = [], 0, 0, 0
    for w in sorted(lex_words()):
        if w in defs:
            lines.append("\t".join([w] + [x for pair in defs[w] for x in pair]))
            direct += 1
        else:
            base = next((c for c in candidates(w) if c in defs), None)
            if base:
                lines.append(f"{w}\t={base}")
                linked += 1
            elif w in webster:
                lines.append(f"{w}\t1913\t{webster[w]}")
                old += 1
    with open(os.path.join(LEX, "definitions.tsv"), "w", encoding="utf-8") as f:
        f.write("# Definitions from Open English WordNet (CC BY 4.0, en-word.net), derived from Princeton WordNet 3.0;\n")
        f.write("# entries tagged 1913 are from Webster's Unabridged Dictionary (1913, public domain, via Project Gutenberg)\n")
        f.write("\n".join(lines) + "\n")
    print(f"definitions.tsv: {direct:,} from WordNet, {old:,} from Webster 1913, {linked:,} linked to a base word")


if __name__ == "__main__":
    main()
