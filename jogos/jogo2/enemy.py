import pygame
import random
import math
import sys
import sprites
from abc import ABC, abstractmethod

sys.path.append("../")

from gamesettings import *

#sys.path.append('../atirar')

import bullets as libat
import player

class BaseEnemy(ABC):

	def __init__(self, x, y):
		self.delta = DELTA_GAME
		self.health = 10
		self.speed = 0
		self.damage = 0
		self.alive = True
		self.killed_by_player = False
		self.xp = 0

		self.death_time = 0
		self.attack_time = 0
		self.idle_time = 0

		self.last_direction_player = 0
		self.lost_player_timer = 0
		self.seeingplayer = False
		self.direction = 0
		self.timer = random.randint(50,100)
		self.roaming = True
		self.max_timer = self.timer
		self.sight_radius = 0

		self.gravity_y = 0.5
		self.speed_y = 0
		self.dx = 0
		self.dy = 0

	def invert_direction(self):
		if self.direction == 0: #direita
			self.direction = 1
		elif self.direction == 1: #esquerda
			self.direction = 0


	def change_direction(self):
		self.direction = random.choice((0, 1))


	def collide(self, plataforms, player, enemies, screen):
		pass

	def update(self, plataforms, player, enemies, screen):
		pass


	@abstractmethod
	def load(self, screen):
		pass


	def decrement_health(self, howmuch):
		self.health -= howmuch
		self.die()


	def die(self):
		if self.health <= 0:
			self.killed_by_player = True
			self.alive = False

			if self.death_time == 0:
				self.death_time += 1


		if self.rect.y > 1000:
			self.alive = False

			if self.death_time == 0:
				self.death_time += 1

	@abstractmethod
	def attack(self, player, screen):
		pass

	def roam(self):
		pass

	def chase(self, player):
		pass


	def can_see_player(self, playerpos, plataforms):
		dx = playerpos[0] - self.rect.center[0]
		dy = playerpos[1] - self.rect.center[1]
		distance = math.hypot(dx, dy)

		if distance > self.sight_radius:
			return False

		for plataform in plataforms:
			if plataform.clipline(self.rect.center, playerpos):
				return False

		return True

