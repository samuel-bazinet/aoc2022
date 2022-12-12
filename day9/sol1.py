
def tail_near_head(tail_pos: tuple[int, int], head_pos: tuple[int, int]) -> bool:
    return (abs(tail_pos[0] - head_pos[0]) <= 1 and abs(tail_pos[1] - head_pos[1]) <= 1)

pos_tail = (0, 0)
pos_head = (0, 0)
tail_positions : set = {(0,0)}
with open('input.txt', 'r') as file:
    lines = file.readlines()
    ops = list(map(lambda x: x.strip().split(' '), lines))
    for op in ops:
        for _ in range(int(op[1])):
            old_head = pos_head
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
            if not tail_near_head(pos_tail, pos_head):
                pos_tail = old_head
                tail_positions.add(pos_tail)

print(f'There are {len(tail_positions)} tail positions')