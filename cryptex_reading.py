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


NUMBER_ACTION = {
    1: "take the first step yourself",
    2: "move together, not alone",
    3: "say it out loud",
    4: "build it slowly and steadily",
    5: "let the change happen",
    6: "take care of your people - and yourself",
    7: "go quiet and trust what you already know",
    8: "claim your power",
    9: "let the old chapter close",
}
SHORT_HARMONY = {
    0: "the same number as {m} - it speaks directly to the main word",
    1: "one step from {m}'s {n} - an easy, natural move",
    2: "close to {m}'s {n} - it colors the main word",
    3: "a stretch from {m}'s {n} - it widens the picture",
    4: "nearly opposite {m}'s {n} - it pulls against the main word",
}


def short_harmony(wn, main_n, main_word):
    d = abs(wn - main_n)
    return SHORT_HARMONY[min(d, 9 - d, 4)].format(m=main_word, n=main_n)


# ------------------------------------------------------------------ meanings
def meaning_of(w, meanings, n=110):
    info = C.explain(w, meanings)
    if not info["lines"]:
        return None, info
    label, text = info["lines"][0]
    text = strip_end(re.sub(r"^\([^)]*\)\s*", "", text))
    if len(text) > n:
        text = text[: n - 1].rsplit(" ", 1)[0] + "..."
    return (label, text), info


_TRAILING = {"a", "an", "the", "of", "to", "in", "into", "on", "for", "with", "and", "or", "so", "as", "by", "at",
             "from", "that", "which", "is", "being", "its", "your", "their", "his", "her", "who", "through", "about",
             "be", "if", "but", "has", "have", "had", "can", "will", "usually", "noted", "especially", "when", "where", "than", "are", "was"}


def gist(w, meanings, words=5):
    """A tiny meaning for one word: its first clause, cut at a natural word boundary ('' if none)."""
    m, _ = meaning_of(w, meanings, 200)
    if not m:
        return ""
    text = m[1].replace('"', "")
    text = re.sub(r"\([^)]*\)", "", text)
    text = re.split(r";| - | — |\. |:", text)[0].strip(" .")
    first = text.split(",")[0].strip()
    if len(first.split()) >= 3 or len(text.split()) <= words:
        text = first if len(first.split()) >= 3 else text
    if m[0] == "name" and ":" in m[1]:
        text = m[1].split(":", 1)[1].replace('"', "").strip(" .")
    parts = text.split()[:words]
    while len(parts) > 1 and parts[-1].lower().strip(",.") in _TRAILING:
        parts.pop()
    text = " ".join(parts).strip(" ,.")
    if len(text) < 3 or re.search(r"\d|\bpers\b|^see |^imp$|^p\. ?p|^pl$|^obs", text, re.I):
        return ""
    ws = text.split()
    keep_caps = (len(ws) > 1 and all(x[:1].isupper() for x in ws)) or m[0] in ("mystic", "name", "title")
    if not keep_caps:
        text = lower_first(text)
    return text


def wm(w, meanings, words=5):
    """WORD (short meaning)"""
    t = gist(w, meanings, words)
    return f"{w} ({t})" if t else w


