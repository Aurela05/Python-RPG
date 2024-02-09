import pygame, sys
from settings import *
from level import Level
from pygame.locals import *

class Game:
	def __init__(self):
		  
		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
		self.fullscreen = False
		pygame.display.set_caption('Midner')
		self.clock = pygame.time.Clock()
		self.font = pygame.font.Font(UI_FONT,60)

		self.level = Level()
		self.player = self.level.player
		self.main_sound = pygame.mixer.Sound('../PythonGeme/audio/MainTheme.ogg')
		self.main_sound.set_volume(0.5)
		self.main_sound.play(loops = -1)
		self.menu_sound = pygame.mixer.Sound('../PythonGeme/audio/menu.wav')
		self.menu_sound.set_volume(0.5)
		self.battle_music = pygame.mixer.Sound('../PythonGeme/audio/idk.ogg')
		self.battle_music.set_volume(1)
		self.click = False
  
	def draw_text(self,text):
		self.display_surface = pygame.display.get_surface()
		self.text_obj = self.font.render(text,False,(0,255,0))
		self.text_rect = self.text_obj.get_rect()
		self.text_rect.topleft = (255,335)
		self.display_surface.blit(self.text_obj,self.text_rect)
  
	def main_menu(self):
		running = True
		while running:
			self.screen.fill((0,0,0))
			

			mx,my = pygame.mouse.get_pos()

			button_1 = pygame.Rect(100,300,500,150)
			
			button_2 = pygame.Rect(250,700,500,150)
			if button_1.collidepoint((mx,my)):
				if self.click:
					self.click = not self.click
					self.run()
			if button_2.collidepoint((mx,my)):
				if self.click:
					#settings menu
					pass
   
			pygame.draw.rect(self.screen,(255,0,0),button_1)
			self.draw_text('Play')
			pygame.draw.rect(self.screen,(255,0,0),button_2)
   
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == MOUSEBUTTONDOWN:
					if event.button == 1:
						self.click = True
						pygame.time.wait(100)
			pygame.display.update()
			self.clock.tick(FPS)
	
	def run(self):
		running = True
		while running:
			if self.level.battle:
				self.main_sound.stop()
				if self.level.counter == 1:
					self.level.counter = 0
					self.battle_music.play(loops = -1)
			if not self.level.battle:
				self.battle_music.stop()
				if self.level.counter == -1:
					self.level.counter = 0
					self.main_sound.play(loops=-1)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						running = False
					if event.key == pygame.K_RETURN:
						self.menu_sound.play()
						self.level.toggle_menu()
					
					if event.key == pygame.K_F11:
						self.fullscreen = not self.fullscreen
						if self.fullscreen:
							self.screen = pygame.display.set_mode((self.screen.get_width(),self.screen.get_height()),pygame.FULLSCREEN)
						else:
							self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
       
			self.screen.fill('black')
			self.level.run()
			pygame.display.update()
			self.clock.tick(FPS)

	def settings(self):
		pass

if __name__ == '__main__':
	game = Game()
	game.main_menu()