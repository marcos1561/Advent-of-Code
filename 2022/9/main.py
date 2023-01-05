import AdventOfCode.aoc as aoc
import numpy as np

# Read Input ###
input_path = "input.txt"
# input_path = "test.txt"
data_temp = aoc.get_input(input_path)

data = [None] * len(data_temp)
for id, row in enumerate(data_temp):
    row_split = row.split(" ")
    data[id] = (row_split[0], int(row_split[1]))
###

class Rope:
    # Direction name to the corresponding movement vector.
    direction_2_vector = {"R": [1, 0], "U": [0, 1], "L": [-1, 0], "D": [0, -1]}
    for key, value in direction_2_vector.items():
        direction_2_vector[key] = np.array(value, dtype=int)

    def __init__(self, knots: list[np.ndarray]) -> None:
        '''
        Creates a rope with some knots.

        Parameters:
        -----------
            knots: list[ndarray]
                This list contains the knots which form the rope. The first elements is the head,
                the second is the knot after the head and so on. Therefore, the last element is the tail.
        '''

        self.knots = knots
        self.unique_tail_positions = [] # List with all unique positions id's the tail has visited.

    def update(self, direction: str, amount: int):
        '''
        Updates rope knots positions given head movements. 
        It updates knots from head to tail.
        It also keep track os all the unique positions the tail has visited.

        Parameters:
        ------------
            direction: str
                The direction the had will move. It can be "R", "L", "D" and "U".
            
            amount: int
                The amount of step the head will move in the given direction.
        
        Return:
            None
        '''
        for _ in range(amount):
            self.knots[0] += Rope.direction_2_vector[direction]
            
            for knot_id in range(1, len(self.knots)):
                knot_pos = self.knots[knot_id]
                parent_pos = self.knots[knot_id - 1]
                self.knots[knot_id] = self.update_knot_pos(knot_pos, parent_pos)

            # Keep track of the unique positions the tail visited ##
            current_tail_pos = self.knots[-1]
            new_pos_id = Rope.position_id(current_tail_pos)
            if new_pos_id not in self.unique_tail_positions:
                self.unique_tail_positions.append(new_pos_id)

    @staticmethod
    def update_knot_pos(knot_pos: np.ndarray, parent_pos: np.ndarray):
        '''
        Update a knot position according the rules described in the puzzle.

        The idea is to calculate the minimum numbers of steps the knot needs to do
        to get to the parent position (which I call `distance`). Since the knot can move diagonally, this can be 
        easily calculated using the position vector from `knot_pos` to `parent_pos` (`delta_pos`),
        because the maximum absolute component of this victor is the `distance`.

        Therefore, if the `distance` is grater than 1, the knot position needs to be updated. Again, the update
        movement the knot needs to do (which I call `knot_move`) can be calculated from 'delta_pos', because this vector with normalized components
        is exactly the movement the knot needs to do.

        Parameters:
        -----------
            knot_pos: ndarray
                The start position of the knot to update.
        
            parent_pos: ndarray
                The parent knot position of the knot to update.

        Return:
        -------
            nparray
                Updated knot position.

        '''
        delta_pos = parent_pos - knot_pos
        distance = max(abs(delta_pos)) 
        
        if distance > 1:
            # Normalizing delta_pos components ##
            knot_move = np.zeros(2, dtype=int)
            for i in range(2):
                if delta_pos[i] != 0:
                    knot_move[i] = delta_pos[i]/abs(delta_pos[i])
            ###

            knot_pos += knot_move
        
        return knot_pos

    @staticmethod
    def position_id(pos: np.ndarray):
        '''
        Unique id that identify a position a knot can have.
        '''
        return str(pos[0]) + "|" +  str(pos[1])

### Part 1 ###
print("="*5, "Part 1", "="*5)

head_pos = np.array((0, 0), dtype=int)
tail_pos = np.array((0, 0), dtype=int)
knots = [head_pos, tail_pos]
rope = Rope(knots)

for direction, amount in data:
    rope.update(direction, amount)

print("Num tail unique positions:", len(rope.unique_tail_positions))
###

print()

### Part 2 ###
print("="*5, "Part 2", "="*5)

num_knots = 10
knots = [np.array((0, 0), dtype=int) for _ in range(num_knots)]
rope = Rope(knots)

for direction, amount in data:
    rope.update(direction, amount)

print("Num tail unique positions:", len(rope.unique_tail_positions))
###