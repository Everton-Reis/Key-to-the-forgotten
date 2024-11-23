import pygame
import sys
import math

import enemy as liben

class Bullet:

	def __init__(self, begin, destiny, damage, color):
		self.speed = 10
		self.shooted = False
		self.damage = damage
		self.begin = begin
		self.destiny = destiny
		self.color = color
		self.rect = pygame.Rect(self.begin[0], self.begin[1], 10, 10)

		dx = self.destiny[0] - self.begin[0]
		dy = self.destiny[1] - self.begin[1]
		distance = math.sqrt(dx ** 2 + dy ** 2)

		if distance == 0:
			return

		self.direction_x = (dx / distance) * self.speed
		self.direction_y = (dy / distance) * self.speed

	def take_damage(self, object):
		if self.rect.colliderect(object.rect) and object.health:
			object.decrement_health(self.damage)
			self.shooted = False

	def platform_collide(self, platforms):
		for platform in platforms:
			if self.rect.colliderect(platform):
				self.shooted = False

	def load(self, screen):
		pygame.draw.rect(screen, self.color, self.rect)


	def move(self):
		if self.shooted == False:
			return

		self.rect.x += self.direction_x
		self.rect.y += self.direction_y


class Bullets():
	def __init__(self):
		self.bullets = list()

	def shoot(self, screen, objects, platforms, shooter):
		if len(self.bullets) == 0:
			return

		for bullet in self.bullets:
			if bullet.shooted == True:
				bullet.load(screen)
				bullet.move()
				bullet.platform_collide(platforms)

				if isinstance(shooter, liben.BaseEnemy):
					bullet.take_damage(objects)
				else:
					if len(objects) != 0:
						for enemy in objects:
							bullet.take_damage(enemy)

			else:
				self.bullets.remove(bullet)