# ------------------------------------------------------------------ strict tone: only clearly dark / clearly good words
WARN_WORDS = set("""
ABUSE AGONY ANGER ANGRY ARSON ASSAULT ATTACK BETRAY BLAME BLEED BRUTAL BULLY CHEAT CHEATS CORPSE CRIME CRUEL CURSE CURSED
CURSES DEATH DECAY DECEIT DEFEAT DEMON DESPAIR DEVIL DOOM DOOMED DREAD DROWN DYING ENEMY ENVY EVIL EXILE FAIL FAILED FAILS
FAKE FEAR FEUD FIEND FRAUD FURY GREED GRIEF GUILT GUN GUNS HARM HATE HATED HATRED HAVOC HEX HEXES HOAX HOSTILE HURT HURTS
INSULT JAIL KILL KILLED KILLS LIAR LIARS LIE LIES LONELY LOSS LUST MALICE MENACE MOCK MOURN MURDER NASTY PAIN PANIC PERIL
PLAGUE POISON PREY PRISON PUNISH RAGE RAID RAPE ROB ROBBED ROBS ROT ROTTEN RUIN RUINED RUINS SATAN SCAM SCAR SCORN SHAME
SIN SINS SLAVE SORROW SPITE STAB STEAL STOLE STOLEN STRIFE SUFFER SWINDLE TERROR THEFT THIEF THREAT TORMENT TORTURE TOXIC
TRAP TRAPS TRICK TRAITOR VENOM VICE VILE VIOLENT VIRUS WAR WARS WEEP WICKED WOE WOES WOUND WOUNDS WRATH WRECK WRONG YOB
SAD ILL DIE DIED DIES DEAD BANE GORE GRIM HELL FOE FOES SORE ACHE ACHES GLOOM BLEAK DIRE TOMB IRE LOSE LOST LOSER BROKEN
SNARE SPY SPIES BRUTE GREEDY STING SLAIN SLAY? HOSTAGE KIDNAP TAINT TAINTED VOID HOLLOW CRUSH CRUSHED BURNED BITTER
""".replace("SLAY? ", "").split())
GOOD_WORDS = set("""
ADORE ALIVE ALLY AMEN ANGEL ANGELS ASCEND BLESS BLESSED BLISS BLOOM BLOSSOM BRAVE CALM CARE CHARM CHEER CURE DIVINE
EASE EDEN FAITH FAVOR FEAST FREE FRIEND FRIENDS GAIN GEM GEMS GIFT GIFTS GLAD GLEE GLORY GLOW GOLD GOOD GRACE GRAIL GROW
GROWTH HALO HAPPY HEAL HEALED HEALS HEALTH HEART HEAVEN HELP HERO HONOR HOPE HUG HUGS JOY JOYS KIND KINDLY KISS LIGHT
LOVE LOVED LOYAL LUCK LUCKY MERCY MERRY MIRTH NOBLE OASIS PEACE PEARL PRAISE PRIZE PROUD PURE RELIEF RICH RISE SAFE
SAINT SALVE SAVE SAVED SHINE SMILE SOAR SOUL SPARK THRIVE TREAT TRUE TRUST TRUTH UNITY VALOR VICTOR WARM WEALTH WIN
WINS WISDOM WISE WON WONDER WORTH YES ZEST
FUN YAY BOON ACE AID AIDS BEST SUN SUNNY DAWN SWEET HONEY BRAVO HOLY SACRED ZEN SERENE GRIN LAUGH LAUGHS CHEERS GIVE GIVEN
SHARE HEALER ADORED BELOVED DEAR DARLING SOULS ANGELIC GIFTED THANK THANKS HAVEN HOME HOMES REST RESCUE REVIVE RENEW
""".split())


def tone(w, meanings=None):
    """+1 clearly good, -1 clearly dark, 0 everything else. No guessing from definitions."""
    if w in WARN_WORDS:
        return -1
    if w in GOOD_WORDS:
        return 1
    return 0


# ------------------------------------------------------------------ one analysis of the spin, shared by everything
def placement(o):
    rows = [r - C.CENTER for r, _ in o["cells"]]
    avg = sum(rows) / len(rows)
    if all(r == 0 for r in rows):
        return "on", 0, "On the main line - present now"
    if any(r == 0 for r in rows):
        return "on", avg, "Growing out of the main line - a direct result of the word"
    d = abs(avg)
    if avg < 0:
        txt = ("Just above the line - arriving soon" if d <= 3 else
               "Above the line - on its way" if d <= 7 else "High above - still forming")
        return "above", avg, txt
    txt = ("Just below the line - close to the root" if d <= 3 else
           "Below the line - in the foundations" if d <= 7 else "Deep below - an old root")
    return "below", avg, txt


