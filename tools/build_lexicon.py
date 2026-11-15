"""Rebuild the Cryptex word lists from open-source sources.

Usage:
    python tools/build_lexicon.py ENABLE1 POPULAR WORDS_ALPHA SWEARS_ALL SWEARS_CLEAN

  ENABLE1      enable1.txt        (github.com/dolph/dictionary — public domain)
  POPULAR      popular.txt        (github.com/dolph/dictionary)
  WORDS_ALPHA  words_alpha.txt    (github.com/dwyl/english-words — public domain)
  SWEARS_ALL   google-10000-english.txt            (github.com/first20hours/google-10000-english)
  SWEARS_CLEAN google-10000-english-no-swears.txt  (same repo)

Writes lexicon/common.txt, dictionary.txt, deep.txt and clean_filter.txt.
slang.txt and mystic.txt are hand-written and never overwritten.
"""
import os
import re
import sys

WORD = re.compile(r"[A-Z]{3,6}")
VOWEL = re.compile(r"[AEIOUY]")


def load(path):
    out = set()
    with open(path, encoding="utf-8", errors="ignore") as f:
        for line in f:
            w = line.strip().upper()
            if WORD.fullmatch(w):
                out.add(w)
    return out


def write(path, words, header):
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# {header}\n")
        for w in sorted(words):
            f.write(w + "\n")
    print(f"{os.path.basename(path)}: {len(words):,} words")


def main():
    enable, popular, alpha, g_all, g_clean = (load(p) for p in sys.argv[1:6])
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lexicon")
    common = popular & enable
    dictionary = enable - common
    deep = {w for w in alpha - enable if VOWEL.search(w)}
    swears = g_all - g_clean
    write(os.path.join(out, "common.txt"), common, "Everyday English (popular.txt ∩ ENABLE)")
    write(os.path.join(out, "dictionary.txt"), dictionary, "Full ENABLE Scrabble dictionary, minus common words")
    write(os.path.join(out, "deep.txt"), deep, "Rare/obscure words, abbreviations & names (dwyl english-words, not in ENABLE)")
    write(os.path.join(out, "clean_filter.txt"), swears, "Words hidden when Clean mode is ON")


if __name__ == "__main__":
    main()
