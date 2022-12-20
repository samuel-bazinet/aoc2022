
def print_grid(grid):
    print(len(grid[0])*'_')
    for i, line in enumerate(grid):
        if i < len(grid) -1 :
            if ('#' not in line and '#' not in grid[i+1]) and ('o' not in line and 'o' not in grid[i+1])and ('+' not in line):
                continue
        for j in line:
            print(j, end='')
        print()

with open('input.txt', 'r') as file:
    lines = [[(int(i[0]), int(i[-1])) for i in list(map(lambda x: x.split(','), i))] for i in [list(filter(lambda x: x != '->', i)) for i in list(map(lambda x: x.strip().split(' '), file.readlines()))]]

[print(line) for line in lines]
min_x = lines[0][0][0]
min_y = lines[0][0][1]
max_x = 0
max_y = 0

for line in lines:
    for t in line:
        if t[0] > max_x:
            max_x = t[0]
        if t[0] < min_x:
            min_x = t[0]
        if t[1] > max_y:
            max_y = t[1]
        if t[1] < min_y:
            min_y = t[1]

print(f'max x: {max_x}, min x: {min_x}')
print(f'max y: {max_y}, min y: {min_y}')

for i in range(min_x-1, max_x+2):
    print(i%10, end='')

print()

grid = [['.' for j in range(min_x-1, max_x+2)] for i in range(0, max_y + 1)]

def draw_line_in_grid(grid, tuple_1, tuple_2):
    if tuple_1[0] != tuple_2[0]:
        for i in range(min(tuple_1[0], tuple_2[0]) - min_x, max(tuple_1[0], tuple_2[0]) - min_x+1):
            grid[tuple_1[1]][i+1] = '#'
    else:
        for i in range(min(tuple_1[1], tuple_2[1])+1, max(tuple_1[1], tuple_2[1]) + 1):
            grid[i-1][tuple_1[0] - min_x+1] = '#'

for line in lines:
    for i in range(len(line)-1):
        draw_line_in_grid(grid, line[i], line[i+1])
#print_grid(grid)

SAND_START = 500-min_x+1

grid[0][SAND_START] = '+'

#print_grid(grid)

valid = True
counter = 0
while (valid):
    #print(counter)
    sand_x = SAND_START
    for i in range(len(grid)):
        if i+1 == len(grid) or sand_x == 0 or sand_x == len(grid[0]) - 1:
            valid = False 
            break
        if grid[i+1][sand_x] == '#' or grid[i+1][sand_x] == 'o':
            if grid[i+1][sand_x-1] != '#' and grid[i+1][sand_x-1] != 'o':
                sand_x -= 1
            elif grid[i+1][sand_x+1] != '#' and grid[i+1][sand_x+1] != 'o':
                sand_x += 1
            else:
                grid[i][sand_x] = 'o'
                counter += 1
                break
    print_grid(grid)
print(counter)