def analyze(main_word, active_len, grid, found, gifts, intents, meanings):
    a = {"main": main_word}
    a["main_n"], a["main_title"], a["main_desc"], a["main_guide"] = C.numerology(main_word)
    def piece_of_main(occ):   # e.g. REAL inside ISREAL: lies entirely on the main line
        return all(all(r == C.CENTER for r, _ in o["cells"]) for o in occ)
    a["g"] = [x for x in gifts if x[0] != main_word and not piece_of_main(x[2])]
    a["i"] = [x for x in intents if x[0] != main_word and not piece_of_main(x[2])]
    gw = [w for w, _, _ in a["g"]]
    iw = [w for w, _, _ in a["i"]]
    a["gift_n"] = reduce_num(sum(word_num(w) for w in gw)) if gw else 0
    a["intent_n"] = reduce_num(sum(word_num(w) for w in iw)) if iw else 0
    a["whole"] = reduce_num(a["main_n"] + a["gift_n"] + a["intent_n"]) or a["main_n"]
    # tone
    a["bad_g"] = [w for w in gw if tone(w) < 0]
    a["good_g"] = [w for w in gw if tone(w) > 0]
    a["bad_i"] = [w for w in iw if tone(w) < 0]
    a["good_i"] = [w for w in iw if tone(w) > 0]
    warn = len(a["bad_g"]) + 1.5 * len(a["bad_i"]) + (1 if tone(main_word) < 0 else 0)
    good = len(a["good_g"]) + 1.5 * len(a["good_i"]) + (1 if tone(main_word) > 0 else 0)
    a["kind"] = ("neutral" if warn == 0 and good == 0 else "warn" if warn >= good * 1.5 else
                 "good" if good >= warn * 1.5 else "mixed")
    # special features
    others = [o for o in found if o["word"] != main_word]
    a["main_elsewhere"] = [o for o in found if o["word"] == main_word and
                           not all(r == C.CENTER for r, _ in o["cells"])]
    a["two_way"] = sorted(set(gw) & set(iw))
    gift_cells = {frozenset(o["cells"]): o["word"] for o in others if o["kind"] == "gift"}
    mirrors = []
    for o in others:
        if o["kind"] == "intent":
            m = gift_cells.get(frozenset(o["cells"]))
            if m and m != o["word"] and (m, o["word"]) not in mirrors:
                mirrors.append((m, o["word"]))
    a["mirrors"] = mirrors
    a["repeats"] = [(w, len(occ)) for w, _, occ in a["g"] + a["i"] if len(occ) > 1]
    a["resonant"] = [w for w in gw + iw if word_num(w) == a["main_n"]]
    a["mystic"] = [w for w, t, _ in a["g"] + a["i"] if t == "mystic"]
    branches = []
    for o in others:
        for r, c in o["cells"]:
            if r == C.CENTER and c < active_len and not all(rr == C.CENTER for rr, _ in o["cells"]):
                branches.append((o["word"], main_word[c], c))
                break
    a["branches"] = list(dict.fromkeys(branches))
    zones = {"above": [], "below": [], "on": []}
    for w, _, occ in a["g"] + a["i"]:
        z, avg, _ = placement(occ[0])
        zones[z].append((abs(avg), w))
    for z in zones:
        zones[z].sort()
    a["zones"] = zones
    return a


