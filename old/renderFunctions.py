import tcod
from config import Config
from enum import Enum
from gameStates import gameStates
from menus import inventoryMenu

#######################################################################################

class renderOrder(Enum):
    corpse = 1
    item = 2
    actor = 3

#######################################################################################

def getNamesUnderMouse(mouse, entities, fovMap):
    x,y = (mouse.cx, mouse.cy)
    names = [entity.name for entity in entities
             if entity.x == x and entity.y == y and tcod.map_is_in_fov(fovMap, entity.x, entity.y)]
    names = ', '.join(names)
    return names.capitalize()

#----------------------------------------------------------------------------------

def renderBar(panel, x, y, totalWidth, name, value, maximum, barColor, backColor):
    barWidth = int(float(value) / maximum * totalWidth)
    
    tcod.console_set_default_background(panel, backColor)
    tcod.console_rect(panel, x, y, totalWidth, 1, False, tcod.BKGND_SCREEN)
    tcod.console_set_default_background(panel, backColor)

    if barWidth > 0:
        tcod.console_rect(panel, x, y, barWidth, 1, False, tcod.BKGND_SCREEN)
    
    tcod.console_set_default_foreground(panel, tcod.white)
    tcod.console_print_ex(panel, int(x + totalWidth / 2), y, tcod.BKGND_MULTIPLY, tcod.CENTER,
                          '{}: {}/{}'.format(name, value, maximum))

#----------------------------------------------------------------------------------

def renderAll(con, panel, entities, player, gameMap, fovMap, fovRecompute, messageLog,
              screenWidth, screenHeight, barWidth, panelHeight, panelY, mouse, colors, gameState):
    if fovRecompute:
        for y in range(gameMap.height):
            for x in range(gameMap.width):
                visible = tcod.map_is_in_fov(fovMap, x, y)
                wall = gameMap.tiles[x][y].blockSight
                if visible:
                    if wall:
                        tcod.console_set_char_background(con, x, y, Config.COLORS.get('lightWall'), tcod.BKGND_SET)
                    else:
                        tcod.console_set_char_background(con, x, y, Config.COLORS.get('lightGround'), tcod.BKGND_SET)
                    gameMap.tiles[x][y].explored = True

                elif gameMap.tiles[x][y].explored:
                    if wall:
                        tcod.console_set_char_background(con, x, y, Config.COLORS.get('darkWall'), tcod.BKGND_SET)
                    else:
                        tcod.console_set_char_background(con, x, y, Config.COLORS.get('darkGround'), tcod.BKGND_SET)

    entitiesInRenderOrder = sorted(entities, key = lambda x: x.rOrder.value)

    for entity in entitiesInRenderOrder:
        drawEntity(con, entity, fovMap)

    # tcod.console_set_default_foreground(con, tcod.white)
    # tcod.console_print_ex(con, 1, screenHeight - 2, tcod.BKGND_NONE, tcod.LEFT,
    #                       'HP: {0:02}/{1:02}'.format(player.fighter.hp, player.fighter.maxHP))

    tcod.console_blit(con, 0, 0, screenWidth, screenHeight, 0, 0, 0)

    tcod.console_set_default_background(panel, tcod.black)
    tcod.console_clear(panel)

    y = 1
    for message in messageLog.messages:
        tcod.console_set_default_foreground(panel, message.color)
        tcod.console_print_ex(panel, messageLog.x, y, tcod.BKGND_NONE, tcod.LEFT, message.text)
        y += 1

    renderBar(panel, 1, 1, barWidth, 'HP', player.fighter.hp, player.fighter.maxHP,
              tcod.light_red, tcod.darker_red)

    tcod.console_set_default_foreground(panel, tcod.light_grey)
    tcod.console_print_ex(panel, 1, 0, tcod.BKGND_NONE, tcod.LEFT,
                          getNamesUnderMouse(mouse, entities, fovMap))

    tcod.console_blit(panel, 0, 0, screenWidth, panelHeight, 0, 0, panelY)

    if gameState == gameStates.SHOW_INVENTORY:
        inventoryMenu(con, 'Press the key next to an item to use it, or Esc to cancel\n',
                      player.inventory, 50, screenWidth, screenHeight)
        

#----------------------------------------------------------------------------------

def drawEntity(con, entity, fovMap):
    if tcod.map_is_in_fov(fovMap, entity.x, entity.y):
        tcod.console_set_default_foreground(con, entity.color)
        tcod.console_put_char(con, entity.x, entity.y, entity.char, tcod.BKGND_NONE)

#----------------------------------------------------------------------------------

def clearEntity(con, entity):
    tcod.console_put_char(con, entity.x, entity.y, ' ', tcod.BKGND_NONE)

#----------------------------------------------------------------------------------

def clearAll(con, entities):
    for entity in entities:
        clearEntity(con, entity)