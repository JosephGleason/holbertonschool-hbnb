#!/usr/bin/python3
"""Review model: Stores user feedback about places"""

from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place

class Review(BaseModel):
    """Defines a Review left by a User on a Place"""

    def __init__(self, text, rating, place, user):
        super().__init__()  # Inherit id, created_at, updated_at

        # Validate review text
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Review text is required and must be a non-empty string")
        self.text = text

        # Validate rating
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")
        self.rating = rating

        # Validate place instance
        if not isinstance(place, Place):
            raise ValueError("place must be a valid Place instance")
        self.place = place

        # Validate user instance
        if not isinstance(user, User):
            raise ValueError("user must be a valid User instance")
        self.user = user
