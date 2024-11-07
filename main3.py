import pygame
from mapa import desenhar_mapa, obter_plataformas, mover_mapa

plataformas = obter_plataformas()

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path):
        super().__init__()

        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255, 0, 0)
        self.gravity_y = 0.5
        self.speed_y = 0
        self.jump_count = 0
        self.jump_count_max = 3
        self.dx = 0
        self.dy = 0
        self.velocidade = 3
        self.on_ground = False # verificar se estpa no chão

        # carregar imagem do jogador e redimensiona
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (40, 40))

        # define o retangulo de colisão e posição inicial do sprite
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        #pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.image, self.rect)
    
    def update(self, plataformas):
        # Aplicar gravidade
        self.speed_y += self.gravity_y
        self.rect.y += self.speed_y

        # Verificar colisão vertical (com plataformas)
        self.on_ground = False
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma): # colisão horizontal
                if self.speed_y > 0: # ta caindo
                    self.rect.bottom = plataforma.top # para de cair
                    self.speed_y = 0 # reseta a velocidade vertical
                    self.on_ground = True # ta no chão
                    self.jump_count = 0 # reseta os saltos
                elif self.speed_y < 0: # ta subindo
                    self.rect.top = plataforma.bottom # impedir que suba
                    self.speed_y = 0 # reseta a velocidade vertical

        # movimentação horizontal 
        self.rect.x += self.dx
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma):
                if self.dx > 0:
                    self.rect.right = plataforma.left
                if self.dx < 0:
                    self.rect.left = plataforma.right

        self.dx = 0


    def on_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Verifica se está no chão
                self._jump()  

    def _jump(self):
        if self.jump_count >= self.jump_count_max:
            return
        self.speed_y = -10
        self.jump_count += 1

    def on_key_pressed(self, key_map):
        if key_map[pygame.K_a]:  # Move para a esquerda
            self.dx = -self.velocidade
        if key_map[pygame.K_d]:  # Move para a direita
            self.dx = self.velocidade
        # if key_map[pygame.K_w]:  # Move para cima
        #     self.dy = -self.velocidade
        # if key_map[pygame.K_s]:  # Move para baixo
        #     self.dy = self.velocidade

class Ground:
    pass
class GameManager:

    def __init__(self) -> None:
        pygame.init()

        self.width = 800
        self.height = 600
        screen_size = (self.width, self.height)
        self.screen = pygame.display.set_mode(screen_size)
        self.screen.fill((0, 0, 0))

        # Caminho para a imagem do jogador
        image_path = r"0.png"  # Altere para o caminho correto

        # iniciando o personagem
        self.player = Player(self.width // 2, self.height // 2, 40, 40, image_path)
        self.plataformas = obter_plataformas()

        # Criando o grupo de sprites (no caso, só o jogador)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        self.clock = None
        self.is_running = False

        self.camera_speed = 50 #quanto menor o numero, mais rapido
        self.time = 0

    def run(self):
        # iniciar o jogo
        self.clock = pygame.time.Clock()
        self.is_running = True
        while self.is_running:
            delta = self.clock.tick(30)
            self.time += delta

            if self.time > self.camera_speed:
                mover_mapa(self.plataformas)
                self.time = 0

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
            self.player.on_event(event)
        
        # Atualizando os sprites
        self.all_sprites.update(self.plataformas)

        # Teclas pressionadas no momento
        key_map = pygame.key.get_pressed()
        self.player.on_key_pressed(key_map)

    def update(self):
        self.player.update(self.plataformas)
    
    def collision_detetion(self):
        pass
    
    def draw(self):
        # renderização
        self.screen.fill((0, 0, 0))
        desenhar_mapa(self.screen, self.plataformas, self.height)
        self.player.draw(self.screen)
        pygame.display.flip()

if __name__ == '__main__':
    game = GameManager()
    game.run()