#code to simulate the flow of rivers through the terrain

import numpy as np
from matplotlib import pyplot as plt
#from collections import deque

test_landscape = np.array([[-10,-10,-10,-10,-10,-10,-10,-10,-10,-10],
                           [-10,-10,-10,-10,-10,-10,-10,-10,-10,-10],
                           [-10,-10,-10,-10,15,10,5,-10,-10,-10],
                           [-10,-10,-10,-10,25,40,30,10,-10,-10],
                           [-10,-10,-10,5,50,100,80,5,-10,-10],
                           [-10,-10,5,5,55,120,20,-10,-10,-10],
                           [-10,-10,5,15,55,115,20,-10,-10,-10],
                           [-10,-10,-10,30,60,125,50,-10,-10,-10],
                           [-10,-10,-10,-10,20,50,10,-10,-10,-10],
                           [-10,-10,-10,-10,-10,10,-10,-10,-10,-10],
                           [-10,-10,-10,-10,-10,-10,-10,-10,-10,-10],
                           [-10,-10,-10,-10,-10,-10,-10,-10,-10,-10],
                           ])

water_landscape = np.array([[5,-10,-10,-10,-10,-10,10,-10,-10,-10],
                           [-10,-10,-10,-10,-10,-10,-10,-10,-10,-10],
                           [-10,-10,-10,-10,15,10,5,-10,-10,-10],
                           [-10,-10,-10,-10,25,40,30,10,-10,-10],
                           [-10,-10,-10,5,50,100,80,5,-10,-10],
                           [5,-10,5,5,55,-10,20,-10,-10,10],
                           [-10,-10,5,15,55,115,20,-10,-10,-10],
                           [-10,-10,-10,30,-10,125,50,-10,-10,-10],
                           [-10,-10,-10,-10,20,50,10,-10,-10,-10],
                           [-10,-10,-10,-10,-10,10,-10,-10,-10,-10],
                           [-10,-10,-10,-10,-10,-10,-10,-10,-10,-10],
                           [-10,-10,-10,-10,-10,-10,-10,-10,-10,-10],
                           ])

test_rainfall = np.array([[0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1],
                                    [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1],
                                    [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1],
                                    [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1],
                                    [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1],
                                    [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1],
                                    [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1],
                                    [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1],
                                    [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1],
                                    [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1],
                                    [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1],
                                    [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1],
                                    ])

test_grid_size = 20000 #side length in metres of grid square
test_rainfall_time = 2628000 #time in seconds that the precipitation period lasts for, our period is one month = 1/12 of a 365 day year

#determine which tiles in a landscape are ocean (altitude below zero and connected to the map edges), return a map of which tiles are ocean
def ocean_fill(landscape : np.ndarray[float]) -> np.ndarray[bool]:
    dimensions = landscape.shape
    height = dimensions[0]
    width = dimensions[1]
    is_ocean = np.full(dimensions,False) 
    #now set all tiles below zero on the outermost rectangle (far left,right,top and bottom) to be ocean
    #go through vertically
    for y in range(height):
        outer_rectangle_ocean(0,y,landscape,is_ocean)
        outer_rectangle_ocean(width-1,y,landscape,is_ocean)
    #and now horizontally
    for x in range(width):
        outer_rectangle_ocean(x,0,landscape,is_ocean)
        outer_rectangle_ocean(x,height-1,landscape,is_ocean)
    #extract the location of all the ocean tiles
    ocean_tiles_list = np.where(is_ocean)
    ocean_tiles_list =  convert_where_to_indice_pairs(ocean_tiles_list)
    #now fill in tiles neighbouring the initial ocean tiles and below zero in altitude
    ocean_fill_from_initial(is_ocean,landscape,ocean_tiles_list)
    return is_ocean

#fill in the ocean from the initial ocean tiles, by flooding neighbouring tiles that are below are zero
#is_ocean is 2D numpy array where true indicates an ocean tile
#ocean_tiles_list is a list of lists of form [y_index,x_index]
def ocean_fill_from_initial(is_ocean : np.ndarray[bool],landscape : np.ndarray[float],ocean_tiles_list : list[list[int]]):
    dimensions = is_ocean.shape
    height = dimensions[0]
    width = dimensions[1]
    neighbour_offsets = [[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]] #offset for each neighbour, counter-clockwise from left
    while(len(ocean_tiles_list)>0):
        indices = ocean_tiles_list[0] #extract indices of first ocean tile in list of ocean tiles
        y = indices[0]
        x = indices[1]
        for neighbour in neighbour_offsets: #go through all the neighbours around this tile
            neighbour_y = y + neighbour[0]
            neighbour_x = x + neighbour[1]
            #now we must check if the neighbour is within the bounds
            if (neighbour_x>=0 and neighbour_x<width) and (neighbour_y>=0 and neighbour_y<height):
                neighbour_height = landscape[neighbour_y,neighbour_x]
                if(neighbour_height<0):
                    if(is_ocean[neighbour_y,neighbour_x]):
                        continue #has already been marked as an ocean tile
                    else: #we have found a new ocean tile
                        is_ocean[neighbour_y,neighbour_x] = True #neighbouring tile is an ocean tile
                        ocean_tiles_list.append([neighbour_y,neighbour_x])
                else:
                    continue
            else: #not within the bounds
                continue
        del ocean_tiles_list[0] #delete the tile we just checked for neighbouring oceanality from the list of tiles to check

#convert the output of np.where too a list of indice pairs
def convert_where_to_indice_pairs(where_output : tuple) -> list:
    y_indices = list(where_output[0])
    x_indices = list(where_output[1])
    num_indices = len(y_indices)
    list_of_indice_pairs = []
    for i in range(num_indices):
        new_pair = [y_indices[i],x_indices[i]]
        list_of_indice_pairs.append(new_pair)
    
    return list_of_indice_pairs

#create the outer rectangle of ocean around the landscape            
def outer_rectangle_ocean(x : int,y : int ,landscape : np.ndarray[float],is_ocean : np.ndarray[bool]):
    height_at_square = landscape[y,x]
    if(height_at_square<0):
        is_ocean[y,x] = True

#display a landscape
def display_landscape(landscape : np.ndarray):
    plt.imshow(landscape,interpolation='nearest')
    plt.show()

