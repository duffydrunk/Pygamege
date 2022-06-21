# -*- coding: utf-8 -*-
import pygame
from defaults import * 

class Tile(pygame.sprite.Sprite):
    """
    Class of non-reflective obstacles
    """
    def __init__(self,pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load("TilesetNature.png").convert_alpha() #Import tileset
        self.image = self.image.subsurface([0,0,32,32]) #Take tree tile from tileset
        self.image = pygame.transform.smoothscale(self.image, (TILESIZE,TILESIZE)) #Scale tile to tile size    
        self.rect = self.image.get_rect(topleft = pos) #Define containing rectangle of the tile and its position
        self.hitbox = self.rect.inflate(-4,-4) #Define hitbox of the tile
