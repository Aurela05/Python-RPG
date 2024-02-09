import pygame
from settings import *

import pygame
from settings import *
from entity import Entity
from support import *

class EnemyBattle(Entity):
    def __init__(self,monster_name,pos,groups,obstacle_sprites,damage_player,trigger_death_particles,add_exp):
        
        #general_setup
        super().__init__(groups)
        self.sprite_type = 'enemy'
        
        #graphics_setup
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.image = pygame.image.load('../PythonGeme/graphics/monsters/test/enemy_test.png')
        
        #movement
        #self.rect = self.image.get_rect(topleft = pos)
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)
        self.obstacle_sprites = obstacle_sprites
        
        #stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']
        
        #player interaction
        self.can_attack = True
        self.attack_cooldown = 400
        self.attack_time = None
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles
        self.add_exp = add_exp
        
        #invincibility
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 400
        
        #sounds
        self.attack_sound = pygame.mixer.Sound(monster_info['attack_sound'])
        self.death_sound = pygame.mixer.Sound('../PythonGeme/audio/creepy.wav')
        self.hit_sound = pygame.mixer.Sound('../PythonGeme/audio/hit.wav')
        self.death_sound.set_volume(0.9)
        self.hit_sound.set_volume(0.05)
        self.attack_sound.set_volume(0.05)
        
    def import_graphics(self,name):
        self.animations = {'idle':[],'move':[],'attack':[]}
        main_path = f'../PythonGeme/graphics/monsters/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)
            
            
    def get_status(self,player):
        pass
    
    def actions(self,player):
        
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage,self.attack_type)
            self.attack_sound.play()
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()
            
    def animate(self):
        animation = self.animations[self.status]
        
        self.frame_index += self.animation_speed
        if self.frame_index > len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0 
    
        #self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)
        
        if not self.vulnerable:
            #flicker
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
        
    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
    
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True
                
    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        #self.animate()
        
    def get_damage(self,player,attack_type):
        if self.vulnerable:
            self.hit_sound.play()
            self.direction = self.get_player_distance_direction(player)[1]
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage()
            else:
                self.health -= player.get_full_magic_damage()
            #magic damage
            self.vulnerable = False
            self.hit_time = pygame.time.get_ticks()
        
        
    def check_death(self,player):
        if self.health <= 0:
            self.kill()
            self.trigger_death_particles(self.rect.center,self.monster_name)
            self.add_exp(self.exp)
            player.energy += 1
            self.death_sound.play()
            
    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance
        

    def enemy_update(self,player):
        self.get_status(player)
        self.actions(player)
        self.cooldowns()
        self.check_death(player)
        #print(self.direction)