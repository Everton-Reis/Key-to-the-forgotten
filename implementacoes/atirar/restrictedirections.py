import pygame
import math

pygame.init()
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))


class Bullet:

	def __init__(self, begin, damage, pivot):
		self.speed = 20
		self.damage = 10
		self.shooted = False
		self.begin = begin
		self.increment = [0,0]

		self.rect = pygame.Rect(self.begin[0], self.begin[1], 10, 10)

		if pivot == 0:
			self.increment[0] = self.speed * (math.sqrt(2)/2)
			self.increment[1] = -self.speed * (math.sqrt(2)/2)
		elif pivot == 1:
			self.increment[0] = -self.speed * (math.sqrt(2)/2)
			self.increment[1] = -self.speed * (math.sqrt(2)/2)
		elif pivot == 2:
			self.increment[0] = -self.speed
		elif pivot == 3:
			self.increment[0] = self.speed
		elif pivot == 4:
			self.increment[1] = -self.speed


	def take_damage(self, object):
		if self.rect.colliderect(object.rect):
			object.decrement_health(self.damage)

	def load(self, screen):
		pygame.draw.rect(screen, (188,0,0), self.rect)

	def move(self):
		self.rect.x += self.increment[0]
		self.rect.y += self.increment[1]


class Bullets():
	def __init__(self):
		self.bullets = list()

	def vanish(self):
		for bullet in self.bullets:
			if bullet.rect.x > WIDTH + 100:
				self.bullets.remove(bullet)
			elif bullet.rect.x < -100:
				self.bullets.remove(bullet)
			elif bullet.rect.y > HEIGHT + 100:
				self.bullets.remove(bullet)
			elif bullet.rect.y < -100:
				self.bullets.remove(bullet)

	def shot(self, screen):
		if len(self.bullets) == 0:
			return

		for bullet in self.bullets:
			if bullet.shooted == True:
				bullet.load(screen)
				bullet.move()


class Player:

	def __init__(self, x, y):
		self.rect = pygame.Rect(x,y, 50, 50)
		self.gravity = 2
		self.speed_x = 5
		self.speed_y = 0
		self.max_jumps = 1
		self.jumps = 0
		self.pivot = 0
		self.bullets = Bullets()

	def load(self, screen):
		pygame.draw.rect(screen, (0,0,188), self.rect)

	def update(self):
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
				bullet = Bullet((self.rect.x, self.rect.y), 5, self.pivot)
				bullet.shooted = True
				self.bullets.bullets.append(bullet)


	def on_hold(self, keys):

		if keys[pygame.K_d] and keys[pygame.K_w]:
			self.pivot = 0
			self.move("right")
		elif keys[pygame.K_a] and keys[pygame.K_w]:
			self.pivot = 1
			self.move("left")
		elif keys[pygame.K_a]:
			self.pivot = 2
			self.move("left")
		elif keys[pygame.K_d]:
			self.pivot = 3
			self.move("right")
		elif keys[pygame.K_w]:
			self.pivot = 4

		


player = Player(0,0)
clock = pygame.time.Clock()


r = True

while r:
	screen.fill((255,255,255))
	clock.tick(30)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			r = False

		player.on_event(event, pygame.mouse)


	keys = pygame.key.get_pressed()
	player.load(screen)
	player.on_hold(keys)
	player.update()
	player.bullets.shot(screen)


	pygame.display.flip()


pygame.quit()