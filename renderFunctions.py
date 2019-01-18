import tcod
from config import Config

def renderAll(con, entities, map, screenWidth, screenHeight):
    for y in range(map.height):
        for x in range(map.width):
            wall = map.tiles[x][y].blockSight
            if wall:
                tcod.console_set_char_background(con, x, y, Config.COLORS.get('darkWall'), tcod.BKGND_SET)
            else:
                tcod.console_set_char_background(con, x, y, Config.COLORS.get('darkGround'), tcod.BKGND_SET)

    for entity in entities:
        drawEntity(con, entity)

    tcod.console_blit(con, 0, 0, screenWidth, screenHeight, 0, 0, 0)

def drawEntity(con, entity):
    tcod.console_set_default_foreground(con, entity.color)
    tcod.console_put_char(con, entity.x, entity.y, entity.char, tcod.BKGND_NONE)

def clearEntity(con, entity):
    tcod.console_put_char(con, entity.x, entity.y, ' ', tcod.BKGND_NONE)

def clearAll(con, entities):
    for entity in entities:
        clearEntity(con, entity)