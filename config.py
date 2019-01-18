import tcod

class Config(object):
    TITLE = 'asciiroguelike'
    FONT = 'arial10x10.png'

    SCREEN_WIDTH = 80
    SCREEN_HEIGHT = 50

    MAP_WIDTH = 80
    MAP_HEIGHT = 50

    COLORS = {
              'darkWall' : tcod.Color(0,0,100),
              'darkGround' : tcod.Color(50,50,150)
             }
    

    

