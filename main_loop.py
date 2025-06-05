import streamlit as st
import cv2
import time
import numpy as np
from datetime import datetime
from rectangle import Rectangle
from status import Status
from utils import get_bbox_id
from zone_config import get_interest_zones

def run_detection_loop(model, db, frame_window):
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        st.error("❌ Impossible d'accéder à la webcam.")
        return

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
        interest_zones = get_interest_zones()
        current_time = time.time()

        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            current_rectangle = Rectangle(x1, y1, x2, y2)

            near_zone = [
                zone.id for zone in interest_zones.values()
                if current_rectangle.is_near_from(zone.rectangle)
            ]

            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            conf = box.conf[0]

            if label == "person":
                leg_region_prev = prev_gray[y1 + (y2 - y1) // 2 : y2, x1:x2]
                leg_region_curr = gray[y1 + (y2 - y1) // 2 : y2, x1:x2]
                diff = cv2.absdiff(leg_region_curr, leg_region_prev)
                _, diff_thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
                motion_level = np.sum(diff_thresh) / 255

                status = Status.WALKING if motion_level > 1500 else Status.STANDING
                person_id = str(int(box.id)) if hasattr(box, 'id') and box.id is not None else get_bbox_id(x1, y1, x2, y2)

                if status == Status.STANDING and near_zone:
                    for zone_id in near_zone:
                        key = (zone_id, person_id)
                        if key not in st.session_state["standing_timers"]:
                            st.session_state["standing_timers"][key] = current_time
                        else:
                            elapsed = current_time - st.session_state["standing_timers"][key]
                            if elapsed >= 2:
                                if zone_id not in st.session_state["counted_people"]:
                                    st.session_state["counted_people"][zone_id] = set()
                                if person_id not in st.session_state["counted_people"][zone_id]:
                                    db.add_element(zone_id)
                                    db.add_time(zone_id, datetime.now().isoformat())
                                    st.session_state["counted_people"][zone_id].add(person_id)
                else:
                    for zone_id in interest_zones:
                        key = (zone_id, person_id)
                        st.session_state["standing_timers"].pop(key, None)

                current_color = (0, 255, 0)
                if status == Status.STANDING and near_zone:
                    for zone_id in near_zone:
                        if person_id in st.session_state["counted_people"].get(zone_id, set()):
                            current_color = (0, 165, 255)
                        else:
                            current_color = interest_zones[zone_id].color
                        break

                zone_text = f" Z: {near_zone}" if near_zone and status == Status.STANDING else ""
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

        for zone in interest_zones.values():
            cv2.rectangle(
                rgb_frame,
                (zone.rectangle.x1, zone.rectangle.y1),
                (zone.rectangle.x2, zone.rectangle.y2),
                zone.color,
                3,
            )

        cv2.putText(rgb_frame, "Zone Color: Before Logging", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
        cv2.putText(rgb_frame, "Green Box: Person", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
        cv2.putText(rgb_frame, "Orange Box: Already Logged", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,165,255), 1)

        frame_window.image(rgb_frame, channels="RGB")
        prev_gray = gray
        time.sleep(0.03)

    camera.release()
    db.close()
