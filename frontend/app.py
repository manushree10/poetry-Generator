import streamlit as st
import base64
import requests
import pyttsx3
import time
from PIL import Image, ImageDraw, ImageFont
import io
import urllib.parse

# ----- Emotion Detection -----
def detect_emotion(user_input: str) -> str:
    EMOTION_WORDS = {
        "joy": ["sunlight", "laugh", "bloom", "golden", "dance", "bright", "cheerful", "warm", "light", "joyous", "hope"],
        "sadness": ["tears", "dark", "alone", "whisper", "lost", "grief", "empty", "silent", "cold", "heartache", "sorrow"],
        "love": ["kiss", "touch", "desire", "eyes", "forever", "passion", "heart", "sweet", "affection", "adore", "beloved"],
        "hope": ["rise", "light", "wings", "new", "begin", "future", "dream", "glow", "blossom", "renew", "spark"],
        "anger": ["rage", "fire", "storm", "wrath", "dark", "burn", "shout", "fury", "burning", "wrathful", "thunder"],
        "fear": ["shadow", "silent", "creep", "darkness", "chill", "dread", "scream", "cold", "terror", "ghost"],
        "regret": ["sorrow", "lost", "time", "faded", "tears", "foolish", "mistake", "dark", "empty", "forgotten", "longing"],
        "peace": ["calm", "soft", "whisper", "breeze", "still", "serenity", "quiet", "dream", "light", "rest", "harmony"],
        "nostalgia": ["old", "time", "memory", "longing", "past", "dream", "soft", "whisper", "youth", "gentle"]
    }
    emotion_scores = {emotion: 0 for emotion in EMOTION_WORDS}
    words = user_input.lower().split()
    for word in words:
        for emotion, emotion_words in EMOTION_WORDS.items():
            if word in emotion_words:
                emotion_scores[emotion] += 1
    return max(emotion_scores, key=emotion_scores.get)

# ----- Page Config -----
st.set_page_config(page_title="AI Poetry Generator", layout="centered")

def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg_img_base64 = get_base64("frontend/poet.jpg")
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bg_img_base64}");
        background-size: cover;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align: center; color: #800080;'>🌸 Emotionally Charged Poetry: AI with ML Magic 🌸</h1>", unsafe_allow_html=True)

# ----- Session State -----
if "poem" not in st.session_state:
    st.session_state.poem = ""
if "feedback" not in st.session_state:
    st.session_state.feedback = {}

# ----- User Inputs -----
poem_type = st.selectbox("Choose poem type", ["haiku", "sonnet", "limerick", "free_verse"])
emotion = st.text_input("Enter an emotion (e.g. joy, love, nostalgia, peace, anger)")
if not emotion:
    emotion = "joy"
style = st.selectbox("Choose a poet style", ["shakespeare", "dickinson", "keats", "whitman", "blake", "default"])

if st.button("🔍 Detect Emotion"):
    detected_emotion = detect_emotion(emotion)
    st.success(f"Detected emotion: **{detected_emotion}**")

if st.button(" Generate Poem"):
    with st.spinner("Crafting your poem..."):
        try:
            response = requests.post("http://127.0.0.1:8000/generate", json={
                "poem_type": poem_type,
                "emotion": emotion,
                "style": style
            })
            if response.status_code == 200:
                st.session_state.poem = response.json()["poem"]
                st.success("Poem generated! Explore the tabs below ✨")
            else:
                st.error("Failed to generate poem. Check FastAPI server.")
        except Exception as e:
            st.error(f"Error: {e}")

# ----- Feature Tabs -----
if st.session_state.poem:
    tabs = st.tabs(["🌟 Your Poem", "🗣 Text-to-Speech", "📥 Download", "💬 Feedback", "📣 Share"])

    # Poem Display
    with tabs[0]:
        st.markdown(f"### ✨ {poem_type.replace('_', ' ').title()} in {style.title()} Style")
        for line in st.session_state.poem.strip().split('\n'):
            st.markdown(f"> {line}")
            time.sleep(0.2)

    # Text-to-Speech
    with tabs[1]:
        if st.button("🔊 Read Aloud"):
            try:
                engine = pyttsx3.init()
                engine.setProperty('rate', 150)
                engine.say(st.session_state.poem)
                engine.runAndWait()
            except Exception as e:
                st.error(f"Text-to-Speech failed: {e}")

    # Download as text and image
    with tabs[2]:
        st.download_button("💾 Save as .txt", data=st.session_state.poem, file_name="your_poem.txt")

        def create_poem_image(poem: str) -> bytes:
            width, height = 800, 600
            image = Image.new("RGB", (width, height), color="#fffaf0")
            draw = ImageDraw.Draw(image)
            try:
                font = ImageFont.truetype("arial.ttf", 22)
            except:
                font = ImageFont.load_default()
            y = 50
            for line in poem.split('\n'):
                draw.text((50, y), line, fill="black", font=font)
                y += 35
            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            buffer.seek(0)
            return buffer

        if st.button("🖼️ Download as Image"):
            img_bytes = create_poem_image(st.session_state.poem)
            st.download_button("📥 Save Poem Image", data=img_bytes, file_name="poem.png", mime="image/png")

    # Feedback
    with tabs[3]:
        rating = st.radio("How well did this poem reflect your emotion?", [1, 2, 3, 4, 5], index=2)
        if st.button("Submit Feedback"):
            st.session_state.feedback[emotion] = rating
            st.success(f"Thanks! You rated this poem {rating}/5.")
            if rating >= 4:
                st.info("👍 The system is improving with your positive feedback!")
            elif rating <= 2:
                st.warning(" Adjusting to better express your emotion next time!")

    # Share on Twitter
    # Share on Social Media
    with tabs[4]:
        st.markdown("### 📣 Share Your Poem")

        short_poem = st.session_state.poem[:150].replace('\n', ' ')
        encoded_text = urllib.parse.quote(f"Check out this AI-generated poem! 🌸\n\n{short_poem}")

        twitter_url = f"https://twitter.com/intent/tweet?text={encoded_text}"
        whatsapp_url = f"https://api.whatsapp.com/send?text={encoded_text}"
        facebook_url = f"https://www.facebook.com/sharer/sharer.php?u=&quote={encoded_text}"

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"[🐦 Share on Twitter]({twitter_url})", unsafe_allow_html=True)
            st.markdown(f"[📘 Share on Facebook]({facebook_url})", unsafe_allow_html=True)
        with col2:
            st.markdown(f"[🟢 Share on WhatsApp]({whatsapp_url})", unsafe_allow_html=True)

        st.markdown("---")

st.markdown(
            """
            <hr style="border: 0.5px solid #ccc;" />
            <div style="text-align: center; font-size: 16px; color: #555;">
                Made with ❤️ by <strong>Manushree</strong> and <strong>Prathibha</strong><br>
                © 2025 | Emotionally Charged Poetry: AI with ML Magic
            </div>
            """,
            unsafe_allow_html=True
        )