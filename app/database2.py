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

    
    # endregion
    #__________________________________________________________________________
    #
    # region Passage
    #__________________________________________________________________________
    def add_passage(self, zone_id : int, date : dt.datetime):
        with Session(self.engine) as session:
            passage = Passage(
                zone_id = zone_id, 
                date = date)
            
            session.add(passage)
            session.commit()

    def get_passage_count(self, zone_id : int, period_start, period_end : dt.datetime ) -> int:
        passage_count = 0
        with Session(self.engine) as session:
            statement = select(Passage).where(Passage.zone_id == zone_id)
            for passage in session.exec(statement).fetchall() :
                if passage.date < period_start :
                    continue
                
                if passage.date > period_end : 
                    continue

                passage_count +=1 

        return passage_count

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
