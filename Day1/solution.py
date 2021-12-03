## General
# Read and properly cast the data
with open('input_data.txt', 'r') as f:
    depths = [int(depth.strip()) for depth in f.readlines()]


## Part 1

# Zip each depth value with the next (current) one
# Sum 1 for each pair of measurements in which depth increases, 0 otherwise.
increases = sum(1 if previous < current else 0 for previous, current in zip(depths, depths[1:]))
print(f'Part 1: There are {increases} increases')

#############################################

## Part 2

# Produce a new list from the original making triplets of data where new[n] = [original[n], original[n + 1], original[n + 2]]
sliding_window_3_depths = [triplet for triplet in zip(depths, depths[1:], depths[2:])]
# Compute the increases using the exact same method as Part 1 but using the sums of the triplets as values to compare
sliding_window_3_increases = sum(1 if sum(previous) < sum(current) else 0 for previous, current in zip(sliding_window_3_depths, sliding_window_3_depths[1:]))

print(f'Part 2: There are {sliding_window_3_increases} sliding window of 3 increases')