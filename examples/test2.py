class Tile:
	# a tile of the map and its properties
	def __init__(self, char, blocked, block_sight = None):
		self.char = char
		self.blocked = blocked
		
		# all tiles start unexplored
		self.explored = False
		
		# by default, if a tile is blocked, it also blocks sight
		if block_sight is None: block_sight = blocked
		self.block_sight = block_sight

			
def create_h_tunnel(x1, x2, y):
	global map
	# horizontal tunnel
	for x in range(min(x1, x2), max(x1, x2) + 1):
		map[x][y].blocked = False
		map[x][y].block_sight = False
		if tcod.heightmap_get_value(hmap, x, y) > 2:
				map[x][y].char = '-'
				
def create_v_tunnel(y1, y2, x):
	global map
	# vertical tunnel
	for y in range(min(y1, y2), max(y1, y2) + 1):
		map[x][y].blocked = False
		map[x][y].block_sight = False
		if tcod.heightmap_get_value(hmap, x, y) > 2:
				map[x][y].char = '#'
				
def create_room(room):
	global map
	# go through the tiles in the rectangle and make them passable
	for x in range(room.x1 + 1, room.x2): # python's range function excludes the last element in the loop
		for y in range(room.y1 + 1, room.y2): # so +1 at the end ensures that the last element is included and
			map[x][y].blocked = False # the room is filled. +1 at the beginning ensures that the first element
			map[x][y].block_sight = False # is exluded
			if tcod.heightmap_get_value(hmap, x, y) > 2:
				map[x][y].char = '*'
			#map[x][y].char = 
			
def create_circular_room(room):
	global map
	#center of circle
	cx = (room.x1 + room.x2) / 2
	cy = (room.y1 + room.y2) / 2
	#radius of circle: make it fit nicely inside the room, by making the
	#radius be half the width or height (whichever is smaller)
	width = room.x2 - room.x1
	height = room.y2 - room.y1
	r = min(width, height) / 2
	#go through the tiles in the circle and make them passable
	for x in range(room.x1, room.x2 + 1):
		for y in range(room.y1, room.y2 + 1):
			if math.sqrt((x - cx) ** 2 + (y - cy) ** 2) <= r:
				map[x][y].blocked = False
				map[x][y].block_sight = False

				
				
