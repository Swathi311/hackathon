import json
from pathlib import Path

file_path = Path("C:/21pw37/Input data/level0.json")
output_path = Path("C:/21pw37/level0_output.json")

with open(file_path, 'r') as json_file:
    data = json.load(json_file)

def calculate_tour_cost(tour, distances_list, neighborhoods):
    total_cost = 0
    for i in range(len(tour) - 1):
        start_index = neighborhoods.index(tour[i])
        end_index = neighborhoods.index(tour[i + 1])
        total_cost += distances_list[start_index][end_index]
    return total_cost

def two_opt(tour, distances_list, neighborhoods):
    improved = True
    while improved:
        improved = False
        for i in range(1, len(tour) - 2):
            for j in range(i + 1, len(tour)):
                if j - i == 1:
                    continue
                new_tour = tour[:i] + tour[i:j][::-1] + tour[j:]
                current_cost = calculate_tour_cost(tour, distances_list, neighborhoods)
                new_cost = calculate_tour_cost(new_tour, distances_list, neighborhoods)
                if new_cost < current_cost:
                    tour = new_tour
                    improved = True
    return tour

neighborhoods = list(data["neighbourhoods"].keys())
distances_list = [data["neighbourhoods"][n]["distances"] for n in neighborhoods]

def nearest_neighbor(neighbourhoods, distances_list):
    unvisited = set(neighbourhoods)
    current = neighbourhoods[0]
    unvisited.remove(current)
    tour = [current]
    while unvisited:
        next_neigh = min(unvisited, key=lambda city: distances_list[neighbourhoods.index(current)][neighbourhoods.index(city)])
        tour.append(next_neigh)
        unvisited.remove(next_neigh)
        current = next_neigh
    return tour


# Try multiple random starting points to find the most optimal tour
best_tour = None
min_cost = float('inf')

for start_point in neighborhoods:
    current_tour = nearest_neighbor(neighborhoods, distances_list)
    current_tour = two_opt(current_tour, distances_list, neighborhoods)
    current_cost = calculate_tour_cost(current_tour, distances_list, neighborhoods)

    if current_cost < min_cost:
        min_cost = current_cost
        best_tour = current_tour

# Get required data for generating outfile
vehicles_data = data.get("vehicles", {})
vehicle_key = list(vehicles_data.keys())[0] if vehicles_data else None
start_point = vehicles_data.get(vehicle_key, {}).get("start_point", None)

best_tour.insert(0, start_point)
best_tour.append(start_point)

output = {vehicle_key: {"path": best_tour}}

# Write to outfile
with open(output_path, 'w') as json_file:
    json.dump(output, json_file, indent=2)
