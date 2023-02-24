import AdventOfCode.aoc as aoc

# Read Input ###
input_path = "input.txt"
# input_path = "test.txt"
data_temp = aoc.get_input(input_path)

class Signal:
    '''
    Used to generate the python list equivalent of the string representation of a signal.
    '''
    def __init__(self, signal: str) -> None:
        '''
        Calculates the fallowing:
        
        open_id_to_close_id: 
            A map between the open brackets id's and its respective closed brackets id's within the signal.
        
        total_list_str_id:
            A list where the i-th element is a tuple, whose first element is the i-th signal
            character, and the second element is the i-th character id. 

        Parameters:
        -----------
        signal:
            The signal in string representation.
        '''

        self.signal = signal
        self.open_id_to_close_id = self.calc_list_limits_map(signal)
        self.total_list_str_id = list(zip(signal, range(len(signal))))

    @staticmethod
    def calc_list_limits_map(signal: str):
        '''
        Creates a map between the open brackets id's and its respective closed brackets id's within the signal.

        The main idea of this algorithm is that, if we walk through the signal, from left to right, and put every open
        bracket we see inside a list (`open_ids`), every time we see a closed bracket, its respective open bracket
        is the last open bracket in `open_ids` that does not yet have a match.  
        '''
        num_lists = signal.count("[")    
        open_ids = [-1]*num_lists
        close_ids = [-1]*num_lists
        can_use = [False]*num_lists

        count_open = 0
        for id, i in enumerate(signal):
            if i == "[":
                open_ids[count_open] = id
                can_use[count_open] = True
                count_open += 1
            elif i == "]":
                for open_close_id in range(num_lists-1, -1, -1):
                    if can_use[open_close_id]:
                        close_ids[open_close_id] = id+1
                        can_use[open_close_id] = False # Found a match, so can no longer use this open bracket
                        break

        open_id_to_close_id = dict(zip(open_ids, close_ids))
        return open_id_to_close_id

    def get_item(self, list_str_id: list[tuple[str, int]], init_id=1):
        '''
        Given the str list with indices from the complete signal `list_str_id`, generates the python item
        of that list, which starts from the index `init_id` (relative to `list_str_id` and not the complete signal)
        and returns the first index of the next item.

        Parameters:
        -----------
        list_str_id
            List with tuples, which first element is the character and second element is the 
            character id, relative to the complete signal.

        init_id
            Where the item starts, relative to ´list_str_id´, not the complete signal.

        Return:
        -------
        new_item: int | list
            Generated python object that representing the item.
        
        next_init_id: int
            First id of the next item in the str list.
        '''

        first_char = list_str_id[init_id][0]
        
        if first_char == "[": # Item is a list
            open_id = list_str_id[init_id][1]
            close_id = self.open_id_to_close_id[open_id]
            list_item = self.total_list_str_id[open_id:close_id]
            new_item = self.get_list(list_item)
            
            next_init_id = init_id + close_id - open_id + 1
        else: # Item is an integer
            new_item = ""
            count = init_id
            char = list_str_id[count][0]
            while char not in [",", "]"]:
                new_item += char
                count += 1
                char = list_str_id[count][0] 

            new_item = int(new_item)
            next_init_id = count + 1
        
        return new_item, next_init_id

    def get_list(self, list_str_id: list[tuple[str, int]]):
        '''
        Creates the respective python list from the ´list_str_id´.
        '''
        final_list = []
        
        next_init_id = 1
        num_chars = len(list_str_id)
        
        if num_chars == 2: # It's an empty list
            return final_list

        while next_init_id < num_chars:
            next_item, next_init_id = self.get_item(list_str_id, init_id=next_init_id)
            final_list.append(next_item)

        return final_list

    def generate(self):
        '''
        Generates the signal python list
        '''
        return self.get_list(self.total_list_str_id)

data = []
count = 0
while count < len(data_temp):
    signal1 = data_temp[count]
    signal2 = data_temp[count+1]

    list_s1 = Signal(signal1).generate()
    list_s2 = Signal(signal2).generate()

    data.append((list_s1, list_s2))

    count += 3
###

### Part 1 ###
print("="*5, "Part 1", "="*5)

class ItemOrders:
    '''
    Collection of all types of orders two signals can have.

    right:
        When a comparison is satisfied.
    
    wrong:
        When a comparison is failed.
    
    inconclusive:
        When all comparison were not satisfied neither failed.
    '''

    class Order:
        order_id_to_name = {0: "right", 1: "wrong", 2: "inconclusive"}
        def __init__(self, value) -> None:
            self.value = value

        def __eq__(self, other):
            return other.value == self.value

        def __str__(self):
            return self.order_id_to_name[self.value]

    right = Order(0)
    wrong = Order(1)
    inconclusive = Order(2)


def get_order(l1: list, l2: list) -> ItemOrders.Order:
    '''
    Given two signals, check what order are they.

    When a comparison fails or succeed, it returns immediately.

    When at least one signal item is a list, it calls itself.
    '''
    l1_len = len(l1)
    l2_len = len(l2)
    min_len = min((l1_len, l2_len))
    
    count = 0
    while count < min_len: 
        item1, item2 = l1[count], l2[count]

        is_item1_list = isinstance(item1, list) 
        is_item2_list = isinstance(item2, list) 
        if is_item1_list or is_item2_list:
            if not is_item1_list:
                item1 = [item1]
            elif not is_item2_list:
                item2 = [item2]

            itens_order = get_order(item1, item2)
        else:
            if item1 == item2:
                itens_order = ItemOrders.inconclusive
            elif item1 < item2:
                itens_order = ItemOrders.right
            else:
                itens_order = ItemOrders.wrong

        if itens_order != ItemOrders.inconclusive:
            return itens_order
        
        count += 1
    
    # If all comparison between itens were inconclusive, compares the lists length.
    if l1_len < l2_len:
        order = ItemOrders.right
    elif l1_len == l2_len:
        order = ItemOrders.inconclusive
    else:
        order = ItemOrders.wrong

    return order

sum_ids = 0
for id, (s1, s2) in enumerate(data):
    order = get_order(s1, s2)
    if order == ItemOrders.right:
        sum_ids += id +1

print("Sum indices:", sum_ids)
###

print()

### Part 2 ###
print("="*5, "Part 2", "="*5)

all_signals = []
for i in data:
    all_signals.extend(i)
all_signals.extend([[[2]], [[6]]])

def sort_signals(signals):
    '''
    Sort signals according to the ordering rules described in the puzzle.
    '''
    has_sorted = True
    num_signals = len(signals)
    while has_sorted:
        has_sorted = False
        for i in range(num_signals-1):
            order = get_order(signals[i], signals[i+1])
            if order == ItemOrders.wrong:
                has_sorted = True
                signals[i], signals[i+1] = signals[i+1], signals[i]

sort_signals(all_signals)

# for s in all_signals:
#     print(s)

distress_signal= (all_signals.index([[2]]) +1) * (all_signals.index([[6]]) + 1)
print("Distress signal:", distress_signal)
###