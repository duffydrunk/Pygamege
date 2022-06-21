# -*- coding: utf-8 -*-
import pygame
import random
import genetic_functions as ga
from tile import Tile
from ninja import Ninja
from projectile import Projectile
from target import Target
from panel import Panel
from defaults import *
from debug import debug
import time

class Level:
    """
    Class of current game level.
    """
    levelCounter = 0
    
    def __init__(self,cam, hitList, brains ,game_map = MAP_easy, game_speed = 10,game_mapx = MAP_xeasy):
        
        #Get the display surface
        self.screen = pygame.display.get_surface()
        self.cam = cam
        self.hitList = hitList
        self.restart = False
        self.map = game_map
        self.mapx = game_mapx
        self.game_speed  = game_speed
        self.id = Level.levelCounter
        Level.levelCounter += 1
        self.recordNumber = 0
        self.record = True
        #Define sprite groups
        self.visible_sprites = pygame.sprite.Group() #Sprites which are always drawn on the screen
        self.obstacle_sprites = pygame.sprite.Group() #Sprites which cause specific actions if collision occours
        self.player_sprites = pygame.sprite.Group() #Sprites which can spawn attack sprites
        self.target_sprites = pygame.sprite.Group() #Sprites which can be killed
        self.attack_sprites = pygame.sprite.Group() #Sprites which can kill killable sprites
        self.mirror_sprites = pygame.sprite.Group() #Sprites that can reflect the projectile
        
        self.create_map(self.map) #Create Map
        
        self.brain_list = brains
        self.brain = self.brain_list.pop(0)
        self.brain_decides()
        self.winner_brains = []
        self.winner_brain = None
        
        self.generation_counter = 0
    
    def create_map(self,M):
        """
        Function that creates initial map according to values from defaults.py
        """
        self.panels = []
        #Check the map matrix from defaults.py
        for r_index, row in enumerate(M):
            for c_index, column in enumerate(row):
                x = c_index * TILESIZE
                y = r_index * TILESIZE  
                
                #Create sprites according to map's index
                if column == 'x': 
                    Tile((x,y),[self.visible_sprites,self.obstacle_sprites])
                elif column == 'n':
                    self.ninja = Ninja((x,y),[self.visible_sprites,self.player_sprites],self.obstacle_sprites,self.game_speed)
                elif column == 't':
                    self.target = Target((x,y),[self.visible_sprites,self.target_sprites])
                elif column == 'p':

                    panel = Panel((x,y),[self.visible_sprites,self.mirror_sprites],self.obstacle_sprites,self.game_speed)
                    self.panels.append(panel)
                else:
                    pass
    
    def draw_line(self):
        """
        Function that draws the trajactory of the projectiles
        """
        if self.attack_sprites: #If any projectile is currently in the game
            for sprite in self.attack_sprites: #For every projectile
                lines = sprite.track.copy() #Copy the track list of the projectile 
                lines[-1].append(sprite.rect.center) #Add current position of the projectile to the copy of the track list
                for line in lines:
                    pygame.draw.lines(self.display_surface,(255,0,255), False, line, width= 2) #Draw the tracjactory of the projectile
    
    def hitting_condition(self):
        """
        Function that checks if a projectile collides with a target. If so, both of the target and projectile are killed.
        """
        if self.attack_sprites: #If there are any projectiles on the game
            for attack_sprite in self.attack_sprites: #For every projectile 
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.target_sprites, False) #Check if projectile collides with a target
                if collision_sprites: #If collision occurred
                    for sprite in collision_sprites: #Kill both projectile and target
                        sprite.kill()
                    
                    self.calc_score(1000,attack_sprite.bounce_number,attack_sprite.bounce_threshold)
                    attack_sprite.kill()
                    self.winner_brains.append(self.brain)
                    self.winner_brain = self.brain
     
                    self.restart = True  
                    self.hitList[self.id] = True
                    return
                    
            for attack_sprite in self.attack_sprites: #For every projectile 
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.obstacle_sprites, False) #Check if projectile collides with a obstacle
                if collision_sprites: #If collision occurred
                    
                    atack_center = pygame.math.Vector2(attack_sprite.hitbox.center)
                    target = min([t for t in self.target_sprites], key=lambda t: atack_center.distance_to(pygame.math.Vector2(t.hitbox.x, t.hitbox.y)))
                    target_center = pygame.math.Vector2(target.hitbox.center)
                    is_close = (atack_center-target_center).magnitude()
                    print(-1*is_close//TILESIZE)
                    
                    self.calc_score(-1*is_close//TILESIZE,attack_sprite.bounce_number,attack_sprite.bounce_threshold)
                    attack_sprite.kill()
                    self.restart = True         
                    self.hitList[self.id] = True
                    self.winner_brain = None
                    return
                                             
    def create_targets(self,max_iteration = 1000):
        """
        Function that creates new targets when the total nubmer of targets are lower than min target number.
        """
        iter_number = 0 #Current iteration number
        possible_positions = [(i, j) for i in range(ROW_NUMBER) for j in range(COLUMN_NUMBER)] #Possible positions of the new target
        proper = True #Flag for proper place of the new target
        while len(self.target_sprites) < MIN_TARGET_NUM: #While a new target is needed
            new_target_pos = random.choice(possible_positions) #Select a random possible position for the new target
            new_target = pygame.Rect((new_target_pos[1] * TILESIZE,new_target_pos[0] * TILESIZE),(TILESIZE,TILESIZE)) #Create a rect object at the selected position

            for sprite in self.visible_sprites: #For every target (Since we don't want targets to overlap)
                if sprite.rect.colliderect(new_target): #Check if there is collision 
                    possible_positions.remove(new_target_pos) #If so, selected position is not proper remove from the list
                    proper = False #Reverse the flag
                    break #No more iteration is needed
                        
            if proper: #If current selected position still proper create new target
                Target((new_target_pos[1] * TILESIZE,new_target_pos[0] * TILESIZE),[self.visible_sprites,self.target_sprites]) #Create new target
                
            if iter_number < max_iteration: #Check iteration number to prevent stucking in a infinite loop
                iter_number += 1
                proper = True #Reverse the flag to select a new possible position if needed

            else: #There is no possible place to place a new target
                return  

    def calc_score(self,points,bounce_time,bounce_th):
        """
        Function that calculates score of the ninja
        """
        # score = -10*len(self.brain.ninja_path) - len(self.brain.panel_path) + points
        
        score = -2* sum([len(x) for x in self.brain.gene[0]]) + points*3 
        
        self.brain.score = score
        
        
        if bounce_time == 0:
            self.forbid_poses = [(self.panels[0].hitbox.y//TILESIZE,self.panels[0].hitbox.x//TILESIZE),None]
        elif bounce_time == bounce_th:
            self.forbid_poses = [None,(self.panels[-1].hitbox.y//TILESIZE,self.panels[-1].hitbox.x//TILESIZE)]
        else:
            self.forbid_poses = []
            
    def brain_decides(self):
        """
        Function that passes the final destination of the agents from the brain
        """
        
        
        for c, panel_path in enumerate(self.brain.gene[0]):
            self.panels[c].path = list(panel_path)
        
        for m, hit in enumerate(self.brain.gene[1]): #Implement hit orders
            self.panels[m].hit_order = hit
        
        self.panels = sorted(self.panels,key = lambda x: x.hit_order) #Sort panels
        
        for k, panel in enumerate(self.panels):
            if k != len(self.panels) - 1:
                # panel.aim = pygame.math.Vector2(self.panels[k+1].hitbox.center)
                self.final_rotation_panel(self.panels[k+1],panel,True)
            else:        
                # panel.aim = pygame.math.Vector2(self.target.hitbox.center)
                self.final_rotation_panel(self.target,panel)

    def final_rotation_panel(self,target,panel,moving_target = False):
        """
        
        """
        if panel.path:
            destination = (panel.path[-1][0]*TILESIZE+TILESIZE/2,panel.path[-1][1]*TILESIZE+TILESIZE/2) #Find final point of the panel position
        else:
            destination = panel.hitbox.center
            
        if moving_target:
            if target.path:
                target_destination = (target.path[-1][0]*TILESIZE+TILESIZE/2,target.path[-1][1]*TILESIZE+TILESIZE/2) #Find final point of the target panel position
            else:
                target_destination = target.hitbox.center
            target_pos = pygame.math.Vector2(target_destination[0],target_destination[1]) #Form target position as a vector
            
        else:        
            target_pos = pygame.math.Vector2(target.hitbox.center) #Form target position as a vector
            
        dest_pos = pygame.math.Vector2(destination[0],destination[1]) #Form destination position as a vector
        direction = (target_pos-dest_pos) #Find the direction vector of panel
        if direction.magnitude():
            direction = (target_pos-dest_pos).normalize() #Find the direction vector of panel
            
        panel_pos_vector = pygame.math.Vector2(0,1) #Form panel position as a vector
        angle = panel_pos_vector.angle_to(direction) #Find the angle between
        panel.new_rot = (angle+90)%360 #New rotation angle for the panel 
    
    def brain_throws(self):
        """
        Function that creates a projectile if agents are in their final position

        """
        if self.ninja.final and all(panel.final is True for panel in self.panels) and self.brain.fire:
            for k, panel in enumerate(self.panels):
                if k != len(self.panels) - 1:
                    panel.aim = pygame.math.Vector2(self.panels[k+1].hitbox.center)
                    # self.final_rotation_panel(self.panels[k+1],panel)
                else:        
                    panel.aim = pygame.math.Vector2(self.target.hitbox.center)
                    # self.final_rotation_panel(self.target,panel)            
            
            
            ninja_pos = pygame.math.Vector2(self.ninja.hitbox.center) #Form ninja position as a vector
            panel_pos = pygame.math.Vector2(self.panels[0].hitbox.center) #Form panel position as a vector
            
            Projectile(self.ninja.hitbox.center,[self.visible_sprites, self.attack_sprites],self.obstacle_sprites,panel_pos,self.mirror_sprites,self.game_speed) #Create p
            self.brain.fire = False

    def run(self):
        
        if self.recordNumber < 300:
                self.display_surface = pygame.Surface((self.cam[2],self.cam[3])) #Refresh the display surface of level
                self.visible_sprites.draw(self.display_surface)
                self.recordNumber += 1
                self.record = False
                return
        
        if self.restart == True:
            for sprite in self.visible_sprites:
                sprite.kill()
            
            self.create_map(self.map)
            self.brain = self.brain_list.pop(0)

            self.brain_decides()
            self.restart = False        
        
        #Update and draw the game
        self.display_surface = pygame.Surface((self.cam[2],self.cam[3])) #Refresh the display surface of level
        self.visible_sprites.draw(self.display_surface)
        self.draw_line()

        #Create targets
        # if len(self.target_sprites) < MIN_TARGET_NUM:
        #     self.create_targets()

            
        #Update moving sprites
        self.player_sprites.update()
        self.mirror_sprites.update()
        if self.attack_sprites:
            self.attack_sprites.update()
            if not self.attack_sprites:
                self.hitList[self.id] = True
                self.calc_score(-100,2,-2)
                self.restart = True
                self.winner_brain = None
        else:
            self.brain_throws() #If there are no projectile check for fire conditions
        
        self.hitting_condition()
        
