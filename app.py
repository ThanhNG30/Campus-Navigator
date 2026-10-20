from flask import Flask, jsonify, request
from main import a_star_algorithm, building_floors, graph, heuristics

app = Flask(__name__)

#NOTE: will need to understand how this endpoint even plays in the wider project; will it just check if the Flask server is running? or can it also be used to check other things?
@app.route('/health', methods=["GET"])
def get_health():
   health_dict = {
      "status": "ok",
      "service": "campus-navigator-api"
   }

   return jsonify(health_dict), 200

# returns all valid locations to be used for origin and destination
@app.route('/locations', methods=["GET"])
def get_locations():
   # LEARN: dict -> list -> dict is a bit redundant, but it allows us to easily add additional metadata (e.g., {"locations": [...], "total_count": 2, "last_updated": "2026-05-01"})
   locations_dict = {
      "locations": [
         {
            "id": "welcomecenter",
            "label": "Welcome Center",
            "floor": 1,
            "aliases": ["welcome center"]
         },
         {
            "id": "library",
            "label": "Library",
            "floor": 3,
            "aliases": ["library"]
         }
      ]
      # NOTE: Consider adding metadata.
   }

   return jsonify(locations_dict), 200

@app.route('/route', methods=["POST"])
def find_route():
   # convert incoming JSON request to Python dict
   data = request.get_json()

   origin = data.get("origin")
   destination = data.get("destination")
   accessibility_mode = data.get("accessibilityMode", "standard")  # default to "standard" if not provided

   if not origin or not destination:
      return jsonify({"error": { "code": "INVALID_REQUEST", "message": "origin or destination missing"}}), 400

   path = compute_path(origin, destination, accessibility_mode)

   # NOTE: should verify if returning origin and destination is really required.
   # on one hand, it's redundant, on the other, it could make the response page on the frontend a bit easier to write? like if backend response contains origin and destination, then the frontend can just display these variables rather than porting over the user's text box responses?
   # RESOLUTION: it's actually useful. If the frontend makes a request but the user navigates away or changes the UI when the response finally arrives, the frontend does not need to "remember" the original request. The backend response will already contain all necessary information to display the path and render the result.
   return jsonify({"origin": origin, "destination": destination, "accessibilityMode": accessibility_mode, "pathNodes": path}), 200

# A* algorithm from `main.py` to calculate shortest route between two locations
def compute_path(origin, destination, accessibility_mode):
   a_star_algorithm()
   return ["shortest", "path", "from", "origin", "to", "destination"]

if __name__ == '__main__':
   app.run()