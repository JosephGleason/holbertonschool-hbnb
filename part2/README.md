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

```
pip install -r requirements.txt
```

2. Run the application:

```
python3 run.py
```

3. Access the Swagger UI at:

```
http://localhost:5000/api/v1/
```

Note: At this stage, no routes are functional yet. Swagger UI will load but show no endpoints.

## Key Concepts

- Flask: A lightweight Python web framework used to build web applications and APIs.
- Flask-RESTx: An extension for Flask that helps build and document RESTful APIs with less effort.
- Facade Pattern: A design pattern used to simplify the communication between the API layer and the business logic.
- In-memory Repository: A temporary, fake data storage layer that simulates how a database will work in Part 3.
- Modular Design: Keeping each part of the application in its own separate module (API, logic, persistence, etc.).

---

## Business Logic Layer Overview

All entities inherit from a shared `BaseModel` class and are located in the `app/models/` directory.

### BaseModel

- `id`: String (UUID)
- `created_at`: datetime
- `updated_at`: datetime
- `save()`: updates the `updated_at` timestamp
- `update(data_dict)`: bulk updates attributes from a dictionary

### User

- `first_name`: string (max 50), required
- `last_name`: string (max 50), required
- `email`: string (must match email pattern), required
- `is_admin`: boolean (default: False)

### Place

- `title`: string (max 100), required
- `description`: string (optional)
- `price`: float, must be ≥ 0
- `latitude`: float, must be between -90.0 and 90.0
- `longitude`: float, must be between -180.0 and 180.0
- `owner`: User instance (required)
- `reviews`: list of Review instances
- `amenities`: list of Amenity instances

### Review

- `text`: string, required
- `rating`: integer (1 to 5), required
- `place`: Place instance, required
- `user`: User instance, required

### Amenity

- `name`: string (max 50), required

---

## Relationships

- **User → Place**: A user can own many places (one-to-many).
- **Place → Review**: A place can have many reviews (one-to-many).
- **Place → Amenity**: A place can have many amenities (many-to-many, simulated via list).

---

## Running Tests

Unit tests are located in the `tests/` directory.

To run tests, use:

```bash
PYTHONPATH=. python3 tests/test_user.py
PYTHONPATH=. python3 tests/test_place.py
PYTHONPATH=. python3 tests/test_review.py
PYTHONPATH=. python3 tests/test_amenity.py
```

---

## Author

Written by:

Joseph Gleason  
Holberton School  
