"""The individualized Oracle reading for Cryptex werd.

Everything here is built from what is actually on the cylinder for this turn of the rings:
the aligned word and its meaning, each Gift and Intent with its meaning, where each word sits
(above or below the main line, which way it reads), words that mirror each other, words that
branch out of the main word, letters where Gifts and Intents cross, and the numbers of the
Gifts, the Intents and the whole reading.

Phrasing is varied with a random generator seeded by the ring positions, so the same position
always gives the same reading, and every different position gives a different one.
"""
import hashlib
import random
import re
from collections import Counter

import cryptex_core as C

# ------------------------------------------------------------------ reference tables
NUMBER_NAME = {n: t[0] for n, t in C.NUMEROLOGY_THEMES.items()}
NUMBER_KEY = {
    1: "beginning", 2: "partnership", 3: "expression", 4: "foundation", 5: "change",
    6: "care", 7: "inner truth", 8: "power", 9: "completion",
}
NUMBER_QUESTIONS = {
    1: ["What would you start today if no one had to approve it?",
        "Where are you waiting for permission you don't actually need?"],
    2: ["Who is the quiet partner in this - and have you listened to them?",
        "What balance are you being asked to restore?"],
    3: ["What have you been holding back from saying out loud?",
        "Where would joy, not effort, carry you farther?"],
    4: ["What foundation needs one more steady stone before you build higher?",
        "Which habit, kept daily, would change everything in a year?"],
    5: ["What are you ready to let change, even though it feels unfamiliar?",
        "Where is a door open that you keep walking past?"],
    6: ["Who needs your care - and are you on that list yourself?",
        "What boundary would make your love stronger, not smaller?"],
    7: ["What do you already know, deep down, that you haven't admitted yet?",
        "What would the quiet hour tell you if you gave it room?"],
    8: ["What would you claim if you trusted your own authority?",
        "Where is your power leaking out, and where should it go instead?"],
    9: ["What chapter is asking you to close it with grace?",
        "What can you forgive so you can move on lighter?"],
}
PAIR_HARMONY = {  # how two numbers sit together
    0: "the same note sounding twice - a strong, focused signal",
    1: "neighbors on the scale - they step naturally from one into the other",
    2: "a third apart - they color each other",
    3: "a fourth apart - they stretch the reading wider",
    4: "nearly opposite - they pull against each other and make you choose",
}


def reduce_num(n):
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n


def word_num(w):
    return reduce_num(sum(C.PYTHAGOREAN_VALUES.get(c, 0) for c in w))


def harmony(a, b):
    d = abs(a - b)
    return PAIR_HARMONY[min(d, 9 - d, 4)]


def join_words(ws):
    ws = list(ws)
    if not ws:
        return ""
    if len(ws) == 1:
        return ws[0]
    return ", ".join(ws[:-1]) + " and " + ws[-1]


def lower_first(s):
    return s[0].lower() + s[1:] if s else s


def strip_end(s):
    return s.rstrip(" .;")


def lm(ch):
    """Letter meaning, all lowercase, for use mid-sentence."""
    return C.LETTER_MEANINGS[ch].lower()


def end(s):
    """Finish a clause with a period unless it already ends in punctuation."""
    s = s.rstrip()
    return s if s.endswith((".", "!", "?", "...")) else s + "."


# ------------------------------------------------------------------ helpers about placement
def placement(o):
    """Plain-language description of where a word sits and how it moves."""
    rows = [r - C.CENTER for r, _ in o["cells"]]
    avg = sum(rows) / len(rows)
    touches_main = any(r == C.CENTER for r, _ in o["cells"])
    if touches_main and all(r == C.CENTER for r, _ in o["cells"]):
        where = "on the main line itself - it is present right now"
    elif touches_main:
        where = "growing straight out of the main line"
    elif avg < 0:
        dist = abs(round(avg))
        where = ("just above the main line - arriving very soon" if dist <= 3 else
                 "above the main line - on its way to you" if dist <= 7 else
                 "high above the main line - far off, still forming")
    else:
        dist = abs(round(avg))
        where = ("just beneath the main line - close to the root of things" if dist <= 3 else
                 "below the main line - in the foundations" if dist <= 7 else
                 "deep below the main line - an old root, from long ago")
    motion = {
        "RIGHT": "reading straight forward", "LEFT": "reading straight back",
        "DOWN-RIGHT": "descending as it moves forward - bringing something down into form",
        "UP-RIGHT": "climbing as it moves forward - rising into being",
        "UP-LEFT": "climbing backward - a motive reaching up from below",
        "DOWN-LEFT": "sinking backward - a motive settling into the depths",
        "DOWN": "falling straight down the ring", "UP": "rising straight up the ring",
    }[o["dir"]]
    return where, motion, avg


