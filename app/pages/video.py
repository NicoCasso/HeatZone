import streamlit as st
import cv2
import numpy as np
import os
import tempfile
import base64
from moviepy.editor import VideoFileClip
from model_utils import load_model

@st.cache_resource
def load_yolo_model():
    return load_model()

model = load_yolo_model()

st.title("🎯 YOLOv8 Video with Audio Playback")

uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi", "mkv"])

def extract_audio_from_video(video_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio
    audio_tempfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    audio_clip.write_audiofile(audio_tempfile.name, logger=None)
    audio_clip.close()
    video_clip.close()
    return audio_tempfile.name

def autoplay_audio(video_path):
    audio_path = extract_audio_from_video(video_path)
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()
    b64_audio = base64.b64encode(audio_bytes).decode()
    audio_html = f"""
    <audio autoplay controls>
        <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
        Your browser does not support the audio element.
    </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)
    os.remove(audio_path)  # Clean up audio temp file

def run_video_detection(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_placeholder = st.empty()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = model(rgb_frame)

        # Assuming results[0].plot() returns annotated frame in RGB format
        annotated_frame = results[0].plot()

        frame_placeholder.image(annotated_frame, channels="RGB")

    cap.release()

if uploaded_file is not None:
    # Save uploaded video to temp file
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tfile.write(uploaded_file.read())
    video_path = tfile.name

    try:
        autoplay_audio(video_path)  # Autoplay extracted audio

        if st.button("Run Detection on Uploaded Video"):
            run_video_detection(video_path)
            st.success("Processing finished ✅")

    except Exception as e:
        st.error(f"Error: {str(e)}")

    finally:
        if os.path.exists(video_path):
            os.remove(video_path)

else:
    st.info("Or run detection on the example video below if you don't want to upload a file.")
    if st.button("Run Detection on Example Video"):
        example_video_path = "/home/david/Heat/HeatZone/app/Rick Astley - Never Gonna Give You Up (Official Video) (4K Remaster).mp4"

        if not os.path.exists(example_video_path):
            st.error("Example video not found.")
        else:
            try:
                autoplay_audio(example_video_path)  # Autoplay example audio
                run_video_detection(example_video_path)
                st.success("Processing finished ✅")
            except Exception as e:
                st.error(f"Error: {str(e)}")
