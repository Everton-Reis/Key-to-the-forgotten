import pygame
from menu import MainMenu, GameOver, GameWin
from game import GameManager
from gamesettings import *

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1000

pygame.init()

class Main:
	"""
	Classe principal que gerencia os estados do jogo e o loop principal.

	Atributos
	---------
	screen : pygame.Surface
		A superfície principal onde o jogo será renderizado.
	states : dict
		Um dicionário que contém os diferentes estados do jogo (menu, jogo, game over, vitória).
	current_state : objeto do estado atual
		O estado que está ativo no momento.
	is_running : bool
		Variável que controla o loop principal do jogo.
	delta : int
		Delta para o tempo de execução (pode ser usado para ajustes relacionados ao jogo).
	"""
	def __init__(self):
		"""
		Inicializa a classe principal, definindo os estados e iniciando a música de fundo.
		"""
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		
		self.states = {
			"main_menu": MainMenu(self),
			"game_level": GameManager(self, self.screen),
			"game_over": GameOver(self, self.screen),
			"game_win": GameWin(self, self.screen)
		}

		# O estado inicial é o menu
		self.current_state = self.states["main_menu"]
		self.is_running = True

		# Carrega e inicia a música de fundo
		pygame.mixer.music.load(BACKGROUND_MUSIC)	
		pygame.mixer.music.play(loops=-1)

		# Define o delta para o tempo, necessario para spawns de montros e outras funções
		self.delta = DELTA_GAME

	def change_state(self, state_name):
		"""
		Muda o estado atual do jogo para o estado especificado.

		Parâmetros
		----------
		state_name : str
			O nome do estado para o qual o jogo deve ser alterado.
		"""
		self.current_state = self.states[state_name]

		# Reinicia a música se o estado for for o menu ou a lógica principal do jogo
		if state_name in ["main_menu", "game_level"] and not pygame.mixer.music.get_busy():
			pygame.mixer.music.stop()
			pygame.mixer.music.play(loops=-1)

	def run(self):
		"""
		Inicia o loop principal do jogo, processando eventos, lógica e renderização.
		"""
		clock = pygame.time.Clock()
		
		# Loop principal do jogo
		while self.is_running:
			
			clock.tick(60)
			events = pygame.event.get()
			for event in events:
				if event.type == pygame.QUIT:
					self.is_running = False
				
				# Passa o evento para o estado atual
				self.current_state.event(event)

			# Lógica específica para o estado do jogo game_level
			if self.current_state == self.states["game_level"]:
				self.current_state.on_key_pressed() 
				self.current_state.update_timers() 
				self.current_state.handle_events()  # Gerencia eventos específico do jogo
				self.current_state.update_logic()  
				self.current_state.draw()          
				self.current_state.update()       
				self.current_state.verify_death(self.change_state)  
				self.current_state.verify_win(self.change_state)    
			else:
				# é chamado no else para evitar problemas, pois o self.current_state.draw() deve vir antes do self.current_state.update()
				self.current_state.draw(self.screen)
			
			pygame.display.flip()
			
if __name__ == "__main__":
	game = Main()
	game.run()
	pygame.quit()