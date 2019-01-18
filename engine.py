print(__name__)

import tcod
from config import Config
from inputHandler import handleKeys
from renderFunctions import renderAll, clearAll

from mapObjects.gameMap import gameMap

from entity import Entity

def main():

    player = Entity(int(Config.SCREEN_WIDTH // 2), int(Config.SCREEN_HEIGHT // 2), '@', tcod.white)
    entities = [player]

    tcod.console_set_custom_font(Config.FONT, tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
    tcod.console_init_root(Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT, Config.TITLE, False)
    
    con = tcod.console_new(Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)

    map = gameMap(Config.MAP_WIDTH, Config.MAP_HEIGHT)

    key = tcod.Key()
    mouse = tcod.Mouse()

    while not tcod.console_is_window_closed():

        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)

        renderAll(con, entities, map, Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)

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

        if EXIT:
            return True

        if FULLSCREEN:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

if __name__ == '__main__':
    main()