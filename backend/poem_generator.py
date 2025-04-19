import random

# Define poet styles with more vocabulary
POET_STYLES = {
    "shakespeare": ["thou", "thee", "hath", "dost", "fair", "love", "sweet", "beauty", "charm", "night", "day", "heart"],
    "dickinson": ["hope", "soul", "buzz", "light", "sky", "dream", "rose", "shadow", "dark", "still", "whisper"],
    "keats": ["night", "dream", "light", "soul", "wild", "flame", "gaze", "beauty", "eternal", "rest", "love"],
    "whitman": ["soul", "earth", "star", "wind", "love", "freedom", "wild", "self", "man", "vast", "universe"],
    "default": ["heart", "light", "shadow", "dream", "time", "truth", "hope", "joy", "desire", "night"],
    "blake": ["rose", "fire", "dream", "dark", "eternal", "soul", "light", "shadow", "god", "truth"]
}

# Expanded Emotion keywords
EMOTION_WORDS = {
    "joy": ["sunlight", "laugh", "bloom", "golden", "dance", "bright", "cheerful", "warm", "light", "joyous", "hope"],
    "sadness": ["tears", "dark", "alone", "whisper", "lost", "grief", "empty", "silent", "cold", "heartache", "sorrow"],
    "love": ["kiss", "touch", "desire", "eyes", "forever", "passion", "heart", "sweet", "affection", "adore", "beloved"],
    "hope": ["rise", "light", "wings", "new", "begin", "future", "dream", "glow", "blossom", "renew", "spark"],
    "anger": ["rage", "fire", "storm", "wrath", "dark", "burn", "shout", "fury", "burning", "wrathful", "thunder"],
    "fear": ["shadow", "silent", "creep", "darkness", "chill", "dread", "scream", "cold", "terror", "creep", "ghost"],
    "regret": ["sorrow", "lost", "time", "faded", "tears", "foolish", "mistake", "dark", "empty", "forgotten", "longing"],
    "peace": ["calm", "soft", "whisper", "breeze", "still", "serenity", "quiet", "dream", "light", "rest", "harmony"],
    "nostalgia": ["old", "time", "memory", "longing", "past", "dream", "soft", "whisper", "youth", "gentle"]
}

# Haiku structure (5-7-5 syllables)
def generate_haiku(emotion: str, style: str) -> str:
    words = EMOTION_WORDS.get(emotion, []) + POET_STYLES.get(style, POET_STYLES["default"])
    return f"{random.choice(words)} in the breeze\n" \
           f"{random.choice(words)} whispers on the wind\n" \
           f"{random.choice(words)} fades at dusk"

# Sonnet structure (14 lines, iambic-like)
def generate_sonnet(emotion: str, style: str) -> str:
    words = EMOTION_WORDS.get(emotion, []) + POET_STYLES.get(style, POET_STYLES["default"])
    poem = ""
    for i in range(14):
        line = f"The {random.choice(words)} {random.choice(['shines', 'weeps', 'waits', 'calls', 'burns', 'glows'])} in {random.choice(words)}"
        poem += line + "\n"
    return poem

# Limerick structure (AABBA rhyme scheme)
def generate_limerick(emotion: str, style: str) -> str:
    words = EMOTION_WORDS.get(emotion, []) + POET_STYLES.get(style, POET_STYLES["default"])
    return f"There once was a {random.choice(words)} from {random.choice(words)}\n" \
           f"Who danced with the wind in the sun\n" \
           f"The light it did shine\n" \
           f"Making everything fine\n" \
           f"And the moon, she did smile just for fun"

# Free verse (no fixed structure, more creative freedom)
def generate_free_verse(emotion: str, style: str) -> str:
    words = EMOTION_WORDS.get(emotion, []) + POET_STYLES.get(style, POET_STYLES["default"])
    poem = f"The {random.choice(words)} drifts like the {random.choice(words)}\n"
    poem += f"A feeling of {random.choice(words)} fills the air\n"
    poem += f"In the {random.choice(words)} the {random.choice(words)} {random.choice(['whispers', 'weeps', 'shines'])}\n"
    poem += f"The stars are still, waiting for the {random.choice(words)}\n"
    return poem