class MovingEnemy(BaseEnemy):
	def __init__(self, x, y):
		super().__init__(x,y)
		self.tomove = random.randint(10,50)
		self.max_tomove = self.tomove
		self.time_to_attack = 0
		self.max_time_to_attack = 1000

	def load(self, screen):
		if self.death_time > 0:
			sprites.load_sprites_enemy_death(self, self.delta, screen)
			return

		if not self.alive:
			return

		# pygame.draw.rect(screen, self.color, self.rect)
		if self.walk_time > 0 and self.attack_time == 0:
			sprites.load_sprites_enemy_walk(self, self.delta, screen)
		elif self.idle_time >= 0 and self.attack_time == 0:
			sprites.load_sprites_enemy_idle(self, self.delta, screen)
		elif self.attack_time > 0:
			sprites.load_sprites_enemy_attack(self, self.delta, screen)

	def chase(self, player):
		if self.seeingplayer:
			dx = self.rect.x - player.rect.x

			if dx > 0:
				self.dx -= self.speed
				self.last_direction_player = -1
				self.direction = 1
			elif dx < 0:
				self.dx += self.speed
				self.last_direction_player = 1
				self.direction = 0

			self.roaming = False
			self.lost_player_timer = 120
			self.timer = self.max_timer

		elif self.lost_player_timer > 0:
			self.dx = self.speed * self.last_direction_player
			self.lost_player_timer -= 1

		else:
			self.roaming = True
			self.dx = 0

	def collide(self, plataforms, player, enemies, screen):
		if enemies and len(enemies.enemies) > 0:
			for enemy in enemies.enemies:
				if enemy != self and self.rect.colliderect(enemy.rect):
					if self.speed_y > 0:
						self.rect.bottom = enemy.rect.top
						self.speed_y = 0
					elif self.speed_y < 0:
						self.rect.top = enemy.rect.bottom
						self.speed_y = 0

		if player and player.rect:
			if self.rect.colliderect(player.rect):
				if self.speed_y > 0 and player.rect:
					self.rect.bottom = player.rect.top
					self.attack(player, screen)
					self.speed_y = 0
				elif self.speed_y < 0 and player.rect:
					self.rect.top = player.rect.bottom

		if len(plataforms) > 0:
			for plataform in plataforms:
				if self.rect.colliderect(plataform):
					if self.speed_y > 0:
						self.rect.bottom = plataform.top
						self.speed_y = 0
					elif self.speed_y < 0:
						self.rect.top = plataform.bottom
						self.speed_y = 0

		self.rect.x += self.dx

		if self.walk_time == 0 and self.dx != 0:
			self.walk_time += 1

		if enemies and len(enemies.enemies) > 0:
			for enemy in enemies.enemies:
				if enemy != self and self.rect.colliderect(enemy.rect):
					if not self.seeingplayer:
						self.invert_direction()

					if self.dx > 0:
						self.rect.right = enemy.rect.left
					if self.dx < 0:
						self.rect.left = enemy.rect.right

		if player and player.rect:
			if self.rect.colliderect(player.rect):
				self.attack(player, screen)
				if self.dx > 0 and player.rect:
					self.rect.right = player.rect.left
				elif self.dx < 0 and player.rect:
					self.rect.left = player.rect.right

		if len(plataforms) > 0:
			for plataform in plataforms:
				if self.rect.colliderect(plataform):
					if self.dx > 0:
						self.rect.right = plataform.left
					if self.dx < 0:
						self.rect.left = plataform.right

					self.invert_direction()

	def update(self, plataforms, player, enemies, screen):
		if self.alive == False:
			return

		self.time_to_attack += self.delta

		if not self.seeingplayer:
			self.attack_time = 0

		self.speed_y += self.gravity_y
		self.rect.y += self.speed_y

		self.collide(plataforms, player, enemies, screen)

		self.die()

		self.dx = 0
		self.dy = 0


	def move(self, time = None):
		if self.tomove == 0:
			return

		if self.direction == 0:
			self.dx = self.speed

		if self.direction == 1:
			self.dx = -self.speed

		self.tomove -= self.speed


	def roam(self):
		if self.seeingplayer == True or self.roaming == False:
			return

		if self.tomove > 0:
			self.move()
			return

		self.timer -= 1
		if self.timer <= 0:
			action = random.choice([1,2])

			if action == 1:
				self.change_direction()
			elif action == 2:
				self.move()

			self.timer = self.max_timer
			self.tomove = self.max_tomove

	def attack(self, player, screen):
		if self.alive == False or self.time_to_attack < self.max_time_to_attack:
			return

		self.attack_time += 1
		self.time_to_attack = 0
		player.decrement_health(self.damage)

class WeakMovingEnemy(MovingEnemy):

	def __init__(self, x,y):
		super().__init__(x, y)
		self.idle_sprites = sprites.cut_sheet(WEAKMOV_IDLE_SPRITE, 7, 1, 1.5)
		self.attack_sprites = sprites.cut_sheet(WEAKMOV_ATTACK_SPRITE, 7, 1, 1.5)
		self.death_sprites = sprites.cut_sheet(WEAKMOV_DEATH_SPRITE, 3, 1, 1.5)
		self.walk_sprites = sprites.cut_sheet(WEAKMOV_WALK_SPRITE, 8, 1, 1.5)

		self.idle_x_0 = 0.8
		self.idle_y_0 = 0.9

		self.idle_x_1 = 1
		self.idle_y_1 = 0.9

		self.attack_x_0 = 0.8
		self.attack_y_0 = 0.9

		self.attack_x_1 = 1.05
		self.attack_y_1 = 0.9

		self.death_x = 0.8
		self.death_y = 0.9

		self.walk_x_0 = 0.9
		self.walk_y_0 = 0.9

		self.walk_x_1 = 0.9
		self.walk_y_1 = 0.9

		self.walk_time = 0
		self.walk_current_sprite = 0
		self.walk_frame_rate = 10

		self.idle_frame_rate = 10
		self.idle_current_sprite = 0

		self.attack_frame_rate = 50
		self.attack_current_sprite = 0

		self.death_frame_rate = 10
		self.death_current_sprite = 0

		self.rect = sprites.cut_transparent_rect(self.idle_sprites[0])
		self.rect.center = (x,y)

		self.health = WEAKMOV_INITIAL_HEALTH
		self.damage = WEAKMOV_INITIAL_DAMAGE
		self.speed = WEAKMOV_INITIAL_SPEED
		self.sight_radius = WEAKMOV_SIGHT_RADIUS
		self.xp = WEAKMOV_XP


