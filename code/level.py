import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice, randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade
from battle_ui import BattleUI
from battle_enemy import EnemyBattle

class Level:
    def __init__(self):
        #sprite group settup
        #get display surface
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False
        
        self.counter = 0
        
        self.battle = False
        self.t = True

        #overworld
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        
        #battlesss
        self.battle_visible_sprites = LevelCameraGroup()
        self.battle_obstacle_sprites = pygame.sprite.Group()
        
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        
        
        
        self.create_map()
        
        #ui
        self.ui = UI()
        self.upgrade = Upgrade(self.player)
        
        #particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)
        
    
        
    def create_map(self):
        layouts = {
            'boundary': import_csv_layout("../PythonGeme/map/test_Boundary.csv"),
            'entities': import_csv_layout('../PythonGeme/map/test_Entities.csv'),
            'object': import_csv_layout('../PythonGeme/map/test_Objects.csv'),
            'wall': import_csv_layout('../PythonGeme/map/test_Walls.csv'),
            'battle_entities': import_csv_layout('../PythonGeme/graphics/test/battle_Entities.csv'),
        }
        graphics = {
            'objects': import_folder('../PythonGeme/graphics/objects'),
            'walls': import_folder('../PythonGeme/graphics/walls')
        }

        if not self.battle:
            for style,layout in layouts.items():
                for row_index,row in enumerate(layout):
                    for col_index,col in enumerate(row):
                        if col != "-1":
                            x = col_index * TILESIZE
                            y = row_index * TILESIZE
                            if style == 'boundary':
                                Tile((x,y),[self.obstacle_sprites],"invisible")
                            if style == 'tree':
                                #create grass tile
                                surf = graphics['trees'][int(col)]
                                Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'tree',surf)
                            if style == 'object':
                                surf = graphics['objects'][int(col)]
                                Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'object',surf)
                            if style == 'wall':
                                surf = graphics['walls'][int(col)]
                                Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'object',surf)
                            if style == 'entities':
                                try:
                                    self.player_battle.kill()
                                    self.enemy_battle.kill()
                                except:
                                    pass
                                if col == '394':                  
                                    self.player = Player(
                                    (x,y),
                                    [self.visible_sprites],
                                    self.obstacle_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic)
                                if col == '0':
                                    self.enemy = Enemy(
                                        'test',
                                        (x,y),
                                        [self.visible_sprites,self.attackable_sprites],
                                        self.obstacle_sprites,
                                        self.damage_player,
                                        self.trigger_death_particles,
                                        self.add_exp
                                    )
        else:
            for style,layout in layouts.items():
                for row_index,row in enumerate(layout):
                    for col_index,col in enumerate(row):
                        if col != "-1":
                            x = col_index * TILESIZE
                            y = row_index * TILESIZE
                            if style == 'battle_entities' and self.battle == True:
                                try:
                                    self.player.kill()
                                    self.enemy.kill()
                                except:
                                    pass
                                if col == '394':                  
                                    self.player_battle = Player(
                                    (x,y),
                                    [self.battle_visible_sprites],
                                    self.battle_obstacle_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic)
                                if col == '0':
                                    self.enemy_battle = EnemyBattle(
                                    'test',
                                    (x,y),
                                    [self.visible_sprites,self.attackable_sprites],
                                    self.obstacle_sprites,
                                    self.damage_player,
                                    self.trigger_death_particles,
                                    self.add_exp)
                                    
                                    self.battle_ui = BattleUI(self.player_battle,self.enemy_battle)
                                    
    def toggle_battle(self):
            if self.enemy.status == 'attack':
                self.battle = not self.battle
                self.create_map()
                              
    def create_attack(self):
        self.current_attack = Weapon(self.player,[self.visible_sprites,self.attack_sprites])
       
    def create_magic(self,style,strength,cost):
        if style == 'heal':
            self.magic_player.heal(self.player,strength,cost,[self.visible_sprites])
        
        if style == 'flame':
            self.magic_player.flame(self.player,strength,cost,[self.visible_sprites,self.attack_sprites])
          
    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None
    
    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0,55)
                            for leaf in range(randint(3,6)):
                                self.animation_player.create_grass_particles(pos - offset,[self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player,attack_sprite.sprite_type)
    
    def damage_player(self,amount,attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type, self.player.rect.center,[self.visible_sprites])
    
    def trigger_death_particles(self,pos,particle_type):
        self.animation_player.create_particles(particle_type,pos,self.visible_sprites)
    
    def add_exp(self,amount):
        self.player.exp += amount
    
    def toggle_menu(self):
        self.game_paused = not self.game_paused
    
    def toggle_level(self):

        
        
        self.battle = not self.battle
        self.create_map()
        
    def run(self):
        #update and draw the game 
        if self.battle == False:
            self.visible_sprites.custom_draw(self.player)
            self.ui.display(self.player)
            if self.game_paused:
                self.upgrade.display()
            else: 
                self.toggle_battle()
                
                self.visible_sprites.update()
                self.visible_sprites.enemy_update(self.player)
                self.player_attack_logic()
        else:
            
            self.battle_visible_sprites.custom_draw(self.player_battle)
            self.ui.display(self.player_battle)
            self.player_battle.battle_input()
            self.battle_ui.display()
            
            if self.game_paused:
                self.upgrade.display()
            else: 
                self.battle_visible_sprites.update()
                self.battle_visible_sprites.enemy_update(self.player_battle)  
            if self.t:
                self.t = False
                self.counter = 1

                
            if self.player_battle.health <= 0 or self.battle_ui.end:
                self.counter = -1
                self.t = True
                self.toggle_battle()
                
                
    
class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        
        #general setup
        super().__init__()
        
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
    #creating the floor
        self.floor_surf = pygame.image.load("../PythonGeme/graphics/tilemap/real.png").convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))
        
        
    def custom_draw(self,player):
        #getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        #drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf,floor_offset_pos)
        
        for sprite in sorted(self.sprites(),key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)
            
    def enemy_update(self,player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
            
class LevelCameraGroup(pygame.sprite.Group):
    def __init__(self):
        
        #general setup
        super().__init__()
        
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
    #creating the floor

        self.floor_surf = pygame.image.load("../PythonGeme/map/battle.png").convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

        
        
    def custom_draw(self,player):
        #getting the offset
        self.offset.x = player.rect.centerx - 200
        self.offset.y = player.rect.centery - 800

        #drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf,floor_offset_pos)
        
        for sprite in sorted(self.sprites(),key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)
            
    def enemy_update(self,player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)