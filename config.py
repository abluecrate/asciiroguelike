import tcod

class Config(object):
    TITLE = 'asciiroguelike'
    FONT = 'arial10x10.png'

    SCREEN_WIDTH = 80
    SCREEN_HEIGHT = 50

    MAP_WIDTH = 80
    MAP_HEIGHT = 45

    COLORS = {
              'darkWall' : tcod.Color(0,0,100),
              'darkGround' : tcod.Color(50,50,150),
              'lightWall' : tcod.Color(130,110,50),
              'lightGround' : tcod.Color(200,180,50)
             }
    
    ROOM_MAX_SIZE = 10
    ROOM_MIN_SIZE = 6
    MAX_ROOMS = 25
    
    FOV_ALGORITHM = 0
    FOV_LIGHT_WALLS = True
    FOV_RADIUS = 15

    MAX_MONSTERS_PER_ROOM = 2

    BAR_WIDTH = 20
    PANEL_HEIGHT = 7
    PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT

    MESSAGE_X = BAR_WIDTH + 2
    MESSAGE_WIDTH = SCREEN_WIDTH - BAR_WIDTH - 2
    MESSAGE_HEIGHT = PANEL_HEIGHT - 1
