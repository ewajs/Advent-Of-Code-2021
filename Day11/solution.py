## General
# Read and format the data in a convenient way
with open('input_data.txt', 'r') as f:
    # This time we'll use a dictionary of points to track our octopuses
    lines = [list(map(int, list(line.strip()))) for line in f.readlines()]


## Part 1
x_limit = len(lines)
y_limit = len(lines[0])    
octopuses = {(x, y) : lines[y][x] for y in range(y_limit) for x in range(x_limit)}

# This helped me debug issues in my logic
def print_o(octopuses):
    oct_str = "\n".join(["".join([str(octopuses[(x,y)]) for x in range(x_limit)]) for y in range(y_limit)])
    print(oct_str)

# As I see this problem, there's one thing we need to do once per step and another
# that we should do recursively until a condition is met, so we'll solve this
# with a loop that does the once per step action and then delegates the recursive
# action to a second block of code

def propagate_flashes(octopuses, flash_positions):
    # Now we need to find the places where an octopus will flash
    new_flash_positions = [k for k in octopuses.keys() if octopuses[k] == 10]
    # Reset those to 0
    octopuses = {k: v if v < 10 else 0 for k, v in octopuses.items()}

    if len(new_flash_positions) == 0:
        # This is our base case, no new flashes to propagate
        return octopuses, flash_positions
    # If the above didn't happen, we have flashes to count and propagate
    flash_positions += new_flash_positions
    # Now, we propagate our flashes to non 0 octopuses (octopuses on flash positions)
    # First all new positions to increase
    new_positions = []
    for delta_x in (-1, 0, 1):
        for delta_y in (-1, 0, 1):
            new_positions += [
                (x + delta_x, y + delta_y) for x, y in new_flash_positions 
                if 0 <= x + delta_x < x_limit and 0 <= y + delta_y < y_limit and (x + delta_x, y + delta_y) not in new_flash_positions
                ]
    for p in new_positions:
        octopuses[p] += 1 if octopuses[p] not in (0, 10) else 0

    return propagate_flashes(octopuses, flash_positions)

def run_step(octopuses, flash_positions):
    # First we increase all octopuses by 1
    octopuses = {k: v + 1 for k, v in octopuses.items()}
    # Then we let flashes propagate and trigger and once they stop we go again
    return propagate_flashes(octopuses, flash_positions)

flash_positions = []
for step in range(100):
    octopuses, flash_positions = run_step(octopuses, flash_positions)
   

print(f"There have been {len(flash_positions)} flashes")

## Part 2

# We'll increase steps until all flash together
all_flashed = False
step_counter = 0

# Restart our octopuses dict and flash_positions list
octopuses = {(x, y) : lines[y][x] for y in range(y_limit) for x in range(x_limit)}
flash_positions = []

while not all_flashed:
    octopuses, flash_positions = run_step(octopuses, flash_positions)
    all_flashed = all(v == 0 for v in octopuses.values())
    step_counter += 1

print(f"It takes {step_counter} steps for all octopuses to synchronize")
