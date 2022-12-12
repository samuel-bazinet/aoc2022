from __future__ import annotations

class Directory:
    name: str
    size: int
    parent: Directory | None
    childs: list[Directory]

    def __init__(self, name: str, size: int, parent: Directory, childs: list[Directory]):
        self.name = name
        self.size = size
        self.parent = parent
        self.childs = childs
    
    def get_total_size(self) -> int:
        size = self.size
        for child in self.childs:
            size += child.get_total_size()
        return size
    
    def get_child(self, name: str) -> None | Directory:
        for child in self.childs:
            if child.name == name:
                return child

    def get_under_100_000(self) -> int:
        ret_val = 0
        if self.get_total_size() <= 100_000:
            ret_val += self.get_total_size()
        
        for child in self.childs:
            ret_val += child.get_under_100_000()
        return ret_val

    def get_smallest_eligible(self, missing_space: int, diff: int) -> int:
        if self.get_total_size() > missing_space:
            if (self.get_total_size() - missing_space) < diff:
                diff = (self.get_total_size() - missing_space)
        for child in self.childs:
            diff = child.get_smallest_eligible(missing_space, diff) - missing_space
        return diff + missing_space

root_dir = Directory('/', 0, None, [])
current_dir: Directory = root_dir
tabbing = 0

with open('input.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip().split(' ')
        if len(line) == 2 and line[0] == '$':
            continue
        if line[1] == 'cd' and line[2] != '..':
            if line[2] == '/':
                current_dir : Directory = root_dir
            else:
                print('  '*tabbing + "Switching to", line[2])
                current_dir : Directory = current_dir.get_child(line[2])
                tabbing += 1
        elif line[1] == 'cd' and line[2] == '..':
            print('  '*tabbing + "Switching to parent", current_dir.parent.name)
            current_dir = current_dir.parent
            tabbing -= 1
        elif line[0] == 'dir':
            print('  '*tabbing + "Adding dir", line[1])
            current_dir.childs.append(Directory(line[1], 0, current_dir, []))
        else:
            #print('  '*tabbing + "Upgrading local size by", line[0])
            current_dir.size += int(line[0])

print(root_dir.get_under_100_000())

missing_space = 30_000_000 - (70_000_000-root_dir.get_total_size())

print('missing space:', missing_space)

print('smallest eligible:', root_dir.get_smallest_eligible(missing_space, 70_000_000))