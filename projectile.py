# -*- coding: utf-8 -*-
"""
Created on Wed May 25 20:46:12 2022

@author: user
"""
# -*- coding: utf-8 -*-
"""
Created on Wed May 25 19:44:03 2022

@author: user
"""
import pygame
from defaults import * 
import numpy as np


class Projectile(pygame.sprite.Sprite):
    def __init__(self,pos, groups, obstacle_sprites):
        super().__init__(groups)
        #Take Asset from the source image
        self.image = pygame.image.load("Shuriken.png").convert_alpha() #Import image
        self.image = self.image.subsurface([0,0,16,16]) #Take the asset
        # self.image = pygame.transform.smoothscale(self.image, (TILESIZE,TILESIZE)) #Scale asset to tile size    
        
        
        # set random direction
        
        self.direction = pygame.math.Vector2()
        v = np.random.rand(2)
        v = v / np.linalg.norm(v)
        
        self.direction.x = v[0] * [1 if np.random.random() < 0.5 else -1][0]
        self.direction.y = v[1] * [1 if np.random.random() < 0.5 else -1][0]
        
        self.rect = self.image.get_rect(topleft = (int(pos[0] + (TILESIZE * self.direction.x)) ,int( pos[1] + ( TILESIZE * self.direction.y)))) #Define position of the ninja at the map
        self.speed = 5
        
        self.obstacle_sprites = obstacle_sprites
        
    
    def move(self,speed):
        if self.direction.magnitude() != 0: # Normalize the direction vector if it's not
            self.direction = self.direction.normalize()
            
        self.rect.x += self.direction.x * speed
        self.collision("horizontal")
        
        self.rect.y += self.direction.y * speed
        self.collision("vertical")
        
        
    def collision(self,direction):

        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0: # Ninja moving right 
                        self.rect.right = sprite.rect.left
                        v = np.random.rand(2)
                        v = v / np.linalg.norm(v)
                        self.direction.x *= -1

                    else: # Ninja moving left 
                        self.rect.left = sprite.rect.right
                        self.direction.x *= -1

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0: # Ninja moving right 
                        self.rect.bottom = sprite.rect.top
                        self.direction.y *= -1
                    else: # Ninja moving left 
                        self.rect.top = sprite.rect.bottom
                        self.direction.y *= -1
                        
        
    def update(self):
        self.move(self.speed)
        