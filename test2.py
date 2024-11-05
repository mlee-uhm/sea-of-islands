import heapq

def make_graph():
    # Dictionary with keys that are the island that we are leaving from and tuples that contain the island we are traveling to and the time needed.
    # tuple = (cost, to_node)
    return {
        'islandA': [(4, 'islandB'), (2, 'islandC')],
        'islandB': [(3, 'islandC'), (3, 'islandE'), (2, 'islandD')],
        'islandC': [(1, 'islandB'), (4, 'islandD'), (5, 'islandE')],
        'islandD': [],
        'islandE': [(1, 'islandD')],
    }

class Island:
    def __init__(self, name):
        self.name = name
        self.experiences = []  # List of experiences available on the island

class SeaOfIslands:
    def __init__(self, graph):
        self.islands = {}
        for island_name in graph:
            self.islands[island_name] = Island(island_name)

        # Build the connections from the graph
        self.graph = graph

    def add_experiences(self, island_name, experiences):
        if island_name in self.islands:
            self.islands[island_name].experiences = experiences

def dijkstra(start_island, sea_of_islands):
    queue = []
    heapq.heappush(queue, (0, start_island))  # (travel_time, island)
    distances = {island: float('inf') for island in sea_of_islands.graph}
    distances[start_island] = 0
    visited = set()

    while queue:
        current_time, current_island = heapq.heappop(queue)

        if current_island in visited:
            continue
        visited.add(current_island)

        for travel_time, neighbor in sea_of_islands.graph[current_island]:
            new_time = current_time + travel_time
            if new_time < distances[neighbor]:
                distances[neighbor] = new_time
                heapq.heappush(queue, (new_time, neighbor))

    return distances

def maximize_experiences(start_island, sea_of_islands):
    visited = set()
    experiences = []
    total_time_spent = 0

    while True:
        distances = dijkstra(start_island, sea_of_islands)
        # Choose the next island based on the shortest travel time
        next_island = min((island for island in distances if island not in visited), key=distances.get, default=None)

        if next_island is None or distances[next_island] == float('inf'):
            break

        # Add experiences from the next island
        if sea_of_islands.islands[next_island].experiences:
            for experience, time in sea_of_islands.islands[next_island].experiences:
                experiences.append(experience)
                total_time_spent += time

        visited.add(next_island)
        total_time_spent += distances[next_island]
        start_island = next_island  # Move to the next island

    return experiences, total_time_spent

# Test case
if __name__ == "__main__":
    # Create the sea of islands using the graph
    graph = make_graph()
    sea = SeaOfIslands(graph)
    # Add experiences with their respective times to the islands
    sea.add_experiences('islandA', experiences=[("Snorkeling", 2), ("Hiking", 3)])
    sea.add_experiences('islandB', experiences=[("Fishing", 1), ("Surfing", 2)])
    sea.add_experiences('islandC', experiences=[("Diving", 4), ("Camping", 2)])
    sea.add_experiences('islandD', experiences=[("Caving", 3)])
    sea.add_experiences('islandE', experiences=[("Bird Watching", 1)])

    # Maximize experiences starting from islandA
    experiences, total_time_spent = maximize_experiences('islandA', sea)

    print("Experiences enjoyed in order:", experiences)
    print("Total time spent (travel + experiences):", total_time_spent)
