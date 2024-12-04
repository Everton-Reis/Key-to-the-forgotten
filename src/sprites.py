import pygame

"""
Responsável por mexer com sprites.
"""

def cut_transparent_rect(image):
	"""
	Corta um retângulo a partir de uma imagem com fundo transparente.

	Parâmetros
	----------
	image: sprite de pygame
	"""
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

def cut_sheet(image, hor_number, ver_number, scale_factor):
	"""
	Corta sprites de uma sheet de sprites a partir do número de sprites na horizontal e na vertical.

	Parâmetros
	----------
	hor_number : int
		Número de sprites na horizontal

	ver_number: int
		Número de sprites na vertical

	scale_factor: float
		Fator de escala
	"""
	sheet = pygame.image.load(image).convert_alpha()

	width = sheet.get_size()[0] / hor_number
	height = sheet.get_size()[1] / ver_number
	new_width = int(width * scale_factor)
	new_height = int(height * scale_factor)

	frames = []

	for i in range(hor_number):
		for j in range(ver_number):
			frame = sheet.subsurface((i * width, j * height, width, height))
			frame = pygame.transform.scale(frame, (new_width, new_height))
			frames.append(frame)


	return frames

def load_sprites_player(object, delta, screen):
	"""
	Carrega sprites idle, death e run de player.

	Parâmetros
	----------
	object: objeto de player

	delta: int
		Intervalo de tempo do jogo.

	screen: tela de pygame
	"""
	frame = None
	position = None

	if object.jump_count > 0:
		frame = object.jump_sprites[0]
		position = (object.rect.x - object.rect.width // 3, object.rect.y - object.rect.height // 2.4)

		if object.direction == 1:
			frame = pygame.transform.flip(frame, True, False)
			position = (object.rect.x - object.rect.width // 0.85, object.rect.y - object.rect.height // 2.4)


	else:
		if object.dx != 0:
			object.run_time += delta

			if object.run_time > 1000 // object.run_frame_rate:
				object.run_current_sprite = (object.run_current_sprite + 1) % len(object.run_sprites)
				object.run_time = 0

			frame = object.run_sprites[object.run_current_sprite]
			position = (object.rect.x - object.rect.width // 3, object.rect.y - object.rect.height // 2.4)

			if object.direction == 1:
				frame = pygame.transform.flip(frame, True, False)
				position = (object.rect.x - object.rect.width // 0.85, object.rect.y - object.rect.height // 2.4)

		else:
			object.idle_time += delta

			if object.idle_time > 1000 // object.idle_frame_rate:
				object.idle_current_sprite = (object.idle_current_sprite + 1) % len(object.idle_sprites)
				object.idle_time = 0

			frame = object.idle_sprites[object.idle_current_sprite]
			position = (object.rect.x - object.rect.width // 5, object.rect.y - object.rect.height // 2.5)

			if object.direction == 1:
				frame = pygame.transform.flip(frame, True, False)
				position = (object.rect.x - object.rect.width*1.35, object.rect.y - object.rect.height // 2.5)


	if not frame or not position:
		return

	screen.blit(frame, position)


def load_sprites_boss_death(object, delta, screen):
	"""
	Carrega sprites death de boss.

	Parâmetros
	----------
	object: objeto de boss

	delta: int
		Intervalo de tempo do jogo.

	screen: tela de pygame
	"""
	object.death_time += delta

	if object.death_time % 500 // object.death_frame_rate == 0:
		object.death_current_sprite = (object.death_current_sprite + 1) % len(object.death_sprites)

	frame = object.death_sprites[object.death_current_sprite]
	position = (object.rect.x - object.rect.width * object.death_x, object.rect.y - object.rect.height*object.death_y)

	if object.death_current_sprite == len(object.death_sprites) - 1:
		object.death_count += 1
		object.death_current_sprite = 0

		if object.death_count == object.max_death_count:
			object.death_time = 0
			return

	screen.blit(frame, position)

def load_sprites_boss_birth(object, delta, screen):
	"""
	Carrega sprites birth de boss.

	Parâmetros
	----------
	object: objeto de boss

	delta: int
		Intervalo de tempo do jogo.

	screen: tela de pygame
	"""
	object.birth_time += delta

	if object.birth_time % 500 // object.birth_frame_rate == 0:
		object.birth_current_sprite = (object.birth_current_sprite + 1) % len(object.birth_sprites)

	frame = object.birth_sprites[object.birth_current_sprite]
	position = (object.rect.x - object.rect.width * object.birth_x, object.rect.y - object.rect.height*object.birth_y)

	if object.birth_current_sprite == len(object.birth_sprites) - 1:
		object.birth_count += 1
		object.birth_current_sprite = 0

		if object.birth_count == object.max_birth_count:
			object.birth_time = 0
			return

	screen.blit(frame, position)

def load_sprites_enemy_death(object, delta, screen):
	"""
	Carrega sprites death de inimigo.

	Parâmetros
	----------
	object: objeto de inimigo

	delta: int
		Intervalo de tempo do jogo.

	screen: tela de pygame
	"""
	object.death_time += delta

	if object.death_time % 500 // object.death_frame_rate == 0:
		object.death_current_sprite = (object.death_current_sprite + 1) % len(object.death_sprites)

	frame = object.death_sprites[object.death_current_sprite]
	position = (object.rect.x - object.rect.width * object.death_x, object.rect.y - object.rect.height*object.death_y)

	if object.death_current_sprite == len(object.death_sprites) - 1:
		object.death_time = 0
		return

	screen.blit(frame, position)


def load_sprites_enemy_attack(object, delta, screen):
	"""
	Carrega sprites attack de inimigo.

	Parâmetros
	----------
	object: objeto de inimigo

	delta: int
		Intervalo de tempo do jogo.

	screen: tela de pygame
	"""
	object.attack_time += delta

	if object.attack_time % 200 // object.attack_frame_rate == 0:
		object.attack_current_sprite = (object.attack_current_sprite + 1) % len(object.attack_sprites)

	frame = object.attack_sprites[object.attack_current_sprite]
	position = (object.rect.x - object.rect.width * object.attack_x_0, object.rect.y - object.rect.height*object.attack_y_0)

	if object.attack_current_sprite == len(object.attack_sprites) - 1:
		object.attack_time = 0
		object.attack_current_sprite = 0

	if object.direction == 1:
		frame = pygame.transform.flip(frame, True, False)
		position = (object.rect.x - object.rect.width * object.attack_x_1, object.rect.y - object.rect.height*object.attack_y_1)

	screen.blit(frame, position)

def load_sprites_enemy_walk(object, delta, screen):
	"""
	Carrega sprites walk de inimigo.

	Parâmetros
	----------
	object: objeto de inimigo

	delta: int
		Intervalo de tempo do jogo.

	screen: tela de pygame
	"""
	object.walk_time += delta

	if object.walk_time > 1000 // object.walk_frame_rate:
		object.walk_current_sprite = (object.walk_current_sprite + 1) % len(object.walk_sprites)
		object.walk_time = 0

	frame = object.walk_sprites[object.walk_current_sprite]
	position = (object.rect.x - object.rect.width * object.walk_x_0, object.rect.y - object.rect.height * object.walk_y_0)

	if object.direction == 1:
		frame = pygame.transform.flip(frame, True, False)
		position = (object.rect.x - object.rect.width * object.walk_x_1, object.rect.y - object.rect.height * object.walk_y_1)

	screen.blit(frame, position)


def load_sprites_enemy_idle(object, delta, screen):
	"""
	Carrega sprites idle de inimigo.

	Parâmetros
	----------
	object: objeto de inimigo

	delta: int
		Intervalo de tempo do jogo.

	screen: tela de pygame
	"""
	object.idle_time += delta

	if object.idle_time > 1000 // object.idle_frame_rate:
		object.idle_current_sprite = (object.idle_current_sprite + 1) % len(object.idle_sprites)
		object.idle_time = 0

	frame = object.idle_sprites[object.idle_current_sprite]
	position = (object.rect.x - object.rect.width * object.idle_x_0, object.rect.y - object.rect.height*object.idle_y_0)

	if object.direction == 1:
		frame = pygame.transform.flip(frame, True, False)
		position = (object.rect.x - object.rect.width * object.idle_x_1, object.rect.y - object.rect.height*object.idle_y_1)

	screen.blit(frame, position)
