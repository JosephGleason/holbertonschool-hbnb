# HBnB - Part 2: Business Logic and API

Welcome to the backend engine of the HBnB app.

This phase focuses on building the Business Logic Layer and RESTful API Endpoints using Flask and Flask-RESTx. The goal is to implement core functionality like managing users, places, reviews, and amenities.

## Project Structure

```
hbnb/
├── app/
│   ├── api/              # RESTful API endpoints (v1/users, places, etc.)
│   ├── models/           # Core business logic classes (User, Place, etc.)
│   ├── services/         # Facade layer (connects API and models)
│   └── persistence/      # In-memory storage (acts like a fake database)
├── run.py                # Entry point to run the Flask app
├── config.py             # Config settings (e.g., debug mode)
├── requirements.txt      # Python dependencies
└── README.md             # Project overview (this file)
```

## Setup Instructions

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the application:

```bash
python3 run.py
```

3. Access the Swagger UI at:

```bash
http://localhost:5000/api/v1/
```

## YAML (Swagger Specification)

Flask-RESTx automatically generates Swagger-compliant API docs.

The OpenAPI YAML schema includes:
- Path operations (`/users/`, `/places/`, etc.)
- Parameter types and validations
- Response models and status codes

This documentation is viewable at:
```
http://localhost:5000/api/v1/
```

## Key Concepts

- **Flask**: Lightweight Python web framework used to build web apps and APIs.
- **Flask-RESTx**: Extension for Flask that helps build/document RESTful APIs.
- **Facade Pattern**: Simplifies communication between API and business logic.
- **In-memory Repository**: A fake database layer for temporary storage.
- **Modular Design**: Each part of the application (API, models, services) is separated into its own module for clarity and reusability.

---

## Business Logic Layer Overview

All entities inherit from a shared `BaseModel` class and are located in the `app/models/` directory.

### BaseModel

- `id`: String (UUID)
- `created_at`: datetime
- `updated_at`: datetime
- `save()`: updates `updated_at`
- `update(data_dict)`: bulk updates fields

### User

- `first_name`: string (max 50), required
- `last_name`: string (max 50), required
- `email`: string (must match email pattern), required
- `is_admin`: boolean (default: False)

### Place

- `title`: string (max 100), required
- `description`: string (optional)
- `price`: float, must be ≥ 0
- `latitude`: float, -90.0 ≤ x ≤ 90.0
- `longitude`: float, -180.0 ≤ x ≤ 180.0
- `owner`: User instance (required)
- `reviews`: list of Review instances
- `amenities`: list of Amenity instances

### Review

- `text`: string, required
- `rating`: integer (1–5), required
- `place`: Place instance, required
- `user`: User instance, required

### Amenity

- `name`: string (max 50), required

---

## Relationships

- **User → Place**: A user can own multiple places (1-to-many).
- **Place → Review**: A place can have multiple reviews.
- **Place → Amenity**: Many-to-many (stored as list references).

---

## Running Tests

Unit tests are in the `tests/` directory.

To run all tests:

```bash
PYTHONPATH=. python3 -m unittest discover tests/
```

Or individually:

```bash
PYTHONPATH=. python3 tests/test_user.py
PYTHONPATH=. python3 tests/test_place.py
PYTHONPATH=. python3 tests/test_amenity.py
PYTHONPATH=. python3 tests/test_endpoints.py
```

---

## Example Manual Tests with cURL

### Create a User
```bash
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Alice", "last_name": "Walker", "email": "alice@example.com"}'
```

### Get All Users
```bash
curl http://127.0.0.1:5000/api/v1/users/
```

### Update User
```bash
curl -X PUT http://127.0.0.1:5000/api/v1/users/<user_id> \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Updated", "last_name": "Name", "email": "updated@example.com"}'
```

---

## Manual Validation Guide

For manual QA reviewers:

- All endpoints return `200`, `201`, `400`, or `404` with proper JSON responses
- Swagger UI (`/api/v1/`) loads all resources and documents input/output clearly
- POST validation errors produce informative messages (e.g., missing fields, bad email)
- All relationships are nested correctly (e.g., `place.reviews`, `place.amenities`)
- DELETE is implemented only for `/reviews/<id>`

---

## Author

Written by:

**Joseph Gleason**  
Holberton School
```
