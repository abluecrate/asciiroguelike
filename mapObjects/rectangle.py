class Rectangle:
    def __init__(self, x, y, w, h):
        self.x1 = x         # Top Left X-Coordinate
        self.y1 = y         # Top Left Y-Coordinate
        self.x2 = x + w     # Bottom Right X-Coordinate
        self.y2 = y + h     # Bottom Right Y-Coordinate
    #-----------------------------------------------------------------------------------------------
    def center(self):
        centerX = int((self.x1 + self.x2) / 2)
        centerY = int((self.y1 + self.y2) / 2)
        return (centerX, centerY)
    #-----------------------------------------------------------------------------------------------
    def checkIntersect(self, other):
        # Boolean Check for Intersection of Rectangles 
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)