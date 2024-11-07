# mapa.py
import pygame

# Configurações do bloco e do mapa
BLOCK_SIZE = 50
BLOCK_SPEED = 1
BLUE = (0, 0, 255)

# Matriz do mapa (1 = bloco de plataforma, 0 = vazio)
mapa_layout = [
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1,1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1,1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1,1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,1],
    [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,1]
]

def desenhar_mapa(screen, plataformas, size_height):
    for plataforma in plataformas:
        pygame.draw.rect(screen, BLUE, plataforma)

        #removendo os retangulos que saíram da tela
        if plataforma.y > size_height:
            plataformas.remove(plataforma)


def obter_plataformas():
    """Retorna uma lista de retângulos representando as plataformas."""
    plataformas = []
    for linha_index, linha in enumerate(mapa_layout):
        for coluna_index, bloco in enumerate(linha):
            if bloco == 1:
                plataformas.append(pygame.Rect(coluna_index * BLOCK_SIZE, 
                                               linha_index * BLOCK_SIZE, 
                                               BLOCK_SIZE, BLOCK_SIZE))
    return plataformas


def mover_mapa(plataformas):
    for plataforma in plataformas:
        plataforma.y += BLOCK_SPEED