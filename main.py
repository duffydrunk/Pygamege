# -*- coding: utf-8 -*-
import pygame, sys
from defaults import *
from level import Level
from brain import Brain
from brain2 import Brain2
import math 
import threading
import genetic_functions as ga
import time
from debug import debug

class Main:
    
    # def __init__(self,playerNumber = 1,game_map = MAP,game_mapx = MAP_x):
    def __init__(self,playerNumber = 1,game_map = MAP_easy2,game_mapx = MAP_xeasy2):
        
        playerNo = int(math.sqrt(playerNumber))*2
        self.playerNumber = playerNumber
        pygame.init() #Initialize the pygame
        pygame.event.set_allowed(pygame.QUIT) #Only allowed event is the Quit event
        self.screen = pygame.display.set_mode((WIDTH*(playerNo//2),HEIGHT*(playerNo//2))) #Create screen
        # self.screen = pygame.display.set_mode((WIDTH,HEIGHT)) #Create screen
        pygame.display.set_caption("Beamer") #Set screen caption
        self.clock = pygame.time.Clock() #Create an object to help track time
        
        camList = []
        self.map = game_map
        self.mapx = game_mapx
        
        for i in range(playerNo//2):
            for j in range(playerNo//2):
                camList.append(pygame.Rect(j*WIDTH,i*HEIGHT,WIDTH,HEIGHT))
                
        self.hitList = [ None for i in range(len(camList)) ]
        self.levelList =[]

        self.empty_slots = []
        self.panel_pos_list = []
        
        self.define_positions(self.map)
        # print(f"EMPTY SLOTS: {len(self.empty_slots)}")
        # print(self.empty_slots)

        self.brain_list = []
        self.winner_brains = []
        self.forbid_poses_first = set([])
        self.forbid_poses_last = set([])
        
        self.genes = None
        self.generation_counter = 0
        self.max_generation = 25
        self.playerPlayTimes = 2 
        self.generation_pop = playerNumber * self.playerPlayTimes
        self.inputBrains = [[Brain(self.panel_pos_list, self.mapx,first_panel_slots = self.empty_slots) for _ in range(self.playerPlayTimes)] for level in range(playerNumber)]
        self.final = False
        
        for counter, cam in enumerate(camList):
            level = Level(cam,self.hitList,self.inputBrains[counter], game_map = self.map , game_speed = 8, game_mapx = self.mapx)
            self.levelList.append(level) 
        
    def define_positions(self,M):
        """
        Function that creates initial map according to values from defaults.py
        """
        #Check the map matrix from defaults.py
        for r_index, row in enumerate(M):
            for c_index, column in enumerate(row):

                #Create sprites according to map's index
                if column == 'n':
                    self.ninja_pos = (r_index,c_index)

                elif column == 'p':
                    self.panel_pos_list.append((r_index,c_index))
                    self.empty_slots.append((r_index,c_index))
                elif column == ' ':
                    self.empty_slots.append((r_index,c_index))
                else:
                    pass
        

    def brain(self):
        if all( hit is True for hit in self.hitList):
            for i in range(len(self.hitList)):
                self.hitList[i] = None
                
            
            for level in self.levelList:
                self.brain_list.append(level.brain)
                #Check if there are any forbidden posses
                if level.forbid_poses:
                    if level.forbid_poses[0]:
                        self.forbid_poses_first.add(level.forbid_poses[0])
                        if level.forbid_poses[0] in self.empty_slots:
                            self.empty_slots.remove(level.forbid_poses[0])
                    else:
                        self.forbid_poses_last.add(level.forbid_poses[1])
                if level.winner_brain: #Check if the brain is a winner
                    self.winner_brains.append(level.brain)
                    self.winner_brains = list(set(self.winner_brains))
            
            # print(f'Gen No: {self.generation_counter}, Times: {0 if len(self.brain_list) == 0 else len(self.brain_list)}')
            # print(f"Forbid 1st: {self.forbid_poses_first} & {len(self.forbid_poses_first)} Forbid 2nd: {self.forbid_poses_last}")
            # print(f"EMPTY SLOTS: {len(self.empty_slots)}")
            # time.sleep(600)
            if len(self.brain_list) == self.generation_pop: #Max iteration number is reached
                if self.generation_counter == self.max_generation: #Best Solutions
                    print("Best Solutions Best SolutionsBest SolutionsBest SolutionsBest SolutionsBest SolutionsBest Solutions")
                    self.brain_list = self.brain_list+ self.winner_brains
                    self.brain_list = sorted(self.brain_list,key = lambda x: x.score,reverse=True)
                    for c, level in enumerate(self.levelList):
                        self.brain_list[c].fire = True
                        level.brain_list = [self.brain_list[c]]
                        
                    self.final = True
                else:
                
                    self.brain_evolves()
            
    def brain_evolves(self):

        self.inputBrains = []
        parents = ga.select_parents(self.brain_list,self.winner_brains)
        new_pop = ga.crossover(parents)
        # self.genes = ga.mutation(new_pop,self.panel_pos_list)
        self.genes = new_pop
        
        if len(self.genes) < self.generation_pop:
            new_random_Brains = [Brain(self.panel_pos_list, self.mapx,first_panel_forbid = self.forbid_poses_first, last_panel_forbid = self.forbid_poses_last,first_panel_slots = self.empty_slots) for _ in range(self.generation_pop-len(self.genes))]
            new_random_genes = tuple([brain.gene for brain in new_random_Brains])
            self.genes += new_random_genes
        
        for i in range(self.playerNumber):
            newGenes = self.genes[i*self.playerPlayTimes : i*self.playerPlayTimes+self.playerPlayTimes]
            newBrains = []
            for gene in newGenes:
                newBrains.append(Brain(self.panel_pos_list, self.mapx,gene,first_panel_forbid = self.forbid_poses_first, last_panel_forbid = self.forbid_poses_last,first_panel_slots = self.empty_slots))

            self.inputBrains.append(newBrains)

        for c, level in enumerate(self.levelList):
            level.brain_list = self.inputBrains[c]
        
        self.generation_counter += 1
        self.brain_list = []
                
    def run(self):
        """
        This is the loop function that updates the screen, according to the events happened during
        the cycle.
        """

        while(1): 
            threadList = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() #If game is stopped quit pypame
                    sys.exit()
                
                
            self.screen.fill("black") #Main background

            for level in self.levelList: #Start threads for every level
                if not self.hitList[level.id]: #Check if specific level is done for this iteration
                    thread = threading.Thread(target = level.run())
                    threadList.append(thread)
                    thread.start()
            
            for thread in threadList: #Join threads so do not blit until every level is done
                thread.join()
            
            for level in self.levelList: #Place every display surface of the levels to the desired parts of the screens
                self.screen.blit(level.display_surface, (level.cam[0],level.cam[1]))

            debug(f'Generation: {self.generation_counter}, Generation Pop: {len(self.brain_list)}')
            pygame.display.update() #Display new events on the screen
            self.clock.tick(FPS) #Limit the run time speed of the game to FPS value
            if not self.final:
                self.brain() #Check if all the levels are hit        

if __name__ == "__main__":
    game = Main()
    game.run()