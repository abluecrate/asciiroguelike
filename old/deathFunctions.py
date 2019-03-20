import tcod
from renderFunctions import renderOrder
from gameStates import gameStates
from gameMessages import Message

def killPlayer(player):
    player.char = '%'
    player.color = tcod.dark_red

    # return 'You died!', gameStates.PLAYER_DEAD
    return Message('You died!', tcod.red), gameStates.PLAYER_DEAD

def killMonster(monster):
    # deathMessage = '{0} is dead!'.format(monster.name.capitalize())
    deathMessage = Message('{} is dead!'.format(monster.name.capitalize()), tcod.orange)

    monster.char = '%'
    monster.color = tcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'Remains of ' + monster.name
    monster.rOrder = renderOrder.corpse

    return deathMessage