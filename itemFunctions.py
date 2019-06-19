import tcod
from gameMessages import Message

def heal(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')

    results = []

    if entity.fighter.hp == entity.fighter.maxHP:
        results.append({'consumed': False, 'message': Message('You are already at full health.')})
    else:
        entity.fighter.heal(amount)
        results.append({'consumed': True, 'message': Message('You have healed.')})

    return results