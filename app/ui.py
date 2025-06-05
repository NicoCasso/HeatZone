import streamlit as st

def setup_ui():
    st.title("📷 Webcam en direct avec détection améliorée de mouvement")

    if "counted_people" not in st.session_state:
        st.session_state["counted_people"] = {}

    if "standing_timers" not in st.session_state:
        st.session_state["standing_timers"] = {}

    if "run" not in st.session_state:
        st.session_state["run"] = False

    start_button = st.button("▶️ Démarrer")
    stop_button = st.button("⏹️ Arrêter")

    if start_button:
        st.session_state["run"] = True
    if stop_button:
        st.session_state["run"] = False

    return st.empty()  # frame_window
