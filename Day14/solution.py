from collections import defaultdict
## General
# Read and format the data in a convenient way
with open('input_data.txt', 'r') as f:
    polymer_template = f.readline().strip()
    _, insertion_rules = f.readline(), {k: v for k, v in [line.strip().split(' -> ') for line in f.readlines()] }

## Part 1
p1_polymer = polymer_template

for step in range(7):
    # We zip the list with itself to make the pairs
    pairs = zip(p1_polymer, p1_polymer[1:])
    # We process the template for the next step by adding the insertion rules between each pair (and the last element which stays at the end)
    p1_polymer = "".join(["".join([p1, insertion_rules[p1 + p2]]) for p1, p2 in pairs] + [p1_polymer[-1]])

# Now we need to count elements to find least and most common, we can use a defaultdict to do this

elements = defaultdict(int)
for element in p1_polymer:
    elements[element] += 1
print(elements)
most_common = max(elements.values())
least_common = min(elements.values())

print(f"The difference between most and least common elements is {most_common - least_common}")

## Part 2
p2_polymer = polymer_template

# The above strategy won't scale to 40 steps.
# We can just track pairs and process insertion from the pairs
# themselves to avoid needing to construct a HUGE string in memory
# since we don't actually care about order, just appeareances
pairs = defaultdict(int)

# This initializes our data structure
for pair in ["".join(t) for t in zip(p2_polymer, p2_polymer[1:])]:
        pairs[pair] += 1

for step in range(40):
    # For each pair, we compute the insertion and increase our pairs count
    # We need to keep track of insertions without modifiying the original at first
    new_pairs = defaultdict(int)
    for pair in pairs.keys():
        # For each pair we create two new ones from the first element and the insertion rule
        new_pair_1 = pair[0] + insertion_rules[pair]
        new_pair_2 = insertion_rules[pair] + pair[1]
        # The new pair will appear as much times as the current pair that produces it already appears
        # plus it's already calculated presence in this step (if any)
        new_pairs[new_pair_1] += pairs[pair]
        new_pairs[new_pair_2] += pairs[pair]

    pairs = new_pairs

# Now we need to count elements to find least and most common, we can use a defaultdict to do this
elements = defaultdict(int)
for pair, amount in pairs.items():
    elements[pair[0]] += amount
    elements[pair[1]] += amount 

# Due to one element belonging always to two pairs (except the first and last), we have duplicated the actual amount.
elements = {k: v // 2 for k, v in elements.items()}
# Since in our case the first and last letter is the same element, we add 1 (we have already divided by 2)
elements[polymer_template[0]] += 1

most_common = max(elements.values())
least_common = min(elements.values())

print(f"The difference between most and least common elements is {most_common - least_common}")