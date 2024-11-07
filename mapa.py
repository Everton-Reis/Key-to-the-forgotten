# mapa.py
import pygame

# Configurações do bloco e do mapa
BLOCK_SIZE = 50
BLUE = (0, 0, 255)

class Mapa:
    def __init__(self, layout):
        """
        Inicializa o mapa com o layout fornecido.
        
        :param layout: Lista de listas representando o layout do mapa (1 para bloco, 0 para vazio).
        """
        self.layout = layout
        self.block_size = BLOCK_SIZE
        self.color = BLUE

    def desenhar(self, screen, camera_offset):
        """
        Desenha o mapa de plataformas na tela com base no deslocamento da câmera.

        :param screen: Tela onde os blocos serão desenhados.
        :param camera_offset: Tupla (x, y) representando o deslocamento da câmera.
        """
        for linha_index, linha in enumerate(self.layout):
            for coluna_index, bloco in enumerate(linha):
                if bloco == 1:
                    pos_x = coluna_index * self.block_size - camera_offset[0]
                    pos_y = linha_index * self.block_size - camera_offset[1]
                    pygame.draw.rect(screen, self.color, 
                                     (pos_x, pos_y, self.block_size, self.block_size))

    def obter_plataformas(self):
        """
        Gera e retorna uma lista de retângulos representando as plataformas.

        :return: Lista de objetos pygame.Rect representando as plataformas.
        """
        plataformas = []
        for linha_index, linha in enumerate(self.layout):
            for coluna_index, bloco in enumerate(linha):
                if bloco == 1:
                    plataforma_rect = pygame.Rect(
                        coluna_index * self.block_size,
                        linha_index * self.block_size,
                        self.block_size,
                        self.block_size
                    )
                    plataformas.append(plataforma_rect)
        return plataformas
