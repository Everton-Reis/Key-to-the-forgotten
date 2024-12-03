import pygame
import bullets as libat
import enemy as liben
import math
import weapon as wp
import sys
import sprites

sys.path.append("../")

from gamesettings import *

class Player:

	def __init__(self, x, y):
		"""
		Inicializa um objeto da classe Player.

		Parâmetros
		----------
		x : float
			posição horizontal
		y : float
			posição vertical
		"""
		self.idle_sprites = sprites.cut_sheet(PLAYER_IDLE_SPRITE, 4, 1, 2)
		self.run_sprites = sprites.cut_sheet(PLAYER_RUN_SPRITE, 6, 1 ,2)
		self.jump_sprites = sprites.cut_sheet(PLAYER_JUMP_SPRITE, 1, 1, 2)
		self.rect = self.idle_sprites[0].get_rect()
		self.rect = sprites.cut_transparent_rect(self.idle_sprites[0])
		self.rect.center = (x, y)

		# nao gostei de ter um som correndo, mas tá aí
		# só descomentar isso aqui e o codigo em collide()
		# self.run_sfx = pygame.mixer.Sound(PLAYER_RUN_SFX)
		# self.run_sfx.set_volume(0.2)
		# self.run_channel = pygame.mixer.Channel(1)

		self.level_sfx = pygame.mixer.Sound(PLAYER_LEVEL_SFX)

		self.jump_sfx = pygame.mixer.Sound(PLAYER_JUMP_SFX)
		self.jump_sfx.set_volume(0.2)
		self.jump_channel = pygame.mixer.Channel(2)

		self.attack_sfx = pygame.mixer.Sound(PLAYER_ATTACK_SFX)
		self.attack_sfx.set_volume(0.3)
		self.attack_channel = pygame.mixer.Channel(3)

		self.death_sfx = pygame.mixer.Sound(PLAYER_DEATH_SFX)
		self.death_sfx.set_volume(0.7)
		self.death_channel = pygame.mixer.Channel(4)

		self.get_sfx = pygame.mixer.Sound(PLAYER_GET_SFX)
		self.get_sfx.set_volume(0.4)
		self.get_channel = pygame.mixer.Channel(5)

		self.idle_time = 0
		self.idle_current_sprite = 0
		self.idle_frame_rate = 10

		self.run_time = 0
		self.run_current_sprite = 0
		self.run_frame_rate = 10

		self.gravity_y = 0.6 # pixels^2 / frame
		self.speed_y = 0
		self.jump_count = 0
		self.dash_count = 0

		self.direction = 0

		self.total_exp = 0
		self.next_level = 100
		self.ant_level = 0
		self.level = 1


		self.health = PLAYER_INITIAL_HEALTH
		self.speed_x = PLAYER_INITIAL_SPEED
		self.MAX_HEALTH = PLAYER_INITIAL_MAX_HEALTH
		self.damage = PLAYER_INITIAL_DAMAGE
		self.dash = PLAYER_INITIAL_DASH
		self.shoot = PLAYER_INITIAL_SHOOT
		self.ls = PLAYER_INITIAL_LS


		self.jump_count_max = 4
		self.alive = True

		self.font = pygame.font.Font(None, 20)

		self.dx = 0
		self.dy = 0

		self.on_ground = 0

		self.bullets = libat.Bullets()

		self.weapon = wp.Weapon(self, PLAYER_WEAPON_SPRITE, PLAYER_WEAPON_SIZE)
		self.weapon_image = PLAYER_WEAPON_SPRITE
		self.weapon.create_weapon()

	def calc_next_level(self, total) -> float:
		"""
		Cálcula o xp necessário para o próximo nível baseado na razão de level up.

		Parâmetros
		----------
		total: float
			Níveis upados.
		"""
		for _ in range(total):
			self.next_level += PLAYER_LEVEL_MULTIPLIER*self.next_level

	def calc_exp(self, level) -> float:
		"""
		Cálculo o xp associado ao nível desejado.

		Parâmetros
		----------
		level: int
			Nível desejado.
		"""
		if level == 0:
			return 0
		if level == 1:
			return PLAYER_INITIAL_NEXT_LEVEL

		exp = PLAYER_INITIAL_NEXT_LEVEL
		return exp * ((PLAYER_LEVEL_MULTIPLIER + 1) ** (level - 2))

	def level_up(self):
		"""
		Upa de nível.
		"""
		if not self.alive:
			return

		if self.total_exp >= self.next_level:
			total = int(self.total_exp // self.next_level)
			self.ant_level = self.level
			self.level += total
			self.calc_next_level(total)
			self.MAX_HEALTH += 0.05 * self.MAX_HEALTH
			self.health = self.MAX_HEALTH
			self.damage += 0.05 * self.damage
			self.level_sfx.play()
			return True

	def draw_status(self, screen) -> None:
		"""
		Desenha na tela os status do player.

		Parâmetros
		----------
		screen : tela de pygame
		"""
		damage_text = f"Dano : {self.damage:.2f}"
		health_text = f"Vida máxima : {self.MAX_HEALTH:.2f}"
		h_text = f"Vida : {self.health:.2f}"
		speed_text = f"Velocidade : {self.speed_x:.2f}"
		jump_text = f"Pulos : {self.jump_count_max}"
		dash_text = f"Dash : {self.dash}"
		shoot_text = f"Tiros : {self.shoot}"
		ls_text = f"Roubo de vida : {self.ls:.2f}"
		level_text = f"Nível : {self.level}"
		exp_text = f"Total xp : {self.total_exp:.2f}"
		next_level_text = f"Próximo nível : {self.next_level:.2f}"


		damage_surface = self.font.render(damage_text, True, (0,0,0))
		screen.blit(damage_surface, (10, 200))
		health_surface = self.font.render(health_text, True, (0,0,0))
		screen.blit(health_surface, (10, 250))
		h_surface = self.font.render(h_text, True, (0,0,0))
		screen.blit(h_surface, (10,300))
		speed_surface = self.font.render(speed_text, True, (0,0,0))
		screen.blit(speed_surface, (10, 350))
		jump_surface = self.font.render(jump_text, True, (0,0,0))
		screen.blit(jump_surface, (10, 400))
		dash_surface = self.font.render(dash_text, True, (0,0,0))
		screen.blit(dash_surface, (10, 450))
		shoot_surface = self.font.render(shoot_text, True, (0,0,0))
		screen.blit(shoot_surface, (10, 500))
		ls_surface = self.font.render(ls_text, True, (0,0,0))
		screen.blit(ls_surface, (10, 550))
		level_surface = self.font.render(level_text, True, (0,0,0))
		screen.blit(level_surface, (10, 600))
		exp_surface = self.font.render(exp_text, True, (0,0,0))
		screen.blit(exp_surface, (10, 650))
		next_level_surface = self.font.render(next_level_text, True, (0,0,0))
		screen.blit(next_level_surface, (10, 700))

	def life_steal(self, enemy):
		"""
		Aplica roubo de vida.

		Parâmetros
		----------
		enemy : objeto inimigo
			Inimigo a ter a vida roubada.
		"""
		if enemy.health > 0 and self.health < self.MAX_HEALTH:
			delta = self.health + self.ls * 0.5*self.damage
			if delta >= self.MAX_HEALTH:
				self.health = self.MAX_HEALTH
			else:
				self.health = delta


	def draw(self, screen, delta, mouse = None) -> None:
		"""
		Responsável por desenhar e carregar sprites.

		Parâmetros
		----------
		screen: tela de pygame

		delta: int
			Intervalo de tempo do jogo.

		mouse: mouse de pygame
		"""
		if not self.alive:
			return

		# pygame.draw.rect(screen, (10,10,10), self.rect)
		sprites.load_sprites_player(self, delta, screen)
		self.draw_status(screen)

		if self.weapon_image and mouse:
			self.weapon.point_mouse(mouse, screen)

	def collide(self, plataforms, enemies) -> None:
		"""
		Responsável pela lógica de colisão entre objetos.

		Parâmetros
		----------
		plataforms: list(retângulo de pygame)
			Lista contendo as plataformas colidíveis do jogo.

		enemies: list(objeto inimigo)
			Lista contendo os inimigos colidíveis do jogo.
		"""

		if not self.rect:
			return

		ver_colis = False
		if len(plataforms) > 0:
			self.on_ground = False

			for plataform in plataforms:
				if self.rect.colliderect(plataform):
					#indica se o player está acima ou abaixo da plataforma
					delta_y = self.rect.centery - plataform.centery
					#distancia maxima pra haver colisão
					overlap_y = self.rect.height / 2 + plataform.height / 2

					if self.speed_y > 0 and delta_y < 0:
						if abs(delta_y) <= overlap_y:
							self.rect.bottom = plataform.top
							self.speed_y = 0
							self.on_ground = True
							self.jump_count = 0
							self.dash_count = 0
					elif self.speed_y < 0 and delta_y > 0:
						if abs(delta_y) <= overlap_y:
							ver_colis = True
							self.rect.top = plataform.bottom
							self.speed_y = 0

		if enemies and len(enemies.enemies) > 0:
			for enemy in enemies.enemies:
				if self.rect.colliderect(enemy.rect):

					if self.speed_y > 0:
						self.rect.bottom = enemy.rect.top
						self.speed_y = 0
						self.jump_count = 0
						self.dash_count = 0
					elif self.speed_y < 0:
						self.rect.top = enemy.rect.bottom
						self.speed_y = 0  
						self.dash_count = 0     

		self.rect.x += self.dx

		# if self.dx != 0:
		# 	if not self.run_channel.get_busy():
		# 		self.run_channel.play(self.run_sfx, loops = -1)

		# if self.dx == 0:
		# 	if self.run_channel.get_busy():
		# 		self.run_channel.stop()



		if len(plataforms) > 0:
			for plataform in plataforms:
				if self.rect.colliderect(plataform):
					delta_x = self.rect.centerx - plataform.centerx
					#distancia maxima pra haver colisão
					overlap_x = self.rect.width // 2 + plataform.width // 2
					delta_y = self.rect.centery - plataform.centery
					overlap_y = self.rect.height / 2 + plataform.height / 2

					# o problema principal desse algoritmo é, na medida em que
					# block_speed aumenta, não conseguir diferenciar dentre dois tipos de colisões
					# verticais que acabam atrapalhando as horizontais:
					# 1° -> o player colide enquanto está embaixo da plataforma
					# 2° -> o player colide horizontalmente enquanto cai (speed_y > 0)
					# quando block_speed aumenta (de 1 para 2 já é possivel notar)
					# essas duas colisões se tornam a mesma colisão pois na 2°,
					# enquanto o player colide horizontalmente, ele vai acabar ficando
					# embaixo da plataforma por estar caindo + a plataforma estar se movendo para baixo
					# por isso tentei encontrar uma tolerancia para a colisão vertical
					# de forma que a horizontal possa acontecer

					# achei essa tolerancia percebendo que abs(delta_y) parece assumir um
					# valor minimo quando o player colide verticalmente e está embaixo da plataforma,
					# onde esse valor minímo parece ser aproximadamente overlap_y - n*BLOCK_SPEED
					# onde n depende de BLOCK_SPEED
					# n = 2 funciona muito bem para speed < 4, mas para maiores velocidades
					# um novo numero de ser encontrado
					# para encontrar o valor exato seria preciso talvez considerar o fps do jogo,
					# e o tamanho dos objetos colidindo de uma forma mais complicada
					# essa tolerancia faz com que a 1° colisão se distingua da 2°

					# enquanto um melhor algoritmo de colisão não é implementado, esse deve servir

					# não sei se compensa adicionar o mesmo algoritmo para os inimigos-plataformas e
					# inimigos-inimigos, pois a colisão entre eles não acontece de forma tão complexa,
					# e por mais que aconteça eventualmente de um inimigo acabar subindo em cima do outro,
					# por opinião pessoal, isso não deveria estragar a experiência do jogo

					# descomente a linha print(abs(delta_y), overlap_y - tolerancia) para ver os valores

					tolerancia = 2*BLOCK_SPEED

					if self.speed_y > 0 and delta_y > 0:
						# print(abs(delta_y), overlap_y - tolerancia)
						if abs(delta_y) >= overlap_y - tolerancia:
							ver_colis = True

					if not ver_colis:
						if self.dx > 0 and delta_x < 0:
							if abs(delta_x) <= overlap_x:
								self.rect.right = plataform.left
								self.dx = 0
						elif self.dx < 0 and delta_x > 0:
							if abs(delta_x) <= overlap_x:
								self.rect.left = plataform.right
								self.dx = 0	


		if enemies and len(enemies.enemies) > 0:
			for enemy in enemies.enemies:
				if self.rect.colliderect(enemy.rect):
					if self.dx > 0:
						self.rect.right = enemy.rect.left
					if self.dx < 0:
						self.rect.left = enemy.rect.right

	def update(self, plataforms, enemies) -> None:
		"""
		Responsável por aplicar a gravidade, chamar collide() e matar o jogador.

		Parâmetros
		----------
		plataforms: list(retângulo de pygame)
			Lista contendo as plataformas colidíveis do jogo.

		enemies: list(objeto inimigo)
			Lista contendo os inimigos colidíveis do jogo.
		"""
		if not self.alive:
			self.health = 0

			# if self.run_channel.get_busy():
			# 	self.run_channel.stop()

			return

		self.speed_y += self.gravity_y
		self.rect.y += self.speed_y
		self.die()

		self.collide(plataforms, enemies)

		self.dx = 0
		self.dy = 0

	def _dash(self, mouse) -> None:
		"""
		Aplica dash ao jogador.

		Parâmetros
		----------
		mouse: mouse de pygame
		"""
		if self.dash <= 0 or self.dash_count >= self.dash:
			return

		mouse_pos = mouse.get_pos()
		dash_distance = 150

		dx = mouse_pos[0] - self.rect.center[0]
		dy = mouse_pos[1] - self.rect.center[1]

		distance = math.sqrt(dx ** 2 + dy ** 2)

		if distance == 0:
			return

		direction_x = dx / distance
		direction_y = dy / distance

		self.rect.x += direction_x * dash_distance
		self.rect.y += direction_y * dash_distance

		self.dash_count += 1


	def on_event(self, event: pygame.event.Event, mouse) -> None:
		"""
		Responsável por chamar funções a medida que eventos acontecem no jogo.

		Parâmetros:
		event: evento de pygame

		mouse: mouse de pygame
		"""
		if not self.alive:
			return

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				self._jump()
		
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				self.attack_channel.play(self.attack_sfx)
				
				bullet = libat.Bullet((self.rect.x + (self.rect.width // 2), self.rect.y + (self.rect.height // 2)), 
									  (mouse.get_pos()[0], mouse.get_pos()[1]),
									  self.damage, PLAYER_BULLET_SPRITE)
				bullet.shooted = True
				self.bullets.bullets.append(bullet)

				if self.shoot > 0:
					distance = 50

					for i in range(self.shoot):
						extra_bullet = libat.Bullet((self.rect.x + (self.rect.width // 2), self.rect.y + (self.rect.height //2)),
										(mouse.get_pos()[0] + (i+1) * distance, mouse.get_pos()[1]),
										self.damage // self.shoot, PLAYER_BULLET_SPRITE)
						extra_bullet.shooted = True
						self.bullets.bullets.append(extra_bullet)

			if event.button == 3:
				self._dash(mouse)
		
	def _jump(self) -> None:
		"""
		Aplica pulo ao jogador.
		"""
		if self.jump_count >= self.jump_count_max:
			return
		self.jump_channel.play(self.jump_sfx)
		self.speed_y = -10
		self.jump_count += 1

	def on_key_pressed(self, key_map) -> None:
		"""
		Responsável por fazer o player se mover.

		Parâmetros
		----------
		key_map: list(key de pygame)
		"""
		if not self.alive:
			return

		if key_map[pygame.K_d]:
			self.dx = self.speed_x
			self.direction = 0
		elif key_map[pygame.K_a]:
			self.dx = - self.speed_x
			self.direction = 1

	def decrement_health(self, howmuch) -> None:
		"""
		Reduz a vida do jogador.

		Parâmetros
		----------
		howmuch: float
			Quanto a se retirar da vida atual do jogador.
		"""
		self.health -= howmuch
		self.get_channel.play(self.get_sfx)
		self.die()

	def increment_health(self, howmuch) -> None:
		"""
		Aumenta a vida do jogador.

		Parâmetros
		----------
		howmuch: float
			Quanto a se aumentar da vida atual do jogador.
		"""
		self.health += howmuch
		if self.health >= self.MAX_HEALTH:
			self.health = self.MAX_HEALTH

	def die(self) -> None:
		"""
		Mata o jogador.
		"""
		if self.health <= 0:
			self.rect = None
			self.alive = False
			self.death_channel.play(self.death_sfx)

		elif self.rect.y > 1000:
			self.rect = None
			self.alive = False
			self.death_channel.play(self.death_sfx)