def make_map():
	global map, objects, stairs, hmap

	rnd = random.randint(1,120)
	rnd2 = random.randint(1,80)
	rndrad = random.randint(55, 125)
	rndhei = random.randint(3, 20)

	hmap = tcod.heightmap_new(MAP_WIDTH,MAP_HEIGHT)
	hmap2 = tcod.heightmap_new(MAP_WIDTH,MAP_HEIGHT)
	hmap3 = tcod.heightmap_new(MAP_WIDTH,MAP_HEIGHT)
	tcod.heightmap_add(hmap, 0)
	tcod.heightmap_add(hmap3, 0)
	
	tcod.heightmap_set_value(hmap2, 2, 2, 1)
	tcod.heightmap_set_value(hmap2, 10, 10, 2)
	tcod.heightmap_set_value(hmap2, 2, 15, 3)

	tcod.heightmap_add_hill(hmap, rnd, rnd, rndrad, rndhei)
	tcod.heightmap_add_hill(hmap, 30, 25, rndrad, rndhei)
	tcod.heightmap_add_hill(hmap, rnd, 15, rndrad, rndhei)
	tcod.heightmap_add_hill(hmap, 40, 15, rndrad, rndhei)
	tcod.heightmap_add_hill(hmap, rnd, 15, rndrad, rndhei)
	tcod.heightmap_add_hill(hmap, 15, 15, rndrad, rndhei)
	tcod.heightmap_add_hill(hmap, rnd, rnd+10, rndrad, rndhei)
	tcod.heightmap_add_hill(hmap, rnd2, rnd, rndrad, rndhei)
	tcod.heightmap_add_hill(hmap, rnd, rnd2, rndrad, rndhei)
	tcod.heightmap_add_hill(hmap, rnd, rnd/rnd2, rndrad, rndhei)
	tcod.heightmap_add_hill(hmap, rnd2+rnd, rnd, rndrad, rndhei)
	tcod.heightmap_add_hill(hmap, rnd+10, rnd, rndrad, rndhei)

	tcod.heightmap_rain_erosion(hmap, MAP_WIDTH*MAP_HEIGHT, 0.4, 0.5)
	
	tcod.heightmap_normalize(hmap, 0, 11)	

	# the list of objects, currently containing only the player
	objects = [player] 
	
	# fill map with "blocked" tiles
	map = [[Tile(224,True)
		for y in range(MAP_HEIGHT) ]
			for x in range(MAP_WIDTH) ]
			
	rooms = []
	num_rooms = 0		

	
	for r in range(MAX_ROOMS):
		# random width and height
		w = tcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE) # 0 is the 'stream' to get the random number
		h = tcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE) # from - not needed here so 0 is taken.
		# random position without going out of the boundaries of the map
		x = tcod.random_get_int(0, 0, MAP_WIDTH - w - 1)
		y = tcod.random_get_int(0, 0, MAP_HEIGHT - h - 1)
		
		# "Rect" class makes rectangles easier to work with
		new_room = Rect(x, y, w, h) # originating coordinates + width and height
		
		# run through the other rooms and see if they intersect with this one
		failed = False # by default, this sets failed to False - meaning room can be created
		for other_room in rooms:
			if new_room.intersect(other_room): # if this room intersects another, BREAK
				failed = True
				break
		
		if not failed:
			room_chances = {}
			room_chances['square'] = 60
			room_chances['circle'] = 40
			choice = random_choice(room_chances)
			if choice == 'square':
				create_room(new_room)
			elif choice == 'circle':
				create_circular_room(new_room)
			(new_x, new_y) = new_room.center()
			
			if num_rooms == 0: # meaning if this is the first room, the below is actioned:
				player.x = new_x
				player.y = new_y
				
			else: # meaning for every room which is not the first room, connect it to the 
				# previous room with a tunnel
							
				# center coordinates of previous room
				(prev_x, prev_y) = rooms[num_rooms-1].center()
				
				# flip a coin (random number that is either 0 or 1)
				if tcod.random_get_int(0, 0, 1) == 1:
					# first move horizontally, then vertically
					create_h_tunnel(prev_x, new_x, prev_y)
					create_v_tunnel(prev_y, new_y, new_x)
				else:
					# first move vertically, then horizontally
					create_v_tunnel(prev_y, new_y, prev_x)
					create_h_tunnel(prev_x, new_x, new_y)
		
			# finally, append the new room to the list
			place_objects(new_room)	# and populate the rooms with items and enemies
			rooms.append(new_room)
			num_rooms += 1
			
	# create stairs at the center of the last room
	stairs = Object(new_x, new_y, '<', 'stairs up', color_light_ground, always_visible=True)
	objects.append(stairs) # appends stairs to the list of objects i tink
	stairs.send_to_back() # so it's drawn below the enemies =)
			

	
