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

		self.total_exp = 0
		self.next_level = 100
		self.ant_level = 1
		self.level = 1


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

	def calc_next_level(self, total):
		for _ in range(total):
			self.next_level += 0.5*self.next_level

	def level_up(self):
		if self.total_exp >= self.next_level:
			total = int(self.total_exp // self.next_level)
			self.ant_level = self.level
			self.level += total
			self.calc_next_level(total)
			return True

	def draw_status(self, screen):
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
		if enemy.health > 0 and self.health < self.MAX_HEALTH:
			self.health += self.ls * (enemy.health + 0.5*self.damage)


	def draw(self, screen, mouse = None):
		if not self.alive:
			return

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
					if isinstance(enemy, liben.MovingEnemy):
						enemy.attack(self)

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
					if isinstance(enemy, liben.MovingEnemy):
						enemy.attack(self)
						
					if self.dx > 0:
						self.rect.right = enemy.rect.left
					if self.dx < 0:
						self.rect.left = enemy.rect.right

	def update(self, plataforms, enemies):
		if not self.alive:
			self.health = 0
			return

		self.speed_y += self.gravity_y
		self.rect.y += self.speed_y
		self.die()

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
		if not self.alive:
			return

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

				if self.shoot > 0:
					distance = 50
					for i in range(self.shoot):
						extra_bullet = libat.Bullet((self.rect.x + (self.width // 2), self.rect.y + (self.height //2)),
										(mouse.get_pos()[0] + (i+1) * distance, mouse.get_pos()[1]),
										self.damage,
										(10, 10, 10))
						extra_bullet.shooted = True
						self.bullets.bullets.append(extra_bullet)

			if event.button == 3:
				self._dash(mouse)
		
	def _jump(self):
		if self.jump_count >= self.jump_count_max:
			return
		self.speed_y = -10
		self.jump_count += 1

	def on_key_pressed(self, key_map):
		if not self.alive:
			return

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

		if self.rect.y > 1000:
			self.alive = False