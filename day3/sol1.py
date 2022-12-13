line_value = []
team_value = []
def char_to_priority(char: str) -> int:
    if ord(char) < 92:
        return ord(char) - 38
    else:
        return ord(char) - 96

with open("input1.txt", 'r') as file:
    lines = file.readlines()
    counter = 0
    team_badge_candidate = {}

    for line in lines:
        line_length : int = len(line) -1
        comp_len : int= line_length/2
        line_dict = {}

        for i, char in enumerate(line):
            if i >= line_length:
                break
            if char not in line_dict.keys():
                if char not in team_badge_candidate.keys():
                    team_badge_candidate[char] = 1
                else:
                    team_badge_candidate[char] += 1
            line_dict[char] = 1

        line_dict = {}
        for i, char in enumerate(line):
            if i < comp_len:
                line_dict[char] = 1
            else:
                if char in line_dict:
                    line_value.append(char_to_priority(char))
                    break
        counter += 1
        if counter == 3:
            counter = 0
            for (key, value) in team_badge_candidate.items():
                if value == 3:
                    print(char)
                    team_value.append(char_to_priority(key))

            team_badge_candidate = {}

print(len(line_value))
print(f'sum of priorities: {sum(line_value)}')
print(len(team_value))
print(f'sum of team badges: {sum(team_value)}')