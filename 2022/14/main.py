import AdventOfCode.aoc as aoc
import numpy as np
from typing import NamedTuple

# Read Input ###
input_path = "input.txt"
# input_path = "test.txt"
data_temp = aoc.get_input(input_path)

class Blocks:
    air = 0
    rock = 1
    sand = 2

global_min_col = 100000
global_max_col = 0
global_max_row = 0
rock_map = np.zeros((10000, 10000), dtype=int)
for id, row in enumerate(data_temp):
    points = row.split("->")
    points = [[int(coord) for coord in reversed(p.strip().split(","))] for p in points ]
    
    p_id = 1
    num_points = len(points)
    while p_id < num_points:
        p1 = points[p_id]
        p2 = points[p_id -1]
        
        if p1[0] == p2[0]:
            if p1[1] < p2[1]:
                p1, p2 = p2, p1

            rock_map[p1[0], p2[1]:p1[1]+1] = Blocks.rock
        else:
            if p1[0] < p2[0]:
                p1, p2 = p2, p1
            
            rock_map[p2[0]:p1[0]+1, p1[1]] = Blocks.rock

        p_id += 1

    min_col = min(points, key= lambda x: x[1])[1]
    max_col = max(points, key= lambda x: x[1])[1]
    max_row = max(points, key= lambda x: x[0])[0]

    if min_col < global_min_col:
        global_min_col = min_col
    if max_col > global_max_col:
        global_max_col = max_col
    if max_row > global_max_row:
        global_max_row = max_row
    
# print(data[0:global_max_row+1, global_min_col:global_max_col+1])
# print(rock_map[0:1000, 494:504])
###

### Part 1 ###
print("="*5, "Part 1", "="*5)

class Coord(NamedTuple):
    row: int
    column: int

    def __add__(self, other):
        return Coord(self.row + other.row, self.column + other.column)

class Directions:
    down = Coord(1, 0)
    down_left = Coord(1, -1)
    down_right = Coord(1, 1)

    @staticmethod
    def all():
        return (Directions.down_left, Directions.down, Directions.down_right)

class BaseBlocks(NamedTuple):
    down_left: int
    down: int
    down_right: int

class SimulateSand:
    source_pos = Coord(0, 500)

    def __init__(self, rock_map: np.ndarray, min_col:int, max_col: int, max_row: int) -> None:
        self.rock_map = rock_map.copy()

        self.min_col = min_col
        self.max_col = max_col
        self.max_row = max_row

    def simulate(self) -> int:
        rock_map = self.rock_map
        source_pos = SimulateSand.source_pos

        num_rest_sand = 0
        current_pos = source_pos + Directions.down
        while rock_map[source_pos] != Blocks.sand and not self.is_out_of_limits(current_pos):
            base_blocks = self.get_base_blocks(current_pos)
            if Blocks.air not in base_blocks:
                rock_map[current_pos] = Blocks.sand
                
                num_rest_sand += 1
                current_pos = source_pos
            else:
                if base_blocks.down == Blocks.air:
                    current_pos += Directions.down
                elif base_blocks.down_left == Blocks.air:
                    current_pos += Directions.down_left
                else:
                    current_pos += Directions.down_right

        # self.print_rock_map(rock_map[0:15, 494-4:504+4])
        return num_rest_sand

    def get_base_blocks(self, coord: Coord):
        base_blocks = [0, 0, 0]
        for id, direction in enumerate(Directions.all()):
            base_blocks[id] = self.rock_map[coord + direction]
        
        return BaseBlocks(*base_blocks)

    def is_out_of_limits(self, coord: Coord) -> bool:
        return coord.column > self.max_col or coord.column < self.min_col or coord.row > self.max_row

    @staticmethod
    def print_rock_map(rock_map: np.ndarray, save_file=False):
        text = ""

        for row in rock_map:
            print("[", end="")
            text += "["
            for i in row:
                print(str(i).ljust(2), end="")
                text += str(i).ljust(2)
            print("]")
            text += "]\n"
        print()
        
        if save_file:
            with open("rock_map.txt", "w") as f:
                f.write(text)

num_rest_sand = SimulateSand(rock_map, max_col=global_max_col, min_col=global_min_col, max_row=global_max_row).simulate()
print("Num rest sand:", num_rest_sand)
###

print()

### Part 2 ###
print("="*5, "Part 2", "="*5)

# Add floor
rock_map[global_max_row+2, :] = Blocks.rock 
global_max_row += 2
global_max_col = rock_map.shape[1]-1
global_min_col = 0

num_rest_sand = SimulateSand(rock_map, max_col=global_max_col, min_col=global_min_col, max_row=global_max_row).simulate()
print("Num rest sand:", num_rest_sand)
###