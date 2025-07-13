# HBnB API Testing Report

## Overview

This document captures the results of testing the RESTful API endpoints for the HBnB project. It includes both model-level validation tests and black-box API tests using `curl`. All tests check for correct responses, validation enforcement, and edge case handling.

---

## User Endpoint Tests

### Valid User Creation

```bash
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Ana", "last_name": "Gomez", "email": "ana@example.com"}'
```

**Expected Status:** `201 Created`

---

### Invalid User Creation

```bash
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name": "", "last_name": "", "email": "invalid-email"}'
```

**Expected Status:** `400 Bad Request`

---

## Amenity Endpoint Tests

### Valid Amenity Creation

```bash
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Wi-Fi"}'
```

**Expected Status:** `201 Created`

---

### Invalid Amenity Creation (Empty Name)

```bash
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": ""}'
```

**Expected Status:** `400 Bad Request`

---

## Place Endpoint Tests

### Valid Place Creation

```bash
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Ocean View Suite",
    "description": "A cozy room by the beach.",
    "price": 150.0,
    "latitude": 18.4655,
    "longitude": -66.1057,
    "owner_id": "VALID_USER_ID",
    "amenities": ["VALID_AMENITY_ID"]
  }'
```

**Expected Status:** `201 Created`

---

### Invalid Place Creation (Bad Latitude and Price)

```bash
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "",
    "description": "Missing title and invalid lat/lon",
    "price": -5,
    "latitude": 999,
    "longitude": -999,
    "owner_id": "INVALID_ID",
    "amenities": []
  }'
```

**Expected Status:** `400 Bad Request`

---

## Review Endpoint Tests

### Valid Review Creation

```bash
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Nice place!",
    "rating": 5,
    "user_id": "VALID_USER_ID",
    "place_id": "VALID_PLACE_ID"
  }'
```

**Expected Status:** `201 Created`

---

### Invalid Review Creation (Empty Text)

```bash
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "",
    "rating": 6,
    "user_id": "INVALID_ID",
    "place_id": "INVALID_ID"
  }'
```

**Expected Status:** `400 Bad Request`

---

## Swagger Documentation

Swagger documentation is accessible at:

```
http://127.0.0.1:5000/api/v1/
```

- All endpoints are registered under their respective namespaces.
- Models show accurate schemas and validation rules.
- Interactive testing via Swagger UI is available.

---

## Summary

| Component | Manual Validation | Automated Test | Swagger Verified |
|----------|--------------------|----------------|------------------|
| User     | Yes                | Pending        | Yes              |
| Amenity  | Yes                | Pending        | Yes              |
| Place    | Yes                | Pending        | Yes              |
| Review   | Yes                | Pending        | Yes              |

---

To complete Task 6:
- Basic validation is implemented in all models.
- Manual testing with curl is complete and passed.
- Swagger UI reflects accurate endpoint schemas.
- Next step: write automated `unittest` scripts for each endpoint.
