buffer = []
cycle_flags = [20, 60, 100, 140, 180, 220]
cycle_sum : int = 0
X : int = 1
pixels = []

with open('input.txt', 'r') as file:
    lines = list(map(lambda x: x.strip().split(' '), file.readlines()))
    for i in range(240):
        if X <= ((i%40)+1) and ((i%40)+1) <= X+2:
            pixels.append('#')
        else: 
            pixels.append('.')
        if i+1 in cycle_flags:
            print(i+1, X, (i+1) * X)
            cycle_sum += (i+1) * X
        if i < len(lines):
            line = lines[i]
            buffer.append(0)
            if len(line) == 2:
                buffer.append(int(line[1]))
        if len(buffer) > 0:
            X += buffer.pop(0)
         
print(cycle_sum)
[print(i, end='') for i in pixels[0:40]]
print()
[print(i, end='') for i in pixels[40:80]]
print()
[print(i, end='') for i in pixels[80:120]]
print()
[print(i, end='') for i in pixels[120:160]]
print()
[print(i, end='') for i in pixels[160:200]]
print()
[print(i, end='') for i in pixels[200:240]]
print()