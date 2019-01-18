class Tile:
    def __init__(self, blocked, blockSight = None):
        self.blocked = blocked
        if blockSight is None:
            blockSight = blocked
        self.blockSight = blockSight