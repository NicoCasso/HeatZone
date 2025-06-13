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
        xi2 = min(self.x2, other.x2)
        if xi1 > xi2 :
           return False
        
        yi1 = max(self.y1, other.y1)
        yi2 = min(self.y2, other.y2)
        if yi1 > yi2:
            return False
        
        return True
    
    def is_near_from2(self, other : Zone) -> bool :
        xi1 = max(self.x1, other.x_left)
        xi2 = min(self.x2, int(other.x_left + other.width))
        if xi1 > xi2 :
           return False
           
 
        yi1 = max(self.y1, other.y_top)
        yi2 = min(self.y2, int(other.y_top+other.height))
        if yi1 < yi2:
            return False
        
        return True


