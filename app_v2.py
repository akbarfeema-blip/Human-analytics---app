import streamlit as st
import random
import time

st.set_page_config(page_title="Human Analytics App", page_icon="🧠", layout="centered")

st.title("🧠 Human Analytics App")
st.write("Upload or record a 2-minute video for AI-based feedback on your performance!")

# Upload section
video = st.file_uploader("🎥 Upload your short video", type=["mp4", "mov", "avi"])

if video:
    st.video(video)
    st.info("Analyzing your video... Please wait ⏳")
    time.sleep(3)   # Simulate AI processing

    # Randomized feedback simulation (demo)
    feedback_list = [
        ("Voice Clarity", "Your voice is clear and confident!"),
        ("Facial Expression", "Good smile 😊, try more eye contact."),
        ("Grammar", "Sentence fluency is decent. Practice smoother transitions."),
        ("Body Language", "Posture is confident. Avoid hand fidgeting."),
        ("Energy Level", "Good energy! Maintain enthusiasm till the end.")
    ]

    st.success("✅ AI Feedback Report Ready")

    for category, message in feedback_list:
        st.subheader(f"🔹 {category}")
        st.write(message)
        time.sleep(0.7)

    st.balloons()
else:
    st.warning("Please upload a short video to start analysis 🎬")
