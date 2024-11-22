import pygame
import random
import math
import sys

#sys.path.append('../atirar')

import bullets as libat
import player

class BaseEnemy():

	def __init__(self, x, y, color = None, w = 0, h = 0):
		self.rect = pygame.Rect(x,y, w, h)
		self.health = 0
		self.speed = 0
		self.damage = 0
		self.color = color
		self.alive = True

		self.last_direction_player = 0
		self.lost_player_timer = 0
		self.seeingplayer = False
		self.direction = random.choice([(1,0),(-1,0)])
		self.timer = random.randint(50,100)
		self.roaming = True
		self.max_timer = self.timer
		self.sight_radius = 0

		self.gravity_y = 0.5
		self.speed_y = 0
		self.dx = 0
		self.dy = 0

	def invert_direction(self):
		if self.direction == (1,0): #direita
			self.direction = (-1,0)
		elif self.direction == (-1,0): #esquerda
			self.direction = (1,0)


	def change_direction(self):
		new_direction = random.choice([(1,0), (-1,0)])
		return new_direction

	def collide(self, plataforms, player, enemies):
		pass

	def update(self, plataforms, player, enemies):
		pass


	def load(self, screen):
		if self.alive == False:
			return

		pygame.draw.rect(screen, self.color, self.rect)


	def decrement_health(self, howmuch):
		self.health -= howmuch
		self.die()


	def die(self):
		if self.health <= 0:
			self.alive = False


	def attack(self, player, screen = None):
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

		steps = int(distance)
		for step in range(steps):
			x = self.rect.center[0] + dx * step / steps
			y = self.rect.center[1] + dy * step / steps

			for plataform in plataforms:
				if plataform.collidepoint((x, y)):
					return False

		return True


class MovingEnemy(BaseEnemy):
	def __init__(self, x, y, color, w, h):
		super().__init__(x,y, color, w, h)
		self.tomove = random.randint(10,50)
		self.max_tomove = self.tomove

	def chase(self, player):
		if self.seeingplayer:
			dx = self.rect.x - player.rect.x

			if dx > 0:
				self.dx -= self.speed
				self.last_direction_player = -1
			elif dx < 0:
				self.dx += self.speed
				self.last_direction_player = 1

			self.roaming = False
			self.lost_player_timer = 120
			self.timer = self.max_timer

		elif self.lost_player_timer > 0:
			self.dx = self.speed * self.last_direction_player
			self.lost_player_timer -= 1

		else:
			self.roaming = True
			self.dx = 0

	def collide(self, plataforms, player, enemies):
		"""
		if len(enemies.enemies) > 0:
			for enemy in enemies.enemies:
				if self.rect.colliderect(enemy.rect):
					if self.speed_y > 0:
						self.rect.bottom = enemy.rect.top
						self.speed_y = 0
					elif self.speed_y < 0:
						self.rect.top = enemy.rect.bottom
						self.speed_y = 0
		"""

		if player:
			if self.rect.colliderect(player.rect):
				self.attack(player)
				if self.speed_y > 0:
					self.rect.bottom = player.rect.top
					self.speed_y = 0
				elif self.speed_y < 0:
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

		"""
		if len(enemies.enemies) > 0:
			for enemy in enemies.enemies:
				if self.rect.colliderect(enemy.rect):
					if self.dx > 0:
						self.rect.right = enemy.rect.left
					if self.dx < 0:
						self.rect.left = enemy.rect.right
		"""

		if player:
			if self.rect.colliderect(player.rect):
				self.attack(player)
				if self.dx > 0:
					self.rect.right = player.rect.left
				elif self.dx < 0:
					self.rect.left = player.rect.right

		if len(plataforms) > 0:
			for plataform in plataforms:
				if self.rect.colliderect(plataform):
					if self.dx > 0:
						self.rect.right = plataform.left
					if self.dx < 0:
						self.rect.left = plataform.right

					self.invert_direction()


	def update(self, plataforms, player, enemies):
		if self.alive == False:
			return

		self.speed_y += self.gravity_y
		self.rect.y += self.speed_y

		self.collide(plataforms, player, enemies)

		self.dx = 0
		self.dy = 0


	def move(self, time = None):
		if self.tomove == 0:
			return

		if self.direction == (1,0):
			self.dx = self.speed

		if self.direction == (-1,0):
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
				self.direction = self.change_direction()
			elif action == 2:
				self.move()

			self.timer = self.max_timer
			self.tomove = self.max_tomove

	def attack(self, player):
		if self.alive == False:
			return
		player.decrement_health(self.damage)

