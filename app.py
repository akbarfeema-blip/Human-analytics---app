# app.py
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
from io import BytesIO

st.set_page_config(page_title="Human Analytics — Demo", layout="wide", initial_sidebar_state="expanded")

# ---------- CUSTOM CSS ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    html, body, [class*="css"]  { font-family: "Inter", sans-serif; }
    .hero {
        background: linear-gradient(90deg, #0f172a 0%, #1e293b 100%);
        color: white;
        padding: 28px;
        border-radius: 12px;
        box-shadow: 0 6px 24px rgba(2,6,23,0.6);
        margin-bottom: 18px;
    }
    .title {
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 6px;
    }
    .subtitle {
        color: rgba(255,255,255,0.82);
        margin-bottom: 14px;
    }
    .card {
        background: white;
        border-radius: 10px;
        padding: 14px;
        box-shadow: 0 4px 18px rgba(15,23,42,0.06);
        margin-bottom: 12px;
    }
    .metric {
        font-size: 20px;
        font-weight: 700;
    }
    .small {
        font-size: 13px;
        color: #6b7280;
    }
    .btn {
        display:inline-block;
        margin-right:8px;
        padding:8px 12px;
        background:linear-gradient(90deg,#06b6d4,#7c3aed);
        color:white;
        border-radius:8px;
        text-decoration:none;
    }
    </style>
    """, unsafe_allow_html=True
)

# ---------- HERO with video ----------
with st.container():
    st.markdown('<div class="hero">', unsafe_allow_html=True)
    col1, col2 = st.columns([2,3])
    with col1:
        st.markdown('<div class="title">Human Analytics — Demo Project</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Realtime human behaviour analysis • CSE Mini Project • Clean UI & Explainable Results</div>', unsafe_allow_html=True)
        st.markdown('<div class="small">Upload video / image → run analysis → view metrics, charts & explanation.</div>', unsafe_allow_html=True)
        st.markdown('<br>')
        st.markdown('<a class="btn" href="#run-demo">Run Demo</a> <a class="btn" href="#download">Download Report</a>', unsafe_allow_html=True)
    with col2:
        # Use HTML5 video tag for autoplay muted (browsers allow autoplay only when muted)
        # Replace "VIDEO_URL" with your hosted video URL (mp4). If using local file, use st.video.
        video_url = "https://path.to/your/analysis_demo.mp4"  # replace
        html = f"""
        <video width="100%" height="100%" playsinline autoplay muted loop style="border-radius:8px;">
          <source src="{video_url}" type="video/mp4">
          Your browser does not support the video tag.
        </video>
        """
        st.markdown(html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.write("")  # spacing

# ---------- TOP METRICS ----------
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.markdown('<div class="card"><div class="small">Dataset rows</div><div class="metric">12,345</div></div>', unsafe_allow_html=True)
with kpi2:
    st.markdown('<div class="card"><div class="small">Model accuracy</div><div class="metric">92.4%</div></div>', unsafe_allow_html=True)
with kpi3:
    st.markdown('<div class="card"><div class="small">Avg inference</div><div class="metric">48 ms</div></div>', unsafe_allow_html=True)
with kpi4:
    st.markdown('<div class="card"><div class="small">Last run</div><div class="metric">2025-11-15</div></div>', unsafe_allow_html=True)

st.write("")

# ---------- MAIN LAYOUT ----------
left, right = st.columns([2,3])

with left:
    st.header("Upload / Run Analysis")
    uploaded = st.file_uploader("Upload a video or CSV (for batch)", type=["mp4","csv","mp3","wav"])
    if uploaded is not None:
        st.success("File uploaded. (Demo flow: we show a preview — actual model inference code goes here.)")
        if uploaded.type == "video/mp4":
            st.video(uploaded)
        elif uploaded.type == "text/csv" or uploaded.name.endswith(".csv"):
            df = pd.read_csv(uploaded)
            st.dataframe(df.head())
            st.markdown("**Action:** Run model on uploaded CSV (placeholder).")
            if st.button("Run Analysis on CSV"):
                st.info("Running demo analysis... (replace with your inference function)")
    st.markdown("---")
    st.header("Model & Method")
    st.markdown("""
    **Model:** CNN + LSTM (placeholder)  
    **Input:** video frames / keypoints  
    **Output:** activity labels, confidence, timestamps  
    **Explainability:** SHAP / Grad-CAM (add visuals)
    """)

with right:
    st.header("Interactive Results")
    # sample interactive chart
    times = pd.date_range("2025-11-01", periods=12, freq="D")
    df_chart = pd.DataFrame({
        "date": times,
        "detected_events": np.random.randint(0, 20, size=len(times))
    })
    fig = px.line(df_chart, x="date", y="detected_events", title="Detected events over time")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Confusion Matrix (placeholder)")
    cm = np.random.randint(0,100,(5,5))
    cm_df = pd.DataFrame(cm, columns=[f"Class {i}" for i in range(1,6)], index=[f"Class {i}" for i in range(1,6)])
    st.dataframe(cm_df.style.format("{:.0f}"))

st.write("")

# ---------- DATA / REPORT ----------
st.header("Dataset Preview & Download")
sample_df = pd.DataFrame({
    "id": range(1,11),
    "label": np.random.choice(["walk","run","sit","stand"], size=10),
    "confidence": np.round(np.random.rand(10), 2)
})
st.dataframe(sample_df)

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='results')
    writer.save()
    processed_data = output.getvalue()
    return processed_data

if st.button("Download sample report"):
    data = to_excel(sample_df)
    st.download_button("Download .xlsx", data, file_name="human_analytics_report.xlsx")

st.write("---")
st.markdown("### How it works")
st.markdown("""
- 1) Upload video or point to webcam.  
- 2) Pre-processing: frame extraction + pose/keypoint detection.  
- 3) Inference: Run trained model on extracted features.  
- 4) Post-processing & visualization: metrics, charts, downloadable report.
""")

st.write("---")
st.markdown("### Notes for instructor")
st.markdown("""
- Project includes: dataset, model, training logs, README with architecture diagrams, and demo video.  
- Add these for grading: `README.md`, `requirements.txt`, `system_design.pdf`, short 2-min demo video.
""")
