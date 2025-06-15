import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from database2 import DatabaseManager2

def put_right_panel_on_screen(right_side : DeltaGenerator, db : DatabaseManager2, screen_id):
    new_zone  = st.session_state.get("new_zone", False) 
    if new_zone :
        right_side.write("Nouvelle zone")
    else :
        right_side.write("Zones")

    current_line = right_side.container(border=True)
    if new_zone :
        show_create_zone(current_line, db, screen_id)
    else:
        show_zone_list(current_line, db, screen_id)

    if not new_zone :
        new_zone = right_side.button("ajouter")

    if new_zone :
        st.session_state["new_zone"] = True
        st.rerun()

def show_zone_list(current_line : DeltaGenerator, db : DatabaseManager2, screen_id) :
    
    columns_proportions = [2,3,2]
    columns = current_line.columns(columns_proportions, gap ="small")
        
    columns[0].write("zone")
    columns[1].write("nom") 
    columns[2].write("action")

    for zone in db.get_zone_list(screen_id):
        columns = current_line.columns(columns_proportions, gap ="small")
        columns[0].write(f"{zone.id_zone}") 
        columns[1].write(f"{zone.name}") 
        button_key = "sup"+str(zone.id_zone)
        if columns[2].button(label="sup", key = button_key ) :
            db.delete_zone(zone.id_zone)
            st.rerun()

def show_create_zone(current_line : DeltaGenerator, db : DatabaseManager2, screen_id) :
    
    columns_proportions = [1,3]
    columns = current_line.columns(columns_proportions, gap ="small")

    columns[0].write("clé")
    columns[1].write("valeur")

    columns = current_line.columns(columns_proportions, gap ="small")
    columns[0].write("name")
    zone_name = columns[1].text_input(label="", value="rouge", key="zone_name")

    columns = current_line.columns([1,1,1,1], gap ="small", vertical_alignment="center")
    columns[0].write("color")
    zone_color_R = columns[1].number_input(label="R", min_value =0, max_value = 255, value =255, step=1, format="%d", key="zone_color_R")
    zone_color_V = columns[2].number_input(label="V", min_value =0, max_value = 255, value =0, step=1, format="%d", key="zone_color_V")
    zone_color_B = columns[3].number_input(label="B", min_value =0, max_value = 255, value =0, step=1, format="%d", key="zone_color_B")
    zone_color = f"({int(zone_color_R)},{int(zone_color_V)},{int(zone_color_B)})"

    screen = db.get_screen(screen_id)
    max_width = screen.width
    max_height = screen.heigth

    columns = current_line.columns(columns_proportions, gap ="small", vertical_alignment="center")
    columns[0].write("left")
    zone_x_left = columns[1].number_input(label = "", min_value =0, max_value = max_width, value = max_width//4,  step=1, format="%d", key="zone_x_left")
    zone_x_left = int(zone_x_left)
 
    columns = current_line.columns(columns_proportions, gap ="small", vertical_alignment="center")
    columns[0].write("top")
    zone_y_top =  columns[1].number_input(label = "", min_value =0, max_value = max_height, value = max_height//4, step=1, format="%d", key="zone_y_top")
    zone_y_top = int(zone_y_top)

    
    columns = current_line.columns(columns_proportions, gap ="small", vertical_alignment="center")
    columns[0].write("width")
    zone_width = columns[1].number_input(label = "", min_value =0, max_value = max_width, value = max_width//2, step=1, format="%d", key="zone_width")
    zone_width = int(zone_width)

     
    columns = current_line.columns(columns_proportions, gap ="small", vertical_alignment="center")
    columns[0].write("height")
    zone_height = columns[1].number_input(label = "", min_value =0, max_value = max_height, value = max_height//2, step=1, format="%d", key="zone_height")
    zone_height = int(zone_height)

    left_col, rigth_col = current_line.columns([1,1])

    commit_zone =left_col.button("envoyer")
    if commit_zone:
        db.insert_zone(screen_id, zone_name, zone_color, zone_x_left, zone_y_top, zone_width, zone_height)
        
    cancel = rigth_col.button("annuler")
    if commit_zone or cancel :
        st.session_state["new_zone"] = False
        st.rerun()

    