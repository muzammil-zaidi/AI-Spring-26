from queue import PriorityQueue

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f

def heuristic(current_pos, goal_pos):
    return abs(current_pos[0] - goal_pos[0]) + abs(current_pos[1] - goal_pos[1])

def best_first_search(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    start_node = Node(start)
    frontier = PriorityQueue()
    frontier.put(start_node)
    visited = set()

    while not frontier.empty():
        current_node = frontier.get()
        current_pos = current_node.position

        if current_pos == goal:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]

        visited.add(current_pos)

        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            new_pos = (current_pos[0] + dx, current_pos[1] + dy)

            if (0 <= new_pos[0] < rows and
                0 <= new_pos[1] < cols and
                maze[new_pos[0]][new_pos[1]] == 0 and
                new_pos not in visited):

                new_node = Node(new_pos, current_node)
                new_node.h = heuristic(new_pos, goal)
                new_node.f = new_node.h   # Best-First: f(n)=h(n)
                frontier.put(new_node)
                visited.add(new_pos)

    return None

def multi_goal_best_first(maze, start, goals):
    current_start = start
    remaining_goals = goals.copy()
    final_path = []

    while remaining_goals:

        nearest_goal = min(remaining_goals,
                           key=lambda g: heuristic(current_start, g))

        path = best_first_search(maze, current_start, nearest_goal)

        if path is None:
            return None

        final_path += path[:-1]
        current_start = nearest_goal
        remaining_goals.remove(nearest_goal)

    final_path.append(current_start)
    return final_path

maze = [
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 1],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0]
]

start = (0, 0)
goals = [(4, 4), (2, 3), (4, 0)]

path = multi_goal_best_first(maze, start, goals)

if path:
    print("Path covering all goals:")
    print(path)
else:
    print("No path found")
