print(__name__)

import tcod
from config import Config
from inputHandler import handleKeys

def main():

    playerX = int(Config.SCREEN_WIDTH // 2)
    playerY = int(Config.SCREEN_HEIGHT // 2)

    tcod.console_set_custom_font(Config.FONT, tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
    tcod.console_init_root(Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT, Config.TITLE, False)
    
    con = tcod.console_new(Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)

    key = tcod.Key()
    mouse = tcod.Mouse()

    while not tcod.console_is_window_closed():

        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)

        tcod.console_set_default_foreground(con, tcod.white)
        tcod.console_put_char(con, playerX, playerY, '@', tcod.BKGND_NONE)
        tcod.console_blit(con, 0, 0, Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT, 0, 0, 0)
        tcod.console_flush()
        tcod.console_put_char(con, playerX, playerY, ' ', tcod.BKGND_NONE)

        action = handleKeys(key)

        move = action.get('move')
        EXIT = action.get('EXIT')
        FULLSCREEN = action.get('FULLSCREEN')

        if move:
            (dx,dy) = move
            playerX += dx
            playerY += dy

        if EXIT:
            return True

        if FULLSCREEN:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

if __name__ == '__main__':
    main()