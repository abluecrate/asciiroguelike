from mapObjects.tile import Tile

class gameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.intitializeTiles()

    def intitializeTiles(self):
        tiles = [[Tile(False) for y in range(self.height)] for x in range(self.width)]
        return tiles

    def isBlocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
        return False