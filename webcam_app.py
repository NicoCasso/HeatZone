import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
import time
from datetime import datetime
from rectangle import Rectangle
from interest_zone import InterestZone
from status import Status
from database import DatabaseManager
from db_setup import initialize_database
from utils import get_bbox_id
from zone_config import get_interest_zones
from model_utils import load_model
from ui import setup_ui
from main_loop import run_detection_loop 

model = load_model()
db = initialize_database()
frame_window = setup_ui()

# --- Main Logic ---
if st.session_state["run"]:
    run_detection_loop(model, db, frame_window)
else:
    st.write("Cliquez sur ▶️ Démarrer pour lancer la webcam.")






