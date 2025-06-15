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
        
    def insert_zone(self, screen_id: int, name: str, color:str, x_left:int, y_top:int, width:int, height:int ) :
        with Session(self.engine) as session:
            new_zone = Zone(
                name=name, 
                color = color, 
                x_left= x_left,
                y_top = y_top,
                width = width ,
                height = height)            
        
            session.add(new_zone)
            session.commit()

    def delete_zone(self, zone_id: int) -> bool:
        with Session(self.engine) as session:
            statement = select(Zone).where(Zone.id_zone == zone_id)
            results = session.exec(statement)
            linked_zone = results.one()
            session.delete(linked_zone)
            session.commit()
            return True
        
        return False

    
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
    def get_screen(self, screen_id) -> Screen :
        screen = None
        with Session(self.engine) as session:
            statement = select(Screen).where(Screen.id_screen == screen_id)
            result = session.exec(statement)
            screen = result.one()
        
        if not screen :
            raise Exception("that screen does not exist")

        return screen
    
    def get_webcam_screen(self) -> Screen :
        return self.get_screen(1)
        
    def update_screen_size(self, screen_id: int, width: int, height : int) -> Screen:
        screen = None
        with Session(self.engine) as session:
            statement = select(Screen).where(Screen.id_screen == screen_id)
            screen = session.exec(statement).one()

            screen.width = width
            screen.heigth = height

            session.add(screen)
            session.commit()
            session.refresh(screen)
    
        if not screen :
            raise Exception("that screen does not exist")

        return screen
            


           

    
    # endregion
