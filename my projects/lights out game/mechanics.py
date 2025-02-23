import time
import random
import os
import copy
WHITE_BG = "\033[48;2;250;250;250m"
GREY_BG = "\033[48;2;105;105;105m"
RED_BG = "\033[41m"
RESET = "\033[0m" 

def create_puzzle(size):
    grid = [[False for row in range(size)]for col in range(size)]
    for i in range(size):
        for j in range(size):
            logic = random.randint(0,1)
            if logic == 1: grid[i][j] = True
    return grid

def win(grid,size):
    if all(grid[i][j] == False for i in range(size) for j in range(size)):
        return True
    
def move(row,col,grid,size):
    new_grid = copy.deepcopy(grid)
    directions = (-1,1)
    new_grid[row][col] = not new_grid[row][col]
    for i in directions:
        if 0<=row+i<size:
            new_grid[row+i][col] = not new_grid[row+i][col]
        if 0<=col+i<size:
            new_grid[row][col+i] = not new_grid[row][col+i]
    return new_grid






