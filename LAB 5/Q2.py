import random

graph = {
    'A': {'B': 4, 'C': 3},
    'B': {'D': 5, 'E': 12},
    'C': {'F': 7},
    'D': {'G': 4},
    'E': {'G': 3},
    'F': {'G': 8},
    'G': {}
}

heuristic = {
    'A': 10,
    'B': 8,
    'C': 5,
    'D': 4,
    'E': 3,
    'F': 6,
    'G': 0
}

def dynamic_cost_update(graph):
    """
    Randomly modify one edge cost to simulate dynamic environment
    """
    node = random.choice(list(graph.keys()))
    if graph[node]:
        neighbor = random.choice(list(graph[node].keys()))
        new_cost = random.randint(1, 15)
        graph[node][neighbor] = new_cost
        print(f"\n Edge cost changed: {node} -> {neighbor} = {new_cost}")


def dynamic_a_star(graph, start, goal):

    open_list = [(start, heuristic[start])]
    closed_list = set()
    g_cost = {start: 0}
    came_from = {start: None}

    while open_list:

        # Sort OPEN by lowest f(n)
        open_list.sort(key=lambda x: x[1])
        current, current_f = open_list.pop(0)

        if current in closed_list:
            continue

        print("Visiting:", current)
        closed_list.add(current)

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            path.reverse()
            print("\n Optimal Path Found:", path)
            return path

        if random.random() < 0.3:
            dynamic_cost_update(graph)

        for neighbor, cost in graph[current].items():

            new_g = g_cost[current] + cost
            new_f = new_g + heuristic[neighbor]

            if neighbor not in g_cost or new_g < g_cost[neighbor]:
                g_cost[neighbor] = new_g
                came_from[neighbor] = current
                open_list.append((neighbor, new_f))

    print(" Goal not reachable")
    return None

print("Dynamic A* Search Running...\n")
dynamic_a_star(graph, 'A', 'G')
