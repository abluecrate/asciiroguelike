import libtcodpy as tcod

from gameStates import GameStates

def killPlayer(player):
    player.char = '%'
    player.color = tcod.dark_red

    return 'You died!', GameStates.PLAYERDEAD

def killMonster(monster):
    deathMessage = '{} is dead!'.format(monster.name.capitalize())

    monster.char = '%'
    monster.color = tcod.dark_red
    monster.blocks = False
    monster.figher = None
    monster.ai = None
    monster.name = 'Remains of ' + monster.name

    return deathMessage