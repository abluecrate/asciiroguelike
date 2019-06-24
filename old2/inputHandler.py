import tcod
from gameStates import GameStates

#-----------------------------------------------------------------------------------------------
def handleKeys(key, gameState):
    if gameState == GameStates.PLAYERTURN:
        return handlePlayerTurnKeys(key)
    elif gameState == GameStates.PLAYERDEAD:
        return handlePlayerDeadKeys(key)
    elif gameState == GameStates.INVENTORY:
        return handleInventoryKeys(key)
    return {}

def handlePlayerTurnKeys(key):
    keyChar = chr(key.c)

    # Movement Keys - Store Vector Movement
    if key.vk == tcod.KEY_UP:
        return {'move': (0,-1)}
    elif key.vk == tcod.KEY_DOWN:
        return {'move': (0,1)}
    elif key.vk == tcod.KEY_LEFT:
        return {'move': (-1,0)}
    elif key.vk == tcod.KEY_RIGHT:
        return {'move': (1,0)}

    if keyChar == 'g':
        return {'pickup': True}
    
    elif keyChar == 'i':
        return {'showInventory': True}

    if key.vk == tcod.KEY_ENTER and key.lalt:
        # Alt + Enter: Toggle Fullscreen
        return {'fullscreen': True}
    elif key.vk == tcod.KEY_ESCAPE:
        # Exit Game
        return {'exit': True}

    # No Key Press
    return {}

def handleInventoryKeys(key):
    index = key.c - ord('a')

    if index >=0:
        return {'inventoryIndex': index}

    if key.vk == tcod.KEY_ENTER and key.lalt:
       # Alt + Enter: Toggle Fullscreen
       return {'fullscreen': True}
    elif key.vk == tcod.KEY_ESCAPE:
       # Exit Menu
       return {'exit': True}

    return {}

def handlePlayerDeadKeys(key):
    keyChar = chr(key.c)

    if keyChar == 'i':
        return {'showInventory': True}

    if key.vk == tcod.KEY_ENTER and key.lalt:
        # Alt + Enter: Toggle Fullscreen
        return {'fullscreen': True}
    elif key.vk == tcod.KEY_ESCAPE:
        # Exit Game
        return {'exit': True}

    return {}
#-----------------------------------------------------------------------------------------------