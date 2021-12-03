## General
# Read and format the data in a convenient way
from os import extsep


with open('input_data.txt', 'r') as f:
    lines = [line.strip() for line in f.readlines()]

# Make a list of counters starting at 0 for each position on the string
counters = [0 for _ in lines[0]]

# Count the amount of 1s in each position
for line in lines:
    for index, bit in enumerate(line):
        counters[index] += 1 if bit == '1' else 0

# If the counter is greater than half, then 1 is the most common bit, otherwise 0
half = len(lines) / 2

# Start empty strings that we'll fill in
gamma_rate = ''
epsilon_rate = ''

for counter in counters:
    if counter > half:
        gamma_rate += '1'
        epsilon_rate += '0'
    else:
        gamma_rate += '0'
        epsilon_rate += '1'

# Now convert the bit string to a decimal value
gamma_rate = int(gamma_rate, 2)
epsilon_rate = int(epsilon_rate, 2)

print(f"Power is {gamma_rate * epsilon_rate}")