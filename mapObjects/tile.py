class Tile:
    # Map Tile Class
    #-----------------------------------------------------------------------------------------------
    def __init__(self, blocked, blockSight = None):
        self.blocked = blocked
        # If tile is blocked, block sight
        if blockSight is None:
            blockSight = blocked
        self.blockSight = blockSight
    #-----------------------------------------------------------------------------------------------