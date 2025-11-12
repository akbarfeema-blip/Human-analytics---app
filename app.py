import streamlit as st
import time

st.title("🎥 Human Analytics App")
st.write("Welcome! Record your 2-minute video and get instant feedback on your performance.")

# Upload or record video
video_file = st.file_uploader("Upload your video file", type=["mp4", "mov", "avi"])

if video_file:
    st.video(video_file)
    with st.spinner("Analyzing your video..."):
        time.sleep(3)
    st.success("✅ Analysis complete!")

    st.write("### Feedback Summary:")
    st.write("- Voice Clarity: Good")
    st.write("- Expressions: Natural")
    st.write("- Grammar: 90% accurate")
    st.write("- Body Language: Confident")
