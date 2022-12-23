#!/usr/bin/python3.11

def dist(x_a, y_a, x_b, y_b):
    return abs(x_a-x_b) + abs(y_a-y_b)

def dist_tuple(tuple_a, tuple_b):
    return dist(tuple_a[0], tuple_a[1], tuple_b[0], tuple_b[1])

def part2(max_x, max_y, sb_pair_dist):
    for x in range(max_x):
        for y in range(max_y):
            good = True
            for s in sb_pair_dist:
                dist_new = dist_tuple((x, y), s[0][0])
                d = s[1]
                if dist_new <= d:
                    good = False
                    break
            if good:
                print("answer =", x*4000000+y, 'x:', x, 'y:', y)
                return x*4000000+y

with open('input.txt', 'r') as file:
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

min_x = 0
min_y = 0
max_x = 4000000
max_y = 4000000
max_dist = 0

for i in sb_pair_dist:
    if i[1] > max_dist:
        max_dist = i[1]

print(f'max_x: {max_x}')
print(f'min_x: {min_x}')
print(f'max_y: {max_y}')
print(f'min_y: {min_y}')
print(f'max_dist: {max_dist}')

answer = part2(max_x, max_y, sb_pair_dist)
print(answer)