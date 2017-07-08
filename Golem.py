'''
  __
 /__  _  |  _  ._ _ 
 \_| (_) | (/_ | | |

This is the basic core of a tile based, turn
driven role playing game engine. Gameplay is
derived from the `Console: Handheld` rules.
-----------------------------------------------
Character Classes:
	
						ATK		DEF		MAG		SPD
	Human			+0		+0		+0		+0
	Esper			-5		-5		+10		+5
	Monster		+45		+5		-10		+10
	Robot			+5		+10		-10		-5

HP & MP start at 100%. Add your level to each
attribute.
-----------------------------------------------
Items:
	
					ATK		DEF
	Sword		+40
	Staff		+35
	Axe			+45
	Bow			+35
	Amour					+10
	Shield				+5
	Helmet				+5

When purchased, items have the ratings above.
They lose 1 point for each level up. Buy new
gear as it wears out.

Weapons cost Gold equal to Level + ATK - 35.
Armour costs Level + DEF.

Humans have:   Sword, Shield, Helmet, Armour
Espers have:   Staff, Helmet, Armour.
               Can't use Shield
Monsters have: Armour
               Can't use weapon, shield, helmet
Robots have:   Punch, Laser, Forcefield
               Can't use other items
               Robot items do not wear out.
-----------------------------------------------
Battles:
	
	Turn based. Fastest character or enemy goes
	first.
	
	Options:
		ATTACK
			Deals damage equal to your ATK minus the
			enemy DEF
		BLOCK
			Adds +15 DEF for one round
		MAGIC
			Damage is your MAG minus the enemy DEF
		RUN

	When battle ends with victory, you level up
	by 1 and gain gold equal to 3x the enemy
	level.
-----------------------------------------------
Monsters

	These have attributes equal to their level,
	with the following modifiers:
		
		ATK		DEF		MAG		SPD
		+45		+10		+50		+0
	
	The type of monster also adds:
		
								ATK		DEF		MAG		SPD	
		Beast				+5								+5
		Boss				Immune to DARK, BIO, HOLY
								Only takes 1/10 normal damage
								Gives 2 levels. May also have
								another type as well.
		Dragon			Immune to FIRE
		Elemental		Immune to one kind of magic
		Mage										+10
		Ogre (ATK)				+5
		Ogre (MAG)				-15
		Undead			Immune to DARK and BIO

	Defeating a bos should provide special items
	not available any other way.
-----------------------------------------------
To use this:

- Create a copy of this for your game
- Create images for each tile. These should be
  .png format, named like:
   0.png
   1.png
   2.png
   etc.
- Create game maps:
	`map.txt`
	`texture.txt`
	These should specify the tiles and look like:
   1,0,0,0,1
   1,0,2,0,1
   1,0,2,0,1
   1,0,0,0,1 
- Golem will examine the tiles and map data to
  determine the sizes to use.
- Add whatever logic you need to make the game
  act as desired.
-----------------------------------------------
Currently working on:
	- player stats creation
	- button handler
	- stubs for spawning enemies
	- display character on screen
	  - move using controls
	  - check boundaries
-----------------------------------------------
Todo:
	- offset maps (for transparency effects)
	- fully track character data
	- allow for enemies
	- interface:
		+--------------+
		| game map     |
		| ............ |
		| ............ |
		| ............ |
		| stats area   |
		| ............ |
		|  ^         a |
		| < >       b  |
		|  v       c   |
		+--------------+
	- control area to be themeable using .png and
	  a map of touch positions
	  - controls.png
	  - controls.txt
	    dpad:left=xx,yy,xx,yy
	    dpad:right=xx,yy,xx,yy
	    etc
	- menu system
	- turn based combat system using menus
	- timing functions
	- music and sound effects
	  - side project: midi generation language
	- track solid tiles (walls, water, etc)
	- animated tile sets
-----------------------------------------------
This should eventually support multiple layers
of map. These are:
	
	- base layer (bottom)
	- texture layer (partial transparency)
	- blend layer (offset by 1/2 tile, partial
	               transparency)
	- player / items layer (partial transparency)
	- sky layer (partial transparency)

Z indexes: 0.1, 0.2, 0.3, 0.4, 0.5

Player & items on 0.4, base is 0.1.

Texture layer and sky layers may support
animations later.
-----------------------------------------------
Fights:
	- attack
	- magic
	- defend
	- run
-----------------------------------------------
Touch events:
	- buttons will trigger on touch
	- it might make sense to allow movement on
	  the dpad for faster shifts
'''

from scene import *
import sound
import random
import math
A = Action

