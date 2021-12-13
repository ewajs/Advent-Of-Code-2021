## General
# Read and format the data in a convenient way
with open('input_data.txt', 'r') as f:
    raw_dots, raw_instructions  = f.read().split('\n\n')

# Cast to integer and convert to a set of tuples
a_dots = set(tuple(map(int, raw_dot.split(','))) for raw_dot in raw_dots.split('\n'))

# Convert the value to an integer
instructions = [(coordinate, int(value)) for coordinate, value in [
    tuple(raw_instruction.split('fold along ')[1].split('=')) for raw_instruction in raw_instructions.split('\n')
    ]
]

# Constants
X = 0
Y = 1

## Part 1

def fold(dots, instruction):
    # We'll leverage sets to handle the dot duplication for us
    x_max = max(dot[X] for dot in dots)
    y_max = max(dot[Y] for dot in dots)
    value = instruction[1]
    # To fold we just create a new set with a coordinate transform
    # It looks like the problem ensures we're always folding 
    # in halves so no negative coordinates appear
    if instruction[0] == 'x':
        return set(dot if dot[X] < value else (2 * value - dot[X], dot[Y]) for dot in dots)
    elif instruction[0] == 'y':
        return set(dot if dot[Y] < value else (dot[X], 2 * value - dot[Y]) for dot in dots)

print(f"There are {len(fold(a_dots, instructions[0]))} after doing the first fold")

## Part 2

# And now the problem requires us to graphically represent the dots after doing
# all folds so we'll use our sets and then transform that into something easy to
# print.

final_fold = a_dots
for instruction in instructions:
    final_fold = fold(final_fold, instruction)

x_max = max(dot[X] for dot in final_fold) + 1
y_max = max(dot[Y] for dot in final_fold) + 1

for y in range(y_max):
    for x in range(x_max):
        print('#' if (x, y) in final_fold else '.', end='')
    print('')