class WeakMovingEnemy(MovingEnemy):

	def __init__(self, x,y):
		super().__init__(x, y, (100,100,100), 25, 100)
		self.health = 3
		self.damage = 5
		self.speed = 2
		self.sight_radius = 200


class StrongMovingEnemy(MovingEnemy):

	def __init__(self, x,y):
		super().__init__(x,y, (100,100, 200), 50, 100)
		self.health = 20
		self.damage = 5
		self.speed = 1
		self.sight_radius = 100

class ShootingEnemy(BaseEnemy):

	def __init__(self, x,y):
		super().__init__(x,y, (0,0,0), 50, 50)
		self.health = 5
		self.damage = 10
		self.bullets = libat.Bullets()
		self.timer = 5
		self.max_timer = self.timer
		self.sight_radius = 600

	def roam(self):
		if self.seeingplayer == True or self.roaming == False:
			return

		self.timer -= 1
		if self.timer <= 0:
			self.direction = self.change_direction()
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


	def update(self, plataforms, player, enemies = []):
		if self.alive == False:
			return

		self.speed_y += self.gravity_y
		self.rect.y += self.speed_y


		self.collide(plataforms, player, enemies)

		self.dx = 0
		self.dy = 0

	def chase(self, player):
		if self.seeingplayer:
			dx = self.rect.x - player.rect.x

			if dx > 0:
				self.last_direction_player = -1
				self.direction = (-1,0)
			elif dx < 0:
				self.direction = (1,0)
				self.last_direction_player = 1

			self.roaming = False
			self.lost_player_timer = 5
			self.timer = self.max_timer

		elif self.lost_player_timer > 0:
			if self.last_direction_player == 1:
				self.direction = (1,0)
			elif self.last_direction_player == -1:
				self.direction = (-1,0)

			self.bullets.bullets.clear()
			self.lost_player_timer -= 1

		else:
			self.roaming = True
			self.dx = 0


	def attack(self, player):
		if self.alive == False or \
		 self.roaming == True or \
		 self.seeingplayer == False or \
		 player.alive == False:
			return

		bullet = libat.Bullet((self.rect.x, self.rect.y),
					(player.rect.x, player.rect.y),
						self.damage, (0,255,100))
		bullet.shooted = True
		self.bullets.bullets.append(bullet)

class BossShootingEnemy(ShootingEnemy):
	def __init__(self, x,y):
		super().__init__(x,y)
		self.max_offset = 2
		self.seeingplayer = True
		self.roaming = False

	def move(self, time):
		self.rect.y += self.max_offset*math.sin(time.get_ticks() / 500)

class Boss(BaseEnemy):
	def __init__(self, x, y, color, w, h):
		super().__init__(x,y, color, w, h)
		self.health = 1000
		self.MAX_HEALTH = 1000
		self.bullets = libat.Bullets()
		self.damage = 200
		self.max_offset = 2
		self.attack2_config = 0

		self.attack2_times = random.randint(5,10)
		self.attack2_count = 0
		self.attack2_isrunning = False

		self.attack3_isrunning = False

		self.enemies = list()

	def move(self, time):
		self.rect.y += self.max_offset*math.sin(time.get_ticks() / 500)


	def attack(self, player):
		if not player.alive or not self.alive:
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
		bullet = libat.Bullet((self.rect.center[0], self.rect.center[1]),
			(player.rect.center[0], player.rect.center[1]),
				self.damage, (0,50,50))
		bullet.shooted = True
		self.bullets.bullets.append(bullet)


	def attack2(self):
		#ataque circular
		number = 10 # != 0
		radius = 50

		config = self.attack2_config % 2 * math.pi / 2
		for i in range(number):
			angle = (2 * math.pi / number) * i
			destiny_x = self.rect.center[0] + radius * math.cos(angle + config)
			destiny_y = self.rect.center[1] + radius * math.sin(angle + config)

			bullet = libat.Bullet(self.rect.center,
									(destiny_x, destiny_y),
									self.damage, (0,50,50))
			bullet.shooted = True
			self.bullets.bullets.append(bullet)

		self.attack2_config += 1
		self.attack2_count += 1

		if self.attack2_count == self.attack2_times:
			self.attack2_isrunning = False

			self.attack2_times = random.randint(5,10)


	def attack3(self):
		number = random.randint(3,6)
		radius = 150

		for i in range(number):
			angle = (2 * math.pi / number) * i
			x = self.rect.center[0] + radius * math.cos(angle + math.pi/2) - self.rect.width // 4
			y = self.rect.center[1] + radius * math.sin(angle + math.pi/2) - self.rect.height // 4

			enemy = BossShootingEnemy(x, y)
			self.enemies.append(enemy)

		self.attack3_isrunning = True

	def move_boss(self, time):
		self.move(time)

		if len(self.enemies) > 0:
			for enemy in self.boss_enemies.enemies:
				enemy.move(time)


