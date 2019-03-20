# Python Libraries
import libtcodpy as tcod
# Game Functions
from renderFunctions import renderAll, clearAll
from inputHandler import handleKeys
# Game Objects
from entity import Entity
from mapObjects.gameMap import GameMap

#-----------------------------------------------------------------------------------------------

# MAIN LOOP
def main():

    # CONFIG
    SCREENWIDTH = 80
    SCREENHEIGHT = 50
    MAPWIDTH = 80
    MAPHEIGHT = 45

    COLORS = {
                'darkWall': tcod.Color(0,0,100),
                'darkGround': tcod.Color(50,50,150)
    }

    #-----------------------------------------------------------------------------------------------

    player = Entity(int(SCREENWIDTH/2), int(SCREENHEIGHT/2), '@', tcod.white)   # Player Entity Object
    
    # Entity List
    ENTITIES = [player]

    #-----------------------------------------------------------------------------------------------

    # Initialize Font
    tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
    # Initialize Console Window
    tcod.console_init_root(SCREENWIDTH, SCREENHEIGHT, title = 'ASCII Roguelike', fullscreen = False)

    baseConsole = tcod.console_new(SCREENWIDTH, SCREENHEIGHT)   # Base Console

    #-----------------------------------------------------------------------------------------------
    
    MAP = GameMap(MAPWIDTH, MAPHEIGHT) # CREATE MAP

    #-----------------------------------------------------------------------------------------------

    key = tcod.Key()        # Store Keyboard Input
    mouse = tcod.Mouse()    # Store Mouse Input

    #-----------------------------------------------------------------------------------------------

    while not tcod.console_is_window_closed():

        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)  # Capture User Input

        #-----------------------------------------------------------------------------------------------

        renderAll(baseConsole, ENTITIES, MAP, SCREENWIDTH, SCREENHEIGHT, COLORS) # Render All Entities

        #-----------------------------------------------------------------------------------------------

        tcod.console_flush()            # Update Console to Current State
        clearAll(baseConsole, ENTITIES) # Clear Entities

        #-----------------------------------------------------------------------------------------------

        action = handleKeys(key) # Get Key Press

        # Key Press Action
        move = action.get('move')               # Movement
        exit = action.get('exit')               # Exit Boolean
        fullscreen = action.get('fullscreen')   # Fullscreen Boolean

        if move:
            dx,dy = move # Movement Deltas
            # If map is not blocked:
            if not MAP.isBlocked(player.x + dx, player.y + dy):
                player.move(dx,dy)  # Move Player By Delta

        if exit:        # Exit Window
            return True
        if fullscreen:  # Fullscreen
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

#-----------------------------------------------------------------------------------------------

# EXECUTE MAIN LOOP
if __name__ == '__main__':
    main()