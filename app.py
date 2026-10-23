import streamlit as st
import random
import time

# --- Page Setup ---
st.set_page_config(page_title="Drew's Cryptex", page_icon="🗝️", layout="centered")

# Drew's exact 26-letter Pythagorean reduction alphabet:
DEVICE_ALPHA = "AJSBKTCLUDMVENWFOXGPYHQZIR"

PYTHAGOREAN_VALUES = {
    'A':1, 'J':1, 'S':1, 'B':2, 'K':2, 'T':2, 'C':3, 'L':3, 'U':3,
    'D':4, 'M':4, 'V':4, 'E':5, 'N':5, 'W':5, 'F':6, 'O':6, 'X':6,
    'G':7, 'P':7, 'Y':7, 'H':8, 'Q':8, 'Z':8, 'I':9, 'R':9
}

NUMEROLOGY_THEMES = {
    1: "New beginnings, leadership, and bold forward action.",
    2: "Balance, partnership, intuition, and harmony.",
    3: "Creative expression, optimism, and joy.",
    4: "Stability, structure, discipline, and order.",
    5: "Dynamic change, freedom, travel, and transformation.",
    6: "Compassion, protection, love, and community.",
    7: "Introspection, mystery, and deep esoteric truth.",
    8: "Manifestation, power, authority, and abundance.",
    9: "Wisdom, completion, and spiritual culmination."
}

# Core dictionary
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
    "MUSIC", "BOTH", "MARK", "OFTEN", "LETTER", "UNTIL", "MILE", "RIVER", "FEET",
    "CARE", "BOOK", "RAIN", "ROOM", "FRIEND", "IDEA", "FISH", "STOP", "BASE",
    "HEAR", "HORSE", "SURE", "WATCH", "COLOR", "FACE", "WOOD", "MAIN", "GIRL",
    "YOUNG", "READY", "ABOVE", "EVER", "LIST", "FEEL", "TALK", "BIRD", "SOON",
    "BODY", "FAMILY", "DIRECT", "LEAVE", "SONG", "DOOR", "BLACK", "SHORT",
    "CLASS", "WIND", "SHIP", "AREA", "HALF", "ROCK", "ORDER", "FIRE", "SOUTH",
    "PIECE", "TOLD", "PASS", "SINCE", "WHOLE", "KING", "SPACE", "HEARD", "BEST",
    "HOUR", "TRUE", "FIVE", "STEP", "EARLY", "HOLD", "WEST", "GROUND", "REACH",
    "FAST", "SING", "LISTEN", "TABLE", "TRAVEL", "LESS", "SIMPLE", "CENTER",
    "LOVE", "PERSON", "MONEY", "SERVE", "ROAD", "RULE", "PULL", "COLD", "VOICE",
    "POWER", "TOWN", "FINE", "FALL", "LEAD", "DARK", "WAIT", "PLAN", "STAR",
    "REST", "ABLE", "DONE", "DRIVE", "FRONT", "WEEK", "GAVE", "GREEN", "QUICK",
    "OCEAN", "WARM", "FREE", "MIND", "CLEAR", "STREET", "STAY", "WHEEL", "FULL",
    "FORCE", "BLUE", "DEEP", "MOON", "FOOT", "TEST", "BOAT", "GOLD", "PLANE",
    "GAME", "HEAT", "SNOW", "EAST", "SECRET", "ORACLE", "RIDDLE", "CIPHER",
    "TEMPLE", "SYMBOL", "DREAM", "TRUTH", "SPIRIT", "WISDOM", "VISION", "SHADOW",
    "FLOWER", "PLANET"
}

# --- State ---
if "offsets" not in st.session_state:
    target = "ORACLE"
    st.session_state.offsets = [DEVICE_ALPHA.index(c) for c in target]

if "free_spin" not in st.session_state:
    st.session_state.free_spin = False

def rotate_ring(i, step):
    st.session_state.offsets[i] = (st.session_state.offsets[i] + step) % 26

def get_word():
    return "".join(DEVICE_ALPHA[st.session_state.offsets[i]] for i in range(6))

