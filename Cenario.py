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
# background1_sprite_group = pygame.sprite.Group()

    


# Map
tmx_data = load_pygame('data/tmx/mapa1.tmx')
visible_layers = tmx_data.layernames
correction = 90 - ROWS # Correção da Altura para encaixar na Tela (Temporário)

# get layers
print(tmx_data.layernames)

# get tiles
layer_tile = tmx_data.get_layer_by_name('tiles')

for x,y,surf in layer_tile.tiles():
    surf = surf.convert_alpha()
    x_pos = (x+MARGIN)*TILE_SIZE
    y_pos = (y-correction)*TILE_SIZE
    pos = (x_pos, y_pos)
    tiles_sprite_group.add(Tile(pos,surf, tiles_sprite_group))

# # get background 1
# background1_layer = tmx_data.get_layer_by_name('background 1')
# for x,y,surf in background1_layer.tiles():
#     surf = surf.convert_alpha()
#     x_pos = (x+MARGIN)*TILE_SIZE
#     y_pos = (y-correction)*TILE_SIZE
#     pos = (x_pos, y_pos)
#     background1_sprite_group.add(Tile(pos,surf, background1_sprite_group))

# # get background 2
# background2_sprite_group = pygame.sprite.Group()
# background2_layer = tmx_data.get_layer_by_name('background 2')
# for x,y,surf in background2_layer.tiles():
#     x_pos = (x+MARGIN)*TILE_SIZE
#     y_pos = (y-correction)*TILE_SIZE
#     pos = (x_pos, y_pos)
#     background2_sprite_group.add(Tile(pos,surf, background2_sprite_group))

# get background 3
paralax_sprite_group = pygame.sprite.Group()
surf = pygame.image.load('data/fundo.png').convert_alpha()

x = MARGIN*TILE_SIZE
y = 0
pos = (x, y)
fundo = Tile(pos, surf,paralax_sprite_group)

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
    background2_sprite_group.draw(screen)
    background1_sprite_group.draw(screen)
    tiles_sprite_group.draw(screen)

    
    pygame.display.update()