# ------------------------------------------------------------------ phrase pools (varied per spin)
P_BAD_I = [
    "The motive underneath is {x} - that's the part working against you.",
    "Read backward, it shows {x}. That's the hidden problem.",
    "{x} is moving under the surface; someone's intent here isn't clean.",
    "Underneath it all sits {x}. Don't ignore that.",
]
P_BAD_G = [
    "{x} is being offered - refuse it.",
    "Of what's coming, {x} is the thing to turn down.",
    "{x} arrives looking like a gift. It isn't.",
    "Say no to {x}, however it's dressed up.",
]
P_GOOD_G = [
    "{x} is real - take it.",
    "The good here is {x}; that part you can trust.",
    "{x} is worth accepting.",
    "What's truly being given is {x}.",
]
P_GOOD_IN_WARN = [
    "One thing is still sound: {x}. Don't let it talk you past the warning.",
    "Not all of it is bad - {x} holds up. But the warning comes first.",
    "{x} is the one clean thread here; keep it, and stay careful with the rest.",
]
P_GOOD_I = [
    "Underneath, {x} - the motive is on your side.",
    "The intent is clean: {x}.",
    "What drives this is {x}, and it's working for you.",
]
P_SPLIT_I = [
    "The motive is split: {g} pulls for you, {b} pulls against you.",
    "Two forces sit underneath - {g} on your side, {b} against it.",
]
P_NEUTRAL = [
    "The truth: this turn is NEUTRAL - nothing clearly dark, nothing clearly blessed.",
    "The truth: this turn is NEUTRAL - no warning and no blessing showed up.",
    "The truth: this turn is NEUTRAL - the cylinder isn't leaning either way.",
    "The truth: this turn is NEUTRAL - no clear omen in either direction.",
    "The truth: this turn is NEUTRAL - plain ground, no hazard and no windfall.",
]
P_NEUTRAL_TAIL = [
    "{x} is the clearest signal here; what you do with it is your call.",
    "The weight sits on {x} - read that one closely and decide for yourself.",
    "If anything speaks loudest, it's {x}. The rest is up to you.",
    "Nothing forces your hand. {x} is the word to think about.",
    "Watch {x}; it carries the most meaning on this turn, but it doesn't decide for you.",
]
P_HEAD = {
    "warn": ["The truth: this is a WARNING.", "The truth: this is a WARNING - take it seriously.",
             "The truth: this is a WARNING, plain and simple."],
    "good": ["The truth: this is a GOOD SIGN.", "The truth: this is a GOOD SIGN - it's real.",
             "The truth: this is a GOOD SIGN, no catch in sight."],
    "mixed": ["The truth: this is MIXED - good and trouble in the same turn.",
              "The truth: this is MIXED - some of it helps you, some of it doesn't.",
              "The truth: this is MIXED - sort it carefully."],
}


def truth_lines(a, meanings, rng):
    if a["kind"] == "neutral":
        pool = [w for w, _, _ in a["g"] + a["i"] if gist(w, meanings)]
        if not pool:
            return [rng.choice(P_NEUTRAL), "Nothing is pushing you; you decide."]
        # the most meaningful word: mystic/slang first, then the longest defined word
        tiers = {w: t for w, t, _ in a["g"] + a["i"]}
        key = sorted(pool, key=lambda w: (tiers[w] not in ("mystic", "slang"), -len(w), w))[0]
        return [rng.choice(P_NEUTRAL), rng.choice(P_NEUTRAL_TAIL).format(x=wm(key, meanings))]
    tag = lambda ws: join_words(wm(w, meanings) for w in ws[:3])
    out = [rng.choice(P_HEAD[a["kind"]])]
    if a["bad_i"] and a["good_i"]:
        out.append(rng.choice(P_SPLIT_I).format(g=tag(a["good_i"]), b=tag(a["bad_i"])))
    elif a["bad_i"]:
        out.append(rng.choice(P_BAD_I).format(x=tag(a["bad_i"])))
    elif a["good_i"]:
        out.append(rng.choice(P_GOOD_I).format(x=tag(a["good_i"])))
    if a["bad_g"]:
        out.append(rng.choice(P_BAD_G).format(x=tag(a["bad_g"])))
    if a["good_g"]:
        if a["kind"] == "warn":   # keep the good part clearly separate from the warning
            out.append(rng.choice(P_GOOD_IN_WARN).format(x=tag(a["good_g"])))
        else:
            out.append(rng.choice(P_GOOD_G).format(x=tag(a["good_g"])))
    if tone(a["main"]) < 0:
        out.append(f"The main word itself, {a['main']}, is dark - be honest about why you chose it.")
    if len(out) == 1:   # verdict came from the main word alone
        if tone(a["main"]) > 0:
            out.append(f"{a['main']} itself is a clearly good word, and nothing dark formed around it.")
        else:
            out.append(f"{a['main']} itself carries it; no other clearly marked word formed around it.")
    return out


