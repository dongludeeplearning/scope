import os
import json

def get_user_videos(email):
    with open("data/user_videos.json", "r") as f:
        user_map = json.load(f)
    return user_map.get(email, [])

def analyze_video(video_path):
    # TODO: Replace this with actual video analysis logic
    return video_path  # Placeholder: return original video

def generate_report(video_path):
    # TODO: Replace this with actual report generation logic
    return f"Analysis report for {os.path.basename(video_path)}: content is clear, engagement is high, no issues detected."

def read_report_text(video_filename):
    try:
        with open("data/report.json", "r") as f:
            data = json.load(f)
        return data.get(video_filename, {}).get("text_report", "No report found for this video.")
    except Exception as e:
        return f"Error reading report: {e}"
    
def read_full_report(video_filename):
    """
    Reads the full multimodal report entry (AU, VA, blink, gaze, text) for a given video filename.
    Returns a dictionary or empty dict if not found.
    """
    try:
        with open("data/report.json", "r") as f:
            data = json.load(f)
        return data.get(video_filename, {})
    except Exception as e:
        return {"error": str(e)}