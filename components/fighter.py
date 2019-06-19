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
        
    def heal(self, amount):
        self.hp += amount
        if self.hp > self.maxHP:
            self.hp = self.maxHP

    def attack(self, target):
        results = []

        # Damage Calculation
        damage = self.power - target.fighter.defense
        
        if damage > 0:
            results.append({'message': Message('{} attacks {} for {} damage.'.format(
                            self.owner.name.capitalize(), target.name, str(damage)), tcod.white)})
            results.extend(target.fighter.takeDamage(damage))
        else:
            results.append({'message': Message('{} attacks {} but does no damage.'.format(
                            self.owner.name.capitalize(), target.name), tcod.white)})
            results.extend(target.fighter.takeDamage(damage))
        
        return results