def render_all():
	global fov_map, color_dark_wall, color_light_wall
	global color_light_ground, mouse, ttw, hmap, cellheight
	global fov_recompute, player, currentlyequipped

	move_camera(player.x, player.y)	
		
	# clears the consoles, ready for OUTPUT > INPUT > PROCESSING cycle.
	tcod.console_set_default_background(tooltip, tcod.BKGND_NONE)
	tcod.console_set_default_background(cornerpanel, tcod.BKGND_NONE)
	tcod.console_set_default_background(hpanel, tcod.BKGND_NONE) # this was 12,12,12 and am keeping that here for a search term. MESSAGE LOG - PUT BORDER ROUND IT (color_light_wall?)
	tcod.console_clear(tooltip)
	tcod.console_clear(hpanel)
	tcod.console_clear(cornerpanel)
	
	
	if fov_recompute:
		# recompute FOV if needed (the player moves frinstance)
		fov_recompute = False
		tcod.map_compute_fov(fov_map, player.x, player.y, TORCH_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)
		tcod.console_clear(con)
		
		# go through all tiles and set their appearance according to the FOV
		for y in range(CAMERA_HEIGHT): # am not sure this quite makes sense. it's setting the appearance based on the cell height ----- but
			for x in range(CAMERA_WIDTH):# it moves with the player. why would that happen if the height of a given cell was defined in make_map
				cellheight = tcod.heightmap_get_value(hmap, x, y)
				hcolor = tcod.light_blue
				if cellheight < 1:
					hcolor = tcod.blue
				if cellheight == 1:
					hcolor = tcod.light_blue
				if cellheight >= 2:
					hcolor = tcod.light_yellow
				if cellheight >= 3:
					hcolor = tcod.green
				if cellheight >= 7:
					hcolor = tcod.light_green
				if cellheight >= 9:
					hcolor = tcod.desaturated_green
				if cellheight >= 11:
					hcolor = tcod.dark_green
				if cellheight >= 20:
					hcolor = tcod.grey
				if cellheight >= 25:
					hcolor = tcod.silver		


				(map_x, map_y) = (camera_x + x, camera_y + y)
				visible = tcod.map_is_in_fov(fov_map, map_x, map_y)

	
				wall = map[map_x][map_y].block_sight
				wallchar = Tile(224, True)
				
				floorchar = Tile('.', False)
				
# SO - this isn't working because what this is doing is working out how to display everything within the range of the camera. when i try to set it to display everything within MAP_WIDTH it doesn't like it because how can it set how to display something onscreen
# that is not actually onscreen.
# so i need to think of how i'm gunna do this.
# it might actually be fairly simple. will give it a bit of thinking. but right now it's calculating the appearance of the tile based on the height, which is worked out here, and clearly that's not working
# so
# maybe if i just went... normally - yknow, thru the actual tile itself rather than dynamically assigning it on runtime - maybe that might work nicer
# hmm

# like actually 
# mapgen
# tiles are assigned there
# do that
# and the problem should be KAPUT
				
# this below bit - this needs improving. currently it's all branching and shit and it's basically a whole bunch of different
# things which could probably be done by one function. surely i could just, instead of this if not visible: else: business,
# just call a function which would calculate this all. let's see.
				
				if not visible:
					# if it's not visible right now, the player can only see it if it's been explored
					if map[map_x][map_y].explored:
						# it's out of the player's FOV - see the code in trinkets.py - this part's just done by if visible: put_char_ex(map.char) and it's decided there
						if wall:
							tcod.console_put_char_ex(con, x, y, wallchar.char, color_dark_wall, tcod.BKGND_SET)
						else:
							tcod.console_put_char_ex(con, x, y, map[x][y].char, color_dark_ground, tcod.BKGND_SET)

				else:
					# it's visible
					if wall:
						tcod.console_put_char_ex(con, x, y, wallchar.char, hcolor, tcod.BKGND_SET)
					else:
						tcod.console_put_char_ex(con, x, y, map[x][y].char, hcolor, tcod.BKGND_SET)
					
						# since it's visible, explore it
					map[map_x][map_y].explored = True
				
	# draw all objects in the list
	for object in objects:
		if object != player:
			object.draw()
	player.draw()

	
	# print the game messages, one line at a time
	y = 0 # this starts on the very first line. y = 1 (its original setting) had a one line linebreak set up. no thanks.
	for (line,color) in game_msgs:
		tcod.console_set_default_foreground(hpanel, color)
		tcod.console_print_ex(hpanel, 0, y, tcod.BKGND_NONE, tcod.LEFT, line)
		y += 1

	# blit each of the consoles to the root console, the screen.
	tcod.console_blit(con, 0, 0, MAP_WIDTH, MAP_HEIGHT, 0, 1, 1)