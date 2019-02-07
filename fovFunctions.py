import tcod

def initializeFOV(map):
    fovMap = tcod.map_new(map.width,map.height)
    for y in range(map.height):
        for x in range(map.width):
            tcod.map_set_properties(fovMap, x, y, not map.tiles[x][y].blockSight, not map.tiles[x][y].blocked)
    return fovMap

def recomputeFOV(fovMap, x, y, radius, lightWalls = True, algorithm = 0):
    tcod.map_compute_fov(fovMap, x, y, radius, lightWalls, algorithm)