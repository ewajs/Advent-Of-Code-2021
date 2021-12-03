## General
# Read and format the data in a convenient way
with open('input_data.txt', 'r') as f:
    # In the nested List Comprehension we get a list of instructions, split by the space, so
    # the first value is the direction and second the value
    # Then we iterate over these pairs to cast the value and leave data ready for consumption
    instructions = [(direction, int(value)) for direction, value in [instruction.strip().split(" ") for instruction in f.readlines()]]


## Part 1

# We'll track our position here
coordinates = {'horizontal': 0, 'depth': 0}

# We'll use this data structure as decoder so we can make a one liner in the for
instructions_decoder = { 
                        'forward': {
                            'axis': 'horizontal',
                            'sign':  +1
                            }, 
                        'up': {
                            'axis':'depth',
                            'sign': -1
                            },
                        'down': {
                            'axis': 'depth',
                            'sign': +1
                            }
                        }

for direction, value in instructions:
    coordinates[instructions_decoder[direction]['axis']] += instructions_decoder[direction]['sign'] * value

print(coordinates)
print(f"Horizontal * Depth = {coordinates['horizontal'] * coordinates['depth']}")


## Part 2

# Reset our coordinates and add aim
coordinates = {'horizontal': 0, 'depth': 0, 'aim': 0}

# We can use or same decoder as before with the exception that
# it's more clear now to call 'aim' what was previously called 'depth', other than
# that this is exactly the same. This is for readability only.
instructions_decoder_2 = { 
                        'forward': {
                            'axis': 'horizontal',
                            'sign':  +1
                            }, 
                        'up': {
                            'axis':'aim',
                            'sign': -1
                            },
                        'down': {
                            'axis': 'aim',
                            'sign': +1
                            }
                        }


for direction, value in instructions:
   # Aim and Horizontal axis work exactly as before
   coordinates[instructions_decoder_2[direction]['axis']] += instructions_decoder_2[direction]['sign'] * value
   # The catch is that now we need to also potentially increase depth by value * aim if going forward
   if direction == 'forward':
       coordinates['depth'] += coordinates['aim'] * value

print(coordinates)
print(f"Horizontal * Depth = {coordinates['horizontal'] * coordinates['depth']}")
