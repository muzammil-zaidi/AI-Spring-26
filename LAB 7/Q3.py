grid = [
    [0,0,6,2,0,5],
    [0,0,0,4,6,0],
    [0,1,2,0,0,0],
    [5,6,0,0,0,4],
    [0,0,4,3,0,2],
    [3,0,0,5,0,6]
]

def is_valid(grid, r, c, num):
    if num in grid[r]:
        return False

    for i in range(6):
        if grid[i][c] == num:
            return False

    start_r = (r // 2) * 2
    start_c = (c // 3) * 3

    for i in range(2):
        for j in range(3):
            if grid[start_r+i][start_c+j] == num:
                return False

    return True

def solve(grid):
    for r in range(6):
        for c in range(6):
            if grid[r][c] == 0:
                for num in range(1,7):
                    if is_valid(grid, r, c, num):
                        grid[r][c] = num
                        if solve(grid):
                            return True
                        grid[r][c] = 0
                return False
    return True

solve(grid)

for row in grid:
    print(row)
