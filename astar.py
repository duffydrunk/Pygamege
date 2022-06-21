import numpy as np
from enum import Enum
from matplotlib import pyplot as plt
from defaults import *

# define our constants here
obstacle = -50
goal = -100
solution = -200
start = -300

def MazeShow(M, title = 'da maze'):
    '''
    Function that visualizes the solution for debugging purposses.
    takes the maze / grid matrix
    plots the target as green
    obstacles as red
    shades of gray for all other cells
    black is the largest hence most difficult to pass
    lighter the gray easier the path
    '''
    # this function could be significantly shorter!!!
    # it works but you can play with if if you have time :)
    MM = M.copy()
    R = np.ones_like(MM)
    G = np.ones_like(MM)
    B = np.ones_like(MM)
    # mark obstacles as red
    R[np.where(MM == obstacle)] = 1
    G[np.where(MM == obstacle)] = 0
    B[np.where(MM == obstacle)] = 0
    # mark target as green
    R[np.where(MM == goal)] = 0
    G[np.where(MM == goal)] = 1
    B[np.where(MM == goal)] = 0
    # mark solution in blue 
    R[np.where(MM == solution)] = 0
    G[np.where(MM == solution)] = 0
    B[np.where(MM == solution)] = 1
    # mark start in magenta
    R[np.where(MM == start)] = 1
    G[np.where(MM == start)] = 0
    B[np.where(MM == start)] = 1
    # invert the color for the rest so that low values are whiter
    # normalize and invert positive values of M
    MM = np.where(MM>0, (1 - (MM/MM.max())), MM)
    # now display this
    res = np.zeros((*MM.shape,3))
    res[:,:,0] = np.where(MM>=0, MM, R)
    res[:,:,1] = np.where(MM>=0, MM, G)
    res[:,:,2] = np.where(MM>=0, MM, B)
    plt.imshow(res)
    plt.title(title)
    plt.show()


class Node:
    # you can add more functions to this class if needed
    def __init__(self, index, cost , parent=None):
        '''
        This is a class for keeping track of nodes in our search tree
        index is a tuple (i,j) that indexes the location of this node in the matrix
        if no parent is given this is the root node is assumed
        '''
        self.parent = parent 
        self.index = index
        self.cost = cost
        # you might add more properties if needed

    def __str__(self):
        # this part is worth to pay attention
        # print any node object and relate the printed value to the code here
        return f'Root node @ {self.index}' if self.parent == None else f'Node @ {self.index}, --> {self.parent.__str__()}'
    
def HeuristicF(M, node_index):
    '''
    Returns the Frobenius norm of the current node and the goal, where node_index is a tuple
    that contains row and column numbers of child node.
    '''
    return np.linalg.norm(np.array((node_index[0]-np.where(M==goal)[0][0],node_index[1]-np.where(M==goal)[1][0])))

def IsNotGoal(final, someNode):
    '''
    returns False if someNode is not the final node
    '''
    return False if someNode.index == final else True


def Spawn(M, current_node, visited_indices):
    '''
    4-neighbors is assumed. List of nodes that are reachable from the current node will be returned
    '''
    res = []
    h,w = M.shape # get the limits of the maze
    i,j = current_node.index
    # pay attention to the order of neighbors are generated, this determines the algorithms choice of direction in depth first!
    # try alternatives and observe the results
    neighbors = [(i+1, j), (i-1, j), (i, j+1), (i, j-1)] # down, up, right, left
    #neighbors = [(i, j+1), (i+1, j), (i, j-1), (i-1, j)] # right, down, left, up
    for n in neighbors:
        if (n not in visited_indices) and (n[0] >= 0) and (n[1] >=0) and (n[0] < h) and (n[1] < w) and M[n]!=obstacle:
            # this is a good index
            res.append(Node(n,cost = M[n[0]][n[1]] ,parent=current_node))
    return res

def Astar(M,initial,final,debug = False):
    # start the search from node @ (i,j)
    rootNode = Node(initial, 0, parent=None)
    # keep track of visited node indices
    visitedNodes = [] # list of indices as tupples (i,j)
    # nodes to visit
    nodes2visit = [] # list of Nodes objects
    nodes2visit_costs = [] # list of Nodes objects with their costs
    
    current_node = rootNode # start from the root
    
    while IsNotGoal(final, current_node):
        visitedNodes.append(current_node.index)
        # now that current node is not goal, get its children
        children = Spawn(M, current_node, [*visitedNodes, *[x.index for x in nodes2visit]])
        # then the first element in the list nodes2visit is used as the current_node
        current_node.cost = 0 if current_node.parent is None else current_node.cost + current_node.parent.cost                                                                     # Define Cummulative real cost of nodes. However, avoid that first node does not have any parent, so prevent crush.
        nodes2visit_costs = sorted(list(zip(children,[child.cost + current_node.cost + HeuristicF(M,child.index) for child in children])) + nodes2visit_costs, key=lambda x:x[-1]) # Sort nodes according to real and heuristic cost values
        nodes2visit = list(list(zip(*nodes2visit_costs))[0]) if len(nodes2visit_costs) > 0 else []                                                                                 # Make nodes2visit a list again, but trying indexing an empty list causes an error, avoid that
        nodes2visit_costs.pop(0) if len(nodes2visit_costs)>0 else nodes2visit_costs                                                                                                # Trying to pop an element from an empty list will cause an error. 
     
        # check for no solution
        if nodes2visit == []: # there is no solution, get out
            current_node = None
            break
        # and the search continues by updating the current_node
        current_node = nodes2visit.pop(0) 
    
    if current_node is not None: # we have a solution
        NodeOnSolution = current_node
        Msolved = M.copy() # get a copy of M on which we will place the solution
        path = [current_node.index]
        while NodeOnSolution.parent is not None:
            NodeOnSolution = NodeOnSolution.parent
            Msolved[NodeOnSolution.index] = solution
            path.append(NodeOnSolution.index)
        # mark start point as well
        Msolved[NodeOnSolution.index] = start
        if debug:
            MazeShow(M, 'maze')
            MazeShow(Msolved)
        return path
    else: # while loop returns None for no solution
        print('There is not solution for this problem')
