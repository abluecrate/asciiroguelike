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
MAP_WIDTH = 60      # Characters Wide
MAP_HEIGHT = 35     # Characters Tall

ROOM_MAX_SIZE = 15  # Max Room Dimension
ROOM_MIN_SIZE = 5   # Min Room Dimension
MAX_ROOMS = 20      # Max Number of Dungeon Rooms

# FOV ALGORITHM
FOV_ALGO = 0
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 15
color_dark_wall = tcod.Color(0,0,100)       # Wall Color
color_light_wall = tcod.Color(130,110,50)   # Lit Wall Color
color_dark_ground = tcod.Color(50,50,150)   # Ground Color
color_light_ground = tcod.Color(200,180,50) # Lit Ground Color

# Game Control Method
TURN_BASED = True  # Turn-Based Boolean

# Game Appearance
TITLE = 'asciiroguelike'        # Window Title
FONT_FILE = 'arial10x10.png'    # Font File

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
    # global player.x, player.y           # Player Position
    global FOV_recompute
    key = get_key_event(TURN_BASED)     # Gather Keyboard Input
    if key.vk == tcod.KEY_ENTER and key.lalt:                           # Key Check For Fullscreen / Exiting
        tcod.console_set_fullscreen(not tcod.console_is_fullscreen())   # Alt + Enter : Toggle Fullscreen
    elif key.vk == tcod.KEY_ESCAPE:                                     # Esc : Exit Game
        return True
    #--------------------------------------------------
    # Movement Keys
    if tcod.console_is_key_pressed(tcod.KEY_UP):        # Up Arrow
        player.move(0, -1)
        FOV_recompute = True
    elif tcod.console_is_key_pressed(tcod.KEY_DOWN):    # Down Arrow
        player.move(0, 1)
        FOV_recompute = True
    elif tcod.console_is_key_pressed(tcod.KEY_LEFT):    # Left Arrow
        player.move(-1, 0)
        FOV_recompute = True
    elif tcod.console_is_key_pressed(tcod.KEY_RIGHT):   # Right Arrow
        player.move(1, 0)
        FOV_recompute = True
    #--------------------------------------------------

# ----------------------------------------------------------------------
# MAP HANDLING
# ----------------------------------------------------------------------

class Tile:
    # Tile Instance
    def __init__(self, blocked, block_sight = None):
        self.explored = False
        self.blocked = blocked          # Block Boolean
        if block_sight is None:         # Default Tile
            block_sight = blocked       # |--> Blocks Sight
        self.block_sight = block_sight  # Sight Boolean

class Rect:
    # Rectangle Handler
    def __init__(self, x, y, w, h):
        self.x1 = x         # Top Left X
        self.y1 = y         # Top Left Y
        self.x2 = x + w     # Bottom Right X
        self.y2 = y + h     # Bottom Right Y
    # Center of Rectangle
    def center(self):
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return center_x, center_y
    # Room Intersection Boolean
    def intersect(self, other):
        # Returns True if Rectangle Coordinate Ranges Overlap
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

def create_room(room):
    # Generate Room --> Rectangle of Passable Tiles
    global map
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            map[x][y].blocked = False
            map[x][y].block_sight = False

def create_h_tunnel(x1, x2, y):
    # Generate Horizontal Tunnel
    global map
    for x in range(min(x1,x2), max(x1,x2)+1):
        map[x][y].blocked = False
        map[x][y].block_sight = False

def create_v_tunnel(y1, y2, x):
    # Generate Vertical Tunnel
    global map
    for y in range(min(y1,y2), max(y1,y2)+1):
        map[x][y].blocked = False
        map[x][y].block_sight = False

