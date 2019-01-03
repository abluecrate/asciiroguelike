# http://www.roguebasin.com/index.php?title=Complete_Roguelike_Tutorial,_using_python3%2Blibtcod

import tcod

# ----------------------------------------------------------------------
# Global Game Settings
# ----------------------------------------------------------------------

# Window Settings
FULLSCREEN = False  # Fullscreen Control
SCREEN_WIDTH = 80   # Characters Wide
SCREEN_HEIGHT = 50  # Characters Tall
LIMIT_FPS = 20      # 20 FPS MAX

# Game Control Method
TURN_BASED = True  # Turn-Based Boolean

def initialize_game():
    # Initialize Player
    global player_x, player_y # Player Position
    player_x = SCREEN_WIDTH // 2    
    player_y = SCREEN_HEIGHT // 2   
    # Initialize Font
    font_filename = 'arial10x10.png' # Font
    tcod.console_set_custom_font(font_filename, tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
    # Initialize Window
    title = 'asciiroguelike' # Window Title
    tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, title, FULLSCREEN)
    # Initialize FPS
    tcod.sys_set_fps(LIMIT_FPS)

# ----------------------------------------------------------------------
# User Input / Controls
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
        player_y -= 1
    elif tcod.console_is_key_pressed(tcod.KEY_DOWN):
        player_y += 1
    elif tcod.console_is_key_pressed(tcod.KEY_LEFT):
        player_x -= 1
    elif tcod.console_is_key_pressed(tcod.KEY_RIGHT):
        player_x += 1
    #-------------------------------------------------- 

# ----------------------------------------------------------------------
# Main Game Loop
# ----------------------------------------------------------------------

def main():
    initialize_game()   # Run Game
    exit_game = False   # Keep Open
    while not tcod.console_is_window_closed() and not exit_game:
        #-----------------------------------------------------------------
        # Player:
        tcod.console_set_default_foreground(0, tcod.white)
        tcod.console_put_char(0, player_x, player_y, '@', tcod.BKGND_NONE)  # Player Character
        tcod.console_flush()
        tcod.console_put_char(0, player_x, player_y, ' ', tcod.BKGND_NONE)  # Previous Player Location
        #-----------------------------------------------------------------
        exit_game = handle_keys()   # Exit
main()
