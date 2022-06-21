# -*- coding: utf-8 -*-
"""
Created on Sun May 22 19:26:13 2022

@author: user
"""
import pygame

pygame.init()
font = pygame.font.Font(None, 20)

def debug(info,y = 0, x = 0):
    display_surface = pygame.display.get_surface()
    debug_surf = font.render(info, True, "White")
    debug_rect = debug_surf.get_rect(topleft = (x,y))
    pygame.draw.rect(display_surface, "Black", debug_rect)
    display_surface.blit(debug_surf, debug_rect)