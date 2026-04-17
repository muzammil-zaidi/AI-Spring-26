colors = ["Red", "Green", "Blue"]

graph = {
    'A': ['B', 'E'],
    'B': ['A', 'C', 'D'],
    'C': ['B', 'D'],
    'D': ['B', 'C', 'E'],
    'E': ['A', 'D']
}

def is_valid(node, color, assignment):
    for neighbor in graph[node]:
        if neighbor in assignment and assignment[neighbor] == color:
            return False
    return True

def backtrack(assignment):
    if len(assignment) == len(graph):
        print(assignment)
        return

    node = list(graph.keys())[len(assignment)]

    for color in colors:
        if is_valid(node, color, assignment):
            assignment[node] = color
            backtrack(assignment)
            del assignment[node]

backtrack({})
