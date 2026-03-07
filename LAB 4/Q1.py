import heapq

# 1) DLS

class DLS_GoalAgent:
    def __init__(self, graph, goal, depth_limit):
        self.graph = graph
        self.goal = goal
        self.depth_limit = depth_limit

    def dls(self, node, depth, path):
        print(f"Visiting: {node}, Depth: {depth}")

        if node == self.goal:
            return path

        if depth == self.depth_limit:
            return None

        for child in self.graph.get(node, []):
            result = self.dls(child, depth + 1, path + [child])
            if result is not None:
                return result

        return None

    def act(self, start):
        print("\n===== DLS Goal-Based Agent =====")
        result = self.dls(start, 0, [start])

        if result:
            print("Goal Found!")
            print("Path:", " -> ".join(result))
        else:
            print("Goal Not Found within Depth Limit.")

# 2) UCS

class UCS_UtilityAgent:
    def __init__(self, graph, goal):
        self.graph = graph
        self.goal = goal

    def ucs(self, start):
        priority_queue = []
        heapq.heappush(priority_queue, (0, start, [start]))

        visited = {}

        while priority_queue:
            cost, node, path = heapq.heappop(priority_queue)

            print(f"Expanding: {node}, Cost: {cost}")

            if node == self.goal:
                return cost, path

            if node not in visited or cost < visited[node]:
                visited[node] = cost

                for neighbor, weight in self.graph.get(node, []):
                    heapq.heappush(
                        priority_queue,
                        (cost + weight, neighbor, path + [neighbor])
                    )

        return None, None

    def act(self, start):
        print("\n===== UCS Utility-Based Agent =====")
        cost, path = self.ucs(start)

        if path:
            print("Goal Found!")
            print("Total Cost:", cost)
            print("Path:", " -> ".join(path))
        else:
            print("Goal Not Found.")

graph_dls = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['G'],
    'F': [],
    'G': []
}

graph_ucs = {
    'A': [('B', 1), ('C', 4)],
    'B': [('D', 2), ('E', 5)],
    'C': [('F', 1)],
    'D': [],
    'E': [('G', 1)],
    'F': [],
    'G': []
}


if __name__ == "__main__":

    dls_agent = DLS_GoalAgent(graph_dls, goal='G', depth_limit=3)
    dls_agent.act(start='A')

    ucs_agent = UCS_UtilityAgent(graph_ucs, goal='G')
    ucs_agent.act(start='A')
