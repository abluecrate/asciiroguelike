# http://www.roguebasin.com/index.php?title=Complete_Roguelike_Tutorial,_using_python3%2Blibtcod

import tcod

# ----------------------------------------------------------------------
# GLOBAL GAME SETTINGS
# ----------------------------------------------------------------------

# Window Settings
FULLSCREEN = False  # Fullscreen Control
LIMIT_FPS = 20      # 20 FPS MAX
SCREEN_WIDTH = 60   # Characters Wide
SCREEN_HEIGHT = 40  # Characters Tall

# Map Settings
MAP_WIDTH = 60
MAP_HEIGHT = 35
color_dark_wall = tcod.Color(0,0,100)
color_dark_ground = tcod.Color(50,50,150)

ROOM_MAX_SIZE = 15
ROOM_MIN_SIZE = 5
MAX_ROOMS = 20

# Game Control Method
TURN_BASED = True  # Turn-Based Boolean

# Game Appearance
TITLE = 'asciiroguelike'
FONT_FILE = 'arial10x10.png'

# ----------------------------------------------------------------------
# USER INPUT / CONTROLS
# ----------------------------------------------------------------------

def get_key_event(turn_based = None):               # Gather Keyboard Input
    if turn_based:
        key = tcod.console_wait_for_keypress(True)  # Turn-Based: Wait For Input
    else:
        key = tcod.console_check_for_keypress()     # Real-Time: Don't Wait
    return key

def handle_keys():
    global player_x, player_y           # Player Position
    key = get_key_event(TURN_BASED)     # Gather Keyboard Input
    # Key Check For Fullscreen / Exiting
    if key.vk == tcod.KEY_ENTER and key.lalt:
        tcod.console_set_fullscreen(not tcod.console_is_fullscreen())   # Alt + Enter: Toggle Fullscreen
    elif key.vk == tcod.KEY_ESCAPE:
        return True  # Exit Game
    #--------------------------------------------------
    # Movement Keys
    if tcod.console_is_key_pressed(tcod.KEY_UP):
        player.move(0, -1)
    elif tcod.console_is_key_pressed(tcod.KEY_DOWN):
        player.move(0, 1)
    elif tcod.console_is_key_pressed(tcod.KEY_LEFT):
        player.move(-1, 0)
    elif tcod.console_is_key_pressed(tcod.KEY_RIGHT):
        player.move(1, 0)
    #--------------------------------------------------

# ----------------------------------------------------------------------
# MAP HANDLING
# ----------------------------------------------------------------------

class Tile:
    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked
        if block_sight is None:
            block_sight = blocked
        self.block_sight = block_sight

