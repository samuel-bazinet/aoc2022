#!/usr/bin/python3.11

def dist(x_a, y_a, x_b, y_b):
    return abs(x_a-x_b) + abs(y_a-y_b)

def dist_tuple(tuple_a, tuple_b):
    return dist(tuple_a[0], tuple_a[1], tuple_b[0], tuple_b[1])

def draw_x(grid, x, y, width):
    for i in range(width//2 + 1):
        if grid[y - i][x] != 'S' and grid[y - i][x] != 'B':
            grid[y - i][x] = '#'
        if grid[y + i][x] != 'S' and grid[y + i][x] != 'B':
            grid[y + i][x] = '#'

def draw_diamond(grid, center_x, center_y, rad):
    for i in range(rad+2):
        width = i * 2 - 1
        draw_x(grid, center_x-rad+i-1, center_y, width)
        draw_x(grid, center_x+rad-i+1, center_y, width)

def draw_grid(grid):
    print(len(grid[0])*'_')
    for i in grid:
        for j in i:
            print(j, end='')
        print()

def get_no_in_y(grid, y):
    no = 0
    for i in grid[y]:
        if i == '#':
            no += 1
    return no

with open('input2.txt', 'r') as file:
    lines = list(map(lambda x: x.strip().split(' '), file.readlines()))

sensors = []
beacons = []

for line in lines:
    sensors.append((int(line[2][2:-1]), int(line[3][2:-1])))
    beacons.append((int(line[8][2:-1]), int(line[9][2:])))

sb_pair = [(sensor, beacons[i]) for i, sensor in enumerate(sensors)]

sb_pair_dist = [(i, dist_tuple(i[0], i[1])) for i in sb_pair]

print("Sensor-beacon pairs + dist:")
[print(f'Sensor: {i[0][0]}, Beacon: {i[0][1]}, distance: {i[1]}') for i in sb_pair_dist]

min_x = sensors[0][0]
min_y = sensors[0][1]
max_x = sensors[0][0]
max_y = sensors[0][1]
max_dist = 0

for i in sb_pair_dist:
    if i[0][0][0] < min_x:
        min_x = i[0][0][0]
    if i[0][1][0] < min_x:
        min_x = i[0][1][0]
    if i[0][0][0] > max_x:
        max_x = i[0][0][0]
    if i[0][1][0] > max_x:
        max_x = i[0][1][0]
    if i[0][0][1] < min_y:
        min_y = i[0][0][1]
    if i[0][1][1] < min_y:
        min_y = i[0][1][1]
    if i[0][0][1] > max_y:
        max_y = i[0][0][1]
    if i[0][1][1] > max_y:
        max_y = i[0][1][1]
    if i[1] > max_dist:
        max_dist = i[1]

print(f'max_x: {max_x}')
print(f'min_x: {min_x}')
print(f'max_y: {max_y}')
print(f'min_y: {min_y}')
print(f'max_dist: {max_dist}')

coord = [['.' for _ in range(min_x - max_dist, max_x + max_dist + 1)] for _ in range(min_y - max_dist, max_y + max_dist + 1)]

for i in sb_pair_dist:
    print(i)
    draw_diamond(coord, i[0][0][0]-min_x + max_dist, i[0][0][1]-min_y + max_dist, i[1])
    coord[i[0][0][1]-min_y + max_dist][i[0][0][0]-min_x + max_dist] = 'S'
    coord[i[0][1][1]-min_y + max_dist][i[0][1][0]-min_x + max_dist] = 'B'

    #draw_grid(coord)

target_y = 10
print(get_no_in_y(coord, target_y-min_y+max_dist))