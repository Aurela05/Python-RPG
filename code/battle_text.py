import pygame
from settings import *


class UI:
    def __init__(self):
        
        #general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)
        
        self.index = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
        self.counter = 0
        self.speed = 30
        self.done = False

        
        #bar setup
        self.health_bar_rect = pygame.Rect(10,10,HEALTH_BAR_WIDTH,BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10,38,ENERGY_BAR_WIDTH,BAR_HEIGHT)
        
    def text_box(self,text,pos,color,counter_num):
        

        self.done = False
        text_surf = self.font.render('',False,color)
        text_rect = text_surf.get_rect(bottomleft = (pos))
        
        for x in self.index:
            
            if self.counter < self.speed * len(text):
                self.counter += 1
            if self.counter >= counter_num:
                self.timer = pygame.time.get_ticks()
                
                if self.timer >= 7000:
                    
                    self.done = True
                    continue
        
            text_surf = self.font.render(text[0:self.counter//self.speed],False,color)
            text_rect = text_surf.get_rect(bottomleft = (pos))
            
            pygame.draw.rect(self.display_surface,UI_BG_COLOR,text_rect.inflate(15,15))
            self.display_surface.blit(text_surf,text_rect)
            pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,text_rect.inflate(15,15),3)
            
            #wip
        if self.done == True:
          
        
            text_surf = self.font.render(text[0:self.counter//self.speed],False,'#222222')
            text_rect = text_surf.get_rect(bottomleft = (pos))
              
            pygame.draw.rect(self.display_surface,UI_BG_COLOR,text_rect.inflate(15,15))
            self.display_surface.blit(text_surf,text_rect)
            pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,text_rect.inflate(15,15),3)    

            
    def player_display(self):
        self.text_box('The player has attacked!',(300,600),TEXT_COLOR,712)
        
        
    def enemy_display(self):
        
        self.text_box('The enemy has attacked!',(600,700),TEXT_COLOR,712)
        
    def flee_failed(self):
        self.text_box('Failed to flee the fight!',(300,600),TEXT_COLOR,400)
        
    #def stop(self):
        #self.bt = self.text_box('The player has attacked!',(300,600),UI_BG_COLOR)