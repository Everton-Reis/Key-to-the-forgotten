import pygame

class LifeBar(pygame.sprite.Sprite):
    def __init__(self, player, name, screen):
        super().__init__()
        self.player = player
        self.screen = screen

        self.x = None
        self.y = None
            
        self.current_health = self.player.health
        #self.target_health = 500
        self.max_health = player.MAX_HEALTH
        self.health_bar_length = None
        self.bar_color = None

        if name == "player":
            self.x = 10
            self.y = 45
            self.health_bar_length = 250
            self.bar_color = (255, 0, 0)
        if name == "boss":
            self.x = 700
            self.y = 45
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
        self.target_health = min(self.player.health, self.max_health)
        self.life_bar_health()

    def life_bar_health(self):
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
        health_bar =pygame.Rect(self.x, self.y, health_bar_width, 25)
        transition_bar = pygame.Rect(health_bar.right, 45, transition_width, 25)
        transition_bar.normalize()
        pygame.draw.rect(self.screen, self.bar_color, health_bar)
        pygame.draw.rect(self.screen, transition_color, transition_bar)
        pygame.draw.rect(self.screen, (0, 0, 0), (self.x, self.y, self.health_bar_length, 25), 4)