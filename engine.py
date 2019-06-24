import tcod
from renderFunctions import clearAll, renderAll
from inputHandler import handleKeys

from gameMap import GameMap
from entity import Entity


##############################################################################


def main():

    # CONFIG

    # Screen Size
    SCREENWIDTH = 80
    SCREENHEIGHT = 50

    # Map Size
    MAPWIDTH = 80
    MAPHEIGHT = 45

    # Map Configuration
    MAXROOMSIZE = 10
    MINROOMSIZE = 6
    MAXROOMS = 30

    COLORS = {
              'darkWall': tcod.Color(0, 0, 100),
              'darkGround': tcod.Color(50, 50, 150)
             }

    player = Entity(int(SCREENWIDTH / 2), int(SCREENHEIGHT / 2), '@',
                    tcod.white)

    # Entity List
    entities = [player]

    # ------------------------------------------------------------------------

    # Set Font
    tcod.console_set_custom_font('arial10x10.png',
                                 tcod.FONT_TYPE_GREYSCALE | 
                                 tcod.FONT_LAYOUT_TCOD)

    # Create Root Screen
    tcod.console_init_root(SCREENWIDTH, SCREENHEIGHT,
                           'ASCII Roguelike', False)

    # Initializing Root Console
    root = tcod.console_new(SCREENWIDTH, SCREENHEIGHT)

    gameMap = GameMap(MAPWIDTH, MAPHEIGHT)
    gameMap.makeMap(MAXROOMS, MINROOMSIZE, MAXROOMSIZE, MAPWIDTH, MAPHEIGHT, player)

    key = tcod.Key()        # Keyboard Input
    mouse = tcod.Mouse()    # Mouse Input

    ##########################################################################

    # GAME LOOP

    while not tcod.console_is_window_closed():
        # Capture User Input
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)

        # --------------------------------------------------------------------
        # RENDER ALL

        renderAll(root, entities, gameMap, SCREENWIDTH, SCREENHEIGHT, COLORS)

        # Present to Screen
        tcod.console_flush()

        # Erase Past Character When Moved
        clearAll(root, entities)

        # --------------------------------------------------------------------

        # Send Keypress to Input Handler
        action = handleKeys(key)

        # Parse Actions
        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            # Move If Not Blocked
            if not gameMap.isBlocked(player.x + dx, player.y + dy):
                player.move(dx, dy)

        # if key.vk == tcod.KEY_ESCAPE:
        #     return True

        if exit:
            return True

        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

##############################################################################


if __name__ == '__main__':
    main()
