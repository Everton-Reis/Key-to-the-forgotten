import pygame
from game import GameManager 
import os

current_dir = os.path.dirname("menu.py")
font_path = os.path.join(current_dir, "../../sprites/menu/PressStart2P_Regular.ttf")

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1000

class Button:
	"""
	Classe que representa os botões do jogo.

	Parâmetros
	----------
	x : int
		A coordenada x do botão.
	y : int
		A coordenada y do botão.
	width : int
		A largura do botão.
	height : int
		A altura do botão.
	text : str
		O texto exibido no botão.
	callback : function
		A função que será executada ao clicar no botão.
	fontsize : int, opcional
		O tamanho da fonte do texto no botão (valor padrão é 36).
	"""
	def __init__(self, x, y, width, height, text, callback, fontsize=36):
		self.rect = pygame.Rect(x, y, width, height)
		self.text = text
		self.font = pygame.font.Font(font_path, fontsize)
		self.callback = callback

		self.color_default = "white"
		self.color_hover = "red"
		self.color_current = self.color_default

	def draw(self, screen):
		"""
		Desenha o botão na tela.

		Parâmetros
		----------
		screen : pygame.Surface
			A superfície onde o botão será desenhado.
		"""
		pygame.draw.rect(screen, self.color_current, self.rect)
		text_box = self.font.render(self.text, True, "black")
		text_box_rect = text_box.get_rect(center=self.rect.center)
		screen.blit(text_box, text_box_rect)

	def on_event(self, event):
		"""
		Verifica e responde aos eventos do mouse sobre o botão.

		Parâmetros
		----------
		event : pygame.event
			O evento que está sendo processado.
		"""
		if event.type == pygame.MOUSEBUTTONDOWN:
			if self.rect.collidepoint(event.pos) and event.button == 1:
				self.callback()
			
		if event.type == pygame.MOUSEMOTION:
			if self.rect.collidepoint(event.pos):
				self.color_current = self.color_hover
			else:
				self.color_current = self.color_default


class MainMenu:
	"""
	Classe que representa o menu principal do jogo.

	Parâmetros
	----------
	manager : pygame.game
		A instância do gerenciador do jogo.
	"""
	def __init__(self, manager): 
		self.manager = manager
		self.start_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50, "Start", self.start_callback)
		self.exit_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50, "Exit", self.exit_callback)

		self.font = pygame.font.Font(None, 200)

	def draw(self, screen):
		"""
		Desenha o menu principal na tela.

		Parâmetros
		----------
		screen : pygame.Surface
			A superfície onde o menu será desenhado.
		"""
		screen.fill((0, 0, 0))
		self.start_button.draw(screen)
		self.exit_button.draw(screen)
		
		menu_text = f"MENU"
		menu_surface = self.font.render(menu_text, True, (255, 0, 0))
		screen.blit(menu_surface, (400, 200))

		pygame.display.flip()
	
	def event(self, event):
		"""
		Processa eventos do menu principal.

		Parâmetros
		----------
		event : pygame.event
			O evento a ser processado.
		"""
		self.start_button.on_event(event)
		self.exit_button.on_event(event)

	def start_callback(self):
		"""Altera o estado do jogo para o nível principal."""
		self.manager.change_state("game_level")

	def exit_callback(self):
		"""Finaliza o jogo."""
		self.manager.is_running = False


class GameOver:
	"""
	Classe que representa a tela de Game Over.
	
	Parâmetros
	----------
	manager : pygame.game
		A instância do gerenciador do jogo.
	screen : pygame.Surface
		A superfície onde a tela será exibida.
	"""
	def __init__(self, manager, screen):
		self.manager = manager
		self.screen = screen
		self.reset_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50, "Reset", self.reset_callback)
		self.exit_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50, "Exit", self.exit_callback)

		self.font = pygame.font.Font(None, 200)

	def draw(self, screen):
		"""
		Desenha a tela de Game Over.

		Parâmetros
		----------
		screen : pygame.Surface
			A superfície onde a tela será desenhada.
		"""
		screen.fill((0, 0, 0))
		self.reset_button.draw(screen)
		self.exit_button.draw(screen)

		game_over_text = f"GAME OVER"
		game_over_surface = self.font.render(game_over_text, True, (255, 0, 0))
		screen.blit(game_over_surface, (200, 200))

		pygame.display.flip()
	
	def event(self, event):
		"""
		Processa eventos da tela de Game Over.

		Parâmetros
		----------
		event : pygame.event
			O evento a ser processado.
		"""
		self.reset_button.on_event(event)
		self.exit_button.on_event(event)

	def reset_callback(self):
		"""Reinicia o nível do jogo."""
		del self.manager.states["game_level"]
		self.manager.states["game_level"] = GameManager(self.manager, self.screen)
		self.manager.change_state("game_level")

	def exit_callback(self):
		"""Finaliza o jogo."""
		self.manager.is_running = False

	# Método de verificação necessário para evitar erros quando a change_state é ativada.
	def verify_win(self, change_state):
		pass


class GameWin:
	"""
	Classe que representa a tela de vitória do jogo.
	
	Parâmetros
	----------
	manager : pygame.game
		A instância do gerenciador do jogo.
	screen : pygame.Surface
		A superfície onde a tela será exibida.
	"""
	def __init__(self, manager, screen):
		self.manager = manager
		self.screen = screen
		self.menu_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50, "Menu", self.menu_callback)
		self.exit_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50, "Exit", self.exit_callback)

		self.font = pygame.font.Font(None, 200)
	def draw(self, screen):
		"""
		Desenha a tela de vitória.

		Parâmetros
		----------
		screen : pygame.Surface
			A superfície onde a tela será desenhada.
		"""
		screen.fill((0, 0, 0))
		self.menu_button.draw(screen)
		self.exit_button.draw(screen)

		win_text = f"WIN"
		win_surface = self.font.render(win_text, True, (255, 0, 0))
		screen.blit(win_surface, (450, 200))

		pygame.display.flip()
	
	def event(self, event):
		"""
		Processa eventos da tela de vitória.

		Parâmetros
		----------
		event : pygame.event
			O evento a ser processado.
		"""
		self.menu_button.on_event(event)
		self.exit_button.on_event(event)

	def menu_callback(self):
		"""Retorna ao menu principal."""
		del self.manager.states["game_level"]
		self.manager.states["game_level"] = GameManager(self.manager, self.screen)
		self.manager.change_state("main_menu")

	def exit_callback(self):
		"""Finaliza o jogo."""
		self.manager.is_running = False