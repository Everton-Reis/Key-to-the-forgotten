import pygame, sys
from pytmx.util_pygame import load_pygame
from Setings import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)


    def draw(self, screen):
        screen.blit(self.image, self.rect)

tiles_sprite_group = pygame.sprite.Group()
background1_sprite_group = pygame.sprite.Group()

 


# Map
tmx_data = load_pygame('data/tmx/mapa_fase1.tmx') # carrega o arquivo com o mapa
visible_layers = tmx_data.layernames #pega as camadas visíveis (nesse caso, as com sprites)
correction = 90 - ROWS # Correção da Altura para encaixar na Tela (Temporário)

# get layers
print(tmx_data.layernames) #printa todas as camadas (debug)

# get tiles
layer_tile = tmx_data.get_layer_by_name('tiles') #camada principal

for x,y,surf in layer_tile.tiles(): # montando o mapa no jogo
    surf = surf.convert_alpha()
    x_pos = (x+MARGIN)*TILE_SIZE
    y_pos = (y-correction)*TILE_SIZE
    pos = (x_pos, y_pos)
    tiles_sprite_group.add(Tile(pos,surf, tiles_sprite_group))


# get background
paralax_sprite_group = pygame.sprite.Group()
surf = pygame.image.load('data/fundo.png').convert_alpha()

x = MARGIN*TILE_SIZE
y = 0
pos = (x, y)
fundo = Tile(pos, surf,paralax_sprite_group) #posiciona o fundo no lugar certo

# get objects
# object_layer = tmx_data.get_layer_by_name('Objects') - esse layer ainda não existe
# for obj in object_layer:
#   if obj.type == 'Shape':
#       if obj.name == 'Rectangle':
#           (PAREDES PARA COLISÃO)



run = True
while run:


     # Eventos
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit
   

    # Update
    screen.fill((0,0,0))
    fundo.draw(screen)
    tiles_sprite_group.draw(screen)

    
    pygame.display.update()