# ------------------------------------------------------------------ the signature: what makes THIS spin unusual
def signature(a, meanings, rng):
    m = a["main"]
    feats = []
    if a["main_elsewhere"]:
        o = a["main_elsewhere"][0]
        feats.append(f"{m} appears a second time on the cylinder, reading {o['dir'].lower()} - "
                     f"the word you set is echoing back at you. That almost never happens.")
    if a["two_way"]:
        w = a["two_way"][0]
        feats.append(f"{wm(w, meanings)} shows up as both a Gift and an Intent - what you're given and why "
                     f"are the same thing here.")
    if a["mirrors"]:
        gw, iw = a["mirrors"][0]
        feats.append(f"The same letters read {wm(gw, meanings)} forward and {wm(iw, meanings)} backward - "
                     f"the gift and its motive are one strip of letters seen from two sides.")
    if a["gift_n"] and a["gift_n"] == a["intent_n"] == a["main_n"]:
        feats.append(f"The Gifts, the Intents and {m} all reduce to {a['main_n']} - a rare triple alignment.")
    elif a["gift_n"] and a["gift_n"] == a["intent_n"]:
        feats.append(f"The Gifts and the Intents both reduce to {a['gift_n']} ({NUMBER_KEY[a['gift_n']]}) - "
                     f"what's offered and why are in step.")
    if a["repeats"]:
        w, n = max(a["repeats"], key=lambda x: x[1])
        feats.append(f"{wm(w, meanings)} appears {n} times - a message repeated is a message underlined.")
    if a["mystic"]:
        w = a["mystic"][0]
        feats.append(f"A sacred word surfaced: {wm(w, meanings, 7)}.")
    if not a["g"] and not a["i"]:
        feats.append(f"The cylinder is silent - no other word formed around {m}. The word stands alone.")
    if a["branches"]:
        w, ch, c = a["branches"][0]
        feats.append(f"{wm(w, meanings)} grows straight out of the {ch} in {m} - a direct consequence of the word you set.")
    ng, ni = len(a["g"]), len(a["i"])
    if ng and ni and (ng >= 2 * ni or ni >= 2 * ng):
        feats.append(f"{'Gifts' if ng > ni else 'Intents'} heavily outnumber "
                     f"{'Intents' if ng > ni else 'Gifts'} ({max(ng, ni)} to {min(ng, ni)}) - "
                     f"{'far more is offered than asked' if ng > ni else 'far more is moving underneath than on the surface'}.")
    if a["resonant"]:
        w = a["resonant"][0]
        feats.append(f"{wm(w, meanings)} carries the same number as {m} ({a['main_n']}), so it speaks to the main word directly.")
    if not feats:
        feats.append(f"Nothing unusual broke the pattern on this turn - a plain, steady reading for {m}.")
    return feats[:2]


