import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
import time
from rectangle import Rectangle
from interest_zone import InterestZone
from status import Status

st.title("📷 Webcam en direct avec détection améliorée de mouvement")

model = YOLO("yolov8n.pt")

if "run" not in st.session_state:
    st.session_state["run"] = False

start_button = st.button("▶️ Démarrer")
stop_button = st.button("⏹️ Arrêter")

if start_button:
    st.session_state["run"] = True
if stop_button:
    st.session_state["run"] = False

frame_window = st.empty()

if st.session_state["run"]:
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        st.error("❌ Impossible d'accéder à la webcam.")
    else:
        ret, prev_frame = camera.read()
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

        while st.session_state["run"]:
            ret, frame = camera.read()
            if not ret:
                st.warning("⚠️ Problème de capture vidéo.")
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            results = model.predict(rgb_frame, conf=0.4)[0]
          
            first_zone = InterestZone(1, "bleu", (0, 0, 255), Rectangle(300, 50, 350, 400))
            second_zone = InterestZone(2, "violet", (255, 0, 255), Rectangle(50, 150, 150, 250))

            interest_zones = {}
            interest_zones[first_zone.id] = first_zone
            interest_zones[second_zone.id] = second_zone

            for box in results.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                current_rectangle = Rectangle(x1,y1,x2,y2)
                near_zone = []
                for zone in interest_zones.values() :
                    zone : InterestZone = zone
                    if current_rectangle.is_near_from(zone.rectangle) :
                        near_zone.append(zone.id) 

                cls_id = int(box.cls[0])
                label = model.names[cls_id]
                conf = box.conf[0]

                if label == "person":
                    # Get lower half of the bounding box for motion detection (legs area)
                    leg_region_prev = prev_gray[y1 + (y2 - y1) // 2 : y2, x1:x2]
                    leg_region_curr = gray[y1 + (y2 - y1) // 2 : y2, x1:x2]

                    # Calculate motion only in legs region
                    diff = cv2.absdiff(leg_region_curr, leg_region_prev)
                    _, diff_thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

                    motion_level = np.sum(diff_thresh) / 255  # Number of changed pixels

                    status = Status.WALKING if motion_level > 1500 else Status.STANDING

                    zone_text =""
                    match status :
                        case Status.WALKING : 
                            current_color = (0, 255, 0)

                        case Status.STANDING : 
                            current_color = (0, 255, 0)
                            if len(near_zone) !=0 :
                                zone_text = f" Z: {near_zone}"

                            for id in near_zone :
                                zone = interest_zones[id]
                                current_color = zone.color

                    cv2.rectangle(rgb_frame, (x1, y1), (x2, y2), current_color, 2)
                    cv2.putText(
                        rgb_frame,
                        f"{status} ({conf:.2f}){zone_text}",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (255, 255, 0),
                        2,
                    )

            for zone in interest_zones.values() :
                interest_zone : InterestZone = zone
                cv2.rectangle(rgb_frame, 
                              (interest_zone.rectangle.x1, interest_zone.rectangle.y1), 
                              (interest_zone.rectangle.x2, interest_zone.rectangle.y2), 
                              interest_zone.color, 3)

            frame_window.image(rgb_frame, channels="RGB")

            prev_gray = gray
            time.sleep(0.03)

        camera.release()
else:
    st.write("Cliquez sur ▶️ Démarrer pour lancer la webcam.")


