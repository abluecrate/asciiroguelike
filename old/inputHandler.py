import tcod
from gameStates import gameStates

def handleKeys(key, gameState):
    if gameState == gameStates.PLAYERS_TURN:
        return handlePlayerTurnKeys(key)
    elif gameState == gameStates.PLAYER_DEAD:
        return handlePlayerDeadKeys(key)
    elif gameState == gameStates.SHOW_INVENTORY:
        return handleInventoryKeys(key)
    return {}

def handlePlayerTurnKeys(key):
    keyChar = chr(key.c)

    if key.vk == tcod.KEY_UP or keyChar == 'w':
        return {'move' : (0,-1)}
    elif key.vk == tcod.KEY_DOWN or keyChar == 's':
        return {'move' : (0,1)}
    elif key.vk == tcod.KEY_LEFT or keyChar == 'a':
        return {'move' : (-1,0)}
    elif key.vk == tcod.KEY_RIGHT or keyChar == 'd':
        return {'move' : (1,0)}
    elif keyChar == 'q':
        return {'move': (-1, -1)}
    elif keyChar == 'e':
        return {'move': (1, -1)}
    elif keyChar == 'z':
        return {'move': (-1, 1)}
    elif keyChar == 'x':
        return {'move': (1, 1)}

    if keyChar == 'g':
        return{'pickup': True}
    elif keyChar == 'i':
        return {'showInventory': True}

    if key.vk == tcod.KEY_ENTER and key.lalt:
        return {'FULLSCREEN' : True}
    elif key.vk == tcod.KEY_ESCAPE:
        return {'EXIT' : True}
    
    return {}

def handlePlayerDeadKeys(key):
    keyChar = chr(key.c)

    if keyChar == 'i':
        return {'showInventory': True}
    if key.vk == tcod.KEY_ENTER and key.lalt:
        return {'FULLSCREEN': True}
    elif key.vk == tcod.KEY_ESCAPE:
        return {'EXIT': True}

    return {}

def handleInventoryKeys(key):
    index = key.c - ord('a')

    if index >= 0:
        return {'inventoryIndex': index}
    
    if key.vk == tcod.KEY_ENTER and key.lalt:
        return {'FULLSCREEN' : True}
    elif key.vk == tcod.KEY_ESCAPE:
        return {'EXIT' : True}
    
    return {}