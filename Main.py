# app.py
import streamlit as st
import random
import tempfile
import os
import speech_recognition as sr
from gtts import gTTS
import datetime
import json
import textwrap

# -----------------------------
# APP CONFIG
# -----------------------------
st.set_page_config(page_title="Human Analytics", page_icon="👤", layout="wide")

# ---------- Styling ----------
st.markdown("""
<style>
.report-box {
    padding: 14px;
    background-color: #f8fafc;
    border-radius: 10px;
    border: 1px solid #e6eef6;
}
.header {
    text-align: center;
}
.small-muted { color: #6b7280; font-size:12px; }
</style>
""", unsafe_allow_html=True)

# ---------- Header / Logo ----------
logo_path = "logo.png"
if os.path.exists(logo_path):
    st.image(logo_path, width=110)
else:
    st.markdown("<h3>👤 Human Analytics – Smart Communication Evaluation</h3>", unsafe_allow_html=True)

st.markdown("<h2 class='header'>Human Analytics — Natural Feedback Assistant</h2>", unsafe_allow_html=True)
st.write("A mobile-friendly Streamlit app that analyzes audio and gives natural, varied feedback (text + voice).")

# -----------------------------
# LOGIN (simple)
# -----------------------------
USERNAME = "student"
PASSWORD = "1234"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login_form():
    st.subheader("🔒 Login to continue")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("Login"):
            if username == USERNAME and password == PASSWORD:
                st.session_state.logged_in = True
                st.success("Login successful — welcome!")
            else:
                st.error("Incorrect username or password.")
    with col2:
        if st.button("Use demo login"):
            st.session_state.logged_in = True
            st.success("Demo login enabled.")

if not st.session_state.logged_in:
    login_form()
    st.stop()

# -----------------------------
# Session initializations
# -----------------------------
if "results" not in st.session_state:
    st.session_state.results = None
if "voice_file" not in st.session_state:
    st.session_state.voice_file = None

# -----------------------------
# NATURAL FEEDBACK TEMPLATES
# (varied, human-like sentences)
# -----------------------------
POSITIVE_PHRASES = [
    "Great delivery — your pace felt natural and easy to follow.",
    "Nice clarity — your words came across clearly and confidently.",
    "Good energy — you sounded engaged and present.",
    "Strong vocabulary — your word choice was appropriate and effective.",
    "Clear openings and closings — good structure in your speech."
]

NEGATIVE_PHRASES = [
    "Try slowing down a bit — a calmer pace will improve clarity.",
    "You used some filler words (like 'um' and 'so') — try to reduce them.",
    "Work on voice modulation — the tone was a bit flat in parts.",
    "Some words were unclear — focus on crisp pronunciation for tricky words.",
    "Add a touch more energy at key moments to keep the audience engaged."
]

GRAMMAR_TIPS = [
    "Watch verb tenses — keep them consistent across sentences.",
    "Break long sentences into two for better clarity.",
    "Use active voice when possible to make sentences stronger."
]

PRONUNCIATION_TIPS = [
    "Practice the pronunciation of multi-syllable words slowly.",
    "Record and match your pronunciation to native examples.",
    "Control your mouth openings on long vowel sounds."
]

ACTIONABLE_TIPS = [
    "Try a short daily practice: read 2 minutes aloud and record once a day.",
    "Use pauses intentionally — count a silent 1–2 seconds between ideas.",
    "Practice tongue twisters to improve articulation and clarity."
]

# Helper to produce human-like paragraph with varied phrasing
def build_natural_feedback(transcript, mood_score=0.5):
    # mood_score 0..1 where >0.5 = more positive
    positives = random.sample(POSITIVE_PHRASES, k=2)
    negatives = random.sample(NEGATIVE_PHRASES, k=2)
    grammar = random.choice(GRAMMAR_TIPS)
    pron = random.choice(PRONUNCIATION_TIPS)
    action = random.choice(ACTIONABLE_TIPS)

    # Compose several sentences, vary order randomly
    parts = []
    if mood_score >= 0.5:
        parts += positives
        parts += [f"One quick note: {random.choice(NEGATIVE_PHRASES)}"]
    else:
        parts += negatives
        parts += [f"A strength: {random.choice(POSITIVE_PHRASES)}"]

    parts += [
        f"Grammar suggestion: {grammar}.",
        f"Pronunciation suggestion: {pron}.",
        f"Practice tip: {action}."
    ]

    # Add a short summary sentence
    summary = "Overall, you're on the right path — a few focused practices will make your delivery stand out."
    parts.append(summary)

    # Make it natural-looking paragraph(s)
    paragraph = " ".join(parts)
    # Make transcript-aware: if transcript short, shorten feedback
    if len(transcript.split()) < 8:
        short_feedback = random.choice(positives + negatives)
        return short_feedback + " " + random.choice(ACTIONABLE_TIPS)
    return paragraph

# -----------------------------
# Speech to text (Google SR)
# -----------------------------
def speech_to_text(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except Exception as e:
        return ""  # blank string if not recognized

# -----------------------------
# Utilities: save upload to temp file
# -----------------------------
def save_temp_file(uploaded_file, suffix):
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.read())
        return tmp.name

