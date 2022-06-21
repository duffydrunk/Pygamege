# -*- coding: utf-8 -*-
import pygame
from defaults import * 
import numpy as np

class Projectile(pygame.sprite.Sprite):
    """
    Projectile class.
    """
    def __init__(self,pos, groups, obstacle_sprites, aim,mirror_sprites, game_speed):
        super().__init__(groups)
        #Take Asset from the source image
        self.lenght = TILESIZE/4
        self.image = pygame.image.load("Shuriken.png").convert_alpha() #Import image
        self.image = self.image.subsurface([0,0,16,16]) #Take the asset
        self.image = pygame.transform.smoothscale(self.image, (self.lenght,self.lenght)) #Scale image to desired size

        self.aim = aim
        self.rect = self.image.get_rect(center = pos) #Define position of the projectile at the map
        self.hitbox = self.rect
        
        self.speed = game_speed
        self.obstacle_sprites = obstacle_sprites
        self.mirror_sprites = mirror_sprites
        self.bounce_number = 0 #Number of bounces that projectile made
        self.bounce_threshold = 3 #Threshold value for maximum bounce a projectile can make
        self.track = [[self.rect.center]]  #List that contains points for trajactories of the projectile
        self.track_line_no = 0 #Current trajactory number, increases if projectile hits a panel
        self.collided_mirror = None

    def move(self,speed):
        """
        Function that moves the projectile.
        """
        
        self.direction =  (self.aim-self.hitbox.center)
        
        if self.direction.magnitude() != 0: # Normalize the direction vector if it's not
            self.direction = self.direction.normalize()
            
        self.hitbox.x += self.direction.x * speed #Move the projectile to it's new x position
        self.hitbox.y += self.direction.y * speed #Move the projectile to it's new y position
        self.collision() #Check if collision occured with a panel
        self.rect.center = self.hitbox.center
        
    def collision(self):
        
        """
        Function that checks collision on the x or y axis. If a collision occurs, the speed on the particular axis is reversed.
        """

        for sprite in self.mirror_sprites: #Iterate for every mirror
            if sprite.hitbox.colliderect(self.hitbox) and self.collided_mirror != sprite : #Check if there is collision
                 self.track[self.track_line_no].append(self.hitbox.center) #Record the collision point with the mirror
                 self.aim = sprite.aim #Get the aim position from mirror
                 self.hitbox.center = sprite.hitbox.center #Record the new center  
                 self.collided_mirror = sprite #Record last reflected mirror
                 self.bounce_number += 1
                 self.track_line_no += 1
                 self.track.append([self.hitbox.center])
    
    def check_bounce_lim(self):
        """
        Function that controls the number of bounces of the projectile. When the projectile's bounce count reaches the threshold number, it is killed.
        """
        if self.bounce_number > self.bounce_threshold: #If projectile bounces more than the threshold value, kill it
            self.kill()
    
    
    def update(self):
        """
        Update method for the projectile class. 
        """

        self.move(self.speed)
        self.check_bounce_lim()
        