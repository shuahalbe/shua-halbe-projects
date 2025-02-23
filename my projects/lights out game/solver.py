from collections import deque

def solver(grid, size):
    initial_state = grid_to_int(grid, size)
    queue = deque([(initial_state, [])])
    visited = {initial_state}

    while queue:
        state, path = queue.popleft()

        if state == 0:
            return path  

        for row in range(size):
            for col in range(size):
                if (row,col) not in path:
                    new_state = move(state, row, col, size)
                    if new_state not in visited:
                        visited.add(new_state)
                        queue.append((new_state, path + [(row, col)]))
    return None 

def move(state, row, col, size):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)] 
    for dr, dc in directions:
        nr, nc = row + dr, col + dc
        if 0 <= nr < size and 0 <= nc < size:
            state ^= (1 << (nr * size + nc))
    return state

def grid_to_int(grid, size):
    state = 0
    for i in range(size):
        for j in range(size):
            if grid[i][j]: 
                state |= (1 << (i * size + j)) 
    return state




                