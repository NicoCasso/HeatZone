import sqlite3
from sqlalchemy import Engine
from sqlmodel import Session, select
from db_models import Screen, Zone, Passage
import datetime as dt

class DatabaseManager2:
    def __init__(self, engine : Engine) :
        self.engine = engine
        

    #__________________________________________________________________________
    #
    # region Zones
    #__________________________________________________________________________
    def get_zone_list(self, screen_id : int) -> list[Zone]:
        with Session(self.engine) as session:
            statement = select(Zone).where(Screen.id_screen == screen_id)
            result = session.exec(statement)
            return list(result)


    def insert_zone(self, zone_id):
        self.cursor.execute("SELECT id FROM ZONES WHERE id=?", (zone_id,))
        if self.cursor.fetchone() is None:
            self.cursor.execute("INSERT INTO ZONES (id, number_of_stops) VALUES (?, 0)", (zone_id,))
            self.conn.commit()

    def add_element(self, id):
        self.cursor.execute('''
            UPDATE ZONES
            SET number_of_stops = number_of_stops + 1
            WHERE id = ?;
        ''', (id,))
        self.conn.commit()

    
    # endregion
    #__________________________________________________________________________
    #
    # region Passage
    #__________________________________________________________________________
    def add_passage(self, zone_id, date : dt.datetime):
        with Session(self.engine) as session:
            passage = Passage(
                zone_id = zone_id, 
                date = date)
            
            session.add(passage)
            session.commit()


    # endregion
    #__________________________________________________________________________
    #
    # region Screen
    #__________________________________________________________________________
    def get_webcam_screen(self) -> Screen :
        with Session(self.engine) as session:
            statement = select(Screen).where(Screen.id_screen == 1)
            result = session.exec(statement)
            return result.one()
    
    # endregion