class StrongMovingEnemy(MovingEnemy):

	def __init__(self, x,y):
		super().__init__(x,y)
		self.idle_sprites = sprites.cut_sheet(STRMOV_IDLE_SPRITE, 5, 1, 1.5)
		self.attack_sprites = sprites.cut_sheet(STRMOV_ATTACK_SPRITE, 6, 1, 1.5)
		self.death_sprites = sprites.cut_sheet(STRMOV_DEATH_SPRITE, 2, 1, 1.5)
		self.walk_sprites = sprites.cut_sheet(STRMOV_WALK_SPRITE, 9, 1, 1.5)

		self.idle_x_0 = 0.75
		self.idle_y_0 = 1.25

		self.idle_x_1 = 0.8
		self.idle_y_1 = 1.25

		self.attack_x_0 = 0.8
		self.attack_y_0 = 1.25

		self.attack_x_1 = 0.8
		self.attack_y_1 = 1.25

		self.death_x = 0.8
		self.death_y = 1.25

		self.walk_x_0 = 0.8
		self.walk_y_0 = 1.25

		self.walk_x_1 = 0.8
		self.walk_y_1 = 1.25

		self.walk_time = 0
		self.walk_current_sprite = 0
		self.walk_frame_rate = 10

		self.idle_frame_rate = 10
		self.idle_current_sprite = 0

		self.attack_frame_rate = 10
		self.attack_current_sprite = 0

		self.death_frame_rate = 10
		self.death_current_sprite = 0

		self.rect = sprites.cut_transparent_rect(self.idle_sprites[0])
		self.rect.center = (x,y)
		self.health = STRMOV_INITIAL_HEALTH
		self.damage = STRMOV_INITIAL_DAMAGE
		self.speed = STRMOV_INITIAL_SPEED
		self.sight_radius = STRMOV_SIGHT_RADIUS
		self.xp = STRMOV_XP

