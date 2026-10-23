import streamlit as st
import streamlit.components.v1 as components
import random
import os

st.set_page_config(page_title="Drew's Cryptex", page_icon="🗝️", layout="centered")

# Drew's 26-letter Pythagorean cipher alphabet
DEVICE_ALPHA = "AJSBKTCLUDMVENWFOXGPYHQZIR"

PYTHAGOREAN_VALUES = {
    'A':1, 'J':1, 'S':1, 'B':2, 'K':2, 'T':2, 'C':3, 'L':3, 'U':3,
    'D':4, 'M':4, 'V':4, 'E':5, 'N':5, 'W':5, 'F':6, 'O':6, 'X':6,
    'G':7, 'P':7, 'Y':7, 'H':8, 'Q':8, 'Z':8, 'I':9, 'R':9
}

NUMEROLOGY_THEMES = {
    1: ("The Pioneer", "New beginnings, bold initiative, independence, and raw potential."),
    2: ("The Mirror", "Partnership, balance, intuition, receptivity, and diplomatic harmony."),
    3: ("The Spark", "Creative expansion, joyous self-expression, communication, and enthusiasm."),
    4: ("The Anchor", "Stability, grounded structure, discipline, patience, and tangible results."),
    5: ("The Catalyst", "Freedom, dynamic movement, curiosity, travel, and sudden transformation."),
    6: ("The Guardian", "Nurturing love, domestic balance, protection, and heartfelt healing."),
    7: ("The Mystic", "Deep introspection, analytical wisdom, spiritual search, and inner mystery."),
    8: ("The Crown", "Manifestation, power, material mastery, ambition, and karmic balance."),
    9: ("The Sage", "Universal wisdom, culmination, compassion, completion, and higher perspective.")
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
    "MAGIC", "RISING", "SHINE", "QUEST", "POWER", "VOICE", "HEART", "RIVER"
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
if "offsets" not in st.session_state:
    st.session_state.offsets = [DEVICE_ALPHA.index(c) for c in "ORACLE"]

if "cylinder_shift" not in st.session_state:
    st.session_state.cylinder_shift = 0

def rotate_ring(i, step):
    st.session_state.offsets[i] = (st.session_state.offsets[i] + step) % 26

def get_center_word():
    return "".join(DEVICE_ALPHA[st.session_state.offsets[i]] for i in range(6))

st.title("🗝️ Drew's Cryptex")
st.caption("Based on Drew's Physical 6-Ring Cylinder Device")

# --- Render 3D Cylinder with Center and Surrounding Rows ---
shift = st.session_state.cylinder_shift
rings_html = ""
for i in range(6):
    off = (st.session_state.offsets[i] + shift) % 26
    m2 = DEVICE_ALPHA[(off - 2) % 26]
    m1 = DEVICE_ALPHA[(off - 1) % 26]
    c0 = DEVICE_ALPHA[off % 26]
    p1 = DEVICE_ALPHA[(off + 1) % 26]
    p2 = DEVICE_ALPHA[(off + 2) % 26]
    rings_html += (
        '<div class="ring-col">'
        f'<div class="char-faint">{m2}</div>'
        f'<div class="char-mid">{m1}</div>'
        f'<div class="char-target">{c0}</div>'
        f'<div class="char-mid">{p1}</div>'
        f'<div class="char-faint">{p2}</div>'
        '</div>'
    )

cylinder_iframe = (
    '<!DOCTYPE html><html><head><style>'
    'body { margin: 0; padding: 0; background: transparent; font-family: sans-serif; }'
    '.cylinder-box { display: flex; justify-content: center; gap: 8px; background: #151619; border: 3px solid #d4af37; border-radius: 12px; padding: 12px 6px; box-sizing: border-box; }'
    '.ring-col { display: flex; flex-direction: column; align-items: center; background: #222429; border: 1px solid #44351a; border-radius: 6px; width: 48px; }'
    '.char-faint { font-size: 14px; color: #555; height: 24px; line-height: 24px; }'
    '.char-mid { font-size: 18px; color: #999; height: 28px; line-height: 28px; }'
    '.char-target { font-size: 26px; font-weight: 900; color: #fff; background: linear-gradient(180deg, #d4af37, #8b6508); width: 100%; text-align: center; height: 42px; line-height: 42px; border-top: 2px solid #ffd700; border-bottom: 2px solid #ffd700; }'
    '</style></head><body>'
    f'<div class="cylinder-box">{rings_html}</div>'
    '</body></html>'
)

components.html(cylinder_iframe, height=195)

# --- Individual Ring Stepper Buttons ---
btn_cols = st.columns(6)
for i, col in enumerate(btn_cols):
    with col:
        if st.button("▲", key=f"u_{i}", use_container_width=True):
            rotate_ring(i, -1)
            st.rerun()
        cur = DEVICE_ALPHA[st.session_state.offsets[i]]
        st.markdown(f"<div style='text-align:center; font-weight:bold; color:#ffd700;'>{cur}</div>", unsafe_allow_html=True)
        if st.button("▼", key=f"d_{i}", use_container_width=True):
            rotate_ring(i, 1)
            st.rerun()

st.write("---")

# --- Quick Controls ---
c1, c2 = st.columns(2)
with c1:
    st.subheader("🎲 Spin Cylinder")
    if st.button("🎲 Random Spin", use_container_width=True, type="primary"):
        st.session_state.offsets = [random.randint(0, 25) for _ in range(6)]
        st.session_state.cylinder_shift = 0
        st.rerun()

with c2:
    st.subheader("🎯 Align Main Word")
    user_input = st.text_input("Enter 1-6 Letters", max_chars=6).strip().upper()
    if st.button("Set Main Word", use_container_width=True):
        clean = "".join(c for c in user_input if c in DEVICE_ALPHA)
        if clean:
            for i, char in enumerate(clean[:6]):
                st.session_state.offsets[i] = DEVICE_ALPHA.index(char)
            st.session_state.cylinder_shift = 0
            st.rerun()

st.write("---")

# --- Scan All 26 Rows Around the Main Word ---
main_word = get_center_word()
total_num = sum(PYTHAGOREAN_VALUES.get(c, 0) for c in main_word)
while total_num > 9:
    total_num = sum(int(d) for d in str(total_num))
num_title, num_desc = NUMEROLOGY_THEMES.get(total_num, ("The Seeker", "Mysterious potential."))

all_found_rows = []
all_orbit_words = []

for s in range(26):
    row_chars = "".join(DEVICE_ALPHA[(st.session_state.offsets[i] + s) % 26] for i in range(6))
    row_words = []
    for length in [6, 5, 4, 3]:
        for start in range(7 - length):
            sub = row_chars[start:start+length]
            if sub in DICTIONARY and sub not in row_words:
                row_words.append(sub)
    if row_words:
        label = "CENTER (Row 0)" if s == 0 else f"Row +{s}" if s <= 13 else f"Row -{26 - s}"
        all_found_rows.append((s, label, row_chars, row_words))
        if s != 0:
            all_orbit_words.extend(row_words)

# Unique words discovered around the main word
unique_surrounding = sorted(list(set(all_orbit_words)), key=lambda w: (-len(w), w))

# --- FORM THE READING ---
st.subheader(f"🔮 The Reading for **{main_word}**")
st.markdown(f"**Vibration Frequency {total_num} — {num_title}:** *{num_desc}*")

# Reading synthesis: weaving main word and surrounding words together
if unique_surrounding:
    words_highlight = ", ".join(f"**{w}**" for w in unique_surrounding[:6])
    story = (
        f"The focal anchor of this configuration is **{main_word}**. "
        f"As Drew's cylinder turns around its circumference, hidden echoes surface: {words_highlight}. "
        f"Together, these orbiting words reveal that **{main_word}** is connected to {num_desc.lower()} "
        f"Focus on **{unique_surrounding[0]}** as the primary lesson, while letting **{unique_surrounding[-1]}** guide your next step."
    )
    st.info(story)
else:
    st.info(f"**{main_word}** stands in solitary focus on the reading line. Rotate individual rings or spin to reveal its orbiting words.")

st.write("---")

# --- Circumference Explorer (Turn the whole cylinder) ---
st.subheader("📜 Inspect Words Formed Around the Cylinder")
st.write(f"Drew's cylinder has 26 rows around its circumference. Found **{len(all_found_rows)}** rows with valid English words:")

# Option to roll the whole cylinder to any row
roll_col1, roll_col2 = st.columns([3, 1])
with roll_col1:
    new_shift = st.slider("Rotate Entire Cylinder View (Row Offset)", min_value=0, max_value=25, value=st.session_state.cylinder_shift)
    if new_shift != st.session_state.cylinder_shift:
        st.session_state.cylinder_shift = new_shift
        st.rerun()

with roll_col2:
    if st.button("Reset to Center", use_container_width=True):
        st.session_state.cylinder_shift = 0
        st.rerun()

# Display all rows and their detected words
for s, label, row_chars, words in all_found_rows:
    is_active = (s == st.session_state.cylinder_shift)
    bullet = "🌟" if is_active else "•"
    word_str = ", ".join(words)
    if is_active:
        st.markdown(f"**{bullet} {label}:** `{row_chars}` $\\rightarrow$ :green[**{word_str}**] *(currently viewing)*")
    else:
        st.markdown(f"{bullet} **{label}:** `{row_chars}` $\\rightarrow$ :green[**{word_str}**]")