class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
    def center(self):
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return center_x, center_y
    def intersect(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

def create_room(room):
    global map
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            map[x][y].blocked = False
            map[x][y].block_sight = False

def create_h_tunnel(x1, x2, y):
    global map
    for x in range(min(x1,x2), max(x1,x2)+1):
        map[x][y].blocked = False
        map[x][y].block_sight = False

def create_v_tunnel(y1, y2, x):
    global map
    for y in range(min(y1,y2), max(y1,y2)+1):
        map[x][y].blocked = False
        map[x][y].block_sight = False

def make_map():
    global map
    map = [[Tile(True) for y in range(MAP_HEIGHT)] for x in range(MAP_WIDTH)]

    rooms = []
    num_rooms = 0

    for r in range(MAX_ROOMS):
        w = tcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        h = tcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        x = tcod.random_get_int(0, 0, MAP_WIDTH - w - 1)
        y = tcod.random_get_int(0, 0, MAP_HEIGHT - h - 1)

        new_room = Rect(x, y, w, h)

        failed = False
        for other_room in rooms:
            if new_room.intersect(other_room):
                failed = True
                break

        if not failed:
            create_room(new_room)
            (new_x, new_y) = new_room.center()
            room_no = Object(new_x, new_y, chr(65 + num_rooms), tcod.white)
            objects.insert(0, room_no)

            if num_rooms == 0:
                player.x = new_x
                player.y = new_y
            else:
                (prev_x, prev_y) = rooms[num_rooms - 1].center()

                if tcod.random_get_int(0, 0, 1) == 1:
                    create_h_tunnel(prev_x, new_x, prev_y)
                    create_v_tunnel(prev_y, new_y, new_x)
                else:
                    create_v_tunnel(prev_y, new_y, prev_x)
                    create_h_tunnel(prev_x, new_x, new_y)

            rooms.append(new_room)
            num_rooms += 1

# ----------------------------------------------------------------------
# OBJECT HANDLING
# ----------------------------------------------------------------------

# Generic Object Class Representing Any Screen Item
class Object:
    def __init__(self, x, y, char, color):
        self.x = x          # X-Coordinate
        self.y = y          # Y-Coordinate
        self.char = char    # Character
        self.color = color  # Color

    def move(self, dx, dy): # Move Object By Given Amount
        if not map[self.x + dx][self.y + dy].blocked:
            self.x += dx
            self.y += dy

    def draw(self):         # Draw Character
        tcod.console_set_default_foreground(con, self.color)
        tcod.console_put_char(con, self.x, self.y, self.char, tcod.BKGND_NONE)

    def clear(self):        # Erase Character
        tcod.console_put_char(con, self.x, self.y, ' ', tcod.BKGND_NONE)

# ----------------------------------------------------------------------
# RENDERING
# ----------------------------------------------------------------------

def render_all():
    global color_light_wall
    global color_light_ground

    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            wall = map[x][y].block_sight
            if wall:
                tcod.console_set_char_background(con, x, y, color_dark_wall, tcod.BKGND_SET)
            else:
                tcod.console_set_char_background(con, x, y, color_dark_ground, tcod.BKGND_SET)

    for object in objects:
        object.draw()

    tcod.console_blit(con, 0, 0 , SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
# ----------------------------------------------------------------------
# INITIALIZATION
# ----------------------------------------------------------------------

tcod.console_set_custom_font(FONT_FILE, tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, FULLSCREEN)
tcod.sys_set_fps(LIMIT_FPS)
con = tcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

# OBJECTS:
player = Object(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, '@', tcod.white)
npc = Object(SCREEN_WIDTH // 2 - 5, SCREEN_HEIGHT // 2, '@', tcod.yellow)
objects = [npc, player]

make_map()

# def initialize_game():
    # Initialize Player
    # global player_x, player_y # Player Position
    # player_x = SCREEN_WIDTH // 2
    # player_y = SCREEN_HEIGHT // 2
    # Initialize Font
    # font_filename = 'arial10x10.png' # Font
    # tcod.console_set_custom_font(font_filename, tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
    # Initialize Window
    # title = 'asciiroguelike' # Window Title
    # tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, title, FULLSCREEN)
    # con = tcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
    # Initialize FPS
    # tcod.sys_set_fps(LIMIT_FPS)

# ----------------------------------------------------------------------
# MAIN GAME LOOP
# ----------------------------------------------------------------------

while not tcod.console_is_window_closed():
    # Render Screen
    render_all()

    tcod.console_flush()

    # Erase Before Move
    for object in objects:
        object.clear()

    exit = handle_keys()
    if exit:
        break

# def main():
    # initialize_game()   # Run Game
    # exit_game = False   # Keep Open
    # while not tcod.console_is_window_closed() and not exit_game:
        #-----------------------------------------------------------------
        # Player:
        # tcod.console_set_default_foreground(con, tcod.white)
        # tcod.console_put_char(con, player_x, player_y, '@', tcod.BKGND_NONE)  # Player Character
        # tcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
        # tcod.console_flush()
        # tcod.console_put_char(con, player_x, player_y, ' ', tcod.BKGND_NONE)  # Previous Player Location
        #-----------------------------------------------------------------
        # exit_game = handle_keys()   # Exit
# main()
