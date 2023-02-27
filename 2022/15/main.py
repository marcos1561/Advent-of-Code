import math, time

import AdventOfCode.aoc as aoc
from closed_intervals import ClosedIntervals

# Read Input ###
input_path = "input.txt"
# input_path = "test.txt"
data_temp = aoc.get_input(input_path)

def manhattan_dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

sensor_coords = []
beacon_coords = []
max_dist = 0
for id, row in enumerate(data_temp):
    column_id = row.index(":")

    sensor_data = row[10: column_id].split(", ")
    beacon_data = row[column_id + 23:].split(", ")

    sensor_coord = [int(str_coord.split("=")[-1]) for str_coord in reversed(sensor_data)]
    beacon_coord = [int(str_coord.split("=")[-1]) for str_coord in reversed(beacon_data)]

    sensor_coords.append(sensor_coord)
    beacon_coords.append(beacon_coord)
###

### Part 1 ###
print("="*5, "Part 1", "="*5)

def row_covered_area(row:int, sensor_coords: list[list[int]], beacon_coords: list[list[int]],
    limits: tuple=(-math.inf, math.inf)) -> tuple[int, int, ClosedIntervals]:
    row_covered_intervals = ClosedIntervals()
    
    for sensor, beacon in zip(sensor_coords, beacon_coords):
        dist = manhattan_dist(sensor, beacon)

        sensor_row, sensor_col = sensor[0], sensor[1]
        if row >= sensor_row - dist and row <= sensor_row + dist: 
            row_diff = row - sensor_row

            init_col_id = sensor_col - dist + abs(row_diff)
            end_col_id = sensor_col + dist - abs(row_diff)

            row_covered_intervals.add(init_col_id, end_col_id)

    row_num_covered = row_covered_intervals.count(limits=limits)
    
    row_num_beacon_in_covered = 0
    unique_beacons = []
    for beacon in beacon_coords:
        if beacon in unique_beacons:
            continue
        
        unique_beacons.append(beacon)
        if beacon[0] == row and beacon[1] >= limits[0] and beacon[1] <= limits[1]:
            if row_covered_intervals.is_in(beacon[1]):
                row_num_beacon_in_covered += 1

    return row_num_covered, row_num_beacon_in_covered, row_covered_intervals

count_covered, count_beacon, _ = row_covered_area(2000000, sensor_coords, beacon_coords)
print("Impossible beacon positions count:", count_covered - count_beacon)
###

print()

### Part 2 ###
print("="*5, "Part 2", "="*5)

start = time.time()
max_limit = 4000000
possible_pos = None
has_found_possible_pos = False
for row in range(max_limit+1):
    if has_found_possible_pos:
        break

    if row % 100000 == 0 and row > 0:
        running_time = time.time() - start
        print("Time to complete:", round(running_time *(max_limit/row - 1) / 60, 2), "minutes")
        print("Complete:", round(100* row/max_limit, 2), "%")
        print()

    count_covered, _, intervals = row_covered_area(row, sensor_coords, beacon_coords, limits=(0, max_limit))
    if count_covered < max_limit + 1:
        for l in intervals.intervals:
            if l.is_divisor:
                if l.a == l.b and l.a > 0 and l.a < max_limit: 
                    possible_pos = (row, l.a)
                    has_found_possible_pos = True
                    break
                    

print("Tuning frequency:", possible_pos[1] * 4000000 + possible_pos[0])
###