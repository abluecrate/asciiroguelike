print(__name__)

import tcod

from config import Config
from gameStates import gameStates

from inputHandler import handleKeys
from renderFunctions import renderAll, clearAll, renderOrder
from gameMessages import Message, MessageLog

from fovFunctions import initializeFOV, recomputeFOV
from mapObjects.gameMap import gameMap

from components.fighter import Fighter
from deathFunctions import killMonster, killPlayer
from entity import Entity, getBlockingEntities

#######################################################################################

def main():

    #----------------------------------------------------------------------------------
    fighterComponent = Fighter(hp = 30, defense = 2, power = 5)
    player = Entity(0, 0, '@', tcod.white, 'Player', blocks = True, rOrder = renderOrder.actor, fighter = fighterComponent)
    entities = [player]
    #----------------------------------------------------------------------------------

    tcod.console_set_custom_font(Config.FONT, tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
    tcod.console_init_root(Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT, Config.TITLE, False)
    
    con = tcod.console_new(Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)
    panel = tcod.console_new(Config.SCREEN_WIDTH, Config.PANEL_HEIGHT)

    map = gameMap(Config.MAP_WIDTH, Config.MAP_HEIGHT)
    map.makeMap(Config.MAX_ROOMS, Config.ROOM_MIN_SIZE, Config.ROOM_MAX_SIZE, Config.MAP_WIDTH, Config.MAP_HEIGHT, 
                player, entities, Config.MAX_MONSTERS_PER_ROOM)
    fovRecompute = True
    fovMap = initializeFOV(map)

    messageLog = MessageLog(Config.MESSAGE_X, Config.MESSAGE_WIDTH, Config.MESSAGE_HEIGHT)

    key = tcod.Key()
    mouse = tcod.Mouse()

    gameState = gameStates.PLAYERS_TURN

    #----------------------------------------------------------------------------------

    while not tcod.console_is_window_closed():

        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, key, mouse)

        if fovRecompute:
            recomputeFOV(fovMap, player.x, player.y, Config.FOV_RADIUS, Config.FOV_LIGHT_WALLS, Config.FOV_ALGORITHM)

        renderAll(con, panel, entities, player, map, fovMap, fovRecompute, 
                  messageLog, Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT, 
                  Config.BAR_WIDTH, Config.PANEL_HEIGHT, Config.PANEL_Y, 
                  mouse, Config.COLORS)

        fovRecompute = False

        tcod.console_flush()

        clearAll(con, entities)

        #----------------------------------------------------------------------------------

        action = handleKeys(key)

        move = action.get('move')
        EXIT = action.get('EXIT')
        FULLSCREEN = action.get('FULLSCREEN')

        playerTurnResults = []

        if move and gameState == gameStates.PLAYERS_TURN:
            dx,dy = move
            destinationX = player.x + dx
            destinationY = player.y + dy 

            if not map.isBlocked(destinationX, destinationY):
                target = getBlockingEntities(entities, destinationX, destinationY)
                if target:
                    attackResults = player.fighter.attack(target)
                    playerTurnResults.extend(attackResults)
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

        for playerTurnResult in playerTurnResults:
            message = playerTurnResult.get('message')
            deadEntity = playerTurnResult.get('dead')

            if message:
                messageLog.addMessage(message)
            if deadEntity:
                if deadEntity == player:
                    message, gameState = killPlayer(deadEntity)
                else:
                    message = killMonster(deadEntity)
                messageLog.addMessage(message)

        #----------------------------------------------------------------------------------

        if gameState == gameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemyTurnResults = entity.ai.takeTurn(player, fovMap, map, entities)

                    for enemyTurnResult in enemyTurnResults:
                        message = enemyTurnResult.get('message')
                        deadEntity = enemyTurnResult.get('dead')

                        if message:
                            messageLog.addMessage(message)
                        if deadEntity:
                            if deadEntity == player:
                                message, gameState = killPlayer(deadEntity)
                            else:
                                message = killMonster(deadEntity)
                            messageLog.addMessage(message)

                            if gameState == gameStates.PLAYER_DEAD:
                                break

                    if gameState == gameStates.PLAYER_DEAD:
                        break
            else:
                gameState = gameStates.PLAYERS_TURN

        #----------------------------------------------------------------------------------

if __name__ == '__main__':
    main()