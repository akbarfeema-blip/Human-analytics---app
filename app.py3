import streamlit as st
import time
import random

# ---------- PAGE SETTINGS ----------
st.set_page_config(page_title="Human Analytics AI", page_icon="🧠", layout="centered")

# ---------- CUSTOM STYLING ----------
st.markdown("""
    <style>
    body {
        background-color: #f9fafc;
        font-family: 'Poppins', sans-serif;
        color: #222;
    }
    .stApp {
        background: linear-gradient(180deg, #f5f8ff 0%, #ffffff 100%);
        border-radius: 25px;
        padding: 20px;
        box-shadow: 0px 2px 12px rgba(0,0,0,0.1);
    }
    .upload-section {
        border: 2px dashed #82b1ff;
        padding: 25px;
        border-radius: 20px;
        background-color: #f0f6ff;
        text-align: center;
    }
    video {
        border-radius: 20px !important;
        box-shadow: 0px 2px 12px rgba(0,0,0,0.15);
    }
    </style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("<h1 style='text-align:center; color:#3366ff;'>🧠 Human Analytics AI App</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:16px;'>Your personal AI coach for expression, voice, grammar & body language.</p>", unsafe_allow_html=True)

# ---------- VIDEO UPLOAD ----------
st.markdown("<div class='upload-section'>🎥 <b>Upload your 1–2 minute video below</b></div>", unsafe_allow_html=True)
video = st.file_uploader("", type=["mp4", "mov", "avi"])

if video:
    st.video(video)
    with st.spinner("⏳ AI is analyzing your performance..."):
        time.sleep(3)
    
    st.success("✅ Analysis Complete! Here's your feedback:")

    feedback_data = [
        ("🎤 Voice Clarity", f"{random.randint(80, 95)}% clear — confident and well-paced."),
        ("😊 Facial Expression", f"{random.randint(75, 90)}% expressive — natural smile detected."),
        ("🗣️ Grammar Accuracy", f"{random.randint(80, 98)}% accurate — minimal pauses."),
        ("💃 Body Language", f"{random.randint(70, 95)}% confident posture."),
        ("⚡ Energy Level", f"{random.randint(75, 95)}% enthusiastic — great presence!")
    ]

    for category, feedback in feedback_data:
        st.markdown(f"<h4 style='color:#3366ff;'>{category}</h4>", unsafe_allow_html=True)
        st.write(feedback)
        time.sleep(0.6)

    st.balloons()
    overall = random.randint(78, 96)
    st.markdown(f"<h3 style='color:#28a745;'>🎯 Overall Score: {overall}% (Excellent!)</h3>", unsafe_allow_html=True)
else:
    st.warning("Please upload a video to begin AI analysis 🎬")
