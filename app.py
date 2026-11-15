import random
import time

import streamlit as st
import streamlit.components.v1 as components

import cryptex_core as C

st.set_page_config(page_title="Cryptex werd", page_icon="🗝️", layout="wide")

# ============================================================ NEON THEME
MINT, CYAN, MAGENTA, VIOLET = "#00FFC6", "#00E5FF", "#FF2BD6", "#B388FF"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Exo+2:wght@400;500;600;700&family=Share+Tech+Mono&display=swap');

:root { --mint:#00FFC6; --cyan:#00E5FF; --magenta:#FF2BD6; --violet:#B388FF; --text:#DFFFF6; }

html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background: #000 !important; color: var(--text);
}
.stApp {
    background:
      radial-gradient(1200px 500px at 50% -200px, rgba(0,255,198,.10), transparent 70%),
      repeating-linear-gradient(0deg, rgba(0,255,198,.035) 0 1px, transparent 1px 42px),
      repeating-linear-gradient(90deg, rgba(0,255,198,.035) 0 1px, transparent 1px 42px),
      #000 !important;
}
.stApp, .stApp p, .stApp li, .stApp label, .stApp span, .stMarkdown {
    font-family: 'Exo 2', system-ui, sans-serif; font-size: 17px; letter-spacing: .2px;
}
.stApp p, .stApp li { color: var(--text); line-height: 1.6; }
h1, h2, h3, h4, h5 { font-family: 'Orbitron', sans-serif !important; letter-spacing: 2px; color: var(--mint) !important;
    text-shadow: 0 0 6px rgba(0,255,198,.55), 0 0 18px rgba(0,255,198,.25); }
