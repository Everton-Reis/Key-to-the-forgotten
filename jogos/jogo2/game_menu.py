import pygame
from game import GameManager as GM

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1000

class Button:

	def __init__(self, x, y, width, height, text, callback, fontsize=36):
		self.rect = pygame.Rect(x, y, width, height)
		self.text = text
		self.font = pygame.font.Font(None, fontsize)
		self.callback = callback

		self.color_default = "white"
		self.color_hover = "red"
		self.color_current = self.color_default

	def draw(self, screen):
		pygame.draw.rect(screen, self.color_current, self.rect)
		text_box = self.font.render(self.text, True, "black")
		text_box_rect = text_box.get_rect(center=self.rect.center)
		screen.blit(text_box, text_box_rect)

	def on_event(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			has_collided = self.rect.collidepoint(event.pos)
			if has_collided and event.button == 1:
				self.callback()
			
		if event.type == pygame.MOUSEMOTION:
			has_collided = self.rect.collidepoint(event.pos)
			if has_collided:
				self.color_current = self.color_hover
			else:
				self.color_current = self.color_default
			
class MainMenu:

	def __init__(self, manager):
		self.manager = manager
		self.start_button = Button(SCREEN_WIDTH //2 - 100, SCREEN_HEIGHT //2 - 25, 200, 50, "Start", self.start_callback)
		self.exit_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT //2 + 100, 200, 50, "exit", self.exit_callback)
		
	def draw(self, screen):
		screen.fill((0, 0, 0))
		self.start_button.draw(screen)
		self.exit_button.draw(screen)
		pygame.display.flip()
	
	def on_event(self, event):
		self.start_button.on_event(event)
		self.exit_button.on_event(event)

	def start_callback(self):
		print("start button clicked")
		self.manager.change_state("game_level")
		# self.manager.is_running = False
		# game_instance = GM()
		# game_instance.run()
		# #self.manager.change_state("game_level")

	def exit_callback(self):
		self.manager.is_running = False
	
class GameLevel:

	def __init__(self, manager):
		self.manager = manager
		self.game_instance = GM(manager.screen)

	def draw(self, screen):
		self.game_instance.run()

	def on_event(self, event):

		if self.game_instance.player.alive:
			print("Esta vivo")
			
		if not self.game_instance.player.alive:
			self.manager.change_state("game_over")

class GameOver:

	def __init__(self, manager):
		self.manager = manager
		self.reset_button = Button(SCREEN_WIDTH //2 - 100, SCREEN_HEIGHT //2 - 25, 200, 50, "Reset", self.reset_callback)
		self.exit_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT //2 + 100, 200, 50, "exit", self.exit_callback)

	def draw(self, screen):
		screen.fill((0, 0, 0))
		self.reset_button.draw(screen)
		self.exit_button.draw(screen)
		pygame.display.flip()
	
	def on_event(self, event):
		self.reset_button.on_event(event)
		self.exit_button.on_event(event)

	def reset_callback(self):
		print("botão de reset foi clicado")
		self.manager.states["game_level"] = GameLevel(self.manager)
		self.manager.change_state("game_level")
	
	def exit_callback(self):
		print("botão de saída foi clicado")
		self.manager.is_running = False

class GameManager:

	def __init__(self):
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		self.states = {
			"main_menu": MainMenu(self),
			"game_level": GameLevel(self),
			"game_over": GameOver(self)
		}
		self.current_state = self.states["main_menu"]
		self.is_running = False

	def change_state(self, state_name):
		self.current_state = self.states[state_name]

	def run(self):
		self.is_running = True
		while self.is_running:
			events = pygame.event.get()
			for event in events:
				if event.type == pygame.QUIT:
					self.is_running = False
					
				self.current_state.on_event(event)
				print(self.current_state)
			
			self.current_state.draw(self.screen)
			pygame.display.flip()
		
		pygame.quit()

if __name__ == "__main__":
	game = GameManager()
	game.run()
			
