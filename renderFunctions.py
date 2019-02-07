import tcod
from config import Config

def renderAll(con, entities, map, fovMap, fovRecompute, screenWidth, screenHeight):
    if fovRecompute:
        for y in range(map.height):
            for x in range(map.width):
                visible = tcod.map_is_in_fov(fovMap, x, y)
                wall = map.tiles[x][y].blockSight
                if visible:
                    if wall:
                        tcod.console_set_char_background(con, x, y, Config.COLORS.get('lightWall'), tcod.BKGND_SET)
                    else:
                        tcod.console_set_char_background(con, x, y, Config.COLORS.get('lightGround'), tcod.BKGND_SET)
                    map.tiles[x][y].explored = True

                elif map.tiles[x][y].explored:
                    if wall:
                        tcod.console_set_char_background(con, x, y, Config.COLORS.get('darkWall'), tcod.BKGND_SET)
                    else:
                        tcod.console_set_char_background(con, x, y, Config.COLORS.get('darkGround'), tcod.BKGND_SET)

    for entity in entities:
        drawEntity(con, entity, fovMap)

    tcod.console_blit(con, 0, 0, screenWidth, screenHeight, 0, 0, 0)

def drawEntity(con, entity, fovMap):
    if tcod.map_is_in_fov(fovMap, entity.x, entity.y):
        tcod.console_set_default_foreground(con, entity.color)
        tcod.console_put_char(con, entity.x, entity.y, entity.char, tcod.BKGND_NONE)

def clearEntity(con, entity):
    tcod.console_put_char(con, entity.x, entity.y, ' ', tcod.BKGND_NONE)

def clearAll(con, entities):
    for entity in entities:
        clearEntity(con, entity)