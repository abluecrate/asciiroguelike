class Tile:
    def __init__(self, blocked, blockSight=None):
        self.blocked = blocked

        if blockSight is None:
            blockSight = blocked

        self.blockSight = blockSight


# ----------------------------------------------------------------------------


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initializeTiles()

    def initializeTiles(self):
        tiles = [[Tile(False)
                 for y in range(self.height)]
                 for x in range(self.width)]

        tiles[30][22].blocked = True
        tiles[30][22].blockSight = True

        return tiles

    def isBlocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False
