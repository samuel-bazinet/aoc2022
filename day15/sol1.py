#!/usr/bin/python3.11

def dist(x_a, y_a, x_b, y_b):
    return abs(x_a-x_b) + abs(y_a-y_b)

def dist_tuple(tuple_a, tuple_b):
    return dist(tuple_a[0], tuple_a[1], tuple_b[0], tuple_b[1])

def draw_x(y, width, target):
    return y + width >= target and y - width <= target

def draw_diamond(x_set: set, center_x, center_y, rad, target):
    for i in range(rad):
        width = i * 2 - 1
        if draw_x(center_y, width, target):
            for j in range(center_x-rad+i, center_x+rad-i):
                x_set.add(j)
            return

with open('./day15/input.txt', 'r') as file:
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

x_set = set()
target = 2000000
#for i in sb_pair_dist:
#    print(i)
#    draw_diamond(x_set, i[0][0][0], i[0][0][1], i[1], target)
for i in range(min(x[0][0][0]-x[1] for x in sb_pair_dist), max(x[0][0][0]+x[1] for x in sb_pair_dist)):
    for j in sb_pair_dist:
        if (abs(i - j[0][0][0]) + abs(target - j[0][0][1])) <= j[1]:
            x_set.add(i)

for i in beacons:
    if i[1] == target:
        if i[0] in x_set:        
            x_set.remove(i[0])

print(len(x_set))
#print(x_set)