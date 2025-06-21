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

## Author

Written by:

Joseph Gleason  
Holberton School  
