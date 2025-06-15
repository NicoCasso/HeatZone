import streamlit as st
from ui_right_side import put_right_panel_on_screen
from database2 import DatabaseManager2

def setup_ui(db : DatabaseManager2, screen_id :int):
    st.title("📷 Webcam en direct avec détection améliorée de mouvement")

    if "counted_people" not in st.session_state:
        st.session_state["counted_people"] = {}

    if "standing_timers" not in st.session_state:
        st.session_state["standing_timers"] = {}

    if "run" not in st.session_state:
        st.session_state["run"] = False

    left_side, right_side = st.columns([6,4], gap="small")

    column_start, column_stop = left_side.columns([1,1])
    start_button = column_start.button("▶️ Démarrer")
    stop_button = column_stop.button("⏹️ Arrêter")

    if start_button:
        st.session_state["run"] = True
    if stop_button:
        st.session_state["run"] = False

    put_right_panel_on_screen(right_side, db, screen_id)

    current_line = left_side.container(border=True)

    return current_line.empty()  # frame_window
