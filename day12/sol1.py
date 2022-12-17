from __future__ import annotations
from typing import List, Set
grid = []
start = (0,0)
end = (0,0)
max = 0

def can_move_to(start: int, end: int) -> bool:
    return end-start <= 1

class Node:    
    def __init__(self, path: List[tuple[int, int]], childs: List[Node], value: int):
        self.path = path
        self.childs = childs
        self.value = value

    def new_child(self, new_node: tuple[int, int]):
        if new_node not in self.path:
            new_path = self.path.copy()
            new_path.append(new_node)
            self.childs.append(Node(new_path, [], self.value+1))

    def traverse_grid(self, grid: List[List[int]]) -> int:
        current_max = max
        current = self.path[-1]
        if current[0] != 0:
            new_node = (current[0]-1, current[1])
            if can_move_to(grid[current[0]][current[1]], grid[new_node[0]][new_node[1]]):
                self.new_child(new_node)
                if new_node == end:
                    return self.value
        if current[0] < len(grid)-1:
            new_node = (current[0]+1, current[1])
            if can_move_to(grid[current[0]][current[1]], grid[new_node[0]][new_node[1]]):
                self.new_child(new_node)
                if new_node == end:
                    return self.value
        if current[1] != 0:
            new_node = (current[0], current[1]-1)
            if can_move_to(grid[current[0]][current[1]], grid[new_node[0]][new_node[1]]):
                self.new_child(new_node)
                if new_node == end:
                    return self.value
        if current[1] < len(grid[0])-1:
            new_node = (current[0], current[1]+1)
            if can_move_to(grid[current[0]][current[1]], grid[new_node[0]][new_node[1]]):
                self.new_child(new_node)
                if new_node == end:
                    return self.value
        for child in self.childs:
            val = child.traverse_grid(grid)
            if val < current_max:
                current_max = val
        return current_max

with open('input.txt', 'r') as file:
    lines = list(map(lambda x: x.strip(), file.readlines()))
    for i, line in enumerate(lines):
        current_line = []
        for j, char in enumerate(line):
            if char == 'S':
                current_line.append(ord('a'))
                start = (i, j)
            elif char == 'E':
                current_line.append(ord('z'))
                end = (i, j)
            else:
                current_line.append(ord(char))
        grid.append(current_line)

[print(line) for line in grid]
print('Start:', start)
print('End:', end)

max = len(grid) * len(grid[0])

parent_node = Node([start], [], 1)
sol = parent_node.traverse_grid(grid)
print(sol)