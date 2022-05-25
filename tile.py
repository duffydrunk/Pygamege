# -*- coding: utf-8 -*-
"""
Created on Tue May 24 23:43:11 2022

@author: user
"""
import pygame
from defaults import * 


class Tile(pygame.sprite.Sprite):
    def __init__(self,pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load("TilesetNature.png").convert_alpha() #Import tileset
        self.image = self.image.subsurface([0,0,32,32]) #Take tree tile from tileset
        self.image = pygame.transform.smoothscale(self.image, (TILESIZE,TILESIZE)) #Scale tile to tile size    
        self.rect = self.image.get_rect(topleft = pos)