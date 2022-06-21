import numpy as np
from astar import Astar
from defaults import * 
from random import shuffle

class Brain():
    
    _id = 0
    
    def __init__(self,panel_pos_list, game_mapx = MAP_xeasy, Gene = None, first_panel_forbid = None, last_panel_forbid = None, first_panel_slots = [] ):
        
        self.mapx = game_mapx
        self.id = Brain._id
        self.possible_positions = np.where(self.mapx == 1)
        panel_destinations = []
        chosen_positions = []
        panel_paths = []
        
        Brain._id += 1
        
        if not Gene:

            while len(panel_destinations) < len(panel_pos_list): #Pick a random position for every panel
                rand_indx = np.random.randint(len(self.possible_positions[0]))
                if rand_indx not in chosen_positions:
                    dest = (self.possible_positions[0][rand_indx],self.possible_positions[1][rand_indx])
                    
                    if len(panel_destinations) == 0 and first_panel_forbid: #First panel restrictions
                        while dest in first_panel_forbid:
                            rand_indx = np.random.randint(len(self.possible_positions[0]))
                            dest = (self.possible_positions[0][rand_indx],self.possible_positions[1][rand_indx])
                            
                    elif len(panel_destinations) == len(panel_pos_list) -1 and last_panel_forbid: #Last panel restrictions
                        while dest in last_panel_forbid:
                            rand_indx = np.random.randint(len(self.possible_positions[0]))
                            dest = (self.possible_positions[0][rand_indx],self.possible_positions[1][rand_indx])
                            
                    panel_destinations.append(dest)
                    chosen_positions.append(rand_indx)       
                    
            for c, panel_destination in enumerate(panel_destinations):     
                panel_path = Astar(self.mapx,panel_pos_list[c],panel_destination) #Find the path 
                if panel_path:
                    panel_path.reverse()
                    panel_path.pop(0)
                    panel_paths.append(tuple(panel_path))
            panel_paths = tuple(panel_paths)
            hit_order = [i for i in range(len(panel_pos_list))]
            shuffle(hit_order)
            hit_order = tuple(hit_order)
            
        else:
            Flag = False
            panel_paths = Gene[0]
            
            if first_panel_forbid:
                if panel_paths:
                    if panel_paths[0]:
                        if panel_paths[0][-1] in first_panel_forbid:
                            Flag = True 
                    
            if  last_panel_forbid:
                if panel_paths:
                    if panel_paths[-1]:
                        if panel_paths[-1][-1] in last_panel_forbid:
                            Flag = True 
            
            if Flag:
                panel_paths = []
                while len(panel_destinations) < len(panel_pos_list): #Pick a random position for every panel
                    rand_indx = np.random.randint(len(self.possible_positions[0]))
                    if rand_indx not in chosen_positions:
                        dest = (self.possible_positions[0][rand_indx],self.possible_positions[1][rand_indx])
                        
                        if len(panel_destinations) == 0 and first_panel_forbid: #First panel restrictions
                            while dest in first_panel_forbid:
                                rand_indx = np.random.randint(len(self.possible_positions[0]))
                                dest = (self.possible_positions[0][rand_indx],self.possible_positions[1][rand_indx])
                                
                        elif len(panel_destinations) == len(panel_pos_list) -1 and last_panel_forbid: #Last panel restrictions
                            while dest in last_panel_forbid:
                                rand_indx = np.random.randint(len(self.possible_positions[0]))
                                dest = (self.possible_positions[0][rand_indx],self.possible_positions[1][rand_indx])
                                
                        panel_destinations.append(dest)
                        chosen_positions.append(rand_indx)       
                        
                for c, panel_destination in enumerate(panel_destinations):     
                    panel_path = Astar(self.mapx,panel_pos_list[c],panel_destination) #Find the path 
                    if panel_path:
                        panel_path.reverse()
                        panel_path.pop(0)
                        panel_paths.append(tuple(panel_path))
                panel_paths = tuple(panel_paths)
                hit_order = [i for i in range(len(panel_pos_list))]
                shuffle(hit_order)
                hit_order = tuple(hit_order)
                
            else:
                hit_order = Gene[1]
        
        
        # print(f"Forbid 1st: {first_panel_forbid} Forbid 2nd: {last_panel_forbid} \n Selected: {panel_paths[0][-1] if panel_paths[0] else panel_paths[0]}")
        self.gene = (panel_paths,hit_order)
        self.fire = True
        self.score = 0

    def __repr__(self):
        return f'Brain id: {self.id}'


    def __eq__(self, other):
        return self.gene == other.gene

    def __hash__(self):
        return hash(self.gene) 


print(Brain._id)

# path = Astar(MAP_x,(2, 16),(1,1),True)
# path.reverse()
# path.pop(0)