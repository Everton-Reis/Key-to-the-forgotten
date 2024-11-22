# mapa.py
import pygame, sys
from pytmx.util_pygame import load_pygame
from Setings import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Configurações do bloco e do mapa
BLOCK_SPEED = 1
BLOCK_SIZE = 50
BLUE = (0, 0, 255)

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups):
        super().__init__(groups)
        self.image = surface.convert()
        self.rect = self.image.get_rect(topleft = pos)


    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
class Map():
    def __init__(self):

        self.tiles_sprite_group = pygame.sprite.Group()
        self.background1_sprite_group = pygame.sprite.Group()


        # Map
        self.tmx_data = load_pygame('data/tmx/mapa_fase1.tmx') # carrega o arquivo com o mapa
        self.correction = 83 - ROWS # Correção da Altura para encaixar na Tela (Temporário)

        # get tiles
        self.layer_tile = self.tmx_data.get_layer_by_name('tiles') #camada principal
        for x,y,surf in self.layer_tile.tiles(): # montando o mapa no jogo
            surf = surf.convert_alpha()
            x_pos = (x+MARGIN)*TILE_SIZE
            y_pos = (y-self.correction)*TILE_SIZE
            pos = (x_pos, y_pos)
            self.tiles_sprite_group.add(Tile(pos,surf, self.tiles_sprite_group))

        # get background
        self.paralax_sprite_group = pygame.sprite.Group()
        surf = pygame.image.load('data/fundo2.png').convert_alpha()
        x = MARGIN*TILE_SIZE
        y = -240 # Hardcode temporário
        pos = (x, y)
        self.fundo = Tile(pos, surf,self.paralax_sprite_group) #posiciona o fundo no lugar certo


    def draw_plataforms(self,screen, plataforms, height, camera_offset): #sugestão draw_scenario
        # """Desenha o mapa de plataformas na tela."""
        self.tiles_sprite_group.draw(screen)

        # Debug: vizualização dos colisores
        # for plataform in plataforms:
        #     pygame.draw.rect(screen, BLUE, plataform)
        

    def draw_background(self, screen):
        self.fundo.draw(screen)

    def give_plataforms(self):
        # """Retorna uma lista de retângulos representando as plataformas."""
        plataformas = []
        standing_plataforms = []
        object_layer = self.tmx_data.get_layer_by_name('colisões')
        for obj in object_layer:
            rect = pygame.Rect(obj.x + MARGIN*TILE_SIZE ,obj.y - self.correction*TILE_SIZE,obj.width, obj.height)

            if obj.name == 'floor':
                standing_plataforms.append(rect)

            plataformas.append(rect)

        return plataformas, standing_plataforms

    def move_map(self, plataformas):
        for plataforma in plataformas:
            plataforma.y += BLOCK_SPEED
        for tile in self.tiles_sprite_group:
            tile.rect.y += BLOCK_SPEED
        self.fundo.rect.y += BLOCK_SPEED * 0.8
