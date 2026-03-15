# 1) FOR TREE

class IDDFS_Tree:
    def __init__(self, tree):
        self.tree = tree

    def dls(self, node, goal, depth):
        print(f"Visiting: {node}, Depth: {depth}")

        if node == goal:
            return True

        if depth <= 0:
            return False

        for child in self.tree.get(node, []):
            if self.dls(child, goal, depth - 1):
                return True

        return False

    def iddfs(self, start, goal, max_depth):
        print("\n===== IDDFS on TREE =====")
        for depth in range(max_depth + 1):
            print(f"\nDepth Limit: {depth}")
            if self.dls(start, goal, depth):
                print(f"\nGoal {goal} found at depth {depth}")
                return True

        print("\nGoal not found within depth limit.")
        return False


# 2) FOR GRAPH

class IDDFS_Graph:
    def __init__(self, graph):
        self.graph = graph

    def dls(self, node, goal, depth, visited):
        print(f"Visiting: {node}, Depth: {depth}")

        if node == goal:
            return True

        if depth <= 0:
            return False

        visited.add(node)

        for neighbor in self.graph.get(node, []):
            if neighbor not in visited:
                if self.dls(neighbor, goal, depth - 1, visited):
                    return True

        visited.remove(node)
        return False

    def iddfs(self, start, goal, max_depth):
        print("\n===== IDDFS on GRAPH =====")
        for depth in range(max_depth + 1):
            print(f"\nDepth Limit: {depth}")
            visited = set()
            if self.dls(start, goal, depth, visited):
                print(f"\nGoal {goal} found at depth {depth}")
                return True

        print("\nGoal not found within depth limit.")
        return False

tree = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': [],
    'E': [],
    'F': [],
    'G': []
}

graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': ['A'], 
    'E': ['F'],
    'F': []
}

if __name__ == "__main__":

    tree_search = IDDFS_Tree(tree)
    tree_search.iddfs(start='A', goal='G', max_depth=3)

    graph_search = IDDFS_Graph(graph)
    graph_search.iddfs(start='A', goal='F', max_depth=3)
