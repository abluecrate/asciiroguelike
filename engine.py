# Python Libraries
import tcod
# Game Functions
from gameStates import GameStates
from gameMessages import Message, MessageLog
from renderFunctions import renderAll, clearAll, RenderOrder
from fovFunctions import initializeFOV, recomputeFOV
from inputHandler import handleKeys
# Game Objects
from entity import Entity, getBlockingEntities
from deathFunctions import killMonster, killPlayer
from mapObjects.gameMap import GameMap
from components.fighter import Fighter
from components.inventory import Inventory

#-----------------------------------------------------------------------------------------------

# MAIN LOOP
def main():

    #-----------------------------------------------------------------------------------------------
    ################################################################################################
    #-----------------------------------------------------------------------------------------------

    # CONFIG
    SCREENWIDTH = 80
    SCREENHEIGHT = 50
    MAPWIDTH = 80
    MAPHEIGHT = 43

    BARWIDTH = 20
    PANELHEIGHT = 7
    PANELY = SCREENHEIGHT - PANELHEIGHT

    MESSAGEX = BARWIDTH + 2
    MESSAGEWIDTH = SCREENWIDTH - BARWIDTH - 2
    MESSAGEHEIGHT = PANELHEIGHT - 2

    ROOMMAX = 10
    ROOMMIN = 6
    NUMROOMSMAX = 30

    FOVALGORITHM = 0
    FOVLIGHTWALLS = True
    FOVRADIUS = 15

    MAXMONSTERSPERROOM = 3
    MAXITEMSPERROOM = 2

    COLORS = {
                'darkWall': tcod.Color(0,0,100),
                'darkGround': tcod.Color(50,50,150),
                'lightWall': tcod.Color(130,110,50),
                'lightGround': tcod.Color(200,180,50)
    }

    #-----------------------------------------------------------------------------------------------
    ################################################################################################
    #-----------------------------------------------------------------------------------------------

    # INITIALIZATION

    fighterComponent = Fighter(hp=30, defense=2, power=5)
    inventoryComponent = Inventory(26)
    player = Entity(0, 0, '@', tcod.white, 'Player', blocks=True, 
                    renderOrder=RenderOrder.ACTOR, fighter=fighterComponent,
                    inventory=inventoryComponent)   # Player Entity Object
    entities = [player] # Entity List

    #-----------------------------------------------------------------------------------------------

    # Initialize Font
    tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
    # Initialize Console Window
    tcod.console_init_root(SCREENWIDTH, SCREENHEIGHT, title = 'ASCII Roguelike', fullscreen = False)

    baseConsole = tcod.console_new(SCREENWIDTH, SCREENHEIGHT)   # Base Console
    panel = tcod.console_new(SCREENWIDTH, PANELHEIGHT)

    #-----------------------------------------------------------------------------------------------
    
    MAP = GameMap(MAPWIDTH, MAPHEIGHT) # CREATE MAP
    MAP.makeMap(NUMROOMSMAX, ROOMMIN, ROOMMAX, MAPWIDTH, MAPHEIGHT, player, entities, 
                MAXMONSTERSPERROOM, MAXITEMSPERROOM)

    fovRecompute = True         # FOV Recomputing Boolean
    fovMap = initializeFOV(MAP) # Initialize FOV Map

    #-----------------------------------------------------------------------------------------------

    messageLog = MessageLog(MESSAGEX, MESSAGEWIDTH, MESSAGEHEIGHT)

    key = tcod.Key()        # Store Keyboard Input
    mouse = tcod.Mouse()    # Store Mouse Input

    gameState = GameStates.PLAYERTURN   # Start On Player's Turn
    previousGameState = gameState

    #-----------------------------------------------------------------------------------------------
    ################################################################################################
    #-----------------------------------------------------------------------------------------------

    # GAME LOOP

    while not tcod.console_is_window_closed():

        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, key, mouse)  # Capture User Input

        #-----------------------------------------------------------------------------------------------

        if fovRecompute:
            # Recompute FOV Based on Player Position
            recomputeFOV(fovMap, player.x, player.y, FOVRADIUS, FOVLIGHTWALLS, FOVALGORITHM)

        # Render All Entities
        renderAll(baseConsole, panel, entities, player, MAP, fovMap, fovRecompute, messageLog,
                  SCREENWIDTH, SCREENHEIGHT, BARWIDTH, PANELHEIGHT, PANELY, mouse, COLORS, gameState)

        fovRecompute = False    # Turn Off FOV Recompute Until Player Move

        #-----------------------------------------------------------------------------------------------

        tcod.console_flush()            # Update Console to Current State
        clearAll(baseConsole, entities) # Clear Entities

        #-----------------------------------------------------------------------------------------------

        action = handleKeys(key, gameState) # Get Key Press

        # Key Press Action
        move = action.get('move')               # Movement
        pickup = action.get('pickup')           # Pickup Object
        showInventory = action.get('showInventory')
        inventoryIndex = action.get('inventoryIndex')
        exit = action.get('exit')               # Exit Boolean
        fullscreen = action.get('fullscreen')   # Fullscreen Boolean

        playerTurnResults = []  # Initialize Player's Turn Results

        # Check for movement and players turn
        if move and gameState == GameStates.PLAYERTURN:
            dx,dy = move # Movement Deltas
            # Movement Destination
            destinationX = player.x + dx
            destinationY = player.y + dy

            # If map is not blocked:
            if not MAP.isBlocked(destinationX, destinationY):
                # Check for blocking entities
                target = getBlockingEntities(entities, destinationX, destinationY)
                
                if target:
                    # player.fighter.attack(target)
                    attackResults = player.fighter.attack(target)   # Gather Attack Results
                    playerTurnResults.extend(attackResults)         # Add to Player Turn Results
                else:
                    player.move(dx,dy)  # Move Player By Delta
                    fovRecompute = True

                gameState = GameStates.ENEMYTURN    # Set To Enemy's Turn

        elif pickup and gameState == GameStates.PLAYERTURN:
            for entity in entities:
                if entity.item and entity.x == player.x and entity.y == player.y:
                    pickupResults = player.inventory.addItem(entity)
                    playerTurnResults.extend(pickupResults)
                    break
            else:
                messageLog.addMessage(Message('There is nothing to pick up.', tcod.yellow))

        if showInventory:
            previousGameState = gameState
            gameState = GameStates.INVENTORY
        
        if inventoryIndex is not None and previousGameState != GameStates.PLAYERDEAD and inventoryIndex < len(player.inventory.items):
            item = player.inventory.items[inventoryIndex]
            playerTurnResults.extend(player.inventory.use(item))

        if exit:        # Exit Window
            if gameState == GameStates.INVENTORY:
                gameState = previousGameState
            else:
                return True

        if fullscreen:  # Fullscreen
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        for playerTurnResult in playerTurnResults:
            message = playerTurnResult.get('message')
            deadEntity = playerTurnResult.get('dead')
            itemAdded = playerTurnResult.get('itemAdded')
            itemConsumed = playerTurnResult.get('consumed')

            if message:
                messageLog.addMessage(message)

            if deadEntity:
                if deadEntity == player:
                    message, gameState = killPlayer(deadEntity)
                else:
                    message = killMonster(deadEntity)
                messageLog.addMessage(message)

            if itemAdded:
                entities.remove(itemAdded)
                gameState = GameStates.ENEMYTURN

            if itemConsumed:
                gameState = GameStates.ENEMYTURN

        if gameState == GameStates.ENEMYTURN:
            for entity in entities:
                if entity.ai:
                    # entity.ai.takeTurn(player, fovMap, MAP, entities)
                    enemyTurnResults = entity.ai.takeTurn(player, fovMap, MAP, entities)

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

                        if gameState == GameStates.PLAYERDEAD:
                            break
                    
                    if gameState == GameStates.PLAYERDEAD:
                        break
            else:
                gameState = GameStates.PLAYERTURN   # Set To Player's Turn

#-----------------------------------------------------------------------------------------------
################################################################################################
#-----------------------------------------------------------------------------------------------

# EXECUTE MAIN LOOP
if __name__ == '__main__':
    main()