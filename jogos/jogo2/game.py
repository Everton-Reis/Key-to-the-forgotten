import pygame
import sys
import random

sys.path.append("../../implementacoes/buffs")

import buffs

from mapa import Map

import player
import enemy as liben
import bars as Life

from gamesettings import *

mapa1 = Map(False)

class Key():
	def __init__(self, number_enemys, pos):
		self.number_enemys = number_enemys

class GameManager:

	def __init__(self) -> None:
		pygame.init()

		# A tela
		self.keys_collected = 0
		self.width = SCREEN_SIZE[0]
		self.height = SCREEN_SIZE[1]
		screen_size = (self.width, self.height)
		self.screen = pygame.display.set_mode(screen_size)
		self.screen.fill((0, 0, 0))

		self.font = pygame.font.Font(None, 36) # tamanho 36

		# Objetos
		self.player = player.Player(PLAYER_SPAWN[0], PLAYER_SPAWN[1])
		self.lifebar_player = Life.LifeBar(self.player, "player", self.screen)
		self.expbar_player = Life.ExpBar(self.player, self.screen)

		self.plataforms, self.standing_plataforms = mapa1.give_plataforms(0, False)
		self.extend = False

		self.clock = None
		self.is_running = False

		self.camera_speed = CAMERA_SPEED
		self.shoot_speed = SHOOT_SPEED
		self.spawn_speed = SPAWN_SPEED

		self.camera_offset = [0, 0]

		self.enemies = liben.Enemies()

		self.buffs = buffs.Buffs()

		self.buff_paused = False
		self.paused = True

		self.lifebar_boss = None

	def run(self):
		# Inicializa o jogo
		self.clock = pygame.time.Clock()
		self.is_running = True

		time_map = 0
		time_shoot_enemy = 0
		time_enemy_spawn = 0

		while self.is_running:      
			delta = 50
			time_shoot_enemy += delta
			time_map += delta
			time_enemy_spawn += delta

			if self.buff_paused:
				self.is_running, self.buff_paused = self.buffs.choose_buff(self.player, self.screen, (200,500))

			if time_map >= self.camera_speed:
				self.extend = mapa1.move_map(self.plataforms)
				time_map = 0

			if time_enemy_spawn >= self.spawn_speed and not self.enemies.boss:
				self.enemies.create_random_enemies(self.standing_plataforms, mapa1.floor)
				time_enemy_spawn = 0

			if time_shoot_enemy >= self.shoot_speed:
				self.enemies.shoot_attack(self.player, self.plataforms, self.screen)
				time_shoot_enemy = 0


			self.event()
			self.lifebar_player.update()
			self.expbar_player.update()
			self.draw(delta)
			self.update()

			if self.lifebar_boss:
				self.lifebar_boss.update()
				time_enemy_spawn = 0

		pygame.quit()

	def event(self):
		# Eventos
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				self.is_running = False

			"""
			if event.type == pygame.MOUSEBUTTONDOWN:
				#pra debug
				if event.button == 2:
					self.player.total_exp = self.player.next_level
			"""

			self.player.on_event(event, pygame.mouse)


		# Chaves pressionadas no momento
		key_map = pygame.key.get_pressed()
		self.player.on_key_pressed(key_map)


	def update(self):
		self.player.update(self.plataforms, self.enemies)
		self.enemies.update(self.plataforms, self.player, self.enemies, pygame.time, self.screen)

		if not self.enemies.boss:
			self.lifebar_boss = None

		if self.extend:
			self.plataforms, self.standing_plataforms, self.lifebar_boss = mapa1.extend_map(self.enemies, self.plataforms, self.standing_plataforms, self.screen)

		if self.player.level_up():
			self.buff_paused = True

		if self.enemies.key.check_collision(self.player):
			self.keys_collected += 1


	def draw(self, delta):
		# Renderizaçao
		self.screen.fill((255, 255, 255))
		self.player.draw(self.screen, delta, pygame.mouse.get_pos())

		self.player.bullets.shoot(self.screen, self.enemies, self.plataforms, self.player)

		self.enemies.load(self.screen)
		self.enemies.shoot_bullets(self.player, self.plataforms, self.screen)
		self.enemies.mov_attack(self.player, self.plataforms, self.screen)
		self.enemies.check_die(self.player)

		mapa1.draw_plataforms(self.screen, self.plataforms, self.height, self.camera_offset)

		font_status = pygame.font.Font(None, 15)
		floor_text = f"Andar : {mapa1.floor}"
		floor_surface = self.font.render(floor_text, True, (0,0,0))
		self.screen.blit(floor_surface, (10, 900))

		keys_text = f"Chaves: {self.keys_collected}"
		keys_surface = self.font.render(keys_text, True, (0, 0, 0))
		self.screen.blit(keys_surface, (self.width - 150, 10))

		if self.lifebar_player:
			self.lifebar_player.life_bar_health()

		if self.expbar_player:
			self.expbar_player.exp_bar()

		if self.lifebar_boss:
			self.lifebar_boss.life_bar_health()

		pygame.display.flip()

if __name__ == '__main__':
	game = GameManager()
	game.run()