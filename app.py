import streamlit as st
import json
import pandas as pd
import os
import time
from utils import get_user_videos, analyze_video, read_report_text, read_full_report


# =================== 页面设置 ====================
# st.set_page_config(page_title="SCOPE: Cognitive State Analysis", layout="wide")
st.set_page_config(page_title="SCOPE: Cognitive State Analysis", layout="centered")

# =================== 初始化状态 ====================
if 'email' not in st.session_state:
    st.session_state.email = ""
if 'selected_video' not in st.session_state:
    st.session_state.selected_video = ""
if 'analyzed_video_path' not in st.session_state:
    st.session_state.analyzed_video_path = None
if 'report_text' not in st.session_state:
    st.session_state.report_text = ""
if 'show_analysis_tabs' not in st.session_state:
    st.session_state.show_analysis_tabs = False

# =================== 页面标题 ====================
# st.title("SCOPE: Student Cognitive Observation and Perception for Extrapolation")
st.markdown("""
<div style='text-align: center; padding: 10px 0;'>
    <h1 style='font-size: 36px; color: white; font-weight: 600;'>
        SCOPE: Student Cognitive Observation and Perception for Extrapolation
    </h1>
</div>
""", unsafe_allow_html=True)

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

# =================== 展开说明区块 ====================
with st.expander(" Know More about the Student Cognitive State Perception and Reasoning"):
    st.markdown("""
This task focuses on analyzing and reasoning about students' cognitive states based on non-verbal behavioral cues captured in online learning videos. The goal is to understand how students engage with learning materials, identify potential learning difficulties, and summarize their mental states throughout the session.

**Key cognitive states interpreted:**
- **Engagement**: sustained attention and focus
- **Boredom**: reduced activity or passive expressions
- **Confusion**: signs of uncertainty, hesitation, or seeking clarification
- **Frustration**: expressions of negative emotions, such as frowning or sighing

**Features used for inference:**
- **Facial expressions** (e.g., basic emotion labels, facial action units, emotional valence/arousal)
- **Eyeblink** and **gaze direction**
- **Temporal behavioral patterns** (e.g., changes in attention over time)
""")

# =================== 登录入口 ====================
email = st.text_input("Enter your email to log in", value=st.session_state.email)
if email:
    st.session_state.email = email
    video_list = get_user_videos(email)

    if not video_list:
        st.warning("Use test@buffalo.edu to view a sample video. For more videos, please contact the admin.")
    else:
        video_list_with_blank = [""] + video_list
        selected_video = st.selectbox("Select a video", video_list)

        if selected_video:
            st.session_state.selected_video = selected_video
            video_id = selected_video.split(".")[0]
            video_path = os.path.join("videos", selected_video)
            st.video(video_path)

            # Step 3: 分析按钮
            if st.button("Analyze Video"):
                with st.spinner("Analyzing video..."):
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.03)
                        progress_bar.progress(i + 1)
                    analyzed_video_path = analyze_video(video_path)
                    st.session_state.analyzed_video_path = analyzed_video_path
                    st.session_state.show_analysis_tabs = True
                st.success("Video analysis complete!")

            # Step 3.5: Tabs 展示（改为动态读取 report.json 内容）
            if st.session_state.show_analysis_tabs:
                st.markdown("### Choose a modality to explore detailed analysis:")
                tabs = st.tabs(["AU Analysis", "VA Plot", "Eye Blink", "Gaze Tracking"])

                video_report = read_full_report(st.session_state.selected_video)
                video_id = st.session_state.selected_video.split(".")[0]

                with tabs[0]:
                    st.markdown("#### Facial Action Unit (AU) Analysis")
                    au_video = video_report.get("AU_video", f"{video_id}_AU.mp4")
                    au_report = video_report.get("AU_report", "No AU report available.")
                    st.video(f"videos/{au_video}")
                    st.markdown(au_report)

                with tabs[1]:
                    st.markdown("#### Valence-Arousal (VA) Analysis")
                    va_plot = video_report.get("VA_plot", f"{video_id}_VA_plot.png")
                    va_report = video_report.get("VA_report", "No VA report available.")
                    st.image(f"videos/{va_plot}", caption="Valence-Arousal Over Time")
                    st.markdown(va_report)

                with tabs[2]:
                    st.markdown("#### Eye Blink Detection")
                    blink_video = video_report.get("Eyeblink_video", f"eyeblink_{video_id}.mp4")
                    blink_report = video_report.get("Eyeblink_report", "No blink report available.")
                    st.video(f"videos/{blink_video}")
                    st.markdown(blink_report)

                with tabs[3]:
                    st.markdown("#### Gaze Tracking")
                    gaze_video = video_report.get("Gaze_tracking", f"gaze_{video_id}.mp4")
                    gaze_report = video_report.get("Gaze_reprot", "No gaze report available.")
                    st.video(f"videos/{gaze_video}")
                    st.markdown(gaze_report)

            # Step 4: 报告生成
            if st.button("Generate Report"):
                with st.spinner("Generating report..."):
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.01)
                        progress_bar.progress(i + 1)
                    report_text = read_report_text(st.session_state.selected_video)
                    st.session_state.report_text = report_text

                st.success("✅ Report generated successfully!")
                st.info("Here's the analysis summary below:")
                # 提取高亮首句（第一行）并加粗展示
                highlight_line = report_text.split('\n')[0].strip()
                st.markdown(f"**🟢 {highlight_line}**")
                st.text_area("📝 Detailed Report Content", report_text, height=200)

            # Step 5: 保存 CSV
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