# ------------------------------------------------------------------ the reading
def build_reading(main_word, active_len, offsets, grid, found, gifts, intents, meanings):
    """Return [(heading, [paragraphs])] - short, precise, and specific to this exact spin."""
    seed = int(hashlib.md5(f"{offsets}|{active_len}|{len(found)}".encode()).hexdigest(), 16)
    rng = random.Random(seed)
    a = analyze(main_word, active_len, grid, found, gifts, intents, meanings)
    m, mn = main_word, a["main_n"]
    secs = []

    # 1. Signature - opens with what is unusual about this spin
    secs.append(("The signature of this spin", [" ".join(signature(a, meanings, rng))]))

    # 2. The word
    mg = gist(m, meanings, 9)
    letters = list(m)
    word_p = (f"{m}{' means ' + mg if mg else ' is not a dictionary word - it speaks through its letters alone'}. "
              f"Its number is {mn}, {a['main_title']}: {lower_first(a['main_desc'])} "
              f"It opens with {letters[0]} ({lm(letters[0])})"
              + (f" and closes with {letters[-1]} ({lm(letters[-1])})." if len(letters) > 1 else "."))
    secs.append((f"The word - {m}", [word_p]))

    # 3 / 4. Given and meant - top three each, one precise sentence per word
    def word_lines(groups, kind):
        lines = []
        for w, _, occ in groups[:3]:
            o = occ[0]
            _, _, where = placement(o)
            t = gist(w, meanings, 8)
            line = f"{end(w + (' - ' + t if t else ''))} {where}"
            if kind == "intent":
                ring = "".join(grid[r][c] for r, c in sorted(o["cells"], key=lambda rc: rc[1]))
                line += f"; on the rings it reads {ring}"
            line += f". Number {word_num(w)}, {short_harmony(word_num(w), mn, m)}."
            lines.append(line)
        rest = [w for w, _, _ in groups[3:9]]
        if rest:
            lines.append(f"Also present: {join_words(rest)}{' and more' if len(groups) > 9 else ''}.")
        return lines

    if a["g"]:
        secs.append((f"What is given ({len(a['g'])})", word_lines(a["g"], "gift")))
    if a["i"]:
        secs.append((f"What is meant ({len(a['i'])})", word_lines(a["i"], "intent")))

    # 5. As above, so below
    z = a["zones"]

    def uniq(pairs):
        seen, out = set(), []
        for d, w in pairs:
            if w not in seen:
                seen.add(w)
                out.append((d, w))
        return out
    above, below = uniq(z["above"]), uniq(z["below"])
    p = []
    if above:
        shown = [w for _, w in above[:5]]
        p.append(f"In the light above the line - what is arriving: {join_words(shown)}"
                 f"{' (and ' + str(len(above) - 5) + ' more)' if len(above) > 5 else ''}. Closest is {above[0][1]}.")
    if below:
        shown = [w for _, w in below[:5]]
        deepest = below[-1][1]
        p.append(f"In the dark below - what is rooted or already behind you: {join_words(shown)}"
                 f"{' (and ' + str(len(below) - 5) + ' more)' if len(below) > 5 else ''}. "
                 f"{'Deepest of all is ' + deepest + '.' if deepest not in shown else 'Deepest is ' + deepest + '.'}")
    if above or below:
        na, nb = len(above), len(below)
        if na != nb:
            p.append(f"With {na} above and {nb} below, this turn is mostly about "
                     f"{'what comes next' if na > nb else 'what already shaped you'}.")
        secs.append(("As above, so below", [" ".join(p)]))

    # 6. Counsel - built from this spin's own words, not stock lines
    secs.append(("Counsel", counsel(a, grid, meanings, rng)))
    return secs


def _pos(w, meanings):
    info = C.explain(w, meanings)
    return info["lines"][0][0] if info["lines"] else ""


def _occ(a, w):
    for x in a["g"] + a["i"]:
        if x[0] == w:
            return x[2][0]
    return None


def _where_advice(a, w, meanings, rng, kind):
    """What to do with a word, given where it sits on the cylinder."""
    o = _occ(a, w)
    m = a["main"]
    zone = placement(o)[0] if o else "on"
    tw = wm(w, meanings)
    if kind == "bad":
        return rng.choice([f"{tw} is in this turn - refuse it, however it's offered.",
                           f"Turn {tw} down before it settles in.",
                           f"Don't take {tw}, even if it looks harmless."])
    if zone == "above":
        return rng.choice([f"{tw} is on its way to you - make room for it.",
                           f"Watch for {tw}; it hasn't arrived yet, but it's coming.",
                           f"{tw} is still forming above the line - get ready to receive it."])
    if zone == "below":
        return rng.choice([f"{tw} is already in your roots - use what you have.",
                           f"You already carry {tw}; look at where it came from.",
                           f"{tw} sits below the line - it's behind you, but it still feeds you."])
    for bw, ch, c in a["branches"]:
        if bw == w:
            return rng.choice([f"{tw} grows out of the {ch} in {m} - it's already in your hands.",
                               f"{tw} comes straight from the {ch} in {m}; act on it directly."])
    return rng.choice([f"{tw} is right here on the main line - deal with it now.",
                       f"{tw} is present now; don't postpone it."])