h4 { color: var(--cyan) !important; text-shadow: 0 0 6px rgba(0,229,255,.5); }
strong, b { color: #fff; }
hr { border-color: rgba(0,255,198,.25) !important; }
[data-testid="stCaptionContainer"], .stCaption, small { color: #8fd9c7 !important; }

/* Title with the giant X */
.cx-title { font-family:'Orbitron',sans-serif; font-weight:900; font-size: clamp(34px, 7vw, 64px); line-height:1.1;
    letter-spacing: 6px; color: var(--mint); margin: 6px 0 0 0;
    text-shadow: 0 0 8px rgba(0,255,198,.8), 0 0 28px rgba(0,255,198,.4); }
.cx-title .x { font-size: 1.75em; color: var(--magenta); display:inline-block; transform: translateY(.08em);
    text-shadow: 0 0 10px rgba(255,43,214,.95), 0 0 34px rgba(255,43,214,.6), 0 0 60px rgba(255,43,214,.35);
    animation: xpulse 3.2s ease-in-out infinite; }
.cx-title .w { color: var(--cyan); text-shadow: 0 0 8px rgba(0,229,255,.8), 0 0 28px rgba(0,229,255,.35); }
@keyframes xpulse { 0%,100% { filter: brightness(1); } 50% { filter: brightness(1.35); } }
.cx-sub { font-family:'Share Tech Mono',monospace; color:#7fe9d2; letter-spacing:2px; font-size:15px; margin-bottom: 8px; }

/* Buttons */
.stButton > button, .stDownloadButton > button, .stFormSubmitButton > button {
    background: rgba(0,0,0,.85) !important; color: var(--mint) !important;
    border: 1.5px solid var(--mint) !important; border-radius: 10px !important;
    font-family: 'Orbitron', sans-serif !important; font-weight: 700 !important; letter-spacing: 1.5px;
    box-shadow: 0 0 8px rgba(0,255,198,.35), inset 0 0 8px rgba(0,255,198,.12); transition: all .15s ease;
}
.stButton > button p, .stDownloadButton > button p, .stFormSubmitButton > button p { font-family:'Orbitron',sans-serif !important; font-size: 14px !important; color: inherit !important; }
.stButton > button:hover, .stDownloadButton > button:hover, .stFormSubmitButton > button:hover {
    background: rgba(0,255,198,.12) !important; color: #fff !important;
    box-shadow: 0 0 14px rgba(0,255,198,.8), inset 0 0 12px rgba(0,255,198,.25);
}
.stButton > button[kind="primary"] { color: var(--magenta) !important; border-color: var(--magenta) !important;
    box-shadow: 0 0 10px rgba(255,43,214,.5), inset 0 0 10px rgba(255,43,214,.15); }
.stButton > button[kind="primary"]:hover { background: rgba(255,43,214,.14) !important; box-shadow: 0 0 18px rgba(255,43,214,.9); }

/* Inputs */
[data-testid="stTextInput"] input, [data-baseweb="select"] > div {
    background: #05080a !important; color: #fff !important; border: 1.5px solid var(--cyan) !important;
    border-radius: 10px !important; font-family: 'Share Tech Mono', monospace !important; font-size: 20px !important; letter-spacing: 4px;
    box-shadow: 0 0 8px rgba(0,229,255,.3);
}
[data-testid="stForm"] { border: 1px solid rgba(0,229,255,.35) !important; border-radius: 14px; background: rgba(0,10,14,.6); }
[data-testid="stExpander"] { border: 1px solid rgba(0,255,198,.35) !important; border-radius: 14px !important; background: rgba(0,12,10,.6); }
[data-testid="stExpander"] summary p { font-family:'Orbitron',sans-serif !important; color: var(--mint) !important; letter-spacing:1.5px; }
[data-testid="stAlert"] { background: rgba(0,255,198,.07) !important; border: 1px solid rgba(0,255,198,.45) !important; border-radius: 12px; }
[data-testid="stAlert"] p { color: var(--text) !important; }
[data-testid="stMetric"] { background: rgba(0,0,0,.7); border: 1px solid rgba(0,229,255,.35); border-radius: 12px; padding: 8px 12px; }
[data-testid="stMetricValue"] { font-family:'Orbitron',sans-serif; color: var(--mint) !important; text-shadow: 0 0 8px rgba(0,255,198,.6); }
[data-testid="stMetricLabel"] p { color: #8fd9c7 !important; font-size: 13px !important; letter-spacing: 1px; }

/* Ring dials: keep all 6 side by side, even on phones */
.st-key-dials [data-testid="stHorizontalBlock"] { flex-wrap: nowrap !important; gap: 6px !important; }
.st-key-dials [data-testid="stColumn"], .st-key-dials [data-testid="column"] { min-width: 0 !important; flex: 1 1 0 !important; width: auto !important; }
.st-key-dials .stButton > button { padding: 2px 0 !important; min-height: 34px; }
.ring-face { text-align:center; font-family:'Share Tech Mono',monospace; font-weight:700; font-size: 34px; color:#fff;
    background: radial-gradient(circle at 50% 40%, rgba(0,255,198,.22), rgba(0,0,0,.9) 70%);
    border: 1.5px solid var(--mint); border-radius: 10px; margin: 4px 0; padding: 2px 0;
    text-shadow: 0 0 8px var(--mint), 0 0 20px var(--mint); box-shadow: 0 0 10px rgba(0,255,198,.4); }
.ring-face.off { color:#3d6b60; text-shadow:none; border-color: rgba(0,255,198,.3); box-shadow:none; }
.ring-no { text-align:center; font-family:'Orbitron',sans-serif; font-size: 11px; color:#7fe9d2; letter-spacing:1px; }

.neon-gift { color: var(--mint); font-weight:700; text-shadow: 0 0 6px rgba(0,255,198,.7); }
.neon-intent { color: var(--magenta); font-weight:700; text-shadow: 0 0 6px rgba(255,43,214,.7); }
.panel { border:1px solid rgba(0,255,198,.35); border-radius:14px; padding: 14px 18px; background: rgba(0,10,8,.65); margin: 6px 0 12px 0; }
.panel.intent { border-color: rgba(255,43,214,.45); background: rgba(14,0,10,.6); }
.chipline span { display:inline-block; margin: 3px 4px 3px 0; padding: 2px 10px; border-radius: 999px; font-family:'Share Tech Mono',monospace; font-size:16px; letter-spacing:1.5px; }
.chipline .g { color: var(--mint); border:1px solid var(--mint); box-shadow: 0 0 6px rgba(0,255,198,.4); }
.chipline .i { color: var(--magenta); border:1px solid var(--magenta); box-shadow: 0 0 6px rgba(255,43,214,.4); }
</style>
""", unsafe_allow_html=True)


# ============================================================ LEXICON
@st.cache_resource(show_spinner=False)
def get_tiers():
    return C.load_tiers()


@st.cache_resource(show_spinner=False)
def get_lookup(enabled, clean_mode):
    tiers, clean_filter = get_tiers()
    return C.build_lookup(tiers, clean_filter, set(enabled), clean_mode)


TIERS_DATA, _ = get_tiers()

# ============================================================ STATE
ss = st.session_state
ss.setdefault("journal", [])
ss.setdefault("offsets", [C.DEVICE_ALPHA.index(c) for c in "ORACLE"])
ss.setdefault("active_len", 6)


def main_word():
    return "".join(C.DEVICE_ALPHA[ss.offsets[c]] for c in range(ss.active_len))


def rotate_ring(i, step):
    ss.offsets[i] = (ss.offsets[i] + step) % 26
    if i >= ss.active_len:          # dialing a ring outside the word extends the word to include it
        ss.active_len = i + 1


# ============================================================ HEADER
st.markdown('<div class="cx-title">CRYPTE<span class="x">X</span> <span class="w">WERD</span></div>'
            '<div class="cx-sub">// 6-RING CIPHER CYLINDER · 26 ROWS · EVERY DIRECTION //</div>',
            unsafe_allow_html=True)

# ============================================================ SEARCH SETTINGS
with st.expander("⚙️  Lexicon & search settings", expanded=False):
    s1, s2 = st.columns(2)
    with s1:
        st.markdown("**Word sources**")
        enabled = []
        for key, _f, label, default, _r in C.TIERS:
            n = len(TIERS_DATA.get(key, ()))
            if st.checkbox(f"{label}  ({n:,})", value=default, key=f"tier_{key}"):
                enabled.append(key)
        clean_mode = st.toggle("Clean mode (hide swears & adult words)", value=False)
    with s2:
        st.markdown("**Directions**")
        use_h = st.checkbox("Horizontal  →  ←", value=True)
        use_d = st.checkbox("Diagonal  ↘ ↗  ↖ ↙", value=True)
        use_v = st.checkbox("Vertical  ↓ ↑  (same every spin — each ring is a fixed alphabet)", value=False)
        min_len = st.select_slider("Shortest word", options=[3, 4, 5, 6], value=3)
        hide_nested = st.checkbox("Hide small words sitting inside bigger ones (e.g. EAR in HEART)", value=True)

lookup = get_lookup(tuple(sorted(enabled)), clean_mode)

# ============================================================ CONTROLS
c1, c2 = st.columns([1, 1])
with c1:
    if st.button("🎲  RANDOM SPIN", use_container_width=True, type="primary"):
        ss.offsets = [random.randint(0, 25) for _ in range(6)]
        ss.active_len = 6
        st.rerun()
with c2:
    with st.form("align", clear_on_submit=False, border=True):
        w_input = st.text_input("Set word (up to 6 letters)", placeholder="LOVE · DREAM · ORACLE",
                                label_visibility="collapsed")
        if st.form_submit_button("🎯  ALIGN WORD", use_container_width=True):
            clean = "".join(ch for ch in w_input.upper() if ch in C.DEVICE_ALPHA)[:6]
            if clean:
                for i, ch in enumerate(clean):
                    ss.offsets[i] = C.DEVICE_ALPHA.index(ch)
                ss.active_len = len(clean)
                st.rerun()
            else:
                st.warning("Type at least one letter A–Z.")

st.markdown("#### ◈ Dial the rings")
with st.container(key="dials"):
    cols = st.columns(6)
    for i, col in enumerate(cols):
        with col:
            if st.button("▲", key=f"u_{i}", use_container_width=True):
                rotate_ring(i, -1)
                st.rerun()
            on = i < ss.active_len
            st.markdown(f"<div class='ring-face{'' if on else ' off'}'>{C.DEVICE_ALPHA[ss.offsets[i]]}</div>"
                        f"<div class='ring-no'>RING {i + 1}</div>", unsafe_allow_html=True)
            if st.button("▼", key=f"d_{i}", use_container_width=True):
                rotate_ring(i, 1)
                st.rerun()

# ============================================================ SEARCH
word = main_word()
active_len = ss.active_len
grid = C.build_grid(ss.offsets)
found = C.find_words(grid, lookup, min_len=min_len, horizontal=use_h, diagonal=use_d,
                     vertical=use_v, hide_nested=hide_nested)
gifts = C.group_words(found, "gift")
intents = C.group_words(found, "intent")
num = C.numerology(word)
total_num, num_title, num_desc, num_guidance = num

st.write("---")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Main word", word)
m2.metric("Vibration", f"{total_num} · {num_title.replace('The ', '')}")
m3.metric("Gifts (forward)", len(gifts))
m4.metric("Intents (backward)", len(intents))

# ============================================================ CYLINDER FACE (interactive)
gift_cells = {cell for o in found if o["kind"] == "gift" for cell in o["cells"]}
intent_cells = {cell for o in found if o["kind"] == "intent" for cell in o["cells"]}


def chip_html(groups, kind):
    if not groups:
        return "<div class='none'>none found</div>"
    out = []
    for w, tier, occ in groups:
        ids = " ".join(f"c{r}_{c}" for o in occ for r, c in o["cells"])
        arrows = "".join(sorted({o["arrow"] for o in occ}))
        count = f"<sup>×{len(occ)}</sup>" if len(occ) > 1 else ""
        out.append(f"<button class='chip {kind} t-{tier}' data-cells='{ids}' title='{C.TIER_LABEL[tier]}'>"
                   f"{w}<span class='ar'>{arrows}</span>{count}</button>")
    return "".join(out)


rows_html = []
for r in range(C.ROWS):
    lab = C.row_label(r)
    cells = []
    for c in range(C.RINGS):
        cls = ["t"]
        if r == C.CENTER:
            cls.append("m" if c < active_len else "mo")
        if (r, c) in gift_cells:
            cls.append("g")
        if (r, c) in intent_cells:
            cls.append("i")
        cells.append(f"<div id='c{r}_{c}' class='{' '.join(cls)}'>{grid[r][c]}</div>")
    rows_html.append(f"<div class='row{' main' if r == C.CENTER else ''}' {'id=mainrow' if r == C.CENTER else ''}>"
                     f"<div class='lab'>{'► MAIN' if lab == 'MAIN' else lab}</div>{''.join(cells)}</div>")

face = f"""<!DOCTYPE html><html><head>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>
:root {{ --mint:{MINT}; --cyan:{CYAN}; --magenta:{MAGENTA}; }}
* {{ box-sizing: border-box; }}
body {{ margin:0; background:transparent; color:#dffff6; font-family:'Share Tech Mono',monospace; }}
.wrap {{ display:flex; gap:16px; flex-wrap:wrap; }}
.cyl {{ flex: 0 0 auto; height: 560px; overflow-y:auto; padding: 10px; border-radius:16px; background:#020405;
       border:1.5px solid rgba(0,255,198,.5); box-shadow: 0 0 18px rgba(0,255,198,.25), inset 0 0 30px rgba(0,255,198,.06); }}
.row {{ display:flex; align-items:center; gap:6px; padding:3px 6px; border-radius:8px; }}
.row.main {{ background: linear-gradient(90deg, rgba(0,255,198,.05), rgba(0,255,198,.18), rgba(0,255,198,.05));
            outline: 1.5px solid var(--mint); box-shadow: 0 0 14px rgba(0,255,198,.55); margin: 4px 0; }}
.lab {{ width:62px; font-size:13px; color:#6fbfae; text-align:right; padding-right:6px; }}
.row.main .lab {{ color: var(--mint); font-family:'Orbitron',sans-serif; font-size:11px; text-shadow:0 0 6px var(--mint); }}
.t {{ width:38px; height:38px; line-height:38px; text-align:center; font-size:22px; font-weight:700; border-radius:7px;
     background:#0a1012; color:#7c9a94; border:1px solid #13221f; transition: all .12s ease; }}
.t.g {{ color: var(--mint); border-color: rgba(0,255,198,.7); background: rgba(0,255,198,.08); text-shadow:0 0 8px var(--mint); }}
.t.i {{ color: var(--magenta); border-color: rgba(255,43,214,.7); background: rgba(255,43,214,.08); text-shadow:0 0 8px var(--magenta); }}
.t.g.i {{ color:#fff; background: linear-gradient(135deg, rgba(0,255,198,.22) 50%, rgba(255,43,214,.22) 50%); border-color:#fff;
         text-shadow: 0 0 8px #fff; }}
.t.m {{ color:#fff; font-size:24px; background: rgba(0,255,198,.2); border:1.5px solid var(--mint); text-shadow: 0 0 10px var(--mint), 0 0 20px var(--mint); }}
.t.mo {{ color:#3d6b60; }}
.t.spot {{ background: #fff !important; color:#000 !important; text-shadow:none !important; transform: scale(1.12);
          box-shadow: 0 0 14px #fff, 0 0 28px var(--cyan); border-color:#fff !important; z-index:2; }}
.side {{ flex: 1 1 280px; min-width: 260px; height: 560px; overflow-y:auto; padding: 12px 14px; border-radius:16px; background:#020405;
        border:1.5px solid rgba(0,229,255,.4); box-shadow: 0 0 18px rgba(0,229,255,.18); }}
h3 {{ font-family:'Orbitron',sans-serif; font-size:14px; letter-spacing:2px; margin: 4px 0 8px 0; }}
h3.g {{ color: var(--mint); text-shadow: 0 0 8px var(--mint); }}
h3.i {{ color: var(--magenta); text-shadow: 0 0 8px var(--magenta); margin-top: 16px; }}
.hint {{ font-size:13px; color:#7fb8ad; margin-bottom: 8px; line-height:1.4; }}
.chip {{ font-family:'Share Tech Mono',monospace; font-size:17px; letter-spacing:1.5px; padding:4px 10px; margin:3px 3px 3px 0;
        border-radius:999px; background:#000; cursor:pointer; }}
.chip.gift {{ color: var(--mint); border:1px solid var(--mint); box-shadow:0 0 6px rgba(0,255,198,.35); }}
.chip.intent {{ color: var(--magenta); border:1px solid var(--magenta); box-shadow:0 0 6px rgba(255,43,214,.35); }}
.chip.t-dictionary {{ opacity:.85; }} .chip.t-deep {{ opacity:.65; border-style:dashed; }}
.chip.on {{ background:#fff; color:#000; box-shadow: 0 0 14px #fff; }}
.chip .ar {{ font-size: 13px; margin-left: 5px; opacity:.85; }}
.chip sup {{ font-size: 11px; margin-left: 2px; }}
.none {{ color:#557; font-size:14px; }}
</style></head><body>
<div class="wrap">
  <div class="cyl" id="cyl">{''.join(rows_html)}</div>
  <div class="side">
    <div class="hint">Tap a word to light up its path on the cylinder. Tap again to clear.</div>
    <h3 class="g">◆ GIFTS — forward ({len(gifts)})</h3>{chip_html(gifts, 'gift')}
    <h3 class="i">◇ INTENTS — backward ({len(intents)})</h3>{chip_html(intents, 'intent')}
  </div>
</div>
<script>
const cyl = document.getElementById('cyl'), main = document.getElementById('mainrow');
cyl.scrollTop = main.offsetTop - cyl.clientHeight / 2 + main.clientHeight / 2;
document.querySelectorAll('.chip').forEach(ch => ch.addEventListener('click', () => {{
  const was = ch.classList.contains('on');
  document.querySelectorAll('.chip.on').forEach(x => x.classList.remove('on'));
  document.querySelectorAll('.t.spot').forEach(x => x.classList.remove('spot'));
  if (was) return;
  ch.classList.add('on');
  let first = null;
  ch.dataset.cells.split(' ').forEach(id => {{ const el = document.getElementById(id); if (el) {{ el.classList.add('spot'); first = first || el; }} }});
  if (first) {{ const row = first.parentElement; if (row.offsetTop < cyl.scrollTop || row.offsetTop > cyl.scrollTop + cyl.clientHeight - 40)
      cyl.scrollTo({{ top: row.offsetTop - cyl.clientHeight / 3, behavior: 'smooth' }}); }}
}}));
</script></body></html>"""

st.markdown("### ◈ The whole cylinder face")
st.caption("All 26 rows unrolled. Mint = GIFT (read forward, left → right). "
           "Magenta = INTENT (read backward, right → left). Split tiles belong to both.")
components.html(face, height=580, scrolling=False)

# ============================================================ READING
st.write("---")
st.markdown(f"## 🔮 Oracle reading · {word}")
st.markdown(f"#### Archetype: {num_title} — Vibration {total_num}")
st.markdown(f"**Core essence:** *{num_desc}*")
st.markdown(f"**Guidance for {word}:** {num_guidance}")
st.markdown("**Letter vibrations:** " + " · ".join(
    f"**{c}**={C.PYTHAGOREAN_VALUES.get(c, 0)} ({C.LETTER_MEANINGS.get(c, '')})" for c in word))


def chipline(groups, cls, limit=24):
    if not groups:
        return "<i>none found</i>"
    extra = f" <span style='border:none;color:#8fd9c7'>+{len(groups) - limit} more</span>" if len(groups) > limit else ""
    return "<div class='chipline'>" + "".join(f"<span class='{cls}'>{w}</span>" for w, _, _ in groups[:limit]) + extra + "</div>"


st.markdown(f"<div class='panel'><span class='neon-gift'>◆ GIFTS</span> — what is being given to you (forward words)"
            f"{chipline(gifts, 'g')}</div>", unsafe_allow_html=True)
st.markdown(f"<div class='panel intent'><span class='neon-intent'>◇ INTENTS</span> — the will beneath it (backward words)"
            f"{chipline(intents, 'i')}</div>", unsafe_allow_html=True)
story = C.synthesis(word, gifts, intents, num_desc)
st.success(f"**Circumference synthesis:** {story}")

# ============================================================ SAVE / PRINT
settings_desc = (f"sources={', '.join(enabled) or 'none'}; directions="
                 f"{'H ' if use_h else ''}{'D ' if use_d else ''}{'V ' if use_v else ''}; "
                 f"min length={min_len}; nested={'hidden' if hide_nested else 'shown'}; clean={'on' if clean_mode else 'off'}")
stamp = time.strftime('%Y%m%d_%H%M%S')

st.write("---")
st.markdown("#### ◈ Save & print")
d1, d2, d3 = st.columns(3)
with d1:
    st.download_button("📄  TEXT FILE (.txt)",
                       data=C.build_text_report(word, active_len, grid, found, gifts, intents, num, settings_desc),
                       file_name=f"cryptex_{word.lower()}_{stamp}.txt", mime="text/plain", use_container_width=True,
                       help="Plain text with every letter in its own column — open in any editor and print. "
                            "Includes the full cylinder, a GIFT map, an INTENT map and the word lists.")
with d2:
    st.download_button("🖨️  PRINTABLE PAGE (.html)",
                       data=C.build_print_html(word, active_len, grid, found, gifts, intents, num),
                       file_name=f"cryptex_{word.lower()}_{stamp}.html", mime="text/html", use_container_width=True,
                       help="Open in a browser and print (or Save as PDF). Colored grid, ink-friendly.")
with d3:
    if st.button("💾  SAVE TO LOG", use_container_width=True):
        ss.journal.append({"time": time.strftime("%Y-%m-%d %H:%M:%S"), "word": word, "num": total_num,
                           "title": num_title, "guidance": num_guidance,
                           "gifts": [w for w, _, _ in gifts[:10]], "intents": [w for w, _, _ in intents[:10]],
                           "story": story})
        st.toast("Reading saved to your log.")

# ============================================================ LOG
if ss.journal:
    with st.expander(f"📖  Saved readings log ({len(ss.journal)})", expanded=False):
        log_lines = []
        for idx, e in enumerate(reversed(ss.journal)):
            n = len(ss.journal) - idx
            st.markdown(f"**#{n} · {e['word']}** — Vibration {e['num']} ({e['title']}) · *{e['time']}*")
            if e["gifts"]:
                st.markdown(f"<span class='neon-gift'>Gifts:</span> {', '.join(e['gifts'])}", unsafe_allow_html=True)
            if e["intents"]:
                st.markdown(f"<span class='neon-intent'>Intents:</span> {', '.join(e['intents'])}", unsafe_allow_html=True)
            st.markdown(f"> {e['story']}")
            st.markdown("---")
        for n, e in enumerate(ss.journal, 1):
            log_lines += [f"#{n}  {e['time']}  {e['word']}  (Vibration {e['num']} - {e['title']})",
                          f"    Gifts:   {', '.join(e['gifts']) or '-'}",
                          f"    Intents: {', '.join(e['intents']) or '-'}",
                          f"    {e['story']}", ""]
        st.download_button("📥  DOWNLOAD LOG (.txt)", data=C._ascii("\n".join(log_lines)),
                           file_name=f"cryptex_log_{stamp}.txt", mime="text/plain")
        st.caption("The log lives in this browser session — download it before closing the tab.")
