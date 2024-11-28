import pygame
import random
import sys

sys.path.append("./inimigos")

# import fovdetection as fov
# import roaming

BLOCK_SIZE = 100
BLOCK_SPEED = 1
BLUE = (0, 0, 255)

map_layout = [
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
	[1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

class Enemy():
    def __init__(self, x, y, color, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.speed = 2
        self.seeingplayer = False
        self.direction = random.choice([(1,0),(-1,0)])
        self.roaming = True
        self.last_direction_player = 0
        self.lost_player_timer = 0
        self.timer = random.randint(50,100)
        self.max_timer = self.timer
        self.tomove = random.randint(10,50)
        self.max_tomove = self.tomove

        self.dx = 0
        self.gravity_y = 0.5
        self.speed_y = 0
        self.dy = 0

    def invert_direction(self):
        if self.direction == (1,0):
            self.direction = (-1,0)
        elif self.direction == (-1,0):
            self.direction = (1,0)


    def update(self, plataforms):
        self.speed_y += self.gravity_y
        self.rect.y += self.speed_y

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


        self.dx = 0
        self.dy = 0

    def load(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def chase(self, player):
        if player.rect.y - 100 < self.rect.y < player.rect.y + 100 and self.seeingplayer:
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

    def move(self):
        if self.tomove == 0:
            return

        if self.direction == (1,0):
            self.dx = self.speed

        if self.direction == (-1,0):
            self.dx = -self.speed

        self.tomove -= self.speed


class Map:
	def __init__(self):


		self.layout = map_layout
		self.block_size = BLOCK_SIZE
		self.color = BLUE
		self.block_speed = BLOCK_SPEED
		self.standing_plataforms = list()
	
	def draw_plataforms(self, screen, plataforms, size_height, camera_offset):
		for plataform in plataforms:
			pygame.draw.rect(screen, BLUE, plataform)    

			if plataform.y > size_height + 400:
				plataforms.remove(plataform)

	def give_plataforms(self):

		plataforms = []
		for line_index, line in enumerate(self.layout):
			for column_index, block in enumerate(line):
				if block == 1:
					plataform_rect = pygame.Rect(
						column_index * self.block_size,
						line_index * self.block_size,
						self.block_size,
						self.block_size
					)
					plataforms.append(plataform_rect)

		return plataforms

mapa1 = Map()

class Player:

	def __init__(self, x, y, sprites):
		self.idle_sprites = self.cut_sheet(sprites[0], 4, 1, 3)
		self.run_sprites = self.cut_sheet(sprites[1], 6, 1 ,3)
		self.rect = self.idle_sprites[0].get_rect()
		self.rect = self.cut_transparent_rect(self.idle_sprites[0])
		self.rect.center = (x, y)

		self.idle_rect = self.cut_transparent_rect(self.idle_sprites[0])
		self.run_rect = self.cut_transparent_rect(self.run_sprites[0])

		self.direction = 0

		self.color = (255, 0, 0)
		self.gravity_y = 0.5 # pixels^2 / frame
		self.speed_y = 0
		self.speed_x = 4
		self.health = 100
		self.damage = 5
		self.jump_count = 0
		self.jump_count_max = 4

		self.idle_time = 0
		self.idle_current_sprite = 0
		self.idle_frame_rate = 10

		self.run_time = 0
		self.run_current_sprite = 0
		self.run_frame_rate = 10

		self.dx = 0
		self.dy = 0

		self.on_ground = 0
		
	
	def draw(self, screen):
		pygame.draw.rect(screen, self.color, self.rect)

	def cut_transparent_rect(self, image):
		min_x, min_y = image.get_width(), image.get_height()
		max_x, max_y = 0, 0

		for y in range(image.get_height()):
			for x in range(image.get_width()):
				"""
				get_at retorna a cor e a opacidade de um pixel
				(r, g, b ,a)
				a > 0 signfica que o pixel não é transparente

				então basta fazer um loop pela imagem inteira de forma
				a encontrar melhores valores para a largura e altura do
				sprite que realmente contem o sprite

				claro que é também possivel cortar a imagem manualmente
				"""
				if image.get_at((x, y))[3] > 0:
					min_x = min(min_x, x)
					min_y = min(min_y, y)
					max_x = max(max_x, x)
					max_y = max(max_y, y)

		return pygame.Rect(min_x, min_y, max_x - min_x + 1, max_y - min_y + 1)

	def cut_sheet(self, image, hor_number, ver_number, scale_factor):
		sheet = pygame.image.load(image).convert_alpha()

		width = sheet.get_size()[0] / hor_number
		height = sheet.get_size()[1] / ver_number
		new_width = int(width * scale_factor)
		new_height = int(height * scale_factor)

		frames = []

		for i in range(hor_number):
			frame = sheet.subsurface((i * width, 0, width, height))
			frame = pygame.transform.scale(frame, (new_width, new_height))
			frames.append(frame)

		return frames

	def load_sprites(self, delta, screen):
		frame = None
		position = None

		if self.dx != 0:
			self.run_time += delta

			if self.run_time > 1000 // self.run_frame_rate:
				self.run_current_sprite = (self.run_current_sprite + 1) % len(self.run_sprites)
				self.run_time = 0

			frame = self.run_sprites[self.run_current_sprite]
			position = (self.rect.x - self.rect.width // 3, self.rect.y - self.rect.height // 2.4)

			if self.direction == 1:
				frame = pygame.transform.flip(frame, True, False)
				position = (self.rect.x - self.rect.width // 0.85, self.rect.y - self.rect.height // 2.4)

		else:
			self.idle_time += delta

			if self.idle_time > 1000 // self.idle_frame_rate:
				self.idle_current_sprite = (self.idle_current_sprite + 1) % len(self.idle_sprites)
				self.idle_time = 0

			frame = self.idle_sprites[self.idle_current_sprite]
			position = (self.rect.x - self.rect.width // 5, self.rect.y - self.rect.height // 2.5)

			if self.direction == 1:
				frame = pygame.transform.flip(frame, True, False)
				position = (self.rect.x - self.rect.width*1.35, self.rect.y - self.rect.height // 2.5)

		if not frame or not position:
			return


		screen.blit(frame, position)


	def update(self, plataforms):
		self.speed_y += self.gravity_y
		self.rect.y += self.speed_y
		
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

		self.rect.x += self.dx
		for plataform in plataforms:
			if self.rect.colliderect(plataform):
				if self.dx > 0:
					self.rect.right = plataform.left
				if self.dx < 0:
					self.rect.left = plataform.right

		self.dx = 0
		self.dy = 0

	def on_event(self, event: pygame.event.Event, mouse):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				self._jump()
	
	def _jump(self):
		if self.jump_count >= self.jump_count_max:
			return
		self.speed_y = -15
		self.jump_count += 1

	def on_key_pressed(self, key_map):
		if key_map[pygame.K_d]:
			self.dx = self.speed_x
			self.direction = 0
		elif key_map[pygame.K_a]:
			self.direction = 1
			self.dx = - self.speed_x

	def decrement_health(self, howmuch):
		self.health -= howmuch
		self.die()

	def die(self):
		if self.health <= 0:
			self.alive = False

class GameManager:

	def __init__(self) -> None:
		pygame.init()

		# A tela
		self.width = 1200
		self.height = 1000
		screen_size = (self.width, self.height)
		self.screen = pygame.display.set_mode(screen_size)
		self.screen.fill((0, 0, 0))

		self.font = pygame.font.Font(None, 36) # tamanho 36

		# Objetos
		self.player = Player(220, 425, ["idle.png", "run.png"])
		self.plataforms = mapa1.give_plataforms()

		self.clock = None
		self.is_running = False

		# self.enemy_test = Enemy(650,100,(100,100,100),50,100)


	def run(self):
		# Inicializa o jogo
		self.clock = pygame.time.Clock()
		self.is_running = True

		while self.is_running: 
			delta = self.clock.tick(60)

			self.event()
			self.draw(delta)
			self.update()

		pygame.quit()

 
	def event(self):
		# Eventos
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				self.is_running = False
			self.player.on_event(event, pygame.mouse)

		# Chaves pressionadas no momento
		key_map = pygame.key.get_pressed()
		self.player.on_key_pressed(key_map)

	def update(self):
		self.player.update(self.plataforms)

		# self.enemy_test.seeingplayer = fov.can_see_player(
		#                                 self.enemy_test.rect.center,
		#                                 self.player.rect.center,
		#                                 self.plataforms, 500)
		# self.enemy_test.update(self.plataforms)

		# if not self.enemy_test.seeingplayer and self.enemy_test.roaming:
		#     roaming.roam(self.enemy_test)
		# else:
		#     self.enemy_test.chase(self.player)


	def draw(self, delta):
		# Renderizaçao
		self.screen.fill((255, 255, 255))
		#self.player.draw(self.screen)
		#self.enemy_test.load(self.screen)
		self.player.load_sprites(delta, self.screen)


		mapa1.draw_plataforms(self.screen, self.plataforms, self.height, None)

		pygame.display.flip()

if __name__ == '__main__':
	game = GameManager()
	game.run()