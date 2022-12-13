overlap = 0
overlap_2 = 0
with open("input1.txt", 'r') as file:
    lines = file.readlines()
    for pairs in lines:
        ranges = pairs.split(',')
        f = ranges[0].split('-')
        s = ranges[1].split('-')
        low_f = int(f[0])
        high_f = int(f[1])
        low_s = int(s[0])
        high_s = int(s[1])
        if (low_f >= low_s and high_f <=high_s) or (low_s >= low_f and high_s <=high_f):
            overlap += 1

        range_f = [i for i in range(low_f, high_f+1)]
        range_s = [i for i in range(low_s, high_s+1)]

        for i in range_f:
            if i in range_s:
                overlap_2 += 1
                break

print('overlap =', overlap)
print(f'overlap 2 = {overlap_2}')