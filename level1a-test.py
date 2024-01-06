import json

file_path = "C:\\21pw37\\Input data\\level1a.json"

with open(file_path, 'r') as json_file:
    data = json.load(json_file)


def nearest_neighbor_with_capacity(neighbourhoods, distances_list, capacities, vehicle_capacity, rest_dist):
    unvisited = set(neighbourhoods)
    current = neighbourhoods[0]
    unvisited.remove(current)
    tour = ["r0", current]
    current_capacity = capacities[neighbourhoods.index(current)]
    num_routes = 0
    routes = {}
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
            num_routes += 1
            tour.append("r0")
            routes[f"path{num_routes}"] = tour
            tour = ["r0"]
            tour.append(next_neigh)
            unvisited.remove(next_neigh)
            current_capacity = next_neigh_capacity
           
        current = next_neigh

    # Add the last route
    tour.append("r0")
    routes[f"path{num_routes}"] = tour

    return routes


neighborhoods = list(data["neighbourhoods"].keys())
distances_list = []
order_quantities = []

for n in neighborhoods:
    distances_list.append(data["neighbourhoods"][n]["distances"])
    order_quantities.append(data["neighbourhoods"][n]["order_quantity"])

rest_dist = data["restaurants"]["r0"]["neighbourhood_distance"]

vehicles_data = data.get("vehicles", {})
vehicle_key = list(vehicles_data.keys())[0] if vehicles_data else None
vehicle = vehicles_data.get(vehicle_key, {})
vehicle_capacity = vehicle.get("capacity", None)

routes = nearest_neighbor_with_capacity(neighborhoods, distances_list, order_quantities, vehicle_capacity, rest_dist)
output = {vehicle_key: routes}

print(json.dumps(output, indent=2))

output_file_path = "C:/21pw37/level1a_output.json"
with open(output_file_path, 'w') as output_file:
    json.dump(output, output_file, indent=2)
