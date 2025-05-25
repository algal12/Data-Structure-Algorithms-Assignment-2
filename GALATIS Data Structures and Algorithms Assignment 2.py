import pandas
import networkx
import random
import re

# Constants for travel timing
transfer_time = 5       # Time (in minutes) to transfer between lines
min_travel_time = 2     # Minimum travel time between stations on same line
max_travel_time = 8     # Maximum travel time between stations on same line

# Load stations from CSV file
def load_stations(csv_path='MRT_Stations.csv'):
    data = pandas.read_csv(csv_path)
    stations = {}

    for _, row in data.iterrows():
        try:
            station = row['STN_NAME'].strip().title()
            stn_no = row['STN_NO'].strip().upper()
        except KeyError:
            print("Error: Ensure CSV has 'STN_NAME' and 'STN_NO' columns.")
            return {}

        match = re.match(r'([A-Z]+)(\d+)', stn_no)
        if not match:
            continue

        line = match.group(1)
        number = int(match.group(2))

        key = (station, line)

        stations[key] = {
            'name': station,
            'line': line,
            'number': number,
            'lat': row['Latitude'],
            'lon': row['Longitude']
        }

    return stations

# Build a graph of MRT stations
def build_graph(stations):
    graph = networkx.Graph()

    for key, data in stations.items():
        graph.add_node(key, **data)

    lines = {}
    for key, data in stations.items():
        lines.setdefault(data['line'], []).append((key, data['number']))

    for line, nodes in lines.items():
        sorted_nodes = sorted(nodes, key=lambda x: x[1])
        for i in range(len(sorted_nodes) - 1):
            a, b = sorted_nodes[i][0], sorted_nodes[i + 1][0]
            travel_time = random.randint(min_travel_time, max_travel_time)
            graph.add_edge(a, b, weight=travel_time, type='travel')

    station_groups = {}
    for key in stations:
        station = key[0]
        station_groups.setdefault(station, []).append(key)

    for station, keys in station_groups.items():
        if len(keys) > 1:
            for i in range(len(keys)):
                for j in range(i + 1, len(keys)):
                    a = keys[i]
                    b = keys[j]
                    graph.add_edge(a, b, weight=transfer_time, type='transfer')

    return graph

# Match user input to nodes
def get_matching_nodes(graph, user_input):
    normalized = user_input.strip().lower()
    return [n for n in graph.nodes if normalized == n[0].lower()]

# Suggest similar station names
def suggest_station_names(graph, input_name):
    print("Did you mean:")
    station_names = sorted(set(n[0] for n in graph.nodes))
    for name in station_names:
        if input_name.lower() in name.lower():
            print(" - {}".format(name))

# Find shortest path (fewest stops)
def find_shortest_path(graph, first_station, last_station):
    first_nodes = get_matching_nodes(graph, first_station)
    last_nodes = get_matching_nodes(graph, last_station)

    if not first_nodes or not last_nodes:
        print("Station not found.\n")
        suggest_station_names(graph, first_station)
        suggest_station_names(graph, last_station)
        return

    shortest = None
    for first in first_nodes:
        for last in last_nodes:
            try:
                path = networkx.shortest_path(graph, source=first, target=last)
                if not shortest or len(path) < len(shortest):
                    shortest = path
            except networkx.NetworkXNoPath:
                continue

    if shortest:
        print("\nShortest path (by number of stops):")
        for node in shortest:
            print("- {} ({})".format(node[0], node[1]))
        print("")
    else:
        print("No path found.\n")

# Find fastest path (based on travel time)
def find_fastest_route(graph, first_station, last_station):
    first_nodes = get_matching_nodes(graph, first_station)
    last_nodes = get_matching_nodes(graph, last_station)

    if not first_nodes or not last_nodes:
        print("Station not found.\n")
        suggest_station_names(graph, first_station)
        suggest_station_names(graph, last_station)
        return

    fastest = None
    min_time = float('inf')

    for first in first_nodes:
        for last in last_nodes:
            try:
                path = networkx.dijkstra_path(graph, source=first, target=last, weight='weight')
                total_time = sum(graph[u][v]['weight'] for u, v in zip(path[:-1], path[1:]))
                if total_time < min_time:
                    min_time = total_time
                    fastest = path
            except networkx.NetworkXNoPath:
                continue

    if fastest:
        print("\nFastest path (total travel time: {} minutes):".format(min_time))
        for node in fastest:
            print("- {} ({})".format(node[0], node[1]))
        print("")
    else:
        print("No path found.\n")

# Main menu for user interaction
def mrt_mtr():
    stations = load_stations("MRT_Stations.csv")
    if not stations:
        return

    graph = build_graph(stations)

    while True:
        print("=== Singapore MRT Route Finder ===\n")
        print("1. Find route")
        print("2. Exit\n")
        choice = input("Choose an option (1 or 2): ").strip()

        if choice == '2':
            print("Goodbye!\n")
            break
        elif choice == '1':
            first = input("\nEnter first station name: ").strip().title()
            last = input("Enter last station name: ").strip().title()

            print("")
            find_shortest_path(graph, first, last)
            find_fastest_route(graph, first, last)
        else:
            print("Invalid option. Please choose 1 or 2.\n")

# Run the program
if __name__ == "__main__":
    mrt_mtr()

