import streamlit as st
import json
import pandas as pd
import os
import time
from utils import get_user_videos, analyze_video, read_report_text

# Set up the Streamlit page
st.set_page_config(page_title="Video Analysis and Report Generator", layout="wide")
# st.set_page_config(page_title="Video Analysis and Report Generator", layout="centered")


# Session state initialization
if 'email' not in st.session_state:
    st.session_state.email = ""
if 'selected_video' not in st.session_state:
    st.session_state.selected_video = ""
if 'analyzed_video_path' not in st.session_state:
    st.session_state.analyzed_video_path = None
if 'report_text' not in st.session_state:
    st.session_state.report_text = ""

# Title
st.title("Student Cognitive State Perception and Reasoning Project ")

# 🔹 Project Statement
st.markdown("""
### Statement

This project analyzes students' non-verbal behaviors during learning to interpret cognitive states 
            such as engagement, boredom, confusion, and frustration using visual cues.
            All interpretations are intended solely for educational improvement and research purposes. 

> ⚠️ The generated reports are not intended to serve as clinical or medical evidence. However, they may support speech-language pathologists (SLPs) in monitoring student progress 
            and evaluating the effectiveness of interventions in exceptional education settings.

<span style='font-size:16px'>
<b>Author:</b> <i>Lu Dong</i>&emsp;&emsp;&emsp;
<b>Advisor:</b> <i>Prof. Ifeoma Nwogu</i>&emsp;&emsp;&emsp;
<b>Research Lab:</b> <i>Human Behavior Modeling Lab</i>
</span>
            
**Acknowledgement:**   *National AI Institute for Exceptional Education (AI4EE)*  
            
  
""", unsafe_allow_html=True)

# This work was conducted by Lu Dong under the supervision of Prof. Ifeoma Nwogu, 
# as part of the Human Behavior Modeling Lab, with support from the National AI Institute for  Exceptional Education (AI4EE).
# | **Author:** *Lu Dong*    **Advisor:** *Prof. Ifeoma Nwogu*    **Research Lab:**  *Human Behavior Modeling Lab*    
# **Acknowledgement:**   *National AI Institute for Exceptional Education (AI4EE)*  

# Student Cognitive State Analysis and Reasoning
with st.expander(" Know More about the Student Cognitive State Perception and Reasoning"):
    st.markdown("""
This task focuses on analyzing and reasoning about students' cognitive states based on non-verbal behavioral cues captured in online learning videos. The goal is to understand how students engage with learning materials, identify potential learning difficulties, and summarize their mental states throughout the session.

**Key cognitive states interpreted:**
- **Engagement**: sustained attention and focus
- **Boredom**: reduced activity or passive expressions
- **Confusion**: signs of uncertainty, hesitation, or seeking clarification
- **Frustration**: expressions of negative emotions, such as frowning or sighing

**Features used for inference:**
- **Facial expressions** (e.g., basic emition labels, facial action units, emotional valence/arousal)
- **Eyeblink** and **gaze direction**
- **Temporal behavioral patterns** (e.g., changes in attention over time)

The reasoning process combines these visual cues using either rule-based logic or machine learning models to generate high-level, human-interpretable summaries of each student’s cognitive state.
""")

# Step 1: Email login
email = st.text_input("Enter your email to log in", value=st.session_state.email)
if email:
    st.session_state.email = email
    video_list = get_user_videos(email)

    if not video_list:
        st.warning("No videos assigned to this email. Please contact admin.")
    else:
        video_list_with_blank = [""] + video_list  # Add blank first option
        selected_video = st.selectbox("Select a video", video_list)
        if selected_video:
            st.session_state.selected_video = selected_video

        # Step 2: Show selected video
        
        video_path = os.path.join("videos", selected_video)
        st.video(video_path)

        # Step 3: Analyze video with progress bar
        if st.button("Analyze Video"):
            with st.spinner("Analyzing video..."):
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.03)  # Simulate work
                    progress_bar.progress(i + 1)
                analyzed_video_path = analyze_video(video_path)
                st.session_state.analyzed_video_path = analyzed_video_path

            st.success("Video analysis complete!")
            # st.video(analyzed_video_path)
        
        # Step 3.5: Tabbed multimodal analysis display
        st.markdown("###  Choose a modality to explore detailed analysis:")
        tabs = st.tabs(["AU Analysis", "VA Plot", "Eye Blink", "Eye Tracking"])

        with tabs[0]:
            st.markdown("#### Facial Action Unit (AU) Analysis")
            st.video("videos/1100021003_AU_annotated_final.mp4")
            st.markdown("""
        - **AU1 (Inner Brow Raiser)** - 14.75%, associated with attentiveness or mild surprise.  
        - **AU12 (Lip Corner Puller)** - 98.36%, sustained smiling and positive affect.  
        - **AU15 (Chin Raiser)** - 98.36%, possible emotional control or mild sadness.  
        - **AU22 (Lips Part)** - 1.64%, limited verbal movement.  
        - **AU40 (Left Dimpler)** - 62.30%, subtle asymmetric smile.
        """)

        with tabs[1]:
            st.markdown("####  Valence-Arousal (VA) Analysis")
            st.image("videos/1100021003_VA_plot.png", caption="Valence-Arousal Over Time")
            st.markdown("""
        Valence fluctuates while arousal remains consistently high.  
        Mid-segment shows high arousal with negative valence (stress/effort),  
        while later frames reflect high arousal with positive valence (engagement).
        """)

        with tabs[2]:
            st.markdown("#### Eye Blink Detection")
            st.video("videos/eyeblink_1100021003.mp4")
            st.markdown("No blinks detected — possibly indicating high visual attention and sustained concentration.")

        with tabs[3]:
            st.markdown("####  Eye Tracking")
            st.video("videos/gaze_1100021003.mp4")
            st.markdown(""" ~80% of the gaze was concentrated on task-relevant content with minimal deviation.  
        Brief glances away occurred during quiz segments, possibly reflecting momentary uncertainty.
        """)

        # Step 4: Generate report from report.json
        if st.button("Generate Report"):
            with st.spinner("Generating report..."):
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)  # Simulate delay
                    progress_bar.progress(i + 1)
                report_text = read_report_text(st.session_state.selected_video)
                st.session_state.report_text = report_text

            st.success("✅ Report generated successfully!")
            st.info("🧾 Here's the analysis summary below:")
            st.text_area("📝 Report Content", report_text, height=200)

        # Step 5: Save results to CSV
        if st.button("💾 Save Report to CSV"):
            if not st.session_state.analyzed_video_path or not st.session_state.report_text:
                st.error("Please analyze the video and generate the report before saving.")
            else:
                df = pd.DataFrame([{
                    "email": st.session_state.email,
                    "original_video": st.session_state.selected_video,
                    "analyzed_video": os.path.basename(st.session_state.analyzed_video_path),
                    "report": st.session_state.report_text
                }])

                csv_path = "data/output_report.csv"
                if os.path.exists(csv_path):
                    df.to_csv(csv_path, mode='a', header=False, index=False)
                else:
                    df.to_csv(csv_path, index=False)

                st.success("✅ Data saved successfully!")