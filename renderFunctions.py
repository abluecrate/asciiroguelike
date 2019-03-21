import libtcodpy as tcod

#-----------------------------------------------------------------------------------------------
# Draw Entities and Map
def renderAll(console, entities, map, fovMap, fovRecompute, screenWidth, screenHeight, colors):
    if fovRecompute:
        # Draw all map tiles
        for y in range(map.mapHeight):
            for x in range(map.mapWidth):
                visible = tcod.map_is_in_fov(fovMap, x, y)
                wall = map.tiles[x][y].blockSight
                if visible:
                    if wall:
                        tcod.console_set_char_background(console, x, y, colors.get('lightWall'), tcod.BKGND_SET)
                    else:
                        tcod.console_set_char_background(console, x, y, colors.get('lightGround'), tcod.BKGND_SET)
                    map.tiles[x][y].explored = True
                elif map.tiles[x][y].explored:
                    if wall:
                        tcod.console_set_char_background(console, x, y, colors.get('darkWall'), tcod.BKGND_SET)
                    else:
                        tcod.console_set_char_background(console, x, y, colors.get('darkGround'), tcod.BKGND_SET)

    # Draw all entities in list
    for entity in entities:
        drawEntity(console, entity, fovMap)

    # Blit Changes
    tcod.console_blit(console, 0,0, screenWidth, screenHeight, 0,0,0)
#-----------------------------------------------------------------------------------------------
# Draw Entity
def drawEntity(console, entity, fovMap):
    if tcod.map_is_in_fov(fovMap, entity.x, entity.y):
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