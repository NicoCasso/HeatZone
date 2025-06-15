import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from database2 import DatabaseManager2

def put_right_panel_on_screen(right_side : DeltaGenerator, db : DatabaseManager2, screen_id):
    right_side.write("Zones")
    current_line = right_side.container(border=True)

    columns_proportions = [2,2]
    if st.session_state["run"] == True :
        columns_proportions = [2,3,2]

    columns = current_line.columns(columns_proportions, gap ="small")
        
    columns[0].write("zone")
    columns[1].write("nom")
    
    if st.session_state["run"] == True :
        columns[2].write("action")

    for zone in  db.get_zone_list(screen_id):
        columns = current_line.columns(columns_proportions, gap ="small")
        columns[0].write(f"{zone.id_zone}") 
        columns[1].write(f"{zone.name}") 
        if st.session_state["run"] == True :
            if columns[2].button("sup", key ="sup"+str(zone.id_zone) ) :
                db.delete_zone(zone.id_zone)
                st.session_state.clear()
                st.rerun()

    if st.session_state["run"] == True :
        new_zone = right_side.button("ajouter")
        if new_zone :
            st.session_state["new_zone"] = True