import itertools

distance = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]

n = len(distance)

def tsp_bruteforce():
    cities = list(range(n))
    
    min_path = None
    min_cost = float('inf')

    for perm in itertools.permutations(cities[1:]):
        current_cost = 0
        k = 0

        path = [k]

        for city in perm:
            current_cost += distance[k][city]
            k = city
            path.append(k)

        current_cost += distance[k][0]
        path.append(0)

        if current_cost < min_cost:
            min_cost = current_cost
            min_path = path

    return min_path, min_cost

if __name__ == "__main__":
    best_path, best_cost = tsp_bruteforce()

    print("===== Traveling Salesman Problem =====")
    print("Shortest Path:", " -> ".join(str(city + 1) for city in best_path))
    print("Minimum Cost:", best_cost)
