from collections import defaultdict
## General
# Read and format the data in a convenient way
with open('input_data.txt', 'r') as f:
    lines = [(start, finish) for start, finish in [line.strip().split('-') for line in f.readlines()]]

# Make a map between Nodes and destination nodes
nodes = defaultdict(set)

# Add bidirectional paths
for start, finish in lines:
    nodes[start].add(finish)
    nodes[finish].add(start)


## Part 1

# Our traversal Depth First Search function
def dfs(node, current_path, visited, paths_to_end):
    # If we are at the end, then this is a possible path to the end.
    # This branch of exploration is done, and we found a path
    if node == 'end':
        paths_to_end.append(current_path)
    else:
        # Otherwise this is a valid visit, we log it
        current_path = current_path[:] + [node]
        # We'll visit any cave except lowercase ones that have already been visited
        next_nodes = [next_node for next_node in nodes[node] if next_node.isupper() or next_node not in visited]
        for next_node in next_nodes:
            # Each time we call dfs again here we're opening a new branch of exploration of the tree
            # in that branch we want to mark this node as visited if it can't be visited again.
            if next_node.islower():
                visited.add(next_node)
            dfs(next_node, current_path, visited, paths_to_end)
            # But in the next branch we're taking it off beacause we'll visit an alternative one
            # so we want this one to remain visitable there
            if next_node.islower():
                 visited.remove(next_node)


paths_to_end = []
visited = set()
visited.add('start')
current_path = []

dfs('start', current_path, visited, paths_to_end)

print(f"There are {len(paths_to_end)} paths from start to end.")


## Part 2

# Very much the same but now we track with a boolean if we can revisit a small cave (lowercase)

# Our traversal Depth First Search function
def dfs2(node, current_path, visited, paths_to_end):
    # If we are at the end, then this is a possible path to the end.
    # This branch of exploration is done, and we found a path
    if node == 'end':
        paths_to_end.append(current_path)
    else:
        # Otherwise this is a valid visit, we log it
        current_path = current_path[:] + [node]
        # We determine if we have already spent our extra visit to a lowercase node
        can_revisit = all(visit < 2 for visit in visited.values())
        # We'll visit any cave except lowercase ones that have already been visited unless we can revisit them still
        next_nodes = [next_node for next_node in nodes[node] if (next_node.isupper() or visited[next_node] < 1 or can_revisit) and next_node != 'start']
        for next_node in next_nodes:
            # Each time we call dfs again here we're opening a new branch of exploration of the tree
            # in that branch we want to mark this node as visited one more time
            if next_node.islower():
                visited[next_node] += 1
            dfs2(next_node, current_path, visited, paths_to_end)
            # But in the next branch we're taking it off beacause we'll visit an alternative one
            # so we want to subtract the visit we added before our recursive call
            if next_node.islower():
                visited[next_node] -= 1


paths_to_end = []
visited = defaultdict(int)
visited['start'] += 1
current_path = []

dfs2('start', current_path, visited, paths_to_end)

print(f"There are {len(paths_to_end)} paths from start to end.")