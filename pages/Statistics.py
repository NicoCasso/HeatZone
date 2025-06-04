import streamlit as st
from database import DatabaseManager

# --- Initialize Database ---
db = DatabaseManager("zones.db")
db.create_table()

# --- UI ---
st.title("📊 Statistiques des zones d'intérêt")

zone_counts = {}

for zone_id in [1, 2]:
    db.insert_zone(zone_id)  # Ensures zones exist
    db.cursor.execute("SELECT number_of_stops FROM ZONES WHERE id = ?", (zone_id,))
    result = db.cursor.fetchone()
    zone_counts[zone_id] = result[0] if result else 0

st.metric("Zone 1 (Bleu)", zone_counts[1])
st.metric("Zone 2 (Violet)", zone_counts[2])

db.close()
