import tcod
from gameMessages import Message

class Fighter:
    def __init__(self, hp, defense, power):
        self.maxHP = hp
        self.hp = hp
        self.defense = defense
        self.power = power
    
    def takeDamage(self, amount):
        results = []
        self.hp -= amount
        if self.hp <= 0:
            results.append({'dead': self.owner})
        return results

    def attack(self, target):
        results = []
        damage = self.power - target.fighter.defense

        if damage > 0:
            results.append({'message': Message('{} attacks {} for {} hit points'.format(
                self.owner.name.capitalize(), target.name, str(damage)), tcod.white)})
            results.extend(target.fighter.takeDamage(damage))
        else:
            results.append({'message': Message('{0} attacks {1} but does no damage'.format(
                self.owner.name.capitalize(), target.name.capitalize()), tcod.white)})

        return results