# mapa.py
import pygame

# Configurações do bloco e do mapa
SCREEN_SIZE = (1200, 1000)
BLOCK_SIZE = 50
BLOCK_SPEED = 1
BLUE = (0, 0, 255)

map_layout = [
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
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
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

class Map:
	def __init__(self):


		self.layout = map_layout
		self.block_size = BLOCK_SIZE
		self.color = BLUE
		self.block_speed = BLOCK_SPEED
	
	def draw_plataforms(self, screen, plataforms, size_height, camera_offset):
		for plataform in plataforms:
			pygame.draw.rect(screen, BLUE, plataform)    

			if plataform.y > size_height + 400:
				plataforms.remove(plataform)

	def give_plataforms(self):

		plataforms = []
		standing_plataforms = []
		for line_index, line in enumerate(self.layout):
			for column_index, block in enumerate(line):
				if block == 1:
					plataform_rect = pygame.Rect(
						column_index * self.block_size + SCREEN_SIZE[0] // 6,
						-line_index * self.block_size + SCREEN_SIZE[1] / 1.1,
						self.block_size,
						self.block_size
					)
					plataforms.append(plataform_rect)
					if line_index < 12 and column_index > 1 and \
					column_index < len(self.layout[0]) - 1 and \
					self.layout[line_index - 1][column_index] == 0:
						standing_plataforms.append(plataform_rect)



		return plataforms, standing_plataforms

	def move_map(self, plataforms):
		for plataform in plataforms:
			plataform.y += self.block_speed

