import tcod

from gameStates import GameStates
from gameMessages import Message
from renderFunctions import RenderOrder

def killPlayer(player):
    player.char = '%'
    player.color = tcod.dark_red

    # return 'You died!', GameStates.PLAYERDEAD
    return Message('You died!', tcod.red), GameStates.PLAYERDEAD

def killMonster(monster):
    # deathMessage = '{} is dead!'.format(monster.name.capitalize())
    deathMessage = Message('{} is dead!'.format(monster.name.capitalize()), tcod.orange)

    monster.char = '%'
    monster.color = tcod.dark_red
    monster.blocks = False
    monster.figher = None
    monster.ai = None
    monster.name = 'Remains of ' + monster.name
    monster.renderOrder = RenderOrder.CORPSE

    return deathMessage