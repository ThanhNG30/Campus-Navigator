# The Plan

Create a web app to plan routes between locations within the President's Place building, with a focus on Quincy College rooms (e.g., the Welcome Center, Library, classrooms, etc.). First focus is President's Place, with potential to add Saville after. We should prioritize mobile usability.

## End Product

1. User visits website and is presented with a model of the school they can interact with along with a search bar to find locations and enter destinations.
2. They enter an origin and a destination point (e.g., `Welcome Center` to `Room 411`).
3. A route is drawn within the model that highlights the path the user should take to get from origin to destination (accounting for stairs/elevators) and directions are given.
4. Success :D

## Ideas

- Using floorplans, use Blender to create a relatively-accurate model of the building. Floors should be consistent with each other (i.e., the roof of the first level matches with the floor of the second level)
- Match points within the 3D model to a mapping graph (JSON file?) in order to find routes algorithmically (e.g., room entrance, bottom of staircase)
- Run A* search algorithm to find shortest path between nodes

## Technologies

- Blender
- Three.js to represent 3D model in browser
- Flask backend to serve model and handle routing requests
- Vercel for hosting frontend
- Heroku for hosting backend

## Current Progress

- Created accurate 3D model of President's Place in Blender
  - Separate objects for each floor and key locations (e.g., rooms, stairs, elevators) NOT yet created
- A* search algorithm implemented in Python that can find routes between nodes in a graph
  - algorithm at main.py
  - graph data structure at campus_map.py

## Members

Jessica - 3D model and database creation, frontend
Arjun - API (Flask), backend
Nick - 3D model