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

class GameManager:
	"""
	Classe responsável por gerenciar o estado principal do jogo, incluindo lógica, renderização, 
	eventos e interação com o jogador e inimigos.
	"""
	
	def __init__(self, game, screen_game) -> None:
		"""
		Inicializa o gerenciador do jogo com seus componentes principais.

		Parâmetros
		----------
		game : objeto do jogo
			Referência ao jogo principal.
		screen_game : pygame.Surface
			Superfície onde o jogo será renderizado.
		"""

		pygame.init()

		self.screen = screen_game
		self.mapa1 = Map(False)

		# A tela
		self.keys_collected = 0
		self.width = SCREEN_SIZE[0]
		self.height = SCREEN_SIZE[1]

		pygame.mixer.set_num_channels(16)
		self.background_music = BACKGROUND_MUSIC
		self.death_music = pygame.mixer.Sound(DEATH_MUSIC)
		self.death_played = False
		self.death_channel = pygame.mixer.Channel(0)

		self.font = pygame.font.Font(None, 36) # tamanho 36

		self.plataforms, self.standing_plataforms = self.mapa1.give_plataforms(0, False)
		self.extend = False

		# player
		self.player = player.Player(PLAYER_SPAWN[0], PLAYER_SPAWN[1])
		self.lifebar_player = Life.LifeBar(self.player, "player")
		self.expbar_player = Life.ExpBar(self.player)	

		self.clock = None
		self.is_running = False

		self.camera_speed = CAMERA_SPEED
		self.shoot_speed = SHOOT_SPEED
		self.spawn_speed = SPAWN_SPEED
		self.changed_speed = False

		self.camera_offset = [0, 0]

		self.enemies = liben.Enemies()

		self.buffs = buffs.Buffs()

		self.buff_paused = False
		self.paused = True

		self.lifebar_boss = None

		# alguns atributos de tempo
		self.delta = DELTA_GAME
		self.time_map = 0
		self.time_shoot_enemy = 0 
		self.time_enemy_spawn = 0

	### essa função deve ser retirada
	def initalize_game(self):
		""" inicializa os componentes"""
		self.clock = pygame.time.Clock()
		self.is_running = True

		pygame.mixer.music.load(self.background_music)
		pygame.mixer.music.play(loops = -1)

	def update_timers(self):
		"""
		Atualiza os temporizadores do jogo.
		"""
		self.time_shoot_enemy += self.delta
		self.time_map += self.delta
		self.time_enemy_spawn += self.delta	
		#print(f"A trindade do tempo é {self.time_shoot_enemy, self.time_map, self.time_enemy_spawn}")
		# a += self.delta
		# b += self.delta
		# c += self.delta
		# return a, b, c

	def run(self):
		# Inicializa o jogo
		self.initalize_game()

		while self.is_running:   
			self.clock.tick(60)

			self.update_timers()
			self.handle_events()
			self.update_logic()
			self.render()

		pygame.quit()
	
	def render(self):
		self.event2()
		self.draw()
		self.update()

	def handle_events(self):
		"""
		Gerencia eventos do jogo, como morte do jogador ou escolha de buffs.
		"""
	
		if not self.player.alive:
			pygame.mixer.music.stop()
			if not self.death_channel.get_busy() and not self.death_played:
				self.death_channel.play(self.death_music)
				self.death_played = True
		
		if self.buff_paused:
			self.is_running, self.buff_paused = self.buffs.choose_buff(self.player, self.screen, (200,500), pygame.mouse)

	def update_logic(self):
		"""
		Atualiza a lógica do jogo, incluindo movimentação do mapa e comportamento dos inimigos.
		"""
		if self.time_map >= self.camera_speed:
			self.extend = self.mapa1.move_map(self.plataforms)
			self.time_map = 0

		if self.mapa1.floor % 4 == 0 and not self.changed_speed:
			self.spawn_speed -= 0.1 * self.spawn_speed
			self.changed_speed = True
		elif self.mapa1.floor % 4 != 0 and self.changed_speed:
			self.changed_speed = False

		if self.time_enemy_spawn >= self.spawn_speed and not self.enemies.boss:
			self.enemies.create_random_enemies(self.standing_plataforms, self.mapa1.floor)
			self.time_enemy_spawn = 0

		if self.time_shoot_enemy >= self.shoot_speed:
			self.enemies.shoot_attack(self.player, self.plataforms, self.screen)
			self.time_shoot_enemy = 0

		if self.lifebar_boss:
			self.lifebar_boss.update()
			self.time_enemy_spawn = 0

	def event(self, event):
		"""
		Processa eventos de entrada, como moviemntos do player.
		"""
		self.player.on_event(event, pygame.mouse)

	def on_key_pressed(self):
		"""
		Processa teclas pressionadas para controlar o player
		"""
		key_map = pygame.key.get_pressed()
		self.player.on_key_pressed(key_map)

	def verify_death(self, change_state):
		"""
		Verifica se o player morreu e altera o estado do jogo para "game_over"
		"""

		if self.death_played:
			change_state("game_over")

	def verify_win(self, change_state):
		"""
		Verifica se o player venceu (coletando a chave) e altera o estado do jogo para game_win
		"""
		if self.keys_collected == 3:
			change_state("game_win")
			self.keys_collected = 0

	def update(self):
		"""
		Atualiza o estado do player, inimigos e barras de saúde e experiência
		"""
		self.player.update(self.plataforms, self.enemies)
		self.enemies.update(self.plataforms, self.player, self.enemies, pygame.time, self.screen)
		self.lifebar_player.update()
		self.expbar_player.update()

		if self.lifebar_player:
			self.lifebar_player.life_bar_health_draw(self.screen)

		if self.expbar_player:
			self.expbar_player.exp_bar_draw(self.screen)

		if self.lifebar_boss:
			self.lifebar_boss.life_bar_health_draw(self.screen)

		if not self.enemies.boss:
			self.lifebar_boss = None

		if self.extend:
			self.plataforms, self.standing_plataforms, lifebar_boss = self.mapa1.extend_map(self.enemies, self.plataforms, self.standing_plataforms)
			if not self.lifebar_boss:
				self.lifebar_boss = lifebar_boss

		if self.player.level_up():
			self.buff_paused = True

		if self.enemies.key.check_collision(self.player):
			self.keys_collected += 1


	def draw(self):

		self.screen.fill((255, 255, 255))
		self.mapa1.draw_plataforms(self.screen, self.plataforms, self.height, self.camera_offset)
		self.player.draw(self.screen, self.delta, pygame.mouse.get_pos())

		self.player.bullets.shoot(self.screen, self.enemies, self.plataforms, self.player)

		self.enemies.load(self.screen)
		self.enemies.shoot_bullets(self.player, self.plataforms, self.screen)
		self.enemies.mov_attack(self.player, self.plataforms, self.screen)
		self.enemies.check_die(self.player)

		font_status = pygame.font.Font(None, 15)
		floor_text = f"Andar : {self.mapa1.floor - 1}"
		floor_surface = self.font.render(floor_text, True, (0,0,0))
		self.screen.blit(floor_surface, (10, 900))

		keys_text = f"Chaves: {self.keys_collected}"
		keys_surface = self.font.render(keys_text, True, (0, 0, 0))
		self.screen.blit(keys_surface, (self.width - 150, 100))

		self.lifebar_player.life_bar_health_draw(self.screen)
		self.expbar_player.exp_bar_draw(self.screen)
		if self.lifebar_boss:
			self.lifebar_boss.life_bar_health_draw(self.screen)