import streamlit as st
from model_utils import load_model

#from db_setup import initialize_database
from sqlalchemy import Engine
from db_setup2 import get_engine
from database2 import DatabaseManager2

from ui import setup_ui
from main_loop import run_detection_loop

# Load model and database once
model = load_model()

#db = initialize_database()
engine = get_engine()
db = DatabaseManager2(engine)

# Render UI (buttons etc) — this should set st.session_state["run"]
frame_window = setup_ui()

# Ensure 'run' key exists in session_state
if "run" not in st.session_state:
    st.session_state["run"] = False

if st.session_state["run"]:
    run_detection_loop(model, db, frame_window)
else:
    st.write("Cliquez sur ▶️ Démarrer pour lancer la webcam.")





