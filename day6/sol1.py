with open('input.txt', 'r') as file:
    line = file.readline()
    chars : dict[str, int] = {}
    for i, char in enumerate(line):
        print(char)
        if char in chars.keys():
            chars[char] += 1
        else:
            chars[char] = 1
        
        print(chars)
        if i > 3:
            if chars[line[i-4]] > 1:
                chars[line[i-4]] -= 1
            else:
                chars.pop(line[i-4])
        
        if len(chars) == 4:
            print(i+1)
            break