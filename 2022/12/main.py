import AdventOfCode.aoc as aoc
import numpy as np
from collections import Counter

alphabet_list = list(map(chr, range(ord('a'), ord('z')+1)))
letter_to_number = dict( zip( alphabet_list, range(len(alphabet_list)) ) )
letter_to_number["S"] = letter_to_number["a"]
letter_to_number["E"] = letter_to_number["z"]

# Read Input ###
input_path = "input.txt"
# input_path = "test.txt"
data_temp = aoc.get_input(input_path)

init_pos, end_pos = (0, 0), (0, 0)
data = [None] * len(data_temp)
for id, row in enumerate(data_temp):
    if "S" in row:
        init_pos = (id+1, row.index("S")+1)
    if "E" in row:
        end_pos = (id+1, row.index("E")+1)

    height_map_row = [letter_to_number[letter] for letter in row]
    data[id] = height_map_row

data = np.array(data)

height_map = np.full((data.shape[0]+2, data.shape[1]+2), 100) 
height_map[1:-1, 1:-1] = data
###

### Part 1 ###
class HeightMapGraph:
    neighbors_directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    neighbors_directions = [np.array(i) for i in neighbors_directions]

    def __init__(self, height_map: np.ndarray) -> None:
        self.heigh_map = height_map
    
        self.order_nodes = {}
        
        self.marked = np.ones(height_map.shape, dtype=int)
        self.marked[1:-1,1:-1] = 0

    def bfs(self, start_node: tuple):
        queue = [start_node]

        order = 0
        while len(queue) > 0:
            self.order_nodes[order] = queue
            for node in queue:
                self.marked[node[0], node[1]] = 1

            new_queue = []
            for node in queue:    
                for new_node in self.get_valid_neighbors(node):
                    if new_node not in new_queue:
                        new_queue.append(new_node)

            queue = new_queue
            order += 1

    def get_valid_neighbors(self, node: tuple):
        valid_neighbors = []
        for direction in self.neighbors_directions:
            neighbor_node = np.array(node) + direction
            neighbor_height = self.heigh_map[neighbor_node[0], neighbor_node[1]]
            
            delta_height =  neighbor_height - self.heigh_map[node[0], node[1]]

            if delta_height < 2 and not self.marked[neighbor_node[0], neighbor_node[1]]:
                valid_neighbors.append(tuple(neighbor_node))
        
        return valid_neighbors

    def print_order_nodes(self):
        orders = list(self.order_nodes.keys())
        orders.sort()

        for o in orders:
            print(o, end=": ")
            for node in self.order_nodes[o]:
                print(node, end=", ")
            print()

    def get_node_order(self, node):
        for order, nodes in graph.order_nodes.items():
            if node in nodes:
                return order

graph = HeightMapGraph(height_map)
graph.bfs(init_pos)
print("Number of fewest steps:", graph.get_node_order(end_pos))
###

print()

### Part 2 ###
print("="*5, "Part 2", "="*5)

###