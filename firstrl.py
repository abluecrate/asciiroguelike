# http://www.roguebasin.com/index.php?title=Complete_Roguelike_Tutorial,_using_python3%2Blibtcod

import tcod

# ----------------------------------------------------------------------
# GLOBAL GAME SETTINGS
# ----------------------------------------------------------------------

# Window Settings
FULLSCREEN = False  # Fullscreen Control
SCREEN_WIDTH = 80   # Characters Wide
SCREEN_HEIGHT = 50  # Characters Tall
LIMIT_FPS = 20      # 20 FPS MAX

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
# OBJECT CLASS
# ----------------------------------------------------------------------

# Generic Object Class Representing Any Screen Item
class Object:
    def __init__(self, x, y, char, color):
        self.x = x          # X-Coordinate
        self.y = y          # Y-Coordinate
        self.char = char    # Character
        self.color = color  # Color

    def move(self, dx, dy): # Move Object By Given Amount
        self.x += dx
        self.y += dy

    def draw(self):         # Draw Character
        tcod.console_set_default_foreground(con, self.color)
        tcod.console_put_char(con, self.x, self.y, self.char, tcod.BKGND_NONE)

    def clear(self):        # Erase Character
        tcod.console_put_char(con, self.x, self.y, ' ', tcod.BKGND_NONE)

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
    # Draw Objects in List
    for object in objects:
        object.draw()

    tcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
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
