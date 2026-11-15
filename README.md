# 🗝️ CRYPTE**X** WERD — Drew's 6-Ring Cylinder Cipher & Oracle

A neon, dark-mode web app that recreates Drew's physical 6-ring brass cipher cylinder. Spin or dial the rings, and the app searches the **whole cylinder face** — all 26 rows, forward, backward and diagonally — for hidden words from a vocabulary of about **56,000 words**, then gives a Pythagorean numerology reading.

Built with [Streamlit](https://streamlit.io/).

---

## 🌟 The device

Drew built the original mechanical cylinder: six brass rings, each wrapped in a hand-lettered strip, in the tradition of Thomas Jefferson's wheel cipher and the Da Vinci cryptex.

Every ring carries the same 26 letters in the **9-column Pythagorean reduction order** — the alphabet written in nine columns (1–9) and read down each column:

```
1 2 3 4 5 6 7 8 9
A B C D E F G H I
J K L M N O P Q R
S T U V W X Y Z

Ring order:  A J S  B K T  C L U  D M V  E N W  F O X  G P Y  H Q Z  I R
```

When a word is dialed onto the main row, the other 25 rows around the cylinder line up in fixed offsets, and hidden words appear across them.

---

## ✨ Features

- **Neon cylinder face** — all 26 rows unrolled, the main row glowing in the middle. Tap any found word to light up its path.
- **Search in every direction**
  - ◆ **GIFTS** (mint) — words read *forward*, left → right: → ↘ ↗
  - ◇ **INTENTS** (magenta) — words read *backward*, right → left: ← ↖ ↙
  - Optional vertical ↓ ↑ search
  - The cylinder wraps around, so diagonals continue from the bottom row to the top, just like the real rings.
- **Huge vocabulary (3–6 letters)** — switch each source on or off:
  | Source | Words | Default |
  |---|---|---|
  | Everyday English | ~9,800 | on |
  | Mystic, myth, titles & names (Mrs, Sir, Odin, Isis, Tarot, Sigil…) | ~350 | on |
  | Slang & internet speak (rizz, slay, vibe, bussin, yeet…) | ~270 | on |
  | Crude & adult slang | ~70 | on |
  | Full Scrabble dictionary (ENABLE) | ~18,900 | on |
  | Deep lexicon — rare words, abbreviations, names | ~26,700 | off |
- **What every word means** — tap any word for a pop-up card, and the reading lists every Gift and Intent with:
  - its meaning in plain English (slang, mystic, name and title meanings written for this app, then the dictionary meaning)
  - its own Pythagorean vibration and archetype
  - exactly where it sits (direction, starting row and ring) — Intents also show how they look on the rings left to right
  - about 85% of words found on a typical spin have a meaning; the rest are rare Scrabble words
- **Clean mode** — one switch hides swears and adult words.
- **Hide nested words** — keeps EAR from cluttering the list when HEART is found (can be turned off).
- **Ring dials** — ▲ / ▼ for each ring, side by side even on a phone.
- **Random Spin** and **Align Word** (type up to 6 letters, press Enter).
- **The Oracle Reading** — a long, detailed reading (often 1,000–1,600 words) written from *this exact turn of the rings*. Change one ring and the whole reading changes; the same position always gives the same reading. It has eight parts:
  1. **The aligned word** — its meaning, vibration, keystone and seal letters, repeating and missing numbers, and a letter-by-letter story
  2. **The shape of this turn** — Gifts vs Intents balance, straight vs diagonal, the voice of the words (sacred, street, old), and the busiest ring
  3. **The Gifts** — the strongest forward words, each with its meaning, where it sits (arriving above the line or rooted below it), how it moves, and how its number meets the main word's
  4. **The Intents** — the same for backward words, plus how each looks on the rings before it's reversed
  5. **Mirrors, branches and crossroads** — the same letters read both ways, words growing out of the main word, and letters where Gifts and Intents cross
  6. **Above and below the line** — what is arriving vs what is rooted
  7. **The numbers** — the Gift number, the Intent number and the number of the whole reading
  8. **Counsel** — guidance, a question to carry with you, and the reading "in one breath"
- **Save & print**
  - **Text file (.txt)** — every letter in its own fixed-width column, so the grid lines up when printed. Includes the full cylinder, a GIFT map, an INTENT map, and every word with its meaning, vibration, direction, start row and ring.
  - **Printable page (.html)** — open in a browser and print or Save as PDF; colored, ink-friendly grid.
  - **Reading log** — save readings during your session and download them as a .txt.

---

## 🚀 Run it on your computer

```bash
git clone https://github.com/RN-Top/Cryptex.git
cd Cryptex
pip install -r requirements.txt
streamlit run app.py
```

It opens at `http://localhost:8501`.

## ☁️ Deploy free on Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io/) and sign in with GitHub.
2. **New app** → repository `RN-Top/Cryptex`, branch `main`, main file `app.py`.
3. **Deploy**. The neon theme is set in `.streamlit/config.toml` and loads automatically.

---

## 📁 Files

```
Cryptex/
├── app.py                  # Streamlit interface (neon theme, dials, cylinder face, downloads)
├── cryptex_core.py         # Word search, readings and printable reports (no Streamlit needed)
├── cryptex_reading.py      # The individualized Oracle reading
├── lexicon/
│   ├── common.txt          # Everyday English
│   ├── mystic.txt          # Mystic, myth, titles & names   ← hand-written, add your own
│   ├── slang.txt           # Slang & internet speak         ← hand-written, add your own
│   ├── crude.txt           # Crude & adult slang            ← hand-written, add your own
│   ├── dictionary.txt      # Full ENABLE Scrabble dictionary
│   ├── deep.txt            # Rare words, abbreviations & names
│   ├── clean_filter.txt    # Extra words hidden by Clean mode
│   ├── glosses.txt         # Hand-written meanings (slang, mystic, names, titles, crude)  ← add your own
│   └── definitions.tsv     # Dictionary meanings (WordNet + Webster 1913)
├── tools/build_lexicon.py  # Rebuilds the generated word lists from their sources
├── tools/build_definitions.py  # Rebuilds definitions.tsv
├── .streamlit/config.toml  # Dark neon theme
└── requirements.txt
```

**Adding words:** open `lexicon/slang.txt`, `mystic.txt` or `crude.txt` and add one word per line (3–6 letters). Lines starting with `#` are notes and are ignored.

**Adding meanings:** open `lexicon/glosses.txt` and add a line like `RIZZ | slang | charm, the ability to attract someone`. Your meanings show up before the dictionary's.

---

## 📚 Word-list credits

- **ENABLE** word list — public domain, via [dolph/dictionary](https://github.com/dolph/dictionary)
- **popular.txt** (common-word subset of ENABLE + Wiktionary frequency lists) — [dolph/dictionary](https://github.com/dolph/dictionary)
- **english-words** — public domain (Unlicense), [dwyl/english-words](https://github.com/dwyl/english-words)
- Clean-mode list derived from [first20hours/google-10000-english](https://github.com/first20hours/google-10000-english)
- Definitions: [Open English WordNet](https://github.com/globalwordnet/english-wordnet) (CC BY 4.0), derived from Princeton WordNet 3.0 — © Princeton University and the Open English Wordnet team
- Older definitions (tagged "1913"): Webster's Unabridged Dictionary, public domain, via Project Gutenberg / [matthewreagan/WebstersEnglishDictionary](https://github.com/matthewreagan/WebstersEnglishDictionary)
- Slang, mystic and crude lists and their meanings written for this project

Original device: **Drew**. App: **Erin Rae Toppe** ([RN-Top](https://github.com/RN-Top)).
