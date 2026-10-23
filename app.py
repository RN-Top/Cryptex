import streamlit as st
import streamlit.components.v1 as components
import random
import os
import time

st.set_page_config(page_title="Cryptex werd", page_icon="🗝️", layout="wide")

# Drew's 26-letter Pythagorean reduction alphabet:
DEVICE_ALPHA = "AJSBKTCLUDMVENWFOXGPYHQZIR"

PYTHAGOREAN_VALUES = {
    'A':1, 'J':1, 'S':1, 'B':2, 'K':2, 'T':2, 'C':3, 'L':3, 'U':3,
    'D':4, 'M':4, 'V':4, 'E':5, 'N':5, 'W':5, 'F':6, 'O':6, 'X':6,
    'G':7, 'P':7, 'Y':7, 'H':8, 'Q':8, 'Z':8, 'I':9, 'R':9
}

NUMEROLOGY_THEMES = {
    1: ("The Pioneer", "New beginnings, bold initiative, independence, and raw potential."),
    2: ("The Mirror", "Partnership, balance, intuition, and diplomatic harmony."),
    3: ("The Spark", "Creative expansion, joyous self-expression, and communication."),
    4: ("The Anchor", "Stability, discipline, grounded structure, and order."),
    5: ("The Catalyst", "Freedom, dynamic movement, curiosity, and transformation."),
    6: ("The Guardian", "Nurturing love, protective balance, and community healing."),
    7: ("The Mystic", "Deep introspection, analytical truth, and spiritual search."),
    8: ("The Crown", "Manifestation, power, material mastery, and ambition."),
    9: ("The Sage", "Universal wisdom, culmination, compassion, and completion.")
}

COMMON_WORDS = {
    "THE", "AND", "FOR", "ARE", "WITH", "THIS", "HAVE", "FROM", "WORD", "WHAT",
    "SOME", "WERE", "THERE", "WHEN", "YOUR", "TIME", "WILL", "ABOUT", "MANY",
    "THEN", "WRITE", "WOULD", "LIKE", "LONG", "MAKE", "THING", "LOOK", "MORE",
    "COME", "NUMBER", "SOUND", "MOST", "WATER", "CALL", "FIRST", "DOWN", "FIND",
    "PART", "TAKE", "PLACE", "MADE", "LIVE", "BACK", "LITTLE", "ROUND", "YEAR",
    "CAME", "SHOW", "GOOD", "GIVE", "NAME", "VERY", "FORM", "GREAT", "THINK",
    "HELP", "LINE", "TURN", "CAUSE", "MUCH", "MEAN", "MOVE", "RIGHT", "SAME",
    "TELL", "WANT", "WELL", "PLAY", "HOME", "READ", "HAND", "PORT", "LARGE",
    "SPELL", "EVEN", "LAND", "HERE", "MUST", "HIGH", "FOLLOW", "CHANGE", "LIGHT",
    "KIND", "NEED", "HOUSE", "POINT", "WORLD", "BUILD", "EARTH", "HEAD", "STAND",
    "PAGE", "FOUND", "ANSWER", "GROW", "STUDY", "PLANT", "COVER", "FOOD", "STATE",
    "KEEP", "NEVER", "LAST", "CITY", "TREE", "CROSS", "FARM", "HARD", "START",
    "MIGHT", "STORY", "DRAW", "LATE", "PRESS", "CLOSE", "NIGHT", "REAL", "LIFE",
    "NORTH", "OPEN", "SEEM", "NEXT", "WHITE", "BEGIN", "WALK", "PAPER", "GROUP",
    "MUSIC", "BOTH", "MARK", "OFTEN", "LETTER", "MILE", "RIVER", "FEET", "CARE",
    "BOOK", "RAIN", "ROOM", "FRIEND", "IDEA", "FISH", "STOP", "BASE", "HEAR",
    "HORSE", "SURE", "WATCH", "COLOR", "FACE", "WOOD", "MAIN", "GIRL", "YOUNG",
    "READY", "ABOVE", "EVER", "LIST", "FEEL", "TALK", "BIRD", "SOON", "BODY",
    "FAMILY", "DIRECT", "LEAVE", "SONG", "DOOR", "BLACK", "SHORT", "CLASS", "WIND",
    "SHIP", "AREA", "HALF", "ROCK", "ORDER", "FIRE", "SOUTH", "PIECE", "TOLD",
    "PASS", "SINCE", "WHOLE", "KING", "SPACE", "HEARD", "BEST", "HOUR", "TRUE",
    "FIVE", "STEP", "EARLY", "HOLD", "WEST", "GROUND", "REACH", "FAST", "SING",
    "LISTEN", "TABLE", "TRAVEL", "LESS", "SIMPLE", "CENTER", "LOVE", "PERSON",
    "MONEY", "SERVE", "ROAD", "RULE", "PULL", "COLD", "VOICE", "POWER", "TOWN",
    "FINE", "FALL", "LEAD", "DARK", "WAIT", "PLAN", "STAR", "REST", "ABLE",
    "DONE", "DRIVE", "FRONT", "WEEK", "GAVE", "GREEN", "QUICK", "OCEAN", "WARM",
    "FREE", "MIND", "CLEAR", "STREET", "STAY", "WHEEL", "FULL", "FORCE", "BLUE",
    "DEEP", "MOON", "FOOT", "TEST", "BOAT", "GOLD", "PLANE", "GAME", "HEAT",
    "SNOW", "EAST", "SECRET", "ORACLE", "RIDDLE", "CIPHER", "TEMPLE", "SYMBOL",
    "DREAM", "TRUTH", "SPIRIT", "WISDOM", "VISION", "SHADOW", "FLOWER", "PLANET",
    "PATH", "GATE", "RING", "SUN", "SOUL", "HOPE", "PEACE", "SEEK", "GUIDE",
    "MAGIC", "RISING", "SHINE", "QUEST", "POWER", "VOICE", "HEART", "RIVER",
    "VEX", "FIR", "LUN", "ENG", "MVO", "COMBO"
}

