import pygame
import sys

#alterar caminhos dependendo do contexto

import bullets as libat
import enemy as liben


class Player:

	def __init__(self, x, y, width, height, weapon_image = None):
		self.rect = pygame.Rect(x, y, width, height)
		self.color = (255, 0, 0)
		self.gravity_y = 0.5 # pixels^2 / frame
		self.speed_y = 0
		self.speed_x = 4
		self.health = 1000
		self.MAX_HEALTH = 1000
		self.damage = 50
		self.jump_count = 0
		self.jump_count_max = 4

		self.alive = True
		
		self.width = width
		self.height = height

		self.dx = 0
		self.dy = 0

		self.on_ground = 0

		self.bullets = libat.Bullets()

		if weapon_image:
			self.weapon = wp.Weapon(self, weapon_image, (50, 50))
			self.weapon_image = weapon_image
			self.weapon.create_weapon()
		else:
			self.weapon_image = None
	
	def draw(self, screen, mouse = None):
		pygame.draw.rect(screen, self.color, self.rect)

		if self.weapon_image and mouse:
			self.weapon_image.point_mouse(mouse, screen)

	def collide(self, plataforms, enemies):

		if len(plataforms) > 0:     
			self.on_ground = False
			for plataform in plataforms:
				if self.rect.colliderect(plataform):
					if self.speed_y > 0:
						self.rect.bottom = plataform.top
						self.speed_y = 0
						self.on_ground = True
						self.jump_count = 0
					elif self.speed_y < 0:
						self.rect.top = plataform.bottom
						self.speed_y = 0

		if enemies and len(enemies.enemies) > 0:
			for enemy in enemies.enemies:
				if self.rect.colliderect(enemy.rect):
					if self.speed_y > 0:
						self.rect.bottom = enemy.rect.top
						self.speed_y = 0
						self.jump_count = 0
					elif self.speed_y < 0:
						self.rect.top = enemy.rect.bottom
						self.speed_y = 0       

		self.rect.x += self.dx

		if len(plataforms) > 0:
			for plataform in plataforms:
				if self.rect.colliderect(plataform):
					if self.dx > 0:
						self.rect.right = plataform.left
					if self.dx < 0:
						self.rect.left = plataform.right

		if enemies and len(enemies.enemies) > 0:
			for enemy in enemies.enemies:
				if self.rect.colliderect(enemy.rect):
					if self.dx > 0:
						self.rect.right = enemy.rect.left
					if self.dx < 0:
						self.rect.left = enemy.rect.right

	def update(self, plataforms, enemies):
		self.speed_y += self.gravity_y
		self.rect.y += self.speed_y

		self.collide(plataforms, enemies)

		self.dx = 0
		self.dy = 0

	def on_event(self, event: pygame.event.Event, mouse):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				self._jump()
		
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				bullet = libat.Bullet((self.rect.x + (self.width // 2), self.rect.y + (self.height // 2)), 
									  (mouse.get_pos()[0], mouse.get_pos()[1]),
									  self.damage,
									  (10, 10, 10))
				bullet.shooted = True
				self.bullets.bullets.append(bullet)
	
	def _jump(self):
		if self.jump_count >= self.jump_count_max:
			return
		self.speed_y = -10
		self.jump_count += 1

	def on_key_pressed(self, key_map):
		if key_map[pygame.K_d]:
			self.dx = self.speed_x
		elif key_map[pygame.K_a]:
			self.dx = - self.speed_x

	def decrement_health(self, howmuch):
		self.health -= howmuch
		self.die()

	def increment_health(self, howmuch):
		self.health += howmuch
		if self.health >= self.MAX_HEALTH:
			self.health = self.MAX_HEALTH

	def die(self):
		if self.health <= 0:
			self.alive = False