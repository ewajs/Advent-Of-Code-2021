## General
# Read and format the data in a convenient way
with open('input_data.txt', 'r') as f:
    crabs = [int(crab) for crab in f.readline().split(",")]


## Part 1

# We can create a dictionary whose keys are the positions
# And populate it with the total amount required for all
# crabs to go to that position
max_position = max(crabs) + 1
fuel_per_position = {p: sum(abs(v - p) for v in crabs) for p in range(max_position)}

least_fuel = min(fuel_per_position.values())

print(f"Part 1: {least_fuel} is the least amount of fuel needed.")

## Part 2
# Same as above but we'll use a different computation for fuel,
# and we'll do it in one go!

least_fuel = min({p: sum(sum(range(1, abs(p - v) + 1)) for v in crabs) for p in range(max_position)}.values())

print(f"Part 2: {least_fuel} is the least amount of fuel needed.")
