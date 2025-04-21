import streamlit as st
import json
import pandas as pd
import os
from utils import get_user_videos, analyze_video, generate_report
import time
from utils import read_report_text

st.set_page_config(page_title="Video Analysis and Report Generator", layout="centered")

# Session state initialization
if 'email' not in st.session_state:
    st.session_state.email = ""
if 'selected_video' not in st.session_state:
    st.session_state.selected_video = ""

st.title("🎥 Video Analysis and Report Generator")

# Step 1: Email login
email = st.text_input("Enter your email to log in", value=st.session_state.email)
if email:
    st.session_state.email = email
    video_list = get_user_videos(email)
    if not video_list:
        st.warning("No videos assigned to this email. Please contact admin.")
    else:
        selected_video = st.selectbox("Select a video", video_list)
        st.session_state.selected_video = selected_video

        # Step 2: Show video
        video_path = os.path.join("videos", selected_video)
        st.video(video_path)

        # Step 3: Analyze video
        if st.button("Analyze Video"):
            with st.spinner("Analyzing video..."):
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)  # total ~1 second
                    progress_bar.progress(i + 1)
                analyzed_video_path = analyze_video(video_path)
            st.success("Video analysis complete!")
            st.video(analyzed_video_path)

        # Step 4: Generate report
        if st.button("Generate Report"):
            with st.spinner("Generating report..."):
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i + 1)
                report_text = read_report_text(st.session_state.selected_video)

            st.success("✅ Report generated successfully!")
            st.info("🧾 Here's the analysis summary below:")
            st.text_area("📝 Report Content", report_text, height=200)
        

        # Step 5: Save results
        if st.button("💾 Save Report to CSV"):
            df = pd.DataFrame([{
                "email": email,
                "original_video": selected_video,
                "analyzed_video": os.path.basename(analyzed_video_path),
                "report": report_text
            }])
            csv_path = "data/output_report.csv"
            if os.path.exists(csv_path):
                df.to_csv(csv_path, mode='a', header=False, index=False)
            else:
                df.to_csv(csv_path, index=False)
            st.success("Data saved successfully!")