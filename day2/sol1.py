options_dict = {
    "Rock" : 1,
    "Paper" : 2,
    "Scissor": 3
}

lose_pts = 0
draw_pts = 3
win_pts = 6

opp_dict = {
    "A" : "Rock",
    "B" : "Paper",
    "C" : "Scissor"
}

play_dict = {
    "X" : "Rock",
    "Y" : "Paper",
    "Z" : "Scissor"
}

def game_points(opp: str, play: str) -> int:
    result = options_dict[play] - options_dict[opp]
    if result == 1 or result == -2:
        return win_pts + options_dict[play]
    elif result == 0:
        return draw_pts + options_dict[play]
    else:
        return lose_pts + options_dict[play]

points = 0

with open("input1.txt", 'r') as file:
    lines = file.readlines()
    for line in lines:
        game = line.split()
        points += game_points(opp_dict[game[0]], play_dict[game[1]])

print(f"Player received {points} points")