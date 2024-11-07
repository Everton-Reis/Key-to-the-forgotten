import pygame
from mapa2 import Mapa

mapa_layout = [
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
mapa = Mapa(mapa_layout)

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
        self.on_ground = False

        # Carregar imagem do jogador e redimensiona
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (40, 40))

        # Define o retângulo de colisão e posição inicial do sprite
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen, camera_offset):
        # Aplica o deslocamento da câmera
        screen.blit(self.image, (self.rect.x - camera_offset[0], self.rect.y - camera_offset[1]))

    def update(self, plataformas):
        # Aplicar gravidade
        self.speed_y += self.gravity_y
        self.rect.y += self.speed_y

        # Verificar colisão vertical (com plataformas)
        self.on_ground = False
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma):  # colisão vertical
                if self.speed_y > 0:  # Descendo
                    self.rect.bottom = plataforma.top  # Para de cair
                    self.speed_y = 0  # Reseta a velocidade vertical
                    self.on_ground = True  # No chão
                    self.jump_count = 0  # Reseta os saltos
                elif self.speed_y < 0:  # Subindo
                    self.rect.top = plataforma.bottom  # Impede de subir
                    self.speed_y = 0  # Reseta a velocidade vertical

        # Movimentação horizontal
        self.rect.x += self.dx
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma):  # Colisão horizontal
                if self.dx > 0:
                    self.rect.right = plataforma.left
                if self.dx < 0:
                    self.rect.left = plataforma.right

        # Reseta as velocidades
        self.dx = 0
        self.dy = 0

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

class GameManager:

    def __init__(self) -> None:
        pygame.init()

        self.width = 800
        self.height = 600
        
        screen_size = (self.width, self.height)
        self.screen = pygame.display.set_mode(screen_size)
        self.screen.fill((0, 0, 0))

        image_path = r"C:\Users\evert\Documents\TrabalhoLp_A2\0.png"

        # Inicializando o personagem
        self.player = Player(self.width // 2, self.height // 2, 40, 40, image_path)
        self.plataformas = mapa.obter_plataformas()

        # Grupo de sprites
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        self.clock = None
        self.is_running = False
        self.camera_offset = [0, 0]

    def run(self):
        self.clock = pygame.time.Clock()
        self.is_running = True
        while self.is_running:
            self.event()
            self.update()
            self.draw()
            self.clock.tick(30)
        pygame.quit()

    def atualizar_camera(self):
        # Mantém a câmera centralizada no jogador horizontalmente
        self.camera_offset[0] = self.player.rect.centerx - self.width // 2
        # Verticalmente, a câmera seguirá o jogador, mas com um "piso" para evitar ir além do chão
        self.camera_offset[1] = min(self.player.rect.centery - self.height // 2, self.height - 100) # -100 pois são dois blocos
        #min(self.player.rect.centery - self.height // 2, 0)
    def event(self):
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
        self.atualizar_camera()

    def draw(self):
        self.screen.fill((0, 0, 0))
        
        # Desenha o mapa com deslocamento da câmera
        mapa.desenhar(self.screen, self.camera_offset)  
        
        # Desenha o jogador com deslocamento da câmera
        self.player.draw(self.screen, self.camera_offset)
        
        pygame.display.flip()

if __name__ == '__main__':
    game = GameManager()
    game.run()
