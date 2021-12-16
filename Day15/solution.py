
import heapq
from collections import defaultdict
## General
# Read and format the data in a convenient way
with open('input_data.txt', 'r') as f:
    # We'll use a dictionary of points to track our grid (and we'll call it a graph)
    graph = {(x, y): int(v) for y, line in enumerate(f.readlines()) for x, v in enumerate(line.strip())}

# Constants
X = 0
Y = 1

## Part 1

# Calculate the limits of our grid
x_limit, y_limit = max(p[X] for p in graph.keys()), max(p[Y] for p in graph.keys())

# This is a Shortest Path problem so we can leverage Dijkstra's Algorithm to find it
# More info @ https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm

def dijkstra(graph, start, end):
    visited = set()

    pq = [] # Start an empty Priority Queue for our unvisited nodes

    # Here we'll keep the distance to the start node, 
    # unknown distances are marked as infinity
    distances = defaultdict(lambda: float('inf')) 
    
    # We only know that the start is at 0 distance from itself
    distances[start] = 0
    heapq.heappush(pq, (distances[start], start))
        
  
    # We'll iterate until discovering the end which will yield the shortest path
    while end not in visited:
        current_distance, current_node = heapq.heappop(pq)
        visited.add(current_node)
        offsets = ((1,0), (-1,0), (0,1), (0,-1))
        # Calculate tentative neighbors
        neighbor_nodes = tuple(tuple(map(sum, zip(current_node, offset))) for offset in offsets)
        # Filter down to those in the graph
        neighbor_nodes = tuple(neighbor for neighbor in neighbor_nodes 
        if neighbor not in visited and 0 <= neighbor[X] <= end[X] and 0 <= neighbor[Y] <= end[Y])
        # The distance from this node to a neighbor is the current distance plus the risk level
        # So we update all our distances discovered so far
        for neighbor in neighbor_nodes:
            new_distance = distances[current_node] + graph[neighbor]
            if(new_distance < distances[neighbor]):
                distances[neighbor] = new_distance
                heapq.heappush(pq, (new_distance, neighbor))


    return distances[end]
        

print(f"The shortest path is {dijkstra(graph, (0,0), (x_limit,y_limit))}")

## Part 2

# We now need to compute a new graph from the original
extended_graph = graph.copy()


# First extend our graph horizontally
for x_patch_offset in range(1, 5):
    for x, y in graph.keys():
        prev_patch_value = extended_graph[(x + (x_patch_offset - 1) * (x_limit + 1), y)]
        extended_graph[(x + x_patch_offset * (x_limit + 1), y)] = prev_patch_value + 1 if prev_patch_value < 9 else 1


row = extended_graph.copy()

# Now Extend our row vertically
for y_patch_offset in range(1, 5):
    for x, y in row.keys():
        prev_patch_value = extended_graph[(x, y + (y_patch_offset - 1) * (y_limit + 1))]
        extended_graph[(x, y + y_patch_offset * (y_limit + 1))] = prev_patch_value + 1 if prev_patch_value < 9 else 1



# Calculate the limits of our grid
x_limit, y_limit = max(p[X] for p in extended_graph.keys()), max(p[Y] for p in extended_graph.keys())

# Now we apply dijkstra again
print(f"The shortest path is {dijkstra(extended_graph, (0,0), (x_limit,y_limit))}")
