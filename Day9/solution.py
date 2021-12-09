import math
## General
# Read and format the data in a convenient way
with open('input_data.txt', 'r') as f:
    # We strip the string for whitespace and cast to list (each character)
    # Then we map the int casting to every element of the list and convert
    # the map to a list to get a list of rows (also lists).
    # Note: This makes it so that to interpret as a grid we shoud do
    # lines[y][x] instead of lines[x][y]
    lines = [list(map(int, list(line.strip()))) for line in f.readlines()]

x_limit = len(lines[0])
y_limit = len(lines)

low_points = []

## Part 1
risk_level = 0
# iterate over rows (vertical)
for y in range(y_limit):
    # iterate over columns (horizontal)
    for x in range(x_limit):
        # Make a tuple with the condition for each neighbor
        # All must be true for the point to be a lowest point.
        # If the point is at or alongside of the edge we skip
        # that test marking it true automatically with a bounds check
        conditions = (
            lines[y][x - 1] > lines[y][x] if x > 0 else True,
            lines[y][x + 1] > lines[y][x] if x + 1 < x_limit else True,
            lines[y - 1][x] > lines[y][x] if y > 0 else True,
            lines[y + 1][x] > lines[y][x] if y + 1 < y_limit else True,
        )

        if all(conditions):
            risk_level += lines[y][x] + 1
            # This will come in handy in part 2
            low_points.append((y, x))

print(f"The Risk Level is {risk_level}")


## Part 2: And the complexity skyrockets.

# So now we can probably recursively find the basin of each low point.
def explore_basin(point, basin = None):
    # This should only be our first call
    # recursive calls will pass in the basin
    if basin is None:
        basin = [point] # Initialize an empty basin with our provided point
    
    # Here comes the tricky part
    y, x = point
    height = lines[y][x]
    
    # Make a tuple of tentative points to explore from here
    points_to_explore = ((y, x - 1), (y, x + 1), (y - 1, x), (y + 1, x))
    
    for new_point in points_to_explore:
        # For each one of those, if it is in the map
        yp, xp = new_point
        if xp >= 0 and xp < x_limit and yp >= 0 and yp < y_limit:
            # If it is upwards from the current point, not 9 and not already explored
            if lines[yp][xp] > height and lines[yp][xp] < 9 and new_point not in basin:
                # Add it to our current basin and expand it recursively by exploring 
                # From the new point.
                basin.append(new_point)
                explore_basin(new_point, basin)

    return basin

three_largest_basins = sorted([len(explore_basin(point)) for point in low_points], reverse=True)[:3]

print(f"The three largest basins' size multiplied is {math.prod(three_largest_basins)}")