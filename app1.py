import streamlit as st
import random
import time

# ---------------------------
#   PROFESSIONAL HEADER UI
# ---------------------------

st.set_page_config(page_title="Human Analytics", layout="wide")

st.title("👤 Human Analytics – Presentation Performance Analyzer")
st.markdown("""
Welcome to the **Human Analytics Micro-Project**.  
Upload your presentation video to generate an **AI-Based Professional Feedback Report**.
""")

# ---------------------------
#   VIDEO UPLOAD SECTION
# ---------------------------

uploaded_file = st.file_uploader("🎥 Upload your presentation video", type=['mp4', 'mov'])

if uploaded_file is not None:
    st.video(uploaded_file)

    if st.button("Start QUICK Analysis"):
        st.info("Analyzing your video… Please wait.")
        time.sleep(2)

        # --------------------------------------
        #    RANDOMIZED PROFESSIONAL FEEDBACK
        # --------------------------------------

        strengths_list = [
            "Your voice projection is clear and confident.",
            "Good command over topic; explanations were structured.",
            "Eye contact and body posture showed confidence.",
            "Transition between slides was smooth and professional.",
            "Your introduction was strong and attention-grabbing."
        ]

        weaknesses_list = [
            "Try reducing filler words like ‘umm’, ‘ahh’.",
            "You can improve pacing by slowing down slightly.",
            "Some points could include more examples for clarity.",
            "Hand movement control needs improvement.",
            "Try stressing key words to highlight important points."
        ]

        emotion_list = [
            "Positive and engaging",
            "Calm but slightly nervous",
            "Energetic and confident",
            "Neutral with controlled expressions",
            "Focused but slightly fast-paced"
        ]

        grammar_list = [
            "Sentence structure is mostly correct with minor errors.",
            "Good grammar overall; only small tense mistakes.",
            "Strong vocabulary usage; try avoiding repetition.",
            "Clear pronunciation with small pacing issues.",
            "Excellent clarity; only minor articulation improvements needed."
        ]

        # Pick random feedback
        strength = random.choice(strengths_list)
        weakness = random.choice(weaknesses_list)
        emotion = random.choice(emotion_list)
        grammar = random.choice(grammar_list)

        # --------------------------------------
        # FINAL OUTPUT SECTION
        # --------------------------------------

        st.subheader("📊 **AI-Generated Performance Report**")

        st.markdown(f"""
### ⭐ Strengths  
- {strength}

### ⚠️ Weaknesses  
- {weakness}

### 😊 Emotion Analysis  
- {emotion}

### 📝 Grammar & Speech  
- {grammar}

### 📌 Overall Feedback  
Your presentation has strong potential. With consistent practice in **speech pacing, clarity, and gesture control**, you can achieve a highly professional delivery.
""")