@st.cache_resource(show_spinner=False)
def load_words():
    words = set(COMMON_WORDS)
    dict_path = os.path.join(os.path.dirname(__file__), "words.txt")
    if os.path.exists(dict_path):
        try:
            with open(dict_path, "r", encoding="utf-8") as f:
                for line in f:
                    w = line.strip().upper()
                    if 3 <= len(w) <= 6 and w.isalpha():
                        words.add(w)
        except:
            pass
    return words

DICTIONARY = load_words()

# --- State ---
if "journal" not in st.session_state:
    st.session_state.journal = []

if "offsets" not in st.session_state:
    st.session_state.offsets = [DEVICE_ALPHA.index(c) for c in "ORACLE"]

if "main_word" not in st.session_state:
    st.session_state.main_word = "ORACLE"

def rotate_ring(i, step):
    st.session_state.offsets[i] = (st.session_state.offsets[i] + step) % 26
    st.session_state.main_word = "".join(DEVICE_ALPHA[st.session_state.offsets[c]] for c in range(6))

st.title("🗝️ Cryptex werd")
st.caption("All 26 rows unrolled in full view. Works with words up to 6 letters.")

# --- Top Controls: Spin & Word Alignment ---
c1, c2 = st.columns([1, 1])
with c1:
    if st.button("🎲 Random Spin All Rings", use_container_width=True, type="primary"):
        st.session_state.offsets = [random.randint(0, 25) for _ in range(6)]
        st.session_state.main_word = "".join(DEVICE_ALPHA[st.session_state.offsets[c]] for c in range(6))
        st.rerun()

with c2:
    # Character limit removed so your keyboard can freely type 6 letters
    w_input = st.text_input("Set Word (Up to 6 Letters)", placeholder="e.g. LOVE, DREAM, ORACLE, SECRET").strip().upper()
    if st.button("🎯 Align Word", use_container_width=True):
        clean = "".join(c for c in w_input if c in DEVICE_ALPHA)[:6]
        if clean:
            st.session_state.main_word = clean
            for i, char in enumerate(clean):
                st.session_state.offsets[i] = DEVICE_ALPHA.index(char)
            st.rerun()

st.write("---")

# --- Column Dials for the 6 Rings ---
st.markdown("#### Dial Individual Rings:")
btn_cols = st.columns(6)
for i, col in enumerate(btn_cols):
    with col:
        if st.button("▲", key=f"u_{i}", use_container_width=True):
            rotate_ring(i, -1)
            st.rerun()
        cur = DEVICE_ALPHA[st.session_state.offsets[i]]
        st.markdown(f"<div style='text-align:center; font-weight:bold; font-size:18px; color:#ffd700; background:#222429; border-radius:4px; padding:2px;'>Ring {i+1}: {cur}</div>", unsafe_allow_html=True)
        if st.button("▼", key=f"d_{i}", use_container_width=True):
            rotate_ring(i, 1)
            st.rerun()

st.write("---")

# --- Scan All 26 Rows and Build the Full-Face View ---
main_word = st.session_state.main_word
active_len = len(main_word)

