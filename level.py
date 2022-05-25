# -*- coding: utf-8 -*-
"""
Created on Tue May 24 23:38:09 2022

@author: user
"""
import pygame
from tile import Tile
from ninja import Ninja
from defaults import *

class Level:
    
    def __init__(self):
        
        #get the display surface
        self.display_surface = pygame.display.get_surface()
        
        #sprite group
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        
        self.create_map()
        
    
    def create_map(self):
        for r_index, row in enumerate(MAP):
            for c_index, column in enumerate(row):
                x = c_index * TILESIZE
                y = r_index * TILESIZE  
                
                if column == 'x':
                    Tile((x,y),[self.visible_sprites,self.obstacle_sprites])
                elif column == 'n':
                    self.ninja = Ninja((x,y),[self.visible_sprites],self.obstacle_sprites)
                else:
                    pass
                   
            
        
    def run(self):
        #Update and draw the game
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()