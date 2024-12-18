import pygame
import sys
import math
from gamesettings import *

import enemy as liben

class Bullet:

	def __init__(self, begin, destiny, damage, sprite_path):
		"""
		Inicializa objeto de classe Bullet.

		Parâmetros
		----------
		begin: tuple(float, float)
			Ponto de partida.

		destiny: tuple(float, float)
			Ponto de chegada.

		damage: float

		sprite_path: str
			Caminho contendo sprite.
		"""
		self.speed = 10
		self.shooted = False
		self.damage = damage
		self.begin = begin
		self.destiny = destiny

		self.image = pygame.image.load(sprite_path)
		self.image = pygame.transform.scale(self.image, (10,10))

		self.rect = self.image.get_rect(center = (self.begin[0], self.begin[1]))

		dx = self.destiny[0] - self.begin[0]
		dy = self.destiny[1] - self.begin[1]
		distance = math.sqrt(dx ** 2 + dy ** 2)

		if distance == 0:
			self.direction_x = 0
			self.direction_y = 0
		else:
			self.direction_x = (dx / distance) * self.speed
			self.direction_y = (dy / distance) * self.speed


	def take_damage(self, object, player = None) -> None:
		"""
		Aplica dano ao objeto.

		Parâmetros
		----------
		object: objeto a receber dano.

		player: objeto de player.
		"""
		if not object.rect or not object.alive:
			return

		if self.rect.colliderect(object.rect) and object.health:
			if player:
				player.life_steal(object)

			object.decrement_health(self.damage)
			self.shooted = False

	def platform_collide(self, platforms) -> None:
		"""
		Responsável pela colisão bullet-plataform.

		Parâmetros
		----------
		platforms: list(retângulo de pygame)
		"""
		for platform in platforms:
			if self.rect.colliderect(platform):
				self.shooted = False

	def load(self, screen) -> None:
		"""
		Desenha a bullet.

		Parâmetros
		----------
		screen: tela de pygame
		"""
		screen.blit(self.image, self.rect)


	def move(self) -> None:
		"""
		Move a bullet.
		"""
		if self.shooted == False:
			return 

		self.rect.x += self.direction_x
		self.rect.y += self.direction_y


class Bullets():
	def __init__(self):
		"""
		Inicializa objeto de classe Bullets.
		"""
		self.bullets = list()

	def shoot(self, screen, objects, platforms, shooter) -> None:
		"""
		Responsável por continuar carregando todas as bullets de self.bullets

		Parâmetros
		----------
		screen: tela de pygame

		objects: list(retângulo de plataforma) / objeto de player
			Objetos que vão tomar dano.
		
		shooter: objeto de player / objeto de inimigo
			Quem está atirando.
		"""
		if len(self.bullets) == 0:
			return

		for bullet in self.bullets:
			if bullet.shooted == True:
				bullet.load(screen)
				bullet.move()
				bullet.platform_collide(platforms)

				if bullet.rect.y > SCREEN_SIZE[1] or bullet.rect.y < 0:
					bullet.shooted = False

				if isinstance(shooter, liben.BaseEnemy):
					bullet.take_damage(objects)
				else:
					if len(objects.enemies) != 0:
						for enemy in objects.enemies:
							bullet.take_damage(enemy, shooter)

					if objects.boss:
						bullet.take_damage(objects.boss, shooter)

						if len(objects.boss.enemies) > 0:
							for enemy in objects.boss.enemies:
								bullet.take_damage(enemy, shooter)

			else:
				self.bullets.remove(bullet)