def make_map():
    # Generate Map
    global map
    # Fill Map with Blocked Tiles
    map = [[Tile(True) for y in range(MAP_HEIGHT)] for x in range(MAP_WIDTH)]

    # ----------------------------------------------------------------------
    # Random Dungeon Room Generation
    rooms = []
    num_rooms = 0

    for r in range(MAX_ROOMS):
        w = tcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)    # Random Width
        h = tcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)    # Random Height
        x = tcod.random_get_int(0, 0, MAP_WIDTH - w - 1)            # Random Position X
        y = tcod.random_get_int(0, 0, MAP_HEIGHT - h - 1)           # Random Position Y

        new_room = Rect(x, y, w, h) # Create New Room

        failed = False
        for other_room in rooms:                # Iterate Over "Other" Rooms
            if new_room.intersect(other_room):  # Check Intersection
                failed = True                   # Fail If Intersected
                break

        if not failed:                                                          # If Room Did Not Intersect:
            create_room(new_room)                                               # Generate New Room
            (new_x, new_y) = new_room.center()                                  # Get Center Point
            room_no = Object(new_x, new_y, chr(65 + num_rooms), tcod.white)     # Show Room Build Order
            objects.insert(0, room_no)

            if num_rooms == 0:      # First Room
                player.x = new_x    # Player Starting Position X
                player.y = new_y    # Player Starting Position Y
            else:
                (prev_x, prev_y) = rooms[num_rooms - 1].center()
                # Random Tunnel Connect
                if tcod.random_get_int(0, 0, 1) == 1:
                    create_h_tunnel(prev_x, new_x, prev_y)  # Horizontal
                    create_v_tunnel(prev_y, new_y, new_x)   # Vertical
                else:
                    create_v_tunnel(prev_y, new_y, prev_x)  # Vertical
                    create_h_tunnel(prev_x, new_x, new_y)   # Horizontal

            rooms.append(new_room)  # Append New Room To List
            num_rooms += 1          # Total Number of Rooms Increase
    # ----------------------------------------------------------------------

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
            self.x += dx    # Move Amount --> X-Direction
            self.y += dy    # Move Amount --> Y-Direction

    def draw(self):         # Draw Character
        if tcod.map_is_in_fov(FOV_map, self.x, self.y):
            tcod.console_set_default_foreground(con, self.color)
            tcod.console_put_char(con, self.x, self.y, self.char, tcod.BKGND_NONE)

    def clear(self):        # Erase Character
        tcod.console_put_char(con, self.x, self.y, ' ', tcod.BKGND_NONE)

# ----------------------------------------------------------------------
# RENDERING
# ----------------------------------------------------------------------

def render_all():
    global color_light_wall, color_dark_wall
    global color_light_ground, color_dark_ground
    global FOV_map, FOV_recompute

    if FOV_recompute:
        FOV_recompute = False
        tcod.map_compute_fov(FOV_map, player.x, player.y, TORCH_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)

    # Iterate Room Tiles and Set Color
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            visible = tcod.map_is_in_fov(FOV_map, x, y)
            wall = map[x][y].block_sight
            if not visible:
                if map[x][y].explored:
                    if wall:
                        tcod.console_set_char_background(con, x, y, color_dark_wall, tcod.BKGND_SET)
                    else:
                        tcod.console_set_char_background(con, x, y, color_dark_ground, tcod.BKGND_SET)
            else:
                if wall:
                    tcod.console_set_char_background(con, x, y, color_light_wall, tcod.BKGND_SET)
                else:
                    tcod.console_set_char_background(con, x, y, color_light_ground, tcod.BKGND_SET)
                map[x][y].explored = True

    for object in objects:  # Object List
        object.draw()       # Draw All Objects

    tcod.console_blit(con, 0, 0 , SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0) # Blit Contents To Root Console

# ----------------------------------------------------------------------
# INITIALIZATION
# ----------------------------------------------------------------------

tcod.console_set_custom_font(FONT_FILE, tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)   # Set Font
tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, FULLSCREEN)                      # Establish Primary Console
tcod.sys_set_fps(LIMIT_FPS)                                                                 # Set FPS
con = tcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)                                         # Create Off-Screen Console

# OBJECTS:
player = Object(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, '@', tcod.white)
npc = Object(SCREEN_WIDTH // 2 - 5, SCREEN_HEIGHT // 2, '@', tcod.yellow)
objects = [npc, player]

make_map()                                      # Generate Map --> Don't Draw Yet
FOV_map = tcod.map_new(MAP_WIDTH, MAP_HEIGHT)   # Genrate FOV Map
for y in range(MAP_HEIGHT):
    for x in range(MAP_WIDTH):
        tcod.map_set_properties(FOV_map, x, y, not map[x][y].block_sight, not map[x][y].blocked)
FOV_recompute = True
# ----------------------------------------------------------------------
# MAIN GAME LOOP
# ----------------------------------------------------------------------

while not tcod.console_is_window_closed():
    render_all()            # Render Screen
    tcod.console_flush()    # Update Display

    for object in objects:
        object.clear()      # Erase Objects at Old Locations

    exit = handle_keys()
    if exit:
        break

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
