# Campus Navigator Dev Guide (V1)

## Mission
Deliver a polished, reliable, mobile-friendly indoor navigation web app for President's Place that new students can use immediately.

## V1 Non-Negotiables
- [ ] Searches origin and destination
- [ ] Draws route on interactive 3D model
- [ ] Generates landmark-rich text directions
- [ ] Supports floor transitions clearly
- [ ] Includes ADA option (avoid stairs / prefer elevators)
- [ ] Works on mobile without broken layout
- [ ] Frontend and backend fully integrated and deployed

## Scope Guardrails
- [ ] Building scope: President's Place only
- [ ] Route logic priority: reliability over edge-case completeness
- [ ] Visual quality: strong enough to impress leadership
- [ ] De-scope rule if timeline tight: simplify routing edge cases before reducing visual polish

## Project Roles
- [ ] Jess: frontend, 3D scene integration, graph data updates
- [ ] Arjun: Flask API, routing service, integration, deployment pipeline
- [ ] Shared: QA, demo prep, acceptance testing

## Baseline Review (current repo)
- [x] A* prototype exists in `main.py`
- [x] Initial graph data exists in `campus_map.py`
- [x] 3D model exists in Blender (per `PLAN.md`)
- [ ] Frontend integrates Flask route API contract

## Delivery Plan (next <2 months)

### Phase 1: Architecture Lock (Week 1)
- [ ] Freeze API contract
: `POST /route` request `{origin, destination, accessibilityMode}`
: response `{pathNodes, steps, floorsUsed, estimatedTimeSeconds}`
- [ ] Define canonical node naming convention (single source of truth)
- [ ] Split graph data into versioned JSON (`qc_campus/`)
- [ ] Confirm mapping between Blender objects and graph node IDs
- [ ] Decide host setup for live demo reliability (frontend + backend)

### Phase 2: Data Completeness and Routing Quality (Weeks 2-3)
- [ ] Reach near-complete destination coverage for President's Place
- [ ] Add metadata per node
: `floor`, `label`, `aliases`, `landmark`, `accessType`
- [ ] Add edge metadata
: `travelTime`, `isStairs`, `isElevator`, `isAccessible`
- [ ] Implement accessibility routing mode in algorithm
- [ ] Add validation script to catch disconnected nodes and broken references

### Phase 3: Backend Productization (Weeks 3-4)
- [ ] Convert A* from CLI flow to importable service module
- [ ] Build Flask endpoints
: `GET /locations`
: `POST /route`
: `GET /health`
- [ ] Add structured error handling for invalid locations and no-route cases
- [ ] Add unit tests for shortest path and accessibility preference behavior
- [ ] Add smoke test for API contract

### Phase 4: Frontend + 3D Integration (Weeks 4-6)
- [ ] Replace placeholder form with V1 UX
: origin/destination search, accessibility toggle, route summary card
- [ ] Load and display 3D model in browser (Three.js)
- [ ] Render selected path highlights with floor-aware visibility
- [ ] Show landmark-rich turn instructions synced to route segments
- [ ] Ensure mobile-first layout and touch interactions are stable

### Phase 5: Hardening + Demo Prep (Weeks 7-8)
- [ ] Run bug bash on real student tasks
: "Welcome Center -> Room X", "Library -> Classroom Y"
- [ ] Fix top navigation failures and unclear directions
- [ ] Improve performance and first-load experience
- [ ] Add fallback handling if backend is temporarily unavailable
- [ ] Prepare scripted live demo path + backup path

## Acceptance Gates (Definition of Done for V1)
- [ ] Gate 1: 90%+ of intended destinations return valid routes
- [ ] Gate 2: ADA mode avoids stairs where elevator route exists
- [ ] Gate 3: Route instructions include at least one landmark cue where available
- [ ] Gate 4: Mobile test passes on at least 2 devices
- [ ] Gate 5: Live hosted demo completes 3 scripted routes without intervention

## Risk Log and Mitigations
- [ ] Risk: node naming drift between model and graph
: mitigation: canonical ID spec + validation script
- [ ] Risk: 3D integration slows schedule
: mitigation: lock minimal route-visualization feature first, then polish
- [ ] Risk: incomplete graph coverage
: mitigation: destination coverage tracker and weekly completeness targets
- [ ] Risk: hosting/demo instability
: mitigation: pre-demo smoke checks and fallback demo path

## Immediate Next 7 Tasks
- [x] Write API contract in `README.md`
- [ ] Refactor `main.py` into reusable routing module
- [ ] Create Flask app skeleton with `/health`, `/locations`, `/route`
- [ ] Move map data into `qc_campus/` JSON with metadata fields
- [ ] Build graph validator script (connectivity + schema)
- [ ] Replace `index.html` placeholder with route input UI shell
- [ ] Wire frontend to call `/route` and display returned steps

## Review
- Added a practical, phased project guide based on your plan and interview responses.
- Prioritized reliability, mobile usability, ADA routing, and polished demo readiness.
- Converted high-level goals into checkable milestones, acceptance gates, and immediate next actions.