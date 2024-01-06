import json

file_path = "C:\\21pw37\\Input data\\level0.json"

with open(file_path, 'r') as json_file:
    data = json.load(json_file)


def nearest_neighbor_with_capacity(data, capacity):
    neighborhoods = data["neighbourhoods"]
    depot = "n0"  # Assuming the starting point is n0

    unvisited = set(neighborhoods.keys())
    unvisited.remove(depot)
    routes = []

    while unvisited:
        current = depot
        route = [current]
        remaining_capacity = capacity

        while remaining_capacity > 0:
            next_neigh = find_nearest_neighbor(current, unvisited, neighborhoods)
            if next_neigh is None:
                break

            order_quantity_str = neighborhoods[next_neigh]["order_quantity"]
            if order_quantity_str.lower() == 'inf':
                order_quantity = float('inf')  # or any other suitable representation for infinity
            else:
                order_quantity = int(order_quantity_str)


            if order_quantity <= remaining_capacity:
                route.append(next_neigh)
                remaining_capacity -= order_quantity
                unvisited.remove(next_neigh)
            else:
                break

        route.append(depot)  # Return to the starting point
        routes.append(route)

    return routes

def find_nearest_neighbor(current, unvisited, neighborhoods):
    distances = neighborhoods[current]["distances"]
    nearest_neighbor = min(unvisited, key=lambda neigh: distances[list(neighborhoods.keys()).index(neigh)])
    return nearest_neighbor


vehicle_capacity = 600

result_routes = nearest_neighbor_with_capacity(data, vehicle_capacity)

print("Number of trips:", len(result_routes))
