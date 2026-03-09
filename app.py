from flask import Flask, request, jsonify

app = Flask(__name__)

#NOTE: will need to understand how this endpoint even plays in the wider project; will it just check if the Flask server is running? or can it also be used to check other things?
@app.route('/health', methods=["GET"])
def get_health():
   health_dict = {
      "status": "ok",
      "service": "campus-navigator-api"
   }

   return jsonify(health_dict), 200

@app.route('/locations', methods=["GET"])
def get_locations():
   locations_dict = {

   }


   return jsonify(locations_dict), 200

@app.route('/route', methods=["POST"])
def find_route():
   # convert incoming JSON request to Python dict
   data = request.get_json()

   origin = data.get("origin")
   destination = data.get("destination")

   if not origin or not destination:
      return jsonify({"error": { "code": "INVALID_REQUEST", "message": "origin or destination missing"}}), 400

   path = compute_path(origin, destination)

   # NOTE: should verify if returning origin and destination is really required.
   # on one hand, it's redundant, on the other, it could make the response page on the frontend a bit easier to write? like if backend response contains origin and destination, then the frontend can just display these variables rather than porting over the user's text box responses?
   return jsonify({"origin": origin, "destination": destination, "pathNodes": path}), 200


# A* algorithm from `main.py` to calculate shortest route between two locations
def compute_path(origin, destination):

   return ["shortest", "path", "from", "origin", "to", "destination"]



if __name__ == '__main__':
   app.run()