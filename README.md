# Campus-Navigator

A web application that helps students navigate through campus buildings by searching locations and showing routes on an interactive map.

## API Contract (V1)

This section defines the backend API contract for the Flask service.
The contract is the agreement between frontend and backend:
- The frontend agrees to send requests in this format.
- The backend agrees to return responses in this format.

If both sides follow this contract, integration is predictable and easier to debug.

### Core Rules

- All request and response bodies use JSON.
- All keys use `camelCase`.
- Location matching is case-insensitive.
- Every error response uses the same error shape.

### Base URL

Use this for local development:

```text
http://localhost:5000
```

In production, replace this with the deployed backend URL.

### Endpoint: `GET /health`

Purpose: quick check that the Flask server is running.

#### Success Response (`200`)

```json
{
	"status": "ok",
	"service": "campus-navigator-api"
}
```

### Endpoint: `GET /locations`

Purpose: return all known locations that can be used for `origin` and `destination`.

#### Success Response (`200`)

```json
{
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
}
```

### Endpoint: `POST /route`

Purpose: compute a route between two valid locations.

#### Request Body

```json
{
	"origin": "Welcome Center",
	"destination": "Room 310",
	"accessibilityMode": "avoid_stairs"
}
```

#### Request Field Rules

- `origin` (string, required): user start location.
- `destination` (string, required): user destination.
- `accessibilityMode` (string, optional):
	- `standard` (default)
	- `avoid_stairs`
	- `prefer_elevator`

#### Success Response (`200`)

```json
{
	"origin": "WelcomeCenter",
	"destination": "Room310",
	"accessibilityMode": "avoid_stairs",
	"pathNodes": [
		"WelcomeCenter",
		"HallwayMainF1",
		"HallwayNorthF1",
		"ElevatorNorthF1",
		"ElevatorNorthF3",
		"Hallway1F3",
		"Library",
		"Room307",
		"Room308",
		"Room309",
		"Room310"
	],
	"steps": [
		"Start at Welcome Center.",
		"Walk to Hallway Main (Floor 1).",
		"Take Elevator North to Floor 3.",
		"Pass the Library and continue to Room 310."
	],
	"floorsUsed": [1, 3],
	"estimatedTimeSeconds": 42
}
```

#### Error Responses

##### Invalid Request (`400`)

```json
{
	"error": {
		"code": "INVALID_REQUEST",
		"message": "origin and destination are required string fields"
	}
}
```

##### Unknown Location (`404`)

```json
{
	"error": {
		"code": "LOCATION_NOT_FOUND",
		"message": "Destination 'Room 999' was not found"
	}
}
```

##### No Route (`422`)

```json
{
	"error": {
		"code": "ROUTE_NOT_FOUND",
		"message": "No route exists between the selected locations"
	}
}
```

##### Server Error (`500`)

```json
{
	"error": {
		"code": "INTERNAL_ERROR",
		"message": "Unexpected server error"
	}
}
```

### cURL Examples

Health check:

```bash
curl -X GET http://localhost:5000/health
```

Fetch locations:

```bash
curl -X GET http://localhost:5000/locations
```

Compute route:

```bash
curl -X POST http://localhost:5000/route \
	-H "Content-Type: application/json" \
	-d '{
		"origin": "Welcome Center",
		"destination": "Room 310",
		"accessibilityMode": "avoid_stairs"
	}'
```

### Flask Terms (Beginner Quick Notes)

- Endpoint: a URL path like `/route` that Flask handles.
- HTTP method: action type (`GET` reads data, `POST` sends data to process).
- Status code: numeric result (`200` success, `400` bad request, etc.).
- JSON: text format used for request and response data.