# HBnB - Part 4: Front-End Web Client

This is Part 4 of the HBnB project: a simple, single-page web client that interacts with a RESTful backend API (built in Part 3) to allow users to browse and review rental places.

## Project Structure

holbertonschool-hbnb/
├── backend/                   # All files from Part 3 (Flask API + Models)
│   └── ...
├── frontend/                  # New files for Part 4
│   ├── base_files/
│   │   ├── login.html
│   │   ├── place.html
│   │   ├── scripts.js
│   │   └── styles.css
│   ├── images/
│   │   └── logo.png
│   ├── index.html
│   └── utils/
│       └── auth.js            # (optional helper for JWT cookies)
├── README.md
└── requirements.txt

## Features

- Single Page Client for HBnB rentals
- JWT Authentication with Login form
- Fetch & Display Places using GET /places
- Authenticated Reviews for logged-in users
- Google Maps integration (optional)
- Token stored in cookies for persistence

## Technologies

- HTML5
- CSS3
- JavaScript (ES6+)
- Fetch API
- JWT Authentication
- Flask (Back-end from Part 3)

## Pages

- index.html – Homepage displaying all places.
- login.html – Simple login form with email/password.
- place.html – Dynamic page for a single place with reviews.

## Authentication Flow

1. User logs in via login.html
2. On success, JWT is returned and saved to cookies.
3. Protected routes (e.g., adding a review) use the token in the Authorization header.
4. User remains logged in across page loads.

## API Endpoints (Consumed)

| Method | Endpoint                     | Description                    |
|--------|------------------------------|--------------------------------|
| POST   | /api/v1/auth/login           | Authenticate user              |
| GET    | /api/v1/places               | Fetch all places               |
| GET    | /api/v1/places/:id           | Get place details              |
| GET    | /api/v1/places/:id/reviews   | Get all reviews for place      |
| POST   | /api/v1/reviews              | Add a new review (auth req)    |

## Testing

You can test the web client with any modern browser. Make sure the Flask back-end server is running at:

http://127.0.0.1:5000/

To test login:

curl -X POST http://127.0.0.1:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@hbnb.com", "password": "admin123"}'

Use the token in the browser's cookies (or inspect via DevTools).

## To-Do Checklist

- [x] Build basic HTML structure
- [x] Implement JWT login flow
- [x] Fetch & render places dynamically
- [x] Render reviews
- [x] Add review (authenticated)
- [ ] Add user logout (optional)
- [ ] Google Maps view (optional)

## Sample Screenshot

images/sample-screenshot.png

## Tips

- Use document.cookie to manage JWT tokens.
- Always check for token presence before making POST requests.
- Keep all dynamic rendering inside scripts.js using DOM APIs.
- Use DOMContentLoaded to initialize events.

## Author

- Joseph Gleason
- Holberton School

## License

MIT License
