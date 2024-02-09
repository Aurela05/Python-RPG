import pygame
from settings import *
from particles import AnimationPlayer
from random import randint

class MagicPlayer:
    def __init__(self,animation_player):
        self.animtion_player = animation_player
        self.sounds = {
            'heal': pygame.mixer.Sound('../PythonGeme/audio/heal.wav'),
            'flame': pygame.mixer.Sound('../PythonGeme/audio/Fire.wav')
        }
        self.sounds['heal'].set_volume(0.3)
        self.sounds['flame'].set_volume(0.1)
        
    def heal(self,player,strength,cost,groups):
        self.sounds['heal'].play()
        strength = player.heal_strength
        if player.energy >= cost:
            player.health += strength
            player.energy -= cost
            
            if player.health >= player.stats['health']:
                player.health = player.stats['health']
            self.animtion_player.create_particles('aura',player.rect.center,groups)
            self.animtion_player.create_particles('heal',player.rect.center + pygame.math.Vector2(0,-50),groups)
    
    def flame(self,player,strength,cost,groups):
        self.sounds['flame'].play()
        strength = player.flame_strength
        if player.energy >= cost:
            player.energy -= cost
            
            if player.status.split('_')[0] == 'right':
                direction = pygame.math.Vector2(1,0)
            elif player.status.split('_')[0] == 'left':
                direction = pygame.math.Vector2(-1,0)
            elif player.status.split('_')[0] == 'up':
                direction = pygame.math.Vector2(0,-1)
            else:
                direction = pygame.math.Vector2(0,1)
                
            for i in range(1,6):
                if direction.x: #horizontal
                    offset_x = (direction.x * i) * TILESIZE
                    x = player.rect.centerx + offset_x + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animtion_player.create_particles('flame',(x,y),groups)
                else:
                    offset_y = (direction.y * i) * TILESIZE
                    x = player.rect.centerx + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + offset_y + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animtion_player.create_particles('flame',(x,y),groups)