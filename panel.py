# -*- coding: utf-8 -*-
import pygame
from defaults import * 

class Panel(pygame.sprite.Sprite):
    """
    Class of reflective obstacles
    """
    def __init__(self,pos, groups,obstacle_sprites, game_speed, aim = None):
        super().__init__(groups)
        self.image = pygame.image.load("Arrow.png").convert_alpha() #Import tileset
        self.image = self.image.subsurface([0,0,13,13]) #Take snowy tree tile from tileset
        self.image = pygame.transform.smoothscale(self.image, (TILESIZE/2,TILESIZE/2)) #Scale image to desired size   
        self.rect = self.image.get_rect(topleft = (pos[0]+TILESIZE/4,pos[1]+TILESIZE/4)) #Define position
        self.hitbox = self.rect.inflate(-4,-4) #Define hitbox of the panel
        self.original_image = self.image.copy() #Keep original image of the panel
        self.aim = aim 
        self.hit_order = None
        
        # movement defaults 
        self.direction = pygame.math.Vector2() #Define a vector
        self.reflect_direction = pygame.math.Vector2(0,1)
        self.speed = game_speed #Define speed
        self.rotation = 0 #Define current rotation
        self.rotation_speed = self.speed / 2 #Define rotation speed as degree per action
 
        self.obstacle_sprites = obstacle_sprites #Define obstacle sprites
    
        self.new_pos = self.hitbox.center
        self.new_rot = None
        self.new_destination = False
        self.path = None
        self.rot_final = False
        self.pos_final = False
        self.final = False
 
    def move(self,speed):
        """
        Function that moves the ninja.
        """
        if self.direction.magnitude() != 0: # Normalize the direction vector if it's not
            self.direction = self.direction.normalize()
            
        self.hitbox.x += self.direction.x * speed #Move hitbox at x-axis
        # self.collision("horizontal") #Check if there are any collisions
        
        self.hitbox.y += self.direction.y * speed #Move hitbox at y-axis
        # self.collision("vertical") #check if there are any collisions
        self.rect.center = self.hitbox.center #Update rectangle's center as the hitbox's cetenr
        
        if self.new_destination:            
            self.path.pop(0)
            if self.path:
                self.new_pos = (self.path[0][1]*TILESIZE+TILESIZE/2,self.path[0][0]*TILESIZE+TILESIZE/2)
 
            self.new_destination = False
            
    # def collision(self,direction):
                
    #     """
    #     Function that checks collision on the x or y axis. If a collision occurs with an obstacle sprite, ninja cannot move towards the collieded obstacle.
    #     """
        
    #     if direction == 'horizontal':
    #         for sprite in self.obstacle_sprites:
    #             if sprite.hitbox.colliderect(self.hitbox):
    #                 if self.direction.x > 0: # Panel moving right 
    #                     self.hitbox.right = sprite.hitbox.left
    #                 else: # Panel moving left 
    #                     self.hitbox.left = sprite.hitbox.right

    #     if direction == 'vertical':
    #         for sprite in self.obstacle_sprites:
    #             if sprite.hitbox.colliderect(self.hitbox):
    #                 if self.direction.y > 0: # Panel moving right 
    #                     self.hitbox.bottom = sprite.hitbox.top
    #                 else: # Panel moving left 
    #                     self.hitbox.top = sprite.hitbox.bottom     


    def brain_rotates(self):
        if self.new_rot and self.new_rot != self.rotation:
            self.image = pygame.transform.rotate(self.original_image, self.rotation) #Rotate original image as desired angle
            self.rect = self.image.get_rect(center = self.hitbox.center) #Find new containing rectangle
            new_hitbox = self.rect.inflate(-6,-6) #Define new  hitbox of the panel
            new_hitbox.center = self.hitbox.center #Prevent shift to define new hitbox's center as previous center
            
            self.hitbox = new_hitbox #Update hitbox with rotated one
            sign = -1 if self.new_rot > 180 else 1
            self.rotation += self.rotation_speed*sign #Update rotation angle
            self.rotation %= 360
            if self.rotation_speed > abs(self.rotation-self.new_rot):
                self.rotation_speed = abs(self.rotation-self.new_rot) 
            else:
                self.rotation_speed = self.speed / 2

            self.reflect_direction = pygame.math.Vector2.rotate(self.reflect_direction, -1*sign*self.rotation_speed) #Update reflection direction
            
        if self.rotation == self.new_rot:
            self.rot_final = True
        
        

    def brain_moves(self):
        if self.path:
            self.new_pos = (self.path[0][1]*TILESIZE+TILESIZE/2,self.path[0][0]*TILESIZE+TILESIZE/2)
            panel_pos = pygame.math.Vector2(self.hitbox.center) #Form ninja position as a vector
            new_pos = pygame.math.Vector2(self.new_pos) #Form final ninja position as a vector
            self.direction = (new_pos-panel_pos) #Find the direction vector between ninja and mouse cursor, and normalize it
            if self.direction.magnitude() < 10:
                self.new_destination = True
            if self.direction.magnitude() > 0: #If there is a vector normalize it
                self.direction = self.direction.normalize()

        else:
            self.direction.x = 0
            self.direction.y = 0
            self.pos_final = True

    def is_not_final(self):
        return 0 if self.pos_final and self.rot_final else 1

    def update(self):
        """
        Update method for the ninja class. 
        """

        if not self.rot_final:
            self.brain_rotates()        
        if self.is_not_final():
            self.brain_moves()
            self.move(self.speed)
            
        else:
            self.final = True