total_num = sum(PYTHAGOREAN_VALUES.get(c, 0) for c in main_word)
while total_num > 9:
    total_num = sum(int(d) for d in str(total_num))
num_title, num_desc = NUMEROLOGY_THEMES.get(total_num, ("The Seeker", "Mysterious potential."))

all_orbit_words = []
rows_data = []

# Scan all 26 rows around the cylinder (-12 to +13)
for shift in range(-12, 14):
    row_chars = [DEVICE_ALPHA[(st.session_state.offsets[c] + shift) % 26] for c in range(6)]
    row_str = "".join(row_chars)
    
    # Detect valid English words
    found_words = []
    for length in [6, 5, 4, 3]:
        for start in range(7 - length):
            sub = row_str[start:start+length]
            if sub in DICTIONARY and sub not in [x[0] for x in found_words]:
                found_words.append((sub, start, length))
    
    # Mark which letter positions are part of a detected word
    highlight_mask = [False] * 6
    for sub, start, length in found_words:
        for idx in range(start, start + length):
            highlight_mask[idx] = True
            
    is_center = (shift == 0)
    label = "► MAIN (Row 0)" if is_center else f"  Row {shift:+d}"
    
    word_names = [x[0] for x in found_words]
    if not is_center:
        all_orbit_words.extend(word_names)
        
    rows_data.append({
        "shift": shift,
        "is_center": is_center,
        "label": label,
        "chars": row_chars,
        "mask": highlight_mask,
        "words": word_names
    })

# --- Build Full-Face HTML Table ---
table_html = """
<!DOCTYPE html>
<html>
<head>
<style>
    body { margin: 0; padding: 4px; background: transparent; font-family: -apple-system, sans-serif; color: #eee; }
    .matrix-wrapper {
        background: #111317;
        border: 2px solid #554422;
        border-radius: 12px;
        padding: 10px;
        max-height: 480px;
        overflow-y: auto;
        box-sizing: border-box;
    }
    .row-line {
        display: flex;
        align-items: center;
        padding: 4px 6px;
        margin-bottom: 4px;
        border-radius: 6px;
        background: #1a1c22;
    }
    .row-center {
        background: linear-gradient(90deg, #3d2f0a, #5c4710, #3d2f0a);
        border: 2px solid #ffd700;
        box-shadow: 0 0 10px rgba(255, 215, 0, 0.4);
    }
    .row-active-word {
        background: #18261e;
        border-left: 3px solid #2ecc71;
    }
    .label-col {
        width: 130px;
        font-size: 13px;
        font-weight: 700;
        color: #b0aba0;
    }
    .label-center {
        color: #ffd700;
        font-size: 14px;
    }
    .tiles-col {
        display: flex;
        gap: 6px;
        margin-right: 15px;
    }
    .tile {
        width: 32px;
        height: 32px;
        line-height: 32px;
        text-align: center;
        font-family: monospace;
        font-size: 18px;
        font-weight: 700;
        border-radius: 4px;
        background: #252830;
        color: #ccc;
    }
    .tile-center {
        background: linear-gradient(180deg, #d4af37, #8b6508);
        color: #fff;
        font-size: 20px;
        font-weight: 900;
    }
    .tile-dim {
        background: #1c1d22;
        color: #444;
    }
    .tile-highlight {
        background: #1b5e20;
        color: #a5d6a7;
        box-shadow: 0 0 6px #4caf50;
        border: 1px solid #81c784;
    }
    .words-col {
        font-size: 13px;
        font-weight: 600;
        color: #81c784;
    }
</style>
</head>
<body>
<div class="matrix-wrapper">
"""

for row in rows_data:
    row_class = "row-line"
    if row["is_center"]:
        row_class += " row-center"
    elif row["words"]:
        row_class += " row-active-word"
        
    label_class = "label-col label-center" if row["is_center"] else "label-col"
    
    tiles_str = ""
    for c_idx, char in enumerate(row["chars"]):
        tile_class = "tile"
        display_char = char
        if row["is_center"]:
            if c_idx < active_len:
                tile_class += " tile-center"
            else:
                tile_class += " tile-dim"
                display_char = "·"
        elif row["mask"][c_idx]:
            tile_class += " tile-highlight"
        tiles_str += f'<div class="{tile_class}">{display_char}</div>'
        
    words_str = ", ".join(row["words"]) if row["words"] else ""
    if words_str:
        words_html = f'<div class="words-col">⭐ {words_str}</div>'
    else:
        words_html = '<div class="words-col" style="color:#555;">-</div>'
        
    table_html += f"""
    <div class="{row_class}">
        <div class="{label_class}">{row['label']}</div>
        <div class="tiles-col">{tiles_str}</div>
        {words_html}
    </div>
    """

