#!/usr/bin/python3

from app.models.base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()  # gives id and timestamps
        
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Amenity name must be a non-empty string")
        if len(name) > 50:
            raise ValueError("Amenity name must be at most 50 characters")
        
        self.name = name.strip()
