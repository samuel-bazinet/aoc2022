from __future__ import annotations
from typing import List, Set
grid = []
start = (0,0)
end = (0,0)

def can_move_to(start: int, end: int) -> bool:
    print(end-start <= 1)
    return end-start <= 1

class Node:    
    def __init__(self, path: List[tuple[int, int]], childs: List[Node], value: int):
        self.path = path
        self.childs = childs
        self.value = value

    def new_child(self, new_node: tuple[int, int]):
        if new_node not in self.path:
            new_path = self.path
            new_path.append(new_node)
            self.childs.append(Node(new_path, [], self.value+1))
        else:
            print(new_node, 'taken')

    def traverse_grid(self, grid: List[List[int]]) -> bool:
        current = self.path[-1]
        print(current, grid[current[0]][current[1]])
        if current[0] != 0:
            new_node = (current[0]-1, current[1])
            print('1', new_node, grid[new_node[0]][new_node[1]])
            if can_move_to(grid[current[0]][current[1]], grid[new_node[0]][new_node[1]]):
                self.new_child(new_node)
                if new_node == end:
                    print('Found end')
                    return True
        if current[0] < len(grid)-1:
            new_node = (current[0]+1, current[1])
            print('2', new_node, grid[new_node[0]][new_node[1]])
            if can_move_to(grid[current[0]][current[1]], grid[new_node[0]][new_node[1]]):
                self.new_child(new_node)
                if new_node == end:
                    print('Found end')
                    return True
        if current[1] != 0:
            new_node = (current[0], current[1]-1)
            print('3', new_node, grid[new_node[0]][new_node[1]])
            if can_move_to(grid[current[0]][current[1]], grid[new_node[0]][new_node[1]]):
                self.new_child(new_node)
                if new_node == end:
                    print('Found end')
                    return True
        if current[1] < len(grid[0])-1:
            new_node = (current[0], current[1]+1)
            print('4', new_node, grid[new_node[0]][new_node[1]])
            if can_move_to(grid[current[0]][current[1]], grid[new_node[0]][new_node[1]]):
                self.new_child(new_node)
                if new_node == end:
                    print('Found end')
                    return True
        for child in self.childs:
            if child.traverse_grid(grid):
                return True
        print('did not find end', current)
        return False
    
    def get_shortest_path(self, lenght: int = 0):
        shortest = -1
        for child in self.childs:
            child_len = child.get_shortest_path(lenght)
            if shortest == -1:
                shortest = child_len
            elif child_len < shortest:
                shortest = child_len
        
        return self.value

with open('input2.txt', 'r') as file:
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
                
parent_node = Node([start], [], 0)
parent_node.traverse_grid(grid)
print(parent_node.get_shortest_path())