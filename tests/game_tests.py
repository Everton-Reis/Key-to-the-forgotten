import unittest
from unittest.mock import MagicMock, patch
import pygame
import math

# Definindo as constantes (As constantes PLAYER_INITIAL_SPEED e PLAYER_DISTANCE_DASH são definidas no gamesettings.py.
# foram redefinidas aqui apenas por facilidade de acesso)
PLAYER_INITIAL_SPEED = 4
PLAYER_DISTANCE_DASH = 150

# Uma simulação para a classe Player, com as mesmas funcionalidades Player do player.py
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)  # Supondo que o jogador tenha um tamanho 50x50
        self.alive = True
        self.dx = 0
        self.dy = 0
        self.speed_x = PLAYER_INITIAL_SPEED
        self.dash = 1  # Quantidade de dash possiveis
        self.dash_count = 0  # Quantas vezes o dash foi usado

    def _dash(self, mouse) -> None:
        """
        Aplica dash ao jogador.

        Parâmetros
        ----------
        mouse: objeto pygame.mouse
        """
        if self.dash <= 0 or self.dash_count >= self.dash:
            return

        mouse_pos = mouse.get_pos()

        dx = mouse_pos[0] - self.rect.center[0]
        dy = mouse_pos[1] - self.rect.center[1]

        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance == 0:
            return

        direction_x = dx / distance
        direction_y = dy / distance

        self.rect.x += direction_x * PLAYER_DISTANCE_DASH
        self.rect.y += direction_y * PLAYER_DISTANCE_DASH

        self.dash_count += 1  # Incrementa o contador de dash

    # essa função é para efeitos de teste
    def on_mouse_button_pressed(self, event) -> None:
        """Controla o dash quando o botão direito do mouse é pressionado."""
        if event.button == pygame.BUTTON_RIGHT:
            self._dash(pygame.mouse)  # Passa o mouse para a função _dash

    def on_key_pressed(self, key_map) -> None:
        """Controla os movimentos do jogador."""
        if not self.alive:
            return

        if key_map[pygame.K_d]:
            self.dx = self.speed_x
        elif key_map[pygame.K_a]:
            self.dx = -self.speed_x
        else:
            self.dx = 0  

        self.rect.x += self.dx

    def update(self):
        """Atualiza a posição do jogador."""
        self.rect.x += self.dx


# Testes para a classe Player, incluindo o método _dash
class TestPlayerOnMousePressed(unittest.TestCase):

    def setUp(self):
        """Configura um objeto Player com posição inicial para os testes."""
        self.initial_x = 10
        self.initial_y = 20
        self.player = Player(self.initial_x, self.initial_y)

    def test_initial_position(self):
        """Testa se o jogador é inicializado na posição correta."""
        self.assertEqual(self.player.rect.x, self.initial_x)
        self.assertEqual(self.player.rect.y, self.initial_y)

    def test_move_right(self):
        """Testa se o jogador se move para a direita ao pressionar 'D'."""
        key_map = [False] * 512
        key_map[pygame.K_d] = True  # Simula a tecla 'D' sendo pressionada

        self.player.on_key_pressed(key_map)

        self.assertEqual(self.player.rect.x, self.initial_x + PLAYER_INITIAL_SPEED)

    def test_move_left(self):
        """Testa se o jogador se move para a esquerda ao pressionar 'A'."""
        key_map = [False] * 512
        key_map[pygame.K_a] = True  # Simula a tecla 'A' sendo pressionada

        self.player.on_key_pressed(key_map)

        self.assertEqual(self.player.rect.x, self.initial_x - PLAYER_INITIAL_SPEED)

    def test_no_move(self):
        """Testa se o jogador não se move ao não pressionar nenhuma tecla."""
        key_map = [False] * 512  # Nenhuma tecla pressionada

        self.player.on_key_pressed(key_map)

        self.assertEqual(self.player.rect.x, self.initial_x)

    @patch('pygame.mouse.get_pos', return_value=(100, 100))  # Mock da posição do mouse
    def test_dash(self, mock_get_pos):
        """Testa se o jogador realiza o dash corretamente com o botão direito do mouse."""
        # Simula um click do mouse direito
        event_mock = MagicMock()
        event_mock.button = pygame.BUTTON_RIGHT

        initial_x = self.player.rect.x
        initial_y = self.player.rect.y

        # Executa a função de clique do botão direito
        self.player.on_mouse_button_pressed(event_mock)

        # Verifica se a posição mudou e se o dash foi executado
        self.assertGreater(self.player.rect.x, initial_x)  # O jogador deve ter se movido
        self.assertGreater(self.player.rect.y, initial_y)  # O jogador deve ter se movido
        self.assertEqual(self.player.dash_count, 1)  # O dash foi contado corretamente

    @patch('pygame.mouse.get_pos', return_value=(100, 100))  # Mock da posição do mouse
    def test_no_dash_when_limit_reached(self, mock_get_pos):
        """Testa se o jogador não pode realizar mais de um dash por vez."""

        self.player.dash_count = 1

        # Simula o click direito do mouse
        event_mock = MagicMock()
        event_mock.button = pygame.BUTTON_RIGHT

        # Tenta executar o dash
        self.player.on_mouse_button_pressed(event_mock)

        self.assertEqual(self.player.dash_count, 1)  # O dash não deve ser incrementado novamente

if __name__ == "__main__":
    pygame.init()  # Inicializa o pygame (evitar erros)
    unittest.main()