def _intent_advice(a, w, meanings, rng):
    tw = wm(w, meanings)
    t = tone(w)
    if t < 0:
        return rng.choice([f"Underneath, {tw} is doing the steering - confront it before it acts for you.",
                           f"The hidden driver is {tw}. Name it out loud and it loses its grip.",
                           f"{tw} is the motive under the surface; don't let it make your choices."])
    if t > 0:
        return rng.choice([f"Underneath, {tw} is on your side - trust it.",
                           f"The motive is {tw}; let it lead.",
                           f"{tw} drives this from below, and it's a good driver."])
    return rng.choice([f"Underneath it all is {tw} - notice where that's moving you.",
                       f"The real driver is {tw}; once you see it, you can choose with it or against it.",
                       f"Read backward, this turn is about {tw}. Keep that in view."])


NUMBER_ACTION_ING = {
    1: "making the first move yourself",
    2: "working with someone instead of alone",
    3: "saying it out loud",
    4: "building slowly and steadily",
    5: "letting the change happen",
    6: "taking care of your people - and yourself",
    7: "going quiet and trusting what you already know",
    8: "claiming your power",
    9: "letting the old chapter close",
}


def _question(a, key, meanings, rng):
    """A closing question made from the key word's own meaning."""
    if key:
        t = gist(key, meanings, 4)
        pos = _pos(key, meanings)
        if t and pos == "noun":
            return rng.choice([f"Where is {t} showing up in your life right now?",
                               f"What would change if you treated {key} - {t} - as a message meant for you?",
                               f"Who or what is the {key} in your life right now?"])
        if t and pos == "verb":
            return rng.choice([f"What would it take for you to {t}?",
                               f"Where are you being asked to {t} - and are you resisting it?"])
        if t and pos == "adj":
            return rng.choice([f"Where in your life do you need to be {t}?",
                               f"What would it look like to be {t} today?"])
        if t:
            return rng.choice([f"What does {key} - {t} - mean for you today?",
                               f"Why would the cylinder show you {key} now?"])
    return rng.choice(NUMBER_QUESTIONS[a["whole"]])


