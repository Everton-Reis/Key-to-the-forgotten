# mapa.py
import pygame
import enemy as liben
import bars as Life
import sys

sys.path.append("../")

from gamesettings import *

# Configurações do bloco e do mapa
BLUE = (0, 0, 255)
RED = (255,0,0)
GREEN = (0,255,0)

#achar uma forma de parar o jogo quando o player terminar o jogo
#ou continuar infinitamente (ENDLESS MODE)

# Map Assets
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
from pytmx.util_pygame import load_pygame

tmx_data = load_pygame("../assets/sprites/mapa/mapas3-4.tmx")
tmx_data2 = load_pygame("../assets/sprites/mapa/mapa4-4.tmx")
end_assets = tmx_data2.get_layer_by_name("end_cenario")
map_assets = tmx_data.get_layer_by_name("map_cenario")
extended_map_assets = tmx_data.get_layer_by_name("extended_cenario")
boss_map_assets = tmx_data.get_layer_by_name("boss_cenario")


map_layout = [
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
]

end_layout = [
	[1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1],
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

extend_map_layout = [
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
]

boss_map_layout = [
	[1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
	[1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
]

class Tile(pygame.sprite.Sprite):

    def __init__(self, pos, surface, tile_size):
        super().__init__()
        self.image = pygame.transform.scale(surface, (tile_size, tile_size))
        self.rect = self.image.get_rect(topleft = pos)
        
    def update(self):
        self.rect.y += BLOCK_SPEED
        
        

class Map_Sprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def update(self):
        for sprite in self.sprites():
            sprite.update()
            if sprite.rect.y >= SCREEN_SIZE[1]:
                self.remove(sprite)
class Map:
	def __init__(self, endless_mode):

		self.normal_layout = map_layout
		self.extend_layout = extend_map_layout
		self.boss_layout = boss_map_layout
		self.end_layout = end_layout
		self.normal_cenario = map_assets
		self.extend_cenario = extended_map_assets
		self.boss_cenario = boss_map_assets
		self.end_cenario = end_assets
		self.block_size = BLOCK_SIZE
		self.color = BLUE
		self.block_speed = BLOCK_SPEED
		self.extend_index = 0
		self.floor = 1
		self.boss_floor = BOSS_FLOOR
		self.max_floor = 500 if endless_mode else MAX_FLOOR
		self.game_ended = False
		self.map_sprites = Map_Sprites()
	
	def draw_plataforms(self, screen, plataforms, size_height, camera_offset):
		self.map_sprites.draw(screen)
		for plataform in plataforms:

			if plataform.y > size_height + 400:
				plataforms.remove(plataform)
    
	def give_cenario(self, type, extend):
		cenario = None

		if self.floor == self.max_floor:
			self.game_ended = True

		if type == 0:
			cenario = self.normal_cenario
		elif type == 1:
			cenario = self.extend_cenario
		elif type == 2:
			cenario  = self.boss_cenario

		if self.floor == self.max_floor and self.floor != 0 and type != 2:
			cenario  = self.end_cenario
			
		
		map_height = 21 * self.block_size
		if cenario == self.end_cenario:
			map_height += self.block_siza
        

		if (len(self.map_sprites.sprites()) <= 750):
			for x,y,surf in cenario.tiles():
				x_pos = x * self.block_size/2 + 700 // 6
				y_pos = y * self.block_size/2 + SCREEN_SIZE[1] - map_height
				if extend:
					y_pos = y * self.block_size/2 - map_height -  self.block_size* 1.5
				pos = (x_pos, y_pos)
				self.map_sprites.add(Tile(pos, surf,(self.block_size/2)))

    

	def give_plataforms(self, type, extend):
		layout = None

		if extend:
			self.floor += 1

		if self.floor == self.max_floor:
			self.game_ended = True

		if type == 0:
			layout = self.normal_layout
		elif type == 1:
			layout = self.extend_layout
		elif type == 2:
			layout = self.boss_layout

		if self.floor == self.max_floor and self.floor != 0:
			layout = self.end_layout

		plataforms = []
		standing_plataforms = []
		for line_index, line in enumerate(layout):
			for column_index, block in enumerate(line):
				if block == 1:
					plataform_rect = None
					if extend:
						plataform_rect = pygame.Rect(
							column_index * self.block_size + 700 // 6,
							-line_index * self.block_size - self.block_size * 1.5,
							self.block_size,
							self.block_size
						)
					else:
						plataform_rect = pygame.Rect(
							column_index * self.block_size + 700 // 6,
							-line_index * self.block_size + SCREEN_SIZE[1],
							self.block_size,
							self.block_size
						)
					plataforms.append(plataform_rect)
					if line_index > 2 and column_index > 1 and \
					column_index < len(layout[0]) - 1 and \
					layout[line_index - 1][column_index] == 0 and \
					type != 3:
						standing_plataforms.append(plataform_rect)



		return plataforms, standing_plataforms

	def move_map(self, plataforms):
		if self.game_ended:
			for index, plataform in enumerate(plataforms):
				if plataforms[0].y >= SCREEN_SIZE[1] + 300:
					break

				plataform.y += self.block_speed
			self.map_sprites.update()

			return True

		extend = False
		for index, plataform in enumerate(plataforms):
			plataform.y += self.block_speed

			if plataform.y == SCREEN_SIZE[1] + plataform.height:
				if index == self.extend_index:
					extend = True

				plataforms.remove(plataform)
		self.map_sprites.update()

		return extend

	def extend_map(self, enemies, old_plat, old_stand_plat):
		if self.floor == self.max_floor:
			return old_plat, [], None

		is_boss_floor = self.floor % self.boss_floor == 0 and self.floor != 0
		is_boss_layout = (self.floor) % self.boss_floor == self.boss_floor - 1 and self.floor != 1

		type = 0
		boss_lifebar = None

		if enemies.boss or is_boss_layout:
			type = 2
		else:
			type = 1 if not is_boss_floor else 2
			if type == 2:
				boss_damage = BOSS_INITIAL_DAMAGE * 0.3 * self.floor
				boss_maxhealth = BOSS_INITIAL_MAX_HEALTH * 0.3 * self.floor
				boss_xp = BOSS_XP * 0.3 * self.floor

				enemies.boss = liben.Boss(1100 // 2 + 25*BLOCK_SPEED, SCREEN_SIZE[1] // 3,
											boss_damage, boss_maxhealth, boss_xp)

				boss_lifebar = Life.LifeBar(enemies.boss, "boss")

		new_plataforms, new_standing_plataforms = self.give_plataforms(type, True)
		old_plat = new_plataforms + old_plat
		old_stand_plat += new_standing_plataforms
		self.give_cenario(type, True)

		return old_plat, old_stand_plat, boss_lifebar


