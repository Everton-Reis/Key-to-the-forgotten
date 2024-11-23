import pygame
import sys

sys.path.append("../../implementacoes/buffs")

import buffs

from mapa import Map

import player
import enemy as liben
import lifebar as Life

mapa1 = Map()

class GameManager:

	def __init__(self) -> None:
		pygame.init()

		# A tela
		self.width = 1200
		self.height = 1000
		screen_size = (self.width, self.height)
		self.screen = pygame.display.set_mode(screen_size)
		self.screen.fill((0, 0, 0))

		self.font = pygame.font.Font(None, 36) # tamanho 36

		# Objetos
		self.player = player.Player(self.width // 2, self.height // 2, 25, 25)
		self.lifebar_player = Life.LifeBar(self.player, self.screen)

		self.plataforms = mapa1.give_plataforms()
		self.standing_plataforms = mapa1.standing_plataforms

		self.clock = None
		self.is_running = False

		self.camera_speed = 10
		self.shoot_speed = 800

		self.camera_offset = [0, 0]

		self.enemies = liben.Enemies()

		self.buffs = buffs.Buffs()

		self.paused = False

	def run(self):
		# Inicializa o jogo
		self.clock = pygame.time.Clock()
		self.is_running = True

		time_map = 0
		time_shoot_enemy = 0

		while self.is_running:      
			delta = self.clock.tick(60)

			if self.paused:
				self.is_running, self.paused = self.buffs.choose_buff(self.player, self.screen, (200,500))


			self.event()
			self.update()
			self.lifebar_player.update()
			self.draw()
		pygame.quit()

	def update_camera(self):
		self.camera_offset[0] = self.player.rect.centerx - self.width // 2
		self.camera_offset[1] = min(self.player.rect.centery - self.height //2, self.height - 100)

	def event(self):
		# Eventos
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				self.is_running = False

			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 3:
					self.paused = True
					self.buffs.create_buffs()

			self.player.on_event(event, pygame.mouse)



		# Chaves pressionadas no momento
		key_map = pygame.key.get_pressed()
		self.player.on_key_pressed(key_map)

	def update(self):
		self.player.update(self.plataforms, None)
		self.update_camera()

	def draw(self):
		# Renderizaçao
		self.screen.fill((255, 255, 255))
		self.player.draw(self.screen)

		self.player.bullets.shoot(self.screen, self.enemies.enemies, self.plataforms, self.player)

		mapa1.draw_plataforms(self.screen, self.plataforms, self.height, self.camera_offset)

		font_status = pygame.font.Font(None, 15)


		self.lifebar_player.life_bar_health()

		pygame.display.flip()

if __name__ == '__main__':
	game = GameManager()
	game.run()