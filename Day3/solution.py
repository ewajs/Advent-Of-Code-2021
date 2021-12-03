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