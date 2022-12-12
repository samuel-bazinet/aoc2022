trees = []
num_lines = 0

with open('input.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        
        trees.append([])
        for char in line.strip():
            trees[num_lines].append(int(char))
        num_lines += 1

print(trees)
print(f'rows = {len(trees)}\ncols = {len(trees[0])}')

visible = len(trees) * 2 + len(trees[0]) * 2 - 4

for i in range(1, len(trees)-1):
    for j in range(1, len(trees[0])-1):
        current = trees[i][j]
        is_visible = True
        for k in range(i):
            is_visible = is_visible and (current > trees[k][j])
        
        if is_visible:
            visible += 1
            continue
        is_visible = True

        for k in range(i+1, len(trees)):
            is_visible = is_visible and (current > trees[k][j])

        if is_visible:
            visible += 1
            continue
        is_visible = True

        if is_visible:
            for k in range(j):
                is_visible = is_visible and (current > trees[i][k])

        if is_visible:
            visible += 1
            continue
        is_visible = True

        for k in range(j+1, len(trees)):
            is_visible = is_visible and (current > trees[i][k])

        if is_visible:
            visible += 1

print(f'visible = {visible}')