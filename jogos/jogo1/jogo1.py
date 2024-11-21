import pygame
import sys

sys.path.append("../../implementacoes/atirar")
sys.path.append("../../implementacoes/inimigos")
sys.path.append("../../implementacoes/player")
sys.path.append("../../implementacoes/lifebar")
sys.path.append("../../implementacoes/mapa")

from mapa import Map

import player
import enemy3_0 as liben
import lifebar as Life

mapa1 = Map()

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
        self.player = player.Player(self.width // 2, self.height // 2, 25, 25)
        self.lifebar = Life.LifeBar(self.player, self.screen)

        self.plataforms = mapa1.give_plataforms()
        self.standing_plataforms = mapa1.standing_plataforms

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

        self.enemies.create_random_enemies(self.standing_plataforms, 2)

        while self.is_running:      
            delta = self.clock.tick()
            time_map += delta
            time_shoot_enemy += delta

            if time_map >= self.camera_speed:
                mapa1.move_map(self.plataforms)
                time_map = 0

            if time_shoot_enemy >= self.shoot_speed:
                self.enemies.shoot_attack(self.player, self.plataforms, self.screen)
                time_shoot_enemy = 0

            self.event()
            self.update()
            self.lifebar.update()
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

        # Chaves pressionadas no momento
        key_map = pygame.key.get_pressed()
        self.player.on_key_pressed(key_map)

    def update(self):
        self.player.update(self.plataforms, self.enemies)
        self.enemies.update(self.plataforms, self.player, self.enemies)
        self.update_camera()

    def draw(self):
        # Renderizaçao
        self.screen.fill((255, 255, 255))
        self.player.draw(self.screen)
        self.player.bullets.shoot(self.screen, self.enemies.enemies, self.plataforms, self.player)
        self.enemies.load(self.screen)
        self.enemies.shoot_bullets(self.player, self.plataforms, self.screen)
        self.enemies.mov_attack(self.player, self.plataforms)
        self.enemies.check_die()

        mapa1.draw_plataforms(self.screen, self.plataforms, self.height, self.camera_offset)

        coords_text = f"Posição do jogador: ({self.player.rect.x}, {self.player.rect.y})"
        coords_surface = self.font.render(coords_text, True, (255, 255, 0))  # Texto na cor preta
        self.screen.blit(coords_surface, (10, 10))  # Desenha no canto superior esquerdo da tela

        self.lifebar.life_bar_health()

        pygame.display.flip()

if __name__ == '__main__':
    game = GameManager()
    game.run()