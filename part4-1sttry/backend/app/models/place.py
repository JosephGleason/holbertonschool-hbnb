#!/usr/bin/python3

from app import db
from app.models.base_model import BaseModel
from sqlalchemy.orm import validates

place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, default="")
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    #validates title
    @validates('title')
    def validate_title(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Title must be a non-empty string")
        return value.strip()
        
    #validate price, latitude, longitude
    @validates('price', 'latitude', 'longitude')
    def validate_floats(self, key, value):
        if not isinstance(value, (float, int)):
            raise ValueError(f"{key} must be a number")
        return float(value)

    reviews = db.relationship('Review', backref='place', lazy=True)

    amenities = db.relationship(
    'Amenity',
    secondary=place_amenity,
    lazy='subquery',
    backref=db.backref('places', lazy=True)
)
