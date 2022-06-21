import numpy as np
from defaults import * 
from random import shuffle


def select_parents(pop, winner_brains, num_parents = None):
    # Selecting the best individuals in the current generation as parents for producing the offspring of the next generation. 
    
    if not num_parents:
        num_parents = len(pop)//2
    
    parents = sorted(pop,key = lambda x: x.score,reverse=True)

    parents = winner_brains + parents
    parents = parents[:num_parents]

    
    return parents


def crossover(parents):

    offspring = []

    # for i in range(len(parents)):
    #     # Index of the first parent to mate.
    #     parent1_idx = i
    #     # Index of the second parent to mate.
    #     parent2_idx = (i+1)%len(parents)
    #     # The new offspring will have its first half of its genes taken from the first parent.
    #     offspring.append(tuple([parents[parent1_idx].gene[0],parents[parent2_idx].gene[1]]))
        
    for i in range(len(parents)):
        # Index of the first parent to mate.
        parent1_idx = i
        # Index of the second parent to mate.
        parent2_idx = (i+1)%len(parents)
        # The new offspring will have its first half of its genes taken from the first parent.
        pos_list1 = parents[parent1_idx].gene[0]
        pos_list2 = parents[parent2_idx].gene[0]
        # print(f'pos_list1: {pos_list1} \n pos_list1[0]: {pos_list1[0]} \n pos_list2: {pos_list2} \n pos_list2[0]: {pos_list2[0]} ')
        
        if len(pos_list1) > 2:
            offspring.append(tuple([((pos_list1[0], ) + (pos_list2[1], ) + (pos_list1[2], )),parents[parent1_idx].gene[1]]))
        else:
            offspring.append(tuple([((pos_list1[0], ) + (pos_list2[1], )),parents[parent1_idx].gene[1]]))
    
    parent_genes = [parent.gene for parent in parents]
    
    new_pop = parent_genes+offspring
    # print(new_pop)
    new_pop = list(set(new_pop))
    
    return tuple(new_pop)

# def mutation(new_pop,panel_pos_list):
    
#     for i in range(2):
#         random_brain = np.random.randint(len(new_pop))
#         # hit_order = [i for i in range(len(panel_pos_list))]
#         hit_order = list(new_pop[random_brain][1])
#         zero_ind = hit_order.index(0)
#         shuffle(hit_order)
#         while hit_order[zero_ind] != 0:
#             shuffle(hit_order)
#         hit_order = tuple(hit_order)
#         new_pop = list(new_pop)
#         new_pop[random_brain] = list(new_pop[random_brain])
#         new_pop[random_brain][1] = hit_order
#         new_pop[random_brain] = tuple(new_pop[random_brain])
   
#     return tuple(new_pop)
        