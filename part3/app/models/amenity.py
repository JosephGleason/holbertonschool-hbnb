#!/usr/bin/python3

from app import db
from app.models.base_model import BaseModel
from sqlalchemy.orm import validates

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)

    @validates('name')
    def validate_name(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Amenity name must be a non-empty string")
        if len(value.strip()) > 50:
            raise ValueError("Amenity name must be at most 50 characters")
        return value.strip()