def counsel(a, grid, meanings, rng):
    m, mn, w_n, k = a["main"], a["main_n"], a["whole"], a["kind"]
    gws = [w for w, _, _ in a["g"]]
    iws = [w for w, _, _ in a["i"]]
    defined = lambda ws: [w for w in ws if gist(w, meanings)]
    p = []
    # what to do with what is given
    if k == "warn" and a["bad_g"]:
        p.append(_where_advice(a, a["bad_g"][0], meanings, rng, "bad"))
    key_g = (a["good_g"] or defined(gws) or gws or [None])[0]
    if key_g and key_g not in a["bad_g"]:
        p.append(_where_advice(a, key_g, meanings, rng, "good" if tone(key_g) > 0 else "plain"))
    # what to do about what is meant
    key_i = (a["bad_i"] or a["good_i"] or defined(iws) or iws or [None])[0]
    if key_i:
        p.append(_intent_advice(a, key_i, meanings, rng))
    if not gws and not iws:
        p.append(f"No other word formed, so the counsel is {m} itself - {gist(m, meanings, 8) or 'its letters and its number'}.")
    # numbers, tied to an actual word where possible
    carrier = next((w for w in gws + iws if word_num(w) == w_n and tone(w) >= 0), None)
    caveat = " - after the warning is dealt with" if k == "warn" else ""
    if w_n == mn:
        p.append(rng.choice([f"{m} and the whole reading both land on {mn}: the work is {NUMBER_ACTION_ING[mn]}{caveat}.",
                             f"Everything here adds up to {mn}, the same as {m} - so this is about {NUMBER_ACTION_ING[mn]}{caveat}."]))
    elif carrier:
        p.append(rng.choice([f"{carrier} carries the reading's number, {w_n} - start there, by {NUMBER_ACTION_ING[w_n]}{caveat}.",
                             f"The whole reading comes to {w_n}, and {carrier} holds that number: the way through is {NUMBER_ACTION_ING[w_n]}{caveat}."]))
    else:
        p.append(rng.choice([f"Start by {NUMBER_ACTION_ING[mn]} ({m}'s {mn}), then move to {NUMBER_ACTION_ING[w_n]} (the reading's {w_n}){caveat}.",
                             f"{m}'s {mn} asks for {NUMBER_ACTION_ING[mn]}; the reading as a whole ({w_n}) asks for {NUMBER_ACTION_ING[w_n]} - in that order{caveat}."]))
    q_key = key_i if (key_i and rng.random() < 0.5) else (key_g or key_i)
    p.append("Carry this question: " + _question(a, q_key, meanings, rng))
    return [" ".join(p)]




def condensed(main_word, gifts, intents, meanings, offsets=None, active_len=None, grid=None, found=None):
    """The brief: every word with a short meaning, the meaning of it all, and the truth (said only here)."""
    seed = int(hashlib.md5(f"{offsets}|{active_len}|{len(found or [])}|brief".encode()).hexdigest(), 16)
    rng = random.Random(seed)
    a = analyze(main_word, active_len or len(main_word), grid, found or [], gifts, intents, meanings)
    g = [w for w, _, _ in a["g"]]
    i = [w for w, _, _ in a["i"]]
    mg = gist(main_word, meanings, 7)
    head = f"{main_word}{' (' + mg + ')' if mg else ''}"
    tagged = lambda ws: join_words(wm(w, meanings) for w in ws)
    out = []
    if not g and not i:
        out.append(f"{head} stands alone - no other words formed around it.")
    else:
        if g:
            out.append(f"{head} is given {tagged(g)}.")
        if i:
            out.append(f"{'Beneath it, the intent is' if g else head + ' carries the intent'} {tagged(i)}.")
    gw = next(((w, gist(w, meanings, 6)) for w in (a["good_g"] + g)[:8] if gist(w, meanings, 6)), (g[0], "") if g else (None, ""))
    iw = next(((w, gist(w, meanings, 6)) for w in (a["bad_i"] + i)[:8] if gist(w, meanings, 6)), (i[0], "") if i else (None, ""))
    fmt = lambda p: f"{p[0]} ({p[1]})" if p[1] else p[0]
    if gw[0] and iw[0]:
        core = f"{main_word} brings you {fmt(gw)}, and the force underneath is {fmt(iw)}"
    elif gw[0]:
        core = f"{main_word} brings you {fmt(gw)}, with nothing hidden behind it"
    elif iw[0]:
        core = f"nothing is handed over yet - the force at work is {fmt(iw)}"
    else:
        core = f"the answer is {main_word} itself"
    w_n = a["whole"]
    out.append(f"The meaning of it all: {core}. It comes down to {w_n}, {NUMBER_KEY[w_n]} - {NUMBER_ACTION[w_n]}.")
    out.append(" ".join(truth_lines(a, meanings, rng)))
    return " ".join(out)


def reading_text(sections, width=74):
    out = []
    for head, paras in sections:
        out += ["", f"  {C._ascii(head).upper()}", "  " + "-" * min(len(head), width)]
        for para in paras:
            out += C._wrap(para, width=width, indent="  ") + [""]
    return out
