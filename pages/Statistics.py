import streamlit as st
import plotly.graph_objects as go
import numpy as np
from database import DatabaseManager

# --- Initialize Database ---
db = DatabaseManager("zones.db")
db.create_table()

# --- UI ---
st.title("📊 Statistiques des zones d'intérêt")

zone_counts = {}

# --- Fetch zone data ---
for zone_id in [1, 2]:
    db.insert_zone(zone_id)  # Ensures zones exist
    db.cursor.execute("SELECT number_of_stops FROM ZONES WHERE id = ?", (zone_id,))
    result = db.cursor.fetchone()
    zone_counts[zone_id] = result[0] if result else 0

# --- Show metrics ---
st.metric("Zone 1 (Bleu)", zone_counts[1])
st.metric("Zone 2 (Violet)", zone_counts[2])

# --- Heatmap Data ---
grid = np.zeros((10, 10))

# Example: Zone 1 in top-right, Zone 2 in middle-left
grid[2:5, 7:9] = zone_counts[1]   # Zone 1 (Bleu)
grid[5:7, 2:4] = zone_counts[2]   # Zone 2 (Violet)

# --- Plot Heatmap ---
fig = go.Figure(data=go.Heatmap(
    z=grid,
    colorscale="Viridis",
    colorbar=dict(title="Nombre d'arrêts")
))

# Add annotations for zones
annotations = [
    dict(
        x=7.5,  # x position in heatmap coordinates (center of zone 1)
        y=3.5,  # y position in heatmap coordinates (center of zone 1)
        text="Zone 1 (Bleu)",
        showarrow=False,
        font=dict(color="white", size=14)
    ),
    dict(
        x=2.5,  # center of zone 2 horizontally
        y=6,    # center of zone 2 vertically
        text="Zone 2 (Violet)",
        showarrow=False,
        font=dict(color="white", size=14)
    )
]

fig.update_layout(
    title="🗺️ Carte de chaleur des zones",
    xaxis=dict(showticklabels=False),
    yaxis=dict(showticklabels=False),
    height=500,
    width=500,
    annotations=annotations
)

st.plotly_chart(fig)

db.close()
