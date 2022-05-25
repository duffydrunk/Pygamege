# -*- coding: utf-8 -*-
"""
Created on Wed May 25 19:44:03 2022

@author: user
"""
import pygame
from defaults import * 
from projectile import Projectile


class Ninja(pygame.sprite.Sprite):
    def __init__(self,pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.groups = groups
        
        #Take Asset from the source image
        self.image = pygame.image.load("SpriteSheet.png").convert_alpha() #Import image
        self.image = self.image.subsurface([0,0,16,16]) #Take the asset
        self.image = pygame.transform.smoothscale(self.image, (TILESIZE,TILESIZE)) #Scale asset to tile size    
        self.rect = self.image.get_rect(topleft = pos) #Define position of the ninja at the map
        
        # movement defaults 
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.shiruken_throwed = False
        self.shiruken_cd = 400
        self.shiruken_time = 0
        
        self.obstacle_sprites = obstacle_sprites
        
        
    def keyboard_input(self):
        keys = pygame.key.get_pressed()
        
        # Movement inputs
        if keys[pygame.K_UP]:
            self.direction.y = -1
 
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1     
            
        else:
            self.direction.y = 0
 
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1

        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        
        else:
            self.direction.x = 0


        # Shriruken
        
        if keys[pygame.K_SPACE] and not self.shiruken_throwed:
            print("yes")
            Projectile((self.rect.x,self.rect.y),[self.groups],self.obstacle_sprites)
            self.shiruken_throwed = True
            self.shiruken_time = pygame.time.get_ticks() # Save the shiruken time
            
    
    def cooldown(self):
        current_time = pygame.time.get_ticks() # Save the current time
        if self.shiruken_throwed == True:
            if current_time - self.shiruken_time >= self.shiruken_cd:
                self.shiruken_throwed = False
    
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
                    else: # Ninja moving left 
                        self.rect.left = sprite.rect.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0: # Ninja moving right 
                        self.rect.bottom = sprite.rect.top
                    else: # Ninja moving left 
                        self.rect.top = sprite.rect.bottom
                        
        
    def update(self):
        self.keyboard_input()
        self.cooldown()
        self.move(self.speed)
        