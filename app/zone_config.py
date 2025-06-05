from rectangle import Rectangle
from interest_zone import InterestZone

def get_interest_zones():
    first_zone = InterestZone(1, "bleu", (0, 0, 255), Rectangle(300, 50, 350, 400))
    second_zone = InterestZone(2, "violet", (255, 0, 255), Rectangle(50, 150, 150, 250))
    return {
        first_zone.id: first_zone,
        second_zone.id: second_zone,
    }
