data_path = "input.txt"


data = []
elf_inventory = []
with open(data_path, "r") as f:
     for line in f.readlines():
        if line == "\n":
            elf_inventory = []
            data.append(elf_inventory)
        else:
            elf_inventory.append(int(line.strip()))

sum_calories = []
for id, elf_inventory in enumerate(data):
    sum_calories.append(sum(elf_inventory))
sum_calories.sort()

print(sum(sum_calories[-3:]))
