#!/usr/bin/python3
"""Review model: Stores user feedback about places"""

from app import db
from app.models.base_model import BaseModel
from sqlalchemy.orm import validates

class Review(BaseModel):
    """Defines a Review left by a User on a Place"""

    __tablename__ = 'reviews'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)


    # Validate review text
    @validates('text')
    def validate_text(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Review text must be a non-empty string")
        return value.strip()

    # Validate rating
    @validates('rating')
    def validate_rating(self, key, value):
        if not isinstance(value, int) or not (1 <= value <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")
        return value
