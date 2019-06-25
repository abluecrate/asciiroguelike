import tcod


##############################################################################


def renderAll(console, entities, gameMap, screenWidth, screenHeight):
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            wall = gameMap.tiles[x][y].blocked
            if wall:
                tcod.console_set_char_background(console, x, y,
                                                 tcod.blue,
                                                 tcod.BKGND_SET)
            else:
                tcod.console_set_char_background(console, x, y,
                                                 tcod.green,
                                                 tcod.BKGND_SET)

    # Draw Entities in List
    for entity in entities:
        drawEntity(console, entity)

    # Blit Changes
    tcod.console_blit(console, 0, 0, screenWidth, screenWidth, 0, 0, 0)


def drawEntity(console, entity):
    tcod.console_set_default_foreground(console, entity.color)
    tcod.console_put_char(console, entity.x, entity.y, entity.char,
                          tcod.BKGND_NONE)


def clearAll(console, entities):
    for entity in entities:
        clearEntity(console, entity)


def clearEntity(console, entity):
    tcod.console_put_char(console, entity.x, entity.y, ' ', tcod.BKGND_NONE)
