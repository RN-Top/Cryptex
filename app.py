import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(page_title="Drew's Cryptex", page_icon="🗝️", layout="centered")

# Drew's 26-letter Pythagorean cipher alphabet
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
    "DREAM", "TRUTH", "SPIRIT", "WISDOM", "VISION", "SHADOW", "FLOWER", "PLANET"
}

if "offsets" not in
