import tcod

def initializeFOV(gameMap):
    # Create New Map
    fovMap = tcod.map_new(gameMap.mapWidth, gameMap.mapHeight)
    # Set Map Properties of Single Tile
    for y in range(gameMap.mapHeight):
        for x in range(gameMap.mapWidth):
            tcod.map_set_properties(fovMap, x, y, 
                                    not gameMap.tiles[x][y].blockSight,
                                    not gameMap.tiles[x][y].blocked)
    return fovMap

def recomputeFOV(fovMap, x, y, radius, lightWalls = True, algorithm = 0):
    tcod.map_compute_fov(fovMap, x, y, radius, lightWalls, algorithm)