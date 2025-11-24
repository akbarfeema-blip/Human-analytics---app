import streamlit as st
import moviepy.editor as mp
import speech_recognition as sr
from textblob import TextBlob
import pandas as pd
import os

st.title("Human Analytics Mini Project")
st.write("Upload a 2-minute video. The app will analyse your communication skills and give feedback.")

# Upload Section
uploaded_file = st.file_uploader("Upload your video (mp4/mov)", type=["mp4", "mov"])

if uploaded_file:
    st.video(uploaded_file)

    # Save video temporarily
    with open("uploaded_video.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.info("Extracting audio from video... Please wait...")

    # Extract audio from the uploaded video
    try:
        video = mp.VideoFileClip("uploaded_video.mp4")
        video.audio.write_audiofile("audio.wav")
        st.success("Audio extracted successfully!")
    except Exception as e:
        st.error("Audio extract nahi hua. Try another video.")
        st.stop()

    # Speech Recognition
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile("audio.wav") as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
    except:
        st.error("Speech detect nahi hua. Video me awaaz clear honi chahiye.")
        text = ""

    # Show transcript
    if text:
        st.subheader("Transcribed Speech:")
        st.write(text)

    # Sentiment / Tone Analysis
    st.subheader("Feedback:")
    if text:
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity

        if sentiment > 0.4:
            st.success("✔ Excellent tone! You sound confident and positive.")
        elif sentiment > 0:
            st.info("✔ Good tone. Lekin thodi energy aur clarity improve karo.")
        else:
            st.warning("⚠ Tone weak laga. Confidence aur clarity improve karo.")

    # Strengths & Weaknesses (Simple Rules)
    st.subheader("Strengths & Weaknesses")
    st.write("**Strengths:** Clear voice (if audio extracted), good pronunciation.")
    st.write("**Weaknesses:** Expressions, body language, grammar improvement needed.")

    # Recommended Courses
    st.subheader("Recommended SkillUp India Courses:")
    st.write("- Public Speaking Training")
    st.write("- Confidence & Personality Development")
    st.write("- Spoken English & Grammar Basics")
    st.write("- Body Language Mastery")

    # Save Performance Data
    if not os.path.exists("performance.csv"):
        pd.DataFrame(columns=["Text_Length", "Sentiment"]).to_csv("performance.csv", index=False)

    if text:
        new_data = pd.DataFrame({
            "Text_Length": [len(text)],
            "Sentiment": [sentiment]
        })

        new_data.to_csv("performance.csv", mode="a", header=False, index=False)
        st.success("Performance saved successfully!")
