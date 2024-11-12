import pygame
import random
import sys

sys.path.append("./lineofsight")
sys.path.append("./roaming")

import fovdetection as fov
import roaming

BLOCK_SIZE = 50
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

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255, 0, 0)
        self.gravity_y = 0.5 # pixels^2 / frame
        self.speed_y = 0
        self.speed_x = 4
        self.health = 100
        self.damage = 5
        self.jump_count = 0
        self.jump_count_max = 4
        
        self.width = width
        self.height = height

        self.dx = 0
        self.dy = 0

        self.on_ground = 0
    
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
        self.player = Player(220, 425, 25, 25)
        self.plataforms = mapa1.give_plataforms()

        self.clock = None
        self.is_running = False

        self.enemy_test = Enemy(650,100,(100,100,100),50,100)


    def run(self):
        # Inicializa o jogo
        self.clock = pygame.time.Clock()
        self.is_running = True

        while self.is_running:      
            self.event()
            self.update()
            self.draw()
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
        self.enemy_test.seeingplayer = fov.can_see_player(
                                        self.enemy_test.rect.center,
                                        self.player.rect.center,
                                        self.plataforms, 500)
        self.enemy_test.update(self.plataforms)

        if not self.enemy_test.seeingplayer and self.enemy_test.roaming:
            roaming.roam(self.enemy_test)
        else:
            self.enemy_test.chase(self.player)


    def draw(self):
        # Renderizaçao
        self.screen.fill((255, 255, 255))
        self.player.draw(self.screen)
        self.enemy_test.load(self.screen)

        mapa1.draw_plataforms(self.screen, self.plataforms, self.height, None)

        chasing = self.enemy_test.seeingplayer == True
        yes = self.enemy_test.lost_player_timer > 0 and self.enemy_test.seeingplayer == False

        coords_text = f"Posição do jogador: ({self.player.rect.x}, {self.player.rect.y})"
        roaming_text = f"Inimigo está patrulhando : {self.enemy_test.roaming}"
        chasing_text = f"Inimigo está perseguindo jogador : {chasing}"
        lost_text = f"Inimigo está indo na ultima direção em que viu o player : {yes}"
        coords_surface = self.font.render(coords_text, True, (255, 255, 0))  # Texto na cor preta
        roaming_surface = self.font.render(roaming_text, True, (0, 0, 0))
        chasing_surface = self.font.render(chasing_text, True, (0,0,0))
        lost_surface = self.font.render(lost_text, True, (0,0,0))
        self.screen.blit(coords_surface, (10, 10))  # Desenha no canto superior esquerdo da tela
        self.screen.blit(roaming_surface, (10, 590))
        self.screen.blit(chasing_surface, (10, 620))
        self.screen.blit(lost_surface, (10, 650))

        pygame.display.flip()

if __name__ == '__main__':
    game = GameManager()
    game.run()