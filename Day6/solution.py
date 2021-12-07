from collections import defaultdict
## General
# Read and format the data in a convenient way
with open('input_data.txt', 'r') as f:
    original = [int(fish) for fish in f.readline().split(",")]


## Part 1 (Naive implementation)
# This will work for a small amount of days, however since this grows exponentially
# if the number of days is too large we'll eventually have a MemoryError because we
# are tracking each fish individually when there's no need
all_fish = original.copy()
for day in range(80):
    # Make a list of the new fish to add
    new_fish = len([fish for fish in all_fish if fish == 0]) * [8]
    # Decrement all current fish
    all_fish = [fish - 1 if fish > 0 else 6 for fish in all_fish]
    # Append the list of new fish
    all_fish += new_fish

print(len(all_fish))


## Part 2
# The algorithm above won't do for this. We need to track the fish differently
# to be more memory efficient and fast. We'll use a default dict to initialize
# the fish counts if missing
fish_dict = defaultdict(int)

for fish in original:
    fish_dict[fish] += 1

# Now we can work with regular dicts as we'll compute new dicts from the original
for _ in range(256):
    # This is the amount of new fish that we need to spawn
    new_fish = fish_dict[0] if 0 in fish_dict else 0
    # Each day all fish move down a key (except the fishes in day 0)
    fish_dict = defaultdict(int, {k - 1: v for k, v in fish_dict.items() if k > 0})
    # If we have fishes at day 0, we add them to those at day 6
    # and also Spawn or new fishes at key 8
    if new_fish > 0:
        fish_dict[6] += new_fish
        fish_dict[8] = new_fish

print(sum(v for v in fish_dict.values()))