class Golem (Scene):
	def setup(self):
		self.create_player()
		self.sprites = list()
		self.load_mapset('world')
		pass
	
	def load_mapset(self, name):
		for child in self.sprites:
			child.remove_from_parent()
		self.sprites = list()
		self.map = self.load_map('{0}.base.txt'.format(name))
		self.texture = self.load_map('{0}.texture.txt'.format(name))
		self.rows = len(self.map)
		self.cols = len(self.map[0])
		self.prepare_tiles()
		self.generate_map()
				
	def load_map(self, file):
		map = list()
		with open(file, 'r') as f:
			for line in f.readlines():
				if len(line) > 1:
					row = list()
					raw = line[:-1].split(',')
					for item in raw:
						row.append(int(item))
					map.append(row)
		return map
							
	def locate(self, row, col, tile_size):
		return ((col * tile_size) + 25, (row * tile_size) + 300)
	
	def prepare_tiles(self):
		self.tiles = list()
		for tile in range(1000):
			self.tiles.append('{0}.png'.format(tile))
	
	def sprite_in(self, map, row, col, z):
		sprite = SpriteNode(self.tiles[map[::-1][row][col]], parent=self)
		tile_size = sprite.size.w
		self.tile_size = tile_size
		sprite.position = self.locate(row, col, tile_size)
		sprite.z_position = z
		return sprite
	
	def generate_map(self):
		self.sprites = list()
		for row in range(self.rows):
			for col in range(self.cols):
				sprite = self.sprite_in(self.map, row,  col, 0.1)
				self.sprites.append(sprite)
				sprite = self.sprite_in(self.texture, row,  col, 0.2)
				self.sprites.append(sprite)

	def did_change_size(self):
		pass
	
	def update(self):
		if self.player['row'] == 1 and self.player['col'] == 1:
			self.load_mapset('other')
		if self.player['row'] == 5 and self.player['col'] == 5:
			self.load_mapset('world')
		pass
	
	def load_button_layout(self):
		pass
	
	def load_button_image(self):
		pass
		
	def ui_control_menu(self):
		pass
	
	def ui_dpad_up(self):
		if self.player['row'] < self.rows - 1:
			self.player['row'] += 1
		self.player['sprite'].position = self.locate(self.player['row'], self.player['col'], self.tile_size)
		pass

	def ui_dpad_down(self):
		if self.player['row'] > 0:
			self.player['row'] -= 1
		self.player['sprite'].position = self.locate(self.player['row'], self.player['col'], self.tile_size)
		pass
		
	def ui_dpad_left(self):
		if self.player['col'] > 0:
			self.player['col'] -= 1
		self.player['sprite'].position = self.locate(self.player['row'], self.player['col'], self.tile_size)
		pass
		
	def ui_dpad_right(self):
		if self.player['col'] < self.cols - 1:
			self.player['col'] += 1
		self.player['sprite'].position = self.locate(self.player['row'], self.player['col'], self.tile_size)
		pass

	def ui_control_a(self):
		pass

	def ui_control_b(self):
		self.player['gp'] += 10
		pass

	def ui_control_c(self):
		self.player['gp'] -= 10
		pass
	
	def tapped(self, x, y, ux, uy, bx, by):
		if x >= ux and x <= bx and y <= uy and y >= by:
			return True
		else:
			return False

	def touch_began(self, touch):
		x, y = touch.location
		if (self.tapped(x, y, 68, 236, 92, 192)): self.ui_dpad_up()
		if (self.tapped(x, y, 10, 186, 60, 160)): self.ui_dpad_left()
		if (self.tapped(x, y, 70, 148, 106, 114)): self.ui_dpad_down()
		if (self.tapped(x, y, 105, 170, 138, 152)): self.ui_dpad_right()
		if (self.tapped(x, y, 298, 248, 337, 202)): self.ui_control_a()
		if (self.tapped(x, y, 265, 172, 304, 135)): self.ui_control_b()
		if (self.tapped(x, y, 227, 90, 260, 55)): self.ui_control_c()
		if (self.tapped(x, y, 131, 264, 234, 218)): self.ui_control_menu()
		self.stats.text = 'HP:{0} - MP:{1} - LVL:{2} - Gold:{3} @ {4},{5}'.format(self.player['hp'], self.player['mp'], self.player['xp'], self.player['gp'],self.player['row'], self.player['col'])
		pass

	def touch_moved(self, touch):
		pass
	
	def touch_ended(self, touch):
		pass
	
	def create_player(self):
		self.player = dict()
		self.player['hp'] = 100 # health points
		self.player['mp'] = 100 # magic points
		self.player['xp'] = 1 # experience points
		self.player['gp'] = 0 # gold points
		self.player['row'] = 5
		self.player['col'] = 5
		self.player['sprite'] = 0
		self.player['items'] = list()
		self.stats = LabelNode('HP:{0} - MP:{1} - LVL:{2} - Gold:{3} @ {4},{5}'.format(self.player['hp'], self.player['mp'], self.player['xp'], self.player['gp'],self.player['row'], self.player['col']))
		self.stats.position = (self.size.width / 2, 630)
		self.stats.font = ('Courier', 12)
		sprite = SpriteNode('player.png', parent=self)
		tile_size = sprite.size.w
		sprite.position = self.locate(5, 5, tile_size)
		sprite.z_position = .9
		self.player['sprite'] = sprite
		self.add_child(self.player['sprite'])
		self.add_child(self.stats)
		self.setup_controls()
		l = LabelNode('  __\n /__  _  |  _  ._ _ \n \_| (_) | (/_ | | |')
		l.position = (self.size.width / 2, 660)
		l.font = ('Courier', 10)
		self.add_child(l)
		pass
		
	def setup_controls(self):
		self.control = SpriteNode('controls.png', parent=self)
		self.control.scale = .5
		self.control.position = (self.size.w/2, 150)
		self.add_child(self.control)
	
	def spawn_enemy(self):
		pass

if __name__ == '__main__':
	run(Golem(), PORTRAIT, show_fps=True)

