import streamlit as st
from moviepy.editor import VideoFileClip
import tempfile, os
import speech_recognition as sr
import numpy as np
import mediapipe as mp
import cv2
from textblob import TextBlob

st.set_page_config(page_title="Human Analytics", layout="centered")

st.title("Human Analytics — Quick Feedback 🎥🗣️")
st.write("Upload a short video (max 2 minutes). The app will transcribe audio, check pace & sentiment, and give simple expression feedback.")

uploaded = st.file_uploader("Upload your video (mp4/mov)", type=["mp4","mov","mkv","webm"])
if uploaded:
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    tfile.write(uploaded.read())
    video_path = tfile.name

    st.video(video_path, start_time=0)

    # --- Extract audio ---
    st.info("Extracting audio and transcribing (may take 10–60s)...")
    clip = VideoFileClip(video_path)
    audio_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
    clip.audio.write_audiofile(audio_path, verbose=False, logger=None)

    # --- Transcribe using Google Web Speech (speech_recognition) ---
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data)
        st.success("Transcription done.")
    except Exception as e:
        st.warning("Auto-transcription failed or not available. You can paste/type transcript below.")
        text = st.text_area("Paste / type transcript (if auto-transcribe failed):", height=150)

    if text:
        st.subheader("Transcript")
        st.write(text)

        # Speaking rate
        words = text.split()
        duration_sec = clip.duration
        wpm = (len(words) / duration_sec) * 60 if duration_sec > 0 else 0
        st.metric("Speaking rate (words per minute)", f"{wpm:.0f} wpm")

        # Sentiment / grammar rough check
        tb = TextBlob(text)
        polarity = tb.sentiment.polarity
        sentiment = "Positive" if polarity > 0.1 else ("Negative" if polarity < -0.1 else "Neutral")
        st.metric("Sentiment", sentiment)
        st.write(f"Sentiment polarity: {polarity:.2f}")

        # Simple grammar hint (very light)
        lang_errors = []
        if len(list(tb.correct().split())) < len(words) - 2:
            lang_errors.append("Possible typos or grammar issues detected — consider clearer sentences.")
        if wpm < 100:
            lang_errors.append("Pace: A bit slow — try to speak a little faster.")
        if wpm > 160:
            lang_errors.append("Pace: A bit fast — slow down for clarity.")
        if lang_errors:
            for e in lang_errors:
                st.warning(e)
        else:
            st.success("Pace and basic grammar look good.")

    # --- Frame analysis: detect face and simple smile metric using MediaPipe Face Mesh ---
    st.info("Analyzing facial expression (smile detection)... this may take a little time.")
    mp_face = mp.solutions.face_mesh
    face_mesh = mp_face.FaceMesh(static_image_mode=True, max_num_faces=1)

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    frame_count = int(min(150, cap.get(cv2.CAP_PROP_FRAME_COUNT)))  # sample up to 150 frames
    step = max(1, int(cap.get(cv2.CAP_PROP_FRAME_COUNT) / frame_count))

    smile_scores = []
    i = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if i % step != 0:
            i += 1
            continue
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)
        if results.multi_face_landmarks:
            lm = results.multi_face_landmarks[0].landmark
            h, w, _ = frame.shape
            # choose mouth corners and upper/lower lip points
            def p(idx): return np.array([lm[idx].x * w, lm[idx].y * h])
            left = p(61)   # approximate left mouth corner
            right = p(291) # approximate right mouth corner
            top = p(13)    # upper lip
            bottom = p(14) # lower lip
            mouth_width = np.linalg.norm(right - left)
            mouth_open = np.linalg.norm(bottom - top)
            if mouth_width > 0:
                score = mouth_open / mouth_width
                smile_scores.append(score)
        i += 1

    cap.release()
    face_mesh.close()

    if smile_scores:
        avg_smile = np.mean(smile_scores)
        st.metric("Smile index (higher = more open mouth / possible speaking or smile)", f"{avg_smile:.3f}")
        if avg_smile > 0.25:
            st.success("Good expressiveness detected — you use mouth movements well (smile/talk).")
        else:
            st.info("Neutral expressiveness — try to smile more or show facial variety.")
    else:
        st.warning("No face detected in sampled frames. Make sure face is visible and well lit.")

    # Final summary card
    st.header("Quick Feedback Summary")
    st.write("- **Pace:**", f"{wpm:.0f} wpm" if text else "N/A")
    st.write("- **Sentiment:**", sentiment if text else "N/A")
    if smile_scores:
        st.write(f"- **Expression:** avg score {avg_smile:.3f}")
    st.write("")
    st.write("**Suggestions:**")
    st.write("• Keep sentences short and clear.  • Use more facial expressions and smile.  • Practice speaking at ~120–140 wpm for clarity.")
