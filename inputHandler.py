import tcod

def handleKeys(key):

    if key.vk == tcod.KEY_UP:
        return {'move' : (0,-1)}
    elif key.vk == tcod.KEY_DOWN:
        return {'move' : (0,1)}
    elif key.vk == tcod.KEY_LEFT:
        return {'move' : (-1,0)}
    elif key.vk == tcod.KEY_RIGHT:
        return {'move' : (1,0)}

    if key.vk == tcod.KEY_ENTER and key.lalt:
        return {'FULLSCREEN' : True}
    elif key.vk == tcod.KEY_ESCAPE:
        return {'EXIT' : True}
    
    return {}