class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        centerX = int((self.x1 + self.x2)/2)
        centerY = int((self.y1 + self.y2)/2)
        return centerX, centerY
    
    def checkIntersect(self, otherRectangle):
        return (self.x1 <= otherRectangle.x2 and self.x2 >= otherRectangle.x1 and
                self.y1 <= otherRectangle.y2 and self.y2 >= otherRectangle.y1)
