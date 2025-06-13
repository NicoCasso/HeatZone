import sqlmodel as sm
from sqlalchemy import Engine
from db_models import Screen, Zone
from interest_zone import InterestZone
from rectangle import Rectangle
from zone_config import get_interest_zones

def get_engine() -> Engine :

    sqlitefile_name = "data/zones2.db"
    sqlite_url = f"sqlite:///{sqlitefile_name}"
    engine = sm.create_engine(sqlite_url, echo = True)

    return engine

def populate_db(engine : Engine):
    
    with sm.Session(engine) as session :
        webcam = Screen(id_screen=1, name="webcam", is_web_cam=True)
        session.add(webcam)
        session.commit()

        for id, content in get_interest_zones().items() :
            interest_zone : InterestZone = content
            zone = Zone(
                id_zone = id, 
                name= interest_zone.color_name, 
                color = str(interest_zone.color),
                x_left = min(interest_zone.rectangle.x1, interest_zone.rectangle.x2),
                y_top = min(interest_zone.rectangle.y1, interest_zone.rectangle.y2),
                width = abs( interest_zone.rectangle.x2 - interest_zone.rectangle.x1 ),
                height = abs( interest_zone.rectangle.y2 - interest_zone.rectangle.y1 )
            )
            session.add(zone)

        session.commit()

if __name__ == "__main__" :
   engine = get_engine()
   echo_object = sm.SQLModel.metadata.create_all(engine)
   print(echo_object)
   populate_db(engine) 