table_html += "</div></body></html>"

st.markdown("### 📜 The Whole Cylinder Face (All 26 Rows Unrolled)")
st.caption("Every row around the cylinder is shown below. Letters that connect into words glow in green. The Center row is your Main Word.")

components.html(table_html, height=500)

st.write("---")

# --- Form The Reading ---
unique_words = sorted(list(set(all_orbit_words)), key=lambda w: (-len(w), w))

st.subheader(f"🔮 The Reading for **{main_word}**")
st.markdown(f"**Vibration Frequency {total_num} — {num_title}:** *{num_desc}*")

if unique_words:
    words_badges = ", ".join(f"**{w}**" for w in unique_words[:8])
    story_text = (
        f"As the cylinder matrix connects across all 26 rows, the primary energy of {main_word} ({num_title}) "
        f"is surrounded by the echoes of {', '.join(unique_words[:8])}. "
        f"This reading indicates that {main_word} calls for {num_desc.lower()} "
        f"Draw guidance from {unique_words[0]} as your central lesson, and look to {unique_words[-1]} for your next step forward."
    )
    st.success(
        f"**Main Word Alignment:** `{main_word}`\n\n"
        f"**Words Discovered Around the Cylinder Face:** {words_badges}\n\n"
        f"**Oracle Interpretation:** {story_text}"
    )
    
    # --- Build Complete Downloadable Text File (Full Rolled-Out Visual) ---
    file_lines = [
        "=" * 78,
        "🗝️ CRYPTEX WERD — COMPLETE CYLINDER ORACLE READING",
        "=" * 78,
        f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"Main Word: {main_word} (Length: {active_len} letters)",
        f"Pythagorean Vibration: Number {total_num} — {num_title}",
        f"Vibrational Theme: {num_desc}",
        "",
        "=" * 78,
        "FULL ROLLED-OUT WRITTEN VISUAL MATRIX (ALL 26 ROWS ACROSS CYLINDER)",
        "=" * 78,
        f"  {'ROW OFFSET':<14} |  {'RINGS 1 - 6':<13} | WORDS FORMED",
        "-" * 16 + "+" + "-" * 17 + "+" + "-" * 43
    ]
    for r in rows_data:
        if r['is_center']:
            chars_str = f"[{' '.join(r['chars'][:active_len])}]"
        else:
            chars_str = f" {' '.join(r['chars'])} "
        words_str = f"⭐ {', '.join(r['words'])}" if r['words'] else ""
        file_lines.append(f"{r['label']:<16} | {chars_str:<15} | {words_str}")
        
    file_lines.extend([
        "=" * 78,
        "ORACLE INTERPRETATION & READING SYNTHESIS",
        "=" * 78,
        f"Main Word Anchor: {main_word}",
        f"Orbiting Words Discovered: {', '.join(unique_words[:8])}",
        "",
        story_text,
        "=" * 78
    ])
    reading_file_content = "\n".join(file_lines)
    
    # Save & Download Buttons
    save_c1, save_c2 = st.columns(2)
    with save_c1:
        st.download_button(
            label="📥 Download Reading File (.txt)",
            data=reading_file_content,
            file_name=f"reading_{main_word.lower()}_{time.strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    with save_c2:
        if st.button("💾 Save to Reading Log", use_container_width=True):
            st.session_state.journal.append({
                "time": time.strftime("%Y-%m-%d %H:%M:%S"),
                "word": main_word,
                "num": total_num,
                "title": num_title,
                "words": unique_words[:8],
                "story": story_text
            })
            st.toast("Reading saved to your log!")
else:
    st.info(f"**{main_word}** is aligned on the main row. Dial individual rings or spin to discover words connecting around the face!")

# --- Saved Readings Log ---
if st.session_state.journal:
    st.write("---")
    with st.expander(f"📖 Saved Readings Log ({len(st.session_state.journal)} saved)", expanded=False):
        for idx, entry in enumerate(reversed(st.session_state.journal)):
            st.markdown(f"**#{len(st.session_state.journal) - idx}: {entry['word']} (Vibration {entry['num']} — {entry['title']})** — *{entry['time']}*")
            st.markdown(f"Words found: `{', '.join(entry['words'])}`")
            st.markdown(f"> {entry['story']}")
            st.markdown("---")
