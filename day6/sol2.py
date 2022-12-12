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
        if i > 13:
            if chars[line[i-14]] > 1:
                chars[line[i-14]] -= 1
            else:
                chars.pop(line[i-14])
        
        if len(chars) == 14:
            print(i+1)
            break