# -----------------------------
# UI: Menu
# -----------------------------
menu = st.sidebar.selectbox("Menu", ["Home", "Audio Analysis", "Download Report", "About"])

# -----------------------------
# HOME
# -----------------------------
if menu == "Home":
    st.header("Welcome 👋")
    st.write("This app analyzes uploaded audio and returns natural, varied feedback (text + voice).")
    st.info("Use the **Audio Analysis** tab. Upload an MP3/WAV (phone-friendly).")

# -----------------------------
# AUDIO ANALYSIS
# -----------------------------
elif menu == "Audio Analysis":
    st.header("🎤 Upload an audio file (WAV / MP3)")
    uploaded = st.file_uploader("Choose audio file", type=["wav", "mp3"])
    st.write("Tip: For best results, use a clear recording and speak for ~20–90 seconds.")

    if uploaded:
        st.audio(uploaded)

        # Optional: show a small input for expected language / name
        speaker_name = st.text_input("Speaker name (optional)", value="Participant")
        run_btn = st.button("Run Analysis")

        if run_btn:
            with st.spinner("Transcribing and generating feedback..."):
                # Save file
                ext = ".wav" if uploaded.name.lower().endswith(".wav") else ".mp3"
                temp_path = save_temp_file(uploaded, suffix=ext)

                # Transcribe
                transcript = speech_to_text(temp_path)
                if transcript == "":
                    transcript = "Could not transcribe audio clearly."

                # Heuristics: filler words count, word count, pause heuristic (approx)
                text_lower = transcript.lower()
                filler_words = ["um", "uh", "like", "so", "actually", "basically", "you know", "right"]
                filler_count = sum(text_lower.count(w) for w in filler_words)
                word_count = len(transcript.split())
                # mood score heuristic: more words and fewer fillers -> higher score
                if word_count == 0:
                    mood_score = 0.4
                else:
                    mood_score = max(0.2, min(0.9, 1 - (filler_count / max(1, word_count / 5))))

                # Build natural feedback
                feedback_text = build_natural_feedback(transcript, mood_score=mood_score)

                # Create structured results
                results = {
                    "timestamp": datetime.datetime.utcnow().isoformat(),
                    "speaker": speaker_name,
                    "transcript": transcript,
                    "filler_count": int(filler_count),
                    "word_count": int(word_count),
                    "mood_score": round(mood_score, 2),
                    "feedback_text": feedback_text
                }
                st.session_state.results = results

                # Generate voice file and store path
                tts = gTTS(text=feedback_text, lang="en", slow=False)
                voice_path = f"voice_feedback_{int(datetime.datetime.utcnow().timestamp())}.mp3"
                tts.save(voice_path)
                st.session_state.voice_file = voice_path

            # Display results
            st.subheader("📝 Transcript")
            st.write(results["transcript"])

            st.subheader("📈 Quick Metrics")
            col1, col2, col3 = st.columns(3)
            col1.metric("Words", results["word_count"])
            col2.metric("Fillers", results["filler_count"])
            col3.metric("Mood score", results["mood_score"])

            st.subheader("🗣 Natural Feedback")
            st.markdown(f"<div class='report-box'>{results['feedback_text']}</div>", unsafe_allow_html=True)

            st.subheader("🔊 Play Voice Feedback")
            if st.session_state.voice_file and os.path.exists(st.session_state.voice_file):
                st.audio(st.session_state.voice_file)

            st.success("Analysis complete — you can download the report from the sidebar.")

# -----------------------------
# DOWNLOAD REPORT
# -----------------------------
elif menu == "Download Report":
    st.header("Download Report")
    if st.session_state.results is None:
        st.warning("Run an analysis first (Audio Analysis).")
    else:
        r = st.session_state.results
        # Create a simple JSON/text report
        report_text = textwrap.dedent(f"""
        Human Analytics Report
        Timestamp (UTC): {r['timestamp']}
        Speaker: {r['speaker']}
        
        Transcript:
        {r['transcript']}
        
        Quick metrics:
        Words: {r['word_count']}
        Filler words: {r['filler_count']}
        Mood score: {r['mood_score']}
        
        Feedback:
        {r['feedback_text']}
        """).strip()

        st.download_button("Download .txt report", data=report_text, file_name="human_analytics_report.txt")
        if st.session_state.voice_file and os.path.exists(st.session_state.voice_file):
            with open(st.session_state.voice_file, "rb") as f:
                st.download_button("Download voice feedback (MP3)", data=f, file_name="voice_feedback.mp3")

# -----------------------------
# ABOUT
# -----------------------------
elif menu == "About":
    st.header("About this App")
    st.write("""
    Human Analytics — Natural Feedback Assistant
    
    Features:
    - Audio upload (WAV/MP3) — mobile friendly  
    - Speech-to-text (Google Speech Recognition)  
    - Natural, varied feedback (positive + negative + tips)  
    - Playable voice feedback (gTTS)  
    - Downloadable report & voice file  
    - Simple login for demo / privacy
    """)
    st.write("For best results, use a clear recording of ~20–90 seconds.")
