import pygame
import math

class Weapon():
    def __init__(self, player, image, size):
        """
        Inicializa objeto de classe Weapon

        Parâmetros
        ----------
        player: objeto de player

        image: str
            Caminho contendo sprite.

        size: tuple(float, float)
            Tamanho a considerar para a sprite.
        """
        self.player = player
        self.image = image
        self.size = size
        self.surface = None
        self.position = self.player.rect.center

    def create_weapon(self) -> None:
        """
        Cria arma.
        """
        weapon_surface = pygame.image.load(self.image)
        weapon_surface = pygame.transform.scale(weapon_surface, self.size)
        self.surface = weapon_surface

    def get_angle_to_mouse(self, mouse_pos) -> float:
        """
        Calcula angulo entre mouse e eixo horizontal.

        Parâmetros
        ----------
        mouse_pos : tuple(float, float)
            Posição do mouse
        """
        dx = mouse_pos[0] - self.position[0]
        dy = mouse_pos[1] - self.position[1]
        angle = math.degrees(math.atan2(dy, dx))
        return -(angle + 90)

    def point_mouse(self, mouse_pos, screen) -> None:
        """
        Direciona arma ao mouse.

        Parâmetros
        ----------
        mouse_pos: tuple(float, float)
            Posição do mouse

        screen: tela de pygame
        """
        self.position = self.player.rect.center
        angle = self.get_angle_to_mouse(mouse_pos)

        rotated_weapon = pygame.transform.rotate(self.surface, angle)
        rotated_weapon_rect = rotated_weapon.get_rect(center = self.position)

        screen.blit(rotated_weapon, rotated_weapon_rect)
