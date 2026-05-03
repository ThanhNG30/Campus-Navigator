# Arjun's Working Notes

## Common HTTP Methods
*(should only need `GET` and `POST` for this project)*

| Method | Purpose | Has Body? | Safe?* | Example |
|--------|---------|-----------|--------|---------|
| **GET** | Read data | No | Yes | Get list of locations |
| **POST** | Create new data | Yes | No | Submit a new route request |
| **PUT** | Replace entire resource | Yes | No | Update location info |
| **DELETE** | Remove data | No | No | Delete a location |

*"Safe" = doesn't change server state*

### Examples for this project
- `GET /health` -> read server status (read-only)
- `GET /locations` -> read location list (read-only)
- `POST /route` -> process route request (creates a result)

---

## Flask

### Decorators (`@app.route`)
```python
@app.route('/health', methods=["GET"])
def get_health():
    ...
```

`@app.route` *registers* the function with Flask. Here...
- **Path** (`'/health'`) is the URL the user/frontend visits
- **Methods** (`["GET, POST"]`) define which HTTP actions are allowed
- **Functions** (`get_health()`) are the code that runs upon visiting the defined path

### Requsts vs Reponses

**Request:** what the client (frontend) sends to the server (backend)
**Response:** what the server (backend) sends back

---

## JSON

### What is JSON?

JSON = JavaScript Object Notation. It's a text format for sending structured data.

**JSON looks exactly like a Python dictionary:**

JSON:
```json
{
  "origin": "Welcome Center",
  "destination": "Room 310",
  "accessibilityMode": "avoid_stairs"
}
```
Python:
```python
{
    "origin": "Welcome Center",
    "destination": "Room 310",
    "accessibilityMode": "avoid_stairs"
}
```

The key difference is that JSON is *text sent over the internet* while Python dicts are *objects in memory*. They still use the same structure.

### JSON Processing Pipeline

#### Operation 1. Request — Parse incoming JSON
```python
from flask import request # <-- USING THE `flask.request` OBJECT, NOT `requests` LIBRARY

@app.route('/route', methods=["POST"])
def find_route():
    # convert: incoming JSON text -> Python dictionary
    data = request.get_json()
    
    # use it like a normal dict
    origin = data.get("origin")
    destination = data.get("destination")
```

**Flow:**
1. User sends JSON text: `{"origin": "Welcome Center", ...}` via frontend
2. `request.get_json()` converts it to a Python dict
3. We access it like a regular Python dictionary

#### Operation 2. Response — Create outgoing JSON
```python
from flask import jsonify

@app.route('/health', methods=["GET"])
def health():
    # Python dict
    response_data = {
        "status": "ok",
        "service": "campus-navigator-api"
    }
    
    # Convert: Python dict -> JSON text AND send back
    return jsonify(response_data)
```

**Flow:**
1. We create a Python dict
2. `jsonify()` converts it to JSON text
3. Flask sends it as response

**Why `jsonify()` instead of just returning the Python dict?**
- `jsonify()` creates response object
- sets the correct HTTP header `Content-Type: application/json`
- ensures proper JSON formatting

#### Operation 3. Status Codes
Examples:
```python
# Success (200 is default)
return jsonify({"status": "ok"}), 200

# Bad request (400)
return jsonify({"error": "Missing origin field"}), 400

# Not found (404)
return jsonify({"error": "Location not found"}), 404
```

#### Complete Example: Parsing & Responding
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/route', methods=["POST"])
def find_route():
    # STEP 1: Get incoming JSON and convert to dict
    data = request.get_json()
    
    # STEP 2: Extract fields
    origin = data.get("origin")
    destination = data.get("destination")
    
    # STEP 3: Validate (we'll do this next)
    if not origin or not destination:
        return jsonify({
            "error": {
                "code": "INVALID_REQUEST",
                "message": "origin and destination required"
            }
        }), 400
    
    # STEP 4: Process (algorithm goes here)
    path = compute_path(origin, destination)
    
    # STEP 5: Return as JSON
    return jsonify({
        "origin": origin,
        "destination": destination,
        "pathNodes": path
    }), 200
```

---