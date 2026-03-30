from queue import PriorityQueue

def heuristic(current, target):
    return abs(current[0] - target[0]) + abs(current[1] - target[1])


def greedy_delivery_route(start, deliveries):

    current_position = start
    current_time = 0
    route = []
    remaining = deliveries.copy()

    while remaining:

        pq = PriorityQueue()

        for point in remaining:
            location = point["location"]
            start_time = point["start"]
            end_time = point["end"]

            travel_time = heuristic(current_position, location)
            arrival_time = current_time + travel_time

            if arrival_time <= end_time:

                priority = (end_time, travel_time)

                pq.put((priority, point))

        if pq.empty():
            print(" No feasible delivery (time window missed)")
            return None

        _, selected = pq.get()

        travel_time = heuristic(current_position, selected["location"])
        current_time += travel_time

        if current_time < selected["start"]:
            current_time = selected["start"]

        print(f"Delivered at {selected['location']} at time {current_time}")

        route.append(selected["location"])
        current_position = selected["location"]
        remaining.remove(selected)

    print("\n Final Optimized Route:", route)
    print("Total Time:", current_time)
    return route

deliveries = [
    {"location": (2, 3), "start": 2, "end": 10},
    {"location": (5, 1), "start": 0, "end": 8},
    {"location": (6, 4), "start": 5, "end": 15},
    {"location": (1, 6), "start": 3, "end": 7}
]

start = (0, 0)

print("Greedy Best-First Delivery Optimization:\n")
greedy_delivery_route(start, deliveries)
