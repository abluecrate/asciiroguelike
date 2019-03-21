import math
import libtcodpy as tcod

class Entity:
    # Generic Game Object
    #-----------------------------------------------------------------------------------------------
    def __init__(self, x, y, char, color, name, 
                 blocks = False, fighter = None, ai = None):
        self.x = x          # X-Coordinate
        self.y = y          # Y-Coordinate
        self.char = char    # Character
        self.color = color  # Color
        self.name = name    # Entity Name
        self.blocks = blocks    # Block Movement

        self.fighter = fighter          # Adds Fighter Component
        if self.fighter:                # Checks for Fighter Component
            self.fighter.owner = self   # Sets Owner of Component

        self.ai = ai                # Adds AI Component
        if self.ai:                 # Checks for AI Component
            self.ai.owner = self    # Sets Owner of Component
    #-----------------------------------------------------------------------------------------------
    def move(self, dx, dy):
        self.x += dx    # X-Coordinate Delta
        self.y += dy    # Y-Coordinate Delta
    #-----------------------------------------------------------------------------------------------
    def moveTowards(self, targetX, targetY, gameMap, entities):
        # Distance Between Entity and Target
        dx = targetX - self.x
        dy = targetY - self.y

        # Euclidean Distance
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # Round to Integer
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        # Check For Blocked Tiles / Blocking Entities
        if not (gameMap.isBlocked(self.x + dx, self.y + dy) or
                getBlockingEntities(entities, self.x + dx, self.y + dy)):
            self.move(dx,dy)
    #-----------------------------------------------------------------------------------------------
    def moveAStar(self, target, entities, gameMap):
        # Create a new FOV map
        fov = tcod.map_new(gameMap.mapWidth, gameMap.mapHeight)
        # Scan current map and set all walls as unwalkable
        for y1 in range(gameMap.mapHeight):
            for x1 in range(gameMap.mapWidth):
                tcod.map_set_properties(fov, x1, y1,
                                        not gameMap.tiles[x1][y1].blockSight,
                                        not gameMap.tiles[x1][y1].blocked)

        # Scan for blocking entities
        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                tcod.map_set_properties(fov, entity.x, entity.y, True, False)

        # Allocate A* Path - No Diagonal Movement
        path = tcod.path_new_using_map(fov, 0.0)
        # Compute path
        tcod.path_compute(path, self.x, self.y, target.x, target.y)

        # Check if path exists and is shorter than 25 moves
        if not tcod.path_is_empty(path) and tcod.path_size(path) < 25:
            x, y = tcod.path_walk(path, recompute = True)
            # Set X and Y coordinates
            if x or y:
                self.x = x
                self.y = y
        else:
            # Backup Move Function
            self.moveTowards(target.x, target.y, gameMap, entities)
        
        tcod.path_delete(path)
    #-----------------------------------------------------------------------------------------------
    def distanceTo(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

#-----------------------------------------------------------------------------------------------
################################################################################################
#-----------------------------------------------------------------------------------------------
def getBlockingEntities(entities, destinationX, destinationY):
    for entity in entities:
        # Check If Entity Blocks Movement and is in Path
        if entity.blocks and entity.x == destinationX and entity.y == destinationY:
            return entity
    return None