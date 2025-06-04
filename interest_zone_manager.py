from interest_zone import InterestZone
from rectangle import Rectangle

class InterestZoneManager():
    def __init__(self) :
        self.zones = {}

    def initialize(self): 
        first_zone = InterestZone(1, "bleu", (0, 0, 255), Rectangle(300, 50, 350, 400))
        second_zone = InterestZone(2, "violet", (255, 0, 255), Rectangle(50, 150, 150, 250))

        self.zones[first_zone.id] = first_zone
        self.zones[second_zone.id] = second_zone


    