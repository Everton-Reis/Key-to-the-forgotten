import pygame

from scripts.mapa import Map
import scripts.followmouse as libat
import scripts.enemy as liben

Mapa = Map()

class Player:

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255, 0, 0)
        self.gravity_y = 0.5 # pixels^2 / frame
        self.speed_y = 0
        self.speed_x = 4
        self.health = 1000
        self.MAX_HEALTH = 1000
        self.damage = 5
        self.jump_count = 0
        self.jump_count_max = 4
        
        self.width = width
        self.height = height

        self.dx = 0
        self.dy = 0

        self.on_ground = 0

        self.bullets = libat.Bullets()
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

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
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                bullet = libat.Bullet((self.rect.x + (self.width // 2), self.rect.y + (self.height // 2)), 
                                      (mouse.get_pos()[0], mouse.get_pos()[1]),
                                      5,
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
            pygame.quit() # por enquanto

class LifeBar(pygame.sprite.Sprite):
    def __init__(self, player, screen):
        super().__init__()
        self.player = player
        self.screen = screen

        self.current_health = self.player.health
        #self.target_health = 500
        self.max_health = player.MAX_HEALTH
        self.health_bar_length = 400
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
        health_bar =pygame.Rect(10, 45, health_bar_width, 25)
        transition_bar = pygame.Rect(health_bar.right, 45, transition_width, 25)
        transition_bar.normalize()
        pygame.draw.rect(self.screen, (255, 0, 0), health_bar)
        pygame.draw.rect(self.screen, transition_color, transition_bar)
        pygame.draw.rect(self.screen, (255, 255, 255), (10, 45, self.health_bar_length, 25), 4)


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
        self.player = Player(self.width // 2, (self.height // 2) - 20, 25, 25) ####
        self.lifebar_def = LifeBar(self.player, self.screen)


        self.plataforms, self.standing_plataforms = Mapa.give_plataforms()
        #self.standing_plataforms = Mapa.standing_plataforms

        self.clock = None
        self.is_running = False

        self.camera_speed = 500
        self.shoot_speed = 500

        self.camera_offset = [0, 0]

        self.enemies = liben.Enemies()

    def run(self):
        # Inicializa o jogo
        self.clock = pygame.time.Clock()
        self.is_running = True

        time_map = 0
        time_shoot_enemy = 0

        #self.enemies.create_random_enemies(self.standing_plataforms, 5)

        while self.is_running:      
            delta = self.clock.tick(60)
            time_map += delta
            time_shoot_enemy += delta

            if time_map >= self.camera_speed:
                Mapa.move_map(self.plataforms)
                time_map = 0

            # if time_shoot_enemy >= self.shoot_speed:
            #     self.enemies.shoot_attack(self.player, self.screen)
            #     time_shoot_enemy = 0

            self.event()
            self.update()
            self.lifebar_def.update()
            self.draw()
        pygame.quit()

    def update_camera(self):
        self.camera_offset[0] = self.player.rect.centerx - self.width // 2
        self.camera_offset[1] = min(self.player.rect.centery - self.height //2, self.height - 100)

    def event(self):
        # Eventos
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.is_running = False
            self.player.on_event(event, pygame.mouse)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.player.increment_health(200)
                    #self.lifebar_def.get_health(200)
                if event.key == pygame.K_DOWN:
                    self.player.decrement_health(200)
                    
        # Chaves pressionadas no momento
        key_map = pygame.key.get_pressed()
        self.player.on_key_pressed(key_map)

    # def check_player_collision(self):
    #     for enemy in self.enemies.enemies:
    #         if self.player.rect.colliderect(enemy.rect):
    #             if self.player.dx > 0:
    #                 self.player.rect.right = enemy.rect.left
    #                 enemy.rect.right = self.player.rect.left
    #             elif self.player.dx < 0:
    #                 self.player.rect.left = enemy.rect.right
    #                 enemy.rect.left = self.player.rect.right
    #             if self.player.speed_y > 0:
    #                 self.player.rect.bottom = enemy.rect.top
    #                 self.player.speed_y = 0
    #                 enemy.rect.bottom = self.player.rect.top
    #             elif self.player.speed_y < 0:
    #                 self.player.rect.top = enemy.rect.bottom
    #                 self.player.speed_y = 0
    #                 enemy.rect.top = self.player.rect.bottom


    def update(self):
        self.player.update(self.plataforms)
        #self.enemies.update(self.plataforms)
        #self.check_player_collision()
        self.update_camera()

    def draw(self):
        # Renderizaçao
        self.screen.fill((255, 255, 255))
        Mapa.draw_background(self.screen)
        self.player.draw(self.screen)



        self.player.bullets.shoot(self.screen, self.enemies.enemies, self.plataforms, self.player)
        # self.enemies.load(self.screen)
        # self.enemies.shoot_bullets(self.player, self.plataforms, self.screen)
        # self.enemies.mov_attack(self.player)
        # self.enemies.move(self.player)
        # self.enemies.check_die()

        Mapa.draw_plataforms(self.screen, self.plataforms, self.height, self.camera_offset)

        coords_text = f"Posição do jogador: ({self.player.rect.x}, {self.player.rect.y})"
        coords_surface = self.font.render(coords_text, True, (255, 255, 0))  # Texto na cor preta
        self.screen.blit(coords_surface, (10, 10))  # Desenha no canto superior esquerdo da tela

        self.lifebar_def.life_bar_health()

        pygame.display.flip()

if __name__ == '__main__':
    game = GameManager()
    game.run()