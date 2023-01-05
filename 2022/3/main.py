import AdventOfCode.aoc as aoc

input_path = "input.txt"
# input_path = "test.txt"
data_temp = aoc.get_input(input_path)

data = [None] * len(data_temp)
for id, row in enumerate(data_temp):
    num_compartment_itens = int(len(row)/2)
    data[id] = (row[:num_compartment_itens], row[num_compartment_itens:])

### 1 ###
alphabet = "abcdefghijklmnopqrstuvwxyz"
alphabet = alphabet + alphabet.upper()
def get_priority(item):
    return alphabet.index(item) + 1

total_priority = 0
for row in data:
    c1, c2 = row

    for item in c1:
        if item in c2:
            total_priority += get_priority(item)
            break
print("Total priority:", total_priority)
###

### 2 ###
def all_items(row):
    return row[0] + row[1]

total_priority = 0
for id in range(0, len(data), 3):
    for item in all_items(data[id]):
        if item in all_items(data[id+1]):
            if item in all_items(data[id+2]):
                total_priority += get_priority(item)
                break

print("Total priority:", total_priority)    
###