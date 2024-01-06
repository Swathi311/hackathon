import json

file_path = "C:\\21pw37\\Input data\\level1a.json"

with open(file_path, 'r') as json_file:
    data = json.load(json_file)


def nearest_neighbor_with_capacity(neighbourhoods, distances_list, capacities, vehicle_capacity):
    unvisited = set(neighbourhoods)
    current = neighbourhoods[0]
    unvisited.remove(current)
    tour = [current]
    current_capacity = 0
    num_routes = 1

    while unvisited:
        next_neigh = min(
            unvisited,
            key=lambda city: distances_list[neighbourhoods.index(current)][neighbourhoods.index(city)]
        )
        
        # Check if adding the next neighborhood exceeds the vehicle capacity
        next_neigh_capacity = capacities[neighbourhoods.index(next_neigh)]
        if current_capacity + next_neigh_capacity <= vehicle_capacity:
            tour.append(next_neigh)
            unvisited.remove(next_neigh)
            current_capacity += next_neigh_capacity
        else:
            # Start a new route if adding the next neighborhood exceeds capacity
            tour.append(neighbourhoods[0])  # Return to the starting point
            tour.append(next_neigh)
            unvisited.remove(next_neigh)
            current_capacity = next_neigh_capacity
            num_routes += 1

        current = next_neigh

    return tour, num_routes

neighborhoods = list(data["neighbourhoods"].keys())
distances_list = []
order_quantities = []

for n in neighborhoods:
    distances_list.append(data["neighbourhoods"][n]["distances"])
    order_quantities.append(data["neighbourhoods"][n]["order_quantity"])

vehicles_data = data.get("vehicles", {})
vehicle_key = list(vehicles_data.keys())[0] if vehicles_data else None
vehicle = vehicles_data.get(vehicle_key, {})
vehicle_capacity = vehicle.get("capacity", None)

tour, num_routes = nearest_neighbor_with_capacity(neighborhoods, distances_list, order_quantities, vehicle_capacity)
print("Optimized Tour:", tour)
print("Number of Routes:", num_routes)
