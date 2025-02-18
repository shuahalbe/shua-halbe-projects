import os
import copy
import time
WHITE_BG = "\033[48;2;240;240;220m" 
BROWN_BG = "\033[48;2;140;100;80m"  
RED_BG = "\033[41m"
GREEN_BG = "\033[48;2;0;255;0m"  
RESET = "\033[0m" 

grid = []
def load_level(level_number,choice):
    global player_loc,end_spots,num_col,grid
    if choice ==2: file_choice = rf"C:\Users\halbj\OneDrive\Documents\python projects\sokoban\levels\original\level{level_number}"
    if choice ==1:file_choice  = rf'C:\Users\halbj\OneDrive\Documents\python projects\sokoban\levels\magic_sokoban6\level{level_number}'
    with open(file_choice, "r") as file:  
        for line in file:
            line = line.rstrip("\n")
            if line:
                grid.append(list(line))
    num_col = 0
    for i in range(len(grid)):
        cols = 0
        for j in grid[i]:
            cols +=1
        num_col = max(num_col,cols)

    end_spots = []
    for i in range(len(grid)):
        for j in range(num_col):
            try:
                if grid[i][j] == '.':
                    end_spots.append((i,j))
            except IndexError:
                pass
    grids()

def print_grid():
    global num_col,grid,end_spots
    os.system('cls' if os.name == 'nt' else 'clear')
    for i in range(len(grid)):
        for j in range(num_col):
            try:
                if grid[i][j] == '#':
                    print(f"{BROWN_BG}{'  '}{RESET}", end="")
                elif grid[i][j] == '@':
                    print(f"{WHITE_BG}{'P '}{RESET}", end="")
                elif grid[i][j] == '$':
                    if grid[i][j] in end_spots: print(f"{GREEN_BG}{'B '}{RESET}", end="")
                    else: print(f"{RED_BG}{'B '}{RESET}", end="")
                elif (i,j) in end_spots: print(f"{WHITE_BG}{'. '}{RESET}", end="")
                else:
                    print(f"{WHITE_BG}{'  '}{RESET}", end="")
            except IndexError:
                print(f"{WHITE_BG}{'  '}{RESET}", end="")
                pass
        print()


def movement(direction):
    global player_loc,grid,end_spots
    for row in range(len(grid)):
        for col in range(num_col):
            try:
                if grid[row][col] == '@':
                    player_loc = row,col
                    break
            except IndexError:
                pass
    row,col = player_loc
    if direction == 'up': player_loc = (row-1,col)
    elif direction == 'down': player_loc = (row+1,col)
    elif direction == 'right': player_loc = (row,col+1)
    elif direction == 'left': player_loc = (row,col-1)
    else:
        return
    if legal(player_loc,direction):
        new_row,new_col = player_loc
        grid[new_row][new_col] = '@'
        grid[row][col] = ' '
    else:
        print('illegal')
        player_loc = (row,col)

def legal(player_loc,direction):
    global grid
    new_row,new_col = player_loc
    if grid[new_row][new_col] == '#':
        return False
    if grid[new_row][new_col] in (' ' , '.') :
        grids()
        return True
    if grid[new_row][new_col] == '$':
        if direction == 'up': box_row,box_col = new_row-1,new_col
        elif direction == 'down': box_row,box_col = new_row+1,new_col
        elif direction == 'right': box_row,box_col = new_row,new_col+1
        elif direction == 'left': box_row,box_col = new_row,new_col-1
        if grid[box_row][box_col] in(' ','.' ):
            grids()
            grid[box_row][box_col] = '$'
            return True
        
def win():
    if all(grid[r][c]=='$' for r,c in end_spots):
        return True

past_grids = [] 
def grids():
    global past_grids,grid
    past_grids.append(copy.deepcopy(grid))


def undo():
    global past_grids,grid
    if past_grids:
        grid[:] = past_grids.pop()







