'''
    The input is processed line by line in the fallowing way:

    * Collect the output of the command.
    * If is a cd command.
        update the current directory variable and added it
        to the file_system.
    * If is a ls command.
        Set the itens in the command output to the current directory
        and add the directory itens to the file system.

    The file system is simply a dictionary with the pair full_path: Directory.

    Directory have a list of it's items and a size property, which calculate it's size recursively.
    Therefore, with that in hands is very straightforward to solve the puzzle.
'''

import AdventOfCode.aoc as aoc

input_path = "input.txt"
# input_path = "test.txt" 
data = aoc.get_input(input_path)

class Item():
    '''
    Represents an item that a directory can have.
    '''
    is_directory: bool
    
    def __init__(self, name, size=0):
        self.name = name
        self.__size = size

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, size):
        self.__size = size

class File(Item):
    is_directory = False

    def __init__(self, name, size):
        super().__init__(name, size)

class Directory(Item):
    is_directory = True

    def __init__(self, name, parent=None, itens: list[Item]=[]):
        super().__init__(name)
        self.parent= parent
        self.itens = itens
        self.has_size_calculated = False

    @property
    def size(self):
        '''
        Iterates over all itens this directory have and add it's size.
        For performance, it only does that once, because it's size is stored in 
        `self.__size`, which is returned after `self.has_size_calculated` is set to True.
        '''
        if not self.has_size_calculated:
            self.has_size_calculated = True

            size = 0
            for item in self.itens:
                size += item.size
            self.__size = size
            return size
        else:
            return self.__size

    @property
    def full_path(self):
        '''
        The full path of this directory.
        '''
        if self.name == "/":
            return "/"
        else:
            return self.parent.full_path + "/" + self.name

### Part 1 ###
file_system = {} # Dictionary with all directorys.

already_ls = [] # Used to check is the ls command has already been run in the current directory. 
skip_ls = False

directory_history = [] # Directory history of the cd commands.

count = 0
num_lines = len(data)
while count < num_lines:
    row = data[count]
    
    # Collects command's output ###
    init_output_id = count+1
    last_output_id = init_output_id
    while data[last_output_id][0] != "$":
        last_output_id +=1
        if last_output_id == num_lines: # The input has terminated
            break
    
    command_output = data[init_output_id: last_output_id]
    count = last_output_id # Set the counter for the next command
    ###

    if row[2:4] == "cd":
        if row[-2:] == "..":
            directory_history.pop(-1)
            current_dir = directory_history[-1]
        else:
            current_dir_name = row.split(" ")[-1]
            
            if len(directory_history) > 0:
                current_dir = Directory(current_dir_name, parent=directory_history[-1])
                if current_dir.full_path in file_system.keys():
                    current_dir = file_system[current_dir.full_path]
                else:
                    file_system[current_dir.full_path] = current_dir

            else: # The first command, which has a directory without parent
                current_dir = Directory(current_dir_name)
                file_system[current_dir.full_path] = current_dir 

            directory_history.append(current_dir)
    else: # ls command
        ###
        # If the ls command has already been run in this directory
        # skip to the next command.
        if current_dir.full_path in already_ls:
            skip_ls = True
        else:
            already_ls.append(current_dir.full_path)
            skip_ls = False

        if skip_ls:
            continue
        ###

        ###
        # Collects all itens in that directory and places them
        # in the same. 
        itens = [] 
        for item in command_output:
            if item[:3] == "dir":
                dir_name = item[4:]
                current_item = Directory(dir_name, current_dir)
                file_system[current_item.full_path] = current_item
            else: # Is a file
                size, name = item.split(" ")
                current_item = File(name, int(size))

            itens.append(current_item)
        
        current_dir.itens = itens
        ###

bigger_dirs_size_sum = 0
for dir in file_system.values():
    dir: Directory
    if dir.size <= 100000:
        bigger_dirs_size_sum += dir.size
print(bigger_dirs_size_sum)
###

### Part 2 ###
current_free_space = 70000000 - file_system["/"].size
space_needed = 30000000 - current_free_space

available_dirs = []
for dir in file_system.values():
    if dir.size >= space_needed:
        available_dirs.append(dir)

print(min(available_dirs, key=lambda x: x.size).size)
###