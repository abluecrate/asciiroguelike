import tcod


##############################################################################


def handleKeys(key):
    # Movement Keys
    if key.vk == tcod.KEY_UP:
        return {'move': (0, -1)}
    elif key.vk == tcod.KEY_DOWN:
        return {'move': (0, 1)}
    elif key.vk == tcod.KEY_LEFT:
        return {'move': (-1, 0)}
    elif key.vk == tcod.KEY_RIGHT:
        return {'move': (1, 0)}

    # Toggle Fullscreen
    if key.vk == tcod.KEY_ENTER and key.lalt:
        return {'fullscreen': True}

    # Exit Game
    elif key.vk == tcod.KEY_ESCAPE:
        return {'exit': True}

    # No Key Press
    return {}
