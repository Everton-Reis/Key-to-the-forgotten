import pygame

def cut_transparent_rect(image):
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
	frame = None
	position = None

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

def load_sprites_enemy_death(object, delta, screen):
	object.death_time += delta

	if object.death_time % 500 // object.death_frame_rate == 0:
		object.death_current_sprite = (object.death_current_sprite + 1) % len(object.death_sprites)

	frame = object.death_sprites[object.death_current_sprite]
	position = (object.rect.x - object.rect.width * object.death_x, object.rect.y - object.rect.height*object.death_y)

	if object.death_current_sprite == len(object.death_sprites) - 1:
		object.death_time = 0
		object.death_current_sprite = 0

	screen.blit(frame, position)


def load_sprites_enemy_attack(object, delta, screen):
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
