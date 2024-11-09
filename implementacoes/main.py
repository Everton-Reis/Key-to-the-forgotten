import pygame
import sys

sys.path.append('./atirar')
sys.path.append('./inimigos')

import enemy as liben
import followmouse as libat

pygame.init()
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))


class Player:

	def __init__(self, x, y):
		self.rect = pygame.Rect(x,y, 50, 50)
		self.gravity = 2
		self.speed_x = 8
		self.speed_y = 0
		self.max_jumps = 1
		self.jumps = 0
		self.health = 100
		self.alive = True
		self.dx = 0
		self.bullets = libat.Bullets()

	def load(self, screen):
		if self.alive == False:
			return

		pygame.draw.rect(screen, (0,0,188), self.rect)

	def update(self, enemies):
		self.speed_y += self.gravity
		self.rect.y += self.speed_y

		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0
		if self.rect.top < 0:
			self.rect.top = 0
		if self.rect.bottom > HEIGHT:
			self.rect.bottom = HEIGHT
			self.speed_y = 0
			self.jumps = 0


	def decrement_health(self, howmuch):
		self.health -= howmuch
		self.die()

	def die(self):
		if self.health <= 0:
			self.alive = False

	def move(self, direction):
		if direction == "right":
			self.rect.x += self.speed_x
		elif direction == "left":
			self.rect.x -= self.speed_x

	def jump(self, howmuch):
		if self.jumps >= self.max_jumps:
			return

		self.speed_y += howmuch
		self.jumps += 1

	def on_event(self, event, mouse):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				self.jump(-20)

		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				bullet = libat.Bullet((self.rect.x, self.rect.y),
					(mouse.get_pos()[0], mouse.get_pos()[1]),
														5,
														(10,10,10))
				bullet.shooted = True
				self.bullets.bullets.append(bullet)


	def on_hold(self, keys):

		if keys[pygame.K_a]:
			self.move("left")
			self.dx = -self.speed_x


		if keys[pygame.K_d]:
			self.move("right")
			self.dx = self.speed_x



player = Player(0,0)

enemies = liben.Enemies()
enemy1 = liben.WeakMovingEnemy(400,HEIGHT - 100)
enemy2 = liben.StrongMovingEnemy(600, HEIGHT - 100)
enemy3 = liben.ShootingEnemy(500, 200)
enemies.mov_enemies.append(enemy1)
enemies.mov_enemies.append(enemy2)
enemies.shoot_enemies.append(enemy3)

clock = pygame.time.Clock()
time = 0


r = True

while r:
	screen.fill((255,255,255))
	time += clock.tick(30)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			r = False

		player.on_event(event, pygame.mouse)


	if time > 1000:
		enemies.shoot_attack(player, screen)
		time = 0


	keys = pygame.key.get_pressed()
	player.update(enemies)
	player.load(screen)
	player.on_hold(keys)

	player.bullets.shoot(screen, enemies,[], who = 0)

	enemies.load(screen)
	enemies.move(player)
	enemies.mov_attack(player)
	enemies.shoot_bullets(player, screen)
	enemies.check_die()

	pygame.display.flip()


pygame.quit()