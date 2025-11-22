# The Plan

Create a web app to plan routes between locations within the President's Place building, with a focus on Quincy College rooms (e.g., the Welcome Center, Library, classrooms, etc.).

## End Product

1. User presented with a model of the school when they visit the website.
2. They enter an origin and a destination point (e.g., `Welcome Center` to `Room 411`).
3. A route is drawn within the model that highlights the path the user should take to get from origin to destination (accounting for stairs and elevators).
4. Success

## Ideas

- Using floorplans, use Blender to create a relatively-accurate model of the building. Floors should be consistent with each other (i.e., the roof of the first level matches with the floor of the second level)
- Match points within the 3D model to a mapping graph (JSON file?) in order to find routes algorithmically (e.g., room entrance, bottom of staircase)
- Run A* search or Dijkstra's algorithm to find shortest path between nodes
- Host on a platform like Vercel? (frontend + backend)

## Technologies

- Blender
- Three.js to represent 3D model in browser