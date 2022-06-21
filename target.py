# -*- coding: utf-8 -*-
import pygame
import random
from defaults import * 
from projectile import Projectile

class Target(pygame.sprite.Sprite):
    """
    Class of killable sprites.
    """
    def __init__(self,pos, groups):
        super().__init__(groups)
        self.groups = groups
        
        #Take Asset from the source image
        self.image = pygame.image.load("TilesetLogic.png").convert_alpha() #Import image
        self.image = self.image.subsurface([0,80,16,16]) #Take the asset
        self.image = pygame.transform.smoothscale(self.image, (TILESIZE,TILESIZE)) #Scale asset to tile size    
        self.rect = self.image.get_rect(topleft = pos) #Define position of the ninja at the map
        self.hitbox = self.rect.inflate(-5,-5) #Define hitbox of the target
        