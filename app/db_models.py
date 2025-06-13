from sqlmodel import Field, Relationship, SQLModel
import datetime as dt
from typing import Optional

class Screen(SQLModel, table = True):
    id_screen : Optional[int] = Field(default=None, primary_key=True)
    name : str
    is_web_cam : bool
    video_file : Optional[str] = Field(default=None) 
    width : Optional[int] = Field(default=None) 
    heigth : Optional[int] = Field(default=None) 

    zone_list : list["Zone"] = Relationship(back_populates="screen")

class Zone(SQLModel, table = True):
    id_zone : Optional[int] = Field(default=None, primary_key=True)
    name : str
    color : str
    x_left : int
    y_top : int
    width : int
    height : int

    screen_id : Optional[int] = Field(default=None, foreign_key="screen.id_screen")
    screen: Optional[Screen] = Relationship(back_populates="zone_list")


class Passage(SQLModel, table = True):
    id_passage : int | None = Field(default=None, primary_key=True)
    zone_id : int | None = Field(default=None, foreign_key="zone.id_zone")
    date : dt.datetime
