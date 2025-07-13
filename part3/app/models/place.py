#!/usr/bin/python3

from app.models.base_model import BaseModel

class Place(BaseModel):
    def __init__(self, title, description=None, price=0.0,
                 latitude=0.0, longitude=0.0, owner=None):
        super().__init__() #calls the constructor of the parent class
        
        #validate title
        if not title or len(title) > 100: #check if empty or None
            raise ValueError("title is required and must be at most 100 characters")
        self.title = title
        
        #if a description was passed and is not empty use it
        self.description = description if description else ""
         
        #validate price
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("price must be a positive number")
        self.price = float(price)
        
        #validtate latitude
        if not isinstance(latitude, (int, float)) or not -90.0 <= latitude <= 90.0:
            raise ValueError("latitude must be between -90.0 and 90.0")
        self.latitude = float(latitude)
        
        #validate longitude
        if not isinstance(longitude, (int, float)) or not -180.0 <= longitude <= 180.0:
            raise ValueError("longitude must be between -180.0 and 180.0")
        self.longitude = float(longitude)

        #validate owner
        if not owner or not hasattr(owner, 'id'): #catches if no owner was passed in or that has id attrib
            raise ValueError("owner must be a valid User instance with an id")
        self.owner = owner

        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        """Add a review to this place"""
        from app.models.review import Review
        if not isinstance(review, Review):
            raise ValueError("Expected a Review")
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to this place"""
        from app.models.amenity import Amenity
        if not isinstance(amenity, Amenity):
            raise ValueError("Expected an Amenity")
        self.amenities.append(amenity)
