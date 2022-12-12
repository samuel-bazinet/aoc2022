
def tail_near_head(tail_pos: tuple[int, int], head_pos: tuple[int, int]) -> bool:
    print(tail_pos, head_pos)
    return (abs(tail_pos[0] - head_pos[0]) <= 1) and (abs(tail_pos[1] - head_pos[1]) <= 1)

def next_move(tail_pos: tuple[int, int], head_pos: tuple[int, int]) -> tuple[int, int]:
    x = 0
    y = 0
    if tail_pos[0] - head_pos[0] == 2:
        x = tail_pos[0]-1
        if tail_pos[1] - head_pos[1] >= 1:
            y = tail_pos[1]-1
        elif tail_pos[1] - head_pos[1] <= -1:
            y = tail_pos[1]+1
        else:
            y = tail_pos[1]
    elif tail_pos[0] - head_pos[0] == -2:
        x = tail_pos[0]+1
        if tail_pos[1] - head_pos[1] >= 1:
            y = tail_pos[1]-1
        elif tail_pos[1] - head_pos[1] <= -1:
            y = tail_pos[1]+1
        else:
            y = tail_pos[1]
    elif tail_pos[0] - head_pos[0] == 1:
        if tail_pos[1] - head_pos[1] == 2:
            x = tail_pos[0]-1
            y = tail_pos[1]-1
        elif tail_pos[1] - head_pos[1] == -2:
            x = tail_pos[0]-1
            y = tail_pos[1]+1
        else:
            x = tail_pos[0]
            y = tail_pos[1]
    elif tail_pos[0] - head_pos[0] == -1:
        if tail_pos[1] - head_pos[1] == 2:
            x = tail_pos[0]+1
            y = tail_pos[1]-1
        elif tail_pos[1] - head_pos[1] == -2:
            x = tail_pos[0]+1
            y = tail_pos[1]+1
        else:
            x = tail_pos[0]
            y = tail_pos[1]
    else:
        x = tail_pos[0]
        if tail_pos[1] - head_pos[1] == 2:
            y = tail_pos[1]-1
        elif tail_pos[1] - head_pos[1] == -2:
            y = tail_pos[1]+1
        else:
            y = tail_pos[1]
    print( (x, y))
    return (x, y)

pos_tails = [(0, 0) for _ in range(9)]
pos_head = (0, 0)
tail_positions : set = {(0,0)}
with open('input.txt', 'r') as file:
    lines = file.readlines()
    ops = list(map(lambda x: x.strip().split(' '), lines))
    for j, op in enumerate(ops):
        for _ in range(int(op[1])):
            match op[0]:
                case 'D':
                    pos_head = (pos_head[0], pos_head[1]-1)
                case 'U':
                    pos_head = (pos_head[0], pos_head[1]+1)
                case 'L':
                    pos_head = (pos_head[0]-1, pos_head[1])
                case 'R':
                    pos_head = (pos_head[0]+1, pos_head[1])
                case other:
                    print("Could not parse command")
            for i in range(len(pos_tails)):
                if i == 0:
                    print('head')
                    print(pos_tails[i], pos_head)
                    pos_tails[i] = next_move(pos_tails[i], pos_head)
                else:
                    print(pos_tails[i-1], pos_tails[i])
                    pos_tails[i] = next_move(pos_tails[i], pos_tails[i-1])
                    if i == len(pos_tails)-1:
                        tail_positions.add(pos_tails[-1])
                old_head = pos_tails[i]

print(f'There are {len(tail_positions)} tail positions')