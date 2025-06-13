import streamlit as st
import cv2
import time
import numpy as np
from datetime import datetime
from rectangle import Rectangle
from status import Status
from utils import get_bbox_id, get_color_from_string
from db_functions import DatabaseManager2
from db_models import Zone

from sqlalchemy import Engine

#def run_detection_loop(model, db, frame_window):
def run_detection_loop(model, engine, frame_window):
    db = DatabaseManager2(engine)

    db_screen =  db.get_webcam_screen()
    db_zone_list = db.get_zone_list(screen_id = 1)

    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        st.error("❌ Impossible d'accéder à la webcam.")
        return

    ret, prev_frame = camera.read()
    if not ret:
        st.error("❌ Impossible de lire le flux vidéo initial.")
        return

    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    # Initialize session state values
    st.session_state.setdefault("standing_timers", {})
    st.session_state.setdefault("counted_people", {})
    st.session_state.setdefault("last_counted", {})

    while st.session_state["run"]:
        ret, frame = camera.read()
        if not ret:
            st.warning("⚠️ Problème de capture vidéo.")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        results = model.track(rgb_frame, persist=True, conf=0.4)[0]
        current_time = time.time()

        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            current_rectangle = Rectangle(x1, y1, x2, y2)

            # Identify zone(s) near person
            near_zone_ids = [
                db_zone.id_zone for db_zone in db_zone_list
                if current_rectangle.is_near_from2(db_zone)
            ]

            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            conf = float(box.conf[0])

            if label != "person":
                continue

            # Determine stable person ID
            if hasattr(box, 'id') and box.id is not None:
                person_id = str(int(box.id))
            else:
                person_id = get_bbox_id(x1, y1, x2, y2, tolerance=15)

            # Motion detection in leg region
            leg_region_prev = prev_gray[y1 + (y2 - y1) // 2 : y2, x1:x2]
            leg_region_curr = gray[y1 + (y2 - y1) // 2 : y2, x1:x2]
            diff = cv2.absdiff(leg_region_curr, leg_region_prev)
            _, diff_thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
            motion_level = np.sum(diff_thresh) / 255

            status = Status.WALKING if motion_level > 1500 else Status.STANDING

            for zone_id in near_zone_ids:
                st.session_state["counted_people"].setdefault(zone_id, set())
                st.session_state["last_counted"].setdefault(zone_id, {})

                key = (zone_id, person_id)

                if status == Status.STANDING:
                    if key not in st.session_state["standing_timers"]:
                        st.session_state["standing_timers"][key] = current_time
                    else:
                        elapsed = current_time - st.session_state["standing_timers"][key]
                        last_count_time = st.session_state["last_counted"][zone_id].get(person_id, 0)

                        if elapsed >= 2 and (current_time - last_count_time) > 10:
                            # Not counted recently
                            if person_id not in st.session_state["counted_people"][zone_id]:
                                
                                db.add_element(zone_id)
                                db.add_time(zone_id, datetime.now().isoformat())
                                st.session_state["counted_people"][zone_id].add(person_id)
                                st.session_state["last_counted"][zone_id][person_id] = current_time
                else:
                    # Clear timer when no longer standing
                    st.session_state["standing_timers"].pop(key, None)

            # Draw bounding box
            if status == Status.STANDING and near_zone_ids:
                for zone_id in near_zone_ids:
                    if person_id in st.session_state["counted_people"].get(zone_id, set()):
                        current_color = (0, 165, 255)  # orange (already counted)
                    else:
                        db_zone : Zone = next(filter(lambda dbz: dbz.id_zone==zone_id, db_zone_list))
                        color_from_db = get_color_from_string(db_zone.color)
                        current_color = color_from_db  # zone color
                    break
            else:
                current_color = (0, 255, 0)  # green

            zone_text = f" Z: {near_zone_ids}" if near_zone_ids else ""
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
        for zone in db_zone_list:
            cv2.rectangle(
                rgb_frame,
                (zone.x_left, zone.y_top),
                ((zone.x_left + zone.width), (zone.y_top + zone.height)),
                get_color_from_string(db_zone.color),
                3,
            )

        # Draw legend
        cv2.putText(rgb_frame, "Zone Color: Before Logging", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
        cv2.putText(rgb_frame, "Green Box: Person", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
        cv2.putText(rgb_frame, "Orange Box: Already Logged", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,165,255), 1)

        frame_window.image(rgb_frame, channels="RGB")
        prev_gray = gray
        time.sleep(0.03)

    camera.release()
    db.close()


