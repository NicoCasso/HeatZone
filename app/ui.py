import streamlit as st
from streamlit.delta_generator import DeltaGenerator
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

    if "new_zone" not in st.session_state:
        st.session_state["new_zone"] = False

    left_side, right_side = st.columns([6,4], gap="small")

    if  st.session_state["run"] == False :
        start_button = left_side.button("▶️ Démarrer")
        if start_button : 
            st.session_state["run"] = True
            st.rerun()
    else :
        stop_button = left_side.button("⏹️ Arrêter")
        if stop_button:
            st.session_state["run"] = False
            st.rerun()

    put_right_panel_on_screen(right_side, db, screen_id)

    return left_side.empty()  # frame_window
