# File: campus_map.py
# Name: Campus Navigator 
# Course: CSI480 (Artificial Intelligence)
# Date: December 15, 2025
# Description: A Campus Navigator using A-Star algorithm
#              to search for the shortest path from user's
#              current location to their desired destination.

# (x, y, z) where z = floor level
building_floors = {
    # Main Floor/ Floor 1
    "EntranceMain": (0, 0, 1),
    "EntranceNorth": (13, -2, 1),
    "EntranceSouth": (-13, -3, 1),
    "WelcomeCenter": (-1, 1, 1),

    "HallwayMainF1": (0, -3, 1),
    "HallwayNorthF1": (5, -3, 1),
    "HallwaySouthF1": (-5, -3, 1),

    "ElevatorNorthF1": (6, -4, 1),
    "ElevatorSouthF1": (-5, -2, 1),

    "StairsNorthF1": (7, -4, 1),
    "StairsWestF1": (-1, -1, 1),

    # Floor 3
    "ElevatorNorthF3": (6, -4, 3),
    "StairsNorthF3": (7, -4, 3),

    "Hallway1F3": (5, -3, 3),
    "StudentLounge": (5, -2, 3),
    "StudentWellness": (3, -3, 3),
    "Bookstore": (6, -5, 3),
    "VeteransAffairs": (5, -5, 3),
    "TutoringCenter": (4, -4, 3),
    "StudentAccessibility": (3, -3, 3),
    "AthleticsOffice": (4, -3, 3),
    "Security": (2, -3, 3),

    "RestroomsF3": (7, -3, 3),
    "Library": (9, -3, 3),

    "Room304": (7, -1, 3),
    "Room307": (8, -1, 3),
    "Room308": (9, -1, 3),
    "Room309": (10, -1, 3),
    "Room310": (11, -1, 3),
    "Room311": (12, -1, 3),
    "Room312": (13, -1, 3),
    "Room313": (13, -2, 3),
    "Room315": (14, -2, 3),
    "Room318": (13, -3, 3),
    "Room319": (14, -3, 3),
    "Room320": (12, -3, 3),
}


# Navigation graph
# Cost = average travel time in seconds

graph = {
    "EntranceMain": {"WelcomeCenter": 2, "HallwayMainF1": 3},
    "EntranceNorth": {"HallwayNorthF1": 10},
    "EntranceSouth": {"HallwaySouthF1": 10},

    "WelcomeCenter": {"EntranceMain": 2, "HallwayMainF1": 1},

    "HallwayMainF1": {
        "HallwayNorthF1": 6,
        "EntranceMain": 3,
        "WelcomeCenter": 1,
        "HallwaySouthF1": 5
    },

    "HallwayNorthF1": {
        "ElevatorNorthF1": 1,
        "StairsNorthF1": 2,
        "EntranceNorth": 10,
        "HallwayMainF1": 6
    },

    "HallwaySouthF1": {
        "ElevatorSouthF1": 1,
        "EntranceSouth": 10,
        "HallwayMainF1": 5
    },

    "ElevatorSouthF1": {"HallwaySouthF1": 1},

    "ElevatorNorthF1": {
        "ElevatorNorthF3": 8,
        "HallwayNorthF1": 1
    },

    "ElevatorNorthF3": {
        "ElevatorNorthF1": 8,
        "Hallway1F3": 1,
        "Bookstore": 2,
        "RestroomsF3": 1
    },

    "StairsNorthF1": {"StairsNorthF3": 14, "HallwayNorthF1": 2},
    "StairsNorthF3": {"StairsNorthF1": 14, "RestroomsF3": 1},

    "Bookstore": {"VeteransAffairs": 1, "ElevatorNorthF3": 2},
    "VeteransAffairs": {"TutoringCenter": 1, "Bookstore": 1},
    "TutoringCenter": {"VeteransAffairs": 1, "StudentAccessibility": 2},
    "StudentAccessibility": {"TutoringCenter": 2, "AthleticsOffice": 1},
    "AthleticsOffice": {"StudentAccessibility": 1},

    "Hallway1F3": {
        "StudentLounge": 1,
        "StudentWellness": 1,
        "RestroomsF3": 1,
        "Library": 3,
        "ElevatorNorthF3": 1
    },

    "RestroomsF3": {
        "Hallway1F3": 1,
        "Library": 3,
        "ElevatorNorthF3": 1,
        "StairsNorthF3": 1
    },

    "StudentLounge": {"Hallway1F3": 1, "StudentWellness": 1, "Security": 2},
    "StudentWellness": {"Security": 1, "Hallway1F3": 1, "StudentLounge": 1},
    "Security": {"StudentWellness": 1, "StudentLounge": 2},

    "Library": {"Hallway1F3": 3, "Room307": 2, "RestroomsF3": 3},

    "Room304": {"Room307": 1},
    "Room307": {"Library": 2, "Room304": 1, "Room308": 1},
    "Room308": {"Room307": 1, "Room309": 1},
    "Room309": {"Room308": 1, "Room310": 1},
    "Room310": {"Room309": 1, "Room311": 1},
    "Room311": {"Room310": 1, "Room312": 1},
    "Room312": {"Room311": 1, "Room313": 1},
    "Room313": {"Room312": 1, "Room315": 1},
    "Room315": {"Room313": 1, "Room318": 1},
    "Room318": {"Room315": 1, "Room319": 1},
    "Room319": {"Room318": 1, "Room320": 1},
    "Room320": {"Room319": 1}
}