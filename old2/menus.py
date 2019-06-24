import tcod

def menu(con, header, options, width, screenWidth, screenHeight):
    if len(options) > 26:
        raise ValueError('Cannot have a menu with more than 26 options.')

    # Calculate height for header and one line per option
    headerHeight = tcod.console_get_height_rect(con, 0, 0, width, screenHeight, header)
    height = len(options) + headerHeight

    # Create off-screen console with menu's window
    window = tcod.console_new(width, height)

    # Print header with auto-wrap
    tcod.console_set_default_foreground(window, tcod.white)
    tcod.console_print_ex(window, 0, 0, tcod.BKGND_NONE, tcod.LEFT, header)

    # Print Options
    y = headerHeight
    letterIndex = ord('a')
    for optionText in options:
        text = '(' + chr(letterIndex) + ')' + optionText
        tcod.console_print_ex(window, 0, y, tcod.BKGND_NONE, tcod.LEFT, text)
        y += 1
        letterIndex += 1

    # BLit contents to root console
    x = int(screenWidth / 2 - width / 2)
    y = int(screenHeight / 2 - height / 2)
    tcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)

def inventoryMenu(con, header, inventory, inventoryWidth, screenWidth, screenHeight):
    # show a menu with each item in inventory as option
    if len(inventory.items) == 0:
        options = ['Inventory is empty.']
    else:
        options = [item.name for item in inventory.items]

    menu(con, header, options, inventoryWidth, screenWidth, screenHeight)
