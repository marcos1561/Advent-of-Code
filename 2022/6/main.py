import AdventOfCode.aoc as aoc

input_path = "input.txt"
# input_path = "test.txt"
data_temp = aoc.get_input(input_path)

data = data_temp[0]

### 1 ###
for i in range(4, len(data)+1):
    if len(set(data[i-4:i])) == 4:
        last_pos = i
        break
print(i)
###

### 2 ###
for i in range(14, len(data)+1):
    if len(set(data[i-14:i])) == 14:
        last_pos = i
        break
print(i)
###