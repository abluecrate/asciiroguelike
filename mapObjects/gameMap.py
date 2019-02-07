import tcod
from random import randint
from mapObjects.tile import Tile
from mapObjects.rectangle import Rect
from entity import Entity

class gameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.intitializeTiles()

    def intitializeTiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]
        return tiles

    def isBlocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
        return False

    def createRoom(self, room):
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].blockSight = False
    
    def createHTunnel(self, x1, x2, y):
        for x in range(min(x1,x2), max(x1,x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].blockSight = False

    def createVTunnel(self, y1, y2, x):
        for y in range(min(y1,y2), max(y1,y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].blockSight = False

    def placeEntities(self, room, entities, maxMonstersPerRoom):
        nMonsters = randint(0, maxMonstersPerRoom)
        
        for _ in range(nMonsters):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                if randint(0,100) < 80:
                    monster = Entity(x, y, 'O', tcod.Color(75,115,85))
                else:
                    monster = Entity(x, y, 'T', tcod.Color(10,70,30))
                entities.append(monster)

    def makeMap(self, maxRooms, roomMinSize, roomMaxSize, mapWidth, mapHeight, player, 
                entities, maxMonstersPerRoom):

        rooms = []
        nRooms = 0

        for _ in range(maxRooms):
            w = randint(roomMinSize, roomMaxSize)
            h = randint(roomMinSize, roomMaxSize)
            x = randint(0, mapWidth - w - 1)
            y = randint(0, mapHeight - h - 1)

            newRoom = Rect(x,y,w,h)

            failed = False
            for otherRoom in rooms:
                if newRoom.checkIntersect(otherRoom):
                    failed = True
                    break

            if not failed:
                self.createRoom(newRoom)
                newX, newY = newRoom.center()

                if nRooms == 0:
                    player.x = newX
                    player.y = newY
                else:
                    prevX, prevY = rooms[nRooms - 1].center()
                    if randint(0,1) == 1:
                        self.createHTunnel(prevX,newX,prevY)
                        self.createVTunnel(prevY,newY,newX)
                    else:
                        self.createVTunnel(prevY,newY,prevX)
                        self.createHTunnel(prevX,newX,newY)

            self.placeEntities(newRoom, entities, maxMonstersPerRoom)

            rooms.append(newRoom)
            nRooms += 1
                            