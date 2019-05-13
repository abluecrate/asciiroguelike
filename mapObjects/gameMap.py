import tcod
from random import randint
from entity import Entity
from mapObjects.tile import Tile
from mapObjects.rectangle import Rectangle
from components.fighter import Fighter
from components.ai import BasicMonster
from components.item import Item
from renderFunctions import RenderOrder

class GameMap:
    # Game Map Class
    #-----------------------------------------------------------------------------------------------
    def __init__(self, mapWidth, mapHeight):
        self.mapWidth = mapWidth
        self.mapHeight = mapHeight
        self.tiles = self.initializeTiles() # Initialize Default Tiles
    #-----------------------------------------------------------------------------------------------
    def initializeTiles(self):
        # Create Initial Array of Non-Blocking Tiles
        return [[Tile(True) 
                    for y in range(self.mapHeight)] 
                        for x  in range(self.mapWidth)]
    #-----------------------------------------------------------------------------------------------
    def isBlocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
        return False
    #-----------------------------------------------------------------------------------------------
    ################################################################################################
    #-----------------------------------------------------------------------------------------------
    def createRoom(self, room):
        # Create Passable Rectangles
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].blockSight = False
    #-----------------------------------------------------------------------------------------------
    def createHTunnel(self, x1, x2, y):
        # Create Passable Horizontal Line (Tunnel)
        for x in range(min(x1,x2), max(x1,x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].blockSight = False
    #-----------------------------------------------------------------------------------------------
    def createVTunnel(self, y1, y2, x):
        # Create Passable Vertical Line (Tunnel)
        for y in range(min(y1,y2), max(y1,y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].blockSight = False
    #-----------------------------------------------------------------------------------------------
    def placeEntities(self, room, entities, maxMonstersPerRoom, maxItemsPerRoom):
        # Random Number of Monsters
        numMonsters = randint(0, maxMonstersPerRoom)
        numItems = randint(0, maxItemsPerRoom)

        for _ in range(numMonsters):
            # Random Position
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)
            # Check For Existing Entities
            if not any([entity for entity in entities
                        if entity.x == x and entity.y == y]):

                aiComponent = BasicMonster()    # AI Component

                if randint(0,100) < 80:
                    fighterComponentOrc = Fighter(hp = 10, defense = 0, power = 3)  # Orc Fighter Component
                    # Orc Entity Class
                    monster = Entity(x, y, 'O', tcod.desaturated_green, 'Orc', 
                                     blocks = True, renderOrder = RenderOrder.ACTOR,
                                     fighter = fighterComponentOrc, ai = aiComponent)
                else:
                    fighterComponentTroll = Fighter(hp = 16, defense = 1, power = 4) # Troll Fighter Component
                    # Troll Entity Class
                    monster = Entity(x, y, 'T', tcod.darker_green, 'Troll', 
                                     blocks = True, renderOrder = RenderOrder.ACTOR,
                                     fighter = fighterComponentTroll, ai = aiComponent)
                entities.append(monster)

        for _ in range(numItems):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                itemComponent = Item()
                item = Entity(x, y, '!', tcod.violet, 'Healing Potion', renderOrder=RenderOrder.ITEM,
                              item=itemComponent)
                entities.append(item)

    #-----------------------------------------------------------------------------------------------
    ################################################################################################
    #-----------------------------------------------------------------------------------------------
    def makeMap(self, maxRooms, roomMin, roomMax, mapWidth, mapHeight, player, entities, 
                maxMonstersPerRoom, maxItemsPerRoom):
        rooms = []
        numRooms = 0

        for _ in range(maxRooms):
            # Random Length and Width with Room Size Boundaries
            w = randint(roomMin, roomMax)
            h = randint(roomMin, roomMax)
            # Random Position with Map Boundaries
            x = randint(0, mapWidth - w - 1)
            y = randint(0, mapHeight - h - 1)

            newRoom = Rectangle(x,y,w,h)    # Initialize New Room Rectangle

            for otherRoom in rooms:
                # Check for room intersections
                if newRoom.checkIntersect(otherRoom):
                    break
            else:
                self.createRoom(newRoom)        # Create New Room
                (newX, newY) = newRoom.center() # New Room Center Coordinates

                if numRooms == 0:
                    # Set Player Starting Position to First Room
                    player.x = newX
                    player.y = newY
                else:
                    (prevX, prevY) = rooms[numRooms - 1].center()   # Center Coordinates of Previous Room
                    # Randomly Choose Side of Previous Room to extend Tunnel To New Room
                    if randint(0,1) == 1:
                        self.createHTunnel(prevX, newX, prevY)   # Move Horizontal
                        self.createVTunnel(prevY, newY, newX)   # Move Vertical
                    else:
                        self.createVTunnel(prevY, newY, prevX)   # Move Vertical
                        self.createHTunnel(prevX, newX, newY)   # Move Horizontal

                self.placeEntities(newRoom, entities, maxMonstersPerRoom, maxItemsPerRoom)

                rooms.append(newRoom)   # Append New Room To List
                numRooms += 1           # Increase Number of Rooms