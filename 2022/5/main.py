import AdventOfCode.aoc as aoc
import numpy as np

input_path = "input.txt"
# input_path = "test.txt"
data_temp = aoc.get_input(input_path, to_strip=False)


box_cfg = []
instructions = []
num_box = 0
is_init_cfg = True
for id, row in enumerate(data_temp):
    if row[:2] == " 1":
        num_addicional_rows = num_box - len(box_cfg)

        if num_addicional_rows > 0:
            box_cfg = ([[" "]*len(box_cfg[0])] * num_addicional_rows) + box_cfg

        box_cfg = box_cfg + [["-"]*len(box_cfg[0])]
        box_cfg = np.array(box_cfg)
        init_box_cfg = box_cfg.copy()
        is_init_cfg = False

    if is_init_cfg:
        box_row = [] 
        for i in range(0, len(row), 4):
            box = row[i+1: i+2]
            if box != " ":
                num_box += 1

            box_row.append(row[i+1: i+2])
        box_cfg.append(box_row)
    elif row[0] == "m":
        row_instruction = row.strip().split(" ")
        instruction = [row_instruction[1], row_instruction[3], row_instruction[-1]]  
        instruction = [int(i) for i in instruction]
        instructions.append(instruction)

### 1 ###
def get_last_box(col):
    box = " "
    row = -1
    
    while box == " ":
        row += 1
        box = box_cfg[row, col]

    return box, row

for amount, init, final in instructions:
    init -= 1
    final -= 1

    first_box_move, row_first = get_last_box(init)
    
    box_to_move = list(box_cfg[row_first: row_first+amount, init])
    box_cfg[row_first:row_first+amount, init] = " "

    last_box_destination, row_destination = get_last_box(final)

    box_to_move.reverse()
    box_cfg[row_destination-amount: row_destination, final] = box_to_move

top_box = []
for j in range(box_cfg.shape[1]):
    box_name, _ = get_last_box(j)
    top_box.append(box_name)
    
print("".join(top_box))
###

### 2 ###
box_cfg = init_box_cfg.copy()
for amount, init, final in instructions:
    init -= 1
    final -= 1

    first_box_move, row_first = get_last_box(init)
    
    box_to_move = list(box_cfg[row_first: row_first+amount, init])
    box_cfg[row_first:row_first+amount, init] = " "

    last_box_destination, row_destination = get_last_box(final)

    box_cfg[row_destination-amount: row_destination, final] = box_to_move

top_box = []
for j in range(box_cfg.shape[1]):
    box_name, _ = get_last_box(j)
    top_box.append(box_name)
    
print("".join(top_box))
###