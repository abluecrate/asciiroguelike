from mapObjects.tile import Tile

class GameMap:
    # Game Map Class
    #-----------------------------------------------------------------------------------------------
    def __init__(self, mapWidth, mapHeight):
        self.mapWidth = mapWidth
        self.mapHeight = mapHeight
        self.tiles = self.initializeTiles() # Initialize Default Tiles
    #-----------------------------------------------------------------------------------------------
    def initializeTiles(self):
        # Create Initial Array of Non-Blocking Tiles
        return [[Tile(False) 
                    for y in range(self.mapHeight)] 
                        for x  in range(self.mapWidth)]
    #-----------------------------------------------------------------------------------------------
    def isBlocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
        return False