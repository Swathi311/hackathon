#level 0 - travelling salesman algorithm

import json

file_path = "C:\\21pw37\\Input data\\level0.json"

with open(file_path, 'r') as json_file:
    data = json.load(json_file)

#TSP algorithm implementation
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

neighborhoods = list(data["neighbourhoods"].keys())
distances_list = []

for n in neighborhoods:
    distances_list.append(data["neighbourhoods"][n]["distances"])

res = nearest_neighbor(neighborhoods, distances_list)

#get required data for generating outfile
vehicles_data = data.get("vehicles", {})
vehicle_key = list(vehicles_data.keys())[0] if vehicles_data else None
vehicle = vehicles_data.get(vehicle_key, {})
start_point = vehicle.get("start_point", None)

res.insert(0, start_point)
res.append(start_point)

output = {vehicle_key: {"path": res}}

#write to outfile
with open('C:\\21pw37\\outfile.json', 'w') as json_file:
    json.dump(output, json_file, indent=2)