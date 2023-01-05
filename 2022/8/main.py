'''
Part 1:
First I constructed a method which count all visible trees for a given line 
(It can be a row or column) when looking directly in this line. After I iterate over
all possible lines (all possible rows and columns) keeping the count of how many trees
are visible.

OBS: I keep track of the visible trees with a mask, to not count them twice.

Part 2:
Iterate over all trees, look for each side and count how many trees are visible.
'''

import AdventOfCode.aoc as aoc
import numpy as np

# Read Input ###
input_path = "input.txt"
# input_path = "test.txt"
data_temp = aoc.get_input(input_path)

data = [None] * len(data_temp)
for id, row in enumerate(data_temp):
    row_numbers = [int(i) for i in row]
    data[id] = row_numbers
data = np.array(data)
###

### Part 1 ###
print("="*5, "Part 1", "="*5)
class Line:
    size: int

    @staticmethod
    def get_data_id(line_number, id):
        '''
        Data id (row, col) of the line element whose id=`id` 
        '''

        pass

class Row(Line):
    size = data.shape[0]

    @staticmethod
    def get_data_id(line_number, id):
        return line_number, id

class Column(Line):
    size = data.shape[1]

    @staticmethod
    def get_data_id(line_number, id):
        return id, line_number

def line_num_visible_trees(line_number: int, line_type: Line, reverse: bool=False, reverse_stop_id: int = 0):
    '''
    Calculates all visible trees when looking directly to this line, from both sides, taking into 
    account if some tree has been already marked as visible from another line.
    
    Parameters:
    -----------
    line_numbers: int
        The id of this line in the data. For exemple:
            * The row line `data[0, :]` has line_number = 0
            * The row line `data[3, :]` has line_number = 3
            * The column line `data[:, 0]` has line_number = 0
    
    line_type: Line
        The type of the line. It can be row or column.

    reverse: bool
        If true it calculates the visible trees when looking in the opposite side of the line.
    
    rever_stop_id: int
        The tree id to stop the iteration when reverse is true. This is set to the hightest tree in the line, which
        is calculated when reverse is False. 
    
    Return:
    -------
        num_visible_trees: int
            Number os trees visible when looking directly to this line, from both sides, taking into 
            account if some tree has been already marked as visible from another line.
    '''
    num_visible_trees = 0

    if reverse:
        id_range = range(line_type.size-1, reverse_stop_id, -1)
    else:
        id_range = range(line_type.size)

    current_max = -1
    max_id = 0
    for id in id_range:
        row_id, col_id = line_type.get_data_id(line_number, id)

        if data[row_id, col_id] > current_max:
            current_max = data[row_id, col_id]
            max_id = id

            if not is_visible[row_id, col_id]:
                is_visible[row_id, col_id] = 1
                num_visible_trees += 1
    
    if not reverse:
        num_visible_trees += line_num_visible_trees(line_number, line_type, reverse=True, reverse_stop_id=max_id)
    
    return num_visible_trees

is_visible = np.zeros(data.shape)

num_visible_trees = 0
for i in range(data.shape[0]):
    num_visible_trees += line_num_visible_trees(i, Row)

for i in range(data.shape[1]):
    num_visible_trees += line_num_visible_trees(i, Column)

print("Num visible trees:", num_visible_trees)
###

print()

### Part 2 ###
print("="*5, "Part 2", "="*5)

offset_list = [[1, 0], [0, 1], [-1, 0], [0, -1]]
offset_list = [np.array(i) for i in offset_list]

max_tree_score = 0
for i in range(1, data.shape[0]-1):
    for j in range(1, data.shape[1]-1):
        tree_id = np.array([i, j])
        tree_height = data[i, j]
        tree_score = 1

        for offset in offset_list:
            num_visible_trees = 0
            side_tree_height = -1
            while side_tree_height < tree_height:
                num_visible_trees += 1
                
                side_tree_id = tree_id + offset * num_visible_trees
            
                # Has reached the end of the forest
                if side_tree_id[0] == 0 or side_tree_id[0] == data.shape[0]-1 or side_tree_id[1] == 0 or side_tree_id[1] == data.shape[1]-1:
                    break
            
                side_tree_height = data[side_tree_id[0], side_tree_id[1]]                

            tree_score *= num_visible_trees
        
        if tree_score > max_tree_score:
            max_tree_score = tree_score

print("Max score:", max_tree_score)
###