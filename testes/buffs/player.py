import pygame
import bullets as libat
import enemy as liben
import math

class Player:

	def __init__(self, x, y, width, height, weapon_image = None):
		self.rect = pygame.Rect(x, y, width, height)
		self.color = (255, 0, 0)
		self.gravity_y = 0.5 # pixels^2 / frame
		self.speed_y = 0
		self.health = 1000
		self.jump_count = 0
		self.dash_count = 0


		self.speed_x = 4
		self.MAX_HEALTH = 1000
		self.damage = 50
		self.jump_count_max = 4
		self.dash = 0
		self.shoot = 0
		self.ls = 0


		self.alive = True
		
		self.width = width
		self.height = height

		self.font = pygame.font.Font(None, 20)

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

	def draw_status(self, screen):
		damage_text = f"Dano : {self.damage}"
		health_text = f"Vida máxima : {self.MAX_HEALTH}"
		speed_text = f"Velocidade : {self.speed_x:.2f}"
		jump_text = f"Pulos : {self.jump_count_max}"
		dash_text = f"Dash : {self.dash}"
		shoot_text = f"Tiros : {self.shoot}"
		ls_text = f"Roubo de vida : {self.ls}"


		damage_surface = self.font.render(damage_text, True, (0,0,0))
		screen.blit(damage_surface, (10, 200))
		health_surface = self.font.render(health_text, True, (0,0,0))
		screen.blit(health_surface, (10, 250))
		speed_surface = self.font.render(speed_text, True, (0,0,0))
		screen.blit(speed_surface, (10, 300))
		jump_surface = self.font.render(jump_text, True, (0,0,0))
		screen.blit(jump_surface, (10, 350))
		dash_surface = self.font.render(dash_text, True, (0,0,0))
		screen.blit(dash_surface, (10, 400))
		shoot_surface = self.font.render(shoot_text, True, (0,0,0))
		screen.blit(shoot_surface, (10, 450))
		ls_surface = self.font.render(ls_text, True, (0,0,0))
		screen.blit(ls_surface, (10, 500))


	def draw(self, screen, mouse = None):
		pygame.draw.rect(screen, self.color, self.rect)
		self.draw_status(screen)

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
						self.dash_count = 0
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
						self.dash_count = 0
					elif self.speed_y < 0:
						self.rect.top = enemy.rect.bottom
						self.speed_y = 0  
						self.dash_count = 0     

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

	def _dash(self, mouse):
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


	def on_event(self, event: pygame.event.Event, mouse):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				self._jump()

			if event.key == pygame.K_q:
				self._dash(mouse)
		
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				bullet = libat.Bullet((self.rect.x + (self.width // 2), self.rect.y + (self.height // 2)), 
									  (mouse.get_pos()[0], mouse.get_pos()[1]),
									  self.damage,
									  (10, 10, 10))
				bullet.shooted = True
				self.bullets.bullets.append(bullet)

				if self.shoot > 0:
					distance = 50
					for i in range(self.shoot):
						extra_bullet = libat.Bullet((self.rect.x + (self.width // 2), self.rect.y + (self.height //2)),
										(mouse.get_pos()[0] + (i+1) * distance, mouse.get_pos()[1]),
										self.damage,
										(10, 10, 10))
						extra_bullet.shooted = True
						self.bullets.bullets.append(extra_bullet)
		
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