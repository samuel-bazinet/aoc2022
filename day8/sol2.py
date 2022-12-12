trees = []
num_lines = 0

with open('input.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        
        trees.append([])
        for char in line.strip():
            trees[num_lines].append(int(char))
        num_lines += 1

max = 0

for i in range(1, len(trees)-1):
    for j in range(1, len(trees[0])-1):
        current = trees[i][j]
        is_visible = True
        vis_xl = 0
        vis_xr = 0
        vis_yt = 0
        vis_yb = 0

        for k in range(i-1, -1, -1):
            is_visible = is_visible and (current > trees[k][j])
            vis_xl += 1
            if not is_visible:
                break
        
        is_visible = True

        for k in range(i+1, len(trees)):
            is_visible = is_visible and (current > trees[k][j])
            vis_xr += 1
            if not is_visible:
                break

        is_visible = True  

        for k in range(j-1, -1, -1):
            is_visible = is_visible and (current > trees[i][k])
            vis_yt += 1
            if not is_visible:
                break

        is_visible = True  

        for k in range(j+1, len(trees)):
            is_visible = is_visible and (current > trees[i][k])
            vis_yb += 1
            if not is_visible:
                break
        
        
        score = vis_xl * vis_xr * vis_yb * vis_yt
        if score > max:
            print(score, vis_xl, vis_xr, vis_yb, vis_yt, current, i, j)
            max = score

print(max)