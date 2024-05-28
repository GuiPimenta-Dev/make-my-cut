grid = [[0,0,1,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,1,1,0,1,0,0,0,0,0,0,0,0],[0,1,0,0,1,1,0,0,1,0,1,0,0],[0,1,0,0,1,1,0,0,1,1,1,0,0],[0,0,0,0,0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,1,1,0,0,0,0]]


def check_neighbors(grid, i, j, total = 1):
    if grid[i][j+1] == 1:
        total += 1
    
    if grid[i][j-1] == 1:
        total += 1
    
    if grid[i+1][j] == 1:
        total += 1
    
    if grid[i-1][j] == 1:
        total += 1
        
    return total
    
        

for i in range(len(grid)):
    for j in range(len(grid[i])):
        if grid[i][j] == 1:
            neighbors = check_neighbors(grid, i , j)
            print(i,j)
            break