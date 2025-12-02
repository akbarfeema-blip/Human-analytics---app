import streamlit as st
import cv2
from pydub import AudioSegment
import random

# -----------------------------
# Helper functions (all in one file)
# -----------------------------

def extract_audio_frames(video_file):
    # Save uploaded video
    video_path = "temp_video.mp4"
    with open(video_path, "wb") as f:
        f.write(video_file.getbuffer())

    # Extract frames
    cap = cv2.VideoCapture(video_path)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()

    # Extract audio
    audio_path = "temp_audio.wav"
    audio = AudioSegment.from_file(video_path)
    audio.export(audio_path, format="wav")

    return audio_path, frames

def analyze_emotions(frames):
    emotions = ["Happy", "Neutral", "Sad", "Angry", "Confident", "Nervous"]
    strength = random.choice(emotions)
    weakness = random.choice([e for e in emotions if e != strength])
    feedback = [
        f"Strength: You mostly appear {strength} in your expressions.",
        f"Weakness: Try to reduce {weakness} expressions.",
        "Body language: Looks confident." if random.random() > 0.3 else "Body language: Work on posture and gestures."
    ]
    return feedback

def analyze_speech(audio_path):
    speech_options = [
        "Your speech clarity is good.",
        "Try to speak more slowly for clarity.",
        "Grammar is mostly correct.",
        "Some grammar mistakes detected, practice speaking.",
        "Voice tone is confident.",
        "Voice tone could be improved."
    ]
    feedback = random.sample(speech_options, 3)
    return feedback

def get_course_suggestions():
    courses = [
        {"title": "Public Speaking Basics", "link": "https://skillupindia.in/public-speaking"},
        {"title": "Improve Body Language", "link": "https://skillupindia.in/body-language"},
        {"title": "Advanced English Grammar", "link": "https://skillupindia.in/english-grammar"},
    ]
    return courses

# -----------------------------
# Streamlit App
# -----------------------------
st.set_page_config(page_title="Human Analytics", page_icon="👤")
st.title("👤 Human Analytics Mini Project")
st.markdown("Upload a short video (≤2 min) to get random feedback on your speech, expressions, grammar, and body language.")

uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "mov"])

if uploaded_file:
    st.video(uploaded_file)

    if st.button("Analyze Video"):
        st.info("Processing...")

        # Extract audio & frames
        audio_path, frames = extract_audio_frames(uploaded_file)

        # Get random feedback
        emotion_feedback = analyze_emotions(frames)
        speech_feedback = analyze_speech(audio_path)

        # Display feedback
        st.success("Analysis Complete!")
        st.subheader("💡 Feedback:")
        for f in emotion_feedback + speech_feedback:
            st.info(f)

        # Show suggested courses
        st.subheader("📚 Suggested Courses:")
        courses = get_course_suggestions()
        for course in courses:
            st.write(f"- [{course['title']}]({course['link']})")
