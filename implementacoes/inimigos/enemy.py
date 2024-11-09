import pygame
import sys

sys.path.append('../atirar')

import followmouse as libat

class BaseEnemy():

	def __init__(self, x, y, color, w, h):
		self.rect = pygame.Rect(x,y, w, h)
		self.health = 0
		self.speed = 0
		self.damage = 0
		self.color = color
		self.alive = True

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

	def move(self, player):
		dx = self.rect.x - player.rect.x

		if dx > 0:
			self.rect.x -= self.speed
		elif dx < 0:
			self.rect.x += self.speed


class WeakMovingEnemy(BaseEnemy):

	def __init__(self, x,y):
		super().__init__(x, y, (100,100,100), 25, 100)
		self.health = 3
		self.damage = 5
		self.speed = 2

	def attack(self, player):
		if self.rect.colliderect(player.rect):
			player.decrement_health(self.damage)


class StrongMovingEnemy(BaseEnemy):

	def __init__(self, x,y):
		super().__init__(x,y, (255, 0, 0), 100,100)
		self.health = 20
		self.damage = 5
		self.speed = 1

	def attack(self, player):
		if self.rect.colliderect(player.rect):
			player.decrement_health(self.damage)

class ShootingEnemy(BaseEnemy):

	def __init__(self, x,y):
		super().__init__(x,y, (0,0,0), 50, 10)
		self.health = 5
		self.damage = 10
		self.bullets = libat.Bullets()

	def attack(self, player, screen):
		if self.alive == False:
			return
		bullet = libat.Bullet((self.rect.x, self.rect.y),
					(player.rect.x, player.rect.y),
						self.damage, (0,255,100))
		bullet.shooted = True
		self.bullets.bullets.append(bullet)


class Enemies():

	def __init__(self):
		self.mov_enemies = list()
		self.shoot_enemies = list()
		self.enemies = list()

	def load(self, screen):
		self.enemies = self.mov_enemies + self.shoot_enemies

		for enemy in self.enemies:
			enemy.load(screen)


	def mov_attack(self, player):
		for enemy in self.mov_enemies:
			enemy.attack(player)

	def shoot_attack(self, player, screen):
		for enemy in self.shoot_enemies:
			enemy.attack(player, screen)

	def shoot_bullets(self, player, screen):
		for enemy in self.shoot_enemies:
			enemy.bullets.shoot(screen, player, [], who = 1)


	def move(self, player):
		self.enemies = self.mov_enemies + self.shoot_enemies
		for enemy in self.enemies:
			enemy.move(player)


	def check_die(self):
		self.enemies = self.mov_enemies + self.shoot_enemies
		if len(self.enemies) == 0:
			return

		for enemy in self.enemies:
			if enemy.alive == False:

				if isinstance(enemy, WeakMovingEnemy) or isinstance(enemy, StrongMovingEnemy):
					self.mov_enemies.remove(enemy)

				if isinstance(enemy, ShootingEnemy) and len(enemy.bullets.bullets) == 0:
						self.shoot_enemies.remove(enemy)
