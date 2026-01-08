"""
File: main.py
Name: Campus Navigator
Course: CSI480 (Artificial Intelligence)
Date: December 15, 2025
Description:
    A Campus Navigator using the A* algorithm to search for the shortest
    path from the user's current location to their desired destination.
"""

import math
import heapq
from campus_map import levels, graph

# Convert all keys in graph to lowercase for case-insensitive matching
graph = {
    k.lower(): {n.lower(): c for n, c in v.items()}
    for k, v in graph.items()
}


def get_start_location(building):
    """
    Prompt the user for their starting level and location.
    Returns a dictionary with name and coordinates, or None if invalid.
    """
    while True:
        start_level = input(
            "Please type in your current level (ex: LL, 1, 2, ...): "
        ).lower()

        if start_level in {"ll", "lower level"}:
            start_level = "0"

        if start_level in building:
            print("Locations on this level:")
            for location in building[start_level]:
                print("-", location)

            start_location = input(
                "Please type in the area/room that is closest to you: "
            ).lower().replace(" ", "")

            for spot, coordinates in building[start_level].items():
                if start_location in spot.lower():
                    return {
                        "name": spot.lower(),
                        "coordinates": coordinates,
                    }

        print("This location is inaccessible.")


def get_destination(building):
    """
    Prompt the user for their destination.
    Returns a dictionary with name and coordinates, or None if invalid.
    """
    while True:
        print("Where do you want to go?")
        destination_name = (
            input(
                "Please enter the room number or area "
                "(ex: room 310, library, bookstore, ...): "
            )
            .lower()
            .replace(" ", "")
        )
        for level in building.values():
            for spot, coordinates in level.items():
                if destination_name in spot.lower().replace(" ", ""):
                    return {
                        "name": spot.lower(),
                        "coordinates": coordinates,
                    }

        print("This location is inaccessible.")


def heuristics(start_node, goal_node, building):
    """
    Calculate heuristic distances from nodes to the goal.
    Returns a dictionary mapping spot_name to estimated_distance.
    """
    estimated_distances = {}

    _, _, start_z = start_node["coordinates"]
    end_x, end_y, end_z = goal_node["coordinates"]

    for level in building.values():
        for spot, coordinates in level.items():
            if coordinates == goal_node["coordinates"]:
                estimated_distances.update({spot.lower(): 0})
            else:
                curr_x, curr_y, curr_z = coordinates

                delta_x = abs(curr_x - end_x)
                delta_y = abs(curr_y - end_y)
                delta_z = abs(curr_z - end_z)

                distance = math.sqrt(
                    delta_x ** 2 + delta_y ** 2 + delta_z ** 2
                )
                estimated_distances.update({spot.lower(): distance})

    return estimated_distances


def a_star_algorithm(start_node, goal_node, h_vals, graph_data):
    """
    Perform the A* search algorithm.
    Returns the shortest path as a list of node names.
    """
    # Priority queue of nodes to explore
    available_nodes = []

    # Set of visited nodes
    checked_nodes = set()

    heapq.heappush(
            available_nodes, 
            (h_vals[start_node["name"]], start_node["name"]))
    

    g_vals = {start_node["name"]: 0}
    f_vals = {start_node["name"]: h_vals[start_node["name"]]}
    came_from = {}


    while available_nodes:
        # string 'current_node' is the name of the node in 'available_nodes' with the lowest 'cost_to_goal'
        _, current_node = heapq.heappop(available_nodes)

        print("Visiting:", current_node) # debug

        if current_node == goal_node["name"]:
            path = []
            while current_node in came_from:
                path.append(current_node)
                current_node = came_from[current_node]
            path.append(start_node["name"])
            return path[::-1]
        
        if current_node in checked_nodes:
            continue # skip already checked nodes

        checked_nodes.add(current_node)

        for neighbor_node, cost in graph_data.get(current_node, {}).items():
            print("Neighbor:", neighbor_node, "cost:", cost)
            if neighbor_node in checked_nodes:
                continue # skip already checked nodes

            tentative_g = g_vals[current_node] + cost

            if (
                neighbor_node not in g_vals
                or tentative_g < g_vals[neighbor_node]
            ):
                g_vals[neighbor_node] = tentative_g
                f_vals[neighbor_node] = tentative_g + h_vals[neighbor_node]
                came_from[neighbor_node] = current_node
                heapq.heappush(available_nodes, (f_vals[neighbor_node], neighbor_node))
                
    return None  # No path found

start = get_start_location(levels)
goal = get_destination(levels)

print("From: ", start["name"])
print("To: ", goal["name"])

estimated_distances_from_goal = heuristics(start, goal, levels)

# test heuristics function
print("h(start):", estimated_distances_from_goal[start["name"]])
print("h(goal):", estimated_distances_from_goal[goal["name"]])

print(a_star_algorithm(start, goal, estimated_distances_from_goal, graph))







