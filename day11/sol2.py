import __future__
from typing import List

class Monkey:
    
    def __init__(self, items, op, cond, target_true, target_false):
        self.items = items
        self.op = op
        self.cond = cond
        self.target_true = target_true
        self.target_false = target_false
        self.item_count = 0

monkeys : List[Monkey] = []
tests = []
lcm = 0

def handle_monkey(monkey : Monkey):
    for old in monkey.items:
        monkey.item_count += 1
        new = eval(monkey.op)
        new %= lcm
        if new % monkey.cond == 0:
            monkeys[monkey.target_true].items.append(new)
        else:
            monkeys[monkey.target_false].items.append(new)
    monkey.items = []

with open('input.txt', 'r') as file:
    lines = list(map(lambda x: x.strip().split(' '), file.readlines()))
    current_monkey  = None
    for line in lines:
        if line[0] == 'Monkey':
            if current_monkey != None:
                monkeys.append(current_monkey)
            current_monkey = Monkey([], '', 0, 0, 0)
        elif line[0] == 'Starting':
            for i in line[2::]:
                current_monkey.items.append(int(i.strip(':,')))
        elif line[0] == 'Operation:':
            current_monkey.op = ' '.join(line[3::])
        elif line[0] == 'Test:':
            current_monkey.cond = int(line[-1])
            tests.append(int(line[-1]))
        elif line[0] == 'If':
            if line[1] == 'true:':
                current_monkey.target_true = int(line[-1])
            else:
                current_monkey.target_false = int(line[-1])
    if current_monkey != None:
        monkeys.append(current_monkey)

#print(len(monkeys))
#[print(monkey.op) for monkey in monkeys]

for i, test in enumerate(tests):
    if i == 0:
        lcm = test
    else:
        lcm *= test

for _ in range(10000):
    for monkey in monkeys:
        handle_monkey(monkey)

counts = [monkey.item_count for monkey in monkeys]
[print(i) for i in counts]
counts.sort()
print('Product of 2 highest:', counts[-1] * counts[-2])