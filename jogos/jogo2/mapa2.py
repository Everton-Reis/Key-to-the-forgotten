import pygame
import enemy as liben
import bars as Life
import sys

#sys.path.append("../")

from gamesettings import *

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)

# Configurações do bloco e do mapa
BLUE = (0, 0, 255)
RED = (255,0,0)
GREEN = (0,255,0)



## NOVO MAPA]
from pytmx.util_pygame import load_pygame

tmx_data = load_pygame("../../implementacao_Mapa/data/map/tmx/mapa1.1.tmx")
##
class Map:
	def __init__(self, endless_mode):

		self.end_layout = [tmx_data.get_layer_by_name('map_layout'), tmx_data.get_layer_by_name('map_objects')]
		self.extend_layout = [tmx_data.get_layer_by_name('extend_map_layout'), tmx_data.get_layer_by_name('extend_map_objects')]
		self.boss_layout = [tmx_data.get_layer_by_name('boss_map_layout'), tmx_data.get_layer_by_name('boss_map_objects')]
		self.normal_layout = [tmx_data.get_layer_by_name('end_layout'), tmx_data.get_layer_by_name('end_objects')]
		self.block_size = BLOCK_SIZE
		self.color = BLUE
		self.block_speed = BLOCK_SPEED
		self.extend_index = 0
		self.floor = 1
		self.boss_floor = BOSS_FLOOR
		self.max_floor = 500 if endless_mode else MAX_FLOOR
		self.game_ended = False
	
	def draw_plataforms(self, screen, plataforms, size_height, camera_offset):
		for plataform in plataforms:
			pygame.draw.rect(screen, self.color, plataform)    

			if plataform.y > size_height + 400:
				plataforms.remove(plataform)

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

		if self.floor == self.max_floor and self.floor != 0 and type != 2:
			layout = self.end_layout

		plataforms = []
		standing_plataforms = []
		for obj in layout[1]:
			plataform_rect = None
			is_standing = (obj.name == 'floor')
			if extend:
				plataform_rect = pygame.Rect(
							obj.x / 32 * self.block_size + SCREEN_SIZE[0] // 6,
							-obj.y/ 32 * self.block_size - self.block_size * 1.5,
							obj.width / 32 * self.block_size,
							obj.height / 32 * self.block_size
						)
			else:
				plataform_rect = pygame.Rect(
                    obj.x /32 * self.block_size + SCREEN_SIZE[0] // 6,
                    (obj.y /32 * self.block_size)-SCREEN_SIZE[1],
                    obj.width * 2,
                    obj.height * 2
                ) 
				print(f'debug:  rect: {obj.x, obj.y, obj.width, obj.height}, plataform{plataform_rect}')
			plataforms.append(plataform_rect)
			if is_standing:
				standing_plataforms.append(plataform_rect)


		return plataforms, standing_plataforms

	def move_map(self, plataforms):
		if self.game_ended:
			for index, plataform in enumerate(plataforms):
				plataform.y += self.block_speed

				if plataforms[0].y >= SCREEN_SIZE[1] + 100:
					break

			return True

		extend = False
		for index, plataform in enumerate(plataforms):
			plataform.y += self.block_speed

			if plataform.y == SCREEN_SIZE[1] + plataform.height:
				if index == self.extend_index:
					extend = True

				plataforms.remove(plataform)

		return extend

	def extend_map(self, enemies, old_plat, old_stand_plat, screen):
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
				enemies.boss = liben.Boss(SCREEN_SIZE[0] // 2 + 25*BLOCK_SPEED, SCREEN_SIZE[1] // 3)
				boss_lifebar = Life.LifeBar(enemies.boss, "boss", screen)

		new_plataforms, new_standing_plataforms = self.give_plataforms(type, True)
		old_plat = new_plataforms + old_plat
		old_stand_plat += new_standing_plataforms

		return old_plat, old_stand_plat, boss_lifebar
