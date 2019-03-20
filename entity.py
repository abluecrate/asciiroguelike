class Entity:
    # Generic Game Object
    #-----------------------------------------------------------------------------------------------
    def __init__(self, x, y, char, color):
        self.x = x          # X-Coordinate
        self.y = y          # Y-Coordinate
        self.char = char    # Character
        self.color = color  # Color
    #-----------------------------------------------------------------------------------------------
    def move(self, dx, dy):
        self.x += dx    # X-Coordinate Delta
        self.y += dy    # Y-Coordinate Delta
    #-----------------------------------------------------------------------------------------------