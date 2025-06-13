import streamlit as st
import plotly.graph_objects as go
import numpy as np
from db_setup2 import get_engine
from database2 import DatabaseManager2
from db_models import Screen, Zone, Passage
import datetime

# --- Initialize Database ---
engine = get_engine()
db = DatabaseManager2(engine)

# --- UI ---
st.title("📊 Statistiques des zones d'intérêt")

# --- Date selector ---
selected_day = st.date_input("📅 Sélectionnez un jour", datetime.date.today())
#start_of_day = selected_day.strftime("%Y-%m-%d 00:00:00")
#end_of_day = (selected_day + datetime.timedelta(days=1)).strftime("%Y-%m-%d 00:00:00")

period_start = datetime.datetime(selected_day.year, selected_day.month, selected_day.day, 0, 0, 0)
period_end = period_start + datetime.timedelta(days=1)

# Format selected_day as string
selected_day_str = selected_day.strftime("%Y-%m-%d")

current_screen = db.get_webcam_screen()
db_zone_list = db.get_zone_list(current_screen.id_screen)

# --- Fetch zone data for selected day ---
zone_counts = {}
for db_zone in db_zone_list :
    zone_counts[db_zone.id_zone] = db.get_passage_count(db_zone.id_zone, period_start, period_end)

# --- Show metrics ---
st.metric("Zone 1 (Bleu)", zone_counts[1])
st.metric("Zone 2 (Violet)", zone_counts[2])

# --- Heatmap Data ---
grid = np.zeros((10, 10))

# Positioning zones (example layout)
grid[2:5, 7:9] = zone_counts[1]   # Zone 1
grid[5:7, 2:4] = zone_counts[2]   # Zone 2

# --- Plot Heatmap ---
fig = go.Figure(data=go.Heatmap(
    z=grid,
    colorscale="Viridis",
    colorbar=dict(title="Nombre d'arrêts")
))

# Add zone annotations
annotations = [
    dict(x=7.5, y=3.5, text="Zone 1 (Bleu)", showarrow=False, font=dict(color="white", size=14)),
    dict(x=2.5, y=6, text="Zone 2 (Violet)", showarrow=False, font=dict(color="white", size=14)),
]

fig.update_layout(
    title=f"🗺️ Carte de chaleur des zones pour {selected_day_str}",
    xaxis=dict(showticklabels=False),
    yaxis=dict(showticklabels=False),
    height=500,
    width=500,
    annotations=annotations
)

st.plotly_chart(fig)

db.close()
