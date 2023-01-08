import AdventOfCode.aoc as aoc

class Monkey:
    def __init__(self, items: list[int], operation, test_num: int, test_true_id: int, test_false_id: int, monkey_list: list) -> None:
        self.items = items
        self.operation = operation
        
        self.test_num = test_num
        self.test_true_id = test_true_id
        self.test_false_id = test_false_id
        
        self.monkey_list = monkey_list

        self.num_process_itens = 0


    def process_itens(self):
        self.num_process_itens += len(self.items)
        for item in self.items:
            item = self.operation(item)
            item = int(item / 3)

            if item % self.test_num == 0:
                self.monkey_list[self.test_true_id].items.append(item)
            else:
                self.monkey_list[self.test_false_id].items.append(item)

        self.items = []

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
monkey_list = []
while count < len(data_temp):
    items = data_temp[count].split(":")[-1].split(",")
    items = [int(i.strip()) for i in items]
    
    operation = get_operation(data_temp[count + 1])

    test_num, test_true_id, test_false_id = get_test_info(data_temp[count + 2: count + 5])

    monkey = Monkey(items, operation, test_num, test_true_id, test_false_id, monkey_list)
    monkey_list.append(monkey)

    monkey_id += 1
    count += 7
###


### Part 1 ###
print("="*5, "Part 1", "="*5)

monkey: Monkey
for round_id in range(20):
    for monkey in monkey_list:
        monkey.process_itens()

monkeys_process_itens = []
for monkey in monkey_list:
    monkeys_process_itens.append(monkey.num_process_itens)

monkeys_process_itens.sort()
print("Monkey business:", monkeys_process_itens[-1] *monkeys_process_itens[-2])
###

print()

### Part 2 ###
print("="*5, "Part 2", "="*5)

###