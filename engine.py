print(__name__)

import tcod
from config import Config
from inputHandler import handleKeys
from renderFunctions import renderAll, clearAll
from fovFunctions import initializeFOV, recomputeFOV

from mapObjects.gameMap import gameMap

from entity import Entity

def main():

    player = Entity(0, 0, '@', tcod.white)
    entities = [player]

    tcod.console_set_custom_font(Config.FONT, tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
    tcod.console_init_root(Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT, Config.TITLE, False)
    
    con = tcod.console_new(Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)

    map = gameMap(Config.MAP_WIDTH, Config.MAP_HEIGHT)
    map.makeMap(Config.MAX_ROOMS, Config.ROOM_MIN_SIZE, Config.ROOM_MAX_SIZE, Config.MAP_WIDTH, Config.MAP_HEIGHT, 
                player, entities, Config.MAX_MONSTERS_PER_ROOM)
    fovRecompute = True
    fovMap = initializeFOV(map)

    key = tcod.Key()
    mouse = tcod.Mouse()

    while not tcod.console_is_window_closed():

        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)

        if fovRecompute:
            recomputeFOV(fovMap, player.x, player.y, Config.FOV_RADIUS, Config.FOV_LIGHT_WALLS, Config.FOV_ALGORITHM)

        renderAll(con, entities, map, fovMap, fovRecompute, Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)

        fovRecompute = False

        tcod.console_flush()

        clearAll(con, entities)

        action = handleKeys(key)

        move = action.get('move')
        EXIT = action.get('EXIT')
        FULLSCREEN = action.get('FULLSCREEN')

        if move:
            (dx,dy) = move
            if not map.isBlocked(player.x + dx, player.y + dy):
                player.move(dx,dy)
                fovRecompute = True

        if EXIT:
            return True

        if FULLSCREEN:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

if __name__ == '__main__':
    main()