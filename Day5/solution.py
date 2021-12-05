from collections import defaultdict
## General
# # Read and format the data in a convenient way
with open('input_data.txt', 'r') as f:
    lines = [ # Here they get properly casted and turned to pairs of int tuples
        (tuple(map(int,(p1.strip().split(",")))), tuple(map(int, p2.strip().split(",")))) 
        for p1, p2 in [ # This list is pairs of point strings
            line.split(" -> ") for line in f.readlines()
            ]
        ]
# Constants (help understanding logic)
P1 = X = 0
P2 = Y = 1

# Test functions
is_vertical = lambda line: line[P1][X] == line[P2][X]
is_horizontal = lambda line: line[P1][Y] == line[P2][Y]

## Part 1
print(f'There are {len(lines)} total lines')
hv_lines = list(filter(lambda line : is_vertical(line) or is_horizontal(line), lines))
print(f'There are {len(hv_lines)} Vertical or Horizontal lines')

# We'll use a dictionary to keep track of visited points
# defaultdict is like dict but allows to auto initialize never
# before visited keys with a function (in our case, int returns 0)
visited_points = defaultdict(int)


for line in hv_lines:
    if is_vertical(line):
        x = line[P1][X]
        y_start = min(line[P1][Y], line[P2][Y])
        y_end = max(line[P1][Y], line[P2][Y]) + 1
        for y in range(y_start, y_end):
            visited_points[(x, y)] += 1
    if is_horizontal(line):
        y = line[P1][Y]
        x_start = min(line[P1][X], line[P2][X])
        x_end = max(line[P1][X], line[P2][X]) + 1
        for x in range(x_start, x_end):
            visited_points[(x, y)] += 1

points_visited_more_than_once = list(filter(lambda v: v > 1, visited_points.values()))
print(f'{len(points_visited_more_than_once)} points have been visited more than once by horizontal or vertical lines.')

## Part 2
# We have already done vertical and horizontal so we just need to add diagonals
# We would have done this all in one go were it not for the problem statement.

# This should give us the converse set of lines from above
d_lines = [line for line in lines if line not in hv_lines]

# We already know all of these are diagonal, no need to check,
# This would have been an else in the hv_lines for above
# but using lines and turning the second if to else if

for line in d_lines:
    # Determine if X and Y increase or decrease when we move from P1 to P2
    x_step = 1 if line[P1][X] < line[P2][X] else -1
    y_step = 1 if line[P1][Y] < line[P2][Y] else -1
    # Get the set of points in that line
    points = zip(range(line[P1][X], line[P2][X] + x_step, x_step), range(line[P1][Y], line[P2][Y] + y_step, y_step))
    for point in points:
        visited_points[point] += 1


points_visited_more_than_once = list(filter(lambda v: v > 1, visited_points.values()))
print(f'{len(points_visited_more_than_once)} points have been visited more than once by any line.')

