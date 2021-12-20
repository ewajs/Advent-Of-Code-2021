## General
# Read and format the data in a convenient way
with open('input_data.txt', 'r') as f:
    # We'll use a dictionary of points to track our grid (and we'll call it a graph)
    line = f.readline()

# Constants
X = 0
Y = 1

# F··k it it's too late and I'm already behind. I'm brute forcing this one.

x_start, x_stop = line.split('x=')[1].split(',')[0].split('..')
x_start, x_stop = int(x_start), int(x_stop)

y_start, y_stop = line.split('y=')[1].split('..')
y_start, y_stop = int(y_start), int(y_stop)


def shoot_probe(velocity):
    position = [0, 0]
    current_velocity = velocity
    while position[Y] >= y_start:
        position[X] = position[X] + current_velocity[X]
        position[Y] = position[Y] + current_velocity[Y]
        current_velocity[X] = current_velocity[X] - 1 if current_velocity[X] > 0 else 0
        current_velocity[Y] -= 1
        if x_start <= position[X] <= x_stop and y_start <= position[Y] <= y_stop:
         #   print("Hit Target!")
            return True
    #print("Miss Target")
    return False

max_y_v = 0
solutions = []
for x_v in range(0, 1000):
    for y_v in range(-200, 1000):
        #print(f'Evaluating {x_v}, {y_v}')
        if shoot_probe([x_v, y_v]):
            solutions.append((x_v, y_v))
            if y_v > max_y_v:
                max_y_v = y_v

max_height = sum(range(max_y_v + 1))
print(f"The Max Height Reached is {max_height}")
print(f"The total amount of solutions is {len(solutions)}")