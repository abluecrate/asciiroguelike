import tcod

class basicMonster:
    def takeTurn(self, target, fovMap, gameMap, entities):
        results = []
        monster = self.owner
        if tcod.map_is_in_fov(fovMap, monster.x, monster.y):
            if monster.distanceTo(target) >= 2:
                monster.moveAStar(target, entities, gameMap)
            elif target.fighter.hp > 0:
                attackResults = monster.fighter.attack(target)
                results.extend(attackResults)
        return results

        