class Enemies():

	def __init__(self):
		self.mov_enemies = list()
		self.shoot_enemies = list()
		self.enemies = list()
		self.boss = None


	def find_random_positions(self, plataforms, number):
		choices = [random.choice(plataforms) for _ in range(number)]

		positions = list()

		for choice in choices:
			x = random.randint(choice.left, choice.right - 10)
			y = choice.top - 10

			positions.append((x,y))

		return positions


	def create_random_enemies(self, plataforms, number):
		enemies_types = [WeakMovingEnemy, ShootingEnemy,
						StrongMovingEnemy]

		positions = self.find_random_positions(plataforms, number)

		choices = [random.choice(enemies_types)(positions[i][0], positions[i][1]) for i in range(number)]

		for choice in choices:
			if isinstance(choice, MovingEnemy):
				self.mov_enemies.append(choice)

			if isinstance(choice, ShootingEnemy):
				self.shoot_enemies.append(choice)


	def update(self, plataforms, player, enemies, time):
		self.enemies = self.mov_enemies + self.shoot_enemies

		for enemy in self.enemies:
			enemy.update(plataforms, player, enemies)

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


	def mov_attack(self, player, plataforms):
		for enemy in self.mov_enemies:
			enemy.seeingplayer = enemy.can_see_player(
									player.rect.center,
									plataforms)

			if not enemy.seeingplayer and enemy.roaming:
				enemy.roam()
			else:
				enemy.chase(player)

	def shoot_attack(self, player, plataforms):
		for enemy in self.shoot_enemies:
			enemy.seeingplayer = enemy.can_see_player(
									player.rect.center,
									plataforms)

			if not enemy.seeingplayer and enemy.roaming:
				enemy.roam()
			else:
				enemy.chase(player)
				enemy.attack(player)

		if self.boss:
			self.boss.attack(player)

			if len(self.boss.enemies) > 0:
				for enemy in self.boss.enemies:
					enemy.attack(player)



	def shoot_bullets(self, player, plataforms, screen):
		for enemy in self.shoot_enemies:
			enemy.bullets.shoot(screen, player, plataforms, enemy)

		if self.boss:
			self.boss.bullets.shoot(screen, player, plataforms, self.boss)

			if len(self.boss.enemies) > 0:
				for enemy in self.boss.enemies:
					enemy.bullets.shoot(screen, player, plataforms, enemy)


	def check_die(self):
		self.enemies = self.mov_enemies + self.shoot_enemies

		if len(self.enemies) > 0:
			for enemy in self.enemies:
				if enemy.alive == False:

					if isinstance(enemy, WeakMovingEnemy) or isinstance(enemy, StrongMovingEnemy):
						self.mov_enemies.remove(enemy)

					if isinstance(enemy, ShootingEnemy) and len(enemy.bullets.bullets) == 0:
						self.shoot_enemies.remove(enemy)


		if self.boss:
			if len(self.boss.enemies) > 0:
				for enemy in self.boss.enemies:
					if enemy.alive == False and len(enemy.bullets.bullets) == 0:
						self.boss.enemies.remove(enemy)



