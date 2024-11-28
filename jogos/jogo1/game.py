import pygame
import sys

sys.path.append("../../implementacoes/atirar")
sys.path.append("../../implementacoes/inimigos")
sys.path.append("../../implementacoes/player")
sys.path.append("../../implementacoes/lifebar")

import mapa
import player1_0 as player
import enemy3_0 as liben
import lifebar1_0 as Life

from mapa import BLOCK_SPEED

mapa1 = mapa.Map()

class Key():
	def __init__(self, number_enemys, pos):
		self.number_enemys = number_enemys

class GameManager:

	def __init__(self) -> None:
		pygame.init()

		self.keys_collected = 0
		# A tela
		self.width = 1200
		self.height = 1000
		screen_size = (self.width, self.height)
		self.screen = pygame.display.set_mode(screen_size)
		self.screen.fill((0, 0, 0))

		self.font = pygame.font.Font(None, 36) # tamanho 36

		# Objetos
		self.player = player.Player(self.width // 2, self.height // 2, 25, 25, "../../sprites/weapon.png")
		self.lifebar = Life.LifeBar(self.player, self.screen)

		self.plataforms, self.standing_plataforms = mapa1.give_plataforms()

		self.clock = None
		self.is_running = False

		self.camera_speed = 50
		self.shoot_speed = 500

		self.camera_offset = [0, 0]

		self.enemies = liben.Enemies()

	def run(self):
		# Inicializa o jogo
		self.clock = pygame.time.Clock()
		self.is_running = True

		time_map = 0
		time_shoot_enemy = 0

		self.enemies.create_random_enemies(self.standing_plataforms, 5)

		while self.is_running:      
			delta = self.clock.tick()
			time_map += delta
			time_shoot_enemy += delta

			if time_map >= self.camera_speed:
				mapa1.move_map(self.plataforms)
				time_map = 0

			if time_shoot_enemy >= self.shoot_speed:
				self.enemies.shoot_attack(self.player, self.plataforms, self.screen)
				time_shoot_enemy = 0

			self.event()
			self.update()
			self.lifebar.update()
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
			self.player.on_event(event, pygame.mouse)

		# Chaves pressionadas no momento
		key_map = pygame.key.get_pressed()
		self.player.on_key_pressed(key_map)

	def update(self):
		self.player.update(self.plataforms, self.enemies)
		self.enemies.update(self.plataforms, self.player, self.enemies)

		if self.enemies.key.check_collision(self.player):
			self.keys_collected += 1

		self.update_camera()

	def draw(self):
		# Renderizaçao
		self.screen.fill((255, 255, 255))
		mapa1.draw_background(self.screen)
		self.player.draw(self.screen, pygame.mouse.get_pos())
		self.player.bullets.shoot(self.screen, self.enemies.enemies, self.plataforms, self.player)
		self.enemies.load(self.screen)
		self.enemies.shoot_bullets(self.player, self.plataforms, self.screen)
		self.enemies.mov_attack(self.player, self.plataforms)
		self.enemies.check_die()

		mapa1.draw_plataforms(self.screen, self.plataforms, self.height, self.camera_offset)

		coords_text = f"Posição do jogador: ({self.player.rect.x}, {self.player.rect.y})"
		coords_surface = self.font.render(coords_text, True, (255, 255, 0))  # Texto na cor preta
		self.screen.blit(coords_surface, (10, 10))  # Desenha no canto superior esquerdo da tela

		keys_text = f"Chaves: {self.keys_collected}"
		keys_surface = self.font.render(keys_text, True, (0, 0, 0))
		self.screen.blit(keys_surface, (self.width - 150, 10))

		self.lifebar.life_bar_health()

		pygame.display.flip()

if __name__ == '__main__':
	game = GameManager()
	game.run()