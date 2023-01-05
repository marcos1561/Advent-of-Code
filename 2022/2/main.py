import AdventOfCode.aoc as aoc
from typing import NamedTuple

input_path = "input.txt"
# input_path = "test.txt"
data_temp = aoc.get_input(input_path)


player_1_to_option = {"A": 0, "B": 1, "C": 2}
player_2_to_option = {"X": 0, "Y": 1, "Z": 2}

data = [("", "")]*len(data_temp)
for id, row in enumerate(data_temp):
    player1, player2 = row.strip().split(" ") 
    data[id] = (player_1_to_option[player1], player_2_to_option[player2])

option_points = {0:1, 1:2, 2:3}

class ResultPoins(NamedTuple):
    win = 6
    draw = 3
    lose = 0

### 1 ###
total_points = 0
for row in data:
    player1, player2 = row

    result_point = ResultPoins.draw 
    if player2 == (player1 + 1) % 3: 
        result_point = ResultPoins.win
    elif player2 == (player1 + 2) % 3:
        result_point = ResultPoins.lose

    round_points = result_point + option_points[player2]
    total_points += round_points

print("Total points:", total_points)
###

### 2 ###
result_to_offset = {0: 2, 1: 0, 2: 1}
result_to_point = {0: 0, 1:3, 2:6}

total_points = 0
for row in data:
    player1, result = row
    player2 = (player1 + result_to_offset[result]) % 3

    result_point = result_to_point[result]

    round_points = result_point + option_points[player2]
    total_points += round_points

print("Total points:", total_points)
###