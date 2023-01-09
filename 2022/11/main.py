'''
Reading the data: First is created a monkey object, than the same is put into a monkey list object. 
This is done for all monkeys in the input.

A monkey object has a method to process all itens that it is holding in the moment, therefore for each
round I just need to iterate over the monkeys and call this method.

Each part has it's process item method, because the second part it's a little more complex.

Part 1: 
    This part was solved very straightforward, just fallowing the rules the puzzle stated.

Part 2:
    Every monkey has a test to perform when deciding for which monkey to pass the item. This
    test consists checking the divisibility of the item worry level by some number, which I will 
    call `test_num`.
    
    Instead of keeping items worry levels, for each item is calculated it's remainder by every `test_num`.
    Then this remainders are used when processing the items, instead the items worry levels. The only difference 
    is that it's needed to recalculate the remainder after the operation is applied to the remainder.
'''

import AdventOfCode.aoc as aoc

class Monkey:
    def __init__(self, id, items: list[int], operation, test_num: int, test_true_id: int, test_false_id: int, monkey_list: list) -> None:
        '''
        Creates a monkey with all information about it's operation and test to passa the item.
        
        The variable `items_remainders` is used in the second part.
        It has the same number of elements as `items` and the ith element it's
        a list containing the remainder of the ith element in `item` for the number
        used in the test for each monkey.

        Parameters:
        -----------
            id: int
                The number of the monkey.

            items: list[int]
                Every worry level item the monkey is holding in the moment.
            
            operation: function
                Function whose input is the old item and the output is the item, 
                according to the input.
            
            test_num: int
                Number that the item must be divisible to pass in the monkey test.
            
            test_true_id: int
                Monkey id to which the item will be passes if the test evaluates to true. 

            test_false_id: int
                Monkey id to which the item will be passes if the test evaluates to false.

            monkey_list: list[Monkey]
                List with all the monkeys. The ith item in the list is the monkey
                whose id is i.
        '''
        self.id = id
        
        self.items = items
        
        # Used for part 2 ##
        self.items_remainders = []

        self.operation = operation
        
        self.test_num = test_num
        self.test_true_id = test_true_id
        self.test_false_id = test_false_id
        
        self.monkey_list = monkey_list

        self.num_process_items = 0

    def process_items(self):
        '''
        Process all the itens that the monkey is holding in the moment,
        according to the rules stated in the puzzle. Also keep track of how many
        itens were processes in the variable `self.num_process_items`.
        '''
        # How many items were processed
        self.num_process_items += len(self.items)
        
        for item in self.items:
            item = self.operation(item)
            item = int(item / 3)

            # Giving the item to another monkey
            if item % self.test_num == 0:
                self.monkey_list[self.test_true_id].items.append(item)
            else:
                self.monkey_list[self.test_false_id].items.append(item)

        # Reset the itens, because all of them were given to another monkey.
        self.items = []

    def process_items_part_2(self):
        '''
        
        '''

        self.num_process_items += len(self.items_remainders)
        for item in self.items_remainders:
            new_item = []
            for remainder, test_num in zip(item, test_num_list):
                new_item.append(self.operation(remainder) % test_num)

            if new_item[self.id] == 0:
                self.monkey_list[self.test_true_id].items_remainders.append(new_item)
            else:
                self.monkey_list[self.test_false_id].items_remainders.append(new_item)

        self.items_remainders = []

class MonkeyList:
    def __init__(self) -> None:
        '''
        Represent a list of monkeys with some useful methods related to the puzzle.    
        '''
        # List with all the monkeys
        self.monkeys = []

        # List with all the numbers used in the test to decide which monkey to give the item.
        # The ith element in the list is the number used in the monkey test whose id is i.
        self.test_num_list = []

    def add_monkey(self, monkey: Monkey):
        self.monkeys.append(monkey)
    
    def reset_num_process_items(self):
        '''
        Reset the count of the items processed by the monkeys. This is used
        to reset the result of part 1.
        '''
        monkey: Monkey
        for monkey in self.monkeys:
            monkey.num_process_items = 0

    def create_items_remainders(self):
        '''
        For each item of each monkey is created the remainder for each
        number used in the tests.
        '''

        monkey: Monkey
        for monkey in self.monkeys:
            items_remainders = []
            for item in monkey.items:
                remainders = [(item % test_num) for test_num in test_num_list]
                items_remainders.append(remainders)
            
            monkey.items_remainders = items_remainders
        
    @property
    def monkey_business(self):
        monkeys_process_itens = []
        monkey: Monkey
        for monkey in self.monkeys:
            monkeys_process_itens.append(monkey.num_process_items)

        monkeys_process_itens.sort()

        return monkeys_process_itens[-1] * monkeys_process_itens[-2]

# Read Input ###
input_path = "input.txt"
# input_path = "test.txt"
data_temp = aoc.get_input(input_path)

def get_operation(string: str):
    operation_str = string.split("= ")[-1]
    components = operation_str.split(" ")
    c1, operator, c2 = components

    if c1 == "old":
        if c2 == "old":
            if operator == "*":
                return lambda x: x * x
            else:
                return lambda x: x + x
        else:
            if operator == "*":
                return lambda x: x * int(c2)
            else:
                return lambda x: x + int(c2)
    else:
        if operator == "*":
            return lambda x: int(c1) * x
        else:
            return lambda x: int(c1) + x

def get_test_info(string: list[str]):
    test_num = int(string[0].split(" ")[-1])
    test_true_id = int(string[1].split(" ")[-1])
    test_false_id = int(string[2].split(" ")[-1])
    
    return test_num, test_true_id, test_false_id

count = 1
monkey_id = 0
monkey_list = MonkeyList()
test_num_list = []
while count < len(data_temp):
    items = data_temp[count].split(":")[-1].split(",")
    items = [int(i.strip()) for i in items]
    
    operation = get_operation(data_temp[count + 1])

    test_num, test_true_id, test_false_id = get_test_info(data_temp[count + 2: count + 5])
    test_num_list.append(test_num)

    monkey = Monkey(monkey_id, items, operation, test_num, test_true_id, test_false_id, monkey_list.monkeys)
    monkey_list.add_monkey(monkey)

    monkey_id += 1
    count += 7
###

monkey_list.test_num_list = test_num_list
monkey_list.create_items_remainders()

### Part 1 ###
print("="*5, "Part 1", "="*5)

monkey: Monkey
for round_id in range(20):
    for monkey in monkey_list.monkeys:
        monkey.process_items()

print("Monkey business:", monkey_list.monkey_business)
###

print()

### Part 2 ###
print("="*5, "Part 2", "="*5)
monkey_list.reset_num_process_items()

monkey: Monkey
for round_id in range(10000):
    for monkey in monkey_list.monkeys:
        monkey.process_items_part_2()

print("Monkey business:", monkey_list.monkey_business)
###