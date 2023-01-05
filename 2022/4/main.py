import AdventOfCode.aoc as aoc

input_path = "input.txt"
# input_path = "test.txt"
data_temp = aoc.get_input(input_path)

data = [None] * len(data_temp)
for id, row in enumerate(data_temp):
    pair_limits = row.split(",")
    data[id] = ([int(lim) for lim in pair_limits[0].split("-")], 
                [int(lim) for lim in pair_limits[1].split("-")])

### 1 ###
num_overlap = 0
for row in data:
    elf1, elf2 = row

    if elf2[1] - elf2[0] > elf1[1] - elf1[0]:
        elf1, elf2 = elf2, elf1

    if elf1[1] >= elf2[1] and elf1[0] <= elf2[0]:
        num_overlap += 1

print("Fully Contains", num_overlap)
###

### 2 ###
num_overlap = 0
for row in data:
    elf1, elf2 = row

    if elf2[0] < elf1[0]:
        elf1, elf2 = elf2, elf1

    if elf2[0] <= elf1[1]:
        num_overlap += 1
print("Num overlap:", num_overlap)
###