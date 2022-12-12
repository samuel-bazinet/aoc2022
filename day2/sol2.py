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
    "X" : "Lose",
    "Y" : "Draw",
    "Z" : "Win"
}

win_dict = {
    "Rock" : "Paper",
    "Paper" : "Scissor",
    "Scissor" : "Rock"
}

lose_dict = {
    "Rock" : "Scissor",
    "Paper" : "Rock",
    "Scissor" : "Paper"
}

def game_points(opp: str, play: str) -> int:
    if play == "Win":
        return win_pts + options_dict[win_dict[opp]]
    if play == "Lose":
        return lose_pts + options_dict[lose_dict[opp]]
    return draw_pts + options_dict[opp]

points = 0

with open("input1.txt", 'r') as file:
    lines = file.readlines()
    for line in lines:
        game = line.split()
        points += game_points(opp_dict[game[0]], play_dict[game[1]])

print(f"Player received {points} points")