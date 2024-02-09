import pygame
from settings import *
from support import import_folder
from entity import Entity

class Player(Entity):
    def __init__(self,pos,groups,obstacle_sprites,create_attack,destroy_attack,create_magic):
        super().__init__(groups)
        self.image = pygame.image.load("../PythonGeme/graphics/test/player.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-6,HITBOX_OFFSET['player'])
        
        #graphics setup
        self.import_player_assets()
        self.status = "down"
        
        #movement
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.knockback = False
        self.can_dash = True
        self.dashing = False
        self.battle = False
        
        self.obstacle_sprites = obstacle_sprites
        
        #weapon
        self.create_attack = create_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.destroy_attack = destroy_attack
        self.can_switch_weapon = True
        self.weapon_switch_duration = 200
        self.switch_time = None
        
        #Magic
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None
        
        #stats
        self.is_dead = False
        self.stats = {"health": 100, "energy": 60, "attack": 10, "magic": 1,"speed": 5}
        self.max_stats = {"health": 300, "energy": 140, "attack": 20, "magic": 10,"speed": 10}
        self.upgrade_cost = {"health": 300, "energy": 500, "attack":300, "magic": 100,"speed": 700}
        self.flame_strength = 5
        self.heal_strength = 20
        self.health = self.stats["health"]
        self.energy = self.stats["energy"]
        self.exp = 5000
        self.speed = self.stats["speed"]
        self.e_recovery_speed = 0.005
        
                        #Battle Shtuff
        #Fight options
        self.attacks = {'Poop': 20,'Scratch':50,'Cover Water': 0}
        self.scratch = {'damage':100}
        self.cry = {'damage':20}
        self.cover_water = {'damage':1}
        
        #interact
        self.can_interact = True
        self.interact_time = None
        self.interact_duration = 1000
        
        #damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500
        
        #import a sound
        self.weapon_attack_sound = pygame.mixer.Sound('../PythonGeme/audio/sword.wav')
        self.weapon_attack_sound.set_volume(0.05)
    
    def import_player_assets(self):
        character_path = "../PythonGeme/graphics/player/"
        self.animations = {"up": [], "down": [], "left": [], "right": [],
            "right_idle": [], "left_idle": [], "up_idle": [], "down_idle": [],
            "right_attack": [], "left_attack": [], "up_attack": [], "down_attack": []}
        
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
             
    def overworld_input(self):
        if not self.battle:
            if not self.attacking:
                keys = pygame.key.get_pressed()
                moo = pygame.mouse.get_pressed(num_buttons=5)
                #wheel = pygame.MOUSEWHEEL
                
                #movement input
                if keys[pygame.K_w] and self.vulnerable:
                    self.direction.y = -0.5
                    self.status = "up"
                elif keys[pygame.K_s] and self.vulnerable:
                    self.direction.y = 0.5
                    self.status = "down"
                elif self.vulnerable == False:
                    self.hit_reaction()
                    if keys[pygame.K_w]:
                        self.direction.y = 0
                        self.status
                    elif keys[pygame.K_s]:
                        self.direction.y = 0
                        self.status
                else:
                    self.direction.y = 0
                if keys[pygame.K_a] and self.vulnerable:
                    self.direction.x = -0.5
                    self.status = "left"
                elif keys[pygame.K_d] and self.vulnerable:
                    self.direction.x = 0.5
                    self.status = "right"
                elif self.vulnerable == False:
                    self.hit_reaction()
                    if keys[pygame.K_a]:
                        self.direction.x = 0
                        self.status
                    elif keys[pygame.K_d]:
                        self.direction.x = 0
                        self.status
                    
                else:
                    self.direction.x = 0
                        
                #attack input
                if moo[0]:
                    self.attacking = True
                    self.attack_time = pygame.time.get_ticks()
                    self.create_attack()
                    self.weapon_attack_sound.play()
                
                #change weapon
                if moo[1] and self.can_switch_weapon == True:
                    self.can_switch_weapon = False
                    self.switch_time = pygame.time.get_ticks()
                    if self.weapon_index < len(list(weapon_data.keys())) - 1:
                        self.weapon_index += 1
                    else:
                        self.weapon_index = 0
                        
                    self.weapon = list(weapon_data.keys())[self.weapon_index]

                    
                
                #magic input
                if moo[2]:
                    self.attacking = True
                    self.attack_time = pygame.time.get_ticks()
                    style = list(magic_data.keys())[self.magic_index]
                    strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats["magic"]
                    cost = list(magic_data.values())[self.magic_index]['cost']
                    self.create_magic(style,strength,cost)
                    
                #change magic
                if moo[-1] and self.can_switch_magic == True:
                    self.can_switch_magic = False
                    self.magic_switch_time = pygame.time.get_ticks()
                    if self.magic_index < len(list(magic_data.keys())) - 1:
                        self.magic_index += 1
                    else:
                        self.magic_index = 0
                        
                    self.magic = list(magic_data.keys())[self.magic_index]
                    
                #interact
                if keys[pygame.K_SPACE] and self.can_interact:
                    self.can_interact = False
                    self.interact_time = pygame.time.get_ticks()
                    print('interact')
        
    def battle_input(self):
        self.battle = True
        self.status = "right"
        
    def get_status(self):
        
        #idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not "idle" in self.status and not "attack" in self.status:
                self.status = self.status + "_idle"
                
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not "attack" in self.status:
                if "idle" in self.status:
                    self.status = self.status.replace("_idle","_attack")
                else:
                    self.status = self.status + "_attack"
        else:
            if "attack" in self.status:
                self.status = self.status.replace("_attack","")
    
    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_attack()
                
        if not self.can_switch_weapon:
            if current_time - self.switch_time >= self.weapon_switch_duration:
                self.can_switch_weapon = True
                
        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.weapon_switch_duration:
                self.can_switch_magic = True
                
        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True
                
        if not self.can_interact:
            if current_time - self.interact_time >= self.interact_duration:
                self.can_interact = True
        
    def animate(self):
        animation = self.animations[self.status]
        
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
            
        #set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)
        
        if not self.vulnerable:
            #flicker
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
    
    def hit_reaction(self):
        
        if self.status.split('_')[0] == 'right':
            self.direction = pygame.math.Vector2(-1,0)
        elif self.status.split('_')[0] == 'left':
            self.direction = pygame.math.Vector2(1,0)
        elif self.status.split('_')[0] == 'up':
            self.direction = pygame.math.Vector2(0,1)
        else:
            self.direction = pygame.math.Vector2(0,-1)
                        
    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage
    
    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        spell_damage = magic_data[self.magic]['strength']
        return base_damage + spell_damage
    
    def get_value_by_index(self,index):
        return list(self.stats.values())[index]
    
    def get_cost_by_index(self,index):
        return list(self.upgrade_cost.values())[index]
    
    def check_death(self):
        
        if self.health <= 0:
            self.is_dead = True
            self.health = 0
    
    def energy_recovery(self):
        if self.energy < self.stats['energy']:
            self.energy += self.e_recovery_speed * self.stats['magic']
        else:
            self.energy = self.stats['energy']
    
    def update(self):
        #self.hit_reaction()
        self.check_death()
        self.overworld_input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.stats['speed'])
        self.energy_recovery()