# --- UI Styling ---
st.markdown("""
<style>
.cylinder-box {
    display: flex;
    justify-content: center;
    gap: 8px;
    background: #18191c;
    border: 3px solid #b8860b;
    border-radius: 12px;
    padding: 16px 8px;
    margin: 15px 0;
}
.ring-col {
    display: flex;
    flex-direction: column;
    align-items: center;
    background: #23252a;
    border: 1px solid #554422;
    border-radius: 6px;
    width: 48px;
}
.char-faint { font-size: 16px; color: #666; height: 26px; line-height: 26px; }
.char-mid { font-size: 20px; color: #aaa; height: 30px; line-height: 30px; }
.char-target {
    font-size: 28px;
    font-weight: 900;
    color: #fff;
    background: linear-gradient(180deg, #d4af37, #8b6508);
    width: 100%;
    text-align: center;
    height: 44px;
    line-height: 44px;
    border-top: 2px solid #ffd700;
    border-bottom: 2px solid #ffd700;
}
</style>
""", unsafe_allow_html=True)

st.title("🗝️ Drew's Cryptex")
st.caption("Based on Drew's Physical 6-Ring Cylinder Device")

# --- Render 3D Cylinder ---
rings_html = ""
for i in range(6):
    off = st.session_state.offsets[i]
    m2 = DEVICE_ALPHA[(off - 2) % 26]
    m1 = DEVICE_ALPHA[(off - 1) % 26]
    c0 = DEVICE_ALPHA[off % 26]
    p1 = DEVICE_ALPHA[(off + 1) % 26]
    p2 = DEVICE_ALPHA[(off + 2) % 26]
    rings_html += f"""
    <div class="ring-col">
        <div class="char-faint">{m2}</div>
        <div class="char-mid">{m1}</div>
        <div class="char-target">{c0}</div>
        <div class="char-mid">{p1}</div>
        <div class="char-faint">{p2}</div>
    </div>
    """

st.markdown(f'<div class="cylinder-box">{rings_html}</div>', unsafe_allow_html=True)

# --- Ring Steppers ---
btn_cols = st.columns(6)
for i, col in enumerate(btn_cols):
    with col:
        if st.button("▲", key=f"u_{i}", use_container_width=True):
            rotate_ring(i, -1)
            st.rerun()
        if st.button("▼", key=f"d_{i}", use_container_width=True):
            rotate_ring(i, 1)
            st.rerun()

st.write("---")

# --- Modes & Controls ---
c1, c2 = st.columns(2)
with c1:
    st.subheader("🎲 Spin Controls")
    if st.button("🎲 Random Spin", use_container_width=True, type="primary"):
        st.session_state.offsets = [random.randint(0, 25) for _ in range(6)]
        st.rerun()
    
    spin_label = "🛑 Stop Free Spin" if st.session_state.free_spin else "⚡ Start Free Spin"
    if st.button(spin_label, use_container_width=True):
        st.session_state.free_spin = not st.session_state.free_spin
        st.rerun()
        
    if st.session_state.free_spin:
        st.session_state.offsets = [random.randint(0, 25) for _ in range(6)]
        time.sleep(0.4)
        st.rerun()

with c2:
    st.subheader("🎯 Align Word")
    user_input = st.text_input("Enter 1-6 Letters", max_chars=6).strip().upper()
    if st.button("Set Cylinder Word", use_container_width=True):
        if user_input.isalpha():
            for i, char in enumerate(user_input[:6]):
                st.session_state.offsets[i] = DEVICE_ALPHA.index(char)
            st.rerun()

# --- Circumference Word Scanner & Reading ---
center_word = get_word()
total_num = sum(PYTHAGOREAN_VALUES.get(c, 0) for c in center_word)
while total_num > 9:
    total_num = sum(int(d) for d in str(total_num))

st.write("---")
st.subheader(f"📜 Cylinder Reading for **{center_word}**")
st.write(f"**Pythagorean Vibration {total_num}:** {NUMEROLOGY_THEMES.get(total_num, '')}")

# Scan all 26 rows
found_rows = []
for shift in range(26):
    row_chars = "".join(DEVICE_ALPHA[(st.session_state.offsets[i] + shift) % 26] for i in range(6))
    row_words = []
    for length in [6, 5, 4, 3]:
        for start in range(7 - length):
            sub = row_chars[start:start+length]
            if sub in COMMON_WORDS and sub not in row_words:
                row_words.append(sub)
    if row_words:
        label = "CENTER (Row 0)" if shift == 0 else f"Row +{shift}"
        found_rows.append((label, row_chars, row_words))

st.markdown("#### Discovered Words Around the Cylinder:")
if found_rows:
    for label, row_chars, words in found_rows:
        st.markdown(f"- **{label}:** `{row_chars}` $\\rightarrow$ **{', '.join(words)}**")
else:
    st.info("No words detected in this position. Try spinning or rotating!")
