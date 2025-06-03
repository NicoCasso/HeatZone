import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
import time

st.title("📷 Webcam en direct avec Streamlit")

# Chargement du modèle YOLOv8
model = YOLO("yolov8n.pt")  # YOLOv8 nano (rapide)

# État de la checkbox
run = st.checkbox("📹 Activer la détection")

# Espace pour afficher l'image
frame_window = st.image([])

# Variable de contrôle de la caméra
camera = None

if run:
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        st.error("❌ Impossible d'accéder à la webcam.")
    else:
        while run:
            ret, frame = camera.read()
            if not ret:
                st.warning("⚠️ Problème de capture vidéo.")
                break

            # Conversion BGR → RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Prédictions YOLO
            results = model.predict(rgb_frame, conf=0.4)[0]

            # Dessiner les cadres sur l'image
            for box in results.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                label = model.names[int(box.cls[0])]
                conf = box.conf[0]

                # Dessin des rectangles et du label
                cv2.rectangle(rgb_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(rgb_frame, f"{label} ({conf:.2f})", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

            frame_window.image(rgb_frame, channels="RGB")

            # Vérifie si l'utilisateur a décoché la case
            run = st.session_state.get("run_checkbox", run)
            time.sleep(0.03)  # petit délai pour éviter un usage CPU excessif

        camera.release()
        st.success("✅ Caméra arrêtée.")

# Synchronisation de l'état de la checkbox avec session_state
st.session_state["run_checkbox"] = run