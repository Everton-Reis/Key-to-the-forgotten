import pygame
import random
import sys

sys.path.append("../../jogos")

from gamesettings import *

class Buff:
	def __init__(self, sprite):
		self.clicked = False
		self.name = "Nome"
		self.description = "Um buff"
		self.effect = 0
		self.prob = 0

		self.image = pygame.image.load(sprite)
		self.image = pygame.transform.scale(self.image, (100, 200))

	def apply(self, player):
		pass

class DamageBuff(Buff):
	def __init__(self):
		super().__init__(DAMAGE_SPRITE)
		self.name = "AUMENTO DE DANO"
		self.description = "Aumenta o dano"
		self.effect = DAMAGE_EFFECT
		self.prob = DAMAGE_PROB

	def apply(self, player):
		player.damage += int(self.effect*player.damage)


class JumpBuff(Buff):
	def __init__(self):
		super().__init__(JUMP_SPRITE)
		self.name = "PULO EXTRA"
		self.description = "Aumenta o número de pulos"
		self.effect = JUMP_EFFECT
		self.prob = JUMP_PROB

	def apply(self, player):
		player.jump_count_max += self.effect

class ShootBuff(Buff):
	def __init__(self):
		super().__init__(SHOOT_SPRITE)
		self.name = "TIRO EXTRA"
		self.description = "Aumenta o número de tiros"
		self.effect = SHOOT_EFFECT
		self.prob = SHOOT_PROB

	def apply(self, player):
		player.shoot += self.effect

class HealthBuff(Buff):
	def __init__(self):
		super().__init__(HEALTH_SPRITE)
		self.name = "AUMENTO DE VIDA MÁXIMA"
		self.description = "Aumenta a vida máxima"
		self.effect = HEALTH_EFFECT
		self.prob = HEALTH_PROB

	def apply(self, player):
		player.MAX_HEALTH += int(self.effect*player.MAX_HEALTH)

class VelBuff(Buff):
	def __init__(self):
		super().__init__(VEL_SPRITE)
		self.name = "AUMENTO DE VELOCIDADE"
		self.description = "Aumenta a velocidade"
		self.effect = VEL_EFFECT
		self.prob = VEL_PROB

	def apply(self, player):
		player.speed_x += self.effect*player.speed_x

class DashBuff(Buff):
	def __init__(self):
		super().__init__(DASH_SPRITE)
		self.name = "DASH"
		self.description = "Dash em direção ao mouse"
		self.effect = DASH_EFFECT
		self.prob = DASH_PROB

	def apply(self, player):
		player.dash += self.effect

class LSBuff(Buff):
	def __init__(self):
		super().__init__(LS_SPRITE)
		self.name = "ROUBO DE VIDA"
		self.description = "Aumenta o roubo de vida"
		self.effect = LS_EFFECT
		self.prob = LS_PROB

	def apply(self, player):
		player.ls += self.effect


class Buffs():
	def __init__(self):
		self.buffs = list()

	def create_buffs(self):
		self.buffs.clear()
		number = NUMBER_BUFFS

		possible = [DamageBuff(), HealthBuff(), VelBuff(),
					DashBuff(), JumpBuff(), ShootBuff(), LSBuff()]

		prob_list = []

		for i, buff in enumerate(possible):
			for _ in range(buff.prob):
				prob_list.append(i)

		for _ in range(number):
			index = random.choice(prob_list)
			
			self.buffs.append(possible[index])


	def display_buffs(self, screen, card_size, player_level):
		width, height = card_size
		spacing = 20


		level_font = pygame.font.Font(None, 50)
		level_text = f"LEVEL UP!!! NÍVEL ATUAL : {player_level}"
		level_surface = level_font.render(level_text, True, (random.randint(0,255),
															random.randint(0,255),
															random.randint(0,255)))
		screen.blit(level_surface, (400, 200))

		name_font = pygame.font.Font(None, 20)
		description_font = pygame.font.Font(None, 20)
		effect_font = pygame.font.Font(None, 20)

		start_x = (screen.get_width() - (len(self.buffs) * (width + spacing) - spacing)) // 2
		start_y = screen.get_height() // 2 - height // 2
		buff_rects = []

		for i, buff in enumerate(self.buffs):
			x = start_x + i * (width + spacing)
			y = start_y
			buff_rect = pygame.Rect(x, y, width, height)
			buff_rects.append((buff, buff_rect))

			pygame.draw.rect(screen, (200, 200, 200), buff_rect, border_radius=10)
			pygame.draw.rect(screen, (100, 100, 100), buff_rect, 3, border_radius=10)

			name_surface = name_font.render(buff.name, True, (0, 0, 0))
			screen.blit(name_surface, (x + 10, y + 10))

			sprite_rect = buff.image.get_rect(center=(x + width // 2, y + height // 2 - 40))
			screen.blit(buff.image, sprite_rect)

			# Descrição
			description_surface = description_font.render(buff.description, True, (0, 0, 0))
			screen.blit(description_surface, (x + 10, y + height - 150))

			if buff.effect < 1:
				effect = f"Aumento : {int(buff.effect*100)}%"
			else:
				effect = f"Aumento : {str(buff.effect)}"

			effect_surface = effect_font.render(effect, True, (210,0,0))
			screen.blit(effect_surface, (x + 10, y + height - 100))

		pygame.display.flip()
		return buff_rects

	def choose_buff(self, player, screen, card_size):
		total = player.level - player.ant_level

		while total > 0:
			self.create_buffs()
			chose = False
			buff_rects = self.display_buffs(screen, card_size, player.level)
			while True:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						return (False, False)

					if event.type == pygame.MOUSEBUTTONDOWN:
						if event.button == 1:
							mouse_pos = event.pos

							for buff, rect, in buff_rects:
								if rect.collidepoint(mouse_pos):
									buff.apply(player)

									total -= 1
									chose = True
									break
					if chose:
						break
				if chose:
					break
									
		return (True, False)


