from enum import Enum

class GameStates(Enum):
    PLAYERTURN = 1
    ENEMYTURN = 2
    PLAYERDEAD = 3