import tcod

FULLSCREEN = False

SCREEN_WIDTH = 60   # Characters Wide
SCREEN_HEIGHT = 40  # Characters Tall

TITLE = 'maptest'        # Window Title
FONT_FILE = 'arial10x10.png'    # Font File

colors = [[17,51,17],[20,48,20],[11,45,11],[18,73,18],[13,79,13],[7,66,7]]

def make_map():
    global map
    for y in range(SCREEN_HEIGHT):
        for x in range(SCREEN_WIDTH):
            r = tcod.random_get_int(0, 0, range(colors))
            tcod.console_set_char_background(con, x, y, tcod.Color(colors[r]), tcod.BKGND_SET)
    tcod.console_blit(con, 0, 0 , SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0) # Blit Contents To Root Console

tcod.console_set_custom_font(FONT_FILE, tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)   # Set Font
tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, FULLSCREEN)                      # Establish Primary Console
con = tcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)                                         # Create Off-Screen Console

make_map()

