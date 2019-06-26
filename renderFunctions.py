import tcod


##############################################################################


def renderAll(console, player, entities, gameMap, screenWidth, screenHeight):

    (minY, maxY, minX, maxX) = getView(player, screenWidth, screenHeight)

    for y in range(minY, maxY):
        for x in range(minX, maxX):
            wall = gameMap.tiles[x][y].blocked
            xMapped = x - minX
            yMapped = y - minY
            if wall:
                tcod.console_set_char_background(console, xMapped, yMapped,
                                                 tcod.dark_blue,
                                                 tcod.BKGND_SET)
            else:
                tcod.console_set_char_background(console, xMapped, yMapped,
                                                 tcod.dark_green,
                                                 tcod.BKGND_SET)

    # Draw Player
    tcod.tcod.console_set_default_foreground(console, player.color)
    tcod.console_put_char(console, player.x - minX, player.y - minY, 
                          player.char, tcod.BKGND_NONE)

    # Draw Entities in List
    for entity in entities:
        drawEntity(console, entity)

    # Blit Changes
    tcod.console_blit(console, 0, 0, screenWidth, screenWidth, 0, 0, 0)


def getView(player, screenWidth, screenHeight):
    return (int(player.y - (screenHeight / 2)),
            int(player.y + (screenHeight / 2)),
            int(player.x - (screenWidth / 2)),
            int(player.x + (screenWidth / 2)))


def drawEntity(console, entity):
    tcod.console_set_default_foreground(console, entity.color)
    tcod.console_put_char(console, entity.x, entity.y, entity.char, 
                          tcod.BKGND_NONE)


def clearAll(console, entities):
    for entity in entities:
        clearEntity(console, entity)


def clearEntity(console, entity):
    tcod.console_put_char(console, entity.x, entity.y, ' ', tcod.BKGND_NONE)