def meaning_of(w, meanings, n=110):
    info = C.explain(w, meanings)
    if not info["lines"]:
        return None, info
    label, text = info["lines"][0]
    text = strip_end(re.sub(r"^\([^)]*\)\s*", "", text))
    if len(text) > n:
        text = text[: n - 1].rsplit(" ", 1)[0] + "..."
    return (label, text), info


def describe_meaning(w, meanings):
    m, info = meaning_of(w, meanings)
    if not m:
        return f"{w} is an old, rare word with no common meaning - its message is carried by its letters and its number"
    label, text = m
    base = f" (a form of {info['base']})" if info["base"] else ""
    if label in ("slang", "crude"):
        return f"{w}{base} - in street speech, {lower_first(text)}"
    if label in ("mystic",):
        return f"{w}{base} - {lower_first(text)}"
    if label == "name":
        return f"{w} - a name; {text}"
    if label == "title":
        return f"{w} - a title: {lower_first(text)}"
    if label == "1913":
        return f"{w}{base} - an old word: {lower_first(text)}"
    return f"{w}{base} - {lower_first(text)}"


# ------------------------------------------------------------------ the reading
def build_reading(main_word, active_len, offsets, grid, found, gifts, intents, meanings):
    """Return a list of (heading, [paragraphs]) for this exact turn of the rings."""
    seed = int(hashlib.md5(f"{offsets}|{active_len}|{len(found)}".encode()).hexdigest(), 16)
    rng = random.Random(seed)
    pick = rng.choice
    sections = []

    main_n, main_title, main_desc, main_guide = C.numerology(main_word)
    gifts = [g for g in gifts if g[0] != main_word]
    intents = [i for i in intents if i[0] != main_word]
    occ_of = {}
    for o in found:
        occ_of.setdefault((o["word"], o["kind"]), []).append(o)

    # 1. The aligned word -------------------------------------------------------------
    m, info = meaning_of(main_word, meanings)
    p = []
    if m:
        p.append(pick([
            f"The rings have locked on {main_word}. In plain words, {main_word} means {lower_first(m[1])}.",
            f"{main_word} sits on the main line. Its everyday meaning: {lower_first(m[1])}.",
            f"The cylinder has been turned to {main_word} - {lower_first(m[1])}.",
        ]))
    else:
        p.append(pick([
            f"The rings have locked on {main_word}. It is not a dictionary word, so it speaks only through its letters and numbers - like a sigil.",
            f"{main_word} sits on the main line - not a word any dictionary knows, which makes it a cipher of its own. Read it letter by letter.",
        ]))
    p.append(f"Its letters add to vibration {main_n}, {main_title}: {lower_first(main_desc)}")
    letters = list(main_word)
    nums = [C.PYTHAGOREAN_VALUES[c] for c in letters]
    p.append(f"The first letter, {letters[0]} ({lm(letters[0])}), is the keystone - it opens the reading. "
             f"The last, {letters[-1]} ({lm(letters[-1])}), is the seal - it is how this closes.")
    cnt = Counter(nums)
    top_n, top_c = cnt.most_common(1)[0]
    if top_c >= 2:
        which = [c for c in letters if C.PYTHAGOREAN_VALUES[c] == top_n]
        p.append(f"The number {top_n} ({NUMBER_KEY[top_n]}) repeats {top_c} times in it, through {join_words(which)} - "
                 f"so {NUMBER_KEY[top_n]} is the undertone of everything that follows.")
    missing = [n for n in range(1, 10) if n not in nums]
    if missing and len(letters) >= 4:
        p.append(f"Missing from the word entirely: {join_words(str(n) for n in missing)} "
                 f"({join_words(NUMBER_KEY[n] for n in missing)}). "
                 + pick(["Those are the qualities you'll have to bring yourself.",
                         "What the word lacks, the surrounding rings may have to supply.",
                         "Notice whether the Gifts and Intents below fill those gaps."]))
    walk = " -> ".join(f"{c} ({lm(c)})" for c in letters)
    p.append(f"Walked letter by letter, {main_word} tells a small story: {walk}.")
    sections.append((f"The aligned word - {main_word}", p))

    # 2. The shape of this turn ---------------------------------------------------------
    p = []
    ng, ni = len(gifts), len(intents)
    total = ng + ni
    if total == 0:
        p.append("The cylinder is silent around the main word - no other words formed on this turn. "
                 "A silent cylinder is a reading of its own: it asks you to sit with the main word alone and not look for outside signs.")
    else:
        if ng > ni * 1.5:
            tone = pick(["This is a generous turn: far more is being offered than asked of you.",
                         "Gifts outnumber Intents - a season of receiving. Your job is to notice and accept."])
        elif ni > ng * 1.5:
            tone = pick(["This turn leans inward: the Intents outweigh the Gifts. Motive matters more than outcome right now.",
                         "More is moving under the surface than on it - Intents outnumber Gifts. Look at why, not just what."])
        else:
            tone = pick(["Gifts and Intents are nearly even - an honest exchange, what you give matching what you get.",
                         "The cylinder is in balance: what is offered and what is meant weigh about the same."])
        p.append(f"Around {main_word} the cylinder formed {ng} Gift{'s' if ng != 1 else ''} (read forward) and "
                 f"{ni} Intent{'s' if ni != 1 else ''} (read backward). {tone}")
        dir_count = Counter(o["dir"] for o in found if o["word"] != main_word)
        straight = dir_count["RIGHT"] + dir_count["LEFT"]
        diag = sum(v for k, v in dir_count.items() if "-" in k)
        if diag > straight:
            p.append(pick(["Most words run on the diagonal - the message is indirect, coming at an angle rather than head-on.",
                           "Diagonals dominate: expect this to arrive sideways, through people and situations you didn't plan on."]))
        elif straight > diag:
            p.append(pick(["Most words run straight across - this is a plain-spoken reading; take it at face value.",
                           "The words lie mostly level - direct, present-tense, nothing hidden in the angles."]))
        tiers = Counter(occ[0]["tier"] for _, _, occ in gifts + intents)
        flavor = []
        if tiers["mystic"]:
            mw = [w for w, t, _ in gifts + intents if t == "mystic"][:4]
            flavor.append(f"old names and sacred words surface ({join_words(mw)})")
        if tiers["slang"] or tiers["crude"]:
            sw = [w for w, t, _ in gifts + intents if t in ("slang", "crude")][:4]
            flavor.append(f"the street tongue speaks too ({join_words(sw)}) - this concerns everyday life, not only the spiritual")
        if tiers["dictionary"] + tiers["deep"] > total / 2:
            flavor.append("many rare and old words appear - the message is coded and rewards patience")
        if flavor:
            p.append("In its voice: " + "; ".join(flavor) + ".")
        # busiest ring
        ring_hits = Counter(c for o in found if o["word"] != main_word for _, c in o["cells"])
        if ring_hits:
            ring, hits = ring_hits.most_common(1)[0]
            if ring < active_len:
                ch = main_word[ring]
                p.append(f"The busiest ring is ring {ring + 1} ({hits} letters used by words), where the main word carries {ch} - "
                         f"{lm(ch)}. That letter is the hinge of this reading.")
            else:
                p.append(f"The busiest ring is ring {ring + 1}, outside the aligned word - "
                         f"what matters most is happening just beyond what you set.")
    sections.append(("The shape of this turn", p))

    # 3. Gifts / 4. Intents ----------------------------------------------------------------
    def word_paragraphs(groups, kind):
        out = []
        for idx, (w, tier, occ) in enumerate(groups[:6]):
            o = occ[0]
            where, motion, _ = placement(o)
            wn = word_num(w)
            line = end(describe_meaning(w, meanings)) + " "
            line += f"It sits {where}, {motion}. "
            if kind == "intent":
                ring_view = "".join(grid[r][c] for r, c in sorted(o["cells"], key=lambda rc: rc[1]))
                line += f"On the rings it shows as {ring_view} - only read in reverse does its intent appear. "
            if wn == main_n:
                line += f"Its number is {wn}, the same as {main_word} - it resonates directly with the main word. "
            else:
                line += (f"Its number is {wn} - {NUMBER_NAME[wn]}, {NUMBER_KEY[wn]}. "
                         f"Beside {main_word}'s {main_n}, they are {harmony(wn, main_n)}. ")
            if len(occ) > 1:
                line += f"It appears {len(occ)} times on the cylinder - a message repeated is a message underlined. "
            if idx == 0:
                line = (pick(["Strongest of all: ", "First and clearest: ", "Leading the way: "]) + line)
            out.append(line.strip())
        if len(groups) > 6:
            rest = [w for w, _, _ in groups[6:14]]
            out.append(f"Further out, quieter {'Gifts' if kind == 'gift' else 'Intents'} echo: {join_words(rest)}"
                       f"{' and more' if len(groups) > 14 else ''}.")
        return out

    if gifts:
        intro = pick(["Gifts are read forward, left to right - they are what is being handed to you.",
                      "Forward words are Gifts: what life is offering on this turn."])
        sections.append((f"The Gifts - what is given ({len(gifts)})", [intro] + word_paragraphs(gifts, "gift")))
    else:
        sections.append(("The Gifts - what is given", ["No forward words formed. Nothing new is being handed to you on this turn - "
                                                        "the gift is in what you already have."]))
    if intents:
        intro = pick(["Intents are read backward, right to left - they are the will and motive moving underneath.",
                      "Backward words are Intents: the purpose behind what is happening, readable only in reverse."])
        sections.append((f"The Intents - the will beneath ({len(intents)})", [intro] + word_paragraphs(intents, "intent")))
    else:
        sections.append(("The Intents - the will beneath", ["No backward words formed. There is no hidden motive here - "
                                                             "what you see is what is meant."]))

    # 5. Mirrors, branches and crossroads ----------------------------------------------------
    p = []
    gift_cells = {}
    for o in found:
        if o["kind"] == "gift" and o["word"] != main_word:
            gift_cells.setdefault(frozenset(o["cells"]), o["word"])
    mirrors = []
    for o in found:
        if o["kind"] == "intent":
            gw = gift_cells.get(frozenset(o["cells"]))
            if gw and gw != o["word"] and (gw, o["word"]) not in mirrors:
                mirrors.append((gw, o["word"]))
    for gw, iw in mirrors[:3]:
        gm, _ = meaning_of(gw, meanings, 60)
        im, _ = meaning_of(iw, meanings, 60)
        gm = (gm[0], lower_first(gm[1].strip("()"))) if gm else None
        im = (im[0], lower_first(im[1].strip("()"))) if im else None
        p.append(f"Mirror pair: the same letters read {gw} forward and {iw} backward. "
                 f"What is given as {gw}{' (' + gm[1] + ')' if gm else ''} is meant as {iw}{' (' + im[1] + ')' if im else ''}. "
                 + pick(["Hold both - the surface and the motive are two faces of one thing.",
                         "Watch for this exact pairing in your days: the gift and its reason arriving together."]))
    branches = []
    for o in found:
        if o["word"] == main_word:
            continue
        for r, c in o["cells"]:
            if r == C.CENTER and c < active_len:
                branches.append((o["word"], main_word[c], c, o["kind"]))
                break
    seen_b = set()
    blines = []
    for w, ch, c, kind in branches:
        if w in seen_b:
            continue
        seen_b.add(w)
        blines.append(f"{w} grows out of the {ch} on ring {c + 1}")
    if blines:
        p.append("Branches from the main word: " + "; ".join(blines[:6]) + ". "
                 + pick([f"These are the directions {main_word} naturally leads.",
                         f"Each is a path that starts inside {main_word} itself - consequences of the word you set."]))
    gc = {cell for o in found if o["kind"] == "gift" and o["word"] != main_word for cell in o["cells"]}
    ic = {cell for o in found if o["kind"] == "intent" and o["word"] != main_word for cell in o["cells"]}
    cross = sorted(gc & ic)
    if cross:
        letters_x = [grid[r][c] for r, c in cross]
        counts = Counter(letters_x)
        top, top_k = counts.most_common(1)[0]
        uniq = sorted(counts)
        p.append(f"Crossroads: {len(cross)} spot{'s' if len(cross) != 1 else ''} on the cylinder belong to both a Gift and an Intent "
                 f"- the places where what is offered and what is meant meet. The letters standing at those crossings are "
                 f"{join_words(uniq)}. "
                 + (f"{top} stands at {top_k} of them - {lm(top)} - making it the master key of this turn."
                    if top_k > 1 else f"Each crossing is its own small turning point."))
    if not p:
        p.append("No mirrors, branches or crossroads formed - the Gifts and Intents keep to their own lanes on this turn. "
                 "What is offered and what is meant are separate matters; don't confuse them.")
    sections.append(("Mirrors, branches and crossroads", p))

    # 6. Above and below the line ------------------------------------------------------------
    above, below = [], []
    for w, t, occ in gifts + intents:
        _, _, avg = placement(occ[0])
        (above if avg < 0 else below if avg > 0 else []).append((abs(avg), w))
    p = []
    if above:
        above.sort()
        p.append(f"Above the main line - what is arriving: {join_words(w for _, w in above[:6])}. "
                 f"Nearest of these is {above[0][1]}, the next thing likely to reach you; "
                 f"farthest is {above[-1][1]}, still forming.")
    if below:
        below.sort()
        p.append(f"Below the main line - what is rooted, underneath, or already behind you: {join_words(w for _, w in below[:6])}. "
                 f"{below[0][1]} lies closest to the surface; {below[-1][1]} is the deepest root.")
    if above and below:
        p.append(pick([f"With {len(above)} words above and {len(below)} below, the reading leans "
                       f"{'toward the future' if len(above) > len(below) else 'toward the past and its roots' if len(below) > len(above) else 'evenly between past and future'}.",
                       f"The balance - {len(above)} above, {len(below)} below - says this is "
                       f"{'mostly about what comes next' if len(above) > len(below) else 'mostly about what has already shaped you' if len(below) > len(above) else 'as much about roots as about what is coming'}."]))
    if p:
        sections.append(("Above and below the line", p))

    # 7. The numbers ---------------------------------------------------------------------------
    p = []
    gift_n = reduce_num(sum(word_num(w) for w, _, _ in gifts)) if gifts else None
    intent_n = reduce_num(sum(word_num(w) for w, _, _ in intents)) if intents else None
    whole = reduce_num(main_n + (gift_n or 0) + (intent_n or 0))
    p.append(f"The main word: {main_n} - {main_title} ({NUMBER_KEY[main_n]}).")
    if gift_n:
        p.append(f"All the Gifts together reduce to {gift_n} - {NUMBER_NAME[gift_n]}. What is being given is, at heart, {NUMBER_KEY[gift_n]}.")
    if intent_n:
        p.append(f"All the Intents together reduce to {intent_n} - {NUMBER_NAME[intent_n]}. The will beneath is about {NUMBER_KEY[intent_n]}.")
    if gift_n and intent_n:
        if gift_n == intent_n:
            p.append("Gift and Intent share one number: what is offered and why it is offered are perfectly aligned. That is rare - trust it.")
        else:
            p.append(f"Gift {gift_n} and Intent {intent_n} are {harmony(gift_n, intent_n)}.")
    wt, wd, wg = C.NUMEROLOGY_THEMES[whole][0], C.NUMEROLOGY_THEMES[whole][1], C.NUMEROLOGY_THEMES[whole][2]
    p.append(f"The whole reading - main word, Gifts and Intents together - comes to {whole}: {wt}. {wd}")
    sections.append(("The numbers", p))

    # 8. Counsel ---------------------------------------------------------------------------------
    p = []
    g0 = gifts[0][0] if gifts else None
    i0 = intents[0][0] if intents else None
    if g0 and i0:
        gm, _ = meaning_of(g0, meanings, 70)
        im, _ = meaning_of(i0, meanings, 70)
        p.append(pick([
            f"Take {g0} as what you are being given{' - ' + lower_first(gm[1]) if gm and gm[0] != 'name' else ''}. "
            f"Understand {i0} as the reason{' - ' + lower_first(im[1]) if im and im[0] != 'name' else ''}. "
            f"Let {main_word} be how you carry both.",
            f"The cylinder hands you {g0} and shows you {i0} underneath it. "
            f"Receive the first; question the second; and stand on {main_word} while you do.",
        ]))
    elif g0:
        p.append(f"Receive {g0}. Nothing hidden is driving this - it is simply being offered. Let {main_word} be your answer to it.")
    elif i0:
        p.append(f"Nothing is being handed over yet; only the motive shows: {i0}. Work on the why before you expect the what.")
    p.append(main_guide)
    if whole != main_n:
        p.append(wg)
    q = pick(NUMBER_QUESTIONS[whole])
    p.append(f"A question to carry with you: {q}")
    if g0 or i0:
        essence = []
        if g0:
            essence.append(f"given {g0}")
        if i0:
            essence.append(f"meant {i0}")
        p.append(f"In one breath: {main_word}, {' and '.join(essence)}, resolving to {whole} - {NUMBER_KEY[whole]}.")
    sections.append(("Counsel", p))
    return sections


def reading_text(sections, width=74):
    """Plain-text version (ASCII, wrapped) for the downloadable file."""
    out = []
    for i, (head, paras) in enumerate(sections, 1):
        out.append("")
        out.append(f"  {C._ascii(head).upper()}")
        out.append("  " + "-" * min(len(head), width))
        for para in paras:
            out += C._wrap(para, width=width, indent="  ")
            out.append("")
    return out
