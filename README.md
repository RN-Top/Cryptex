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
- **Clean mode** — one switch hides swears and adult words.
- **Hide nested words** — keeps EAR from cluttering the list when HEART is found (can be turned off).
- **Ring dials** — ▲ / ▼ for each ring, side by side even on a phone.
- **Random Spin** and **Align Word** (type up to 6 letters, press Enter).
- **Oracle reading** — Pythagorean vibration (1–9) of the main word, letter meanings, gifts, intents and a synthesis.
- **Save & print**
  - **Text file (.txt)** — every letter in its own fixed-width column, so the grid lines up when printed. Includes the full cylinder, a GIFT map, an INTENT map and tables of every word with its direction, start row and ring.
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
├── lexicon/
│   ├── common.txt          # Everyday English
│   ├── mystic.txt          # Mystic, myth, titles & names   ← hand-written, add your own
│   ├── slang.txt           # Slang & internet speak         ← hand-written, add your own
│   ├── crude.txt           # Crude & adult slang            ← hand-written, add your own
│   ├── dictionary.txt      # Full ENABLE Scrabble dictionary
│   ├── deep.txt            # Rare words, abbreviations & names
│   └── clean_filter.txt    # Extra words hidden by Clean mode
├── tools/build_lexicon.py  # Rebuilds the generated word lists from their sources
├── .streamlit/config.toml  # Dark neon theme
└── requirements.txt
```

**Adding words:** open `lexicon/slang.txt`, `mystic.txt` or `crude.txt` and add one word per line (3–6 letters). Lines starting with `#` are notes and are ignored.

---

## 📚 Word-list credits

- **ENABLE** word list — public domain, via [dolph/dictionary](https://github.com/dolph/dictionary)
- **popular.txt** (common-word subset of ENABLE + Wiktionary frequency lists) — [dolph/dictionary](https://github.com/dolph/dictionary)
- **english-words** — public domain (Unlicense), [dwyl/english-words](https://github.com/dwyl/english-words)
- Clean-mode list derived from [first20hours/google-10000-english](https://github.com/first20hours/google-10000-english)
- Slang, mystic and crude lists written for this project

Original device: **Drew**. App: **Erin Rae Toppe** ([RN-Top](https://github.com/RN-Top)).
