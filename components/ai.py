import libtcodpy as tcod

class BasicMonster:
    def takeTurn(self, target, fovMap, gameMap, entities):
        results = []

        monster = self.owner
        # Check if monster can see you
        if tcod.map_is_in_fov(fovMap, monster.x, monster.y):
            if monster.distanceTo(target) >= 2: # Check distance to target
                # Move Towards Target
                monster.moveAStar(target, entities, gameMap)
            elif target.fighter.hp > 0:
                # Attack Target
                # monster.fighter.attack(target)
                attackResults = monster.fighter.attack(target)
                results.extend(attackResults)
        
        return results