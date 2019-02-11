import tcod
import math

#######################################################################################

class Entity:

    #----------------------------------------------------------------------------------

    def __init__(self, x, y, char, color, name, 
                 blocks = False, fighter = None, ai = None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.fighter = fighter
        self.ai = ai
    
        if self.fighter:
            self.fighter.owner = self
        if self.ai:
            self.ai.owner = self

    #----------------------------------------------------------------------------------

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    #----------------------------------------------------------------------------------

    def moveTowards(self, targetX, targetY, gameMap, entities):
        dx = targetX - self.x
        dy = targetY - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not (gameMap.isBlocked(self.x + dx, self.y + dy) or 
                getBlockingEntities(entities, self.x + dx, self.y + dy)):
            self.move(dx, dy)

    #----------------------------------------------------------------------------------

    def moveAStar(self, target, entities, gameMap):
        fov = tcod.map_new(gameMap.width, gameMap.height)

        for y1 in range(gameMap.height):
            for x1 in range(gameMap.width):
                tcod.map_set_properties(fov, x1, y1, 
                                        not gameMap.tiles[x1][y1].blockSight,
                                        not gameMap.tiles[x1][y1].blocked)

        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                tcod.map_set_properties(fov, entity.x, entity.y, True, False)

        path = tcod.path_new_using_map(fov, 1.41)

        tcod.path_compute(path, self.x, self.y, target.x, target.y)

        if not tcod.path_is_empty(path) and tcod.path_size(path) < 25:

            x, y = tcod.path_walk(path, True)
            if x or y:
                self.x = x
                self.y = y
        else:
            self.moveTowards(target.x, target.y, gameMap, entities)

        tcod.path_delete(path)

    #----------------------------------------------------------------------------------

    def distanceTo(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

#######################################################################################

def getBlockingEntities(entities, destinationX, destinationY):
    for entity in entities:
        if entity.blocks and entity.x == destinationX and entity.y == destinationY:
            return entity
    return None