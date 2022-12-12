# open the file
numbers = [0]
line_counter = 0 
with open("input1.txt", 'r') as file:
    lines = file.readlines()
    for line in lines:
        line_counter += 1
        if line.strip() == "":
            # if empty line, start new entry
            numbers.append(0)
        else:
            # start adding the numbers together
            numbers[-1] += int(line)

print(f'lines_number = {line_counter}')
print(f'elf number = {len(numbers)}')
print(numbers)

# get max number + index
print(max(numbers))

numbers.sort()
top_3 = numbers[-1] + numbers[-2] + numbers[-3]

print(f"Top 3 = {top_3}")