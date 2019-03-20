import libtcodpy as tcod

#-----------------------------------------------------------------------------------------------
# Draw Entities and Map
def renderAll(console, entities, map, screenWidth, screenHeight, colors):
    # Draw all map tiles
    for y in range(map.mapHeight):
        for x in range(map.mapWidth):
            wall = map.tiles[x][y].blockSight
            if wall:
                tcod.console_set_char_background(console, x, y, colors.get('darkWall'), tcod.BKGND_SET)
            else:
                tcod.console_set_char_background(console, x, y, colors.get('darkGround'), tcod.BKGND_SET)

    # Draw all entities in list
    for entity in entities:
        drawEntity(console, entity)

    # Blit Changes
    tcod.console_blit(console, 0,0, screenWidth, screenHeight, 0,0,0)
#-----------------------------------------------------------------------------------------------
# Draw Entity
def drawEntity(console, entity):
    # Set Position, Color, and Character on Console
    tcod.console_set_default_foreground(console, entity.color)
    tcod.console_put_char(console, entity.x, entity.y, entity.char, tcod.BKGND_NONE)
#-----------------------------------------------------------------------------------------------
# Erase Entity
def clearEntity(console, entity):
    tcod.console_put_char(console, entity.x, entity.y, ' ', tcod.BKGND_NONE)
#-----------------------------------------------------------------------------------------------
# Clear All Entities
def clearAll(console, entities):
    for entity in entities:
        clearEntity(console, entity)
#-----------------------------------------------------------------------------------------------