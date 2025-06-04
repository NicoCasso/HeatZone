import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
import time
from rectangle import Rectangle
from interest_zone import InterestZone
from status import Status
from database import DatabaseManager

# --- Streamlit UI ---
st.title("📷 Webcam en direct avec détection améliorée de mouvement")

# --- Initialize Database ---
db = DatabaseManager("zones.db")
db.create_table()
db.insert_zone(1)
db.insert_zone(2)

# --- Track counted people ---
if "counted_people" not in st.session_state:
    st.session_state["counted_people"] = {}  # format: {zone_id: set of person_ids}

# --- YOLOv8 Model ---
model = YOLO("yolov8n.pt")

# --- Controls ---
if "run" not in st.session_state:
    st.session_state["run"] = False

start_button = st.button("▶️ Démarrer")
stop_button = st.button("⏹️ Arrêter")

if start_button:
    st.session_state["run"] = True
if stop_button:
    st.session_state["run"] = False

# --- Frame display ---
frame_window = st.empty()

# --- BBox ID helper (used only as fallback) ---
def get_bbox_id(x1, y1, x2, y2, tolerance=10):
    x1 = (x1 // tolerance) * tolerance
    y1 = (y1 // tolerance) * tolerance
    x2 = (x2 // tolerance) * tolerance
    y2 = (y2 // tolerance) * tolerance
    return f"{x1}-{y1}-{x2}-{y2}"

# --- Main Logic ---
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

            results = model.track(rgb_frame, persist=True, conf=0.4)[0]

            # Define zones
            first_zone = InterestZone(1, "bleu", (0, 0, 255), Rectangle(300, 50, 350, 400))
            second_zone = InterestZone(2, "violet", (255, 0, 255), Rectangle(50, 150, 150, 250))

            interest_zones = {
                first_zone.id: first_zone,
                second_zone.id: second_zone,
            }

            for box in results.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                current_rectangle = Rectangle(x1, y1, x2, y2)

                near_zone = []
                for zone in interest_zones.values():
                    if current_rectangle.is_near_from(zone.rectangle):
                        near_zone.append(zone.id)

                cls_id = int(box.cls[0])
                label = model.names[cls_id]
                conf = box.conf[0]

                if label == "person":
                    # Motion detection in leg region
                    leg_region_prev = prev_gray[y1 + (y2 - y1) // 2 : y2, x1:x2]
                    leg_region_curr = gray[y1 + (y2 - y1) // 2 : y2, x1:x2]

                    diff = cv2.absdiff(leg_region_curr, leg_region_prev)
                    _, diff_thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
                    motion_level = np.sum(diff_thresh) / 255

                    status = Status.WALKING if motion_level > 1500 else Status.STANDING

                    zone_text = ""
                    if status == Status.STANDING and len(near_zone) != 0:
                        zone_text = f" Z: {near_zone}"

                        # Use YOLO tracking ID if available
                        person_id = str(int(box.id)) if hasattr(box, 'id') and box.id is not None else get_bbox_id(x1, y1, x2, y2)

                        for zone_id in near_zone:
                            if zone_id not in st.session_state["counted_people"]:
                                st.session_state["counted_people"][zone_id] = set()

                            if person_id not in st.session_state["counted_people"][zone_id]:
                                db.add_element(zone_id)
                                st.session_state["counted_people"][zone_id].add(person_id)

                    current_color = (0, 255, 0)
                    if status == Status.STANDING and len(near_zone) > 0:
                        current_color = interest_zones[near_zone[0]].color

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

            # Draw zones
            for zone in interest_zones.values():
                cv2.rectangle(
                    rgb_frame,
                    (zone.rectangle.x1, zone.rectangle.y1),
                    (zone.rectangle.x2, zone.rectangle.y2),
                    zone.color,
                    3,
                )

            frame_window.image(rgb_frame, channels="RGB")
            prev_gray = gray
            time.sleep(0.03)

        camera.release()
        db.close()
else:
    st.write("Cliquez sur ▶️ Démarrer pour lancer la webcam.")



