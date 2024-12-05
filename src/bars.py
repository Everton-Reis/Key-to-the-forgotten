import pygame

class LifeBar(pygame.sprite.Sprite):
	def __init__(self, player, name):
		super().__init__()
		self.player = player

		self.x = None
		self.y = None
			
		self.current_health = self.player.health
		self.target_health = 500
		self.max_health = player.MAX_HEALTH
		self.health_bar_length = None
		self.bar_color = None

		if name == "player":
			self.x = 10
			self.y = 75
			self.health_bar_length = 250
			self.bar_color = (255, 0, 0)
		if name == "boss":
			self.x = 700
			self.y = 75
			self.health_bar_length = 450
			self.bar_color = (0, 255, 0)

		self.health_ratio = self.max_health / self.health_bar_length
		self.health_change_speed = 5

	def get_damage(self, amount):
		if self.target_health > 0:
			self.target_health -= amount
		if self.target_health < 0:
			self.target_health = 0
	
	def get_health(self, amount):
		if self.target_health < self.max_health:
			self.target_health += amount
		if self.target_health > self.max_health:
			self.target_health = self.max_health
	
	def update(self):
		self.max_health = self.player.MAX_HEALTH
		self.health_ratio = self.max_health / self.health_bar_length
		
		self.target_health = min(self.player.health, self.max_health)

	def life_bar_health_draw(self, screen):
		transition_width = 0
		transition_color = (255, 0, 0)
		
		if self.current_health < self.target_health:
			self.current_health +=self.health_change_speed
			transition_width = int((self.target_health - self.current_health) / self.health_ratio)
			transition_color = (0, 255, 0)
		
		if self.current_health > self.target_health:
			self.current_health -= self.health_change_speed
			transition_width = int((self.target_health - self.current_health)/ self.health_ratio)
			transition_color = (255, 255, 0)
		
		health_bar_width = int(min(self.current_health, self.max_health) / self.health_ratio)
		health_bar = pygame.Rect(self.x, self.y, health_bar_width, 25)
		pygame.draw.rect(screen, self.bar_color, health_bar, border_radius = 10)
		pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.health_bar_length, 25), 4, border_radius = 10)

class ExpBar():
	def __init__(self, player):
		self.player = player
		self.length = 200
		self.current_exp = self.player.total_exp
		self.color = (100,100,100)
		self.x = 10
		self.y = 110
		self.ratio = self.player.next_level / self.length
		self.change_speed = 5
		self.target_exp = 0

	def update(self):
		total_exp = self.player.next_level - self.player.calc_exp(self.player.level)
		if self.player.level == 1:
			total_exp = 100
		if self.target_exp < total_exp:
			self.target_exp = self.player.total_exp - self.player.calc_exp(self.player.level)
			if self.target_exp <= 0:
				self.target_exp = self.player.total_exp

		if self.target_exp > total_exp:
			self.target_exp = 0

	def exp_bar_draw(self, screen):
		total_exp = self.player.next_level - self.player.calc_exp(self.player.level) 
		if self.player.level == 1:
			total_exp = 100

		self.ratio = total_exp / self.length
		transition_width = 0
		transition_color = (190, 0, 100)
		
		if self.current_exp < self.target_exp:
			self.current_exp +=self.change_speed
			transition_width = int((self.target_exp - self.current_exp) / self.ratio)
		
		if self.current_exp > self.target_exp:
			self.current_exp -= self.change_speed
			transition_width = int((self.target_exp - self.current_exp)/ self.ratio)

		exp_bar_width = int(min(self.target_exp, total_exp) / self.ratio)
		exp_bar = pygame.Rect(self.x, self.y, exp_bar_width, 15)
		transition_bar = pygame.Rect(exp_bar.right, self.y, transition_width, 15)
		transition_bar.normalize()
		pygame.draw.rect(screen, self.color, exp_bar, border_radius = 5)
		pygame.draw.rect(screen, transition_color, transition_bar, border_radius = 5)
		pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.length, 15), 4, border_radius = 5)