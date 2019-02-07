import tcod

FULLSCREEN = False

SCREEN_WIDTH = 60
SCREEN_HEIGHT = 40

TITLE = 'maptest' 
FONT_FILE = 'arial10x10.png' 

colors = [[17,51,17],[20,48,20],[14,50,13],[18,49,18],[16,48,19],[19,52,15]]
character = ['A','B','C','D','E','F']

def get_key_event():                        # Gather Keyboard Input
    key = tcod.console_wait_for_keypress(True)    # Wait For Input
    return key

def handle_keys():
    key = get_key_event()
    if tcod.console_is_key_pressed(tcod.KEY_UP):
        make_map()
    if key.vk == tcod.KEY_ESCAPE:
        return True

def make_map():
    # global map
    for y in range(SCREEN_HEIGHT):
        for x in range(SCREEN_WIDTH):
            r = tcod.random_get_int(0, 0, len(colors)-1)
            color = colors[r]
            tcod.console_set_char_background(con, x, y, tcod.Color(color[0],color[1],color[2]), tcod.BKGND_SET)
    tcod.console_blit(con, 0, 0 , SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

tcod.console_set_custom_font(FONT_FILE, tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD) 
tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, FULLSCREEN)                
con = tcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)                       

make_map()

while not tcod.console_is_window_closed():
    tcod.console_flush() 
    exit = handle_keys()
    if exit:
        break