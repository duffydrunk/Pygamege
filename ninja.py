# -*- coding: utf-8 -*-
import pygame
from defaults import * 
from projectile import Projectile
import itertools


class Ninja(pygame.sprite.Sprite):
    """
    Class that creates a ninja chracter that can throw projectiles that can reflect from reflective obstacles
    """
    def __init__(self,pos, groups, obstacle_sprites, game_speed):
        super().__init__(groups)
        
        #Take Asset from the source image
        self.image = pygame.image.load("SpriteSheet.png").convert_alpha() #Import image
        self.image = self.image.subsurface([0,0,16,16]) #Take the asset
        self.image = pygame.transform.smoothscale(self.image, (TILESIZE,TILESIZE)) #Scale asset to tile size    
        self.rect = self.image.get_rect(topleft = pos) #Define position of the ninja at the map
        self.hitbox = self.rect.inflate(-4,-4) #Define hitbox of the ninja
        
        # movement defaults 
        self.direction = pygame.math.Vector2() #Define a vector
        self.speed = game_speed #Define speed
         
        self.obstacle_sprites = obstacle_sprites #Define obstacle sprites
        
        self.new_pos = self.hitbox.center
        self.new_destination = False
        # self.path = None
        self.final = True
        
    
    def move(self,speed):
        """
        Function that moves the ninja.
        """
        self.hitbox.x += self.direction.x * speed
        self.collision("horizontal")
        
        self.hitbox.y += self.direction.y * speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center
        
        if self.new_destination:            
            self.path.pop(0)
            if self.path:
                self.new_pos = (self.path[0][1]*TILESIZE+TILESIZE/2,self.path[0][0]*TILESIZE+TILESIZE/2)
            
            self.new_destination = False

    
    def collision(self,direction):
                
        """
        Function that checks collision on the x or y axis. If a collision occurs with an obstacle sprite, ninja cannot move towards the collieded obstacle.
        """
        
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: # Ninja moving right 
                        self.hitbox.right = sprite.hitbox.left
                    else: # Ninja moving left 
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: # Ninja moving right 
                        self.hitbox.bottom = sprite.hitbox.top
                    else: # Ninja moving left 
                        self.hitbox.top = sprite.hitbox.bottom
                        
    def brain_moves(self):
        if self.path:
            self.new_pos = (self.path[0][1]*TILESIZE+TILESIZE/2,self.path[0][0]*TILESIZE+TILESIZE/2)
            ninja_pos = pygame.math.Vector2(self.hitbox.center) #Form ninja position as a vector
            new_pos = pygame.math.Vector2(self.new_pos) #Form final ninja position as a vector
            self.direction = (new_pos-ninja_pos) #Find the direction vector between ninja and mouse cursor, and normalize it
            if self.direction.magnitude() < 3:
                self.new_destination = True
            if self.direction.magnitude() > 0: #If there is a vector normalize it
                self.direction = self.direction.normalize()
        else:
            self.direction.x = 0
            self.direction.y = 0
            self.final = True
        
    def update(self):
        """
        Update method for the ninja class. 
        """
        if not self.final:
            self.brain_moves()
            self.move(self.speed)
        
        