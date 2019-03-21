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

        # Damage Calculation
        damage = self.power - target.fighter.defense
        
        if damage > 0:
            # Take Damage
            # target.fighter.takeDamage(damage)
            # print('{} attacks {} for {} damage'.format(self.owner.name.capitalize(), target.name, str(damage)))
            results.append({
                            'message': '{} attacks {} for {} damage'.format(self.owner.name.capitalize(), target.name, str(damage))
                           })
            results.extend(target.fighter.takeDamage(damage))
        else:
            # print('{} attacks {} for no damage'.format(self.owner.name.capitalize(), target.name))
            results.append({
                            'message': '{} attacks {} for no damage'.format(self.owner.name.capitalize(), target.name)
                           })
            results.extend(target.fighter.takeDamage(damage))
        
        return results