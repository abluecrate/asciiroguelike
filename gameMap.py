from random import randint


##############################################################################


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initializeTiles()

    def initializeTiles(self):
        # Initialize All Blocked Tiles
        # --> "Dig Out" Rooms
        tiles = [[Tile(True)
                 for y in range(self.height)]
                 for x in range(self.width)]

        return tiles

    def isBlocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False

    # ------------------------------------------------------------------------

    # Map Tools

    def createRoom(self, room):
        # Create Passable Rectangle
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].blockSight = False

    def createHorizontalTunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].blockSight = False

    def createVerticalTunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].blockSight = False

    # ------------------------------------------------------------------------

    # MAP GENERATION

    def makeMap(self, maxRooms, minRoomSize, maxRoomSize, mapWidth, mapHeight, player):
        rooms = []
        numRooms = 0

        for room in range(maxRooms):
            # Random Size
            w = randint(minRoomSize, maxRoomSize)
            h = randint(minRoomSize, maxRoomSize)
            # Random Position
            x = randint(0, mapWidth - w - 1)
            y = randint(0, mapHeight - h - 1)

            # Establish New Room
            newRoom = Rectangle(x, y, w, h)

            # Check For Interections with Other Rooms
            for otherRoom in rooms:
                if newRoom.intersect(otherRoom):
                    break
            else:
                # Create Room and Get Center Coordinates
                self.createRoom(newRoom)
                (newX, newY) = newRoom.center()

                if numRooms == 0:
                    # Set Player Start to First Room Created
                    player.x = newX
                    player.y = newY
                else:
                    # Center Coordinates of Previous Room
                    (prevX, prevY) = rooms[numRooms - 1].center()

                    if randint(0, 1) == 1:
                        self.createHorizontalTunnel(prevX, newX, prevY)
                        self.createVerticalTunnel(prevY, newY, prevX)
                    else:
                        self.createVerticalTunnel(prevY, newY, prevX)
                        self.createHorizontalTunnel(prevX, newX, prevY)

            # Add New Room To List
            rooms.append(newRoom)
            # Increase Room Count
            numRooms += 1

##############################################################################


class Tile:
    def __init__(self, blocked, blockSight=None):
        self.blocked = blocked

        if blockSight is None:
            blockSight = blocked

        self.blockSight = blockSight


# ----------------------------------------------------------------------------


class Rectangle:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        centerX = int((self.x1 + self.x2) / 2)
        centerY = int((self.y1 + self.y2) / 2)
        return (centerX, centerY)

    def intersect(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)
