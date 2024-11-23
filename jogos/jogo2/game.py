import pygame
import sys
import random

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
		self.player = player.Player(self.width // 2 + 200, self.height - 300, 25, 25)
		self.lifebar_player = Life.LifeBar(self.player, self.screen)

		self.plataforms, self.standing_plataforms = mapa1.give_plataforms(0, False)
		self.extend = False

		self.clock = None
		self.is_running = False

		self.camera_speed = 10
		self.shoot_speed = 800
		self.spawn_speed = 5000

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
		time_enemy_spawn = 0


		while self.is_running:      
			delta = self.clock.tick(200)
			time_shoot_enemy += delta
			time_map += delta
			time_enemy_spawn += delta


			if self.paused:
				self.is_running, self.paused = self.buffs.choose_buff(self.player, self.screen, (200,500))

			if time_enemy_spawn >= self.spawn_speed and not self.enemies.boss:
				self.enemies.create_random_enemies(self.standing_plataforms, random.randint(5,10))
				time_enemy_spawn = 0

			if time_shoot_enemy >= self.shoot_speed:
				self.enemies.shoot_attack(self.player, self.plataforms)
				time_shoot_enemy = 0

			if time_map >= self.camera_speed:
				self.extend = mapa1.move_map(self.plataforms)
				time_map = 0

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
				if event.button == 2:
					self.player.total_exp = self.player.next_level

			self.player.on_event(event, pygame.mouse)



		# Chaves pressionadas no momento
		key_map = pygame.key.get_pressed()
		self.player.on_key_pressed(key_map)

	def update(self):
		self.player.update(self.plataforms, self.enemies)
		self.enemies.update(self.plataforms, self.player, self.enemies, pygame.time)

		if self.player.level_up():
			self.paused = True

		self.update_camera()

	def draw(self):
		# Renderizaçao
		self.screen.fill((255, 255, 255))
		self.player.draw(self.screen)

		if self.enemies.boss:
			self.enemies.enemies = [self.enemies.boss] +  self.enemies.boss.enemies

		self.player.bullets.shoot(self.screen, self.enemies.enemies, self.plataforms, self.player)

		self.enemies.load(self.screen)
		self.enemies.shoot_bullets(self.player, self.plataforms, self.screen)
		self.enemies.mov_attack(self.player, self.plataforms)
		self.enemies.check_die(self.player)

		if self.extend:
			type = 1 if mapa1.floor < 1 else 2
			if not self.enemies.boss and type == 2:
				self.enemies.boss = liben.Boss(self.width // 2, 100, (100,100,100), 100,100)

			new_plataforms, new_standing_plataforms = mapa1.give_plataforms(type, True)
			self.plataforms = new_plataforms + self.plataforms
			self.standing_plataforms += new_standing_plataforms

		mapa1.draw_plataforms(self.screen, self.plataforms, self.height, self.camera_offset)

		font_status = pygame.font.Font(None, 15)
		self.lifebar_player.life_bar_health()
		floor_text = f"Andar : {mapa1.floor}"
		floor_surface = self.font.render(floor_text, True, (0,0,0))
		self.screen.blit(floor_surface, (10, 900))


		pygame.display.flip()

if __name__ == '__main__':
	game = GameManager()
	game.run()