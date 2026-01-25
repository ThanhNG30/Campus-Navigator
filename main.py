"""
File: main.py
Name: Campus Navigator
Course: CSI480 (Artificial Intelligence)
Date: December 15, 2025

Problem Solved:
This project solves the problem of indoor navigation and find
the shortest path between two locations inside a building.

AI Technique Used:
A* (A-Star) search algorithm is used to compute the shortest
path between a start location and a destination. For this 
algorithm, the path cost combined with heuristic estimation to reduce
the search space. The heuristic is based on the Euclidean distance
between locations using their (x, y, z) coordinates.

Interesting Component:
The turn-by-turn navigation instruction system that helps determine
the change in direction (straight / left / right) relative to the 
direction that the user was facing, even with diagonal hallways.

Outcome and What Was Learned:
I learned how A* search can be applied to real-world navigation problems,
how heuristics affect search performance, and how geometric reasoning 
can be used to translate paths into user-friendly instructions.
"""

import math
import heapq
from campus_map import building_floors, graph

# Convert all keys in navigation graph
# and locations dictionary to lowercase
# for case-insensitive matching
graph = {
    k.lower(): {n.lower(): c for n, c in v.items()}
    for k, v in graph.items()
}

building_floors = {k.lower(): v for k, v in building_floors.items()}

def get_start_location(building):
    """
    Prompt the user for their starting location.

    :param building: Dictionary of building locations and their coordinates.
    """
    while True:
        curr_level = -1
        start_level = input(
            "Please type in your current level" \
            "\n(ex: Lower Level, Main, 2, 3, ...): ").lower().replace(" ", "")
        
        if "ll" in start_level or "lower" in start_level:
            curr_level = 0 
        elif "main" in start_level:
            curr_level = 1
        else: 
            curr_level = int(start_level)
            
        if curr_level not in range(5):   
            continue
        else: 
            print("Locations on level", curr_level, ":") 
            for location_name, coordinates in building.items():
                _, _, loc_z = coordinates
                if int(loc_z) == curr_level:
                    print("- ", location_name)
        
            start_location = input(
                "Please type in the area/room that is closest to you: ").lower().replace(" ", "")

            for location_name, coordinates in building.items():
                if start_location in location_name:
                    return  {"name": location_name, "coordinates": coordinates}
                
            print("This location is inaccessible.")



def get_destination(building):
    """
    Prompt the user for their destination.

    :param building: Dictionary of building locations and their coordinates.
    """
    while True:
        destination = (
            input(
                "Please enter the room number or area of your destination"
                "(ex: room 310, library, bookstore): "
            )
            .lower()
            .replace(" ", "")
        )

        for spot, coordinates in building.items():
            if destination in spot.replace(" ", ""):
                return {
                    "name": spot,
                    "coordinates": coordinates
                }

        print("This location is inaccessible.")


def heuristics(goal_node, building):
    """
    Return a dictionary of all locations and their 
    Euclidean distance heuristic in 3D (x, y, z).

    :param goal_node: End location's name and coordinates.
    :param building: Dictionary of building locations and their coordinates.
    """
    estimated_distances = {}

    end_x, end_y, end_z = goal_node["coordinates"]

    for spot, (x, y, z) in building.items():
        if spot == goal_node["name"]:
            estimated_distances[spot] = 0
        else:
            distance = math.sqrt(
                (x - end_x) ** 2 +
                (y - end_y) ** 2 +
                (z - end_z) ** 2
            )
            estimated_distances[spot] = distance

    return estimated_distances


def a_star_algorithm(start_node, goal_node, h_vals, graph_data):
    # Reference: https://youtu.be/F5reERwFiOI?si=9hb4dWgpnhmQjXC7
    """
    Implement a_star_algorithm to find the shortest path
    from start location to goal and return that path as a
    list of locations visited.
    
    :param start_node: Start location's name and coordinates.
    :param goal_node: End location's name and coordinates.
    :param h_vals: Dictionary of all location names and their heuristics.
    :param graph_data: Navigation graph. Cost = average travel time in seconds.
    """
    available_nodes = []
    checked_nodes = set()

    heapq.heappush(
        available_nodes,
        (h_vals[start_node["name"]], start_node["name"])
    )

    g_vals = {start_node["name"]: 0}
    came_from = {}

    while available_nodes:
        _, current_node = heapq.heappop(available_nodes)

        # print("Visiting:", current_node)  # debug

        if current_node == goal_node["name"]:
            path = []
            while current_node in came_from:
                path.append(current_node)
                current_node = came_from[current_node]
            path.append(start_node["name"])
            return path[::-1]

        if current_node in checked_nodes:
            continue

        checked_nodes.add(current_node)

        for neighbor, cost in graph_data.get(current_node, {}).items():
            if neighbor in checked_nodes:
                continue

            tentative_g = g_vals[current_node] + cost

            if neighbor not in g_vals or tentative_g < g_vals[neighbor]:
                g_vals[neighbor] = tentative_g
                f_val = tentative_g + h_vals[neighbor]
                came_from[neighbor] = current_node
                heapq.heappush(available_nodes, (f_val, neighbor))

    return None


def print_path(path, building):
    """
    Print instructions to walk user through their route.
    
    :param path: list of locations visited in the route.
    :param building: Dictionary of building locations and their coordinates.
    """
    print("\nNavigation Instructions:")

    prev_dir = None


    for i in range(len(path) - 1):
        curr_x, curr_y, curr_z = building[path[i]]
        next_x, next_y, next_z = building[path[i + 1]]

        dx = next_x - curr_x
        dy = next_y - curr_y
        dz = next_z - curr_z

        # Handle floor changes
        if dz != 0:
            if dz > 0:
                print(f"Go up {abs(dz)} floor(s) using {path[i]}")
            else:
                print(f"Go down {abs(dz)} floor(s) using {path[i]}")
            prev_dir = None
            continue

        # First movement on a new floor
        if prev_dir == None:
            print(f"Go straight from {path[i]} to {path[i + 1]}")
            prev_dir = (dx, dy)
            continue

        else:
            # Determine next turning left/right
            # Reference: https://stackoverflow.com/questions/27635188/algorithm-to-detect-left-or-right-turn-from-x-y-co-ordinates?utm_source=chatgpt.com
            next_dir = (dx, dy)
            dm = prev_dir[0] * next_dir[1] - prev_dir[1] * next_dir[0]
            if dm != 0.0:
                if dm > 0.0:
                    print(f"Turn left at {path[i]} to {path[i + 1]}")
                else:
                    print(f"Turn right at {path[i]} to {path[i + 1]}")
            else:
                print(f"Continue forward to {path[i + 1]}")
        
            prev_dir = next_dir
       

# Main Program
start = get_start_location(building_floors)
goal = get_destination(building_floors)

print("\nFrom:", start["name"])
print("To:", goal["name"])

h_vals = heuristics(goal, building_floors)

path = a_star_algorithm(start, goal, h_vals, graph)

if path:
    print_path(path, building_floors)
else:
    print("No path found.")