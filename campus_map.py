# File: floor.py
# Name: Campus Navigator 
# Course: CSI480 (Artificial Intelligence)
# Date: December 15, 2025
# Description: A Campus Navigator using A-Star algorithm
#              to search for the shortest path from user's
#              current location to their desired destination.


level_lower = {
    
}

# Completed level 1
level_1 = {
    "EntranceMain" : (0,0,1), #(x,y,z where z is the floor level)
    "EntranceNorth" : (13,-2,1),
    "EntranceSouth" : (-13,-3,1),
    "WelcomeCenter" : (-1,1,1),
    "HallwayMainF1" : (0,-3,1),
    "HallwayNorthF1" : (5,-3,1),
    "HallwaySouthF1" : (-5,-3,1),
    "ElevatorNorthF1" : (6,-4,1),
    "ElevatorSouthF1" : (-5,-2,1),
    "StairsNorthF1" : (7,-4,1),
    "StairsWestF1" : (-1,-1,1)
}

# Completed level 3
level_3 = {
    "ElevatorNorthF3" : (6,-4,3),
    "StairsNorthF3" : (7,-4,3),
    "Hallway1F3" : (5,-3,3),
    "StudentLounge" : (5,-2,3),
    "StudentWellness" : (3,-3,3),
    "Bookstore" : (6,-5,3),
    "VeteransAffairs" : (5,-5,3),
    "TutoringCenter" : (4,-4,3),
    "StudentAccessibility" : (3,-3,3),
    "AthleticsOffice" : (4,-3,3),
    "Security" : (2,-3,3),
    "RestroomsF3" : (7,-3,3),
    "Library" : (9,-3,3),
    "Room304" : (7,-1,3),
    "Room307" : (8,-1,3),
    "Room308" : (9,-1,3),
    "Room309" : (10,-1,3),
    "Room310" : (11,-1,3),
    "Room311" : (12,-1,3),
    "Room312" : (13,-1,3),
    "Room313" : (13,-2,3),
    "Room315" : (14,-2,3),
    "Room319" : (14,-3,3),
    "Room318" : (13,-3,3),
    "Room320" : (12,-3,3)
}

level_4 = {
#     "ElevatorNorthF4" : (6,-4,4),
#     "StairsNorthF4" : (7,-4,4),
#     "Room423" : (5,-5,4),
#     "Restrooms" : (7,-3,4),
#     "Hallway1F4" : (6,-3,4),
#     "Hallway2F4" : (8,-3,4),
#     "Room421" : (8,-4,4),
#     "Room402" : (8,-2,4),
#     "Room403" : (8,-1,4),
#     "Room404" : (9,-1,4),
#     "Room405" : (9,-2,4),
#     "Room420" : (9,-4,4),
#     "Hallway3F4" : ()
#     "Room419" : (9,-5,4),
#     "Room418" : (10,-5,4),
#     "Room" 
}

levels = {
    "0": level_lower,
    "1" : level_1,
    "3" : level_3,
    "4" : level_4
}

graph = {
    # the cost is the average time it takes from 1 location to another in seconds.
    "EntranceMain": {"WelcomeCenter": 2, "HallwayMainF1": 3},
    "EntranceNorth": {"HallwayNorthF1": 10},
    "EntranceSouth": {"HallwaySouthF1": 10},
    "WelcomeCenter": {"EntranceMain": 2, "HallwayMainF1": 1},
    "HallwayMainF1": {"HallwayNorthF1": 6, "EntranceMain": 3, "WelcomeCenter": 1, "HallwaySouthF1": 5},
    "HallwayNorthF1": {"ElevatorNorthF1": 1, "StairsNorthF1": 2, "EntranceNorth": 10, "HallwayMainF1": 6},
    "HallwaySouthF1": {"ElevatorSouthF1": 1, "EntranceSouth": 10, "HallwayMainF1": 5},
    "ElevatorSouthF1": {"HallwaySouthF1": 1},
    "ElevatorNorthF1": {"ElevatorNorthF3": 8, "HallwayNorthF1": 1},
    "ElevatorNorthF3": {"ElevatorNorthF1": 8, "Hallway1F3": 1, "Bookstore": 2, "RestroomsF3": 1},
    "StairsNorthF1": {"StairsNorthF3": 14, "HallwayNorthF1": 2},
    "StairsNorthF3": {"StairsNorthF1": 14, "RestroomsF3": 1},
    "Bookstore": {"VeteransAffairs": 1, "ElevatorNorthF3": 2},
    "VeteransAffairs": {"TutoringCenter": 1, "Bookstore": 1},
    "TutoringCenter": {"VeteransAffairs": 1, "StudentAccessibility": 2},
    "StudentAccessibility": {"TutoringCenter": 2, "AthleticsOffice": 1},
    "AthleticsOffice": {"StudentAccessibility": 1},
    "Hallway1F3": {"StudentLounge": 1, "StudentWellness": 1, "RestroomsF3": 1, "Library": 3, "ElevatorNorthF3": 1}, 
    "RestroomsF3": {"Hallway1F3": 1, "Library": 3, "ElevatorNorthF3": 1, "StairsNorthF3": 1},
    "StudentLounge": {"Hallway1F3": 1, "StudentWellness": 1, "Security": 2},
    "StudentWellness": {"Security": 1, "Hallway1F3": 1, "StudentLounge": 1},
    "Library": {"Hallway1F3": 3, "Room307": 2, "RestroomsF3": 3},
    "Security": {"StudentWellness": 1, "StudentLounge": 2},
    "Room304": {"Room307": 1},
    "Room307": {"Library":2, "Room304": 1, "Room308": 1},
    "Room308": {"Room307": 1, "Room309": 1},
    "Room309": {"Room308":1, "Room310": 1},
    "Room310": {"Room309":1, "Room311": 1},
    "Room311": {"Room310":1, "Room312": 1},
    "Room312": {"Room311":1, "Room313": 1},
    "Room313": {"Room312":1, "Room315": 1},
    "Room315": {"Room313":1, "Room318": 1},
    "Room318": {"Room315":1, "Room319": 1},
    "Room319": {"Room318": 1, "Room320": 1},
    "Room320": {"Room319": 1}
    

}