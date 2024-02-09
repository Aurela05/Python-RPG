import pygame
from settings import *
from battle_text import UI
from random import randint

class BattleUI:
    def __init__(self,player,enemy):
        
        #general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)
        self.text_boxes = UI()
        self.end = False
        self.activate_flee = False
        self.text_boxes.counter = 0
        self.can_flee = True
        
        #player setup
        self.player = player
        self.main_options = ['Fight','Flee','Items']
        self.atk_options = list(self.player.attacks.keys())
        self.atk_stats = list(self.player.attacks.values())
        self.player_turn = True
        self.player_attacked = False
        
        self.menu1 = True
        self.atk_menu = False
        
        self.can_attack = True
        self.attacked = False
        self.trig = False
        self.untrig = False
        
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True
        
        #enemy setup
        self.enemy = enemy
        self.enemy_health = self.enemy.health
        self.is_dead = False
        self.vulnerable = True
        self.enemy_turn = False
        
    def input(self):
        if self.can_move:
            keys = pygame.key.get_pressed()
            moo = pygame.mouse.get_pressed()
            
            if keys[pygame.K_w]:
                self.selection_index = 0
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_s]:
                self.selection_index = 2
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()    
                
            if keys[pygame.K_a]:
                self.selection_index = 0
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_d]:
                self.selection_index = 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                
            if moo[0]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.trig = True
                self.trigger()
                
            if moo[2]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.untrig = True
                self.untrigger()
            
    def cooldowns(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 200:
                self.can_move = True
        if not self.can_flee:
            current_time = pygame.time.get_ticks()
            if current_time - self.flee_cooldown >= 500:
                self.can_flee = True
                
    def trigger(self):
        if self.trig:
            self.trig = False
            
            #first menu
            if self.menu1:
                
                
                if self.selection_index == 0:
                    self.atk_menu = True
                    self.menu1 = False
                    pygame.time.wait(1000)
                    
                elif self.selection_index == 1:
                    pass
                
                elif self.selection_index == 2 and self.can_flee:
                    self.can_flee = False
                    self.flee_cooldown = pygame.time.get_ticks()
                    self.activate_flee = True
                    if self.text_boxes.done:
                        pass
                    
            
            #attack menu
            if self.atk_menu and self.player_turn:
                pygame.time.wait(1000)
                if self.selection_index == 0:
                    
                    self.player_attacked = True
                    self.player_atk()
                    self.atk_menu = False
                    self.menu1 = True
                    
                elif self.selection_index == 1:
                    self.enemy_health -= self.atk_stats[0]

                elif self.selection_index == 2:
                    self.enemy_health -= self.atk_stats[0]

                
    def untrigger(self):
        if self.untrig:
            self.untrig = False
            #first menu
            if self.atk_menu:
                self.selection_index = 0
                self.menu1 = True
                self.atk_menu = False
 
    def check_enemy_death(self,player):
        if self.enemy_health <= 0:
            self.enemy_health = 0
            self.enemy.kill()
            #self.trigger_death_particles(self.rect.center,self.monster_name)
            #self.add_exp(self.exp)
            #player.energy += 1
            #self.death_sound.play()
                           
    def show_box(self,opt,pos):
        text_surf = self.font.render((opt),False,TEXT_COLOR)
        text_rect = text_surf.get_rect(bottomleft = (pos))
        
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,text_rect.inflate(15,15))
        self.display_surface.blit(text_surf,text_rect)
        pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,text_rect.inflate(15,15),3)
        
    def selected(self,opt,pos):
        text_surf = self.font.render((opt),False,'black')
        text_rect = text_surf.get_rect(bottomleft = (pos))
        
        pygame.draw.rect(self.display_surface,'white',text_rect.inflate(15,15))
        self.display_surface.blit(text_surf,text_rect)
        pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,text_rect.inflate(15,15),3)
        
    def player_atk(self):
        self.text_boxes.counter = 0
        if self.text_boxes.done:
            self.enemy_health -= self.atk_stats[0]
            print(self.enemy_health)
            pygame.time.wait(500)
            self.player_turn = False
            self.enemy_turn = True
            self.text_boxes.done = False
            self.attacked = True
            self.enemy_atk()
            
        
    def enemy_atk(self):
        self.text_boxes.counter = 0
        if self.text_boxes.done:
            self.player.health -= 20
            self.enemy_turn = False
            self.player_turn = True
            
    def tb(self):
        if self.player_attacked:
            wt = pygame.time.get_ticks()
            self.text_boxes.player_display()
            if wt >= 80000:
                self.player_attacked = False
                
        if self.attacked:
            wt = pygame.time.get_ticks()
            self.text_boxes.enemy_display()
            if wt >= 10000:
                self.attacked = False
                
        if self.activate_flee and self.can_flee:
            self.activate_flee = False
            self.flee_rng = randint(0,9)        
            if self.flee_rng >= 8:
                self.end = True
            elif self.flee_rng <= 7:
                wt = pygame.time.get_ticks()
                self.text_boxes.flee_failed()
            
    def boxes(self):
        #default menu
        if self.selection_index == 0 and self.menu1:
            self.selected(self.main_options[0],(300,1000))
            self.show_box(self.main_options[1],(300,1050))
            self.show_box(self.main_options[2],(400,1000))
            
        elif self.selection_index == 2 and self.menu1:
            self.show_box(self.main_options[0],(300,1000))
            self.selected(self.main_options[1],(300,1050))
            self.show_box(self.main_options[2],(400,1000))
            self.tb()
        elif self.selection_index == 1 and self.menu1:
            self.show_box(self.main_options[0],(300,1000))
            self.show_box(self.main_options[1],(300,1050))
            self.selected(self.main_options[2],(400,1000))
        #attacks
        if self.selection_index == 0 and self.atk_menu:
            print(self.atk_menu, self.menu1, self.player_turn,self.selection_index)
            self.selected(self.atk_options[0],(300,1000))
            self.show_box(self.atk_options[2],(300,1050))
            self.show_box(self.atk_options[1],(400,1000))
            self.tb()
            
        elif self.selection_index == 2 and self.atk_menu:
            self.show_box(self.atk_options[0],(300,1000))
            self.selected(self.atk_options[2],(300,1050))
            self.show_box(self.atk_options[1],(400,1000))
            
        elif self.selection_index == 1 and self.atk_menu:
            self.show_box(self.atk_options[0],(300,1000))
            self.show_box(self.atk_options[2],(300,1050))
            self.selected(self.atk_options[1],(400,1000))
            
    def display(self):
        self.check_enemy_death(self.player)
        self.input()
        self.cooldowns()
        self.boxes()