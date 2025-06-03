import streamlit as st
from pytube import YouTube
from ultralytics import YOLO
import cv2
import os
from pathlib import Path

# Config Streamlit
st.set_page_config(page_title="YOLO YouTube App", layout="centered")
st.title("🧠 Détection d'objets sur vidéos YouTube avec YOLOv8")

# Session
if "video_path" not in st.session_state:
    st.session_state.video_path = None

# Étape 1 : Téléchargement
st.header("📥 Étape 1 : Télécharger une vidéo YouTube")

url = st.text_input("🔗 Lien de la vidéo YouTube", placeholder="https://www.youtube.com/watch?v=...")
if st.button("Télécharger"):
    if url:
        try:
            yt = YouTube(url)
            stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first()
            output_dir = Path("downloads")
            output_dir.mkdir(exist_ok=True)
            path = stream.download(output_path=str(output_dir))
            st.success("✅ Téléchargement terminé")
            st.session_state.video_path = path
            st.video(path)
        except Exception as e:
            st.error(f"❌ Erreur : {str(e)}")
    else:
        st.warning("⚠️ Veuillez entrer une URL valide.")

# Étape 2 : Détection avec YOLO
st.header("🎯 Étape 2 : Détection d'objets avec YOLOv8")

if st.session_state.video_path:
    if st.button("Lancer la détection"):
        st.info("⏳ Détection en cours...")
        model = YOLO("yolov8n.pt")
        cap = cv2.VideoCapture(st.session_state.video_path)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        output_path = "downloads/yolo_detected.mp4"
        out = cv2.VideoWriter(output_path, fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            results = model(frame, verbose=False)
            annotated_frame = results[0].plot()
            out.write(annotated_frame)

        cap.release()
        out.release()

        st.success("✅ Détection terminée")
        st.video(output_path)
else:
    st.info("💡 Téléchargez d'abord une vidéo pour activer la détection.")
