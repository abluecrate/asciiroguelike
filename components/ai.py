import tcod

class basicMonster:
    def takeTurn(self, target, fovMap, gameMap, entities):
        monster = self.owner
        if tcod.map_is_in_fov(fovMap, monster.x, monster.y):
            if monster.distanceTo(target) >= 2:
                monster.moveAStar(target, entities, gameMap)
            elif target.fighter.hp > 0:
                print('The {0} insults you! Your ego is damaged!'.format(monster.name))

        