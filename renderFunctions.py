import tcod
from enum import Enum
#-----------------------------------------------------------------------------------------------
# Entity Render Order
class RenderOrder(Enum):
    CORPSE = 1
    ITEM = 2
    ACTOR = 3
#-----------------------------------------------------------------------------------------------
# Mouse Hover
def getNamesUnderMouse(mouse, entities, fovMap):
    (x, y) = (mouse.cx, mouse.cy)
    names = [entity.name for entity in entities
             if entity.x == x and entity.y == y and tcod.map_is_in_fov(fovMap, entity.x, entity.y)]
    names = ', '.join(names)
    return names
#-----------------------------------------------------------------------------------------------
# Draw Panel
def renderPanel(panel, x, y, totalWidth, name, value, maximum, barColor, backColor):
    barWidth = int(float(value) / maximum * totalWidth)
    tcod.console_set_default_background(panel, backColor)
    tcod.console_rect(panel, x, y, totalWidth, 1, False, tcod.BKGND_SCREEN)
    tcod.console_set_default_background(panel, backColor)
    if barWidth > 0:
        tcod.console_rect(panel, x, y, barWidth, 1, False, tcod.BKGND_SCREEN)
    tcod.console_set_default_foreground(panel, tcod.white)
    tcod.console_print_ex(panel, int(x + totalWidth / 2), y, tcod.BKGND_NONE, tcod.CENTER,
                          '{}: {}/{}'.format(name, value, maximum))
#-----------------------------------------------------------------------------------------------
# Draw Entities and Map
def renderAll(console, panel, entities, player, map, fovMap, fovRecompute, messageLog,
              screenWidth, screenHeight, barWidth, panelHeight, panelY, mouse, colors):
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

    # Sort Entities in Render Order
    entitiesRenderSorted = sorted(entities, key = lambda x: x.renderOrder.value)
    # Draw all entities in list
    for entity in entitiesRenderSorted:
        drawEntity(console, entity, fovMap)

    # Blit Changes
    tcod.console_blit(console, 0,0, screenWidth, screenHeight, 0,0,0)

    tcod.console_set_default_background(panel, tcod.black)
    tcod.console_clear(panel)

    y = 1
    for message in messageLog.messages:
        tcod.console_set_default_foreground(panel, message.color)
        tcod.console_print_ex(panel, messageLog.x, y, tcod.BKGND_NONE, tcod.LEFT, message.text)
        y += 1

    renderPanel(panel, 1, 1, barWidth, 'HP', player.fighter.hp, player.fighter.maxHP,
                tcod.light_red, tcod.darker_red)

    tcod.console_set_default_foreground(panel, tcod.light_grey)
    tcod.console_print_ex(panel, 1, 0, tcod.BKGND_NONE, tcod.LEFT,
                          getNamesUnderMouse(mouse, entities, fovMap))

    tcod.console_blit(panel, 0, 0, screenWidth, panelHeight, 0, 0, panelY)

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