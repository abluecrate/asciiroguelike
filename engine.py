print(__name__)

import tcod

from config import Config
from gameStates import gameStates

from inputHandler import handleKeys
from renderFunctions import renderAll, clearAll

from fovFunctions import initializeFOV, recomputeFOV
from mapObjects.gameMap import gameMap

from components.fighter import Fighter
from entity import Entity, getBlockingEntities

#######################################################################################

def main():

    #----------------------------------------------------------------------------------
    fighterComponent = Fighter(hp = 30, defense = 2, power = 5)
    player = Entity(0, 0, '@', tcod.white, 'Player', blocks = True, fighter = fighterComponent)
    entities = [player]
    #----------------------------------------------------------------------------------

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

    gameState = gameStates.PLAYERS_TURN

    #----------------------------------------------------------------------------------

    while not tcod.console_is_window_closed():

        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)

        if fovRecompute:
            recomputeFOV(fovMap, player.x, player.y, Config.FOV_RADIUS, Config.FOV_LIGHT_WALLS, Config.FOV_ALGORITHM)

        renderAll(con, entities, map, fovMap, fovRecompute, Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)

        fovRecompute = False

        tcod.console_flush()

        clearAll(con, entities)

        #----------------------------------------------------------------------------------

        action = handleKeys(key)

        move = action.get('move')
        EXIT = action.get('EXIT')
        FULLSCREEN = action.get('FULLSCREEN')

        if move and gameStates.PLAYERS_TURN:
            dx,dy = move
            destinationX = player.x + dx
            destinationY = player.y + dy 

            if not map.isBlocked(destinationX, destinationY):
                target = getBlockingEntities(entities, destinationX, destinationY)
                if target:
                    print('You kick the {}'.format(target.name))
                else:
                    player.move(dx,dy)
                    fovRecompute = True
                gameState = gameStates.ENEMY_TURN

        #----------------------------------------------------------------------------------

        if EXIT:
            return True

        if FULLSCREEN:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        #----------------------------------------------------------------------------------

        if gameState == gameStates.ENEMY_TURN:
            print('--------------------------------------------------------')
            for entity in entities:
                if entity.ai:
                    entity.ai.takeTurn(player, fovMap, map, entities)
            gameState = gameStates.PLAYERS_TURN      
            print('--------------------------------------------------------')

        #----------------------------------------------------------------------------------

if __name__ == '__main__':
    main()