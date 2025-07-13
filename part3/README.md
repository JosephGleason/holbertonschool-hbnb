# HBnB - Part 3: API, Authentication & SQLAlchemy

## Overview

This is Part 3 of the HBnB project, extending the RESTful API with secure authentication, admin authorization, and SQLAlchemy-based persistence. The goal is to move from in-memory data to a robust database-backed backend with complete access control.

---
## Entity-Relationship Diagram

![ER Diagram](./diagrams/diagram.png)

## Features

-  JWT Authentication (`/api/v1/auth`)
-  Role-based access control (`is_admin`)
-  SQLAlchemy models with database persistence
-  RESTful CRUD routes for:
  - Users
  - Places
  - Amenities
  - Reviews
-  Admin bootstrap on startup
-  SQLite for development, MySQL-ready for production
-  ER diagram visualization with Mermaid.js

---

## Project Structure

<details>
<summary><strong>Click to expand project layout</strong></summary>

```plaintext
part3/
├── app/
│   ├── __init__.py
│   ├── models/
│   ├── api/
│   └── services/
├── sql/
│   ├── schema.sql
│   └── data.sql
├── diagrams/
│   └── er_diagram.png
├── test.db
├── README.md
└── ...
```
</details> 

---

## Authentication & Authorization

- `POST /api/v1/auth/login`: returns JWT access token
- Users can:
  - Access and modify their own data
  - Review others' places (1 review max per place)
- Admins can:
  - Create/update/delete any user, place, or review

---

## Tech Stack

- **Flask**
- **SQLAlchemy**
- **Flask-JWT-Extended**
- **Flask-Bcrypt**
- **Flask-RESTx**
- **SQLite / MySQL**
- **Mermaid.js**

---

## Testing & Usage

### Run the Flask App

```bash
flask run
```

### Launch the Flask Shell

```bash
flask shell
```

### Inspect the SQLite Database

```bash
sqlite3 test.db
```

Inside the SQLite prompt, you can run SQL commands like:

```sql
SELECT * FROM users;
SELECT * FROM places;
```

### Recreate Database from SQL Files

```bash
sqlite3 test.db < sql/schema.sql
sqlite3 test.db < sql/data.sql
```


## Initial Admin User
Auto-created on startup if not present:

makefile
Copy
Edit
Email:    admin@hbnb.com
Password: admin123
ER Diagram

## SQL Schema + Seed
All tables and initial data can be recreated manually:

bash
Copy
Edit
sqlite3 test.db < schema.sql
sqlite3 test.db < data.sql

---
## Author

Written by:

**Joseph Gleason**  
Holberton School
```