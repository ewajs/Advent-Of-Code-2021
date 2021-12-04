## General
# Read and format the data in a convenient way
with open('input_data.txt', 'r') as f:
    lines = [line.strip() for line in f.readlines()]


## Part 1

# Make a list of counters starting at 0 for each position on the string
counters = [0 for _ in lines[0]]

# Count the amount of 1s in each position
for line in lines:
    for index, bit in enumerate(line):
        counters[index] += 1 if bit == '1' else 0

# If the counter is greater than half, then 1 is the most common bit, otherwise 0
half = len(lines) / 2

# Compute the rates using a joined list comprehension, then cast to integer in base 2
gamma_rate = int(''.join(['1' if counter > half else '0' for counter in counters]), 2)
epsilon_rate = int(''.join(['0' if counter > half else '1' for counter in counters]), 2)

print(f"Power is {gamma_rate * epsilon_rate}")

## Part 2

# This is a werid one to explain but smells to recursion
# We could also have our function take a function evaluator as parameter to have a little less code
# but this is confusing enough


def oxygen(lines, index = 0):
    # If we receive a single element, then that's the answer, this is our base case
    # index == len(lines[0]) is also a base case but seems like the problem ensures it won't happen
    if len(lines) == 1 or index == len(lines[0]):
        return lines[0]
    # Otherwhise, compute the total 
    total = len(lines)
    # if more than half of the elements at this index are 1 then 1 is popular, otherwhise 0 is popular
    popular = '1' if sum([1 if line[index] == '1' else 0 for line in lines]) >= total / 2 else '0'
    # Produce a new list composed only of the items who have a popular digit at index
    new_lines = [line for line in lines if line[index] == popular]
    # Recurse on ourselves until we get a single element
    return oxygen(new_lines, index + 1)

# This is self explanatory given the above (only change is List Comprehension and naming)
def co2(lines, index = 0):
    if len(lines) == 1:
        return lines[0]
    total = len(lines)
    unpopular = '1' if sum([1 if line[index] == '1' else 0 for line in lines]) < total / 2 else '0'
    new_lines = [line for line in lines if line[index] == unpopular]
    return co2(new_lines, index + 1)

print(f'Life Support Rating is {int(oxygen(lines), 2) * int(co2(lines), 2)}')