class ShootingEnemy(BaseEnemy):

	def __init__(self, x,y):
		super().__init__(x,y)
		self.idle_sprites = sprites.cut_sheet(SHOOT_ENEMIES_IDLE_SPRITE, 6, 1, 1.5)
		self.attack_sprites = sprites.cut_sheet(SHOOT_ENEMIES_ATTACK_SPRITE, 8, 1, 1.5)
		self.death_sprites = sprites.cut_sheet(SHOOT_ENEMIES_DEATH_SPRITE, 5, 1, 1.5)
		self.rect = sprites.cut_transparent_rect(self.idle_sprites[0])
		self.rect.center = (x, y)

		self.idle_x_0 = 2
		self.idle_y_0 = 1.2

		self.idle_x_1 = 2
		self.idle_y_1 = 1.2

		self.attack_x_0 = 2
		self.attack_y_0 = 1

		self.attack_x_1 = 2
		self.attack_y_1 = 1

		self.death_x = 2
		self.death_y = 1.1

		self.idle_current_sprite = 0
		self.idle_frame_rate = 10

		self.attack_current_sprite = 0
		self.attack_frame_rate = 10

		self.death_current_sprite = 0
		self.death_frame_rate = 5

		self.health = SHOOT_INITIAL_HEALTH
		self.damage = SHOOT_INITIAL_DAMAGE
		self.bullets = libat.Bullets()
		self.timer = SHOOT_TIMER
		self.max_timer = self.timer
		self.sight_radius = SHOOT_SIGHT_RADIUS
		self.xp = SHOOT_XP

	def roam(self):
		if self.seeingplayer == True or self.roaming == False:
			return

		self.timer -= 1
		if self.timer <= 0:
			self.change_direction()
			self.timer = self.max_timer

	def collide(self, plataforms, player, enemies = []):

		if len(plataforms) > 0:
			for plataform in plataforms:
				if self.rect.colliderect(plataform):
					if self.speed_y > 0:
						self.rect.bottom = plataform.top
						self.speed_y = 0
					elif self.speed_y < 0:
						self.rect.top = plataform.bottom
						self.speed_y = 0
		self.rect.x += self.dx
		for plataform in plataforms:
			if self.rect.colliderect(plataform):
				if self.dx > 0:
					self.rect.right = plataform.left
				if self.dx < 0:
					self.rect.left = plataform.right

				self.invert_direction()


	def update(self, plataforms, player, enemies = [], screen = None):
		if self.alive == False:
			return

		self.speed_y += self.gravity_y
		self.rect.y += self.speed_y


		self.collide(plataforms, player, enemies)

		self.die()
		self.dx = 0
		self.dy = 0


	def chase(self, player):
		if self.seeingplayer:
			dx = self.rect.x - player.rect.x

			if dx > 0:
				self.last_direction_player = -1
				self.direction = 1
			elif dx < 0:
				self.last_direction_player = 1
				self.direction = 0

			self.roaming = False
			self.lost_player_timer = 5
			self.timer = self.max_timer

		elif self.lost_player_timer > 0:
			if self.last_direction_player == 1:
				self.direction = 1
			elif self.last_direction_player == -1:
				self.direction = 0

			self.bullets.bullets.clear()
			self.lost_player_timer -= 1

		else:
			self.roaming = True
			self.dx = 0

	def load(self, screen):
		if self.death_time > 0:
			sprites.load_sprites_enemy_death(self, self.delta, screen)

		if not self.alive:
			return

		# pygame.draw.rect(screen, self.color, self.rect)
		if self.idle_time >= 0 and self.attack_time == 0:
			sprites.load_sprites_enemy_idle(self, self.delta, screen)
		elif self.attack_time > 0:
			sprites.load_sprites_enemy_attack(self, self.delta, screen)


	def attack(self, player, screen):
		if self.alive == False or \
		 self.roaming == True or \
		 self.seeingplayer == False or \
		 player.alive == False or \
		 self.attack_current_sprite != 0:
			return

		bullet = libat.Bullet((self.rect.center[0], self.rect.center[1]),
					(player.rect.center[0],
					 player.rect.center[1] + player.rect.height // 2),
						self.damage, (0,255,100), SHOOT_ENEMIES_BULLET_SPRITE)
		bullet.shooted = True
		self.attack_time += 1

		self.bullets.bullets.append(bullet)

class BossShootingEnemy(BaseEnemy):
	def __init__(self, x,y):
		super().__init__(x,y)
		self.idle_sprites = sprites.cut_sheet(BOSS_SHOOT_IDLE, 6, 1, 1.5)
		self.attack_sprites = sprites.cut_sheet(BOSS_SHOOT_SHOT, 8, 1, 1.5)
		self.death_sprites = sprites.cut_sheet(BOSS_SHOOT_DEAD, 5, 1, 1.5)

		sh_s = sprites.cut_sheet(SHOOT_ENEMIES_IDLE_SPRITE, 6, 1, 1.5)
		self.rect = sprites.cut_transparent_rect(sh_s[0])
		self.rect.center = (x, y)

		self.idle_x_0 = 2
		self.idle_y_0 = 1.1

		self.idle_x_1 = 2
		self.idle_y_1 = 1.1

		self.attack_x_0 = 2
		self.attack_y_0 = 0.9

		self.attack_x_1 = 2
		self.attack_y_1 = 0.9

		self.death_x = 2
		self.death_y = 1.1

		self.idle_current_sprite = 0
		self.idle_frame_rate = 10

		self.attack_current_sprite = 0
		self.attack_frame_rate = 10

		self.death_current_sprite = 0
		self.death_frame_rate = 10

		self.health = BOSS_SHOOT_INITIAL_HEALTH
		self.damage = BOSS_SHOOT_INITIAL_DAMAGE
		self.max_offset = BOSS_SHOOT_MAX_OFFSET
		self.seeingplayer = True
		self.roaming = False
		self.xp = BOSS_SHOOT_XP
		self.bullets = libat.Bullets()

	def load(self, screen):
		if self.death_time > 0:
			sprites.load_sprites_enemy_death(self, self.delta, screen)
			return

		if not self.alive:
			return

		if self.idle_time >= 0 and self.attack_time == 0:
			sprites.load_sprites_enemy_idle(self, self.delta, screen)
		elif self.attack_time > 0:
			sprites.load_sprites_enemy_attack(self, self.delta, screen)

	def attack(self, player, screen):
		if not self.alive:
			return

		dx = self.rect.center[0] - player.rect.center[0]
		if dx > 0:
			self.direction = 1
		elif dx < 0:
			self.direction = 0

		bullet = libat.Bullet((self.rect.center[0], self.rect.center[1]),
			(player.rect.center[0], player.rect.center[1] + player.rect.height // 2),
				self.damage, (0,50,50), BOSS_SHOOT_BULLET_SPRITE)
		bullet.shooted = True
		self.attack_time += 1
		self.bullets.bullets.append(bullet)

	def move(self, time):
		self.rect.y += self.max_offset*math.sin(time.get_ticks() / 500)
		self.die()

class Boss(BaseEnemy):
	def __init__(self, x, y):
		super().__init__(x,y)
		self.idle_sprites = sprites.cut_sheet(BOSS_IDLE_SPRITE, 2, 2, 1)
		self.attack_sprites = sprites.cut_sheet(BOSS_ATTACK2_SPRITE, 2, 2, 2.5)
		self.birth_sprites = sprites.cut_sheet(BOSS_BIRTH_SPRITE, 2, 2, 1.5)
		self.death_sprites = sprites.cut_sheet(BOSS_DEATH_SPRITE, 2, 2, 1.5)
		self.rect = sprites.cut_transparent_rect(self.idle_sprites[0])
		self.rect.center = (x, y)
		self.direction = 0

		self.idle_x_0 = 0.03
		self.idle_y_0 = 0.03

		self.idle_x_1 = 0.03
		self.idle_y_1 = 0.03

		self.attack_x_0 = 0.15
		self.attack_y_0 = 0.1

		self.death_x = 0.03
		self.death_y = 0.03

		self.birth_x = 0.03
		self.birth_y = 0.03

		self.idle_current_sprite = 0
		self.idle_frame_rate = 0.5

		self.death_current_sprite = 0
		self.death_frame_rate = 10
		self.death_count = 0
		self.max_death_count = 5

		self.attack_current_sprite = 0
		self.attack_frame_rate = 5

		self.birth_time = 1
		self.birth_count = 0
		self.max_birth_count = 5
		self.birth_current_sprite = 0
		self.birth_frame_rate = 2

		self.health = BOSS_INITIAL_HEALTH
		self.MAX_HEALTH = BOSS_INITIAL_MAX_HEALTH
		self.bullets = libat.Bullets()
		self.damage = BOSS_INITIAL_DAMAGE
		self.max_offset = BOSS_MAX_OFFSET
		self.attack2_config = 0
		self.xp = BOSS_XP

		self.attack2_times = random.randint(5,10)
		self.attack2_count = 0
		self.attack2_isrunning = False

		self.attack3_isrunning = False

		self.enemies = list()

	def move(self, time):
		if not self.alive:
			return

		self.rect.y += self.max_offset*math.sin(time.get_ticks() / 500)
		self.die()

	def load(self, screen):
		if self.death_time > 0 and self.death_count < self.max_death_count:
			sprites.load_sprites_boss_death(self, self.delta, screen)
			return

		if not self.alive:
			return

		if self.birth_time > 0:
			sprites.load_sprites_boss_birth(self, self.delta, screen)
			return

		# pygame.draw.rect(screen, self.color, self.rect)
		if self.idle_time >= 0  and self.attack2_count == 0 and self.attack_time == 0:
			sprites.load_sprites_enemy_idle(self, self.delta, screen)
		elif self.attack_time > 0 or self.attack2_count > 0:
			sprites.load_sprites_enemy_attack(self, self.delta, screen)


	def attack(self, player, screen):
		if not player.alive or not self.alive or self.birth_time > 0:
			self.attack_time = 0
			self.attack_current_sprite = 0
			return

		if self.attack2_isrunning:
			self.attack2()
			return

		prob = random.randint(0,10)

		if 0 <= prob <= 8:
			self.attack1(player)

		elif prob == 9:
			self.attack2_isrunning = True
			self.attack2()
		else:
			if self.attack3_isrunning:
				if len(self.enemies) > 0:
					return
				else:
					self.attack3_isrunning = False

			self.attack3()


	def attack1(self, player):
		dx = self.rect.center[0] - player.rect.center[0]
		if dx > 0:
			self.direction = 1
		elif dx < 0:
			self.direction = 0

		bullet = libat.Bullet((self.rect.center[0], self.rect.center[1]),
			(player.rect.center[0], player.rect.center[1] + player.rect.height // 2),
				self.damage, (0,50,50), BOSS_BULLET_SPRITE)
		bullet.shooted = True
		self.bullets.bullets.append(bullet)


	def attack2(self):
		#ataque circular
		self.direction = 0
		number = BOSS_ATTACK2_PROJECTS # != 0
		radius = 50

		config = self.attack2_config % 2 * math.pi / 2
		for i in range(number):
			angle = (2 * math.pi / number) * i
			destiny_x = self.rect.center[0] + radius * math.cos(angle + config)
			destiny_y = self.rect.center[1] + radius * math.sin(angle + config)

			bullet = libat.Bullet(self.rect.center,
									(destiny_x, destiny_y),
									self.damage, (0,50,50), BOSS_BULLET_SPRITE)
			bullet.shooted = True
			self.bullets.bullets.append(bullet)

		self.attack2_config += 1
		self.attack2_count += 1
		self.attack_time += 1

		if self.attack2_count == self.attack2_times:
			self.attack2_isrunning = False
			self.attack2_count = 0
			self.attack_time = 0
			self.attack_current_sprite = 0

			self.attack2_times = random.randint(5,10)


	def attack3(self):
		number = random.randint(3,6)
		radius = 200

		for i in range(number):
			angle = (2 * math.pi / number) * i
			x = self.rect.center[0] + radius * math.cos(angle + math.pi/2)
			y = self.rect.center[1] + radius * math.sin(angle + math.pi/2)

			enemy = BossShootingEnemy(x, y)
			self.enemies.append(enemy)

		self.attack3_isrunning = True

	def update(self, time):
		self.move(time)

		if len(self.enemies) > 0:
			for enemy in self.boss_enemies.enemies:
				enemy.move(time)

class Key:
	def __init__(self, image_path, position=(0, 0)):
		self.image = pygame.image.load(image_path).convert_alpha()
		self.rect = self.image.get_rect(center=position)
		self.visible = False  # A chave será visível somente quando ativada

	def activate(self, position):
		self.rect.center = position
		self.visible = True

	def load(self, screen):
		if self.visible:
			screen.blit(self.image, self.rect)

	def check_collision(self, player):
		if self.visible and self.rect.colliderect(player.rect):
			self.visible = False
			return True
		return False

class Enemies():

	def __init__(self):
		self.mov_enemies = list()
		self.shoot_enemies = list()
		self.enemies = list()
		self.boss = None
		self.key = Key(KEY_SPRITE)
		self.last_enemy = None


	def find_random_positions(self, plataforms, number):
		if len(plataforms) == 0:
			return

		choices = [random.choice(plataforms) for _ in range(number)]

		positions = list()

		x_fix = 20
		y_fix = 10

		for choice in choices:
			x = choice.center[0]
			y = choice.top - 10

			positions.append((x,y))

		return positions


	def create_random_enemies(self, plataforms, floor):
		if len(plataforms) == 0:
			return

		multiplier = ENEMY_FLOOR_MULTIPLIER

		enemies_types = [StrongMovingEnemy, ShootingEnemy, WeakMovingEnemy]

		number = random.randint(2, floor + 2)
		positions = self.find_random_positions(plataforms, number)

		choices = [random.choice(enemies_types)(positions[i][0], positions[i][1]) for i in range(number)]

		for choice in choices:
			choice.damage += multiplier*choice.damage*floor
			choice.health += multiplier*choice.health*floor
			choice.xp += multiplier*choice.xp


			if isinstance(choice, MovingEnemy):
				self.mov_enemies.append(choice)

			if isinstance(choice, ShootingEnemy):
				self.shoot_enemies.append(choice)


	def update(self, plataforms, player, enemies, time, screen):
		self.enemies = self.mov_enemies + self.shoot_enemies

		for enemy in self.enemies:
			enemy.update(plataforms, player, enemies, screen)

		if self.boss:
			self.boss.move(time)

			if len(self.boss.enemies) > 0:
				for enemy in self.boss.enemies:
					enemy.move(time)



	def load(self, screen):
		self.enemies = self.mov_enemies + self.shoot_enemies

		for enemy in self.enemies:
			enemy.load(screen)

		if self.boss:
			self.boss.load(screen)

			if len(self.boss.enemies) > 0:
				for enemy in self.boss.enemies:
					enemy.load(screen)

		self.key.load(screen)


	def mov_attack(self, player, plataforms, screen):
		if not player or not player.rect:
			return

		for enemy in self.mov_enemies:
			enemy.seeingplayer = enemy.can_see_player(
									player.rect.center,
									plataforms)

			if not enemy.seeingplayer and enemy.roaming:
				enemy.roam()
			else:
				enemy.chase(player)

	def shoot_attack(self, player, plataforms, screen):
		if not player or not player.rect:
			return

		for enemy in self.shoot_enemies:
			enemy.seeingplayer = enemy.can_see_player(
									player.rect.center,
									plataforms)

			if not enemy.seeingplayer and enemy.roaming:
				enemy.roam()
			else:
				enemy.chase(player)
				enemy.attack(player, screen)

		if self.boss:
			self.boss.attack(player, screen)

			if len(self.boss.enemies) > 0:
				for enemy in self.boss.enemies:
					enemy.attack(player, screen)



	def shoot_bullets(self, player, plataforms, screen):
		for enemy in self.shoot_enemies:
			enemy.bullets.shoot(screen, player, plataforms, enemy)

		if self.boss:
			self.boss.bullets.shoot(screen, player, plataforms, self.boss)

			if len(self.boss.enemies) > 0:
				for enemy in self.boss.enemies:
					enemy.bullets.shoot(screen, player, plataforms, enemy)


	def check_die(self, player):
		self.enemies = self.mov_enemies + self.shoot_enemies

		if len(self.enemies) > 0:
			for enemy in self.enemies:
				if enemy.alive == False:
					
					if enemy.killed_by_player:
						player.total_exp += enemy.xp
						enemy.xp = 0

					if isinstance(enemy, MovingEnemy) and enemy.death_time == 0:
						self.last_enemy = enemy
						self.mov_enemies.remove(enemy)

					if isinstance(enemy, ShootingEnemy) and len(enemy.bullets.bullets) == 0 and enemy.death_time == 0:
						self.last_enemy = enemy
						self.shoot_enemies.remove(enemy)

		if self.boss:
			if not self.boss.alive:
				self.last_enemy = self.boss
				player.total_exp += self.boss.xp
				self.boss.xp = 0



			if len(self.boss.enemies) > 0:
				for enemy in self.boss.enemies:
					if enemy.alive == False and len(enemy.bullets.bullets) == 0 and enemy.death_time == 0:
						self.last_enemy = enemy
						if enemy.killed_by_player:
							player.total_exp += enemy.xp
							enemy.xp = 0

						self.boss.enemies.remove(enemy)


			self.enemies = self.mov_enemies + self.shoot_enemies
			if not self.boss.alive and self.boss.death_time == 0:
				if not self.enemies and not self.boss.enemies:
					if not self.key.visible:
						if self.last_enemy:
							self.key.activate(self.last_enemy.rect.center)


				if len(self.boss.enemies) == 0:
					self.boss = None
