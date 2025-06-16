from db_models import Zone

class Rectangle() :  ...

class Rectangle() :
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def is_near_from(self, other : Rectangle) -> bool :
        xi1 = max(self.x1, other.x1)
        yi1 = max(self.y1, other.y1)
        xi2 = min(self.x2, other.x2)
        yi2 = min(self.y2, other.y2)

        if xi1 < xi2 and yi1 < yi2:
            return True
        
        return False

    
    def is_near_from2(self, zone : Zone) -> bool :
        other = Rectangle(
            zone.x_left, 
            zone.y_top, 
            int(zone.x_left+zone.width),
            int(zone.y_top+zone.height))
        
        return self.is_near_from(other)


