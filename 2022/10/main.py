import AdventOfCode.aoc as aoc
import numpy as np

# Read Input ###
input_path = "input.txt"
# input_path = "test.txt"
data_temp = aoc.get_input(input_path)

data = [None] * len(data_temp)
for id, row in enumerate(data_temp):
    row_split = row.split(" ")
    if len(row_split) == 1:
        command, value = row_split[0], 0
    else:
        command, value = row_split[0], int(row_split[1])

    data[id] = (command, value)
###

command_to_cycles = {"addx": 2, "noop": 1} # How many cycles until the command execution.

### Part 1 ###
print("="*5, "Part 1", "="*5)

register = 1
register_values = {1: 1} # cycle: register value

# Initializing loop variables and executing the first cycle ###
command, value = data[0]
num_execution_cycles = command_to_cycles[command]

num_commands_completed = 0
current_command_cycle = 1
cycle_count = 2 
###

commands_to_run = True
while commands_to_run:
    '''
    The beginning of the loop represents the beginning of the cycle.
    One iteration of the loop is equivalente of one cycle executed.
    The loop needs to start in the second cycle, because there is no cycle before the first.

    It starts by checking whether enough cycles have passed to execute the current command. 
    If it has passed, executes the command updating the register value and starts the next command.
    In the end of the cycle, updates the cycle conter, the command cycle counter and saves the current
    register value. 
    '''
    if current_command_cycle == num_execution_cycles:
        register += value

        num_commands_completed += 1
        commands_to_run = num_commands_completed < len(data)
        if commands_to_run:
            command, value = data[num_commands_completed]
            
            current_command_cycle = 0
            num_execution_cycles = command_to_cycles[command]
    
    register_values[cycle_count] = register
    cycle_count += 1
    current_command_cycle += 1

signal_strength_sum = 0
for cycle in range(20, 221, 40):
    signal_strength_sum += cycle * register_values[cycle]

print("Signal sum:", signal_strength_sum)
###

print()

### Part 2 ###
print("="*5, "Part 2", "="*5)
register = 1
register_values = {1: 1} # cycle: register value

screen_shape = (6, 40)
screen = np.full(fill_value="0", shape=screen_shape)

# Initializing loop variables and executing the first cycle ###
command, value = data[0]
num_execution_cycles = command_to_cycles[command]

num_commands_completed = 0
current_command_cycle = 1
cycle_count = 2 

# CRT execution 
screen[0, 0] = "#"
###

commands_to_run = True
while commands_to_run:
    '''
    The beginning of the loop represents the beginning of the cycle.
    One iteration of the loop is equivalente of one cycle executed.
    The loop needs to start in the second cycle, because there is no cycle before the first.

    It starts by checking whether enough cycles have passed to execute the current command. 
    If it has passed, executes the command updating the register value and starts the next command.
    In the end of the cycle, updates the screen, updates the cycle conter, the command cycle counter and saves the current
    register value. 
    '''
    if current_command_cycle == num_execution_cycles:
        register += value

        num_commands_completed += 1
        commands_to_run = num_commands_completed < len(data)
        if commands_to_run:
            command, value = data[num_commands_completed]
            
            current_command_cycle = 0
            num_execution_cycles = command_to_cycles[command]
        
    # CRT execution ##
    if cycle_count < screen.size+1:
        row = (cycle_count-1) // screen.shape[1]
        column = (cycle_count-1) % screen_shape[1]

        screen_icon = "." 
        if register-2 < column < register+2:
            screen_icon = "#" 

        screen[row, column] = screen_icon
    ###

    register_values[cycle_count] = register
    cycle_count += 1
    current_command_cycle += 1

for i in range(screen.shape[0]):
    for j in range(screen.shape[1]):
        print(screen[i, j], end="")
    print()
###